"""Canonical BCP-47 locale resolution and language metadata.

This module is the single source of truth for locale normalization, canonical
language resolution, writing-system metadata, spacing, and reading-length
semantics shared by curriculum and prompt generation.
"""

from __future__ import annotations

from dataclasses import dataclass

_LANGUAGE_INFO: dict[str, dict[str, str]] = {
    "en-US": {
        "name": "English (US)",
        "self_name": "English (US)",
        "iso639": "en",
    },
    "en-GB": {
        "name": "English (UK)",
        "self_name": "English (UK)",
        "iso639": "en",
    },
    "de-DE": {"name": "German", "self_name": "Deutsch", "iso639": "de"},
    "es-ES": {
        "name": "Spanish (Spain)",
        "self_name": "Español (España)",
        "iso639": "es",
    },
    "fr-FR": {"name": "French", "self_name": "Français", "iso639": "fr"},
    "it-IT": {"name": "Italian", "self_name": "Italiano", "iso639": "it"},
    "pt-PT": {
        "name": "European Portuguese",
        "self_name": "Português (Portugal)",
        "iso639": "pt",
    },
    "pt-BR": {
        "name": "Brazilian Portuguese",
        "self_name": "Português (Brasil)",
        "iso639": "pt",
    },
    "ja-JP": {"name": "Japanese", "self_name": "日本語", "iso639": "ja"},
    "ko-KR": {
        "name": "Korean (South Korea)",
        "self_name": "한국어",
        "iso639": "ko",
    },
    "zh-CN": {
        "name": "Chinese (Mainland China)",
        "self_name": "中文（中国）",
        "iso639": "zh",
    },
    "ru-RU": {
        "name": "Russian",
        "self_name": "Русский",
        "iso639": "ru",
    },
    "nl-NL": {
        "name": "Dutch",
        "self_name": "Nederlands",
        "iso639": "nl",
    },
    "pl-PL": {
        "name": "Polish",
        "self_name": "Polski",
        "iso639": "pl",
    },
    "da-DK": {
        "name": "Danish",
        "self_name": "Dansk",
        "iso639": "da",
    },
    "sv-SE": {
        "name": "Swedish",
        "self_name": "Svenska",
        "iso639": "sv",
    },
    "no-NO": {
        "name": "Norwegian",
        "self_name": "Norsk",
        "iso639": "no",
    },
    "fi-FI": {
        "name": "Finnish",
        "self_name": "Suomi",
        "iso639": "fi",
    },
    "cs-CZ": {
        "name": "Czech",
        "self_name": "Čeština",
        "iso639": "cs",
    },
    "el-GR": {
        "name": "Greek",
        "self_name": "Ελληνικά",
        "iso639": "el",
    },
    "ar": {"name": "Arabic", "self_name": "العربية", "iso639": "ar"},
    "tr": {"name": "Turkish", "self_name": "Türkçe", "iso639": "tr"},
    "ro": {"name": "Romanian", "self_name": "Română", "iso639": "ro"},
    "hu": {"name": "Hungarian", "self_name": "Magyar", "iso639": "hu"},
    "uk": {"name": "Ukrainian", "self_name": "Українська", "iso639": "uk"},
    "he": {"name": "Hebrew", "self_name": "עברית", "iso639": "he"},
    "vi": {"name": "Vietnamese", "self_name": "Tiếng Việt", "iso639": "vi"},
    "mr": {"name": "Marathi", "self_name": "मराठी", "iso639": "mr"},
    "bg": {"name": "Bulgarian", "self_name": "Български", "iso639": "bg"},
    "sr": {"name": "Serbian", "self_name": "Српски", "iso639": "sr"},
    "fa": {"name": "Persian", "self_name": "فارسی", "iso639": "fa"},
    "ur": {"name": "Urdu", "self_name": "اردو", "iso639": "ur"},
    "hi": {"name": "Hindi", "self_name": "हिन्दी", "iso639": "hi"},
    "bn": {"name": "Bengali", "self_name": "বাংলা", "iso639": "bn"},
    "ta": {"name": "Tamil", "self_name": "தமிழ்", "iso639": "ta"},
    "te": {"name": "Telugu", "self_name": "తెలుగు", "iso639": "te"},
    "gu": {"name": "Gujarati", "self_name": "ગુજરાતી", "iso639": "gu"},
    "th": {"name": "Thai", "self_name": "ไทย", "iso639": "th"},
    "ka": {"name": "Georgian", "self_name": "ქართული", "iso639": "ka"},
    "hy": {"name": "Armenian", "self_name": "Հայերեն", "iso639": "hy"},
    "am": {"name": "Amharic", "self_name": "አማርኛ", "iso639": "am"},
    "ti": {"name": "Tigrinya", "self_name": "ትግርኛ", "iso639": "ti"},
    "zh-TW": {"name": "Chinese (Traditional)", "self_name": "中文（繁體）", "iso639": "zh"},
    "zh-Hant": {"name": "Traditional Chinese", "self_name": "繁體中文", "iso639": "zh"},
    "zh-Hant-TW": {"name": "Chinese (Traditional, Taiwan)", "self_name": "臺灣繁體中文", "iso639": "zh"},
    "zh-Hant-HK": {"name": "Traditional Chinese", "self_name": "繁體中文", "iso639": "zh"},
    "zh-HK": {"name": "Traditional Chinese (Hong Kong)", "self_name": "繁體中文（香港）", "iso639": "zh"},
    "zh-MO": {"name": "Traditional Chinese (Macau)", "self_name": "繁體中文（澳門）", "iso639": "zh"},
    "hr": {"name": "Croatian", "self_name": "Hrvatski", "iso639": "hr"},
    "sk": {"name": "Slovak", "self_name": "Slovenčina", "iso639": "sk"},
    "sl": {"name": "Slovenian", "self_name": "Slovenščina", "iso639": "sl"},
    "lt": {"name": "Lithuanian", "self_name": "Lietuvių", "iso639": "lt"},
    "lv": {"name": "Latvian", "self_name": "Latviešu", "iso639": "lv"},
    "is": {"name": "Icelandic", "self_name": "Íslenska", "iso639": "is"},
    "ga": {"name": "Irish", "self_name": "Gaeilge", "iso639": "ga"},
    "cy": {"name": "Welsh", "self_name": "Cymraeg", "iso639": "cy"},
    "az": {"name": "Azerbaijani", "self_name": "Azərbaycanca", "iso639": "az"},
    "kk": {"name": "Kazakh", "self_name": "Қазақша", "iso639": "kk"},
    "uz": {"name": "Uzbek", "self_name": "Oʻzbekcha", "iso639": "uz"},
    "sq": {"name": "Albanian", "self_name": "Shqip", "iso639": "sq"},
    "eu": {"name": "Basque", "self_name": "Euskara", "iso639": "eu"},
    "gl": {"name": "Galician", "self_name": "Galego", "iso639": "gl"},
    "mt": {"name": "Maltese", "self_name": "Malti", "iso639": "mt"},
    "af": {"name": "Afrikaans", "self_name": "Afrikaans", "iso639": "af"},
    "eo": {"name": "Esperanto", "self_name": "Esperanto", "iso639": "eo"},
    "lb": {"name": "Luxembourgish", "self_name": "Lëtzebuergesch", "iso639": "lb"},
    "gd": {"name": "Scottish Gaelic", "self_name": "Gàidhlig", "iso639": "gd"},
    "yo": {"name": "Yoruba", "self_name": "Yorùbá", "iso639": "yo"},
    "ha": {"name": "Hausa", "self_name": "Hausa", "iso639": "ha"},
    "so": {"name": "Somali", "self_name": "Soomaali", "iso639": "so"},
    "zu": {"name": "Zulu", "self_name": "isiZulu", "iso639": "zu"},
    "xh": {"name": "Xhosa", "self_name": "isiXhosa", "iso639": "xh"},
    "rw": {"name": "Kinyarwanda", "self_name": "Ikinyarwanda", "iso639": "rw"},
    "ig": {"name": "Igbo", "self_name": "Igbo", "iso639": "ig"},
    "mg": {"name": "Malagasy", "self_name": "Malagasy", "iso639": "mg"},
    "ny": {"name": "Chichewa", "self_name": "Chichewa", "iso639": "ny"},
    "sn": {"name": "Shona", "self_name": "ChiShona", "iso639": "sn"},
    "st": {"name": "Southern Sotho", "self_name": "Sesotho", "iso639": "st"},
    "fy": {"name": "Western Frisian", "self_name": "Frysk", "iso639": "fy"},
    "co": {"name": "Corsican", "self_name": "Corsu", "iso639": "co"},
    "fil": {"name": "Filipino", "self_name": "Filipino", "iso639": "fil"},
    "bs": {"name": "Bosnian", "self_name": "Bosanski", "iso639": "bs"},
    "tk": {"name": "Turkmen", "self_name": "Türkmençe", "iso639": "tk"},
    "mn": {"name": "Mongolian", "self_name": "Монгол", "iso639": "mn"},
    "ku": {"name": "Kurdish", "self_name": "Kurdî", "iso639": "ku"},
    "lo": {"name": "Lao", "self_name": "ລາວ", "iso639": "lo"},
    "jv": {"name": "Javanese", "self_name": "Basa Jawa", "iso639": "jv"},
    "as": {"name": "Assamese", "self_name": "অসমীয়া", "iso639": "as"},
    "ay": {"name": "Aymara", "self_name": "Aymar aru", "iso639": "ay"},
    "be": {"name": "Belarusian", "self_name": "Беларуская", "iso639": "be"},
    "bo": {"name": "Tibetan", "self_name": "བོད་སྐད", "iso639": "bo"},
    "ca": {"name": "Catalan", "self_name": "Català", "iso639": "ca"},
    "ee": {"name": "Ewe", "self_name": "Eʋegbe", "iso639": "ee"},
    "dz": {"name": "Dzongkha", "self_name": "རྫོང་ཁ", "iso639": "dz"},
    "et": {"name": "Estonian", "self_name": "Eesti", "iso639": "et"},
    "fj": {"name": "Fijian", "self_name": "Na Vosa Vakaviti", "iso639": "fj"},
    "gn": {"name": "Guarani", "self_name": "Avañe’ẽ", "iso639": "gn"},
    "or": {"name": "Odia", "self_name": "ଓଡ଼ିଆ", "iso639": "or"},
    "tg": {"name": "Tajik", "self_name": "Тоҷикӣ", "iso639": "tg"},
    "su": {"name": "Sundanese", "self_name": "Basa Sunda", "iso639": "su"},
    "suq": {"name": "Suri", "self_name": "Suri", "iso639": "suq"},
    "to": {"name": "Tongan", "self_name": "Lea fakatonga", "iso639": "to"},
}

