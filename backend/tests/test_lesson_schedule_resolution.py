"""Tests for deterministic lesson-plan resolution."""

from app.services.lesson_generator import _resolve_scheduled_lesson


def test_arabic_a1_resolves_by_unit_week_day():
    result = _resolve_scheduled_lesson(
        target_language="ar",
        cefr_level="A1",
        unit_id="a1-unit-1",
        week=1,
        day=1,
    )
    assert result is not None
    assert result["topic"] == "التحية والتعريف بالنفس"
    assert result["lesson_type"] == "grammar"
    assert "pronouns" in result["grammar_points"]
    assert "greetings_a1" in result["vocabulary_set_ids"]


def test_non_arabic_languages_keep_existing_generation_path():
    assert _resolve_scheduled_lesson(
        target_language="en-GB",
        cefr_level="A1",
        unit_id="a1-unit-1",
        week=1,
        day=1,
    ) is None


def test_missing_arabic_schedule_entry_falls_back():
    assert _resolve_scheduled_lesson(
        target_language="ar",
        cefr_level="A1",
        unit_id="a1-unit-999",
        week=1,
        day=1,
    ) is None


def test_arabic_non_a1_keeps_existing_generation_path():
    assert _resolve_scheduled_lesson(
        target_language="ar",
        cefr_level="A2",
        unit_id="a2-unit-1",
        week=1,
        day=1,
    ) is None
