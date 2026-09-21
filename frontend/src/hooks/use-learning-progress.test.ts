import { renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { useLearningProgressSync } from '@/hooks/use-learning-progress'

const flush = () => new Promise((resolve) => setTimeout(resolve, 0))

describe('useLearningProgressSync', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('refreshes when learning progress is broadcast', async () => {
    const refresh = vi.fn()
    renderHook(() => useLearningProgressSync(refresh))

    window.dispatchEvent(new Event('juba:learning-progress-updated'))
    await flush()

    expect(refresh).toHaveBeenCalledTimes(1)
  })

  it('refreshes when the page becomes visible again', async () => {
    const refresh = vi.fn()
    renderHook(() => useLearningProgressSync(refresh))

    document.dispatchEvent(new Event('visibilitychange'))
    await flush()

    expect(refresh).toHaveBeenCalledTimes(1)
  })

  it('can disable lifecycle refreshes while retaining the progress event', async () => {
    const refresh = vi.fn()
    renderHook(() =>
      useLearningProgressSync(refresh, {
        refreshOnVisibility: false,
        refreshOnPageShow: false,
      }),
    )

    window.dispatchEvent(new Event('juba:learning-progress-updated'))
    window.dispatchEvent(new Event('pageshow'))
    document.dispatchEvent(new Event('visibilitychange'))
    await flush()

    expect(refresh).toHaveBeenCalledTimes(1)
  })
})
