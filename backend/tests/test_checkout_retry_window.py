from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock
import pytest
import stripe
from app.models.billing_intent import BillingIntent
from app.routers.billing import CheckoutRequest
from app.services.billing_checkout_service import checked_checkout
from app.services.subscription_catalog import product_settings


@pytest.mark.asyncio
async def test_delayed_creation_rejection_rotates_only_after_explicit_expiry_error(test_user, db_session, monkeypatch):
    user, _ = test_user
    user.stripe_customer_id = "cus_test"
    intent = BillingIntent(user_id=user.id, identifier="old", tier="go", interval="monthly",
        expires_at=datetime.now(UTC).replace(tzinfo=None)+timedelta(minutes=29))
    db_session.add(intent)
    await db_session.commit()
    monkeypatch.setattr(product_settings, "STRIPE_PRICE_GO_MONTHLY", "price_go")
    monkeypatch.setattr(stripe.Price, "retrieve_async", AsyncMock(return_value={"active":True,"currency":"eur","unit_amount":799,"recurring":{"interval":"month"}}))
    create = AsyncMock(side_effect=[stripe.InvalidRequestError("Expiry must be at least 30 minutes", "expires_at"), {"url":"https://checkout.stripe.com/test"}])
    monkeypatch.setattr(stripe.checkout.Session, "create_async", create)
    assert (await checked_checkout(CheckoutRequest(tier="go", interval="monthly"), user, db_session))["url"]
    assert create.await_count == 2
    first, second = [call.kwargs for call in create.call_args_list]
    assert first["idempotency_key"] == "juba-checkout-old"
    assert second["idempotency_key"] != first["idempotency_key"]
    assert second["expires_at"] > first["expires_at"]


@pytest.mark.asyncio
async def test_uncertain_api_failure_keeps_original_intent(test_user, db_session, monkeypatch):
    user, _ = test_user
    user.stripe_customer_id = "cus_test"
    db_session.add(BillingIntent(user_id=user.id, identifier="stable", tier="go", interval="monthly",
        expires_at=datetime.now(UTC).replace(tzinfo=None)+timedelta(minutes=29)))
    await db_session.commit()
    monkeypatch.setattr(product_settings, "STRIPE_PRICE_GO_MONTHLY", "price_go")
    monkeypatch.setattr(stripe.Price, "retrieve_async", AsyncMock(return_value={"active":True,"currency":"eur","unit_amount":799,"recurring":{"interval":"month"}}))
    create = AsyncMock(side_effect=TimeoutError("Uncertain provider reply"))
    monkeypatch.setattr(stripe.checkout.Session, "create_async", create)
    with pytest.raises(TimeoutError):
        await checked_checkout(CheckoutRequest(tier="go", interval="monthly"), user, db_session)
    await db_session.refresh(await db_session.get(BillingIntent,user.id))
    assert (await db_session.get(BillingIntent,user.id)).identifier == "stable"
    assert create.await_count == 1
