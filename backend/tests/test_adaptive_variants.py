from dataclasses import dataclass

from app.services.exercise_retry import classify_score
from app.services.adaptive_variants import (
    collect_attempted_adaptive_identities,
    collect_attempted_exercise_ids,
    recommend_adaptive_action,
    select_unanswered_variant,
    summarize_adaptive_mastery,
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
    content_id: str | None = None
    variant: str | None = None



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


def test_collect_attempted_adaptive_identities_canonicalize_history():
    attempts = [
        Attempt(1, " c1 ", "Fill-Blank"),
        Attempt(2, "c1", "fill_blank"),
        Attempt(3, "c2", "multiple-choice"),
        Attempt(4, None, "translate"),
    ]

    assert collect_attempted_adaptive_identities(attempts) == {
        ("c1", "fill_blank"),
        ("c2", "multiple_choice"),
    }


def test_selector_skips_regenerated_duplicate_variant_by_identity():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "fill-blank"),
        VariantExercise(4, "c1", "translate"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={1, 2},
        attempted_adaptive_identities={("c1", "fill_blank")},
    )

    assert selected is exercises[3]


def test_selector_accepts_malformed_adaptive_identity_history():
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
        attempted_adaptive_identities=[
            ("c1", "fill_blank"),
            ("", "translate"),
            ("c1", True),
            "invalid",
        ],
    )

    assert selected is exercises[2]



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


def test_recommend_adaptive_action_rejects_boolean_scores():
    import pytest

    with pytest.raises(ValueError, match="score must be numeric"):
        recommend_adaptive_action(True, "multiple_choice", ["fill_blank"])


def test_recommend_adaptive_variant_rejects_boolean_scores():
    import pytest

    with pytest.raises(ValueError, match="score must be numeric"):
        recommend_adaptive_variant(
            [VariantExercise(1, "c1", "multiple_choice")],
            content_id="c1",
            current_variant="multiple_choice",
            score=False,
        )


def test_recommend_adaptive_action_normalizes_runtime_score_values():
    assert recommend_adaptive_action(
        "0.90",
        "multiple_choice",
        ["fill_blank"],
    ) == ("advance_harder", "fill_blank")


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



def test_selector_accepts_malformed_attempt_history_collections():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids=["1", True, 0, 1, 2.0],
    )

    assert selected is exercises[1]



def test_selector_rejects_string_and_float_candidate_ids():
    exercises = [
        {"id": "1", "content_id": "c1", "variant": "multiple_choice"},
        {"id": 2.0, "content_id": "c1", "variant": "fill_blank"},
        {"id": 3, "content_id": "c1", "variant": "translate"},
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={"1", 2.0},
        get_exercise_id=lambda item: item["id"],
        get_variant=lambda item: item["variant"],
        get_content_id=lambda item: item["content_id"],
    )

    assert selected is exercises[2]



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


def test_recommendation_accepts_runtime_history_collections():
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
        attempted_exercise_ids=["1", True, 1, 2.0],
    )

    assert action == "advance_harder"
    assert variant == "translate"
    assert target is exercises[2]



def test_recommendation_accepts_missing_attempt_history():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
    ]

    action, variant, target = recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score=0.90,
    )

    assert action == "advance_harder"
    assert variant == "fill_blank"
    assert target is exercises[1]


def test_selector_ignores_malformed_variant_values():
    exercises = [
        {"id": 1, "content_id": "c1", "variant": "multiple_choice"},
        {"id": 2, "content_id": "c1", "variant": True},
        {"id": 3, "content_id": "c1", "variant": "fill_blank"},
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

    assert selected is exercises[2]

def test_low_score_falls_back_when_all_easier_variants_were_attempted():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "translate"),
    ]

    assert recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="translate",
        score=0.20,
        attempted_exercise_ids={1, 2, 3},
    ) == ("reinforce", None, None)


def test_recommendation_ignores_attempts_from_other_lessons_via_caller_history():
    exercises = [
        VariantExercise(10, "c1", "multiple_choice"),
        VariantExercise(11, "c1", "fill_blank"),
    ]

    action, variant, target = recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score=0.90,
        attempted_exercise_ids={99},
    )

    assert action == "advance_harder"
    assert variant == "fill_blank"
    assert target is exercises[1]

