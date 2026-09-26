"""Structural integrity checks for registered language foundation modules."""

from __future__ import annotations

import importlib
from typing import get_args

import pytest

from app.data import curriculum as curriculum_dispatcher
from app.data._types import LessonType, PartOfSpeech, Register, Skill
from app.services.language_helpers import get_iso639, get_language_name, get_language_self_name
from app.services.prompts.common import get_language_prompt_overlay


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


def test_registered_language_metadata_resolves_core_and_foundation_locales():
    cases = {
        "en-US": ("English (US)", "en"),
        "en_US": ("English (US)", "en"),
        "de-DE": ("German", "de"),
        "hr-HR": ("Croatian", "hr"),
        "bn-BD": ("Bengali", "bn"),
        "suq-ET": ("Suri", "suq"),
    }
    failures: list[str] = []
    for locale, (expected_name, expected_iso) in cases.items():
        if get_language_name(locale) != expected_name:
            failures.append(f"{locale}: unexpected language name")
        if get_iso639(locale) != expected_iso:
            failures.append(f"{locale}: unexpected ISO 639 code")
    assert not failures, "\\n".join(failures)


def test_curriculum_dispatcher_resolves_regional_locales():
    cases = {
        "en-US": "app.data.en_US.curriculum",
        "en_US": "app.data.en_US.curriculum",
        "de-DE": "app.data.de.curriculum",
        "hr-HR": "app.data.language_foundations.hr",
        "bn-BD": "app.data.language_foundations.bn",
        "suq-ET": "app.data.language_foundations.suq",
    }
    failures: list[str] = []
    for locale, expected_module in cases.items():
        try:
            module = curriculum_dispatcher._resolve_module(locale)
        except Exception as exc:
            failures.append(f"{locale}: resolve failed: {exc}")
            continue
        actual = getattr(module, "__name__", "")
        if actual != expected_module:
            failures.append(f"{locale}: expected {expected_module}, got {actual}")
    assert not failures, "\\n".join(failures)


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
        global_unit_levels: dict[str, str] = {}
        for declared_level, declared_units in getattr(module, "CURRICULUM", {}).items():
            for declared_unit in declared_units:
                previous_level = global_unit_levels.get(declared_unit.id)
                if previous_level and previous_level != declared_level:
                    failures.append(
                        f"{language}: unit id {declared_unit.id} is declared at both "
                        f"{previous_level} and {declared_level}"
                    )
                global_unit_levels[declared_unit.id] = declared_level

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


def test_registered_foundations_keep_vocabulary_attached_to_declared_units():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        units = {
            unit.id: unit
            for level_units in getattr(module, "CURRICULUM", {}).values()
            for unit in level_units
        }
        for vocab in getattr(module, "VOCABULARY_SETS", []):
            unit = units.get(vocab.unit_ref)
            if unit is None:
                continue
            if vocab.id not in unit.vocabulary_set_ids:
                failures.append(
                    f"{language}/{vocab.id}: unit_ref {vocab.unit_ref} does not declare this vocabulary set"
                )
            if vocab.level != unit.level:
                failures.append(
                    f"{language}/{vocab.id}: vocabulary level {vocab.level} does not match unit {unit.id} level {unit.level}"
                )

    assert not failures, "\n".join(failures)


