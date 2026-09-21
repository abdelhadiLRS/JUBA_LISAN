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

  it('returns a safe no-op unsubscribe when window is unavailable', () => {
    const originalWindow = globalThis.window
    vi.stubGlobal('window', undefined)

    try {
      expect(subscribeToLearningProgressUpdated(vi.fn())).toEqual(expect.any(Function))
    } finally {
      vi.stubGlobal('window', originalWindow)
    }
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

  it('broadcasts progress updates through BroadcastChannel', () => {
    const listener = vi.fn()
    const postMessage = vi.spyOn(BroadcastChannel.prototype, 'postMessage')
    const unsubscribe = subscribeToLearningProgressUpdated(listener)

    markLearningProgressUpdated()

    expect(postMessage).toHaveBeenCalledWith(
      expect.objectContaining({
        type: 'juba:learning-progress-updated',
      }),
    )

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

  it('ignores storage events that clear the progress key', () => {
    const listener = vi.fn()
    const unsubscribe = subscribeToLearningProgressUpdated(listener)

    window.dispatchEvent(
      new StorageEvent('storage', {
        key: 'juba:learning-progress-updated',
        newValue: null,
        storageArea: localStorage,
      }),
    )

    expect(listener).not.toHaveBeenCalled()

    unsubscribe()
  })

  it('ignores storage events from a different storage area', () => {
    const listener = vi.fn()
    const unsubscribe = subscribeToLearningProgressUpdated(listener)

    window.dispatchEvent(
      new StorageEvent('storage', {
        key: 'juba:learning-progress-updated',
        newValue: String(Date.now()),
        storageArea: sessionStorage,
      }),
    )

    expect(listener).not.toHaveBeenCalled()

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
