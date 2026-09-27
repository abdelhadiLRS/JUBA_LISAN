from app.data.vi.lesson_seeds import get_lesson_seed

LEVELS = {
    "A2": "vi-a2-unit-1",
    "B1": "vi-b1-unit-1",
    "B2": "vi-b2-unit-1",
    "C1": "vi-c1-unit-1",
    "C2": "vi-c2-unit-1",
}
SKILLS = ["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"]


def test_vietnamese_seeds_cover_all_core_skills_from_a2_to_c2():
    for level, unit_id in LEVELS.items():
        for skill in SKILLS:
            seed = get_lesson_seed(level, unit_id, skill)
            assert seed is not None, (level, skill)
            assert seed["title"]
            assert seed["objective"]
            assert seed["unit_id"] == unit_id
            assert seed["source"] == "curated_vietnamese"
            if skill == "reading":
                assert seed.get("text") and len(seed.get("questions", [])) >= 3
            elif skill == "listening":
                assert seed.get("transcript")
            elif skill in {"speaking", "writing"}:
                assert seed.get("prompt")
            elif skill == "vocabulary":
                assert seed.get("words")


def test_unknown_vietnamese_unit_returns_none():
    assert get_lesson_seed("B1", "vi-b1-unit-999", "reading") is None