def test_registered_foundations_have_nonempty_core_content():
    failures: list[str] = []

    for language, module_name in curriculum_dispatcher._LANG_MODULES.items():
        module = importlib.import_module(module_name)
        for topic in getattr(module, "GRAMMAR_TOPICS", []):
            for field in ("title", "summary", "explanation"):
                if not str(getattr(topic, field, "")).strip():
                    failures.append(f"{language}/{topic.slug}: empty grammar {field}")
            if not getattr(topic, "examples", []):
                failures.append(f"{language}/{topic.slug}: no grammar examples")
        for vocab in getattr(module, "VOCABULARY_SETS", []):
            if not str(vocab.topic).strip() or not vocab.words:
                failures.append(f"{language}/{vocab.id}: empty vocabulary set")
            for entry in vocab.words:
                if not str(entry.word).strip() or not str(entry.definition).strip() or not str(entry.example).strip():
                    failures.append(f"{language}/{vocab.id}: incomplete vocabulary entry {entry.word!r}")
        for category in getattr(module, "PHRASEBOOK_CATEGORIES", []):
            if not str(category.situation).strip() or not category.phrases:
                failures.append(f"{language}/{category.id}: empty phrasebook category")
            for phrase in category.phrases:
                if not str(phrase.text).strip() or not str(phrase.context).strip():
                    failures.append(f"{language}/{category.id}: incomplete phrasebook entry")

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
                if phrase.unit_ref:
                    phrase_unit = next(
                        (
                            unit
                            for units in getattr(module, "CURRICULUM", {}).values()
                            for unit in units
                            if unit.id == phrase.unit_ref
                        ),
                        None,
                    )
                    if phrase_unit and phrase_unit.level != category.level:
                        failures.append(
                            f"{language}/{category.id}: phrase unit {phrase.unit_ref} is "
                            f"level {phrase_unit.level}, but category is {category.level}"
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
            if question.grammar_slug:
                grammar = next(
                    (
                        topic
                        for topic in getattr(module, "GRAMMAR_TOPICS", [])
                        if topic.slug == question.grammar_slug
                    ),
                    None,
                )
                if grammar and grammar.level != question.difficulty:
                    failures.append(
                        f"{language}/{question.id}: grammar {question.grammar_slug} is "
                        f"level {grammar.level}, but assessment is {question.difficulty}"
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


def test_curriculum_dispatcher_resolves_explicit_locale_alias_table():
    failures: list[str] = []
    for locale, canonical in curriculum_dispatcher._LOCALE_ALIASES.items():
        expected = curriculum_dispatcher._LANG_MODULES.get(canonical)
        if expected is None:
            failures.append(f"{locale}: alias target {canonical!r} is not registered")
            continue
        try:
            resolved = curriculum_dispatcher._resolve_module(locale)
        except Exception as exc:
            failures.append(f"{locale}: resolve failed: {exc}")
            continue
        if resolved.__name__ != expected:
            failures.append(
                f"{locale}: resolved {resolved.__name__!r}, expected {expected!r}"
            )
    assert not failures, "\\n".join(failures)


def test_curriculum_dispatcher_resolves_every_registered_language():
    failures: list[str] = []

    for language, expected_module in curriculum_dispatcher._LANG_MODULES.items():
        try:
            resolved = curriculum_dispatcher._resolve_module(language)
        except Exception as exc:
            failures.append(f"{language}: dispatcher import failed: {exc}")
            continue
        if resolved.__name__ != expected_module:
            failures.append(
                f"{language}: resolved {resolved.__name__!r}, expected {expected_module!r}"
            )

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


def test_all_registered_languages_have_resolvable_metadata():
    from app.services.language_helpers import (
        get_iso639,
        get_language_name,
        get_language_self_name,
    )

    failures: list[str] = []
    for language in curriculum_dispatcher._LANG_MODULES:
        name = get_language_name(language)
        self_name = get_language_self_name(language)
        iso = get_iso639(language)
        if not name.strip() or name == language:
            failures.append(f"{language}: unresolved display name {name!r}")
        if not self_name.strip() or self_name == language:
            failures.append(f"{language}: unresolved self-name {self_name!r}")
        if not iso.strip() or iso == language:
            failures.append(f"{language}: unresolved ISO code {iso!r}")

    assert not failures, "\\n".join(failures)


@pytest.mark.parametrize(
    ("locale", "expected_module"),
    [
        ("hr-HR", "app.data.language_foundations.hr"),
        ("sk-SK", "app.data.language_foundations.sk"),
        ("sl-SI", "app.data.language_foundations.sl"),
        ("lt-LT", "app.data.language_foundations.lt"),
        ("lv-LV", "app.data.language_foundations.lv"),
        ("is-IS", "app.data.language_foundations.is"),
        ("ga-IE", "app.data.language_foundations.ga"),
        ("cy-GB", "app.data.language_foundations.cy"),
        ("az-AZ", "app.data.language_foundations.az"),
        ("kk-KZ", "app.data.language_foundations.kk"),
        ("uz-UZ", "app.data.language_foundations.uz"),
        ("mr-IN", "app.data.language_foundations.mr"),
        ("sq-AL", "app.data.language_foundations.sq"),
        ("eu-ES", "app.data.language_foundations.eu"),
        ("gl-ES", "app.data.language_foundations.gl"),
        ("bs-BA", "app.data.language_foundations.bs"),
        ("ca-ES", "app.data.language_foundations.ca"),
        ("to-TO", "app.data.language_foundations.to"),
    ],
)
def test_foundation_locale_variants_resolve_to_registered_modules(locale: str, expected_module: str):
    assert curriculum_dispatcher._resolve_module(locale).__name__ == expected_module


@pytest.mark.parametrize(
    ("locale", "expected_name", "expected_iso"),
    [
        ("en_US", "English (US)", "en"),
        ("de-DE", "German", "de"),
        ("fr-FR", "French", "fr"),
        ("pt-BR", "Brazilian Portuguese", "pt"),
        ("zh-TW", "Chinese (Traditional)", "zh"),
        ("ar-DZ", "Arabic", "ar"),
        ("hr-HR", "Croatian", "hr"),
        ("sk-SK", "Slovak", "sk"),
        ("sl-SI", "Slovenian", "sl"),
        ("lt-LT", "Lithuanian", "lt"),
        ("lv-LV", "Latvian", "lv"),
        ("az-AZ", "Azerbaijani", "az"),
        ("kk-KZ", "Kazakh", "kk"),
        ("uz-UZ", "Uzbek", "uz"),
        ("suq", "Suri", "suq"),
        ("to-TO", "Tongan", "to"),
    ],
)
def test_language_helpers_normalize_common_locale_aliases(
    locale: str, expected_name: str, expected_iso: str
):
    from app.services.language_helpers import get_iso639, get_language_name

    assert get_language_name(locale) == expected_name
    assert get_iso639(locale) == expected_iso


@pytest.mark.parametrize(
    ("locale", "expected_self_name"),
    [
        ("pt-PT", "Português (Portugal)"),
        ("pt-BR", "Português (Brasil)"),
        ("pt_BR", "Português (Brasil)"),
    ],
)
def test_portuguese_locale_metadata_preserves_regional_variant(locale, expected_self_name):
    from app.services.language_helpers import get_language_self_name

    assert get_language_self_name(locale) == expected_self_name


@pytest.mark.parametrize(
    ("locale", "expected_fragment"),
    [
        ("en_US", "American English"),
        ("en-US", "American English"),
        ("fr-FR", "standard French"),
        ("fr", "standard French"),
        ("pt-BR", "European Portuguese"),
        ("zh-TW", "traditional Chinese"),
        ("ar", "Modern Standard Arabic"),
        ("tr-TR", "standard Turkish"),
        ("ru-RU", "standard Russian"),
        ("hi-IN", "standard Hindi"),
        ("fa", "standard Persian"),
        ("he", "Modern Hebrew"),
        ("th-TH", "standard Thai"),
        ("el-GR", "Modern Greek"),
        ("el", "Modern Greek"),
        ("ro-RO", "standard Romanian"),
        ("uk-UA", "standard Ukrainian"),
        ("bn-BD", "standard Bengali"),
        ("ur-PK", "standard Urdu"),
        ("lo-LA", "standard Lao"),
        ("bo-CN", "standard Tibetan"),
        ("dz-BT", "standard Dzongkha"),
        ("ka-GE", "standard Georgian"),
    ],
)
def test_prompt_overlay_covers_additional_foundation_locales(locale, expected_fragment):
    from app.services.prompts.common import get_language_prompt_overlay

    assert expected_fragment in get_language_prompt_overlay(locale)


def test_registered_languages_have_nonempty_prompt_overlays():
    from app.services.prompts.common import get_language_prompt_overlay

    failures: list[str] = []
    for language in curriculum_dispatcher._LANG_MODULES:
        overlay = get_language_prompt_overlay(language)
        if not overlay.strip():
            failures.append(f"{language}: missing prompt overlay")

    assert not failures, "\n".join(failures)


@pytest.mark.parametrize(
    ("locale", "expected_overlay_fragment"),
    [
        ("hr-HR", "standard Croatian"),
        ("sk-SK", "standard Slovak"),
        ("is-IS", "standard Icelandic"),
        ("ga-IE", "standard Irish"),
        ("az-AZ", "standard Azerbaijani"),
        ("kk-KZ", "standard Kazakh"),
        ("uz-UZ", "standard Uzbek"),
        ("ca-ES", "standard Catalan"),
        ("or-IN", "standard Odia"),
        ("suq", "standard Suri"),
        ("to-TO", "standard Tongan"),
    ],
)
def test_prompt_overlay_locale_aliases_resolve_to_foundation_guidance(locale, expected_overlay_fragment):
    from app.services.prompts.common import get_language_prompt_overlay

    assert expected_overlay_fragment in get_language_prompt_overlay(locale)


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
        ("ro-RO", "latin", "words"),
        ("hr-HR", "latin", "words"),
        ("sk-SK", "latin", "words"),
        ("sl-SI", "latin", "words"),
        ("lt-LT", "latin", "words"),
        ("lv-LV", "latin", "words"),
        ("az-AZ", "latin", "words"),
        ("kk-KZ", "cyrillic", "words"),
        ("uz-UZ", "latin", "words"),
        ("tr-TR", "latin", "words"),
        ("lo-LA", "lao", "characters"),
        ("bo-CN", "tibetan", "characters"),
        ("dz-BT", "tibetan", "characters"),
        ("or-IN", "odia", "words"),
        ("suq", "latin", "words"),
    ],
)
def test_language_capability_aliases_cover_foundation_locales(locale, expected_script, expected_unit):
    from app.services.language_helpers import (
        get_language_script,
        get_reading_length_unit,
    )

    assert get_language_script(locale) == expected_script
    assert get_reading_length_unit(locale) == expected_unit


