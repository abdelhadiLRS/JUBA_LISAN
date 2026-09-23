from app.data.ar.lessons import ARABIC_A1_CONTENT_SEEDS, get_arabic_a1_content_seed
from app.data.ar.lessons import get_arabic_a1_lessons


def test_every_arabic_a1_lesson_has_a_curated_seed():
    lessons = get_arabic_a1_lessons()
    assert len(lessons) == 80
    assert len(ARABIC_A1_CONTENT_SEEDS) == 80
    assert {seed.lesson_id for seed in ARABIC_A1_CONTENT_SEEDS} == {lesson.id for lesson in lessons}


def test_seed_contains_teaching_material():
    seed = get_arabic_a1_content_seed("a1-u6-w2-d4")
    assert seed is not None
    assert len(seed.target_phrases) >= 4
    assert len(seed.model_sentences) >= 2
    assert seed.comprehension_prompt
    assert seed.production_prompt


def test_unknown_lesson_has_no_seed():
    assert get_arabic_a1_content_seed("a1-u9-w1-d1") is None


def test_arabic_a1_course_content_integrity():
    from app.data.ar.lessons import validate_arabic_a1_content_quality

    assert validate_arabic_a1_content_quality() == []
