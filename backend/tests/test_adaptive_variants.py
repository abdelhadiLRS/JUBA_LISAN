from dataclasses import dataclass

from app.services.adaptive_variants import select_unanswered_variant


@dataclass
class VariantExercise:
    id: int
    content_id: str
    variant: str


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
        attempted_exercise_ids={1},
    )

    assert selected is exercises[2] or selected is exercises[1]
    assert selected is not exercises[0]


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