def test_registered_languages_have_language_capabilities():
    from app.services.language_helpers import (
        get_language_script,
        get_reading_length_unit,
    )

    failures: list[str] = []
    for language in curriculum_dispatcher._LANG_MODULES:
        script = get_language_script(language)
        unit = get_reading_length_unit(language)
        if not script.strip():
            failures.append(f"{language}: missing writing-system capability")
        if unit not in {"words", "characters"}:
            failures.append(f"{language}: invalid reading-length unit {unit!r}")

    assert not failures, "\\n".join(failures)


def test_registered_base_languages_resolve_region_variants_consistently():
    from app.services.language_helpers import get_iso639, get_language_script

    failures: list[str] = []
    for language, expected_module in curriculum_dispatcher._LANG_MODULES.items():
        if "-" in language:
            continue
        locale = f"{language}-ZZ"
        try:
            resolved = curriculum_dispatcher._resolve_module(locale)
        except Exception as exc:
            failures.append(f"{language}: region variant import failed: {exc}")
            continue
        if resolved.__name__ != expected_module:
            failures.append(
                f"{language}: {locale} resolved to {resolved.__name__!r}, expected {expected_module!r}"
            )
        if get_iso639(locale) != get_iso639(language):
            failures.append(
                f"{language}: ISO mismatch for {locale}: "
                f"{get_iso639(locale)!r} != {get_iso639(language)!r}"
            )
        if not get_language_script(locale).strip():
            failures.append(f"{language}: missing capability for {locale}")

    assert not failures, "\\n".join(failures)


