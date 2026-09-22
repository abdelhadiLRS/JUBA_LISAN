from types import SimpleNamespace

from app.services.lesson_mastery import summarize_lesson_mastery


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
