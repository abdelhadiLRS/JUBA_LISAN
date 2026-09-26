"""Shared prompt fragments used across LLM-backed services."""

JSON_ONLY_INSTRUCTION = (
    "IMPORTANT: Respond with ONLY a valid JSON object. "
    "No markdown, no code fences, no extra text."
)

STRUCTURED_OUTPUT_RETRY_PROMPT = (
    "That response was not valid JSON. Error: {error}. " "Please return ONLY the JSON object."
)

ANTHROPIC_SYSTEM_ONLY_TRIGGER = "Generate the content as specified."
TUTOR_DISPLAY_NAME = "Lingu"

_LANGUAGE_PROMPT_OVERLAYS: dict[str, str] = {
    "en-US": """
Language-specific guidance:
- Use American English spelling, vocabulary, punctuation, and idiom consistently.
- Prefer US forms such as color, center, organize, apartment, elevator, truck, and vacation.
- Avoid British-only spelling and vocabulary unless explicitly comparing variants.
""".strip(),
    "en-GB": """
Language-specific guidance:
- Use British English spelling, vocabulary, punctuation, and idiom consistently.
- Prefer UK forms such as colour, centre, organise, flat, lift, lorry, and holiday.
- Avoid American-only spelling and vocabulary unless explicitly comparing variants.
""".strip(),
    "es-ES": """
Language-specific guidance:
- Use Peninsular Spanish from Spain consistently.
- Prefer Spain usage, including vosotros for informal plural address when appropriate.
- Avoid voseo and Latin American-only vocabulary unless explicitly comparing variants.
- Pay close attention to accents, gender, number agreement, and natural Spain Spanish phrasing.
""".strip(),
    "it-IT": """
Language-specific guidance:
- Use standard Italian as used in Italy consistently.
- Pay close attention to articles, gender, number agreement, articulated prepositions, and clitic pronouns.
- Use tu or Lei consistently according to the context and learner level.
- Avoid strong regionalisms unless explicitly teaching or comparing them.
""".strip(),
    "pt-PT": """
Language-specific guidance:
- Use European Portuguese from Portugal consistently.
- Avoid Brazilian Portuguese vocabulary, syntax, and pronoun placement unless explicitly comparing variants.
- Prefer Portugal usage such as telemóvel, autocarro, pequeno-almoço, and comboio.
- Pay close attention to European Portuguese clitic placement, contractions, accents, and register.
""".strip(),
    "fr-FR": """
Language-specific guidance:
- Use standard French from France consistently.
- Pay close attention to accents, elision, contractions, gender, number agreement, and register.
- Use tu or vous consistently according to the context and learner level.
- Avoid Canadian or other regional French variants unless explicitly comparing them.
""".strip(),
    "de-DE": """
Language-specific guidance:
- Use standard German spelling and vocabulary as used in Germany consistently.
- Pay close attention to noun capitalization, grammatical gender, cases, adjective endings, and verb position.
- Use du or Sie consistently according to the context and learner level.
- Avoid Austrian or Swiss variants unless explicitly comparing them.
""".strip(),
    "ja-JP": """
Language-specific guidance:
- Use standard Japanese as used in Japan consistently.
- Use Japanese script naturally: hiragana, katakana, and level-appropriate kanji. Use romaji only as a short support aid for beginners or when explicitly teaching pronunciation.
- Pay close attention to particles, politeness level, verb forms, counters, and natural word order.
- Keep register consistent with the learner level; avoid abrupt shifts between plain and polite style unless teaching the contrast.
""".strip(),
    "ko-KR": """
Language-specific guidance:
- Use standard Korean as used in South Korea consistently.
- Use Hangul as the primary script. Use romanization only as a short support aid for beginners or when explicitly teaching pronunciation.
- Pay close attention to particles, speech level, honorifics, verb endings, batchim, and natural Korean phrasing.
- Avoid North Korean vocabulary, spelling, or usage unless explicitly comparing variants.
""".strip(),
    "ar": """
Language-specific guidance:
- Use Modern Standard Arabic consistently unless a regional variety is explicitly requested.
- Use Arabic script as the primary writing system and preserve correct right-to-left text.
- Pay close attention to gender, number, case endings when taught, verb patterns, agreement, and natural word order.
- Do not mix dialect vocabulary into standard Arabic lessons unless explicitly teaching a dialect.
""".strip(),
    "tr-TR": """
Language-specific guidance:
- Use standard Turkish from Türkiye consistently.
- Use Turkish Latin orthography and preserve diacritics such as ç, ğ, ı, İ, ö, ş, and ü.
- Pay close attention to vowel harmony, agglutination, case suffixes, evidentiality, and natural word order.
""".strip(),
    "ru-RU": """
Language-specific guidance:
- Use standard Russian consistently.
- Use Cyrillic as the primary script.
- Pay close attention to case, gender, aspect, verb conjugation, stress where relevant, and natural word order.
""".strip(),
    "nl-NL": """
Language-specific guidance:
- Use standard Dutch from the Netherlands consistently.
- Pay close attention to word order, separable verbs, articles, diminutives, and de/het distinctions.
- Avoid Belgian Dutch variants unless explicitly comparing them.
""".strip(),
    "pl-PL": """
Language-specific guidance:
- Use standard Polish consistently.
- Use Polish Latin orthography and preserve diacritics.
- Pay close attention to grammatical case, gender, aspect, consonant alternations, and natural word order.
""".strip(),
    "sv-SE": """
Language-specific guidance:
- Use standard Swedish from Sweden consistently.
- Pay close attention to definite forms, word order, noun gender, verb forms, and natural Swedish phrasing.
""".strip(),
    "da-DK": """
Language-specific guidance:
- Use standard Danish from Denmark consistently.
- Pay close attention to word order, definite forms, noun gender, verb placement, and natural Danish phrasing.
""".strip(),
    "no-NO": """
Language-specific guidance:
- Use standard Norwegian Bokmål for generated learner content.
- Keep spelling and grammar consistent with Bokmål rather than switching to Nynorsk.
""".strip(),
    "fi-FI": """
Language-specific guidance:
- Use standard Finnish consistently.
- Pay close attention to case endings, consonant gradation, vowel harmony, possessive structures, and natural word order.
""".strip(),
    "cs-CZ": """
Language-specific guidance:
- Use standard Czech consistently.
- Use Czech Latin orthography and preserve diacritics.
- Pay close attention to grammatical case, gender, aspect, declension, and natural word order.
""".strip(),
    "vi": """
Language-specific guidance:
- Use standard Vietnamese consistently.
- Use Vietnamese Latin orthography and preserve tone marks and diacritics.
- Pay close attention to classifiers, pronouns, word order, and register.
""".strip(),
    "zh-TW": """
Language-specific guidance:
- Use Taiwan Standard Mandarin consistently.
- Use traditional Chinese characters as the primary writing system. Use pinyin only as pronunciation support when appropriate.
- Avoid simplified-character forms and Mainland-specific vocabulary unless explicitly comparing variants.
""".strip(),
    "hi": """
Language-specific guidance:
- Use standard Hindi consistently.
- Use Devanagari as the primary script.
- Pay close attention to postpositions, gender agreement, verb aspect, honorifics, and natural Hindi word order.
""".strip(),
    "fa": """
Language-specific guidance:
- Use standard Persian consistently.
- Use Persian-Arabic script as the primary writing system and preserve correct right-to-left text.
- Pay close attention to ezafe, verb constructions, pronouns, colloquial versus formal register, and natural word order.
""".strip(),
    "he": """
Language-specific guidance:
- Use Modern Hebrew consistently.
- Use Hebrew script as the primary writing system.
- Pay close attention to gender agreement, construct state, verb patterns, definiteness, and natural modern usage.
""".strip(),
    "th": """
Language-specific guidance:
- Use standard Thai consistently.
- Use Thai script as the primary writing system.
- Pay close attention to tones, classifiers, particles, politeness, and natural Thai word order.
""".strip(),
    "zh-CN": """
Language-specific guidance:
- Use Mainland China Standard Mandarin (Putonghua) consistently.
- Use simplified Chinese characters. Use pinyin with tone marks only as support for pronunciation or beginner scaffolding, never as the main writing system.
- Pay close attention to tones, measure words, aspect particles, word order, and natural Mainland usage.
- Avoid Traditional Chinese, Cantonese, Taiwan, Hong Kong, or Macau variants unless explicitly comparing them.
""".strip(),
    "ro": "Language-specific guidance:\n- Use standard Romanian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Romanian diacritics (ă, â, î, ș, ț).\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "hu": "Language-specific guidance:\n- Use standard Hungarian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Hungarian diacritics; pay close attention to vowel harmony, case suffixes, and definite/indefinite conjugation.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "uk": "Language-specific guidance:\n- Use standard Ukrainian consistently.\n- Use Cyrillic as the primary writing system and preserve its standard orthography.\n- Do not substitute Russian vocabulary or spelling.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "bg": "Language-specific guidance:\n- Use standard Bulgarian consistently.\n- Use Cyrillic as the primary writing system and preserve its standard orthography.\n- Pay close attention to definite articles, aspect, and standard Bulgarian vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "sr": "Language-specific guidance:\n- Use standard Serbian consistently.\n- Use Cyrillic as the primary writing system and preserve its standard orthography.\n- Use standard Serbian; use Latin only when explicitly requested.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "hr": "Language-specific guidance:\n- Use standard Croatian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Croatian diacritics and standard Croatian vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "sk": "Language-specific guidance:\n- Use standard Slovak consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Slovak diacritics and declension.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "sl": "Language-specific guidance:\n- Use standard Slovenian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Slovenian diacritics and distinguish dual forms where relevant.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "lt": "Language-specific guidance:\n- Use standard Lithuanian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Pay close attention to case and declension.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "lv": "Language-specific guidance:\n- Use standard Latvian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Pay close attention to case and declension.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "et": "Language-specific guidance:\n- Use standard Estonian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Pay close attention to case forms and consonant gradation.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "el": "Language-specific guidance:\n- Use standard Greek consistently.\n- Use Greek as the primary writing system and preserve its standard orthography.\n- Preserve Greek accents and standard spelling.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ka": "Language-specific guidance:\n- Use standard Georgian consistently.\n- Use Georgian as the primary writing system and preserve its standard orthography.\n- Use Georgian script and standard Georgian morphology.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "hy": "Language-specific guidance:\n- Use standard Eastern Armenian consistently.\n- Use Armenian as the primary writing system and preserve its standard orthography.\n- Use Armenian script and standard Eastern Armenian vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "am": "Language-specific guidance:\n- Use standard Amharic consistently.\n- Use Ethiopic (Ge'ez) as the primary writing system and preserve its standard orthography.\n- Use Ethiopic script and standard Amharic morphology.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ti": "Language-specific guidance:\n- Use standard Tigrinya consistently.\n- Use Ethiopic (Ge'ez) as the primary writing system and preserve its standard orthography.\n- Use Ethiopic script and standard Tigrinya morphology.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "mr": "Language-specific guidance:\n- Use standard Marathi consistently.\n- Use Devanagari as the primary writing system and preserve standard Marathi orthography.\n- Preserve Marathi-specific vocabulary and grammar rather than substituting Hindi forms.\n- Pay close attention to agreement, inflection, natural word order, and learner-appropriate register.",
    "ku": "Language-specific guidance:\n- Use standard Kurdish consistently and follow the curriculum's selected Kurdish variety.\n- Preserve the script and orthography used by the supplied Kurdish curriculum content; do not silently substitute Turkish, Persian, or Arabic vocabulary.\n- Keep regional or dialectal variation explicit when it is relevant to the lesson.\n- Pay close attention to agreement, inflection, natural word order, and learner-appropriate register.",
    "bn": "Language-specific guidance:\n- Use standard Bengali consistently.\n- Use Bengali as the primary writing system and preserve its standard orthography.\n- Use Bengali script and standard Bengali vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ta": "Language-specific guidance:\n- Use standard Tamil consistently.\n- Use Tamil as the primary writing system and preserve its standard orthography.\n- Use Tamil script and distinguish formal and spoken register when relevant.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "te": "Language-specific guidance:\n- Use standard Telugu consistently.\n- Use Telugu as the primary writing system and preserve its standard orthography.\n- Use Telugu script and standard Telugu morphology.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "gu": "Language-specific guidance:\n- Use standard Gujarati consistently.\n- Use Gujarati as the primary writing system and preserve its standard orthography.\n- Use Gujarati script and standard Gujarati morphology.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ur": "Language-specific guidance:\n- Use standard Urdu consistently.\n- Use Urdu Nastaliq/Arabic-derived as the primary writing system and preserve its standard orthography.\n- Preserve right-to-left text and standard Urdu register.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "lo": "Language-specific guidance:\n- Use standard Lao consistently.\n- Use Lao as the primary writing system and preserve its standard orthography.\n- Do not insert English-style spaces between every Lao word.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "dz": "Language-specific guidance:\n- Use standard Dzongkha consistently.\n- Use Tibetan-derived as the primary writing system and preserve its standard orthography.\n- Use standard Dzongkha spelling; use romanization only as learner support.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "bo": "Language-specific guidance:\n- Use standard Tibetan consistently.\n- Use Tibetan as the primary writing system and preserve its standard orthography.\n- Use Tibetan script; use Wylie only as learner support.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "mn": "Language-specific guidance:\n- Use standard Mongolian consistently.\n- Use Mongolian Cyrillic as the primary writing system and preserve its standard orthography.\n- Pay close attention to vowel harmony and case suffixes.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "is": "Language-specific guidance:\n- Use standard Icelandic consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Icelandic diacritics and inflection.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ga": "Language-specific guidance:\n- Use standard Irish consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Irish orthography and mutation patterns where relevant.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "cy": "Language-specific guidance:\n- Use standard Welsh consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Welsh orthography and mutation patterns where relevant.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "az": "Language-specific guidance:\n- Use standard Azerbaijani consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Azerbaijani diacritics and do not substitute Turkish forms.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "kk": "Language-specific guidance:\n- Use standard Kazakh consistently.\n- Use Cyrillic as the primary writing system and preserve its standard orthography.\n- Preserve Kazakh-specific vocabulary and agglutinative morphology; do not substitute Russian forms.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "uz": "Language-specific guidance:\n- Use standard Uzbek consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Uzbek orthography and standard vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "sq": "Language-specific guidance:\n- Use standard Albanian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Albanian diacritics and standard vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "eu": "Language-specific guidance:\n- Use standard Basque consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Basque morphology and standard vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "gl": "Language-specific guidance:\n- Use standard Galician consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Galician diacritics and standard vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "mt": "Language-specific guidance:\n- Use standard Maltese consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Maltese diacritics and Semitic morphology.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "af": "Language-specific guidance:\n- Use standard Afrikaans consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Afrikaans spelling and word order.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "eo": "Language-specific guidance:\n- Use standard Esperanto consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Esperanto orthography and regular affix morphology.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "lb": "Language-specific guidance:\n- Use standard Luxembourgish consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Luxembourgish spelling and standard vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "gd": "Language-specific guidance:\n- Use standard Scottish Gaelic consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Gaelic spelling and mutation patterns where relevant.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "yo": "Language-specific guidance:\n- Use standard Yoruba consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve tone-marked Yoruba orthography where provided.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ha": "Language-specific guidance:\n- Use standard Hausa consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve standard Hausa orthography and tone information when provided.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "so": "Language-specific guidance:\n- Use standard Somali consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Somali orthography and agreement.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "zu": "Language-specific guidance:\n- Use standard Zulu consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve standard Zulu orthography and noun-class agreement.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "xh": "Language-specific guidance:\n- Use standard Xhosa consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve standard Xhosa orthography and noun-class agreement.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "rw": "Language-specific guidance:\n- Use standard Kinyarwanda consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve standard Kinyarwanda noun-class agreement.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ig": "Language-specific guidance:\n- Use standard Igbo consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve standard Igbo orthography and tone marks when provided.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "mg": "Language-specific guidance:\n- Use standard Malagasy consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Malagasy vocabulary and word order.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ny": "Language-specific guidance:\n- Use standard Chichewa consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve standard Chichewa orthography and noun-class agreement.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "sn": "Language-specific guidance:\n- Use standard Shona consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Shona orthography and noun-class agreement.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "st": "Language-specific guidance:\n- Use standard Southern Sotho consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve standard Sesotho noun-class agreement.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "fy": "Language-specific guidance:\n- Use standard Western Frisian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Western Frisian orthography and vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "co": "Language-specific guidance:\n- Use standard Corsican consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Corsican orthography and vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "fil": "Language-specific guidance:\n- Use standard Filipino consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Filipino vocabulary and natural word order.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "bs": "Language-specific guidance:\n- Use standard Bosnian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Bosnian diacritics and standard vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "tk": "Language-specific guidance:\n- Use standard Turkmen consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Turkmen diacritics and agglutinative morphology.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "jv": "Language-specific guidance:\n- Use standard Javanese consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Javanese vocabulary and register.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "as": "Language-specific guidance:\n- Use standard Assamese consistently.\n- Use Assamese as the primary writing system and preserve its standard orthography.\n- Preserve Assamese vocabulary rather than substituting Bengali forms.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ay": "Language-specific guidance:\n- Use standard Aymara consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Aymara morphology and vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "be": "Language-specific guidance:\n- Use standard Belarusian consistently.\n- Use Cyrillic as the primary writing system and preserve its standard orthography.\n- Preserve Belarusian orthography; do not substitute Russian vocabulary or grammar.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ca": "Language-specific guidance:\n- Use standard Catalan consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Catalan diacritics and standard vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "ee": "Language-specific guidance:\n- Use standard Ewe consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Ewe orthography and tone information when provided.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "fj": "Language-specific guidance:\n- Use standard Fijian consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Fijian vocabulary and natural word order.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "gn": "Language-specific guidance:\n- Use standard Guarani consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Preserve Guarani diacritics and standard vocabulary.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "or": "Language-specific guidance:\n- Use standard Odia consistently.\n- Use Odia as the primary writing system and preserve its standard orthography.\n- Use Odia script and standard Odia spelling and grammar.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "tg": "Language-specific guidance:\n- Use standard Tajik consistently.\n- Use Cyrillic as the primary writing system and preserve its standard orthography.\n- Preserve Tajik vocabulary and Cyrillic orthography.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "su": "Language-specific guidance:\n- Use standard Sundanese consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Sundanese vocabulary and register.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "suq": "Language-specific guidance:\n- Use standard Suri consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use the project's Suri curriculum conventions; do not infer regional variants without explicit source content.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
    "to": "Language-specific guidance:\n- Use standard Tongan consistently.\n- Use Latin as the primary writing system and preserve its standard orthography.\n- Use standard Tongan vocabulary and natural word order.\n- Pay close attention to grammatical agreement, inflection, natural word order, and learner-appropriate register.",
}