def test_bare_language_codes_use_explicit_capability_aliases():
    from app.services.language_helpers import get_language_script, get_reading_length_unit

    # Profile records often store ISO 639-1 codes without a region. Those
    # values must follow the same explicit capability path as their canonical
    # regional locale rather than falling back to English defaults.
    expected = {
        "en": ("latin", "words"),
        "de": ("latin", "words"),
        "es": ("latin", "words"),
        "zh": ("simplified-hanzi", "characters"),
        "ja": ("hiragana-katakana-kanji", "characters"),
        "ko": ("hangul", "words"),
    }
    for locale, (script, unit) in expected.items():
        assert get_language_script(locale) == script
        assert get_reading_length_unit(locale) == unit


@pytest.mark.parametrize(
    ("locale", "expected_script", "expected_unit"),
    [
        ("ro-RO", "latin", "words"), ("hr-HR", "latin", "words"), ("sk-SK", "latin", "words"),
        ("sl-SI", "latin", "words"), ("lt-LT", "latin", "words"), ("lv-LV", "latin", "words"),
        ("ga-IE", "latin", "words"), ("cy-GB", "latin", "words"), ("az-AZ", "latin", "words"),
        ("kk-KZ", "cyrillic", "words"), ("uz-UZ", "latin", "words"), ("bn-BD", "bengali", "words"),
        ("lo-LA", "lao", "characters"), ("bo-CN", "tibetan", "characters"), ("dz-BT", "tibetan", "characters"),
        ("or-IN", "odia", "words"), ("to-TO", "latin", "words"),
    ],
)
def test_explicit_foundation_locale_capability_aliases(locale, expected_script, expected_unit):
    from app.services.language_helpers import get_language_script, get_reading_length_unit
    assert get_language_script(locale) == expected_script
    assert get_reading_length_unit(locale) == expected_unit


