from app.data.fi.lesson_seeds import get_lesson_seed

LEVELS = ["A2", "B1", "B2", "C1", "C2"]
SKILLS = ["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"]

def test_finnish_curated_seeds_cover_all_a2_to_c2_units():
    for level in LEVELS:
        for unit_no in range(1, 9):
            unit = f"fi-{level.lower()}-unit-{unit_no}"
            for skill in SKILLS:
                seed = get_lesson_seed(level, unit, skill)
                assert seed is not None
                assert seed["source"] == "curated_finnish"
                assert seed["title"]
                assert seed["objective"]
                assert seed["examples"]
                if skill == "reading":
                    assert seed["text"]
                    assert len(seed["questions"]) >= 3
                elif skill == "listening":
                    assert seed["transcript"]
                elif skill in {"speaking", "writing"}:
                    assert seed["prompt"]
                elif skill == "vocabulary":
                    assert seed["words"]

def test_finnish_unknown_unit_returns_none():
    assert get_lesson_seed("C2", "fi-c2-missing", "reading") is None
