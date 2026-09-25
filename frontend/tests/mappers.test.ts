import { describe, expect, it } from 'vitest'
import { mapUser, mapUserLanguageInfo } from '@/lib/mappers'

describe('language API mappers', () => {
  it('canonicalizes supported target language codes on user payloads', () => {
    const user = mapUser({
      id: 1,
      username: 'learner',
      display_name: 'Learner',
      target_language: ' cs-cz ',
      role: 'user',
    })

    expect(user.target_language).toBe('cs-CZ')
  })

  it('canonicalizes supported target language codes on user-language payloads', () => {
    const language = mapUserLanguageInfo({
      target_language: ' EL-gr ',
      is_active: true,
      plan: null,
      progress: null,
    })

    expect(language.target_language).toBe('el-GR')
  })

  it('preserves unknown target codes for API compatibility', () => {
    const language = mapUserLanguageInfo({
      target_language: 'custom-code',
      is_active: false,
    })

    expect(language.target_language).toBe('custom-code')
  })
})
