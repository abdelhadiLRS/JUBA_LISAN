from unittest.mock import AsyncMock
import pytest
import stripe
from app.core.config import settings
from app.models.billing_intent import BillingIntent
from app.routers.billing import CheckoutRequest
from app.services.billing_checkout_service import checked_checkout
from app.services.subscription_catalog import product_settings


@pytest.mark.asyncio
async def test_same_checkout_is_reused_and_other_tier_blocked(test_user, db_session, monkeypatch):
    from fastapi import HTTPException
    user, _ = test_user
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(product_settings, "STRIPE_PRICE_GO_MONTHLY", "price_go")
    monkeypatch.setattr(product_settings, "STRIPE_PRICE_PLUS_MONTHLY", "price_plus")
    async def price(identifier):
        return {"active": True, "currency": "eur", "unit_amount": 799 if identifier == "price_go" else 1499,
                "recurring": {"interval": "month", "interval_count": 1}}
    monkeypatch.setattr(stripe.Price, "retrieve_async", AsyncMock(side_effect=price))
    customer = AsyncMock(return_value={"id": "cus_test"})
    checkout = AsyncMock(return_value={"url": "https://checkout.stripe.com/pay/test"})
    monkeypatch.setattr(stripe.Customer, "create_async", customer)
    monkeypatch.setattr(stripe.checkout.Session, "create_async", checkout)
    request = CheckoutRequest(tier="go", interval="monthly")
    first = await checked_checkout(request, user, db_session)
    second = await checked_checkout(request, user, db_session)
    assert first == second
    assert checkout.await_count == 1
    assert customer.await_count == 1
    intent = await db_session.get(BillingIntent, user.id)
    assert checkout.call_args.kwargs["idempotency_key"] == f"juba-checkout-{intent.identifier}"
    with pytest.raises(HTTPException) as exc:
        await checked_checkout(CheckoutRequest(tier="plus", interval="monthly"), user, db_session)
    assert exc.value.status_code == 409
