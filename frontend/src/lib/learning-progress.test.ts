import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  markLearningProgressUpdated,
  subscribeToLearningProgressUpdated,
} from '@/lib/learning-progress'

describe('learning progress signal', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    sessionStorage.clear()
  })

  it('persists a timestamp and dispatches the shared event', () => {
    const listener = vi.fn()
    const unsubscribe = subscribeToLearningProgressUpdated(listener)

    markLearningProgressUpdated()

    expect(listener).toHaveBeenCalledTimes(1)
    expect(sessionStorage.getItem('juba:learning-progress-updated')).toMatch(/^\d+$/)

    unsubscribe()
  })

  it('removes the listener when unsubscribed', () => {
    const listener = vi.fn()
    const unsubscribe = subscribeToLearningProgressUpdated(listener)

    unsubscribe()
    window.dispatchEvent(new Event('juba:learning-progress-updated'))

    expect(listener).not.toHaveBeenCalled()
  })
})
