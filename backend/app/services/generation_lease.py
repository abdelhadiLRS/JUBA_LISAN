"""Optional Redis coordination; quota reservations remain database-backed."""
import logging
from app.core.config import settings
from app.utils.redis import redis_client
logger = logging.getLogger(__name__)


async def release_generation_lock(key: str, token: str) -> None:
    if not token or not settings.REDIS_ENABLED or not settings.REDIS_URL:
        return
    try:
        async with redis_client() as redis:
            await redis.eval("if redis.call('GET', KEYS[1]) == ARGV[1] then return redis.call('DEL', KEYS[1]) else return 0 end", 1, key, token)
    except Exception:
        logger.exception("Could not release generation lease; it will expire")
