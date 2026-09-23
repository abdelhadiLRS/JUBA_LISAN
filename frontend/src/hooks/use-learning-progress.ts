'use client'

import { useEffect, useRef } from 'react'
import { subscribeToLearningProgressUpdated } from '@/lib/learning-progress'

type LearningProgressRefreshOptions = {
  refreshOnVisibility?: boolean
  refreshOnPageShow?: boolean
}

export function useLearningProgressSync(
  onRefresh: () => void | Promise<void>,
  options: LearningProgressRefreshOptions = {},
): void {
  const refreshRef = useRef(onRefresh)

  useEffect(() => {
    refreshRef.current = onRefresh
  }, [onRefresh])

  useEffect(() => {
    let refreshInFlight = false
    let refreshQueued = false
    let disposed = false

    const refresh = () => {
      if (disposed) return
      if (refreshInFlight) {
        refreshQueued = true
        return
      }

      refreshInFlight = true
      Promise.resolve()
        .then(() => refreshRef.current())
        .catch(() => {
          // Refresh failures are owned by the caller; lifecycle sync must stay alive.
        })
        .finally(() => {
          refreshInFlight = false
          if (refreshQueued && !disposed) {
            refreshQueued = false
            refresh()
          }
        })
    }

    const unsubscribe = subscribeToLearningProgressUpdated(refresh)
    const onPageShow = () => refresh()
    const onVisibilityChange = () => {
      if (document.visibilityState === 'visible') refresh()
    }

    if (options.refreshOnPageShow !== false) {
      window.addEventListener('pageshow', onPageShow)
    }
    if (options.refreshOnVisibility !== false) {
      document.addEventListener('visibilitychange', onVisibilityChange)
    }

    return () => {
      disposed = true
      refreshQueued = false
      unsubscribe()
      window.removeEventListener('pageshow', onPageShow)
      document.removeEventListener('visibilitychange', onVisibilityChange)
    }
  }, [options.refreshOnPageShow, options.refreshOnVisibility])
}
