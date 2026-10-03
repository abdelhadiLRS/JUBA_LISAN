"""Durable checkout idempotency, including delayed failed-creation retries."""
from datetime import UTC, datetime, timedelta
from uuid import uuid4
import stripe
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.core.config import settings
from app.models.billing_intent import BillingIntent
from app.services.subscription_catalog import PRICES, price_id


def get(obj, key, default=None):
    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)


def invalid_creation_window(exc) -> bool:
    # Rotate ONLY after Stripe explicitly rejects expiry validation. A timeout or
    # ambiguous API error may hide an accepted session and must retain its key.
    return isinstance(exc, stripe.InvalidRequestError) and getattr(exc, "param", None) == "expires_at"


async def checked_checkout(body, user, db) -> dict:
    selected_price = price_id(body.tier, body.interval, settings)
    if not selected_price:
        raise HTTPException(status_code=503, detail="This product is not configured for checkout")
    price = await stripe.Price.retrieve_async(selected_price)
    recurring = get(price, "recurring", {})
    if (get(price, "currency") != "eur" or get(price, "unit_amount") != PRICES[body.tier][body.interval]
        or get(recurring, "interval") != ("month" if body.interval == "monthly" else "year")
        or get(recurring, "interval_count", 1) != 1 or not get(price, "active", False)):
        raise HTTPException(status_code=503, detail="Configured Stripe price does not match the product catalog")
    now = datetime.now(UTC).replace(tzinfo=None)
    expires = now + timedelta(minutes=31)
    dialect = db.bind.dialect.name
    if dialect not in ("sqlite", "postgresql"):
        raise HTTPException(status_code=503, detail="Unsupported checkout store")
    insert = sqlite_insert if dialect == "sqlite" else pg_insert
    await db.execute(insert(BillingIntent).values(user_id=user.id, identifier=str(uuid4()), tier=body.tier,
        interval=body.interval, expires_at=expires).on_conflict_do_nothing(index_elements=["user_id"]))
    await db.execute(update(BillingIntent).where(BillingIntent.user_id == user.id).values(identifier=BillingIntent.identifier))
    await db.refresh(user)
    if user.subscription_status in ("active", "trialing"):
        raise HTTPException(status_code=409, detail="Manage your existing subscription in the billing portal")
    intent = await db.get(BillingIntent, user.id)
    await db.refresh(intent)
    if intent.expires_at <= now:
        intent.identifier, intent.tier, intent.interval = str(uuid4()), body.tier, body.interval
        intent.expires_at, intent.url = expires, None
    elif intent.tier != body.tier or intent.interval != body.interval:
        raise HTTPException(status_code=409, detail="A different checkout is pending. Complete it or wait for it to expire.")
    identifier, expires_at, existing_url = intent.identifier, intent.expires_at, intent.url
    await db.commit()
    if existing_url:
        return {"url": existing_url}
    customer_id = user.stripe_customer_id
    if not customer_id:
        customer = await stripe.Customer.create_async(email=user.email or "", name=user.display_name,
            metadata={"user_id": str(user.id)}, idempotency_key=f"juba-customer-{user.id}")
        customer_id = get(customer, "id")
        if not customer_id:
            raise HTTPException(status_code=502, detail="Stripe did not return a customer")
        user.stripe_customer_id = customer_id
        await db.commit()
    metadata = {"user_id": str(user.id), "tier": body.tier, "interval": body.interval}
    async def create(key, expiration):
        return await stripe.checkout.Session.create_async(customer=customer_id,
            line_items=[{"price": selected_price, "quantity": 1}], mode="subscription", locale="auto",
            allow_promotion_codes=True, metadata=metadata, subscription_data={"metadata": metadata},
            expires_at=int(expiration.replace(tzinfo=UTC).timestamp()),
            success_url=f"{settings.STRIPE_BASE_URL}/billing/success", cancel_url=f"{settings.STRIPE_BASE_URL}/billing/canceled",
            idempotency_key=f"juba-checkout-{key}")
    try:
        session = await create(identifier, expires_at)
    except stripe.InvalidRequestError as exc:
        if not invalid_creation_window(exc):
            raise
        # A rejected expiry request did not create a new session. Serialize renewal
        # and reuse another worker's already-renewed intent instead of rotating again.
        await db.execute(update(BillingIntent).where(BillingIntent.user_id == user.id).values(identifier=BillingIntent.identifier))
        await db.refresh(user)
        if user.subscription_status in ("active", "trialing"):
            raise HTTPException(status_code=409, detail="Manage your existing subscription in the billing portal") from exc
        intent = await db.get(BillingIntent, user.id)
        await db.refresh(intent)
        if intent.identifier == identifier:
            intent.identifier = str(uuid4())
            intent.expires_at = datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=31)
            intent.url = None
        elif intent.tier != body.tier or intent.interval != body.interval:
            raise HTTPException(status_code=409, detail="Checkout selection changed; review your plan") from exc
        identifier, expires_at, existing_url = intent.identifier, intent.expires_at, intent.url
        await db.commit()
        if existing_url:
            return {"url": existing_url}
        session = await create(identifier, expires_at)
    url = get(session, "url")
    if not url:
        raise HTTPException(status_code=502, detail="Stripe did not return a checkout URL")
    await db.execute(update(BillingIntent).where(BillingIntent.user_id == user.id, BillingIntent.identifier == identifier).values(url=url))
    await db.commit()
    return {"url": url}
