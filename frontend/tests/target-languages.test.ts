import { describe, expect, it } from 'vitest'
import {
  TARGET_LANGUAGE_CATALOG,
  getCanonicalLanguageCode,
  normalizeLanguageCode,
  TARGET_LANGUAGE_CAPABILITIES,
  getLanguageByCode,
  getTargetLanguageCapability,
} from '@/lib/target-languages'

const ACTIVE_CODES = [
  'de-DE',
  'en-GB',
  'en-US',
  'es-ES',
  'fr-FR',
  'it-IT',
  'ja-JP',
  'ko-KR',
  'pt-PT',
  'zh-CN',
  'ar',
  'ru-RU',
  'nl-NL',
  'pl-PL',
  'da-DK',
  'el-GR',
  'sv-SE',
  'no-NO',
  'fi-FI',
  'cs-CZ',
]

describe('target language catalog', () => {
  it('keeps the 20 active target languages available exactly once', () => {
    const codes = TARGET_LANGUAGE_CATALOG.map((language) => language.code)
    expect(codes).toHaveLength(20)
    expect(new Set(codes).size).toBe(20)
    expect(codes.sort()).toEqual([...ACTIVE_CODES].sort())
  })

  it('has capabilities for every active target language and no flag metadata', () => {
    for (const code of ACTIVE_CODES) {
      const language = getLanguageByCode(code)
      expect(language).toBeDefined()
      expect(TARGET_LANGUAGE_CAPABILITIES[code]).toBeDefined()
      expect(getTargetLanguageCapability(code).script).toBeDefined()
      expect(language).not.toHaveProperty('flag')
      expect(language).not.toHaveProperty('flagPath')
    }
  })

  it('resolves target language codes case-insensitively', () => {
    expect(getLanguageByCode('cs-cz')?.code).toBe('cs-CZ')
    expect(getLanguageByCode('EL-gr')?.code).toBe('el-GR')
    expect(getTargetLanguageCapability('CS-cz').script).toBe('latin')
    expect(getTargetLanguageCapability('EL-gr').script).toBe('greek')
  })

  it('resolves trimmed and empty codes safely', () => {
    expect(getLanguageByCode('  cs-CZ  ')?.code).toBe('cs-CZ')
    expect(getLanguageByCode('   ')).toBeUndefined()
  })

  it('returns canonical language codes', () => {
    expect(getCanonicalLanguageCode(' CS-cz ')).toBe('cs-CZ')
    expect(getCanonicalLanguageCode('el-gr')).toBe('el-GR')
    expect(getCanonicalLanguageCode('unknown')).toBeUndefined()
  })

  it('normalizes known and unknown language codes consistently', () => {
    expect(normalizeLanguageCode(' CS-cz ')).toBe('cs-CZ')
    expect(normalizeLanguageCode(' el-gr ')).toBe('el-GR')
    expect(normalizeLanguageCode(' custom-code ')).toBe('custom-code')
  })


  it('normalizes mixed-case available codes in the selector contract', () => {
    const availableCodes = ['en-gb', 'CS-cz', 'EL-gr']
    const availableCodeSet = new Set(
      availableCodes.map((code) => code.trim().toUpperCase()).filter(Boolean)
    )

    expect(
      TARGET_LANGUAGE_CATALOG.filter((language) =>
        availableCodeSet.has(language.code.toUpperCase())
      ).map((language) => language.code)
    ).toEqual(['en-GB', 'el-GR', 'cs-CZ'])
  })

  it('canonicalizes language mutation payloads', () => {
    const canonicalize = (code: string) =>
      getLanguageByCode(code)?.code ?? code.trim()

    expect(canonicalize(' CS-cz ')).toBe('cs-CZ')
    expect(canonicalize('el-gr')).toBe('el-GR')
    expect(canonicalize('en-US')).toBe('en-US')
  })
})
