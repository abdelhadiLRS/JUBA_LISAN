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