def test_recommend_adaptive_action_uses_shared_boundaries_without_rows():
    assert recommend_adaptive_action(0.49, "translate") == ("retry_easier", "fill_blank")
    assert recommend_adaptive_action(0.50, "translate") == ("reinforce", None)
    assert recommend_adaptive_action(0.79, "translate") == ("reinforce", None)
    assert recommend_adaptive_action(0.80, "multiple_choice") == ("advance", None)


def test_recommend_adaptive_action_selects_directional_variant_when_available():
    assert recommend_adaptive_action(
        0.20,
        "translate",
        ["multiple_choice", "fill_blank", "translate"],
    ) == ("retry_easier", "fill_blank")
    assert recommend_adaptive_action(
        0.90,
        "multiple_choice",
        ["multiple_choice", "fill_blank", "translate"],
    ) == ("advance_harder", "fill_blank")



def test_recommend_adaptive_action_ignores_malformed_available_variants():
    assert recommend_adaptive_action(
        0.20,
        "translate",
        [True, None, "", "fill_blank", "fill_blank"],
    ) == ("retry_easier", "fill_blank")


def test_recommend_adaptive_action_returns_none_for_unknown_current_variant():
    assert recommend_adaptive_action(0.90, "unknown_variant", ["fill_blank"]) == (
        "advance",
        None,
    )

def test_selector_trims_content_identity_before_matching():
    exercises = [
        VariantExercise(1, " c1 ", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
    ]

    selected = select_unanswered_variant(
        exercises,
        content_id=" c1 ",
        current_variant="multiple_choice",
        succeeded=True,
        attempted_exercise_ids={1},
    )

    assert selected is exercises[1]


def test_recommend_adaptive_action_middle_score_ignores_malformed_variants():
    assert recommend_adaptive_action(0.60, "translate", [True, None, "fill_blank"]) == (
        "reinforce",
        None,
    )



def test_recommend_adaptive_action_accepts_numeric_score_values():
    assert recommend_adaptive_action("0.90", "multiple_choice", ["fill_blank"]) == (
        "advance_harder",
        "fill_blank",
    )

def test_recommendation_accepts_numeric_string_score_values():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
    ]

    action, variant, target = recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score="0.90",
        attempted_exercise_ids={1},
    )

    assert action == "advance_harder"
    assert variant == "fill_blank"
    assert target is exercises[1]


def test_recommendation_preserves_boundary_semantics_for_numeric_strings():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
    ]

    assert recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score="0.50",
    ) == ("reinforce", None, None)

    action, variant, target = recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score="0.80",
        attempted_exercise_ids={1},
    )
    assert action == "advance_harder"
    assert variant == "fill_blank"
    assert target is exercises[1]
\n

def test_recommend_adaptive_action_rejects_non_finite_scores():
    import pytest

    with pytest.raises(ValueError, match="score must be finite"):
        recommend_adaptive_action(float("nan"), "multiple_choice", ["fill_blank"])

    with pytest.raises(ValueError, match="score must be finite"):
        recommend_adaptive_action(float("inf"), "multiple_choice", ["fill_blank"])

    with pytest.raises(ValueError, match="score must be finite"):
        recommend_adaptive_action(float("-inf"), "multiple_choice", ["fill_blank"])


def test_recommendation_rejects_non_finite_scores():
    import pytest

    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
    ]

    with pytest.raises(ValueError, match="score must be finite"):
        recommend_adaptive_variant(
            exercises,
            content_id="c1",
            current_variant="multiple_choice",
            score=float("nan"),
        )

def test_recommend_adaptive_action_rejects_non_finite_numeric_strings():
    import pytest

    for value in ("nan", "NaN", "inf", "-inf", "Infinity", "-Infinity"):
        with pytest.raises(ValueError, match="score must be finite"):
            recommend_adaptive_action(value, "multiple_choice", ["fill_blank"])


def test_recommendation_rejects_non_finite_numeric_strings():
    import pytest

    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
    ]

    for value in ("nan", "inf", "-inf"):
        with pytest.raises(ValueError, match="score must be finite"):
            recommend_adaptive_variant(
                exercises,
                content_id="c1",
                current_variant="multiple_choice",
                score=value,
            )


