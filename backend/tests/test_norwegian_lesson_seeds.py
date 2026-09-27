from app.data.no.lesson_seeds import get_lesson_seed

LEVELS = ["A2", "B1", "B2", "C1", "C2"]
SKILLS = ["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"]


def test_norwegian_curated_seeds_cover_all_units_and_skills():
    for level in LEVELS:
        for number in range(1, 9):
            unit = f"no-{level.lower()}-unit-{number}"
            for skill in SKILLS:
                seed = get_lesson_seed(level, unit, skill)
                assert seed is not None
                assert seed["title"]
                assert seed["objective"]
                assert seed["source"] == "curated_norwegian"
                if skill == "reading":
                    assert seed.get("text")
                elif skill == "listening":
                    assert seed.get("transcript")
                elif skill in {"speaking", "writing"}:
                    assert seed.get("prompt")
                elif skill == "vocabulary":
                    assert seed.get("words")


def test_norwegian_unknown_unit_returns_none():
    assert get_lesson_seed("C2", "no-c2-missing", "reading") is None
