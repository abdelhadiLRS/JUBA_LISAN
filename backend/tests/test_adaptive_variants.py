from dataclasses import dataclass

from app.services.exercise_retry import classify_score
from app.services.adaptive_variants import (
    collect_attempted_exercise_ids,
    select_unanswered_variant,
    recommend_adaptive_variant,
)


def test_classify_score_uses_stable_boundaries():
    assert classify_score(0.49) == "low"
    assert classify_score(0.50) == "middle"
    assert classify_score(0.79) == "middle"
    assert classify_score(0.80) == "success"


def test_classify_score_accepts_out_of_range_scores_deterministically():
    assert classify_score(-1.0) == "low"
    assert classify_score(1.5) == "success"


@dataclass
class VariantExercise:
    id: int
    content_id: str
    variant: str


@dataclass
class Attempt:
    exercise_id: int


def test_collect_attempted_exercise_ids_deduplicates_history():
    attempts = [Attempt(1), Attempt(2), Attempt(1)]

    assert collect_attempted_exercise_ids(attempts) == {1, 2}


def test_collect_attempted_exercise_ids_ignores_invalid_ids():
    attempts = [Attempt(1), Attempt(0), Attempt(-2), Attempt("3")]

    assert collect_attempted_exercise_ids(attempts) == {1}


def test_collect_attempted_exercise_ids_rejects_boolean_ids():
    attempts = [Attempt(True), Attempt(False), Attempt(2)]

    assert collect_attempted_exercise_ids(attempts) == {2}


def test_collect_attempted_exercise_ids_supports_custom_getter():
    attempts = [{"exercise": 4}, {"exercise": 5}, {"exercise": 4}]

    assert (
        collect_attempted_exercise_ids(
            attempts,
            get_exercise_id=lambda item: item["exercise"],
        )
        == {4, 5}
    )


def test_selector_rejects_boolean_candidate_ids():
    exercises = [
        {"id": True, "content_id": "c1", "variant": "multiple_choice"},
        {"id": 2, "content_id": "c1", "variant": "fill_blank"},
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={1},
        get_exercise_id=lambda item: item["id"],
        get_variant=lambda item: item["variant"],
        get_content_id=lambda item: item["content_id"],
    )

    assert selected is exercises[1]


def test_selector_ignores_boolean_attempt_history_ids():
    exercises = [
        {"id": 1, "content_id": "c1", "variant": "translate"},
        {"id": 2, "content_id": "c1", "variant": "free_write"},
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="fill_blank",
        succeeded=True,
        attempted_exercise_ids={True},
        get_exercise_id=lambda item: item["id"],
        get_variant=lambda item: item["variant"],
        get_content_id=lambda item: item["content_id"],
    )

    assert selected is exercises[0]


def test_selector_rejects_non_positive_candidate_ids():
    exercises = [
        {"id": 0, "content_id": "c1", "variant": "multiple_choice"},
        {"id": 2, "content_id": "c1", "variant": "fill_blank"},
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={0},
        get_exercise_id=lambda item: item["id"],
        get_variant=lambda item: item["variant"],
        get_content_id=lambda item: item["content_id"],
    )

    assert selected is exercises[1]


def test_selects_adjacent_easier_unanswered_variant():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "translate"),
        VariantExercise(4, "c1", "free_write"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="free_write",
        succeeded=False,
        attempted_exercise_ids={4},
    )

    assert selected is exercises[2]


def test_selects_adjacent_harder_unanswered_variant():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "translate"),
        VariantExercise(4, "c1", "free_write"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={1},
    )

    assert selected is exercises[1]


def test_never_crosses_stable_content_identity():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c2", "fill_blank"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={1},
    )

    assert selected is None


def test_attempted_sibling_is_skipped():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "translate"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={1, 2},
    )

    assert selected is None


def test_variant_aliases_are_normalized_before_selection():
    exercises = [
        VariantExercise(1, "c1", "multiple-choice"),
        VariantExercise(2, "c1", "fill-blank"),
        VariantExercise(3, "c1", "free-write"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple-choice",
        succeeded=True,
        attempted_exercise_ids={1},
    )

    assert selected is exercises[1]


def test_empty_content_identity_is_rejected():
    exercises = [VariantExercise(1, "c1", "multiple_choice")]

    assert (
        select_unanswered_variant(
            exercises,
            content_id=" ",
            current_variant="multiple_choice",
            succeeded=True,
            attempted_exercise_ids={1},
        )
        is None
    )


def test_selector_supports_lesson_metadata_callbacks():
    exercises = [
        {"id": 1, "meta": {"content_id": "c1", "variant": "multiple-choice"}},
        {"id": 2, "meta": {"content_id": "c1", "variant": "fill-blank"}},
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={1},
        get_exercise_id=lambda item: item["id"],
        get_variant=lambda item: item["meta"]["variant"],
        get_content_id=lambda item: item["meta"]["content_id"],
    )

    assert selected is exercises[1]


def test_attempt_history_blocks_a_variant_even_when_exercise_is_unanswered():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "translate"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={1, 2},
    )

    assert selected is None


def test_duplicate_variant_rows_keep_the_first_unattempted_match():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "fill-blank"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={1, 2},
    )

    assert selected is exercises[2]


def test_unknown_sibling_variants_do_not_affect_difficulty_selection():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "experimental_variant"),
        VariantExercise(3, "c1", "fill_blank"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={1},
    )

    assert selected is exercises[2]

def test_recommendation_returns_action_variant_and_target_from_same_selection():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "translate"),
    ]

    action, variant, target = recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score=0.90,
        attempted_exercise_ids={1},
    )

    assert action == "advance_harder"
    assert variant == "fill_blank"
    assert target == exercises[1]


def test_recommendation_never_returns_an_attempted_target():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "translate"),
    ]

    action, variant, target = recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score=0.90,
        attempted_exercise_ids={1, 2},
    )

    assert action == "advance_harder"
    assert variant == "translate"
    assert target == exercises[2]


def test_recommendation_normalizes_target_alias():
    exercises = [
        VariantExercise(1, "c1", "multiple-choice"),
        VariantExercise(2, "c1", "fill-blank"),
    ]

    action, variant, target = recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple-choice",
        score=0.90,
        attempted_exercise_ids={1},
    )

    assert action == "advance_harder"
    assert variant == "fill_blank"
    assert target == exercises[1]


def test_recommendation_reinforces_middle_score_without_target():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
    ]

    assert recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score=0.79,
    ) == ("reinforce", None, None)

def test_recommendation_uses_shared_score_boundaries():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "translate"),
    ]

    assert recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="translate",
        score=0.50,
    ) == ("reinforce", None, None)

    action, variant, target = recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score=0.80,
        attempted_exercise_ids={1},
    )
    assert action == "advance_harder"
    assert variant == "fill_blank"
    assert target is exercises[1]


def test_recommendation_returns_easier_variant_for_low_score():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "translate"),
    ]

    action, variant, target = recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="translate",
        score=0.20,
        attempted_exercise_ids={3},
    )

    assert action == "retry_easier"
    assert variant == "fill_blank"
    assert target is exercises[1]


def test_recommendation_falls_back_when_all_directional_variants_were_attempted():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
    ]

    assert recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score=0.95,
        attempted_exercise_ids={1, 2},
    ) == ("advance", None, None)

