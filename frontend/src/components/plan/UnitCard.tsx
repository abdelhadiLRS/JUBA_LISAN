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
        className="flex h-12 w-12 items-center justify-center rounded-[18px]"
        style={{
          background: status.active
            ? 'var(--juba-lilac)'
            : '#f5f2ff',
          color: status.active ? 'var(--juba-violet-dark)' : '#938da2',
        }}
      >
        <Ribbon className="h-5 w-5" aria-hidden="true" />
      </span>
    )
  }
  if (status.completed) {
    return (
      <span
        className="flex h-12 w-12 items-center justify-center rounded-[18px]"
        style={{
          background: 'var(--juba-violet)',
          color: '#fff',
        }}
      >
        <Check className="h-5 w-5" aria-hidden="true" />
      </span>
    )
  }
  if (status.active) {
    return (
      <span
        className="flex h-12 w-12 items-center justify-center rounded-[18px]"
        style={{
          background: 'var(--juba-yellow)',
          color: 'var(--juba-violet-dark)',
        }}
      >
        <PlayCircle className="h-5 w-5" aria-hidden="true" />
      </span>
    )
  }
  if (status.locked) {
    return (
      <span className="bg-white-2 text-[#938da2] flex h-12 w-12 items-center justify-center rounded-[18px]">
        <Lock className="h-4 w-4" aria-hidden="true" />
      </span>
    )
  }
  return (
    <span className="border-[#ebe7f5] text-[#938da2] flex h-12 w-12 items-center justify-center rounded-[18px] border">
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
    ? 'var(--juba-violet)'
    : status.active
      ? 'var(--juba-coral)'
      : '#938da2'

  return (
    <div
      className={`border-[#ebe7f5] bg-white rounded-[26px] border-2 transition-all ${
        status.locked
          ? 'opacity-55'
          : 'hover:shadow-[0_14px_32px_rgba(39,28,72,0.08)]'
      } ${status.active ? 'ring-1' : ''}`}
      style={
        status.active
          ? {
              // @ts-expect-error CSS custom property
              '--tw-ring-color':
                'color-mix(in srgb, var(--juba-coral) 45%, transparent)',
            }
          : undefined
      }
    >
      <button
        onClick={onClick}
        disabled={status.locked}
        className={`group w-full rounded-[24px] text-start ${
          status.locked ? 'cursor-default' : ''
        }`}
        aria-label={t('unitAriaLabel', { index: index + 1, title })}
      >
        <div className="flex items-center gap-3.5 px-5 py-5 sm:px-6">
          <StatusBadge status={status} />
          <div className="min-w-0 flex-1">
            <div className="flex items-baseline gap-2">
              <span className="text-[#938da2] shrink-0 text-xs font-semibold tabular-nums">
                {String(index + 1).padStart(2, '0')}
              </span>
              <span
                className={`truncate text-sm font-semibold ${
                  status.locked
                    ? 'text-[#938da2]'
                    : 'text-[#242033] group-hover:text-[var(--juba-violet-dark)]'
                }`}
              >
                {title}
              </span>
            </div>
            <div className="mt-1 flex items-center gap-3 text-xs text-[#938da2]">
              <span>{t('nLessons', { count: lessonCount })}</span>
              {grammarCount > 0 && (
                <span>{t('nGrammar', { count: grammarCount })}</span>
              )}
              {status.isLevelTest && (
                <span
                  className="rounded-full px-2 py-0.5 text-[11px] font-semibold"
                  style={{
                    color: 'var(--juba-violet-dark)',
                    background: 'var(--juba-lilac)',
                  }}
                >
                  {t('levelTestLabel')}
                </span>
              )}
            </div>
          </div>
          {!status.locked && (
            <span className="text-[#777087] shrink-0 text-sm font-semibold tabular-nums">
              {barWidth}%
            </span>
          )}
        </div>

        {!status.locked && (
          <div className="bg-white-2 mx-5 mb-5 h-2 overflow-hidden rounded-full sm:mx-5">
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{ width: `${barWidth}%`, background: barColor }}
            />
          </div>
        )}
      </button>

      {status.active && onStartLesson && (
        <div className="border-[#ebe7f5] flex justify-end border-t px-4 py-3 sm:px-5">
          <button
            onClick={onStartLesson}
            className="rounded-xl bg-[var(--juba-violet)] px-4 py-2 text-xs font-bold text-[#fff] transition-colors hover:bg-[var(--juba-violet-dark)]"
          >
            {tCommon('start')} →
          </button>
        </div>
      )}
    </div>
  )
}
