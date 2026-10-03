"""Signed Stripe billing with distinct product tier and billing interval."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict, model_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.app_logger import get_logger
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.services.subscription_catalog import PRICES, price_id, verified_price_tier
from app.services.subscription_service import apply_subscription_quotas

router = APIRouter(prefix="/api/billing", tags=["billing"])
logger = get_logger(__name__)
STRIPE_SUBSCRIPTION_STATUSES = {"active", "canceled", "incomplete", "incomplete_expired", "past_due", "paused", "trialing", "unpaid"}


def _stripe_client() -> None:
    stripe.api_key = settings.STRIPE_SECRET_KEY


def _sget(obj: object, key: str, default=None):
    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)


def _normalize_subscription_status(value: object, fallback: str = "none") -> str:
    return value if isinstance(value, str) and value in STRIPE_SUBSCRIPTION_STATUSES else fallback


class CheckoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tier: Literal["go", "plus"] = "plus"
    interval: Literal["monthly", "yearly"] | None = None
    # Backward-compatible old clients select the legacy Plus product.
    plan: Literal["monthly", "yearly"] | None = None

    @model_validator(mode="after")
    def select_interval(self):
        if not self.interval and not self.plan:
            raise ValueError("Billing interval is required")
        if self.interval and self.plan and self.interval != self.plan:
            raise ValueError("Conflicting billing intervals")
        self.interval = self.interval or self.plan
        return self


@router.post("/checkout")
@limiter.limit("60/minute")
async def create_checkout_session(request: Request, body: CheckoutRequest,
                                  current_user: User = Depends(get_current_user),
                                  db: AsyncSession = Depends(get_db)) -> dict:
    if current_user.subscription_status in ("active", "trialing"):
        raise HTTPException(status_code=409, detail="Manage your existing subscription in the billing portal")
    selected_price = price_id(body.tier, body.interval, settings)
    if not selected_price:
        raise HTTPException(status_code=503, detail="This product is not configured for checkout")
    # Never show approved EUR prices then silently charge a different legacy price.
    price = await stripe.Price.retrieve_async(selected_price)
    recurring = _sget(price, "recurring", {})
    expected_interval = "month" if body.interval == "monthly" else "year"
    if (_sget(price, "currency") != "eur" or _sget(price, "unit_amount") != PRICES[body.tier][body.interval]
            or _sget(recurring, "interval") != expected_interval
            or _sget(recurring, "interval_count", 1) != 1 or not _sget(price, "active", False)):
        raise HTTPException(status_code=503, detail="Configured Stripe price does not match the product catalog")
    customer_id = current_user.stripe_customer_id
    if not customer_id:
        customer = await stripe.Customer.create_async(email=current_user.email or "", name=current_user.display_name,
                                                      metadata={"user_id": str(current_user.id)})
        customer_id = _sget(customer, "id")
        current_user.stripe_customer_id = customer_id
        await db.commit()
    metadata = {"user_id": str(current_user.id), "tier": body.tier, "interval": body.interval}
    # The seven-day Go trial is issued by the application, without a payment card.
    # Checkout starts paid billing and never grants a second card-based trial.
    session = await stripe.checkout.Session.create_async(
        customer=customer_id, line_items=[{"price": selected_price, "quantity": 1}],
        mode="subscription", locale="auto", allow_promotion_codes=True,
        metadata=metadata, subscription_data={"metadata": metadata},
        success_url=f"{settings.STRIPE_BASE_URL}/billing/success",
        cancel_url=f"{settings.STRIPE_BASE_URL}/billing/canceled")
    return {"url": _sget(session, "url")}


@router.post("/portal")
@limiter.limit("60/minute")
async def create_portal_session(request: Request, current_user: User = Depends(get_current_user)) -> dict:
    if not current_user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No billing customer found")
    session = await stripe.billing_portal.Session.create_async(customer=current_user.stripe_customer_id,
                                                              return_url=f"{settings.STRIPE_BASE_URL}/settings")
    return {"url": _sget(session, "url")}


@router.post("/webhook")
@limiter.limit("200/minute")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    try:
        event = stripe.Webhook.construct_event(await request.body(), request.headers.get("stripe-signature", ""), settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.SignatureVerificationError) as exc:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature or payload") from exc
    handlers = {"checkout.session.completed": _handle_checkout_completed,
                "customer.subscription.updated": _handle_subscription_updated,
                "customer.subscription.deleted": _handle_subscription_deleted,
                "invoice.payment_failed": _handle_payment_failed}
    handler = handlers.get(event["type"])
    if handler:
        try:
            await handler(db, event["data"]["object"])
        except Exception as exc:
            await db.rollback()
            logger.exception("Stripe event processing failed")
            raise HTTPException(status_code=500, detail="Webhook processing failed") from exc
    return {"received": True}


def _subscription_period_end(sub: object) -> datetime | None:
    value = _sget(sub, "current_period_end")
    if value is None:
        items = _sget(_sget(sub, "items", {}), "data", []) or []
        if items:
            value = _sget(items[0], "current_period_end")
    return datetime.fromtimestamp(int(value), UTC).replace(tzinfo=None) if value is not None else None


def _invoice_subscription_id(invoice: object) -> str | None:
    return _sget(invoice, "subscription") or _sget(_sget(_sget(invoice, "parent", {}), "subscription_details", {}), "subscription")


async def _get_user_by_customer_id(db: AsyncSession, customer_id: str) -> User | None:
    return (await db.execute(select(User).where(User.stripe_customer_id == customer_id).with_for_update())).scalar_one_or_none()


def _subscription_event_is_current(user: User, event_subscription_id: str | None, event_type: str, *, bind_if_missing: bool = False) -> bool:
    if not event_subscription_id:
        return False
    if user.stripe_subscription_id and user.stripe_subscription_id != event_subscription_id:
        return False
    if bind_if_missing:
        user.stripe_subscription_id = event_subscription_id
    return True


async def _apply_verified_subscription(db: AsyncSession, user: User, sub: object) -> None:
    tier = verified_price_tier(sub, _sget, settings)
    if tier is None:
        # Do not trust arbitrary subscription metadata to grant Plus.
        raise ValueError("Subscription price is not in the configured product catalog")
    user.subscription_tier = tier
    user.subscription_status = _normalize_subscription_status(_sget(sub, "status"))
    end = _subscription_period_end(sub)
    if end is not None:
        user.subscription_ends_at = end
    user.cancel_at_period_end = bool(_sget(sub, "cancel_at_period_end", False) or _sget(sub, "cancel_at"))
    if user.subscription_status in ("active", "trialing"):
        user.freemium_trial_used = True
        user.freemium_trial_ends_at = None
        if user.subscription_status == "trialing":
            user.trial_used = True
    await apply_subscription_quotas(user, db)


async def _handle_checkout_completed(db: AsyncSession, session: object) -> None:
    customer_id, subscription_id = _sget(session, "customer"), _sget(session, "subscription")
    if not customer_id or not subscription_id:
        return
    user = await _get_user_by_customer_id(db, customer_id)
    if user is None:
        identifier = _sget(_sget(session, "metadata", {}), "user_id")
        user = await db.get(User, int(identifier)) if identifier else None
        if user is None or (user.stripe_customer_id and user.stripe_customer_id != customer_id):
            return
        user.stripe_customer_id = customer_id
    if user.stripe_subscription_id and user.stripe_subscription_id != subscription_id:
        if user.subscription_status in ("active", "trialing"):
            return
        old = await stripe.Subscription.retrieve_async(user.stripe_subscription_id)
        if _sget(old, "status") in ("active", "trialing"):
            return
    sub = await stripe.Subscription.retrieve_async(subscription_id)
    if _sget(sub, "customer") != customer_id:
        raise ValueError("Subscription customer mismatch")
    user.stripe_subscription_id = subscription_id
    await _apply_verified_subscription(db, user, sub)


async def _handle_subscription_updated(db: AsyncSession, subscription: object) -> None:
    user = await _get_user_by_customer_id(db, _sget(subscription, "customer"))
    identifier = _sget(subscription, "id")
    if user is None or not _subscription_event_is_current(user, identifier, "updated", bind_if_missing=True):
        return
    # Fetch current Stripe state so out-of-order signed events cannot undo a change.
    current = await stripe.Subscription.retrieve_async(identifier)
    if _sget(current, "customer") != user.stripe_customer_id:
        raise ValueError("Subscription customer mismatch")
    await _apply_verified_subscription(db, user, current)


async def _handle_subscription_deleted(db: AsyncSession, subscription: object) -> None:
    user = await _get_user_by_customer_id(db, _sget(subscription, "customer"))
    if user is None or not _subscription_event_is_current(user, _sget(subscription, "id"), "deleted"):
        return
    user.subscription_status = "canceled"
    user.cancel_at_period_end = False
    user.freemium_trial_ends_at = None
    await db.commit()


async def _handle_payment_failed(db: AsyncSession, invoice: object) -> None:
    user = await _get_user_by_customer_id(db, _sget(invoice, "customer"))
    identifier = _invoice_subscription_id(invoice)
    if user is None or not _subscription_event_is_current(user, identifier, "payment_failed"):
        return
    current = await stripe.Subscription.retrieve_async(identifier)
    await _apply_verified_subscription(db, user, current)
