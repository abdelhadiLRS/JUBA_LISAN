import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  markLearningProgressUpdated,
  subscribeToLearningProgressUpdated,
} from '@/lib/learning-progress'

describe('learning progress signal', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    sessionStorage.clear()
    localStorage.clear()
  })

  it('persists a timestamp and dispatches the shared event', () => {
    const listener = vi.fn()
    const unsubscribe = subscribeToLearningProgressUpdated(listener)

    markLearningProgressUpdated()

    expect(listener).toHaveBeenCalledTimes(1)
    expect(sessionStorage.getItem('juba:learning-progress-updated')).toMatch(/^\d+$/)
    expect(localStorage.getItem('juba:learning-progress-updated')).toMatch(/^\d+$/)

    unsubscribe()
  })

  it('refreshes from a cross-tab storage event', () => {
    const listener = vi.fn()
    const unsubscribe = subscribeToLearningProgressUpdated(listener)

    window.dispatchEvent(
      new StorageEvent('storage', {
        key: 'juba:learning-progress-updated',
        newValue: String(Date.now()),
        storageArea: localStorage,
      }),
    )

    expect(listener).toHaveBeenCalledTimes(1)

    unsubscribe()
  })

  it('ignores unrelated storage events', () => {
    const listener = vi.fn()
    const unsubscribe = subscribeToLearningProgressUpdated(listener)

    window.dispatchEvent(
      new StorageEvent('storage', {
        key: 'unrelated-key',
        newValue: '1',
        storageArea: localStorage,
      }),
    )

    expect(listener).not.toHaveBeenCalled()

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