def test_registered_core_languages_have_explicit_capabilities():
    from app.services.language_helpers import get_language_script, get_reading_length_unit

    expected = {
        "tr": ("latin", "words"),
        "ru": ("cyrillic", "words"),
        "sv": ("latin", "words"),
    }
    for locale, (script, unit) in expected.items():
        assert get_language_script(locale) == script
        assert get_reading_length_unit(locale) == unit

@pytest.mark.parametrize(
    ("locale", "expected_fragments"),
    [
        ("ar", ['"script": "arabic"', '"reading_length_unit": "words"']),
        ("zh-TW", ['"script": "traditional-hanzi"', '"reading_length_unit": "characters"']),
        ("th-TH", ['"script": "thai"', '"reading_length_unit": "characters"']),
        ("ro-RO", ['"script": "latin"', '"reading_length_unit": "words"']),
    ],
)
def test_lesson_generation_exposes_language_capabilities_to_prompt_layer(
    locale: str, expected_fragments: list[str]
):
    from app.services.lesson_generator import _language_capability_metadata

    metadata = _language_capability_metadata(locale, "A1")
    for fragment in expected_fragments:
        assert fragment in metadata


def test_lesson_prompt_builders_accept_language_capabilities():
    from app.services.prompts.lesson import (
        build_fill_blank_eval_prompt,
        build_free_write_eval_prompt,
        build_lesson_generation_prompt,
        build_pronunciation_eval_prompt,
        build_regenerate_exercise_prompt,
    )

    capability = '{"script":"arabic","uses_word_spacing":true,"reading_length_unit":"words"}'
    generation = build_lesson_generation_prompt(
        cefr_level="A1",
        target_language_name="Arabic",
        native_language_name="English",
        lesson_type="reading",
        topic="Greetings",
        unit_id="a1-unit-1",
        grammar_points="none",
        vocabulary_set_ids="general",
        day=1,
        valid_slugs="",
        language_prompt_overlay="Arabic overlay",
        language_capabilities=capability,
    )
    assert capability in generation

    fill = build_fill_blank_eval_prompt(
        cefr_level="A1",
        target_language_name="Arabic",
        native_language_name="English",
        question="___ أنا",
        correct_answer="أنا",
        student_answer="أنا",
        language_prompt_overlay="Arabic overlay",
        language_capabilities=capability,
    )
    assert capability in fill

    writing = build_free_write_eval_prompt(
        cefr_level="A1",
        target_language_name="Arabic",
        native_language_name="English",
        prompt="اكتب جملة.",
        criteria="grammar",
        answer="أنا طالب.",
        language_prompt_overlay="Arabic overlay",
        language_capabilities=capability,
    )
    assert capability in writing

    pronunciation = build_pronunciation_eval_prompt(
        cefr_level="A1",
        target_language_name="Arabic",
        native_language_name="English",
        target="مرحبا",
        transcription="مرحبا",
        language_prompt_overlay="Arabic overlay",
        language_capabilities=capability,
    )
    assert capability in pronunciation

    regenerate = build_regenerate_exercise_prompt(
        cefr_level="A1",
        target_language_name="Arabic",
        native_language_name="English",
        lesson_type="reading",
        topic="Greetings",
        exercise_type="multiple_choice",
        lesson_explanation="{}",
        lesson_vocabulary="[]",
        invalid_exercise="{}",
        options_schema='["a","b","c","d"]',
        language_prompt_overlay="Arabic overlay",
        language_capabilities=capability,
    )
    assert capability in regenerate


