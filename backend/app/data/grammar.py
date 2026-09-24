"""
Language-aware grammar dispatcher.

Mirrors the vocabulary/phrasebook dispatcher pattern: resolves the correct
per-language grammar module by ISO 639-1 prefix.
"""

from __future__ import annotations

import sys

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic  # noqa: F401

_LANG_MODULES: dict[str, str] = {
    "en-GB": "app.data.en_GB.grammar",
    "en-US": "app.data.en_US.grammar",
    "de": "app.data.de.grammar",
    "es": "app.data.es.grammar",
    "fr": "app.data.fr.grammar",
    "it": "app.data.it.grammar",
    "ja": "app.data.ja.grammar",
    "ko": "app.data.ko.grammar",
    "pt": "app.data.pt.grammar",
    "zh": "app.data.zh.grammar",
    "ar": "app.data.ar.grammar",
    "tr": "app.data.tr.grammar",
    "ru": "app.data.ru.grammar",
    "nl": "app.data.nl.grammar",
    "pl": "app.data.pl.grammar",
    "el": "app.data.el.grammar",
    "sv": "app.data.sv.grammar",
    "da": "app.data.da.grammar",
    "no": "app.data.no.grammar",
    "fi": "app.data.fi.grammar",
    "cs": "app.data.cs.grammar",
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

_CACHE: dict[str, list[GrammarTopic]] = {}


def _resolve_topics(target_language: str) -> list[GrammarTopic]:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.en_GB.grammar"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name].GRAMMAR_TOPICS

    return _CACHE[module_name]


def get_grammar_topics(target_language: str = "en-GB") -> list[GrammarTopic]:
    """Return all grammar topics for the given target language."""
    return _resolve_topics(target_language)


def get_grammar_topic(slug: str, target_language: str = "en-GB") -> GrammarTopic | None:
    """Return a single grammar topic by slug for the given target language."""
    topics = _resolve_topics(target_language)
    for t in topics:
        if t.slug == slug:
            return t
    return None
