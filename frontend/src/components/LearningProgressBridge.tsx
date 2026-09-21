'use client'

import { usePathname } from 'next/navigation'
import { useLearningProgressSync } from '@/hooks/use-learning-progress'

export function refreshLearningPlan(
  pathname: string,
  reload: () => void = () => window.location.reload(),
): void {
  if (pathname === '/plan' || pathname.startsWith('/plan/')) {
    reload()
  }
}

export function LearningProgressBridge(): null {
  const pathname = usePathname()

  useLearningProgressSync(() => {
    refreshLearningPlan(pathname)
  })

  return null
}
