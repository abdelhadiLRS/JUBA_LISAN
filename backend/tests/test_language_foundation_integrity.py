"""Structural integrity checks for registered language foundation modules."""

from __future__ import annotations

import importlib
from typing import get_args

import pytest

from app.data import curriculum as curriculum_dispatcher
from app.data._types import LessonType, PartOfSpeech, Register, Skill


ALLOWED_SKILLS = set(get_args(Skill))
ALLOWED_REGISTERS = set(get_args(Register))
ALLOWED_LESSON_TYPES = set(get_args(LessonType))
ALLOWED_POS = set(get_args(PartOfSpeech))


def _public_ids(items: object, attribute: str = "id") -> set[str]:
    if not isinstance(items, (list, tuple)):
        return set()
    return {
        getattr(item, attribute)
        for item in items
        if getattr(item, attribute, None)
    }


def test_registered_foundations_import_and_expose_curriculum():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # pragma: no cover
            failures.append(f"{language}: import failed: {exc}")
            continue

        curriculum = getattr(module, "CURRICULUM", None)
        if not isinstance(curriculum, dict) or not curriculum:
            failures.append(f"{language}: missing/empty CURRICULUM")
            continue

        for level in curriculum_dispatcher.CEFR_LEVELS:
            if not curriculum.get(level, []):
                failures.append(f"{language}: {level} has no curriculum units")

    assert not failures, "\n".join(failures)


def test_registered_foundations_have_no_dangling_unit_references():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        grammar_topics = getattr(module, "GRAMMAR_TOPICS", [])
        vocabulary_sets = getattr(module, "VOCABULARY_SETS", [])
        grammar_ids = _public_ids(grammar_topics)
        vocabulary_ids = _public_ids(vocabulary_sets)
        grammar_by_id = {
            item.slug: item
            for item in grammar_topics
            if getattr(item, "slug", None)
        }
        vocabulary_by_id = {
            item.id: item
            for item in vocabulary_sets
            if getattr(item, "id", None)
        }
        all_units = {
            unit.id: unit
            for units in getattr(module, "CURRICULUM", {}).values()
            for unit in units
        }

        for level, units in getattr(module, "CURRICULUM", {}).items():
            unit_ids: set[str] = set()
            for unit in units:
                if unit.id in unit_ids:
                    failures.append(f"{language}: duplicate unit id {unit.id}")
                unit_ids.add(unit.id)

                if unit.level != level:
                    failures.append(
                        f"{language}/{unit.id}: stored level {unit.level} does not match curriculum key {level}"
                    )
                if unit.unit_number < 1:
                    failures.append(
                        f"{language}/{unit.id}: unit_number must be positive, got {unit.unit_number}"
                    )

                missing_grammar = set(unit.grammar_points) - grammar_ids
                if missing_grammar:
                    failures.append(
                        f"{language}/{level}/{unit.id}: missing grammar {sorted(missing_grammar)}"
                    )
                for grammar_slug in unit.grammar_points:
                    topic = grammar_by_id.get(grammar_slug)
                    if topic and topic.level != level:
                        failures.append(
                            f"{language}/{level}/{unit.id}: grammar {grammar_slug} is level {topic.level}"
                        )

                missing_vocab = set(unit.vocabulary_set_ids) - vocabulary_ids
                if missing_vocab:
                    failures.append(
                        f"{language}/{level}/{unit.id}: missing vocabulary {sorted(missing_vocab)}"
                    )

                for vocab_id in unit.vocabulary_set_ids:
                    vocab = vocabulary_by_id.get(vocab_id)
                    if vocab and vocab.unit_ref not in all_units:
                        failures.append(
                            f"{language}/{level}/{unit.id}: vocabulary {vocab_id} points to missing unit {vocab.unit_ref}"
                        )
                    if vocab and vocab.unit_ref in all_units:
                        primary_unit = all_units[vocab.unit_ref]
                        if primary_unit.level != vocab.level:
                            failures.append(
                                f"{language}/{vocab_id}: primary unit {vocab.unit_ref} is level {primary_unit.level}, "
                                f"but vocabulary is {vocab.level}"
                            )

                invalid_lesson_types = set(unit.lesson_types) - ALLOWED_LESSON_TYPES
                if invalid_lesson_types:
                    failures.append(
                        f"{language}/{level}/{unit.id}: invalid lesson types {sorted(invalid_lesson_types)}"
                    )
                if not unit.lesson_types:
                    failures.append(f"{language}/{level}/{unit.id}: no lesson types")
                if not unit.competency_checklist:
                    failures.append(f"{language}/{level}/{unit.id}: no competency checklist")

        for vocab in vocabulary_sets:
            if vocab.level not in curriculum_dispatcher.CEFR_LEVELS:
                failures.append(f"{language}/{vocab.id}: invalid vocabulary level {vocab.level}")
            if vocab.unit_ref not in all_units:
                failures.append(f"{language}/{vocab.id}: missing primary unit {vocab.unit_ref}")
            words = [entry.word for entry in vocab.words]
            duplicates = sorted({word for word in words if words.count(word) > 1})
            if duplicates:
                failures.append(
                    f"{language}/{vocab.id}: duplicate words in vocabulary set {duplicates}"
                )
            for entry in vocab.words:
                if entry.pos not in ALLOWED_POS:
                    failures.append(f"{language}/{vocab.id}: invalid part of speech {entry.pos!r}")

    assert not failures, "\n".join(failures)


