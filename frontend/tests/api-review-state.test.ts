import { beforeEach, describe, expect, it } from 'vitest'

const REVIEW_KEY = 'juba_lisan_review_state'

describe('getGuestReviewState', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('drops malformed cards and normalizes unsafe numeric values', async () => {
    localStorage.setItem(
      REVIEW_KEY,
      JSON.stringify({
        valid: { repetitions: 2, interval: 10, ease: 2.5, due: 1000 },
        negative: { repetitions: -2, interval: -5, ease: 0, due: -10 },
        text: { repetitions: '2', interval: 10, ease: 2.5, due: 1000 },
        missing: { repetitions: 1, interval: 10, ease: 2.5 },
        nested: null,
        array: [],
      })
    )

    const { getGuestReviewState } = await import('@/lib/api')
    expect(getGuestReviewState()).toEqual({
      valid: { repetitions: 2, interval: 10, ease: 2.5, due: 1000 },
      negative: { repetitions: 0, interval: 0, ease: 1, due: 0 },
    })
  })

  it('returns an empty state when persisted JSON is not an object', async () => {
    localStorage.setItem(REVIEW_KEY, JSON.stringify([1, 2, 3]))

    const { getGuestReviewState } = await import('@/lib/api')
    expect(getGuestReviewState()).toEqual({})
  })
})
