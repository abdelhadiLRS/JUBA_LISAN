"""Account-wide product entitlements, independent of billing interval.

Prices are EUR minor units. Stripe product IDs are deployment configuration,
never browser-controlled. Legacy paid accounts retain Plus during migration.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from typing import Literal

from pydantic_settings import BaseSettings

Tier = Literal["free", "go", "plus"]
Interval = Literal["monthly", "yearly"]


class ProductSettings(BaseSettings):
    STRIPE_PRICE_GO_MONTHLY: str = ""
    STRIPE_PRICE_GO_YEARLY: str = ""
    STRIPE_PRICE_PLUS_MONTHLY: str = ""
    STRIPE_PRICE_PLUS_YEARLY: str = ""
    model_config = {"env_file": ".env", "extra": "ignore"}


product_settings = ProductSettings()


@dataclass(frozen=True)
class Allowance:
    limit: int
    period: Literal["day", "week", "month"]
    unit: Literal["requests", "cards", "seconds"] = "requests"


LIMITS: dict[str, dict[str, Allowance]] = {
    "free": {
        "chat": Allowance(5, "day"), "lessons": Allowance(1, "day"),
        "reading": Allowance(2, "week"), "listening": Allowance(2, "week"),
        "flashcards": Allowance(20, "week", "cards"),
        "translation": Allowance(5, "day"),
        "voice": Allowance(300, "month", "seconds"),
        "tts": Allowance(300, "month", "seconds"),
    },
    "go": {
        "chat": Allowance(40, "day"), "lessons": Allowance(5, "day"),
        "reading": Allowance(15, "week"), "listening": Allowance(10, "week"),
        "flashcards": Allowance(150, "week", "cards"),
        "translation": Allowance(30, "day"),
        "voice": Allowance(3600, "month", "seconds"),
        "tts": Allowance(1800, "month", "seconds"),
    },
    "plus": {
        "chat": Allowance(120, "day"), "lessons": Allowance(15, "day"),
        "reading": Allowance(40, "week"), "listening": Allowance(25, "week"),
        "flashcards": Allowance(400, "week", "cards"),
        "translation": Allowance(100, "day"),
        "voice": Allowance(10800, "month", "seconds"),
        "tts": Allowance(5400, "month", "seconds"),
    },
}
PRICES = {"free": {"monthly": 0, "yearly": 0},
          "go": {"monthly": 799, "yearly": 7999},
          "plus": {"monthly": 1499, "yearly": 14999}}
SESSION_SECONDS = {"free": 300, "go": 900, "plus": 1800}
TRIAL_DAYS = 7
MAX_CHAT_CHARS = 2000
MAX_TRANSLATION_CHARS = 1000
MAX_FLASHCARDS_PER_REQUEST = 20


def utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def effective_tier(user, *, now: datetime | None = None, trial_enabled: bool = True) -> Tier:
    """Only verified paid state or a server-issued trial grants paid entitlements."""
    now = utc(now or datetime.now(UTC))
    tier = getattr(user, "subscription_tier", "free")
    if getattr(user, "subscription_status", "none") in ("active", "trialing"):
        # Legacy accounts predate tier storage and were previously unrestricted.
        return tier if tier in ("go", "plus") else "plus"
    end = getattr(user, "freemium_trial_ends_at", None)
    if trial_enabled and end is not None and utc(end) > now:
        return "go"
    return "free"


def period_bounds(period: str, now: datetime | None = None) -> tuple[datetime, datetime]:
    now = utc(now or datetime.now(UTC))
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == "day":
        return start, start + timedelta(days=1)
    if period == "week":
        start -= timedelta(days=start.weekday())
        return start, start + timedelta(days=7)
    if period == "month":
        start = start.replace(day=1)
        end = start.replace(year=start.year + 1, month=1) if start.month == 12 else start.replace(month=start.month + 1)
        return start, end
    raise ValueError("Unknown quota period")


def price_id(tier: str, interval: str, legacy_settings=None) -> str:
    if tier not in ("go", "plus") or interval not in ("monthly", "yearly"):
        return ""
    configured = getattr(product_settings, f"STRIPE_PRICE_{tier.upper()}_{interval.upper()}")
    # Existing Plus product remains usable without replacing a live price.
    if not configured and tier == "plus" and legacy_settings is not None:
        configured = getattr(legacy_settings, f"STRIPE_PRICE_{interval.upper()}", "")
    return configured


def verified_price_tier(subscription, get, legacy_settings) -> Tier | None:
    """Resolve from signed webhook price IDs, never metadata or client tier alone."""
    data = get(get(subscription, "items", {}), "data", []) or []
    if len(data) != 1:
        return None
    price = get(data[0], "price")
    identifier = price if isinstance(price, str) else get(price, "id")
    matches = {tier for tier in ("go", "plus") for interval in ("monthly", "yearly")
               if identifier and identifier == price_id(tier, interval, legacy_settings)}
    return next(iter(matches)) if len(matches) == 1 else None


def public_catalog(stripe_enabled: bool, legacy_settings=None) -> dict:
    return {
        "currency": "EUR", "trial": {"tier": "go", "days": TRIAL_DAYS, "card_required": False},
        "metered": stripe_enabled, "quota_scope": "account", "reset_timezone": "UTC",
        "rollover": False, "paid_xp_bonus": False,
        "request_limits": {"chat_characters": MAX_CHAT_CHARS,
                           "translation_characters": MAX_TRANSLATION_CHARS,
                           "flashcards": MAX_FLASHCARDS_PER_REQUEST},
        "plans": [{"tier": tier, "prices": PRICES[tier],
                   "checkout_available": {interval: bool(stripe_enabled and price_id(tier, interval, legacy_settings))
                                          for interval in ("monthly", "yearly")},
                   "voice_session_max_seconds": SESSION_SECONDS[tier],
                   "allowances": {name: asdict(limit) for name, limit in LIMITS[tier].items()}}
                  for tier in ("free", "go", "plus")],
    }
