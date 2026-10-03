"""Regression coverage for the shared automatic/explicit Go trial policy."""
from datetime import UTC, datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings
from app.models.user import User
from app.services.subscription_catalog import TRIAL_DAYS, effective_tier
from app.services.subscription_trial_service import issue_go_trial, trial_available


@pytest.fixture
def enabled_trial():
    with (
        patch.object(settings, "STRIPE_ENABLED", True),
        patch.object(settings, "FREEMIUM_TRIAL_ENABLED", True),
        patch.object(settings, "FREEMIUM_TRIAL_DAYS", 30),
    ):
        yield


@pytest.mark.asyncio
async def test_trial_uses_catalog_seven_days_and_normalizes_utc(test_user, db_session, enabled_trial):
    user, _ = test_user
    now = datetime(2026, 10, 3, 13, 43, tzinfo=timezone(timedelta(hours=1)))
    end = await issue_go_trial(db_session, user, now=now)
    assert end == datetime(2026, 10, 10, 12, 43)
    assert TRIAL_DAYS == 7
    assert user.freemium_trial_used is True
    assert user.freemium_trial_ends_at == end
    assert effective_tier(user, now=now) == "go"
    assert effective_tier(user, now=end.replace(tzinfo=UTC)) == "free"


@pytest.mark.asyncio
async def test_repeat_claim_does_not_extend_deadline(test_user, db_session, enabled_trial):
    user, _ = test_user
    now = datetime(2026, 10, 3, tzinfo=UTC)
    first = await issue_go_trial(db_session, user, now=now)
    assert await issue_go_trial(db_session, user, now=now + timedelta(days=1)) is None
    assert user.freemium_trial_ends_at == first


@pytest.mark.asyncio
@pytest.mark.parametrize("paid_status", ["active", "trialing"])
async def test_paid_users_are_not_given_a_no_card_trial(test_user, db_session, enabled_trial, paid_status):
    user, _ = test_user
    user.subscription_status = paid_status
    user.subscription_tier = "plus"
    await db_session.commit()
    assert not trial_available(user)
    assert await issue_go_trial(db_session, user) is None
    assert user.freemium_trial_ends_at is None


@pytest.mark.asyncio
@pytest.mark.parametrize("flag", ["STRIPE_ENABLED", "FREEMIUM_TRIAL_ENABLED"])
async def test_disabled_or_self_hosted_never_issues_trial(test_user, db_session, enabled_trial, flag):
    user, _ = test_user
    with patch.object(settings, flag, False):
        assert await issue_go_trial(db_session, user) is None
    assert user.freemium_trial_used is False


@pytest.mark.asyncio
@pytest.mark.parametrize("offset", [-1, 30])
async def test_existing_deadline_is_preserved_even_with_legacy_unused_flag(test_user, db_session, enabled_trial, offset):
    user, _ = test_user
    old = datetime.now(UTC).replace(tzinfo=None) + timedelta(days=offset)
    user.freemium_trial_ends_at = old
    user.freemium_trial_used = False
    await db_session.commit()
    assert not trial_available(user)
    assert await issue_go_trial(db_session, user) is None
    assert user.freemium_trial_ends_at == old


@pytest.mark.asyncio
async def test_stale_two_session_claim_cannot_extend_trial(test_user, test_engine, enabled_trial):
    user, _ = test_user
    factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with factory() as a, factory() as b:
        first_user = await a.get(User, user.id)
        stale_user = await b.get(User, user.id)
        # Both requests read unused before either claims. End the read transaction
        # without expiring the stale object, then emulate serial SQL execution.
        await b.commit()
        now = datetime(2026, 10, 3, tzinfo=UTC)
        first = await issue_go_trial(a, first_user, now=now)
        assert await issue_go_trial(b, stale_user, now=now + timedelta(hours=1)) is None
        assert stale_user.freemium_trial_used is True
        assert stale_user.freemium_trial_ends_at == first


@pytest.mark.asyncio
async def test_paid_webhook_wins_over_stale_trial_read(test_user, test_engine, enabled_trial):
    user, _ = test_user
    factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with factory() as a, factory() as b:
        paid_user = await a.get(User, user.id)
        stale_user = await b.get(User, user.id)
        await b.commit()
        paid_user.subscription_status = "active"
        paid_user.subscription_tier = "plus"
        await a.commit()
        assert await issue_go_trial(b, stale_user) is None
        assert stale_user.subscription_status == "active"
        assert stale_user.freemium_trial_ends_at is None


@pytest.mark.asyncio
async def test_auth_me_and_explicit_trial_share_one_deadline(client, test_user, enabled_trial):
    _, headers = test_user
    me = await client.get("/api/auth/me", headers=headers)
    assert me.status_code == 200
    first = me.json()["freemium_trial_ends_at"]
    repeat = await client.post("/api/subscriptions/trial", headers=headers)
    assert repeat.status_code == 409
    again = await client.get("/api/auth/me", headers=headers)
    assert again.json()["freemium_trial_ends_at"] == first


@pytest.mark.asyncio
async def test_explicit_trial_then_auth_me_does_not_extend(client, test_user, enabled_trial):
    _, headers = test_user
    trial = await client.post("/api/subscriptions/trial", headers=headers)
    assert trial.status_code == 200
    assert trial.json()["tier"] == "go"
    assert trial.json()["card_required"] is False
    me = await client.get("/api/auth/me", headers=headers)
    assert me.json()["freemium_trial_ends_at"] == trial.json()["trial_ends_at"]


@pytest.mark.asyncio
async def test_registration_ignores_old_configured_duration(client, enabled_trial):
    before = datetime.now(UTC).replace(tzinfo=None)
    response = await client.post("/api/auth/register", json={
        "username": "catalogtrial", "email": "catalogtrial@test.com",
        "password": "Test1234!@", "native_language": "es",
    })
    after = datetime.now(UTC).replace(tzinfo=None)
    assert response.status_code == 200
    token = response.json()["access_token"]
    me = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    end = datetime.fromisoformat(me.json()["freemium_trial_ends_at"]).replace(tzinfo=None)
    assert before + timedelta(days=7) <= end <= after + timedelta(days=7)
