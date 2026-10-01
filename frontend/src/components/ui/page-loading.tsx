'use client'

import { useEffect } from 'react'

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
        className={`text-[var(--duo-muted)] animate-pulse text-xs font-medium tracking-[0.12em] uppercase ${className}`}
        role="status"
        aria-busy="true"
        aria-label={text}
      >
        {showDot && <i className="ti ti-loader-2 icon icon-spin" aria-hidden="true" />}
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
      <div className="card flex min-w-52 flex-col items-center gap-3 border border-[var(--duo-line)] bg-[var(--duo-card)] px-6 py-5 shadow-sm">
        <span className="inline-flex items-center rounded-full border border-[var(--duo-line)] bg-[var(--duo-mint)] px-3 py-1.5 text-[var(--duo-green-dark)] text-xs font-semibold tracking-[0.08em] uppercase">
          {showDot && <i className="ti ti-loader-2 icon icon-spin" aria-hidden="true" />}
          {text}
        </span>
        {subtext && (
          <p className="flex items-center gap-1.5 text-[var(--duo-muted)] max-w-xs text-center text-xs leading-5">
            {subtext}
          </p>
        )}
      </div>
    </div>
  )
}
