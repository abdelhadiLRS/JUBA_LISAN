"""Durable account-wide quotas with short reserve/settle transactions."""
from __future__ import annotations
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import select, update, func
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.feature_usage import FeatureReservation, FeatureUsage
from app.services.subscription_catalog import LIMITS, effective_tier, period_bounds


class Reservation:
    def __init__(self, identifier: str | None, amount: int):
        self.id, self.amount, self.actual = identifier, amount, amount

    def charge(self, actual: int) -> None:
        if isinstance(actual, bool) or not isinstance(actual, int) or not 0 <= actual <= self.amount:
            raise ValueError("Actual usage must fit the reservation")
        self.actual = actual


async def reserve(user, feature: str, amount: int = 1, *, session_factory=None) -> Reservation:
    if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
        raise ValueError("Reservation amount must be a positive integer")
    tier = effective_tier(user, trial_enabled=settings.FREEMIUM_TRIAL_ENABLED)
    allowance = LIMITS[tier].get(feature)
    if allowance is None:
        raise ValueError("Unknown metered feature")
    if not settings.STRIPE_ENABLED:
        return Reservation(None, amount)
    factory = session_factory or AsyncSessionLocal
    now = datetime.now(UTC)
    start, end = period_bounds(allowance.period, now)
    start = start.replace(tzinfo=None)
    async with factory() as db, db.begin():
        dialect = db.bind.dialect.name
        if dialect not in ("sqlite", "postgresql"):
            raise HTTPException(status_code=503, detail="Unsupported quota store")
        insert = sqlite_insert if dialect == "sqlite" else pg_insert
        await db.execute(insert(FeatureUsage).values(user_id=user.id, feature=feature, period_start=start, used=0, reserved=0)
            .on_conflict_do_nothing(index_elements=["user_id", "feature", "period_start"]))
        usage_id = (await db.execute(select(FeatureUsage.id).where(FeatureUsage.user_id == user.id,
            FeatureUsage.feature == feature, FeatureUsage.period_start == start))).scalar_one()
        await db.execute(update(FeatureUsage).where(FeatureUsage.id == usage_id).values(reserved=FeatureUsage.reserved))
        expired = (await db.execute(update(FeatureReservation).where(FeatureReservation.usage_id == usage_id,
            FeatureReservation.state == "pending", FeatureReservation.expires_at <= now.replace(tzinfo=None))
            .values(state="expired").returning(FeatureReservation.amount))).scalars().all()
        if expired:
            await db.execute(update(FeatureUsage).where(FeatureUsage.id == usage_id).values(reserved=FeatureUsage.reserved - sum(expired)))
        changed = (await db.execute(update(FeatureUsage).where(FeatureUsage.id == usage_id,
            FeatureUsage.used + FeatureUsage.reserved + amount <= allowance.limit)
            .values(reserved=FeatureUsage.reserved + amount).returning(FeatureUsage.id))).scalar_one_or_none()
        if changed is None:
            usage = await db.get(FeatureUsage, usage_id)
            raise HTTPException(status_code=402, detail={"reason": "quota_exhausted", "feature": feature, "tier": tier,
                "limit": allowance.limit, "remaining": max(0, allowance.limit - usage.used - usage.reserved), "resets_at": end.isoformat()})
        identifier = str(uuid4())
        db.add(FeatureReservation(id=identifier, usage_id=usage_id, amount=amount, state="pending",
            expires_at=(now + timedelta(hours=2)).replace(tzinfo=None)))
    return Reservation(identifier, amount)


async def settle(reservation: Reservation, *, success: bool, session_factory=None) -> None:
    if reservation.id is None:
        return
    factory = session_factory or AsyncSessionLocal
    async with factory() as db, db.begin():
        pending = await db.get(FeatureReservation, reservation.id)
        if pending is None:
            raise HTTPException(status_code=503, detail="Quota reservation missing")
        await db.execute(update(FeatureUsage).where(FeatureUsage.id == pending.usage_id).values(reserved=FeatureUsage.reserved))
        row = (await db.execute(update(FeatureReservation).where(FeatureReservation.id == reservation.id,
            FeatureReservation.state == "pending").values(state="charged" if success else "released")
            .returning(FeatureReservation.usage_id, FeatureReservation.amount))).first()
        if row is None:
            await db.refresh(pending)
            if success and pending.state != "charged":
                raise HTTPException(status_code=503, detail="Quota reservation expired or released")
            return
        await db.execute(update(FeatureUsage).where(FeatureUsage.id == row.usage_id)
            .values(reserved=FeatureUsage.reserved - row.amount, used=FeatureUsage.used + (reservation.actual if success else 0)))


@asynccontextmanager
async def feature_quota(user, feature: str, amount: int = 1, *, session_factory=None):
    reservation = await reserve(user, feature, amount, session_factory=session_factory)
    try:
        yield reservation
    except BaseException:
        await settle(reservation, success=False, session_factory=session_factory)
        raise
    else:
        await settle(reservation, success=True, session_factory=session_factory)


async def quota_status(db, user) -> dict:
    tier = effective_tier(user, trial_enabled=settings.FREEMIUM_TRIAL_ENABLED)
    now = datetime.now(UTC)
    earliest = min(period_bounds(period, now)[0] for period in ("day", "week", "month")).replace(tzinfo=None)
    rows = (await db.execute(select(FeatureUsage).where(FeatureUsage.user_id == user.id, FeatureUsage.period_start >= earliest)
                            .execution_options(populate_existing=True))).scalars().all()
    live = {}
    if rows:
        values = (await db.execute(select(FeatureReservation.usage_id, func.sum(FeatureReservation.amount))
            .where(FeatureReservation.usage_id.in_([row.id for row in rows]), FeatureReservation.state == "pending",
                   FeatureReservation.expires_at > now.replace(tzinfo=None)).group_by(FeatureReservation.usage_id))).all()
        live = dict(values)
    result = {}
    for feature, allowance in LIMITS[tier].items():
        start, end = period_bounds(allowance.period, now)
        row = next((item for item in rows if item.feature == feature and item.period_start == start.replace(tzinfo=None)), None)
        used, reserved = (row.used, int(live.get(row.id, 0))) if row else (0, 0)
        result[feature] = {"limit": allowance.limit, "used": used, "reserved": reserved,
            "remaining": max(0, allowance.limit - used - reserved), "period": allowance.period,
            "unit": allowance.unit, "resets_at": end.isoformat()}
    return {"tier": tier, "metered": settings.STRIPE_ENABLED, "quota_scope": "account", "features": result}
