import { describe, expect, it } from 'vitest'
import {
  TARGET_LANGUAGE_CATALOG,
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
    expect(getLanguageByCode('EL-gr')?.code).toBe('el-GR')\n    expect(getTargetLanguageCapability('CS-cz').script).toBe('latin')\n    expect(getTargetLanguageCapability('EL-gr').script).toBe('greek')
  })
})
