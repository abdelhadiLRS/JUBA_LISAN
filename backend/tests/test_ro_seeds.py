from app.data.ro.lesson_seeds import get_lesson_seed

LEVELS = ["A2", "B1", "B2", "C1", "C2"]
SKILLS = ["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"]

def test_romanian_seeds():
    for level in LEVELS:
        unit = "ro-" + level.lower() + "-unit-1"
        for skill in SKILLS:
            seed = get_lesson_seed(level, unit, skill)
            assert seed
            assert seed.get("title")
            assert seed.get("objective")
