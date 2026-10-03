"""Subscription state compatibility; feature limits live in the tier catalog."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models.user import User
from app.services.subscription_catalog import SESSION_SECONDS, effective_tier


def is_subscribed(user: User, stripe_enabled: bool) -> bool:
    """Paid status only, not a claim that AI usage is unlimited."""
    return not stripe_enabled or user.subscription_status in ("trialing", "active")


async def apply_subscription_quotas(user: User, db: AsyncSession) -> None:
    user.conversation_weekly_sessions = settings.DEFAULT_CONVERSATION_WEEKLY_SESSIONS
    user.conversation_weekly_minutes = settings.DEFAULT_CONVERSATION_WEEKLY_MINUTES
    user.conversation_daily_minutes = settings.DEFAULT_CONVERSATION_DAILY_MINUTES
    user.monthly_tokens_limit = settings.DEFAULT_MONTHLY_TOKENS_LIMIT
    user.conversation_max_duration = SESSION_SECONDS[effective_tier(user, trial_enabled=settings.FREEMIUM_TRIAL_ENABLED)] if settings.STRIPE_ENABLED else settings.DEFAULT_CONVERSATION_MAX_DURATION
    user.conversation_inactivity_timeout = settings.DEFAULT_CONVERSATION_INACTIVITY_TIMEOUT
    await db.commit()