def test_registered_languages_have_complete_display_metadata():
    failures: list[str] = []
    for language in curriculum_dispatcher._LANG_MODULES:
        name = get_language_name(language)
        self_name = get_language_self_name(language)
        iso639 = get_iso639(language)
        if not name.strip() or name == language:
            failures.append(f"{language}: missing display name")
        if not self_name.strip() or self_name == language:
            failures.append(f"{language}: missing self name")
        if not iso639.strip():
            failures.append(f"{language}: missing ISO 639 code")
    assert not failures, "\n".join(failures)


@pytest.mark.parametrize(
    ("locale", "expected_iso"),
    [
        ("hr-HR", "hr"),
        ("sk-SK", "sk"),
        ("sl-SI", "sl"),
        ("lt-LT", "lt"),
        ("lv-LV", "lv"),
        ("is-IS", "is"),
        ("ga-IE", "ga"),
        ("cy-GB", "cy"),
        ("az-AZ", "az"),
        ("kk-KZ", "kk"),
        ("uz-UZ", "uz"),
        ("ar-DZ", "ar"),
        ("zh-TW", "zh"),
        ("pt-BR", "pt"),
        ("en_US", "en"),
    ],
)
def test_language_metadata_resolves_locale_variants(locale: str, expected_iso: str):
    assert get_iso639(locale) == expected_iso
    assert get_language_name(locale).strip()
    assert get_language_self_name(locale).strip()

@pytest.mark.parametrize(
    ("locale", "expected_name", "expected_self_name", "expected_script"),
    [
        ("pt-BR", "Brazilian Portuguese", "Português (Brasil)", "latin"),
        ("PT_br", "Brazilian Portuguese", "Português (Brasil)", "latin"),
        ("zh-Hant", "Traditional Chinese", "繁體中文", "traditional-hanzi"),
        ("zh-Hant-TW", "Chinese (Traditional, Taiwan)", "臺灣繁體中文", "traditional-hanzi"),
        ("zh-Hant-HK", "Traditional Chinese", "繁體中文", "traditional-hanzi"),
        ("zh-HK", "Traditional Chinese (Hong Kong)", "繁體中文（香港）", "traditional-hanzi"),
        ("zh-MO", "Traditional Chinese (Macau)", "繁體中文（澳門）", "traditional-hanzi"),
    ],
)
def test_script_and_region_sensitive_language_metadata(
    locale: str, expected_name: str, expected_self_name: str, expected_script: str
):
    from app.services.language_helpers import get_language_script

    assert get_language_name(locale) == expected_name
    assert get_language_self_name(locale) == expected_self_name
    assert get_language_script(locale) == expected_script


@pytest.mark.parametrize(
    ("locale", "expected_fragment"),
    [
        ("pt-BR", "standard Brazilian Portuguese"),
        ("PT_br", "standard Brazilian Portuguese"),
        ("zh-Hant", "Traditional Chinese"),
        ("zh-Hant-TW", "traditional Chinese characters"),
        ("zh-HK", "traditional Chinese characters"),
        ("zh-MO", "traditional Chinese characters"),
    ],
)
def test_prompt_overlay_preserves_script_and_regional_variant(locale: str, expected_fragment: str):
    assert expected_fragment.lower() in get_language_prompt_overlay(locale).lower()


@pytest.mark.parametrize(
    "locale",
    [
        "en_US",
        "de-DE",
        "es-ES",
        "pt-BR",
        "zh-TW",
        "ar-DZ",
        "hr-HR",
        "sk-SK",
        "sl-SI",
        "lt-LT",
        "lv-LV",
        "az-AZ",
        "kk-KZ",
        "uz-UZ",
    ],
)
def test_prompt_overlay_resolves_locale_aliases(locale: str):
    overlay = get_language_prompt_overlay(locale)
    assert overlay.strip(), f"{locale}: prompt overlay resolved to empty text"



def test_generic_prompt_overlay_handles_uncurated_locale_without_runtime_error():
    from app.services.prompts.common import get_language_prompt_overlay

    overlay = get_language_prompt_overlay("zz-ZZ")
    assert "reading-length decisions" in overlay
    assert "100 words" in overlay