_LANGUAGE_CAPABILITIES: dict[str, dict[str, str | bool]] = {
    "sv-SE": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "tr": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "en-US": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "en-GB": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "de-DE": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "es-ES": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "fr-FR": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "it-IT": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "pt-PT": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "ja-JP": {
        "script": "hiragana-katakana-kanji",
        "romanization": "romaji",
        "uses_word_spacing": False,
        "reading_length_unit": "characters",
    },
    "ko-KR": {
        "script": "hangul",
        "romanization": "revised-romanization",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "zh-CN": {
        "script": "simplified-hanzi",
        "romanization": "pinyin",
        "uses_word_spacing": False,
        "reading_length_unit": "characters",
    },
    "zh-TW": {
        "script": "traditional-hanzi",
        "romanization": "pinyin",
        "uses_word_spacing": False,
        "reading_length_unit": "characters",
    },
    "ru-RU": {
        "script": "cyrillic",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "nl-NL": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "pl-PL": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "da-DK": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "el-GR": {
        "script": "greek",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "no-NO": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "fi-FI": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "cs-CZ": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "ar": {"script": "arabic", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "fa": {"script": "arabic-persian", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ur": {"script": "arabic", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "he": {"script": "hebrew", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "hi": {"script": "devanagari", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "bn": {"script": "bengali", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ta": {"script": "tamil", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "te": {"script": "telugu", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "gu": {"script": "gujarati", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "th": {"script": "thai", "romanization": "", "uses_word_spacing": False, "reading_length_unit": "characters"},
    "uk": {"script": "cyrillic", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "bg": {"script": "cyrillic", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "sr": {"script": "cyrillic", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ka": {"script": "georgian", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "hy": {"script": "armenian", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "am": {"script": "geez", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ti": {"script": "geez", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "vi": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},

    # Foundation-language defaults. These entries keep generation from silently
    # falling back to English-script assumptions when a foundation is selected.
    "ro": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "hu": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "hr": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "mr": {"script": "devanagari", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ku": {"script": "latin-arabic", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "jv": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "to": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "sk": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "sl": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "lt": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "lv": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "is": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ga": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "cy": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "az": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "kk": {"script": "cyrillic", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "uz": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "sq": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "eu": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "gl": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "mt": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "af": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "eo": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "lb": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "gd": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "yo": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ha": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "so": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "zu": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "xh": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "rw": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ig": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "mg": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ny": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "sn": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "st": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "fy": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "co": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "fil": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "bs": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "tk": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "mn": {"script": "cyrillic", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "lo": {"script": "lao", "romanization": "", "uses_word_spacing": False, "reading_length_unit": "characters"},
    "as": {"script": "assamese", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ay": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "be": {"script": "cyrillic", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "bo": {"script": "tibetan", "romanization": "wylie", "uses_word_spacing": False, "reading_length_unit": "characters"},
    "ca": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ee": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "dz": {"script": "tibetan", "romanization": "wylie", "uses_word_spacing": False, "reading_length_unit": "characters"},
    "et": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "fj": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "gn": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "or": {"script": "odia", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "tg": {"script": "cyrillic", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "su": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "ti": {"script": "geez", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
    "suq": {"script": "latin", "romanization": "", "uses_word_spacing": True, "reading_length_unit": "words"},
}

_LANGUAGE_CAPABILITY_ALIASES: dict[str, str] = {
    # Keep the bare English code on the same explicit capability path as the
    # regional variants; this avoids an unnecessary fallback for profile data
    # that stores only a base ISO 639 language code.
    "en": "en-GB",
    "de": "de-DE",
    "es": "es-ES",
    "fr": "fr-FR",
    "it": "it-IT",
    "pt": "pt-PT",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "zh": "zh-CN",
    "ru": "ru-RU",
    "nl": "nl-NL",
    "pl": "pl-PL",
    "da": "da-DK",
    "el": "el-GR",
    "sv": "sv-SE",
    "no": "no-NO",
    "fi": "fi-FI",
    "cs": "cs-CZ",
    "uk-UA": "uk",
    "bg-BG": "bg",
    "sr-RS": "sr",
    "zh-TW": "zh-TW",
    "zh-Hant": "zh-TW",
    "zh-Hant-TW": "zh-TW",
    "zh-Hant-HK": "zh-TW",
    "zh-HK": "zh-TW",
    "zh-MO": "zh-TW",
    "zh-Hans": "zh-CN",
    "pt-BR": "pt-BR",
    # Explicit foundation locale aliases keep profile/browser locales stable.
    "ro-RO": "ro", "hu-HU": "hu", "he-IL": "he", "vi-VN": "vi",
    "hr-HR": "hr", "sk-SK": "sk", "sl-SI": "sl", "lt-LT": "lt", "lv-LV": "lv",
    "is-IS": "is", "ga-IE": "ga", "cy-GB": "cy", "ka-GE": "ka", "hy-AM": "hy",
    "az-AZ": "az", "kk-KZ": "kk", "uz-UZ": "uz", "mr-IN": "mr", "gu-IN": "gu",
    "sq-AL": "sq", "eu-ES": "eu", "gl-ES": "gl", "mt-MT": "mt", "af-ZA": "af",
    "lb-LU": "lb", "gd-GB": "gd", "yo-NG": "yo", "ha-NG": "ha", "so-SO": "so",
    "zu-ZA": "zu", "xh-ZA": "xh", "rw-RW": "rw", "ig-NG": "ig", "mg-MG": "mg",
    "ny-MW": "ny", "sn-ZW": "sn", "st-LS": "st", "fy-NL": "fy", "co-FR": "co",
    "fil-PH": "fil", "bs-BA": "bs", "tk-TM": "tk", "bn-BD": "bn", "mn-MN": "mn",
    "ku-TR": "ku", "lo-LA": "lo", "jv-ID": "jv", "as-IN": "as", "ay-BO": "ay",
    "be-BY": "be", "bo-CN": "bo", "ca-ES": "ca", "ee-GH": "ee", "dz-BT": "dz",
    "et-EE": "et", "fj-FJ": "fj", "gn-PY": "gn", "or-IN": "or", "tg-TJ": "tg",
    "su-ID": "su", "ti-ER": "ti", "suq-ET": "suq", "to-TO": "to",
}

@dataclass(frozen=True)
class LocaleResolution:
    requested: str
    normalized: str
    base: str
    canonical: str
    metadata: dict[str, str]
    capability: dict[str, str | bool]


# Canonical locale aliases shared by all consumers. A canonical value is either
# a regional core locale (where content differs by region) or a foundation ISO
# code (where the curriculum is shared across regions).
_LOCALE_ALIASES: dict[str, str] = {
    "en": "en-GB", "en-GB": "en-GB", "en-US": "en-US",
    "de-DE": "de", "es-ES": "es", "fr-FR": "fr", "it-IT": "it",
    "pt-PT": "pt", "pt-BR": "pt-BR", "ja-JP": "ja", "ko-KR": "ko",
    "zh-CN": "zh", "zh-TW": "zh", "zh-Hant": "zh", "zh-Hant-TW": "zh",
    "zh-Hant-HK": "zh", "zh-HK": "zh", "zh-MO": "zh", "zh-Hans": "zh",
    "ar-DZ": "ar", "tr-TR": "tr", "ru-RU": "ru", "nl-NL": "nl",
    "pl-PL": "pl", "el-GR": "el", "sv-SE": "sv", "da-DK": "da",
    "no-NO": "no", "fi-FI": "fi", "cs-CZ": "cs", "uk-UA": "uk",
    "bg-BG": "bg", "sr-RS": "sr",
}

# Foundation languages resolve by base code, including all registered regional
# variants. Keep this set aligned with the available foundation curricula.
_FOUNDATION_CODES = frozenset({
    "ro", "hu", "uk", "he", "vi", "bg", "sr", "hr", "sk", "sl", "lt", "lv",
    "is", "ga", "cy", "ka", "hy", "az", "kk", "uz", "ur", "ta", "te", "mr",
    "gu", "sq", "eu", "gl", "mt", "af", "eo", "lb", "gd", "yo", "ha", "am",
    "so", "zu", "xh", "rw", "ig", "mg", "ny", "sn", "st", "fy", "co", "fa",
    "fil", "hi", "th", "bs", "tk", "bn", "mn", "ku", "lo", "jv", "as", "ay",
    "be", "bo", "ca", "ee", "dz", "et", "fj", "gn", "or", "tg", "su", "ti",
    "suq", "to",
})


def normalize_locale(value: str | None) -> str:
    raw = (value or "").strip().replace("_", "-") or "en-GB"
    parts = raw.split("-")
    normalized = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 4 and part.isalpha():
            normalized.append(part.title())
        elif (len(part) == 2 and part.isalpha()) or (len(part) == 3 and part.isdigit()):
            normalized.append(part.upper())
        else:
            normalized.append(part.lower())
    return "-".join(normalized)


def resolve_locale(value: str | None) -> LocaleResolution:
    normalized = normalize_locale(value)
    base = normalized.split("-")[0].lower()
    canonical = _LOCALE_ALIASES.get(normalized)
    if canonical is None and base in _FOUNDATION_CODES:
        canonical = base
    if canonical is None:
        canonical = base

    metadata = _LANGUAGE_INFO.get(normalized)
    if metadata is None:
        metadata = _LANGUAGE_INFO.get(base)
    if metadata is None:
        fallback_locale = _LOCALE_ALIASES.get(base, base)
        metadata = _LANGUAGE_INFO.get(fallback_locale)
    if metadata is None:
        metadata = {"name": value or "English (UK)", "self_name": value or "English (UK)", "iso639": base}

    capability_key = _LANGUAGE_CAPABILITY_ALIASES.get(normalized, normalized)
    if capability_key not in _LANGUAGE_CAPABILITIES:
        capability_key = _LANGUAGE_CAPABILITY_ALIASES.get(base, base)
    capability = _LANGUAGE_CAPABILITIES.get(capability_key, _LANGUAGE_CAPABILITIES["en-GB"])

    return LocaleResolution(
        requested=value or "en-GB",
        normalized=normalized,
        base=base,
        canonical=canonical,
        metadata=metadata,
        capability=capability,
    )


def get_locale_metadata(value: str | None) -> dict[str, str]:
    return resolve_locale(value).metadata


def get_locale_capability(value: str | None) -> dict[str, str | bool]:
    return resolve_locale(value).capability
