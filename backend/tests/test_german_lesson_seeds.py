from app.data.de.lesson_seeds import get_lesson_seed


def test_german_curated_seeds_cover_a2_to_c2():
    for level in ("A2", "B1", "B2", "C1", "C2"):
        unit_id = f"{level.lower()}-unit-1"
        grammar = get_lesson_seed(level, unit_id, "grammar")
        vocabulary = get_lesson_seed(level, unit_id, "vocabulary")
        reading = get_lesson_seed(level, unit_id, "reading")

        assert grammar is not None
        assert grammar["title"]
        assert grammar["objective"]
        assert vocabulary is not None
        assert len(vocabulary["words"]) >= 6
        assert reading is not None
        assert reading["text"]
        assert len(reading["questions"]) >= 2
