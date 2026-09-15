from app.schemas.study_plan import TodayLesson


def test_today_lesson_normalizes_unknown_type():
    lesson = TodayLesson(
        title="Malformed lesson",
        lesson_type="unknown_type",
        week=1,
        day=1,
        objectives=["valid", 123, None],
        estimated_minutes=0,
    )

    assert lesson.lesson_type == "review"
    assert lesson.objectives == ["valid"]
    assert lesson.estimated_minutes == 25


def test_today_lesson_normalizes_type_case_and_minutes():
    lesson = TodayLesson(
        title="Grammar",
        lesson_type="  GRAMMAR ",
        week=1,
        day=1,
        objectives=[],
        estimated_minutes=30.9,
    )

    assert lesson.lesson_type == "grammar"
    assert lesson.estimated_minutes == 30


def test_today_lesson_defaults_non_numeric_minutes():
    lesson = TodayLesson(
        title="Review",
        lesson_type=None,
        week=1,
        day=1,
        objectives="not-a-list",
        estimated_minutes="not-a-number",
    )

    assert lesson.lesson_type == "review"
    assert lesson.objectives == []
    assert lesson.estimated_minutes == 25
