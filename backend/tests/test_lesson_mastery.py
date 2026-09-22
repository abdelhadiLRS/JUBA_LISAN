from types import SimpleNamespace

from app.services.lesson_mastery import (
    select_next_mastery_candidate,
    summarize_lesson_mastery,
)


def test_lesson_mastery_aggregates_states_and_variants():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha"),
        SimpleNamespace(id=2, content_id="beta"),
        SimpleNamespace(id=3, content_id="gamma"),
        SimpleNamespace(id=4, content_id="delta"),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.8),
        SimpleNamespace(content_id="alpha", variant="b", score=0.8),
        SimpleNamespace(content_id="beta", variant="a", score=0.2),
        SimpleNamespace(content_id="gamma", variant="a", score=0.6),
    ]

    result = summarize_lesson_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
    )

    assert result.total_exercises == 4
    assert result.attempted_exercises == 3
    assert result.mastered_exercises == 1
    assert result.learning_exercises == 1
    assert result.struggling_exercises == 1
    assert result.unseen_exercises == 1
    assert result.average_mastery_score == 0.4
    assert result.attempt_rate == 0.75
    assert result.mastery_rate == 0.25
    assert result.covered_variants == 4


def test_lesson_mastery_treats_blank_or_non_string_content_as_unseen():
    exercises = [
        SimpleNamespace(content_id=""),
        SimpleNamespace(content_id=None),
    ]
    attempts = [
        SimpleNamespace(content_id="x", variant="a", score=1.0),
    ]

    result = summarize_lesson_mastery(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
    )

    assert result.attempted_exercises == 0
    assert result.unseen_exercises == 2
    assert result.average_mastery_score == 0.0
    assert result.attempt_rate == 0.0
    assert result.mastery_rate == 0.0
    assert result.covered_variants == 0


def test_lesson_mastery_rate_is_zero_for_empty_lesson():
    result = summarize_lesson_mastery(
        [],
        [],
        get_content_id=lambda item: item.content_id,
    )

    assert result.total_exercises == 0
    assert result.attempted_exercises == 0
    assert result.mastered_exercises == 0
    assert result.average_mastery_score == 0.0
    assert result.attempt_rate == 0.0
    assert result.mastery_rate == 0.0
    assert result.covered_variants == 0


def test_next_mastery_candidate_prioritizes_struggling_then_unseen_then_learning():
    exercises = [
        SimpleNamespace(id=10, content_id="learning"),
        SimpleNamespace(id=20, content_id="unseen"),
        SimpleNamespace(id=30, content_id="struggling"),
        SimpleNamespace(id=40, content_id="mastered"),
    ]
    attempts = [
        SimpleNamespace(content_id="learning", variant="a", score=0.60),
        SimpleNamespace(content_id="struggling", variant="a", score=0.20),
        SimpleNamespace(content_id="mastered", variant="a", score=0.90),
        SimpleNamespace(content_id="mastered", variant="b", score=0.90),
    ]

    result = select_next_mastery_candidate(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_exercise_id=lambda item: item.id,
    )

    assert result is not None
    assert result.exercise is exercises[2]
    assert result.mastery_state == "struggling"
    assert result.mastery_score == 0.2
    assert result.mastery_variants == 1


def test_next_mastery_candidate_uses_lowest_score_within_same_state():
    exercises = [
        SimpleNamespace(id=10, content_id="first"),
        SimpleNamespace(id=20, content_id="second"),
    ]
    attempts = [
        SimpleNamespace(content_id="first", variant="a", score=0.60),
        SimpleNamespace(content_id="second", variant="a", score=0.55),
    ]

    result = select_next_mastery_candidate(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_exercise_id=lambda item: item.id,
    )

    assert result is not None
    assert result.exercise is exercises[1]
    assert result.mastery_state == "learning"
    assert result.mastery_score == 0.55


def test_next_mastery_candidate_returns_none_when_everything_is_mastered():
    exercises = [
        SimpleNamespace(id=1, content_id="alpha"),
        SimpleNamespace(id=2, content_id="beta"),
    ]
    attempts = [
        SimpleNamespace(content_id="alpha", variant="a", score=0.90),
        SimpleNamespace(content_id="alpha", variant="b", score=0.90),
        SimpleNamespace(content_id="beta", variant="a", score=0.80),
        SimpleNamespace(content_id="beta", variant="b", score=0.80),
    ]

    assert select_next_mastery_candidate(
        exercises,
        attempts,
        get_content_id=lambda item: item.content_id,
        get_exercise_id=lambda item: item.id,
    ) is None
