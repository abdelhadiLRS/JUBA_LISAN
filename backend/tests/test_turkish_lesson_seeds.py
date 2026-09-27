from app.data.tr.lesson_seeds import get_lesson_seed


def test_turkish_curated_seeds_cover_a2_to_c2():
    for level in ("A2", "B1", "B2", "C1", "C2"):
        seed = get_lesson_seed(level, f"{level.lower()}-unit-1", "grammar")
        assert seed is not None
        assert seed["title"]
        assert seed["objective"]


def test_turkish_reading_and_listening_seeds_have_questions():
    for level in ("A2", "B1", "B2", "C1", "C2"):
        unit_id = f"{level.lower()}-unit-1"
        for lesson_type in ("reading", "listening"):
            seed = get_lesson_seed(level, unit_id, lesson_type)
            assert seed is not None
            assert seed.get("text") or seed.get("transcript")
            assert len(seed["questions"]) >= 2

def test_turkish_full_skill_cycle_has_authored_content():
    for level in ("A2", "B1", "B2", "C1", "C2"):
        unit_id = f"{level.lower()}-unit-1"
        for lesson_type in ("listening", "speaking", "writing", "review"):
            seed = get_lesson_seed(level, unit_id, lesson_type)
            assert seed is not None
            assert seed["title"]
            assert seed["objective"]

        assert get_lesson_seed(level, unit_id, "listening")["transcript"]
        assert get_lesson_seed(level, unit_id, "speaking")["prompt"]
        assert get_lesson_seed(level, unit_id, "writing")["prompt"]
        assert len(get_lesson_seed(level, unit_id, "review")["questions"]) >= 3

