import { beforeEach, describe, expect, it } from 'vitest'

describe('saveTranslatedWordLocally', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('rejects malformed runtime input instead of throwing', async () => {
    const { saveTranslatedWordLocally } = await import('@/lib/api')

    expect(saveTranslatedWordLocally({ word: 123 } as never)).toEqual([])
    expect(saveTranslatedWordLocally({ word: 'hello', translation: 'bonjour', target: '' } as never)).toEqual([])
  })

  it('normalizes valid runtime input before persisting', async () => {
    const { saveTranslatedWordLocally } = await import('@/lib/api')

    const result = saveTranslatedWordLocally({
      source: 'en',
      target: 'fr',
      word: 'hello',
      translation: 'bonjour',
    })

    expect(result).toHaveLength(1)
    expect(result[0]).toMatchObject({ source: 'en', target: 'fr', word: 'hello', translation: 'bonjour' })
    expect(result[0].createdAt).toEqual(expect.any(String))
  })
})