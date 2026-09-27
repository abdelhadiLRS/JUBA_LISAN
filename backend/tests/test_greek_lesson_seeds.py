from app.data.el.lesson_seeds import get_lesson_seed

LEVELS=["A2","B1","B2","C1","C2"]
SKILLS=["grammar","vocabulary","reading","listening","speaking","writing","review"]

def test_greek_curated_seeds_cover_all_units_and_skills():
    for level in LEVELS:
        for number in range(1,5):
            unit=f"{level.lower()}-unit-{number}"
            for skill in SKILLS:
                seed=get_lesson_seed(level,unit,skill)
                assert seed
                assert seed["title"]
                assert seed["objective"]
                if skill=="reading": assert seed.get("text") and len(seed.get("questions",[]))>=3
                elif skill=="listening": assert seed.get("transcript")
                elif skill in {"speaking","writing"}: assert seed.get("prompt")
                elif skill=="vocabulary": assert seed.get("words")

def test_unknown_greek_seed_returns_none():
    assert get_lesson_seed("C1","c1-unit-99","reading") is None
