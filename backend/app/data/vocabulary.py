"""
Language-aware vocabulary dispatcher.

Mirrors the curriculum dispatcher pattern: resolves the correct
per-language vocabulary module by ISO 639-1 prefix.
"""

from __future__ import annotations

import sys

from app.data._types import CEFRLevel, VocabularyEntry, VocabularySet  # noqa: F401

_LANG_MODULES: dict[str, str] = {
    "en-GB": "app.data.en_GB.vocabulary",
    "en-US": "app.data.en_US.vocabulary",
    "de": "app.data.de.vocabulary",
    "es": "app.data.es.vocabulary",
    "fr": "app.data.fr.vocabulary",
    "it": "app.data.it.vocabulary",
    "ja": "app.data.ja.vocabulary",
    "ko": "app.data.ko.vocabulary",
    "pt": "app.data.pt.vocabulary",
    "zh": "app.data.zh.vocabulary",
    "ar": "app.data.ar.vocabulary",
    "tr": "app.data.tr.vocabulary",
    "ru": "app.data.ru.vocabulary",
    "nl": "app.data.nl.vocabulary",
    "pl": "app.data.pl.vocabulary",
    "el": "app.data.el.vocabulary",
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
    "sq": "app.data.language_foundations.sq", "eu": "app.data.language_foundations.eu", "gl": "app.data.language_foundations.gl", "mt": "app.data.language_foundations.mt", "af": "app.data.language_foundations.af",
    "eo": "app.data.language_foundations.eo", "lb": "app.data.language_foundations.lb", "gd": "app.data.language_foundations.gd", "yo": "app.data.language_foundations.yo", "ha": "app.data.language_foundations.ha",
    "am": "app.data.language_foundations.am", "so": "app.data.language_foundations.so", "zu": "app.data.language_foundations.zu", "xh": "app.data.language_foundations.xh", "rw": "app.data.language_foundations.rw",
    "ig": "app.data.language_foundations.ig", "mg": "app.data.language_foundations.mg", "ny": "app.data.language_foundations.ny", "sn": "app.data.language_foundations.sn", "st": "app.data.language_foundations.st",
}

_CACHE: dict[str, list[VocabularySet]] = {}


def _resolve_sets(target_language: str) -> list[VocabularySet]:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.en_GB.vocabulary"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name].VOCABULARY_SETS

    return _CACHE[module_name]


def get_vocabulary_sets(target_language: str = "en-GB") -> list[VocabularySet]:
    """Return all vocabulary sets for the given target language."""
    return _resolve_sets(target_language)


def get_vocabulary_set(set_id: str, target_language: str = "en-GB") -> VocabularySet | None:
    """Return a single vocabulary set by ID for the given target language."""
    sets = _resolve_sets(target_language)
    for s in sets:
        if s.id == set_id:
            return s
    return None


def get_vocabulary_by_level(
    level: CEFRLevel, target_language: str = "en-GB"
) -> list[VocabularySet]:
    """Return all vocabulary sets for a specific CEFR level."""
    sets = _resolve_sets(target_language)
    return [s for s in sets if s.level == level]
