"""Public runtime flags and product catalog. No credentials are exposed."""
from __future__ import annotations
from fastapi import APIRouter, Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import MAINTENANCE_KEY, get_redis
from app.core.limiter import limiter
from app.models.dashboard_banner import DashboardBanner
from app.services.subscription_catalog import public_catalog

router = APIRouter(tags=["config"])


@router.get("/api/config")
@limiter.limit("60/minute")
async def get_config(request: Request, redis: Redis | None = Depends(get_redis), db: AsyncSession = Depends(get_db)) -> dict:
    maintenance = False
    try:
        if redis is not None:
            maintenance = await redis.get(MAINTENANCE_KEY) == "1"
    except Exception:
        pass
    banner_data = None
    try:
        banner = await db.get(DashboardBanner, 1)
        if banner is not None and banner.is_active:
            banner_data = {"revision": banner.revision, "translations": banner.translations}
    except Exception:
        pass
    return {"allow_registration": settings.ALLOW_REGISTRATION,
        "stripe_enabled": settings.STRIPE_ENABLED, "stripe_trial_days": 0,
        "freemium_trial_enabled": settings.FREEMIUM_TRIAL_ENABLED,
        "tts_provider": settings.TTS_PROVIDER, "openai_tts_voice": settings.OPENAI_TTS_VOICE,
        "maintenance_mode": maintenance, "price_monthly": settings.PRICE_MONTHLY,
        "price_yearly": settings.PRICE_YEARLY, "total_price_monthly": settings.TOTAL_PRICE_MONTHLY,
        "total_price_yearly": settings.TOTAL_PRICE_YEARLY, "dashboard_banner": banner_data,
        "subscription_catalog": public_catalog(settings.STRIPE_ENABLED, settings)}
