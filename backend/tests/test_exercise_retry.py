from app.services.exercise_retry import get_retry_variant

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
