"""Coverage tests for curated French lesson seeds."""
from app.data.fr.lesson_seeds import get_lesson_seed

LEVELS = ("A2", "B1", "B2", "C1", "C2")
LESSON_TYPES = (
    "grammar",
    "vocabulary",
    "reading",
    "listening",
    "speaking",
    "writing",
    "review",
)


def test_french_full_skill_coverage():
    for level in LEVELS:
        unit_id = f"{level.lower()}-unit-1"
        for lesson_type in LESSON_TYPES:
            seed = get_lesson_seed(level, unit_id, lesson_type)
            assert seed is not None, f"Missing French {level} {lesson_type} seed"
            assert seed.get("title")
            assert seed.get("objective")


def test_french_skill_specific_fields():
    for level in LEVELS:
        unit_id = f"{level.lower()}-unit-1"
        assert get_lesson_seed(level, unit_id, "listening").get("transcript")
        assert get_lesson_seed(level, unit_id, "speaking").get("prompt")
        assert get_lesson_seed(level, unit_id, "writing").get("prompt")
        assert get_lesson_seed(level, unit_id, "review").get("questions")
