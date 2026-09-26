export interface TargetLanguage {
  code: string
  name: string
  nameEn: string
  iso639: string
  script: TargetLanguageScript
  fontClass: string
  usesWordSpacing: boolean
  romanization?: TargetLanguageRomanization
  flagPath: string
}

export type TargetLanguageScript =
  | 'latin'
  | 'cyrillic'
  | 'greek'
  | 'hiragana-katakana-kanji'
  | 'hangul'
  | 'simplified-hanzi'
  | 'arabic'
  | 'devanagari'

export type TargetLanguageRomanization =
  | 'romaji'
  | 'revised-romanization'
  | 'pinyin'

interface TargetLanguageCapability {
  script: TargetLanguageScript
  fontClass: string
  usesWordSpacing: boolean
  romanization?: TargetLanguageRomanization
}

const LATIN_LANGUAGE_CAPABILITY: TargetLanguageCapability = {
  script: 'latin',
  fontClass: 'font-target-latin',
  usesWordSpacing: true,
}

export const TARGET_LANGUAGE_CAPABILITIES: Record<
  string,
  TargetLanguageCapability
> = {
  'en-US': LATIN_LANGUAGE_CAPABILITY,
  'en-GB': LATIN_LANGUAGE_CAPABILITY,
  'es-ES': LATIN_LANGUAGE_CAPABILITY,
  'it-IT': LATIN_LANGUAGE_CAPABILITY,
  'pt-PT': LATIN_LANGUAGE_CAPABILITY,
  'fr-FR': LATIN_LANGUAGE_CAPABILITY,
  'de-DE': LATIN_LANGUAGE_CAPABILITY,
  'ja-JP': {
    script: 'hiragana-katakana-kanji',
    fontClass: 'font-target-ja',
    usesWordSpacing: false,
    romanization: 'romaji',
  },
  'ko-KR': {
    script: 'hangul',
    fontClass: 'font-target-ko',
    usesWordSpacing: true,
    romanization: 'revised-romanization',
  },
  'zh-CN': {
    script: 'simplified-hanzi',
    fontClass: 'font-target-zh',
    usesWordSpacing: false,
    romanization: 'pinyin',
  },
  ar: {
    script: 'arabic',
    fontClass: 'font-sans',
    usesWordSpacing: true,
  },
  'ru-RU': { script: 'cyrillic', fontClass: 'font-target-latin', usesWordSpacing: true },
  'nl-NL': LATIN_LANGUAGE_CAPABILITY,
  'pl-PL': LATIN_LANGUAGE_CAPABILITY,
  'da-DK': LATIN_LANGUAGE_CAPABILITY,
  'el-GR': { script: 'greek', fontClass: 'font-target-latin', usesWordSpacing: true },
  'sv-SE': LATIN_LANGUAGE_CAPABILITY,
  'no-NO': LATIN_LANGUAGE_CAPABILITY,
  'fi-FI': LATIN_LANGUAGE_CAPABILITY,
  'cs-CZ': LATIN_LANGUAGE_CAPABILITY,
  'fa-IR': {
    script: 'arabic',
    fontClass: 'font-sans',
    usesWordSpacing: true,
  },
  'hi-IN': {
    script: 'devanagari',
    fontClass: 'font-sans',
    usesWordSpacing: true,
  },
  'id-ID': LATIN_LANGUAGE_CAPABILITY,
  'ms-MY': LATIN_LANGUAGE_CAPABILITY,
  'tr-TR': LATIN_LANGUAGE_CAPABILITY,
}

const FLAG_PATHS: Record<string, string> = {
  'en-US': '/flags/usa.jpg', 'en-GB': '/flags/uk.jpg', 'es-ES': '/flags/spain.jpg',
  'it-IT': '/flags/italy.jpg', 'pt-PT': '/flags/portugal.jpg', 'fr-FR': '/flags/france.jpg',
  'de-DE': '/flags/germany.jpg', 'ja-JP': '/flags/japan.jpg', 'ko-KR': '/flags/south_korea.jpg',
  'zh-CN': '/flags/china.jpg', ar: '/flags/ar.svg',
}