def test_mastery_uses_best_score_once_per_distinct_variant():
    attempts = [
        {"content_id": "c1", "variant": "multiple-choice", "score": 1.0},
        {"content_id": "c1", "variant": "multiple-choice", "score": 0.2},
        {"content_id": "c1", "variant": "fill_blank", "score": 0.8},
        {"content_id": "other", "variant": "translate", "score": 1.0},
    ]

    score, state, covered = summarize_adaptive_mastery(
        attempts,
        content_id="c1",
        get_content_id=lambda item: item["content_id"],
        get_variant=lambda item: item["variant"],
        get_score=lambda item: item["score"],
    )

    assert score == 0.9
    assert state == "mastered"
    assert covered == 2


def test_mastery_distinguishes_struggling_from_learning():
    attempts = [
        {"content_id": "c1", "variant": "multiple_choice", "score": 0.4},
        {"content_id": "c1", "variant": "fill_blank", "score": 0.6},
    ]

    assert summarize_adaptive_mastery(
        attempts,
        content_id="c1",
        get_content_id=lambda item: item["content_id"],
        get_variant=lambda item: item["variant"],
        get_score=lambda item: item["score"],
    ) == (0.5, "learning", 2)

    score, state, covered = summarize_adaptive_mastery(
        [{"content_id": "c1", "variant": "multiple_choice", "score": 0.3}],
        content_id="c1",
        get_content_id=lambda item: item["content_id"],
        get_variant=lambda item: item["variant"],
        get_score=lambda item: item["score"],
    )
    assert (score, state, covered) == (0.3, "struggling", 1)


def test_mastery_ignores_invalid_scores_and_empty_identity():
    attempts = [
        {"content_id": "c1", "variant": "translate", "score": float("nan")},
        {"content_id": "c1", "variant": True, "score": 1.0},
    ]

    assert summarize_adaptive_mastery(
        attempts,
        content_id="c1",
        get_content_id=lambda item: item["content_id"],
        get_variant=lambda item: item["variant"],
        get_score=lambda item: item["score"],
    ) == (0.0, "unseen", 0)

    assert summarize_adaptive_mastery(attempts, content_id=" ") == (0.0, "unseen", 0)


def test_middle_score_advances_after_mastery_is_established():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
        VariantExercise(3, "c1", "translate"),
    ]
    history = [
        {"content_id": "c1", "variant": "multiple_choice", "score": 0.90},
        {"content_id": "c1", "variant": "fill_blank", "score": 0.85},
    ]

    assert recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="fill_blank",
        score=0.70,
        attempt_history=history,
        attempted_exercise_ids={1, 2},
        attempted_adaptive_identities={("c1", "multiple_choice"), ("c1", "fill_blank")},
    ) == ("advance", None, None)


def test_middle_score_stays_reinforcement_before_mastery():
    exercises = [
        VariantExercise(1, "c1", "multiple_choice"),
        VariantExercise(2, "c1", "fill_blank"),
    ]
    history = [
        {"content_id": "c1", "variant": "multiple_choice", "score": 0.90},
    ]

    assert recommend_adaptive_variant(
        exercises,
        content_id="c1",
        current_variant="multiple_choice",
        score=0.70,
        attempt_history=history,
        attempted_exercise_ids={1},
        attempted_adaptive_identities={("c1", "multiple_choice")},
    ) == ("reinforce", None, None)


def test_mastery_boundaries_require_threshold_score_and_variant_coverage():
    base = [
        {"content_id": "c1", "variant": "multiple_choice", "score": 0.80},
        {"content_id": "c1", "variant": "fill_blank", "score": 0.80},
    ]

    assert summarize_adaptive_mastery(
        base,
        content_id="c1",
        get_content_id=lambda item: item["content_id"],
        get_variant=lambda item: item["variant"],
        get_score=lambda item: item["score"],
    ) == (0.80, "mastered", 2)

    assert summarize_adaptive_mastery(
        [*base, {"content_id": "c1", "variant": "translate", "score": 0.20}],
        content_id="c1",
        get_content_id=lambda item: item["content_id"],
        get_variant=lambda item: item["variant"],
        get_score=lambda item: item["score"],
    ) == (0.60, "learning", 3)

    assert summarize_adaptive_mastery(
        [{"content_id": "c1", "variant": "multiple_choice", "score": 0.80}],
        content_id="c1",
        get_content_id=lambda item: item["content_id"],
        get_variant=lambda item: item["variant"],
        get_score=lambda item: item["score"],
    ) == (0.80, "learning", 1)
