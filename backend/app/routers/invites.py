from fastapi import APIRouter, Request, Depends, HTTPException, status
from redis.asyncio import Redis
import secrets

from app.core.config import settings
from app.core.deps import get_redis, require_learner
from app.core.limiter import limiter
from app.models.user import User

router = APIRouter(prefix="/api/invites", tags=["invites"])


@router.post("/create")
@limiter.limit("10/hour")
async def create_member_invite(
    request: Request,
    member: User = Depends(require_learner),
    redis: Redis | None = Depends(get_redis),
):
    """Create a registration invitation for an active community member."""
    token = secrets.token_urlsafe(32)

    if redis is not None:
        await redis.setex(f"invite:{token}", 172800, str(member.id))
    elif not settings.ALLOW_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Invitations require Redis when registration is closed",
        )

    return {"invite_url": f"/register?invite={token}"}