# Locale aliases for prompt overlays. Foundation languages use their ISO base
# code directly, while locale-specific core languages resolve to their
# canonical regional variant.
_LANGUAGE_PROMPT_OVERLAY_ALIASES: dict[str, str] = {
    "en": "en-GB",
    "de": "de-DE",
    "es": "es-ES",
    "fr": "fr-FR",
    "it": "it-IT",
    "pt": "pt-PT",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "zh": "zh-CN",
    "tr": "tr-TR",
    "ru": "ru-RU",
    "nl": "nl-NL",
    "pl": "pl-PL",
    "sv": "sv-SE",
    "da": "da-DK",
    "no": "no-NO",
    "fi": "fi-FI",
    "cs": "cs-CZ",
    "el": "el",
}


def get_language_prompt_overlay(target_language: str) -> str:
    """Return language-specific prompt guidance for a BCP-47-ish locale.

    Core locales use curated overlays above. Foundation languages receive a
    deterministic metadata-aware overlay so they never silently lose
    language-specific generation constraints.
    """
    locale = (target_language or "").strip().replace("_", "-") or "en-GB"
    base_language = locale.split("-")[0].lower()
    canonical_language = _LANGUAGE_PROMPT_OVERLAY_ALIASES.get(locale, locale)
    if canonical_language not in _LANGUAGE_PROMPT_OVERLAYS:
        canonical_language = _LANGUAGE_PROMPT_OVERLAY_ALIASES.get(
            base_language, base_language
        )
    curated = _LANGUAGE_PROMPT_OVERLAYS.get(canonical_language)
    if curated:
        return curated

    from app.services.language_helpers import (
        get_comprehension_length_guidance,
        get_language_name,
        get_language_script,
        get_reading_length_unit,
        uses_word_spacing,
    )

    language_name = get_language_name(locale)
    script = get_language_script(locale)
    spacing = "word spacing is expected" if uses_word_spacing(locale) else "word boundaries may not be represented by spaces"
    length_unit = get_reading_length_unit(locale)
    length_guidance = get_comprehension_length_guidance(locale)

    return (
        "Language-specific guidance:\n"
        f"- Generate the target language as {language_name}; do not substitute English or another language.\n"
        f"- Preserve the target writing system ({script}) and its native orthography; do not transliterate unless explicitly requested.\n"
        f"- Treat {spacing}; use native tokenisation and punctuation conventions.\n"
        f"- For reading-length decisions, measure in {length_unit}; {length_guidance}.\n"
        "- Keep grammar, vocabulary, register, and examples natural for the target language and CEFR level.\n"
        "- Do not invent language-specific rules when the supplied curriculum or exercise context does not establish them."
    )


MEMORY_SYSTEM_INSTRUCTION_BASE = """
Memory capability: use the save_user_memory tool when you genuinely learn a new,
durable fact about the student that would help personalise future interactions,
such as personal details, preferences, tastes, hobbies, profession, plans, goals,
learning style, or motivations. Most replies should not call the tool. Never save
temporary details, uncertain inferences, conversation summaries, or instructions.
Do not save facts already present in the supplied memories. Write each memory as
a concise, self-contained fact in the student's native language ({native_language_name})
so the student can review it in Settings. Continue the visible response after the tool result and never
claim the memory was saved when the tool reports an error.
"""


def get_memory_system_instruction(native_language_name: str) -> str:
    """Return the shared native memory-tool policy."""
    return MEMORY_SYSTEM_INSTRUCTION_BASE.format(native_language_name=native_language_name)
