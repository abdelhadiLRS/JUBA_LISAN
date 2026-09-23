"""Integrity checks for the Arabic A1 sequenced lesson map."""
from app.data.ar.curriculum import CURRICULUM
from app.data.ar.grammar import GRAMMAR_TOPICS
from app.data.ar.vocabulary import VOCABULARY_SETS
from app.data.ar.phrasebook import PHRASEBOOK_CATEGORIES
from app.data.ar.lessons import ARABIC_A1_LESSONS


def test_arabic_a1_sequence_is_complete():
    assert len(ARABIC_A1_LESSONS) == 80
    assert [x.id for x in ARABIC_A1_LESSONS] == list(dict.fromkeys(x.id for x in ARABIC_A1_LESSONS))
    assert {x.unit_id for x in ARABIC_A1_LESSONS} == {f"a1-unit-{n}" for n in range(1, 9)}
    for unit in range(1, 9):
        lessons = [x for x in ARABIC_A1_LESSONS if x.unit_id == f"a1-unit-{unit}"]
        assert [(x.week, x.day) for x in lessons] == [(1, d) for d in range(1, 6)] + (
            [(2, d) for d in range(1, 6)] if unit <= 4 else []
        )


def test_arabic_a1_lesson_references_resolve():
    curriculum = {u.id for u in CURRICULUM["A1"]}
    grammar = {g.slug for g in GRAMMAR_TOPICS}
    vocab = {v.id for v in VOCABULARY_SETS}
    phrases = {p.id for p in PHRASEBOOK_CATEGORIES}
    for lesson in ARABIC_A1_LESSONS:
        assert lesson.unit_id in curriculum
        assert set(lesson.grammar_refs) <= grammar
        assert set(lesson.vocabulary_set_ids) <= vocab
        assert set(lesson.phrasebook_ids) <= phrases


def test_arabic_a1_units_have_two_week_sequence():
    for unit in range(1, 9):
        lessons = [x for x in ARABIC_A1_LESSONS if x.unit_id == f"a1-unit-{unit}"]
        assert len(lessons) == 10