def test_registered_foundation_languages_have_prompt_guidance():
    failures: list[str] = []
    for language in curriculum_dispatcher._LANG_MODULES:
        if not get_language_prompt_overlay(language).strip():
            failures.append(f"{language}: missing language-specific prompt overlay")
    assert not failures, "\n".join(failures)



@pytest.mark.parametrize(
    ("locale", "expected_iso", "expected_module"),
    [
        ("HR-hr", "hr", "app.data.language_foundations.hr"),
        ("SK-sk", "sk", "app.data.language_foundations.sk"),
        ("ZH-tw", "zh", "app.data.zh.curriculum"),
        ("PT-br", "pt", "app.data.pt.curriculum"),
        ("EN-us", "en", "app.data.en_US.curriculum"),
        ("GA-ie", "ga", "app.data.language_foundations.ga"),
    ],
)
def test_locale_lookup_is_case_insensitive(locale: str, expected_iso: str, expected_module: str):
    from app.services.prompts.common import get_language_prompt_overlay

    assert get_iso639(locale) == expected_iso
    assert get_language_name(locale).strip()
    assert get_language_self_name(locale).strip()
    assert curriculum_dispatcher._resolve_module(locale).__name__ == expected_module
    assert get_language_prompt_overlay(locale).strip()

def test_foundation_locale_registry_matches_registered_foundation_modules():
    """Keep region fallback codes and foundation module registrations in sync."""
    registered_foundations = {
        language
        for language, module_path in curriculum_dispatcher._LANG_MODULES.items()
        if module_path.startswith("app.data.language_foundations.")
    }
    assert registered_foundations == curriculum_dispatcher._FOUNDATION_LOCALE_REGIONS


def test_explicit_locale_aliases_point_to_registered_curricula():
    """A locale alias must never route to a missing curriculum module key."""
    invalid = {
        locale: canonical
        for locale, canonical in curriculum_dispatcher._LOCALE_ALIASES.items()
        if canonical not in curriculum_dispatcher._LANG_MODULES
    }
    assert not invalid, f"Locale aliases target unregistered curricula: {invalid}"

def test_registered_languages_use_two_or_three_letter_iso_codes():
    failures: list[str] = []
    for language in curriculum_dispatcher._LANG_MODULES:
        code = get_iso639(language)
        if len(code) not in {2, 3} or not code.isalpha() or code != code.lower():
            failures.append(f"{language}: invalid ISO 639 language identifier {code!r}")
    assert not failures, "\\n".join(failures)

def test_registered_base_locales_keep_metadata_and_prompt_guidance_for_region_variants():
    from app.services.language_helpers import (
        get_iso639,
        get_language_name,
        get_language_script,
        get_language_self_name,
    )
    from app.services.prompts.common import get_language_prompt_overlay

    failures: list[str] = []
    for language, expected_module in curriculum_dispatcher._LANG_MODULES.items():
        if "-" in language:
            continue

        locale = f"{language}-ZZ"
        try:
            module = curriculum_dispatcher._resolve_module(locale)
            name = get_language_name(locale)
            self_name = get_language_self_name(locale)
            iso = get_iso639(locale)
            script = get_language_script(locale)
            overlay = get_language_prompt_overlay(locale)
        except Exception as exc:
            failures.append(f"{language}: region variant {locale} failed: {exc}")
            continue

        if module.__name__ != expected_module:
            failures.append(
                f"{language}: {locale} resolved to {module.__name__!r}, expected {expected_module!r}"
            )
        if name != get_language_name(language):
            failures.append(f"{language}: display name changed for {locale}: {name!r}")
        if self_name != get_language_self_name(language):
            failures.append(f"{language}: self-name changed for {locale}: {self_name!r}")
        if iso != get_iso639(language):
            failures.append(f"{language}: ISO code changed for {locale}: {iso!r}")
        if not script.strip():
            failures.append(f"{language}: missing script for {locale}")
        if not overlay.strip() or name not in overlay:
            failures.append(f"{language}: prompt overlay for {locale} lacks language name {name!r}")

    assert not failures, "\\n".join(failures)

