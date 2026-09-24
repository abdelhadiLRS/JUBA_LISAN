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
    <div className="flex min-h-[60vh] items-center justify-center p-4 sm:p-6">
      <div className="w-full max-w-2xl overflow-hidden rounded-[26px] border-2 border-[var(--juba-app-green-soft)] bg-white shadow-[8px_8px_0_var(--juba-app-ink)]">
        <div className="flex items-center gap-3 border-b-2 border-[var(--juba-app-green-soft)] bg-[var(--juba-app-green-soft)]/40 px-6 py-4">
          <span className="text-xs text-[var(--juba-app-muted)]">●</span>
          <span className="text-xs text-[var(--juba-app-muted)] font-semibold tracking-[0.12em] uppercase">
            {t('step3')}
          </span>
        </div>

        <div className="space-y-8 p-6 sm:p-8">
          {/* Duration */}
          <div>
            <p className="text-xs text-[var(--juba-app-muted)] mb-3 font-semibold tracking-[0.12em] uppercase">
              {t('howManyWeeks', { cefr_level })}
            </p>
            <div className="grid grid-cols-2 gap-3">
              {DURATION_OPTIONS.map((opt) => (
                <button
                  key={opt.weeks}
                  onClick={() => onSelectDuration(opt)}
                  className={`rounded-[20px] border-2 px-4 py-4 text-left transition-all ${
                    selectedWeeks === opt.weeks
                      ? 'bg-[var(--juba-app-green)] text-white border-[var(--juba-app-ink)]'
                      : 'border-[var(--juba-app-line)] text-[var(--juba-app-muted)] hover:border-2 hover:text-[var(--juba-app-green-dark)]'
                  }`}
                >
                  <p className="font-sans text-xs font-bold tracking-widest uppercase">
                    {t('nWeeks', { count: opt.weeks })}
                  </p>
                  <p
                    className={`text-[var(--juba-app-muted)] mt-0.5 font-sans ${
                      selectedWeeks === opt.weeks
                        ? 'opacity-70'
                        : 'text-[var(--juba-app-muted)]'
                    }`}
                  >
                    {intensityMap[opt.intensity]} ·{' '}
                    {t('approxLessons', { count: opt.weeks * opt.daysPerWeek })}
                  </p>
                  <p
                    className={`text-[var(--juba-app-muted)] mt-0.5 font-sans ${
                      selectedWeeks === opt.weeks
                        ? 'opacity-60'
                        : 'text-[var(--juba-app-muted)]'
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
            <p className="text-xs text-[var(--juba-app-muted)] mb-3 font-semibold tracking-[0.12em] uppercase">
              {t('mainGoals')}
            </p>
            <div className="flex flex-wrap gap-2">
              {GOAL_OPTIONS.map((g) => (
                <button
                  key={g.id}
                  onClick={() => onToggleGoal(g.id)}
                  className={`rounded-full border-2 px-3 py-2 text-xs font-semibold tracking-[0.08em] uppercase transition-all ${
                    selectedGoals.includes(g.id)
                      ? 'bg-[var(--juba-app-green)] text-white border-[var(--juba-app-ink)]'
                      : 'border-[var(--juba-app-line)] text-[var(--juba-app-muted)] hover:border-2 hover:text-[var(--juba-app-green-dark)]'
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
          <div className="border-[var(--juba-app-line)] text-xs text-[var(--juba-app-ink)] space-y-1 border px-4 py-3 font-sans tracking-wide">
            <p>
              {t('summaryLevel')}:{' '}
              <span className="text-[var(--juba-app-ink)] font-bold">{cefr_level}</span>
            </p>
            <p>
              {t('summaryDuration')}:{' '}
              <span className="text-[var(--juba-app-ink)]">
                {t('nWeeks', { count: selected.weeks })}
              </span>
              {' · '}
              <span className="text-[var(--juba-app-ink)]">
                {t('daysPerWeek', { count: selected.daysPerWeek })}
              </span>
            </p>
            <p>
              {t('summaryGoals')}:{' '}
              <span className="text-[var(--juba-app-ink)]">
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

          <div className="flex gap-2">
            <button
              type="button"
              onClick={onBack}
              className="border-[var(--juba-app-line)] text-[var(--juba-app-muted)] hover:border-2 hover:text-[var(--juba-app-green-dark)] flex-1 border py-3 font-sans text-xs tracking-widest uppercase transition-colors"
            >
              ← {tCommon('back')}
            </button>
            <button
              type="button"
              onClick={onConfirm}
              disabled={loading || selectedGoals.length === 0}
              className="bg-[var(--juba-app-green)] text-white hover:bg-[var(--juba-app-green-dark)] flex-[2] py-3 font-sans text-xs font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
            >
              {loading ? t('buildingPlan') : `${t('startMyPlan')} →`}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