def test_registered_foundations_have_valid_phrasebook_references():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        unit_ids = {
            unit.id
            for units in getattr(module, "CURRICULUM", {}).values()
            for unit in units
        }
        for category in getattr(module, "PHRASEBOOK_CATEGORIES", []):
            if category.level not in curriculum_dispatcher.CEFR_LEVELS:
                failures.append(f"{language}: invalid phrasebook level {category.level}")

            phrase_texts = [phrase.text for phrase in category.phrases]
            duplicate_phrases = sorted(
                {phrase for phrase in phrase_texts if phrase_texts.count(phrase) > 1}
            )
            if duplicate_phrases:
                failures.append(
                    f"{language}/{category.id}: duplicate phrases {duplicate_phrases}"
                )

            for phrase in category.phrases:
                if phrase.register not in ALLOWED_REGISTERS:
                    failures.append(
                        f"{language}/{category.id}: invalid phrase register {phrase.register}"
                    )
                if phrase.unit_ref and phrase.unit_ref not in unit_ids:
                    failures.append(
                        f"{language}/{category.id}: missing phrase unit {phrase.unit_ref}"
                    )

    assert not failures, "\n".join(failures)


def test_registered_foundations_have_valid_assessment_grammar_links():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        grammar_ids = _public_ids(getattr(module, "GRAMMAR_TOPICS", []), "slug")
        for question in getattr(module, "ASSESSMENT_BANK", []):
            if question.grammar_slug and question.grammar_slug not in grammar_ids:
                failures.append(
                    f"{language}/{question.id}: missing grammar {question.grammar_slug}"
                )

    assert not failures, "\n".join(failures)


def test_registered_foundations_have_valid_assessments():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        for question in getattr(module, "ASSESSMENT_BANK", []):
            if question.skill not in ALLOWED_SKILLS:
                failures.append(f"{language}/{question.id}: invalid skill {question.skill}")
            if len(question.options) != 4:
                failures.append(f"{language}/{question.id}: expected exactly 4 options")
            if question.correct not in question.options:
                failures.append(f"{language}/{question.id}: correct answer is not an option")
            if question.difficulty not in curriculum_dispatcher.CEFR_LEVELS:
                failures.append(f"{language}/{question.id}: invalid difficulty {question.difficulty}")

    assert not failures, "\n".join(failures)


def test_registered_foundations_have_unique_content_ids():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        collections = (
            ("grammar", getattr(module, "GRAMMAR_TOPICS", []), "slug"),
            ("assessment", getattr(module, "ASSESSMENT_BANK", []), "id"),
            ("phrasebook", getattr(module, "PHRASEBOOK_CATEGORIES", []), "id"),
        )
        for label, items, attribute in collections:
            ids = [
                getattr(item, attribute)
                for item in items
                if getattr(item, attribute, None)
            ]
            duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
            if duplicates:
                failures.append(f"{language}: duplicate {label} ids {duplicates}")

    assert not failures, "\n".join(failures)


def test_registered_foundations_have_unique_vocabulary_ids():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        vocabulary = getattr(module, "VOCABULARY_SETS", [])
        ids = [item.id for item in vocabulary if getattr(item, "id", None)]
        duplicates = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
        if duplicates:
            failures.append(f"{language}: duplicate vocabulary ids {duplicates}")

    assert not failures, "\n".join(failures)


