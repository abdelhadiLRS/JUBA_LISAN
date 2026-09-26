from __future__ import annotations

import pytest

from app.data.curriculum import get_curriculum
from app.services.language_helpers import (
    get_language_name,
    get_language_script,
    get_reading_length_unit,
    uses_word_spacing,
)
from app.services.locale import normalize_locale, resolve_locale
from app.services.prompts.common import get_language_prompt_overlay


@pytest.mark.parametrize(
    ("locale", "canonical", "base"),
    [
        ("hr-HR", "hr", "hr"),
        ("sk-SK", "sk", "sk"),
        ("ar-DZ", "ar", "ar"),
        ("zh-TW", "zh", "zh"),
        ("pt-BR", "pt-BR", "pt"),
        ("suq-ET", "suq", "suq"),
        ("fr-CA", "fr", "fr"),
        ("de-AT", "de", "de"),
        ("en-AU", "en-AU", "en"),
        ("zh-Hant-HK", "zh", "zh"),
    ],
)
def test_locale_contract_resolves_registered_regional_variants(locale, canonical, base):
    resolution = resolve_locale(locale)

    assert resolution.normalized == locale
    assert resolution.canonical == canonical
    assert resolution.base == base
    assert get_language_script(locale) == resolution.capability["script"]
    assert get_reading_length_unit(locale) == resolution.capability["reading_length_unit"]
    assert uses_word_spacing(locale) == resolution.capability["uses_word_spacing"]
    assert get_language_name(locale) == resolution.metadata["name"]


@pytest.mark.parametrize("locale", ["hr-HR", "sk-SK", "ar-DZ", "zh-TW", "pt-BR", "suq-ET"])
def test_locale_contract_drives_curriculum_and_prompt_layers(locale):
    resolution = resolve_locale(locale)
    curriculum = get_curriculum(locale)
    overlay = get_language_prompt_overlay(locale)

    assert curriculum
    assert "A1" in curriculum
    assert overlay.startswith("Language-specific guidance:")
    assert resolution.base not in {"en", "en-GB"} or locale.startswith("en-")


@pytest.mark.parametrize(
    ("locale", "expected_script", "expected_unit"),
    [
        ("fr-CA", "latin", "words"),
        ("de-AT", "latin", "words"),
        ("en-AU", "latin", "words"),
        ("zh-Hant-HK", "traditional-hanzi", "characters"),
    ],
)
def test_unregistered_regional_variants_inherit_foundation_capabilities(locale, expected_script, expected_unit):
    resolution = resolve_locale(locale)

    assert resolution.base in {"fr", "de", "en", "zh"}
    assert resolution.capability["script"] == expected_script
    assert resolution.capability["reading_length_unit"] == expected_unit
    assert get_language_script(locale) == expected_script
    assert get_reading_length_unit(locale) == expected_unit


def test_unknown_locale_keeps_a_safe_generation_capability():
    resolution = resolve_locale("xx-ZZ")

    assert resolution.normalized == "xx-ZZ"
    assert resolution.base == "xx"
    assert resolution.canonical == "xx"
    assert resolution.capability["script"] == "latin"
    assert resolution.capability["uses_word_spacing"] is True
    assert resolution.capability["reading_length_unit"] == "words"


def test_locale_normalization_is_shared_for_underscored_and_cased_input():
    assert normalize_locale("pt_br") == "pt-BR"
    assert normalize_locale("AR_dz") == "ar-DZ"
    assert resolve_locale("SUQ_et").canonical == "suq"


def test_additional_foundation_languages_have_cefr_curricula():
    """New foundation languages must resolve to real multi-level lesson sequences."""
    from app.data.curriculum import get_units

    expected = {
        "ceb": 8,
        "haw": 4,
        "id": 4,
        "sw": 4,
        "km": 4,
        "kn": 4,
    }

    for locale, minimum_units in expected.items():
        for level in ("A2", "B1", "B2", "C1", "C2"):
            units = get_units(level, locale)
            assert len(units) >= minimum_units, (locale, level, len(units))
            assert all(unit.id.startswith(f"{locale}-{level.lower()}-") for unit in units)
