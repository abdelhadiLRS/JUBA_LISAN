from app.services.exercise_retry import get_retry_variant, normalise_variant
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


def test_whitespace_separators_normalize_to_canonical_variants():
    assert normalise_variant(" free   write ") == "free-write"
    assert normalise_variant("multiple_choice") == "multiple-choice"


def test_easy_to_hard_chain_uses_adjacent_difficulty():
    variants = ["multiple_choice", "fill_blank", "translate", "free_write"]

    assert get_retry_variant("multiple_choice", succeeded=True, available_variants=variants) == "fill_blank"
    assert get_retry_variant("fill_blank", succeeded=True, available_variants=variants) == "translate"
    assert get_retry_variant("translate", succeeded=True, available_variants=variants) == "free-write"


def test_hard_to_easy_chain_uses_adjacent_difficulty():
    variants = ["multiple_choice", "fill_blank", "translate", "free_write"]

    assert get_retry_variant("free_write", succeeded=False, available_variants=variants) == "translate"
    assert get_retry_variant("translate", succeeded=False, available_variants=variants) == "fill_blank"
    assert get_retry_variant("fill_blank", succeeded=False, available_variants=variants) == "multiple-choice"
