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
    <div className="flex min-h-[60vh] items-center justify-center bg-[#f4f4f2] p-4 sm:p-6">
      <div className="w-full max-w-2xl overflow-hidden rounded-[26px] border border-[rgba(7,7,9,.08)] bg-white shadow-[0_12px_30px_rgba(43,45,90,.055)]">
        <div className="flex items-center gap-3 border-b border-[rgba(7,7,9,.07)] bg-[#f4f4f2] px-6 py-4">
          <span className="text-xs text-[rgba(32,33,39,.52)]">●</span>
          <span className="text-xs text-[rgba(32,33,39,.52)] font-semibold tracking-[0.12em] uppercase">
            {t('step3')}
          </span>
        </div>

        <div className="space-y-8 p-6 sm:p-8">
          {/* Duration */}
          <div>
            <p className="text-xs text-[rgba(32,33,39,.52)] mb-3 font-semibold tracking-[0.12em] uppercase">
              {t('howManyWeeks', { cefr_level })}
            </p>
            <div className="grid grid-cols-2 gap-3">
              {DURATION_OPTIONS.map((opt) => (
                <button
                  type="button"
                  key={opt.weeks}
                  onClick={() => onSelectDuration(opt)}
                  className={`rounded-[20px] border-2 px-4 py-4 text-left transition-all ${
                    selectedWeeks === opt.weeks
                      ? 'bg-[#5862e2] text-white border-[#5862e2] shadow-[0_8px_20px_rgba(88,98,226,.16)]'
                      : 'border-[rgba(7,7,9,.08)] bg-[#f4f4f2] text-[#202127] hover:border-[#5862e2] hover:bg-[#ededff] hover:text-[#373fb8]'
                  }`}
                >
                  <p className="font-sans text-xs font-bold tracking-widest uppercase">
                    {t('nWeeks', { count: opt.weeks })}
                  </p>
                  <p
                    className={`text-[rgba(32,33,39,.52)] mt-0.5 font-sans ${
                      selectedWeeks === opt.weeks
                        ? 'opacity-70'
                        : 'text-[rgba(32,33,39,.52)]'
                    }`}
                  >
                    {intensityMap[opt.intensity]} ·{' '}
                    {t('approxLessons', { count: opt.weeks * opt.daysPerWeek })}
                  </p>
                  <p
                    className={`text-[rgba(32,33,39,.52)] mt-0.5 font-sans ${
                      selectedWeeks === opt.weeks
                        ? 'opacity-60'
                        : 'text-[rgba(32,33,39,.52)]'
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
            <p className="text-xs text-[rgba(32,33,39,.52)] mb-3 font-semibold tracking-[0.12em] uppercase">
              {t('mainGoals')}
            </p>
            <div className="flex flex-wrap gap-2">
              {GOAL_OPTIONS.map((g) => (
                <button
                  type="button"
                  key={g.id}
                  onClick={() => onToggleGoal(g.id)}
                  className={`rounded-full border-2 px-3 py-2 text-xs font-semibold tracking-[0.08em] uppercase transition-all ${
                    selectedGoals.includes(g.id)
                      ? 'bg-[#5862e2] text-white border-[#5862e2] shadow-[0_6px_14px_rgba(88,98,226,.14)]'
                      : 'border-[rgba(7,7,9,.08)] bg-[#f4f4f2] text-[#202127] hover:border-[#5862e2] hover:bg-[#ededff] hover:text-[#373fb8]'
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
          <div className="space-y-1 rounded-[18px] border border-[rgba(7,7,9,.08)] bg-[#f4f4f2] px-4 py-3 text-xs tracking-wide text-[#202127]">
            <p>
              {t('summaryLevel')}:{' '}
              <span className="text-[#202127] font-bold">{cefr_level}</span>
            </p>
            <p>
              {t('summaryDuration')}:{' '}
              <span className="text-[#202127]">
                {t('nWeeks', { count: selected.weeks })}
              </span>
              {' · '}
              <span className="text-[#202127]">
                {t('daysPerWeek', { count: selected.daysPerWeek })}
              </span>
            </p>
            <p>
              {t('summaryGoals')}:{' '}
              <span className="text-[#202127]">
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
              className="rounded-[18px] border-2 border-[#b33a32]/30 bg-[#b33a32]/10 px-4 py-3 text-left text-xs leading-relaxed text-[#b33a32]"
            >
              ✕ {error}
            </div>
          )}

          <div className="flex gap-2">
            <button
              type="button"
              onClick={onBack}
              className="border-[rgba(7,7,9,.08)] text-[rgba(32,33,39,.52)] hover:border-[rgba(7,7,9,.14)] hover:bg-[#ededff] hover:text-[#373fb8] flex-1 rounded-[14px] border py-3 font-sans text-xs tracking-widest uppercase transition-colors"
            >
              ← {tCommon('back')}
            </button>
            <button
              type="button"
              onClick={onConfirm}
              disabled={loading || selectedGoals.length === 0}
              className="bg-[#5862e2] text-white hover:bg-[#373fb8] flex-[2] rounded-[14px] py-3 font-sans text-xs font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
            >
              {loading ? t('buildingPlan') : `${t('startMyPlan')} →`}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