const TARGET_LANGUAGE_ALIASES: Record<string, string> = {
  en: 'en-GB',
  'en-us': 'en-US',
  'en-gb': 'en-GB',
  es: 'es-ES',
  'es-es': 'es-ES',
  it: 'it-IT',
  'it-it': 'it-IT',
  pt: 'pt-PT',
  'pt-pt': 'pt-PT',
  fr: 'fr-FR',
  'fr-fr': 'fr-FR',
  de: 'de-DE',
  'de-de': 'de-DE',
  ja: 'ja-JP',
  'ja-jp': 'ja-JP',
  ko: 'ko-KR',
  'ko-kr': 'ko-KR',
  zh: 'zh-CN',
  'zh-cn': 'zh-CN',
  ru: 'ru-RU',
  'ru-ru': 'ru-RU',
  nl: 'nl-NL',
  'nl-nl': 'nl-NL',
  pl: 'pl-PL',
  'pl-pl': 'pl-PL',
  da: 'da-DK',
  'da-dk': 'da-DK',
  el: 'el-GR',
  'el-gr': 'el-GR',
  sv: 'sv-SE',
  'sv-se': 'sv-SE',
  no: 'no-NO',
  'no-no': 'no-NO',
  fi: 'fi-FI',
  'fi-fi': 'fi-FI',
  cs: 'cs-CZ',
  'cs-cz': 'cs-CZ',
  fa: 'fa-IR',
  'fa-ir': 'fa-IR',
  hi: 'hi-IN',
  'hi-in': 'hi-IN',
  id: 'id-ID',
  'id-id': 'id-ID',
  ms: 'ms-MY',
  'ms-my': 'ms-MY',
  tr: 'tr-TR',
  'tr-tr': 'tr-TR',
}

function withCapabilities(
  language: Omit<TargetLanguage, keyof TargetLanguageCapability | 'flagPath'>
): TargetLanguage {
  return {
    ...language,
    ...(TARGET_LANGUAGE_CAPABILITIES[language.code] ?? LATIN_LANGUAGE_CAPABILITY),
    flagPath: FLAG_PATHS[language.code] ?? '/flags/arab-league.svg',
  }
}

