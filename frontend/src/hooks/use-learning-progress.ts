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
    const refresh = () => {
      void refreshRef.current()
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
      unsubscribe()
      window.removeEventListener('pageshow', onPageShow)
      document.removeEventListener('visibilitychange', onVisibilityChange)
    }
  }, [options.refreshOnPageShow, options.refreshOnVisibility])
}
