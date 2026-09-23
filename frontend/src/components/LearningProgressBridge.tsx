'use client'

import { usePathname, useRouter } from 'next/navigation'
import { useLearningProgressSync } from '@/hooks/use-learning-progress'

function isLearningPlanRoute(pathname: string): boolean {
  const normalized = pathname.split('?')[0].replace(/\/+$/, '') || '/'
  return normalized === '/plan' || /^\/[^/]+\/plan(?:\/.*)?$/.test(normalized)
}

export function refreshLearningPlan(
  pathname: string,
  refresh: () => void = () => window.location.reload(),
): void {
  if (isLearningPlanRoute(pathname)) {
    refresh()
  }
}

export function LearningProgressBridge(): null {
  const pathname = usePathname()
  const router = useRouter()

  useLearningProgressSync(() => {
    refreshLearningPlan(pathname, () => router.refresh())
  })

  return null
}