export const TARGET_LANGUAGE_CATALOG: TargetLanguage[] = [
  withCapabilities({
    code: 'en-US',
    name: 'English (US)',
    nameEn: 'English (US)',
    iso639: 'en',
  }),
  withCapabilities({
    code: 'en-GB',
    name: 'English (UK)',
    nameEn: 'English (UK)',
    iso639: 'en',
  }),
  withCapabilities({
    code: 'es-ES',
    name: 'Español',
    nameEn: 'Spanish',
    iso639: 'es',
  }),
  withCapabilities({
    code: 'it-IT',
    name: 'Italiano',
    nameEn: 'Italian',
    iso639: 'it',
  }),
  withCapabilities({
    code: 'pt-PT',
    name: 'Português',
    nameEn: 'Portuguese',
    iso639: 'pt',
  }),
  withCapabilities({
    code: 'fr-FR',
    name: 'Français',
    nameEn: 'French',
    iso639: 'fr',
  }),
  withCapabilities({
    code: 'de-DE',
    name: 'Deutsch',
    nameEn: 'German',
    iso639: 'de',
  }),
  withCapabilities({
    code: 'ja-JP',
    name: '日本語',
    nameEn: 'Japanese',
    iso639: 'ja',
  }),
  withCapabilities({
    code: 'ko-KR',
    name: '한국어',
    nameEn: 'Korean',
    iso639: 'ko',
  }),
  withCapabilities({
    code: 'zh-CN',
    name: '中文（中国）',
    nameEn: 'Chinese (Mainland China)',
    iso639: 'zh',
  }),
  withCapabilities({
    code: 'ar',
    name: 'العربية',
    nameEn: 'Arabic',
    iso639: 'ar',
  }),
  withCapabilities({ code: 'ru-RU', name: 'Русский', nameEn: 'Russian', iso639: 'ru' }),
  withCapabilities({ code: 'nl-NL', name: 'Nederlands', nameEn: 'Dutch', iso639: 'nl' }),
  withCapabilities({ code: 'pl-PL', name: 'Polski', nameEn: 'Polish', iso639: 'pl' }),
  withCapabilities({ code: 'da-DK', name: 'Dansk', nameEn: 'Danish', iso639: 'da' }),
  withCapabilities({ code: 'el-GR', name: 'Ελληνικά', nameEn: 'Greek', iso639: 'el' }),
  withCapabilities({ code: 'sv-SE', name: 'Svenska', nameEn: 'Swedish', iso639: 'sv' }),
  withCapabilities({ code: 'no-NO', name: 'Norsk', nameEn: 'Norwegian', iso639: 'no' }),
  withCapabilities({ code: 'fi-FI', name: 'Suomi', nameEn: 'Finnish', iso639: 'fi' }),
  withCapabilities({ code: 'cs-CZ', name: 'Čeština', nameEn: 'Czech', iso639: 'cs' }),
  withCapabilities({ code: 'fa-IR', name: 'فارسی', nameEn: 'Persian', iso639: 'fa' }),
  withCapabilities({ code: 'hi-IN', name: 'हिन्दी', nameEn: 'Hindi', iso639: 'hi' }),
  withCapabilities({ code: 'id-ID', name: 'Bahasa Indonesia', nameEn: 'Indonesian', iso639: 'id' }),
  withCapabilities({ code: 'ms-MY', name: 'Bahasa Melayu', nameEn: 'Malay', iso639: 'ms' }),
  withCapabilities({ code: 'tr-TR', name: 'Türkçe', nameEn: 'Turkish', iso639: 'tr' }),
]

export const SUPPORTED_TARGET_LANGUAGES: TargetLanguage[] =
  TARGET_LANGUAGE_CATALOG

export function getLanguageByCode(code: string): TargetLanguage | undefined {
  if (typeof code !== 'string') return undefined

  const raw = code.trim()
  if (!raw) return undefined

  const normalized = raw.replace(/_/g, '-').toLowerCase()
  const canonical = TARGET_LANGUAGE_ALIASES[normalized] ?? raw
  const lookup = canonical.toUpperCase()

  return TARGET_LANGUAGE_CATALOG.find(
    (language) => language.code.toUpperCase() === lookup
  )
}

export function getCanonicalLanguageCode(code: string): string | undefined {
  return getLanguageByCode(code)?.code
}

export function normalizeLanguageCode(code: string): string {
  return getCanonicalLanguageCode(code) ?? code.trim()
}

export function getTargetLanguageCapability(
  code: string
): TargetLanguageCapability {
  const language = getLanguageByCode(code)
  return (language && TARGET_LANGUAGE_CAPABILITIES[language.code]) ??
    LATIN_LANGUAGE_CAPABILITY
}

export function getTargetLanguageTextClass(code: string): string {
  const capability = getTargetLanguageCapability(code)
  if (capability.script === 'latin') {
    return `${capability.fontClass} text-sm leading-relaxed tracking-normal normal-case`
  }
  return `${capability.fontClass} text-base leading-loose tracking-normal normal-case`
}

export const DEFAULT_TARGET_LANGUAGE = 'en-GB'

const LOCALES_CAPITALIZE_LANGUAGE = new Set(['en', 'de', 'nl'])

export function formatLanguageName(name: string, locale: string): string {
  const lang = locale.split('-')[0]
  return LOCALES_CAPITALIZE_LANGUAGE.has(lang) ? name : name.toLowerCase()
}
