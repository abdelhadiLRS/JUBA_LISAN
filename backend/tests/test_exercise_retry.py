from app.services.exercise_retry import (
    classify_score,
    get_retry_variant,
    normalise_variant,
)


def test_failed_exercise_moves_to_nearest_easier_variant():
    assert get_retry_variant(
        "free_write", succeeded=False,
        available_variants=["multiple_choice", "fill_blank", "translate", "free_write"],
    ) == "translate"


def test_success_moves_to_nearest_harder_variant():
    assert get_retry_variant(
        "multiple_choice", succeeded=True,
        available_variants=["multiple_choice", "fill_blank", "translate"],
    ) == "fill_blank"


def test_retry_is_bounded_at_edges():
    assert get_retry_variant("multiple_choice", succeeded=False, available_variants=["multiple_choice"]) is None
    assert get_retry_variant("free_write", succeeded=True, available_variants=["free_write"]) is None


def test_aliases_are_supported():
    assert get_retry_variant("writing", succeeded=False, available_variants=["gap", "writing"]) == "fill_blank"


def test_unknown_variants_are_safe():
    assert get_retry_variant("unknown", succeeded=False, available_variants=["multiple_choice"]) is None


def test_hyphenated_and_underscored_aliases_normalize():
    assert get_retry_variant(
        "free-write",
        succeeded=False,
        available_variants=["multiple-choice", "fill_blank", "free_write"],
    ) == "fill_blank"


def test_variant_normalization_is_case_and_separator_insensitive():
    assert normalise_variant("  FREE_WRITE  ") == "free_write"
    assert normalise_variant(" Multiple-Choice ") == "multiple_choice"
    assert normalise_variant(None) == ""


def test_malformed_variant_values_are_ignored():
    assert normalise_variant(1) == ""
    assert normalise_variant(True) == ""
    assert normalise_variant(object()) == ""
    assert get_retry_variant(
        "fill_blank",
        succeeded=False,
        available_variants=[True, 1, "multiple-choice", None, "fill_blank"],
    ) == "multiple_choice"


def test_duplicate_aliases_do_not_change_selection():
    assert get_retry_variant(
        "fill_blank",
        succeeded=False,
        available_variants=["multiple-choice", "choice", "multiple_choice", "fill-blank"],
    ) == "multiple_choice"


def test_score_classification_uses_canonical_boundaries():
    assert classify_score(0.0) == "low"
    assert classify_score(0.49) == "low"
    assert classify_score(0.50) == "middle"
    assert classify_score(0.79) == "middle"
    assert classify_score(0.80) == "success"
    assert classify_score(1.0) == "success"


def test_score_classification_is_monotonic_at_decimal_boundaries():
    assert classify_score(0.499999) == "low"
    assert classify_score(0.500001) == "middle"
    assert classify_score(0.799999) == "middle"
    assert classify_score(0.800001) == "success"
