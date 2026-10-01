'use client'

import { useTranslations } from 'next-intl'

export interface DurationOption {
  weeks: number
  daysPerWeek: number
  intensity: 'intensive' | 'standard' | 'relaxed' | 'very_relaxed'
}

export const DURATION_OPTIONS: DurationOption[] = [
  { weeks: 4, daysPerWeek: 5, intensity: 'intensive' },
  { weeks: 8, daysPerWeek: 5, intensity: 'standard' },
  { weeks: 12, daysPerWeek: 4, intensity: 'relaxed' },
  { weeks: 16, daysPerWeek: 3, intensity: 'very_relaxed' },
]

export const GOAL_OPTIONS = [
  { id: 'grammar' },
  { id: 'vocabulary' },
  { id: 'reading' },
  { id: 'writing' },
  { id: 'conversation' },
  { id: 'listening' },
]

interface Props {
  selectedWeeks: number
  selectedGoals: string[]
  onSelectDuration: (option: DurationOption) => void
  onToggleGoal: (goal: string) => void
  onConfirm: () => void
  onBack: () => void
  cefr_level: string
  loading: boolean
  error?: string
}

export default function DurationSelector({
  selectedWeeks,
  selectedGoals,
  onSelectDuration,
  onToggleGoal,
  onConfirm,
  onBack,
  cefr_level,
  loading,
  error = '',
}: Props) {
  const t = useTranslations('assessment')
  const tCommon = useTranslations('common')
  const selected =
    DURATION_OPTIONS.find((o) => o.weeks === selectedWeeks) ??
    DURATION_OPTIONS[2]

  const intensityMap: Record<string, string> = {
    intensive: t('intensity.intensive'),
    standard: t('intensity.standard'),
    relaxed: t('intensity.relaxed'),
    very_relaxed: t('intensity.veryRelaxed'),
  }

  return (
    <div className="flex min-h-[60vh] items-center justify-center bg-[var(--duo-bg)] p-4 sm:p-6">
      <div className="w-full max-w-2xl overflow-hidden rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] shadow-sm">
        <div className="flex items-center gap-3 border-b border-[var(--duo-line)] bg-[var(--duo-bg)] px-6 py-4">
          <span className="text-xs text-[var(--duo-muted)]">●</span>
          <span className="text-xs text-[var(--duo-muted)] font-semibold tracking-[0.12em] uppercase">
            {t('step3')}
          </span>
        </div>

        <div className="space-y-8 p-6 sm:p-8">
          {/* Duration */}
          <div>
            <p className="text-xs text-[var(--duo-muted)] mb-3 font-semibold tracking-[0.12em] uppercase">
              {t('howManyWeeks', { cefr_level })}
            </p>
            <div className="grid grid-cols-2 gap-3">
              {DURATION_OPTIONS.map((opt) => (
                <button
                  type="button"
                  key={opt.weeks}
                  onClick={() => onSelectDuration(opt)}
                  className={`rounded-[10px] border px-4 py-4 text-left transition-colors ${
                    selectedWeeks === opt.weeks
                      ? 'bg-[var(--duo-green)] text-white border-[var(--duo-green)] shadow-sm'
                      : 'border-[var(--duo-line)] bg-[var(--duo-bg)] text-[var(--duo-ink)] hover:border-[var(--duo-green)] hover:bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] hover:text-[var(--duo-green-dark)]'
                  }`}
                >
                  <p className="font-sans text-xs font-bold tracking-widest uppercase">
                    {t('nWeeks', { count: opt.weeks })}
                  </p>
                  <p
                    className={`text-[var(--duo-muted)] mt-0.5 font-sans ${
                      selectedWeeks === opt.weeks
                        ? 'opacity-70'
                        : 'text-[var(--duo-muted)]'
                    }`}
                  >
                    {intensityMap[opt.intensity]} ·{' '}
                    {t('approxLessons', { count: opt.weeks * opt.daysPerWeek })}
                  </p>
                  <p
                    className={`text-[var(--duo-muted)] mt-0.5 font-sans ${
                      selectedWeeks === opt.weeks
                        ? 'opacity-60'
                        : 'text-[var(--duo-muted)]'
                    }`}
                  >
                    {t('daysPerWeek', { count: opt.daysPerWeek })}
                  </p>
                </button>
              ))}
            </div>
          </div>

          {/* Goals */}
          <div>
            <p className="text-xs text-[var(--duo-muted)] mb-3 font-semibold tracking-[0.12em] uppercase">
              {t('mainGoals')}
            </p>
            <div className="flex flex-wrap gap-2">
              {GOAL_OPTIONS.map((g) => (
                <button
                  type="button"
                  key={g.id}
                  onClick={() => onToggleGoal(g.id)}
                  className={`rounded-full border px-3 py-2 text-xs font-semibold tracking-[0.08em] uppercase transition-colors ${
                    selectedGoals.includes(g.id)
                      ? 'bg-[var(--duo-green)] text-white border-[var(--duo-green)] shadow-sm'
                      : 'border-[var(--duo-line)] bg-[var(--duo-bg)] text-[var(--duo-ink)] hover:border-[var(--duo-green)] hover:bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] hover:text-[var(--duo-green-dark)]'
                  }`}
                >
                  {selectedGoals.includes(g.id) ? '✓ ' : ''}
                  {t(
                    `goals.${g.id as 'grammar' | 'vocabulary' | 'reading' | 'writing' | 'conversation' | 'listening'}`
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Summary */}
          <div className="space-y-1 rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-bg)] px-4 py-3 text-xs tracking-wide text-[var(--duo-ink)]">
            <p>
              {t('summaryLevel')}:{' '}
              <span className="text-[var(--duo-ink)] font-bold">{cefr_level}</span>
            </p>
            <p>
              {t('summaryDuration')}:{' '}
              <span className="text-[var(--duo-ink)]">
                {t('nWeeks', { count: selected.weeks })}
              </span>
              {' · '}
              <span className="text-[var(--duo-ink)]">
                {t('daysPerWeek', { count: selected.daysPerWeek })}
              </span>
            </p>
            <p>
              {t('summaryGoals')}:{' '}
              <span className="text-[var(--duo-ink)]">
                {selectedGoals.length > 0
                  ? selectedGoals
                      .map((g) =>
                        t(
                          `goals.${g as 'grammar' | 'vocabulary' | 'reading' | 'writing' | 'conversation' | 'listening'}`
                        )
                      )
                      .join(', ')
                  : t('noneSelected')}
              </span>
            </p>
          </div>

          {error && (
            <div
              role="alert"
              aria-live="polite"
              className="rounded-[10px] border border-[var(--duo-red)]/30 bg-[var(--duo-red)]/10 px-4 py-3 text-left text-xs leading-relaxed text-[var(--duo-red)]"
            >
              ✕ {error}
            </div>
          )}

          <div className="flex gap-2">
            <button
              type="button"
              onClick={onBack}
              className="border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-ink)] hover:bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] hover:text-[var(--duo-green-dark)] flex-1 rounded-[10px] border py-3 font-sans text-xs tracking-widest uppercase transition-colors"
            >
              ← {tCommon('back')}
            </button>
            <button
              type="button"
              onClick={onConfirm}
              disabled={loading || selectedGoals.length === 0}
              className="bg-[var(--duo-green)] text-white hover:bg-[var(--duo-blue-dark)] flex-[2] rounded-[10px] py-3 font-sans text-xs font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
            >
              {loading ? t('buildingPlan') : `${t('startMyPlan')} →`}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
