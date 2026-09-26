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
}


    "ro": "Language-specific guidance:\n- Use standard Romanian consistently and preserve Romanian diacritics (ă, â, î, ș, ț).\n- Pay close attention to gender, articles, case remnants, verb conjugation, and natural Romanian word order.",
    "hu": "Language-specific guidance:\n- Use standard Hungarian consistently and preserve Hungarian diacritics.\n- Pay close attention to vowel harmony, case suffixes, definite/indefinite conjugation, and natural word order.",
    "uk": "Language-specific guidance:\n- Use standard Ukrainian consistently and use Cyrillic as the primary script.\n- Preserve Ukrainian spelling and diacritics; pay close attention to case, gender, aspect, and natural word order.",
    "bg": "Language-specific guidance:\n- Use standard Bulgarian consistently and use Cyrillic as the primary script.\n- Pay close attention to definite articles, gender, verb aspect, and natural word order.",
    "sr": "Language-specific guidance:\n- Use standard Serbian consistently and use Cyrillic as the primary script unless Latin is explicitly requested.\n- Pay close attention to case, gender, aspect, and agreement.",
    "hr": "Language-specific guidance:\n- Use standard Croatian consistently and preserve Croatian diacritics.\n- Pay close attention to case, gender, aspect, and standard Croatian vocabulary.",
    "sk": "Language-specific guidance:\n- Use standard Slovak consistently and preserve Slovak diacritics.\n- Pay close attention to case, gender, aspect, and declension.",
    "sl": "Language-specific guidance:\n- Use standard Slovenian consistently and preserve Slovenian diacritics.\n- Pay close attention to dual forms, case, gender, and agreement.",
    "lt": "Language-specific guidance:\n- Use standard Lithuanian consistently and preserve Lithuanian diacritics.\n- Pay close attention to case, gender, declension, and natural word order.",
    "lv": "Language-specific guidance:\n- Use standard Latvian consistently and preserve Latvian diacritics.\n- Pay close attention to case, gender, declension, and verb forms.",
    "et": "Language-specific guidance:\n- Use standard Estonian consistently and preserve Estonian diacritics.\n- Pay close attention to case forms, consonant gradation, and natural word order.",
    "el": "Language-specific guidance:\n- Use standard Greek consistently and use Greek script as the primary writing system.\n- Pay close attention to gender, case, articles, verb aspect, and accents.",
    "ka": "Language-specific guidance:\n- Use standard Georgian consistently and use Georgian script as the primary writing system.\n- Preserve Georgian spelling and focus on case markers, verb morphology, and natural word order.",
    "hy": "Language-specific guidance:\n- Use standard Eastern Armenian consistently and use Armenian script as the primary writing system.\n- Preserve Armenian spelling and focus on case, agreement, and verb forms.",
    "am": "Language-specific guidance:\n- Use standard Amharic consistently and use Ethiopic (Ge'ez) script as the primary writing system.\n- Pay close attention to verb morphology, gender, agreement, and natural phrasing.",
    "ti": "Language-specific guidance:\n- Use standard Tigrinya consistently and use Ethiopic (Ge'ez) script as the primary writing system.\n- Pay close attention to verb morphology, gender, agreement, and natural phrasing.",
    "bn": "Language-specific guidance:\n- Use standard Bengali consistently and use Bengali script as the primary writing system.\n- Pay close attention to postpositions, honorifics, verb forms, and natural Bengali phrasing.",
    "ta": "Language-specific guidance:\n- Use standard Tamil consistently and use Tamil script as the primary writing system.\n- Pay close attention to case markers, honorifics, verb forms, and formal versus spoken register.",
    "te": "Language-specific guidance:\n- Use standard Telugu consistently and use Telugu script as the primary writing system.\n- Pay close attention to case markers, verb forms, agreement, and natural word order.",
    "gu": "Language-specific guidance:\n- Use standard Gujarati consistently and use Gujarati script as the primary writing system.\n- Pay close attention to postpositions, gender, agreement, and verb forms.",
    "ur": "Language-specific guidance:\n- Use standard Urdu consistently and use Urdu Nastaliq/Arabic-derived script as the primary writing system.\n- Preserve right-to-left text and pay close attention to gender, agreement, and formal register.",
    "lo": "Language-specific guidance:\n- Use standard Lao consistently and use Lao script as the primary writing system.\n- Do not insert English-style spaces between every Lao word; preserve natural Lao phrasing and tone-sensitive spelling.",
    "dz": "Language-specific guidance:\n- Use standard Dzongkha consistently and use Tibetan-derived script as the primary writing system.\n- Use romanization only as learner support when explicitly requested.",
    "bo": "Language-specific guidance:\n- Use standard Tibetan consistently and use Tibetan script as the primary writing system.\n- Use Wylie or another romanization only as learner support when explicitly requested.",
    "mn": "Language-specific guidance:\n- Use standard Mongolian consistently and use Mongolian Cyrillic as the primary script.\n- Pay close attention to vowel harmony, case suffixes, and natural word order.",
\n_LANGUAGE_PROMPT_OVERLAY_ALIASES: dict[str, str] = {
    "de": "de-DE",
    "fr": "fr-FR",
    "es": "es-ES",
    "it": "it-IT",
    "pt": "pt-PT",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "zh": "zh-CN",
    "tr": "tr-TR",
    "ar": "ar",
    "ru": "ru-RU",
    "nl": "nl-NL",
    "pl": "pl-PL",
    "sv": "sv-SE",
    "da": "da-DK",
    "no": "no-NO",
    "fi": "fi-FI",
    "cs": "cs-CZ",
    "hi": "hi",
    "fa": "fa",
    "he": "he",
    "th": "th",

    "ro": "ro",
    "hu": "hu",
    "uk": "uk",
    "bg": "bg",
    "sr": "sr",
    "hr": "hr",
    "sk": "sk",
    "sl": "sl",
    "lt": "lt",
    "lv": "lv",
    "et": "et",
    "el": "el-GR",
    "ka": "ka",
    "hy": "hy",
    "am": "am",
    "ti": "ti",
    "bn": "bn",
    "ta": "ta",
    "te": "te",
    "gu": "gu",
    "ur": "ur",
    "lo": "lo",
    "dz": "dz",
    "bo": "bo",
    "mn": "mn",
}


def get_language_prompt_overlay(target_language: str) -> str:
    """Return concise language/variant guidance for prompt composition."""
    locale = (target_language or "").strip().replace("_", "-")
    canonical_language = _LANGUAGE_PROMPT_OVERLAY_ALIASES.get(locale, locale)
    if canonical_language not in _LANGUAGE_PROMPT_OVERLAYS:
        canonical_language = _LANGUAGE_PROMPT_OVERLAY_ALIASES.get(locale.split("-")[0], locale)
    return _LANGUAGE_PROMPT_OVERLAYS.get(canonical_language, "")


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
