'use client'

import { useEffect, useRef } from 'react'
import { useLoadingStore } from '@/store/loading'

interface PaginationProps {
  /** 0-indexed current page. */
  page: number
  /** Total number of pages. */
  totalPages: number
  /** Disables buttons during fetch. */
  loading?: boolean
  /** Called with the new 0-indexed page number. */
  onPageChange: (page: number) => void
  /** Translated text for the previous button. */
  prevLabel: string
  /** Translated text for the next button. */
  nextLabel: string
  /** Pre-formatted page info shown between buttons (e.g. "2 / 5"). Falls back to "page+1 / totalPages". */
  pageInfo?: string
  /** Extra classes for the outer container. */
  className?: string
}

export function Pagination({
  page,
  totalPages,
  loading = false,
  onPageChange,
  prevLabel,
  nextLabel,
  pageInfo,
  className = '',
}: PaginationProps) {
  const incDone = useRef(false)

  useEffect(() => {
    if (loading && !incDone.current) {
      incDone.current = true
      useLoadingStore.getState().inc()
    }
    if (!loading && incDone.current) {
      useLoadingStore.getState().dec()
      incDone.current = false
    }
    return () => {
      if (incDone.current) {
        useLoadingStore.getState().dec()
        incDone.current = false
      }
    }
  }, [loading])

  if (totalPages <= 1) return null

  const isFirst = page <= 0
  const isLast = page >= totalPages - 1
  const isDisabled = loading

  const info = pageInfo ?? `${page + 1} / ${totalPages}`

  return (
    <div
      className={`juba-card flex items-center justify-between gap-3 px-4 py-3 md:px-5`}
    >
      <button
        onClick={() => onPageChange(Math.max(0, page - 1))}
        disabled={isFirst || isDisabled}
        className="rounded-xl border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-xs font-bold tracking-widest uppercase text-[var(--juba-muted)] transition-colors hover:border-[var(--juba-primary)] hover:bg-[var(--juba-primary-soft)] hover:text-[var(--juba-primary-dark)] disabled:cursor-not-allowed disabled:opacity-30"
      >
        {prevLabel}
      </button>
      <span className="rounded-lg bg-[var(--juba-surface-soft)] px-3 py-1.5 text-xs font-semibold tabular-nums text-[var(--juba-muted)]">
        {info}
      </span>
      <button
        onClick={() => onPageChange(page + 1)}
        disabled={isLast || isDisabled}
        className="rounded-xl border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-xs font-bold tracking-widest uppercase text-[var(--juba-muted)] transition-colors hover:border-[var(--juba-primary)] hover:bg-[var(--juba-primary-soft)] hover:text-[var(--juba-primary-dark)] disabled:cursor-not-allowed disabled:opacity-30"
      >
        {nextLabel}
      </button>
    </div>
  )
}
