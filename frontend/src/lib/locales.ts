// Single source of truth for supported site UI locales.
// Learning-language coverage is maintained separately by the language atlas.
export const SUPPORTED_LOCALES = [
  'en',
  'ar',
  'es',
  'fr',
  'pt',
  'de',
  'it',
  'pl',
  'nl',
  'ro',
  'ru',
] as const

export type Locale = (typeof SUPPORTED_LOCALES)[number]

const LOCALE_ALIASES: Record<string, Locale> = {
  en: 'en',
  'en-gb': 'en',
  'en-us': 'en',
  'en-au': 'en',
  'en-ca': 'en',
  ar: 'ar',
  'ar-dz': 'ar',
  'ar-sa': 'ar',
  es: 'es',
  'es-es': 'es',
  'es-mx': 'es',
  fr: 'fr',
  'fr-fr': 'fr',
  'fr-ca': 'fr',
  de: 'de',
  'de-de': 'de',
  'de-at': 'de',
  it: 'it',
  'it-it': 'it',
  pt: 'pt',
  'pt-pt': 'pt',
  'pt-br': 'pt',
  pl: 'pl',
  'pl-pl': 'pl',
  nl: 'nl',
  'nl-nl': 'nl',
  ro: 'ro',
  'ro-ro': 'ro',
  ru: 'ru',
  'ru-ru': 'ru',
  'uk-ua': 'ru',
}

export function normalizeLocale(value: string | undefined | null): Locale {
  const raw = value?.trim().replace(/_/g, '-').toLowerCase()
  if (!raw) return 'en'
  return LOCALE_ALIASES[raw] ?? LOCALE_ALIASES[raw.split('-')[0]] ?? 'en'
}
