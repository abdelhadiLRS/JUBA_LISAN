"""Durable checkout idempotency across tabs, workers and uncertain Stripe replies."""
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
    await db.commit()  # Persist idempotency before any paid-session creation.
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
    session = await stripe.checkout.Session.create_async(customer=customer_id,
        line_items=[{"price": selected_price, "quantity": 1}], mode="subscription", locale="auto",
        allow_promotion_codes=True, metadata=metadata, subscription_data={"metadata": metadata},
        expires_at=int(expires_at.replace(tzinfo=UTC).timestamp()),
        success_url=f"{settings.STRIPE_BASE_URL}/billing/success", cancel_url=f"{settings.STRIPE_BASE_URL}/billing/canceled",
        idempotency_key=f"juba-checkout-{identifier}")
    url = get(session, "url")
    if not url:
        raise HTTPException(status_code=502, detail="Stripe did not return a checkout URL")
    await db.execute(update(BillingIntent).where(BillingIntent.user_id == user.id, BillingIntent.identifier == identifier).values(url=url))
    await db.commit()
    return {"url": url}
