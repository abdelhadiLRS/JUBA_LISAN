from app.data.is.lesson_seeds import get_lesson_seed

LEVELS = ["A2", "B1", "B2", "C1", "C2"]
SKILLS = ["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"]

def test_icelandic_curated_seeds_cover_all_levels_and_skills():
    for level in LEVELS:
        for number in range(1, 9):
            unit = f"is-{level.lower()}-unit-{number}"
            for skill in SKILLS:
                seed = get_lesson_seed(level, unit, skill)
                assert seed
                assert seed["title"]
                assert seed["objective"]
                assert seed["source"] == "curated_icelandic"
                if skill == "reading":
                    assert seed.get("text")
                elif skill == "listening":
                    assert seed.get("transcript")
                elif skill in {"speaking", "writing"}:
                    assert seed.get("prompt")

def test_icelandic_unknown_unit_returns_none():
    assert get_lesson_seed("C2", "is-c2-unit-99", "reading") is None
