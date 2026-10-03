"""Adapt legacy generation services that own their commit without changing APIs.

Callbacks are installed ONLY on the owned content session and removed on exit.
A failure in flush/settlement rolls back both content and usage. No quota-state
commit is issued from an event; it participates in the content commit.
"""
from contextlib import asynccontextmanager
from fastapi import HTTPException
from sqlalchemy import event, select, update
from app.models.feature_usage import FeatureReservation, FeatureUsage


@asynccontextmanager
async def atomic_generation(db, reservation):
    session = db.sync_session
    prepared = False

    def before_commit(sync_session):
        nonlocal prepared
        if reservation.committed or prepared:
            return
        sync_session.flush()
        if reservation.id is not None:
            usage_id = sync_session.execute(select(FeatureReservation.usage_id).where(FeatureReservation.id == reservation.id)).scalar_one_or_none()
            if usage_id is None:
                raise HTTPException(status_code=503, detail="Quota reservation missing")
            sync_session.execute(update(FeatureUsage).where(FeatureUsage.id == usage_id).values(reserved=FeatureUsage.reserved))
            row = sync_session.execute(update(FeatureReservation).where(FeatureReservation.id == reservation.id,
                FeatureReservation.state == "pending").values(state="charged")
                .returning(FeatureReservation.amount)).scalar_one_or_none()
            if row is None:
                raise HTTPException(status_code=503, detail="Quota reservation is not pending")
            sync_session.execute(update(FeatureUsage).where(FeatureUsage.id == usage_id)
                .values(reserved=FeatureUsage.reserved-row, used=FeatureUsage.used+reservation.actual))
        prepared = True

    def after_commit(sync_session):
        if prepared:
            reservation.committed = True

    def after_rollback(sync_session):
        nonlocal prepared
        prepared = False

    event.listen(session, "before_commit", before_commit)
    event.listen(session, "after_commit", after_commit)
    event.listen(session, "after_rollback", after_rollback)
    try:
        yield
        if not reservation.committed:
            raise RuntimeError("Generation service did not commit its content")
    except BaseException:
        await db.rollback()
        raise
    finally:
        event.remove(session, "before_commit", before_commit)
        event.remove(session, "after_commit", after_commit)
        event.remove(session, "after_rollback", after_rollback)
