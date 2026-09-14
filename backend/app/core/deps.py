from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError as JWTError
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.services.subscription_service import is_subscribed

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

MAINTENANCE_KEY = "maintenance_mode"
REDIS_SOCKET_TIMEOUT = 5.0


async def get_redis():
    redis = Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=REDIS_SOCKET_TIMEOUT,
        socket_timeout=REDIS_SOCKET_TIMEOUT,
    )
    try:
        yield redis
    finally:
        await redis.aclose()


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token") from None

    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


async def check_maintenance_mode(redis: Redis = Depends(get_redis)) -> None:
    """Raise 503 if maintenance mode is active in Redis."""
    try:
        if await redis.get(MAINTENANCE_KEY) == "1":
            raise HTTPException(
                status_code=503,
                detail="Service temporarily unavailable — maintenance mode is active",
            )
    except HTTPException:
        raise
    except Exception:
        return
