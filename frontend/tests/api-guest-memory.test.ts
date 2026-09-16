import { beforeEach, describe, expect, it } from 'vitest'

describe('getGuestMemory', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('drops malformed saved words before sync code can consume them', async () => {
    localStorage.setItem(
      'juba_lisan_saved_vocabulary',
      JSON.stringify([
        { source: 'en', target: 'fr', word: 'hello', translation: 'bonjour' },
        { source: 'en', target: 42, word: 'bad-target', translation: 'mauvaise' },
        { source: 'en', target: 'fr', word: 'bad-translation', translation: 123 },
        { source: 'en', target: 'fr', word: '', translation: 'empty' },
        null,
      ])
    )

    const { getGuestMemory } = await import('@/lib/api')
    expect(getGuestMemory()).toEqual([
      { source: 'en', target: 'fr', word: 'hello', translation: 'bonjour' },
    ])
  })

  it('preserves an optional createdAt only when it is a string', async () => {
    localStorage.setItem(
      'juba_lisan_saved_vocabulary',
      JSON.stringify([
        { source: 'en', target: 'fr', word: 'hello', translation: 'bonjour', createdAt: '2026-09-16T10:00:00.000Z' },
        { source: 'en', target: 'fr', word: 'salut', translation: 'hi', createdAt: 123 },
      ])
    )

    const { getGuestMemory } = await import('@/lib/api')
    expect(getGuestMemory()).toEqual([
      { source: 'en', target: 'fr', word: 'hello', translation: 'bonjour', createdAt: '2026-09-16T10:00:00.000Z' },
      { source: 'en', target: 'fr', word: 'salut', translation: 'hi' },
    ])
  })
})
