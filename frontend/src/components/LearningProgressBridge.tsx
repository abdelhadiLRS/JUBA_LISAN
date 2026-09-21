'use client'

import { usePathname } from 'next/navigation'
import { useLearningProgressSync } from '@/hooks/use-learning-progress'

export function LearningProgressBridge(): null {
  const pathname = usePathname()

  useLearningProgressSync(() => {
    if (pathname === '/plan' || pathname.startsWith('/plan/')) {
      window.location.reload()
    }
  })

  return null
}
