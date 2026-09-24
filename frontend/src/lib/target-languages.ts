export interface TargetLanguage {
  code: string
  name: string
  nameEn: string
  iso639: string
  script: TargetLanguageScript
  fontClass: string
  usesWordSpacing: boolean
  romanization?: TargetLanguageRomanization
}

export type TargetLanguageScript =
  | 'latin'
  | 'hiragana-katakana-kanji'
  | 'hangul'
  | 'simplified-hanzi'
  | 'arabic'

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
}

function withCapabilities(
  language: Omit<TargetLanguage, keyof TargetLanguageCapability>
): TargetLanguage {
  return {
    ...language,
    ...(TARGET_LANGUAGE_CAPABILITIES[language.code] ??
      LATIN_LANGUAGE_CAPABILITY),
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
]

export const SUPPORTED_TARGET_LANGUAGES: TargetLanguage[] =
  TARGET_LANGUAGE_CATALOG

export function getLanguageByCode(code: string): TargetLanguage | undefined {
  const upper = code.toUpperCase()
  return TARGET_LANGUAGE_CATALOG.find((l) => l.code.toUpperCase() === upper)
}

export function getTargetLanguageCapability(
  code: string
): TargetLanguageCapability {
  return TARGET_LANGUAGE_CAPABILITIES[code] ?? LATIN_LANGUAGE_CAPABILITY
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
