from app.routers import lessons


def test_low_score_recommends_easier_variant(monkeypatch):
    monkeypatch.setattr(
        lessons,
        "get_retry_variant",
        lambda current_variant, succeeded, available_variants: (
            "guided" if not succeeded else "challenge"
        ),
    )

    action, variant = lessons._adaptive_recommendation(
        0.49,
        "standard",
        ["guided", "standard"],
    )

    assert action == "retry_easier"
    assert variant == "guided"


def test_high_score_recommends_harder_variant(monkeypatch):
    monkeypatch.setattr(
        lessons,
        "get_retry_variant",
        lambda current_variant, succeeded, available_variants: (
            "challenge" if succeeded else "guided"
        ),
    )

    action, variant = lessons._adaptive_recommendation(
        0.80,
        "standard",
        ["standard", "challenge"],
    )

    assert action == "advance_harder"
    assert variant == "challenge"


def test_middle_score_reinforces_without_variant():
    action, variant = lessons._adaptive_recommendation(
        0.65,
        "standard",
        ["guided", "standard", "challenge"],
    )

    assert action == "reinforce"
    assert variant is None


def test_missing_easier_variant_falls_back_to_reinforce(monkeypatch):
    monkeypatch.setattr(
        lessons,
        "get_retry_variant",
        lambda current_variant, succeeded, available_variants: None,
    )

    action, variant = lessons._adaptive_recommendation(
        0.20,
        "guided",
        ["guided"],
    )

    assert action == "reinforce"
    assert variant is None


def test_missing_harder_variant_falls_back_to_advance(monkeypatch):
    monkeypatch.setattr(
        lessons,
        "get_retry_variant",
        lambda current_variant, succeeded, available_variants: None,
    )

    action, variant = lessons._adaptive_recommendation(
        0.95,
        "challenge",
        ["challenge"],
    )

    assert action == "advance"
    assert variant is None


def test_half_score_stays_in_reinforce_band():
    action, variant = lessons._adaptive_recommendation(
        0.50,
        "standard",
        ["guided", "standard", "challenge"],
    )

    assert action == "reinforce"
    assert variant is None


def test_thresholds_are_deterministic_at_eighty_percent(monkeypatch):
    monkeypatch.setattr(
        lessons,
        "get_retry_variant",
        lambda current_variant, succeeded, available_variants: "challenge" if succeeded else "guided",
    )

    action, variant = lessons._adaptive_recommendation(
        0.80,
        "standard",
        ["guided", "standard", "challenge"],
    )

    assert action == "advance_harder"
    assert variant == "challenge"
