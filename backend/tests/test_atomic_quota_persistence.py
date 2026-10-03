from unittest.mock import AsyncMock
import pytest
from sqlalchemy import select, func
from app.core.config import settings
from app.models.reading import ReadingExercise
from app.models.feature_usage import FeatureReservation
from app.services.feature_quota_service import feature_quota, quota_status
from app.services.quota_persistence import atomic_generation


def exercise():
    return ReadingExercise(level="A1", target_language="en-US", exercise_type="email", topic="test", text="Hello", questions=[])


@pytest.fixture
def metered(monkeypatch):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)


@pytest.mark.asyncio
async def test_content_and_usage_commit_together(test_user, test_session_factory, metered):
    user, _ = test_user
    async with test_session_factory() as db:
        async with feature_quota(user, "reading", db=db) as quota:
            db.add(exercise())
            await quota.commit(db)
    async with test_session_factory() as db:
        assert (await db.execute(select(func.count(ReadingExercise.id)))).scalar() == 1
        status = await quota_status(db, user)
        assert status["features"]["reading"]["used"] == 1
        assert status["features"]["reading"]["reserved"] == 0


@pytest.mark.asyncio
async def test_settlement_failure_rolls_back_content_before_release(test_user, test_session_factory, metered, monkeypatch):
    from app.services import feature_quota_service as service
    user, _ = test_user
    original = service._settle_in_transaction
    async def failure(db, reservation, success):
        if success:
            raise RuntimeError("Failed quota write")
        await original(db, reservation, success)
    monkeypatch.setattr(service, "_settle_in_transaction", failure)
    async with test_session_factory() as db:
        with pytest.raises(RuntimeError):
            async with feature_quota(user, "reading", db=db) as quota:
                db.add(exercise())
                await quota.commit(db)
    async with test_session_factory() as db:
        assert (await db.execute(select(func.count(ReadingExercise.id)))).scalar() == 0
        status = await quota_status(db, user)
        assert status["features"]["reading"]["used"] == 0
        assert status["features"]["reading"]["reserved"] == 0


@pytest.mark.asyncio
async def test_legacy_service_commit_is_atomic(test_user, test_session_factory, metered):
    from app.services.feature_quota_service import reserve
    user, _ = test_user
    quota = await reserve(user, "reading", session_factory=test_session_factory)
    async with test_session_factory() as db:
        async with atomic_generation(db, quota):
            db.add(exercise())
            await db.commit()  # Existing generation service contract.
    assert quota.committed
    async with test_session_factory() as db:
        assert (await quota_status(db,user))["features"]["reading"]["used"] == 1


@pytest.mark.asyncio
async def test_post_commit_exception_does_not_refund_saved_content(test_user, test_session_factory, metered):
    user, _ = test_user
    async with test_session_factory() as db:
        with pytest.raises(RuntimeError):
            async with feature_quota(user, "reading", db=db) as quota:
                db.add(exercise())
                await quota.commit(db)
                raise RuntimeError("Refresh or response failed after commit")
    async with test_session_factory() as db:
        assert (await db.execute(select(func.count(ReadingExercise.id)))).scalar() == 1
        assert (await quota_status(db,user))["features"]["reading"]["used"] == 1
