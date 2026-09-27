"""Tests for deterministic English speaking fallback content."""

from app.services.lesson_generator import _fallback_lesson


def test_english_a2_speaking_fallback_is_available() -> None:
    lesson = _fallback_lesson(
        cefr_level="A2",
        lesson_type="speaking",
        topic="Travel & Transport",
        unit_id="a2-unit-7",
        target_language="en-GB",
    )
    assert lesson is not None
    assert lesson.lesson_type == "speaking"
    assert lesson.exercises
    assert lesson.exercises[0].type == "free_write"
    assert "Travel & Transport" in lesson.title


def test_english_c2_speaking_fallback_is_nuanced() -> None:
    lesson = _fallback_lesson(
        cefr_level="C2",
        lesson_type="speaking",
        topic="Academic Style",
        unit_id="c2-unit-2",
        target_language="en-US",
    )
    assert lesson is not None
    assert lesson.cefr_level == "C2"
    assert lesson.explanation["guidance"]
    assert lesson.exercises[0].correct


def test_non_english_speaking_does_not_use_english_fallback() -> None:
    lesson = _fallback_lesson(
        cefr_level="B2",
        lesson_type="speaking",
        topic="Test",
        unit_id="b2-unit-1",
        target_language="fr",
    )
    assert lesson is None
