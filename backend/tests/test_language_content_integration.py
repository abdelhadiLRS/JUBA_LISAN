"""Regression tests for fully integrated target-language content."""

from app.data.assessment_bank import get_assessment_bank
from app.data.curriculum import get_curriculum
from app.data.grammar import get_grammar_topics
from app.data.phrasebook import get_phrasebook_categories
from app.data.vocabulary import get_vocabulary_sets
from app.services.language_helpers import (
    get_language_flag,
    get_language_name,
    get_language_romanization,
    get_language_script,
    get_language_self_name,
    get_iso639,
)


def test_czech_dispatchers_resolve_dedicated_content() -> None:
    curriculum = get_curriculum("cs-CZ")
    assert set(curriculum) == {"A1", "A2", "B1", "B2", "C1", "C2"}
    assert sum(len(units) for units in curriculum.values()) == 24
    assert len(get_grammar_topics("cs-CZ")) == 45
    assert len(get_vocabulary_sets("cs-CZ")) == 48
    assert len(get_phrasebook_categories("cs-CZ")) == 18
    assert len(get_assessment_bank("cs-CZ")) == 24


def test_czech_curriculum_and_vocabulary_references_are_consistent() -> None:
    curriculum = get_curriculum("cs-CZ")
    vocabulary_ids = {vocab.id for vocab in get_vocabulary_sets("cs-CZ")}

    units = [unit for level in curriculum.values() for unit in level]
    assert len(units) == 24
    assert all(unit.vocabulary_set_ids for unit in units)
    assert all(
        vocabulary_id in vocabulary_ids
        for unit in units
        for vocabulary_id in unit.vocabulary_set_ids
    )


def test_czech_assessment_bank_is_balanced_and_valid() -> None:
    bank = get_assessment_bank("cs-CZ")
    levels = {question.difficulty for question in bank}

    assert levels == {"A1", "A2", "B1", "B2", "C1", "C2"}
    assert all(len(question.options) >= 2 for question in bank)
    assert all(question.correct in question.options for question in bank)
    assert all(question.skill in {"grammar", "vocabulary", "reading"} for question in bank)
    assert all(question.question.strip() for question in bank)


def test_czech_helper_metadata_and_flags_policy() -> None:
    assert get_language_name("cs-CZ") == "Czech"
    assert get_language_self_name("cs-CZ") == "Čeština"
    assert get_iso639("cs-CZ") == "cs"
    assert get_language_script("cs-CZ") == "latin"
    assert get_language_romanization("cs-CZ") == ""
    assert get_language_flag("cs-CZ") == ""


def test_czech_and_swedish_are_not_foundation_fallbacks() -> None:
    assert get_curriculum("cs-CZ")["A1"][0].id.startswith("cs-a1-")
    assert get_curriculum("sv-SE")["A1"][0].id.startswith("sv-a1-")
    assert get_grammar_topics("cs-CZ")[0].slug.startswith("cs-")
    assert get_grammar_topics("sv-SE")[0].slug.startswith("sv-")
