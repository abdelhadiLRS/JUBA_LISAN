"""
Language-aware assessment bank dispatcher.

Mirrors the curriculum dispatcher pattern: resolves the correct
per-language assessment bank module by ISO 639-1 prefix.
"""

from __future__ import annotations

import sys

from app.data._types import AssessmentQuestion  # noqa: F401

_LANG_MODULES: dict[str, str] = {
    "en-GB": "app.data.en_GB.assessment_bank",
    "en-US": "app.data.en_US.assessment_bank",
    "de": "app.data.de.assessment_bank",
    "es": "app.data.es.assessment_bank",
    "fr": "app.data.fr.assessment_bank",
    "it": "app.data.it.assessment_bank",
    "ja": "app.data.ja.assessment_bank",
    "ko": "app.data.ko.assessment_bank",
    "pt": "app.data.pt.assessment_bank",
    "zh": "app.data.zh.assessment_bank",
    "ar": "app.data.ar.assessment_bank",
    "tr": "app.data.tr.assessment_bank",
    "ru": "app.data.ru.assessment_bank",
    "nl": "app.data.nl.assessment_bank",
    "pl": "app.data.pl.assessment_bank",
    "el": "app.data.el.assessment_bank",
    "sv": "app.data.language_foundations.sv",
    "da": "app.data.language_foundations.da",
    "no": "app.data.language_foundations.no",
    "fi": "app.data.language_foundations.fi",
    "cs": "app.data.language_foundations.cs",
    "ro": "app.data.language_foundations.ro",
    "hu": "app.data.language_foundations.hu",
    "uk": "app.data.language_foundations.uk",
    "he": "app.data.language_foundations.he",
    "vi": "app.data.language_foundations.vi",
    "bg": "app.data.language_foundations.bg",
    "sr": "app.data.language_foundations.sr",
    "hr": "app.data.language_foundations.hr",
    "sk": "app.data.language_foundations.sk",
    "sl": "app.data.language_foundations.sl",
    "lt": "app.data.language_foundations.lt",
    "lv": "app.data.language_foundations.lv",
    "is": "app.data.language_foundations.is",
    "ga": "app.data.language_foundations.ga",
    "cy": "app.data.language_foundations.cy",
    "ka": "app.data.language_foundations.ka",
    "hy": "app.data.language_foundations.hy",
    "az": "app.data.language_foundations.az",
    "kk": "app.data.language_foundations.kk",
    "uz": "app.data.language_foundations.uz",
    "ur": "app.data.language_foundations.ur",
    "ta": "app.data.language_foundations.ta",
    "te": "app.data.language_foundations.te",
    "mr": "app.data.language_foundations.mr",
    "gu": "app.data.language_foundations.gu",
}

_CACHE: dict[str, list[AssessmentQuestion]] = {}


def _resolve_bank(target_language: str) -> list[AssessmentQuestion]:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.en_GB.assessment_bank"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name].ASSESSMENT_BANK

    return _CACHE[module_name]


def get_assessment_bank(target_language: str = "en-GB") -> list[AssessmentQuestion]:
    """Return the full assessment bank for the given target language."""
    return _resolve_bank(target_language)
