import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.config import settings
from app.services.feature_quota_service import feature_quota, reserve, settle, quota_status


@pytest.fixture
def metered(monkeypatch):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(settings, "FREEMIUM_TRIAL_ENABLED", True)


@pytest.mark.asyncio
async def test_boundary_and_failure_release(test_engine, test_user, db_session, metered):
    user, _ = test_user
    factory = async_sessionmaker(test_engine, expire_on_commit=False)
    for _ in range(5):
        async with feature_quota(user, "translation", session_factory=factory):
            pass
    with pytest.raises(HTTPException) as exc:
        await reserve(user, "translation", session_factory=factory)
    assert exc.value.status_code == 402
    status = await quota_status(db_session, user)
    assert status["features"]["translation"]["used"] == 5
    with pytest.raises(RuntimeError):
        async with feature_quota(user, "chat", session_factory=factory):
            raise RuntimeError("provider failure")
    status = await quota_status(db_session, user)
    assert status["features"]["chat"]["used"] == 0
    assert status["features"]["chat"]["reserved"] == 0


@pytest.mark.asyncio
async def test_inflight_reservations_and_idempotent_settle(test_engine, test_user, metered):
    user, _ = test_user
    factory = async_sessionmaker(test_engine, expire_on_commit=False)
    token = await reserve(user, "flashcards", 20, session_factory=factory)
    with pytest.raises(HTTPException):
        await reserve(user, "flashcards", 1, session_factory=factory)
    token.charge(3)
    await settle(token, success=True, session_factory=factory)
    await settle(token, success=True, session_factory=factory)
    async with factory() as db:
        status = await quota_status(db, user)
    assert status["features"]["flashcards"]["used"] == 3
    assert status["features"]["flashcards"]["remaining"] == 17


@pytest.mark.asyncio
async def test_paid_user_is_metered_not_unlimited(test_engine, test_user, metered):
    user, _ = test_user
    user.subscription_status, user.subscription_tier = "active", "go"
    factory = async_sessionmaker(test_engine, expire_on_commit=False)
    token = await reserve(user, "voice", 3600, session_factory=factory)
    with pytest.raises(HTTPException):
        await reserve(user, "voice", 1, session_factory=factory)
    await settle(token, success=False, session_factory=factory)
