from app.data.hu.lesson_seeds import get_lesson_seed

LEVEL_UNITS = {
    "A2": ["hu-a2-unit-1", "hu-a2-unit-2", "hu-a2-unit-3"],
    "B1": ["hu-b1-unit-1", "hu-b1-unit-2"],
    "B2": ["hu-b2-unit-1", "hu-b2-unit-2"],
    "C1": ["hu-c1-unit-1"],
    "C2": ["hu-c2-unit-1"],
}
SKILLS = ["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"]

def test_hungarian_curated_seeds_cover_all_cefr_units_and_skills():
    for level, units in LEVEL_UNITS.items():
        for unit in units:
            for skill in SKILLS:
                seed = get_lesson_seed(level, unit, skill)
                assert seed is not None
                assert seed["title"]
                assert seed["objective"]
                assert seed["source"] == "curated_hungarian"
                if skill == "reading":
                    assert seed.get("text")
                    assert len(seed.get("questions", [])) >= 3
                elif skill == "listening":
                    assert seed.get("transcript")
                elif skill in {"speaking", "writing"}:
                    assert seed.get("prompt")
                elif skill == "vocabulary":
                    assert seed.get("words")

def test_hungarian_unknown_unit_returns_none():
    assert get_lesson_seed("C2", "hu-c2-missing", "reading") is None
