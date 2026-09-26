"""Helpers for BCP-47 target_language codes.

Used by service layer to translate the generic target_language field into
human-readable names, self-names, and ISO 639-1 codes.
"""

from __future__ import annotations

from datetime import UTC, datetime

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
    # that stores only ISO 639-1 language codes.
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

_VOICE_SESSION_TITLES: dict[str, str] = {
    "es": "Sesión de voz",
    "fr": "Session vocale",
    "pt": "Sessão de voz",
    "de": "Sprachsitzung",
    "it": "Sessione vocale",
    "pl": "Sesja głosowa",
    "nl": "Spraaksessie",
    "ro": "Sesiune vocală",
    "ru": "Голосовая сессия",
    "no": "Taleøkt",
}

_NATIVE_LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "pt": "Portuguese",
    "de": "German",
    "it": "Italian",
    "pl": "Polish",
    "nl": "Dutch",
    "ro": "Romanian",
    "ru": "Russian",
    "no": "Norwegian",
}

def _normalize_locale(target_language: str) -> str:
    """Normalize BCP-47-ish locale spellings used by clients and profiles."""
    return (target_language or "").strip().replace("_", "-") or "en-GB"


def _resolve_language_info(target_language: str) -> dict[str, str] | None:
    locale = _normalize_locale(target_language)
    info = _LANGUAGE_INFO.get(locale)
    if info:
        return info
    base = locale.split("-")[0]
    direct = _LANGUAGE_INFO.get(base)
    if direct:
        return direct
    aliases = {
        "en": "en-GB", "de": "de-DE", "es": "es-ES", "fr": "fr-FR",
        "it": "it-IT", "pt": "pt-PT", "ja": "ja-JP", "ko": "ko-KR",
        "zh": "zh-CN", "ru": "ru-RU", "nl": "nl-NL", "pl": "pl-PL",
        "da": "da-DK", "sv": "sv-SE", "no": "no-NO", "fi": "fi-FI",
        "cs": "cs-CZ", "el": "el-GR",
    }
    return _LANGUAGE_INFO.get(aliases.get(base, ""))


_MONTH_NAMES: dict[str, list[str]] = {
    "es": [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ],
    "fr": [
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "août",
        "septembre",
        "octobre",
        "novembre",
        "décembre",
    ],
    "pt": [
        "janeiro",
        "fevereiro",
        "março",
        "abril",
        "maio",
        "junho",
        "julho",
        "agosto",
        "setembro",
        "outubro",
        "novembro",
        "dezembro",
    ],
    "de": [
        "Januar",
        "Februar",
        "März",
        "April",
        "Mai",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "Dezember",
    ],
    "it": [
        "gennaio",
        "febbraio",
        "marzo",
        "aprile",
        "maggio",
        "giugno",
        "luglio",
        "agosto",
        "settembre",
        "ottobre",
        "novembre",
        "dicembre",
    ],
    "pl": [
        "stycznia",
        "lutego",
        "marca",
        "kwietnia",
        "maja",
        "czerwca",
        "lipca",
        "sierpnia",
        "września",
        "października",
        "listopada",
        "grudnia",
    ],
    "nl": [
        "januari",
        "februari",
        "maart",
        "april",
        "mei",
        "juni",
        "juli",
        "augustus",
        "september",
        "oktober",
        "november",
        "december",
    ],
    "ro": [
        "ianuarie",
        "februarie",
        "martie",
        "aprilie",
        "mai",
        "iunie",
        "iulie",
        "august",
        "septembrie",
        "octombrie",
        "noiembrie",
        "decembrie",
    ],
    "ru": [
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        "ноября",
        "декабря",
    ],
}


def get_language_name(target_language: str) -> str:
    """'it-IT' → 'Italian', 'en-US' → 'English (US)'"""
    info = _resolve_language_info(target_language)
    return info["name"] if info else target_language


def get_language_self_name(target_language: str) -> str:
    """'it-IT' → 'Italiano', 'es-ES' → 'Español'"""
    info = _resolve_language_info(target_language)
    return info["self_name"] if info else target_language


def get_iso639(target_language: str) -> str:
    """'en-US' → 'en', 'it-IT' → 'it'"""
    info = _resolve_language_info(target_language)
    return info["iso639"] if info else _normalize_locale(target_language).split("-")[0].lower()


def get_language_flag(target_language: str) -> str:
    """Flags are intentionally disabled; kept only as a compatibility accessor."""
    return ""


def _get_language_capability(target_language: str) -> dict[str, str | bool]:
    locale = _normalize_locale(target_language)
    canonical_language = _LANGUAGE_CAPABILITY_ALIASES.get(locale, locale)

    # Prefer an explicit locale entry, then the language-base entry, before
    # falling back to an alias or English. This keeps foundation locale
    # variants such as ``hr-HR`` and ``tr-TR`` on their own capabilities.
    if canonical_language not in _LANGUAGE_CAPABILITIES:
        base_language = locale.split("-")[0].lower()
        canonical_language = _LANGUAGE_CAPABILITY_ALIASES.get(
            base_language,
            base_language,
        )

    return _LANGUAGE_CAPABILITIES.get(
        canonical_language,
        _LANGUAGE_CAPABILITIES["en-GB"],
    )

def get_language_script(target_language: str) -> str:
    """Return the primary writing-system metadata for a target language."""
    return str(_get_language_capability(target_language)["script"])


def get_language_romanization(target_language: str) -> str:
    """Return the romanization system used as learner support, or an empty string."""
    return str(_get_language_capability(target_language)["romanization"])


def uses_word_spacing(target_language: str) -> bool:
    """Return whether ordinary text uses visible spaces between words."""
    return bool(_get_language_capability(target_language)["uses_word_spacing"])


def get_reading_length_unit(target_language: str) -> str:
    """Return the best length unit for generated reading/listening prompts."""
    return str(_get_language_capability(target_language)["reading_length_unit"])


def get_comprehension_length_guidance(target_language: str, base_word_count: int) -> str:
    """Return language-aware length guidance for generated comprehension content."""
    unit = get_reading_length_unit(target_language)
    if unit == "characters":
        return f"{base_word_count * 2}–{base_word_count * 3} characters"
    return f"{base_word_count} words"


def get_native_language_name(native_language: str) -> str:
    """Return a human-readable name for native language codes used by user profiles."""
    return _NATIVE_LANGUAGE_NAMES.get(native_language, native_language)


def voice_session_title(native_language: str) -> str:
    """Return a localized 'Voice session - date' title for a conversation.

    Falls back to English if the native language is not supported.
    """
    label = _VOICE_SESSION_TITLES.get(native_language, "Voice session")
    now = datetime.now(UTC).replace(tzinfo=None)
    months = _MONTH_NAMES.get(native_language)
    if months:
        month_name = months[now.month - 1]
        if native_language in ("es", "pt"):
            return f"{label} — {now.day} de {month_name} de {now.year}"
        return f"{label} — {now.day} {month_name} {now.year}"
    return f"{label} — {now.strftime('%B %d, %Y')}"
