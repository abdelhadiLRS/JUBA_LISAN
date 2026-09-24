'use client'

import { useEffect } from 'react'
import { Loader2, Sparkles } from 'lucide-react'
import { useTranslations } from 'next-intl'
import { useLoadingStore } from '@/store/loading'

interface PageLoadingProps {
  /** Translated label. Defaults to common.loading. */
  label?: string
  /** Optional subtext shown below the main label. */
  subtext?: string
  /** Whether to show the loading indicator. Default true. */
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
        {showDot && <Loader2 className="mr-1.5 inline-block h-3.5 w-3.5 animate-spin align-[-0.2em]" aria-hidden="true" />}
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
      <div className="juba-card flex min-w-52 flex-col items-center gap-3 border-2 border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] px-6 py-5 shadow-[4px_4px_0_var(--juba-app-line)]">
        <span className="inline-flex items-center rounded-full border border-[var(--juba-app-line)] bg-[var(--juba-app-green-soft)] px-3 py-1.5 text-[var(--juba-app-green-dark)] text-xs font-semibold tracking-[0.08em] uppercase">
          {showDot && <Loader2 className="mr-1.5 inline-block h-3.5 w-3.5 animate-spin align-[-0.2em] text-[var(--juba-app-green-dark)]" aria-hidden="true" />}
          {text}
        </span>
        {subtext && (
          <p className="flex items-center gap-1.5 text-[var(--juba-app-muted)] max-w-xs text-center text-xs leading-5">
            {subtext}
          </p>
        )}
      </div>
    </div>
  )
}
