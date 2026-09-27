from app.data.nl.lesson_seeds import get_lesson_seed


def test_dutch_curated_seeds_cover_a2_to_c2():
    for level in ("A2", "B1", "B2", "C1", "C2"):
        seed = get_lesson_seed(level, f"{level.lower()}-unit-1", "grammar")
        assert seed is not None
        assert seed["title"]
        assert seed["objective"]


def test_dutch_full_skill_cycle_has_authored_content():
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
