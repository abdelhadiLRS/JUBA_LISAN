from types import SimpleNamespace
from app.services.subscription_catalog import product_settings, verified_price_tier


def test_old_price_retains_plus_when_new_plus_prices_are_configured(monkeypatch):
    monkeypatch.setattr(product_settings, "STRIPE_PRICE_PLUS_MONTHLY", "new_plus")
    monkeypatch.setattr(product_settings, "STRIPE_PRICE_GO_MONTHLY", "go_price")
    legacy = SimpleNamespace(STRIPE_PRICE_MONTHLY="old_paid", STRIPE_PRICE_YEARLY="old_yearly")
    sub = {"items": {"data": [{"price": {"id": "old_paid"}}]}}
    assert verified_price_tier(sub, lambda obj, key, default=None: obj.get(key, default), legacy) == "plus"


def test_ambiguous_price_mapping_is_rejected(monkeypatch):
    monkeypatch.setattr(product_settings, "STRIPE_PRICE_GO_MONTHLY", "duplicate")
    legacy = SimpleNamespace(STRIPE_PRICE_MONTHLY="duplicate", STRIPE_PRICE_YEARLY="")
    sub = {"items": {"data": [{"price": {"id": "duplicate"}}]}}
    assert verified_price_tier(sub, lambda obj, key, default=None: obj.get(key, default), legacy) is None
