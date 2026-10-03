"""Authenticated product state and server-issued no-card Go trial."""
from datetime import UTC, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user, require_learner
from app.core.limiter import limiter
from app.models.user import User
from app.services.feature_quota_service import quota_status
from app.services.subscription_catalog import SESSION_SECONDS, TRIAL_DAYS, public_catalog

router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])


@router.get("/catalog")
@limiter.limit("60/minute")
async def catalog(request: Request):
    return public_catalog(settings.STRIPE_ENABLED, settings)


@router.get("/me", dependencies=[Depends(require_learner)])
@limiter.limit("60/minute")
async def my_subscription(request: Request, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await quota_status(db, user)
    result.update({"subscription_status": user.subscription_status,
                   "stored_tier": user.subscription_tier,
                   "cancel_at_period_end": user.cancel_at_period_end,
                   "subscription_ends_at": user.subscription_ends_at,
                   "trial_ends_at": user.freemium_trial_ends_at,
                   "trial_available": bool(settings.STRIPE_ENABLED and settings.FREEMIUM_TRIAL_ENABLED
                                           and not user.freemium_trial_used and user.subscription_status not in ("active", "trialing")),
                   "voice_session_max_seconds": SESSION_SECONDS[result["tier"]],
                   # Integration is explicit, not a claim that unwired routes are metered.
                   "enforced_features": ["translation"]})
    return result


@router.post("/trial", dependencies=[Depends(require_learner)])
@limiter.limit("10/minute")
async def start_trial(request: Request, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not settings.STRIPE_ENABLED or not settings.FREEMIUM_TRIAL_ENABLED:
        raise HTTPException(status_code=409, detail="Trial is not available")
    end = (datetime.now(UTC) + timedelta(days=TRIAL_DAYS)).replace(tzinfo=None)
    changed = (await db.execute(update(User).where(User.id == user.id, User.freemium_trial_used.is_(False),
                            User.subscription_status.notin_(["active", "trialing"]))
                            .values(freemium_trial_used=True, freemium_trial_ends_at=end)
                            .returning(User.id))).scalar_one_or_none()
    if changed is None:
        raise HTTPException(status_code=409, detail="Trial was already used or account is subscribed")
    await db.commit()
    await db.refresh(user)
    return {"tier": "go", "trial_ends_at": end, "card_required": False}
