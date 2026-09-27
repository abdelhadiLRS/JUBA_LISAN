"""Coverage checks for curated Italian A2-C2 lesson seeds."""

from app.data.it.lesson_seeds import get_lesson_seed

LEVELS = ["A2", "B1", "B2", "C1", "C2"]
SKILLS = ["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"]
UNITS = {"A2":"a2-unit-1","B1":"b1-unit-1","B2":"b2-unit-1","C1":"c1-unit-1","C2":"c2-unit-1"}


def test_italian_has_full_curated_skill_cycle():
    for level in LEVELS:
        for skill in SKILLS:
            seed = get_lesson_seed(level, UNITS[level], skill)
            assert seed is not None, f"missing Italian {level} {skill} seed"
            assert seed["title"]
            assert seed["objective"]


def test_italian_production_seeds_have_prompts():
    for level in LEVELS:
        for skill in ("speaking", "writing"):
            seed = get_lesson_seed(level, UNITS[level], skill)
            assert seed["prompt"]
            assert seed.get("phrases") or seed.get("guidance")
            assert seed.get("examples")
