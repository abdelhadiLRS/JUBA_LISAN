'use client'

import { type ReactNode } from 'react'
import { useTranslations } from 'next-intl'
import { Check, Circle, Lock, PlayCircle, Ribbon } from 'lucide-react'

interface UnitStatus {
  completed: boolean
  active: boolean
  locked: boolean
  isLevelTest: boolean
}

interface Props {
  title: string
  index: number
  lessonCount: number
  grammarCount: number
  competency: number // 0–1, completion ratio
  status: UnitStatus
  onClick: () => void
  /** When provided and status.active, a start CTA is rendered on the card */
  onStartLesson?: () => void
}

function StatusBadge({ status }: { status: UnitStatus }): ReactNode {
  if (status.isLevelTest) {
    return (
      <span
        className="flex h-9 w-9 items-center justify-center rounded-full"
        style={{
          background: status.active
            ? 'var(--juba-primary-soft)'
            : 'var(--juba-surface-soft)',
          color: status.active ? 'var(--juba-primary)' : 'var(--juba-muted)',
        }}
      >
        <Ribbon className="h-4.5 w-4.5" aria-hidden="true" />
      </span>
    )
  }
  if (status.completed) {
    return (
      <span
        className="flex h-9 w-9 items-center justify-center rounded-full text-white"
        style={{ background: 'var(--juba-primary)' }}
      >
        <Check className="h-4.5 w-4.5" aria-hidden="true" />
      </span>
    )
  }
  if (status.active) {
    return (
      <span
        className="flex h-9 w-9 items-center justify-center rounded-full"
        style={{
          background: 'var(--juba-warm-soft)',
          color: 'var(--juba-warm)',
        }}
      >
        <PlayCircle className="h-4.5 w-4.5" aria-hidden="true" />
      </span>
    )
  }
  if (status.locked) {
    return (
      <span className="bg-fl-surface-2 text-fl-muted-3 flex h-9 w-9 items-center justify-center rounded-full">
        <Lock className="h-4 w-4" aria-hidden="true" />
      </span>
    )
  }
  return (
    <span className="border-fl-border text-fl-muted-3 flex h-9 w-9 items-center justify-center rounded-full border">
      <Circle className="h-3.5 w-3.5" aria-hidden="true" />
    </span>
  )
}

export default function UnitCard({
  title,
  index,
  lessonCount,
  grammarCount,
  competency,
  status,
  onClick,
  onStartLesson,
}: Props) {
  const t = useTranslations('plan')
  const tCommon = useTranslations('common')
  const barWidth = Math.round(competency * 100)

  const barColor = status.completed
    ? 'var(--juba-primary)'
    : status.active
      ? 'var(--juba-warm)'
      : 'var(--juba-muted)'

  return (
    <div
      className={`border-fl-border bg-fl-surface rounded-2xl border transition-all ${
        status.locked
          ? 'opacity-55'
          : 'hover:shadow-[0_4px_16px_rgba(23,35,27,0.06)]'
      } ${status.active ? 'ring-1' : ''}`}
      style={
        status.active
          ? {
              // @ts-expect-error CSS custom property
              '--tw-ring-color':
                'color-mix(in srgb, var(--juba-warm) 45%, transparent)',
            }
          : undefined
      }
    >
      {/* Clickable card header — opens drawer */}
      <button
        onClick={onClick}
        disabled={status.locked}
        className={`group w-full rounded-2xl text-start ${
          status.locked ? 'cursor-default' : ''
        }`}
        aria-label={t('unitAriaLabel', { index: index + 1, title })}
      >
        <div className="flex items-center gap-3.5 px-4 py-4 sm:px-5">
          <StatusBadge status={status} />
          <div className="min-w-0 flex-1">
            <div className="flex items-baseline gap-2">
              <span className="text-fl-muted-3 shrink-0 text-xs font-semibold tabular-nums">
                {String(index + 1).padStart(2, '0')}
              </span>
              <span
                className={`truncate text-sm font-semibold ${
                  status.locked
                    ? 'text-fl-muted-3'
                    : 'text-fl-fg group-hover:text-[var(--juba-primary-dark)]'
                }`}
              >
                {title}
              </span>
            </div>
            <div className="mt-1 flex items-center gap-3 text-xs text-[var(--juba-muted)]">
              <span>{t('nLessons', { count: lessonCount })}</span>
              {grammarCount > 0 && (
                <span>{t('nGrammar', { count: grammarCount })}</span>
              )}
              {status.isLevelTest && (
                <span
                  className="rounded-full px-2 py-0.5 text-[11px] font-semibold"
                  style={{
                    color: 'var(--juba-primary-dark)',
                    background: 'var(--juba-primary-soft)',
                  }}
                >
                  {t('levelTestLabel')}
                </span>
              )}
            </div>
          </div>
          {!status.locked && (
            <span className="text-fl-muted-2 shrink-0 text-sm font-semibold tabular-nums">
              {barWidth}%
            </span>
          )}
        </div>

        {/* Progress bar */}
        {!status.locked && (
          <div className="bg-fl-surface-2 mx-4 mb-4 h-1.5 overflow-hidden rounded-full sm:mx-5">
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{ width: `${barWidth}%`, background: barColor }}
            />
          </div>
        )}
      </button>

      {/* Start CTA — only shown on the active unit when a lesson is ready */}
      {status.active && onStartLesson && (
        <div className="border-fl-border flex justify-end border-t px-4 py-3 sm:px-5">
          <button
            onClick={onStartLesson}
            className="rounded-xl bg-[var(--juba-primary)] px-4 py-2 text-xs font-bold text-white transition-colors hover:bg-[var(--juba-primary-dark)]"
          >
            {tCommon('start')} →
          </button>
        </div>
      )}
    </div>
  )
}
