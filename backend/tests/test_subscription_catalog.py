from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from app.services.subscription_catalog import (
    LIMITS, PRICES, SESSION_SECONDS, effective_tier, period_bounds, verified_price_tier,
)


def user(**kwargs):
    return SimpleNamespace(subscription_status=kwargs.get("status", "none"), subscription_tier=kwargs.get("tier", "free"), freemium_trial_ends_at=kwargs.get("end"))


@pytest.mark.parametrize("tier", ["go", "plus"])
def test_paid_tiers(tier):
    assert effective_tier(user(status="active", tier=tier)) == tier


def test_untrusted_tier_is_not_entitlement():
    assert effective_tier(user(tier="plus")) == "free"
    assert effective_tier(user(status="past_due", tier="plus")) == "free"
    assert effective_tier(user(status="active")) == "plus"


def test_trial_is_go_not_unlimited():
    now = datetime(2026, 10, 3, tzinfo=UTC)
    assert effective_tier(user(end=datetime(2026, 10, 4)), now=now) == "go"
    assert effective_tier(user(end=now), now=now) == "free"
    assert effective_tier(user(end=datetime(2026, 10, 4)), now=now, trial_enabled=False) == "free"


def test_approved_catalog():
    assert PRICES["go"] == {"monthly": 799, "yearly": 7999}
    assert PRICES["plus"] == {"monthly": 1499, "yearly": 14999}
    assert SESSION_SECONDS == {"free": 300, "go": 900, "plus": 1800}
    for tier, cards in (("free", 20), ("go", 150), ("plus", 400)):
        assert LIMITS[tier]["flashcards"].limit == cards
        assert LIMITS[tier]["voice"].period == "month"


@pytest.mark.parametrize("now,period,start,end", [
    (datetime(2026, 10, 3, 10), "week", datetime(2026, 9, 28), datetime(2026, 10, 5)),
    (datetime(2026, 12, 31, 23), "month", datetime(2026, 12, 1), datetime(2027, 1, 1)),
    (datetime(2028, 2, 29, 23), "month", datetime(2028, 2, 1), datetime(2028, 3, 1)),
])
def test_periods(now, period, start, end):
    assert period_bounds(period, now) == (start.replace(tzinfo=UTC), end.replace(tzinfo=UTC))


def test_unknown_stripe_price_does_not_grant_access(monkeypatch):
    monkeypatch.setattr("app.services.subscription_catalog.price_id", lambda *args: "known")
    sub = {"metadata": {"tier": "plus"}, "items": {"data": [{"price": {"id": "unknown"}}]}}
    assert verified_price_tier(sub, lambda obj, key, default=None: obj.get(key, default), None) is None
