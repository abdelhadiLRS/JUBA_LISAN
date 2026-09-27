from app.data.uk.lesson_seeds import get_lesson_seed

LEVEL_UNITS={
"A2":[f"uk-a2-unit-{i}" for i in range(1,5)],
"B1":[f"uk-b1-unit-{i}" for i in range(1,3)],
"B2":[f"uk-b2-unit-{i}" for i in range(1,3)],
"C1":[f"uk-c1-unit-{i}" for i in range(1,3)],
"C2":[f"uk-c2-unit-{i}" for i in range(1,3)],
}
SKILLS=["grammar","vocabulary","reading","listening","speaking","writing","review"]

def test_ukrainian_curated_seeds_cover_all_units_and_skills():
    for level,units in LEVEL_UNITS.items():
        for unit in units:
            for skill in SKILLS:
                seed=get_lesson_seed(level,unit,skill)
                assert seed is not None
                assert seed["title"]
                assert seed["objective"]
                assert seed["source"]=="curated_ukrainian"
                if skill=="reading":
                    assert seed.get("text") and len(seed.get("questions",[]))>=3
                elif skill=="listening":
                    assert seed.get("transcript")
                elif skill in {"speaking","writing"}:
                    assert seed.get("prompt")
                elif skill=="vocabulary":
                    assert seed.get("words")

def test_ukrainian_unknown_unit_returns_none():
    assert get_lesson_seed("C2","uk-c2-missing","reading") is None
