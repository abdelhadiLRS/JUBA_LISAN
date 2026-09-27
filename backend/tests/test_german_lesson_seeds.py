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



def test_german_curriculum_includes_full_skill_cycle():
    from app.data.de.curriculum import CURRICULUM

    expected = {"grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"}
    for level in ("A2", "B1", "B2", "C1", "C2"):
        assert CURRICULUM[level]
        for unit in CURRICULUM[level]:
            assert expected.issubset(set(unit.lesson_types))

def test_german_curated_seeds_cover_full_skill_content():
    for level in ("A2", "B1", "B2", "C1", "C2"):
        unit_id = f"{level.lower()}-unit-1"

        listening = get_lesson_seed(level, unit_id, "listening")
        speaking = get_lesson_seed(level, unit_id, "speaking")
        writing = get_lesson_seed(level, unit_id, "writing")
        review = get_lesson_seed(level, unit_id, "review")

        assert listening is not None
        assert listening["objective"]
        assert listening["transcript"]
        assert len(listening["questions"]) >= 3

        assert speaking is not None
        assert speaking["objective"]
        assert speaking["prompt"]
        assert len(speaking.get("phrases", [])) >= 3

        assert writing is not None
        assert writing["objective"]
        assert writing["prompt"]
        assert len(writing.get("guidance", [])) >= 2

        assert review is not None
        assert review["objective"]
        assert len(review["questions"]) >= 3

