'use client'

import { useEffect } from 'react'
import { useTranslations } from 'next-intl'
import { useLoadingStore } from '@/store/loading'

interface PageLoadingProps {
  /** Translated label. Defaults to common.loading. */
  label?: string
  /** Optional subtext shown below the main label. */
  subtext?: string
  /** Whether to show the ● decorative dot. Default true. */
  showDot?: boolean
  /** Container min-height Tailwind class. Default "min-h-[60vh]". */
  minHeight?: string
  /** Render as full-screen centered block. Set false for inline usage. */
  fullScreen?: boolean
  /** Extra classes for the outer container / span. */
  className?: string
}

export function PageLoading({
  label,
  subtext,
  showDot = true,
  minHeight = 'min-h-[60vh]',
  fullScreen = true,
  className = '',
}: PageLoadingProps) {
  const t = useTranslations('common')

  useEffect(() => {
    const { inc, dec } = useLoadingStore.getState()
    inc()
    return () => {
      dec()
    }
  }, [])

  const text = label ?? t('loading')

  if (!fullScreen) {
    return (
      <span
        className={`text-[var(--juba-app-muted)] animate-pulse text-xs font-medium tracking-[0.12em] uppercase ${className}`}
        role="status"
        aria-busy="true"
        aria-label={text}
      >
        {showDot && <span className="mr-1.5 text-[var(--juba-app-green-dark)]">●</span>}
        {text}
      </span>
    )
  }

  return (
    <div
      className={`flex ${minHeight} items-center justify-center ${className}`}
      role="status"
      aria-busy="true"
      aria-label={text}
    >
      <div className="juba-card flex min-w-44 flex-col items-center gap-3 border-2 border-[var(--juba-app-line)] px-5 py-4 shadow-[4px_4px_0_var(--juba-app-line)]">
        <span className="text-[var(--juba-app-muted)] animate-pulse text-xs font-medium tracking-[0.12em] uppercase">
          {showDot && <span className="mr-1.5 text-[var(--juba-app-green-dark)]">●</span>}
          {text}
        </span>
        {subtext && (
          <p className="text-[var(--juba-app-muted)] max-w-xs text-center text-xs leading-5">
            {subtext}
          </p>
        )}
      </div>
    </div>
  )
}
