"""Compatibility status fields plus authoritative tier feature usage."""
from datetime import UTC, datetime
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user, require_learner
from app.core.limiter import limiter
from app.models.user import User
from app.services.feature_quota_service import quota_status
from app.services.subscription_catalog import utc

router = APIRouter(prefix="/api/freemium", tags=["freemium"], dependencies=[Depends(require_learner)])


@router.get("/status")
@limiter.limit("60/minute")
async def freemium_status(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    result = await quota_status(db, current_user)
    end = current_user.freemium_trial_ends_at
    result.update({"trial_active": bool(settings.STRIPE_ENABLED and settings.FREEMIUM_TRIAL_ENABLED and end is not None
                                       and utc(end) > datetime.now(UTC) and current_user.subscription_status not in ("active", "trialing")),
                   "trial_ends_at": utc(end).isoformat() if end is not None else None})
    for name in ("chat", "lessons", "listening", "reading"):
        result[f"{name}_remaining"] = result["features"][name]["remaining"]
        result[f"{name}_limit"] = result["features"][name]["limit"]
    result["voice_remaining_seconds"] = result["features"]["voice"]["remaining"]
    result["voice_limit_seconds"] = result["features"]["voice"]["limit"]
    return result
