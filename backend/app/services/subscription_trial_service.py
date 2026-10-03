"""One no-card Go trial per account, with the catalog as duration authority.

Automatic registration/auth-me activation is retained for compatibility.
Existing deadlines, including historic longer trials, are never rewritten.
"""
from datetime import UTC, datetime, timedelta

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User
from app.services.subscription_catalog import TRIAL_DAYS, utc


def trial_available(user) -> bool:
    return bool(
        settings.STRIPE_ENABLED
        and settings.FREEMIUM_TRIAL_ENABLED
        and user.is_active
        and not user.freemium_trial_used
        and user.freemium_trial_ends_at is None
        and user.subscription_status not in ("active", "trialing")
    )


async def issue_go_trial(
    db: AsyncSession, user: User, *, now: datetime | None = None
) -> datetime | None:
    """Return a new deadline only for the request that wins the SQL claim.

    Do not trust eligibility from a previously loaded ORM object: a webhook or
    another request may already have changed this account. Refresh even after
    losing so auth-me cannot return the stale unused flag. Caller must have
    persisted unrelated changes before calling this transaction-owning helper.
    """
    if not trial_available(user):
        return None
    end = (utc(now or datetime.now(UTC)) + timedelta(days=TRIAL_DAYS)).replace(tzinfo=None)
    try:
        changed = (await db.execute(
            update(User)
            .where(
                User.id == user.id,
                User.is_active.is_(True),
                User.freemium_trial_used.is_(False),
                User.freemium_trial_ends_at.is_(None),
                User.subscription_status.notin_(["active", "trialing"]),
            )
            .values(freemium_trial_used=True, freemium_trial_ends_at=end)
            .execution_options(synchronize_session=False)
            .returning(User.id)
        )).scalar_one_or_none()
        if changed is not None:
            await db.commit()
        await db.refresh(user)
    except BaseException:
        await db.rollback()
        raise
    return end if changed is not None else None
