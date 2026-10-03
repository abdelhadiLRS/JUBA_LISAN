"""Reserve in a short transaction; save content and charge atomically.

Persisting callers must use `await quota.commit(db)` instead of committing the
content and later charging it. Nonpersistent outputs settle on context exit.
"""
from __future__ import annotations
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import select, update, func
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from app.core.config import settings
from app.core.session_factory import current_session_factory
from app.models.feature_usage import FeatureReservation, FeatureUsage
from app.services.subscription_catalog import LIMITS, effective_tier, period_bounds


class Reservation:
    def __init__(self, identifier: str | None, amount: int, session_factory=None):
        self.id, self.amount, self.actual = identifier, amount, amount
        self.session_factory = session_factory or current_session_factory()
        self.committed = False

    def charge(self, actual: int) -> None:
        if isinstance(actual, bool) or not isinstance(actual, int) or not 0 <= actual <= self.amount:
            raise ValueError("Actual usage must fit the reservation")
        self.actual = actual

    async def commit(self, db) -> None:
        """Flush content and charge on the SAME connection before the single commit."""
        try:
            await db.flush()
            await settle(self, success=True, db=db)
            await db.commit()
            self.committed = True
        except BaseException:
            await db.rollback()
            raise


async def reserve(user, feature: str, amount: int = 1, *, session_factory=None) -> Reservation:
    if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
        raise ValueError("Reservation amount must be a positive integer")
    tier = effective_tier(user, trial_enabled=settings.FREEMIUM_TRIAL_ENABLED)
    allowance = LIMITS[tier].get(feature)
    if allowance is None:
        raise ValueError("Unknown metered feature")
    factory = session_factory or current_session_factory()
    if not settings.STRIPE_ENABLED:
        return Reservation(None, amount, factory)
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
    return Reservation(identifier, amount, factory)


async def _settle_in_transaction(db, reservation: Reservation, success: bool) -> None:
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


async def settle(reservation: Reservation, *, success: bool, session_factory=None, db=None) -> None:
    if reservation.id is None or reservation.committed:
        return
    if db is not None:
        await _settle_in_transaction(db, reservation, success)
        return
    factory = session_factory or reservation.session_factory
    async with factory() as session, session.begin():
        await _settle_in_transaction(session, reservation, success)


@asynccontextmanager
async def feature_quota(user, feature: str, amount: int = 1, *, session_factory=None, db=None):
    # End a read transaction before a separate reserve writer (important for SQLite).
    # Callers must not stage content until after reservation admission.
    if db is not None:
        if db.new or db.dirty or db.deleted:
            raise RuntimeError("Reserve quota before staging content")
        await db.commit()
    reservation = await reserve(user, feature, amount, session_factory=session_factory)
    try:
        yield reservation
    except BaseException:
        if db is not None:
            await db.rollback()  # Release write locks BEFORE the compensating transaction.
        if not reservation.committed:
            await settle(reservation, success=False)
        raise
    else:
        if db is not None and not reservation.committed:
            await db.rollback()
            await settle(reservation, success=False)
            raise RuntimeError("Persisted generation must call quota.commit(db)")
        if not reservation.committed:
            await settle(reservation, success=True)


async def quota_status(db, user) -> dict:
    tier = effective_tier(user, trial_enabled=settings.FREEMIUM_TRIAL_ENABLED)
    now = datetime.now(UTC)
    earliest = min(period_bounds(period, now)[0] for period in ("day", "week", "month")).replace(tzinfo=None)
    rows = (await db.execute(select(FeatureUsage).where(FeatureUsage.user_id == user.id, FeatureUsage.period_start >= earliest)
        .execution_options(populate_existing=True))).scalars().all()
    live = {}
    if rows:
        live = dict((await db.execute(select(FeatureReservation.usage_id, func.sum(FeatureReservation.amount))
            .where(FeatureReservation.usage_id.in_([row.id for row in rows]), FeatureReservation.state == "pending",
                FeatureReservation.expires_at > now.replace(tzinfo=None)).group_by(FeatureReservation.usage_id))).all())
    result = {}
    for feature, allowance in LIMITS[tier].items():
        start, end = period_bounds(allowance.period, now)
        row = next((item for item in rows if item.feature == feature and item.period_start == start.replace(tzinfo=None)), None)
        used, reserved = (row.used, int(live.get(row.id, 0))) if row else (0, 0)
        result[feature] = {"limit": allowance.limit, "used": used, "reserved": reserved,
            "remaining": max(0, allowance.limit - used - reserved), "period": allowance.period,
            "unit": allowance.unit, "resets_at": end.isoformat()}
    return {"tier": tier, "metered": settings.STRIPE_ENABLED, "quota_scope": "account", "features": result}
