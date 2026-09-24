"""
Language-aware phrasebook dispatcher.

Mirrors the vocabulary dispatcher pattern: resolves the correct
per-language phrasebook module by ISO 639-1 prefix.
"""

from __future__ import annotations

import sys

from app.data._types import CEFRLevel, PhrasebookCategory, PhrasebookEntry  # noqa: F401

_LANG_MODULES: dict[str, str] = {
    "en-GB": "app.data.en_GB.phrasebook",
    "en-US": "app.data.en_US.phrasebook",
    "de": "app.data.de.phrasebook",
    "es": "app.data.es.phrasebook",
    "fr": "app.data.fr.phrasebook",
    "it": "app.data.it.phrasebook",
    "ja": "app.data.ja.phrasebook",
    "ko": "app.data.ko.phrasebook",
    "pt": "app.data.pt.phrasebook",
    "zh": "app.data.zh.phrasebook",
    "ar": "app.data.ar.phrasebook",
    "tr": "app.data.tr.phrasebook",
    "ru": "app.data.ru.phrasebook",
    "nl": "app.data.nl.phrasebook",
    "pl": "app.data.pl.phrasebook",
    "el": "app.data.el.phrasebook",
    "sv": "app.data.language_foundations.sv",
    "da": "app.data.da.phrasebook",
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

_CACHE: dict[str, list[PhrasebookCategory]] = {}


def _resolve_categories(target_language: str) -> list[PhrasebookCategory]:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.en_GB.phrasebook"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name].PHRASEBOOK_CATEGORIES

    return _CACHE[module_name]


def get_phrasebook_categories(
    target_language: str = "en-GB",
) -> list[PhrasebookCategory]:
    """Return all phrasebook categories for the given target language."""
    return _resolve_categories(target_language)


def get_phrasebook_category(
    category_id: str, target_language: str = "en-GB"
) -> PhrasebookCategory | None:
    """Return a single phrasebook category by ID for the given target language."""
    categories = _resolve_categories(target_language)
    for c in categories:
        if c.id == category_id:
            return c
    return None


def get_phrasebook_by_level(
    level: CEFRLevel, target_language: str = "en-GB"
) -> list[PhrasebookCategory]:
    """Return all phrasebook categories for a specific CEFR level."""
    categories = _resolve_categories(target_language)
    return [c for c in categories if c.level == level]