@pytest.mark.parametrize(
    ("requested_locale", "expected_module"),
    [
        ("en_US", "app.data.en_US.curriculum"),
        ("en-US", "app.data.en_US.curriculum"),
        ("fr-FR", "app.data.fr.curriculum"),
        ("fr", "app.data.fr.curriculum"),
        ("pt-BR", "app.data.pt.curriculum"),
        ("zh-TW", "app.data.zh.curriculum"),
    ],
)
def test_curriculum_dispatcher_normalizes_locale_aliases(requested_locale: str, expected_module: str):
    module = curriculum_dispatcher._resolve_module(requested_locale)
    assert module.__name__ == expected_module


@pytest.mark.parametrize(
    ("requested_locale", "expected_title"),
    [
        ("en_US", "Lesson"),
        ("fr", "Leçon"),
        ("pt-BR", "Lição"),
        ("de", "Lektion"),
    ],
)
def test_curriculum_distribution_uses_locale_aware_labels(requested_locale: str, expected_title: str):
    units = curriculum_dispatcher.get_curriculum_units("A1", requested_locale)
    slots = curriculum_dispatcher.distribute_units(units[:1], 1, 2, requested_locale)
    assert slots
    assert expected_title in slots[0]["title"]


@pytest.mark.parametrize(
    ("locale", "expected_name", "expected_iso"),
    [
        ("en_US", "English (US)", "en"),
        ("fr", "French", "fr"),
        ("pt-BR", "European Portuguese", "pt"),
        ("de-DE", "German", "de"),
        ("ar", "Arabic", "ar"),
        ("hi-IN", "Hindi", "hi"),
        ("zh-TW", "zh-TW", "zh"),
    ],
)
def test_language_helpers_normalize_common_locale_aliases(locale: str, expected_name: str, expected_iso: str):
    from app.services.language_helpers import get_iso639, get_language_name

    assert get_language_name(locale) == expected_name
    assert get_iso639(locale) == expected_iso


@pytest.mark.parametrize(
    ("locale", "expected_fragment"),
    [
        ("en_US", "American English"),
        ("en-US", "American English"),
        ("fr-FR", "standard French"),
        ("fr", "standard French"),
        ("pt-BR", "European Portuguese"),
        ("zh-TW", "simplified Chinese"),
        ("ar", "Modern Standard Arabic"),
        ("tr-TR", "standard Turkish"),
        ("ru-RU", "standard Russian"),
        ("hi-IN", "standard Hindi"),
        ("fa", "standard Persian"),
        ("he", "Modern Hebrew"),
        ("th-TH", "standard Thai"),
    ],
)
def test_prompt_overlay_normalizes_locale_aliases(locale: str, expected_fragment: str):
    from app.services.prompts.common import get_language_prompt_overlay

    assert expected_fragment in get_language_prompt_overlay(locale)


@pytest.mark.parametrize(
    ("units", "total_weeks", "days_per_week"),
    [([], 1, 5), ([], 0, 5), ([], 1, 0)],
)
def test_distribute_units_handles_empty_or_invalid_schedule_inputs(units, total_weeks, days_per_week):
    assert curriculum_dispatcher.distribute_units(
        units, total_weeks, days_per_week, "en-GB"
    ) == []


def test_distribute_units_never_emits_invalid_schedule_dimensions():
    units = curriculum_dispatcher.get_curriculum_units("A1", "en-GB")[:1]
    assert curriculum_dispatcher.distribute_units(units, 0, 5, "en-GB") == []
    assert curriculum_dispatcher.distribute_units(units, 2, 0, "en-GB") == []


@pytest.mark.parametrize(
    ("locale", "expected_script", "expected_unit"),
    [
        ("ar", "arabic", "words"),
        ("fa", "arabic-persian", "words"),
        ("uk-UA", "cyrillic", "words"),
        ("bn-BD", "bengali", "words"),
        ("hi-IN", "devanagari", "words"),
        ("th-TH", "thai", "characters"),
        ("zh-TW", "traditional-hanzi", "characters"),
    ],
)
def test_language_capability_aliases_cover_foundation_locales(locale, expected_script, expected_unit):
    from app.services.language_helpers import (
        get_language_script,
        get_reading_length_unit,
    )

    assert get_language_script(locale) == expected_script
    assert get_reading_length_unit(locale) == expected_unit
