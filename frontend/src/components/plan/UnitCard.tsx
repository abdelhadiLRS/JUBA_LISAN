'use client'

import { type ReactNode } from 'react'
import { useTranslations } from 'next-intl'
import { Check, Circle, Lock, Play, Ribbon, Sparkles } from 'lucide-react'

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
  competency: number
  status: UnitStatus
  onClick: () => void
  onStartLesson?: () => void
}

function StatusBadge({ status, index }: { status: UnitStatus; index: number }): ReactNode {
  const palettes = [
    { bg: 'var(--juba-mint)', fg: 'var(--juba-violet-dark)' },
    { bg: 'var(--juba-sky)', fg: 'var(--juba-violet-dark)' },
    { bg: 'var(--juba-yellow)', fg: 'var(--juba-violet-dark)' },
    { bg: 'var(--juba-lilac)', fg: 'var(--juba-violet-dark)' },
    { bg: '#ffd9d1', fg: 'var(--juba-violet-dark)' },
  ]
  const palette = palettes[index % palettes.length]

  if (status.isLevelTest) {
    return <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-[22px] bg-[var(--juba-lilac)] text-[var(--juba-violet-dark)] shadow-[0_7px_0_#d8ccff]"><Ribbon className="h-7 w-7" /></span>
  }
  if (status.completed) {
    return <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-[22px] bg-[var(--juba-violet)] text-white shadow-[0_7px_0_var(--juba-violet-dark)]"><Check className="h-7 w-7" strokeWidth={3} /></span>
  }
  if (status.active) {
    return <span className="relative flex h-16 w-16 shrink-0 items-center justify-center rounded-[22px] text-[var(--juba-violet-dark)] shadow-[0_7px_0_rgba(79,43,209,.16)]" style={{ background: palette.bg }}><span className="absolute -end-1 -top-1 flex h-6 w-6 items-center justify-center rounded-full bg-white text-[var(--juba-violet)] shadow-sm"><Sparkles className="h-3.5 w-3.5" /></span><Play className="h-7 w-7 fill-current" /></span>
  }
  if (status.locked) {
    return <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-[22px] bg-[#f2eff9] text-[#aaa4b5]"><Lock className="h-5 w-5" /></span>
  }
  return <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-[22px] text-[var(--juba-violet-dark)]" style={{ background: palette.bg }}><Circle className="h-6 w-6" /></span>
}

export default function UnitCard({ title, index, lessonCount, grammarCount, competency, status, onClick, onStartLesson }: Props) {
  const t = useTranslations('plan')
  const tCommon = useTranslations('common')
  const barWidth = Math.round(competency * 100)
  const barColor = status.completed ? 'var(--juba-violet)' : status.active ? 'var(--juba-coral)' : 'var(--juba-sky)'

  return (
    <div className={`juba-ff-unit-card group ${status.locked ? 'juba-ff-unit-locked' : status.active ? 'juba-ff-unit-active' : ''}`}>
      <button
        onClick={onClick}
        disabled={status.locked}
        className={`w-full rounded-[26px] p-5 text-start sm:p-6 ${status.locked ? 'cursor-default' : 'hover:-translate-y-0.5'} transition-transform`}
        aria-label={t('unitAriaLabel', { index: index + 1, title })}
      >
        <div className="flex items-center gap-4">
          <StatusBadge status={status} index={index} />
          <div className="min-w-0 flex-1">
            <div className="mb-1 flex items-center gap-2">
              <span className="juba-ff-unit-index rounded-full px-2.5 py-1 text-[10px] font-black">{String(index + 1).padStart(2, '0')}</span>
              {status.active && <span className="juba-ff-unit-start rounded-full px-2.5 py-1 text-[10px] font-black">{tCommon('start')}</span>}
            </div>
            <h3 className={`juba-ff-unit-title truncate text-lg font-black tracking-tight ${status.locked ? 'juba-ff-unit-title-locked' : ''}`}>{title}</h3>
            <div className="juba-ff-unit-meta mt-1.5 flex flex-wrap items-center gap-2 text-xs font-semibold">
              <span>{t('nLessons', { count: lessonCount })}</span>
              {grammarCount > 0 && <><span aria-hidden="true">•</span><span>{t('nGrammar', { count: grammarCount })}</span></>}
              {status.isLevelTest && <span className="rounded-full bg-[var(--juba-lilac)] px-2 py-0.5 text-[10px] font-black text-[var(--juba-violet-dark)]">{t('levelTestLabel')}</span>}
            </div>
          </div>
          {!status.locked && <div className="juba-ff-unit-percent hidden shrink-0 rounded-full px-3 py-1.5 text-xs font-black sm:block">{barWidth}%</div>}
        </div>
        {!status.locked && <div className="juba-ff-unit-progress mt-5 h-3 overflow-hidden rounded-full"><div className="h-full rounded-full transition-all duration-700" style={{ width: `${barWidth}%`, background: barColor }} /></div>}
      </button>

      {status.active && onStartLesson && (
        <div className="juba-ff-unit-action flex justify-end px-5 pb-5 sm:px-6">
          <button onClick={onStartLesson} className="juba-ff-unit-cta rounded-full px-5 py-2.5 text-xs font-black transition-transform hover:-translate-y-0.5 active:translate-y-1">{tCommon('start')} →</button>
        </div>
      )}
    </div>
  )
}
