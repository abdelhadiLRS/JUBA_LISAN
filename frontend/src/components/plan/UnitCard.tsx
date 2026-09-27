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
    { bg: 'var(--juba-learning-green-soft)', fg: 'var(--juba-learning-green-dark)' },
    { bg: 'var(--juba-learning-green-soft)', fg: 'var(--juba-learning-green-dark)' },
    { bg: '#fff8df', fg: '#9a6700' },
    { bg: 'var(--juba-learning-green-soft)', fg: 'var(--juba-learning-green-dark)' },
    { bg: '#fff0ed', fg: '#b42318' },
  ]
  const palette = palettes[index % palettes.length]

  if (status.isLevelTest) {
    return <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border-2 border-[var(--juba-learning-border)] bg-[var(--juba-learning-green-soft)] text-[var(--juba-learning-green-dark)] shadow-[0_4px_0_rgba(0,0,0,.06)]"><Ribbon className="h-7 w-7" /></span>
  }
  if (status.completed) {
    return <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border-2 border-[var(--juba-learning-green-dark)] bg-[var(--juba-learning-green)] text-white shadow-[0_5px_0_var(--juba-learning-green-dark)]"><Check className="h-7 w-7" strokeWidth={3} /></span>
  }
  if (status.active) {
    return <span className="relative flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border-2 border-[var(--juba-learning-border)] text-[var(--juba-learning-green-dark)] shadow-[0_4px_0_rgba(0,0,0,.06)]" style={{ background: palette.bg }}><span className="absolute -end-1 -top-1 flex h-6 w-6 items-center justify-center rounded-full border-2 border-[var(--juba-learning-border)] bg-white text-[var(--juba-learning-green)] shadow-sm"><Sparkles className="h-3.5 w-3.5" /></span><Play className="h-7 w-7 fill-current" /></span>
  }
  if (status.locked) {
    return <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border-2 border-[var(--juba-learning-border)] bg-[#f1f3f0] text-[#7c877f]"><Lock className="h-5 w-5" /></span>
  }
  return <span className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border-2 border-[var(--juba-learning-border)] text-[var(--juba-learning-green-dark)]" style={{ background: palette.bg }}><Circle className="h-6 w-6" /></span>
}

export default function UnitCard({ title, index, lessonCount, grammarCount, competency, status, onClick, onStartLesson }: Props) {
  const t = useTranslations('plan')
  const tCommon = useTranslations('common')
  const barWidth = Math.max(0, Math.min(100, Math.round(competency * 100)))
  const barColor = status.completed ? 'var(--juba-learning-green)' : status.active ? 'var(--juba-learning-yellow)' : 'var(--juba-learning-green-soft)'

  return (
    <div className="overflow-hidden rounded-[20px] border-2 border-[var(--juba-learning-border)] bg-white shadow-[var(--juba-learning-shadow)]">
      <button
        onClick={onClick}
        disabled={status.locked}
        className="group w-full p-5 text-start transition-transform sm:p-6 enabled:hover:-translate-y-0.5 disabled:cursor-default disabled:opacity-80"
        aria-label={t('unitAriaLabel', { index: index + 1, title })}
      >
        <div className="flex items-center gap-4">
          <StatusBadge status={status} index={index} />
          <div className="min-w-0 flex-1">
            <div className="mb-1 flex items-center gap-2">
              <span className="rounded-full border border-[var(--juba-learning-border)] bg-[#f8f8f8] px-2.5 py-1 text-[10px] font-black text-[var(--juba-learning-muted)]">{String(index + 1).padStart(2, '0')}</span>
              {status.active && <span className="rounded-full bg-[var(--juba-learning-green-soft)] px-2.5 py-1 text-[10px] font-black text-[var(--juba-learning-green-dark)]">{tCommon('start')}</span>}
            </div>
            <h3 className="truncate text-lg font-black tracking-tight text-[var(--juba-learning-ink)]">{title}</h3>
            <div className="mt-1.5 flex flex-wrap items-center gap-2 text-xs font-semibold text-[var(--juba-learning-muted)]">
              <span>{t('nLessons', { count: lessonCount })}</span>
              {grammarCount > 0 && <><span aria-hidden="true">•</span><span>{t('nGrammar', { count: grammarCount })}</span></>}
              {status.isLevelTest && <span className="rounded-full bg-[var(--juba-learning-green-soft)] px-2 py-0.5 text-[10px] font-black text-[var(--juba-learning-green-dark)]">{t('levelTestLabel')}</span>}
            </div>
          </div>
          {!status.locked && <div className="hidden shrink-0 rounded-full bg-[var(--juba-learning-green-soft)] px-3 py-1.5 text-xs font-black text-[var(--juba-learning-green-dark)] sm:block">{barWidth}%</div>}
        </div>
        {!status.locked && <div className="mt-5 h-3 overflow-hidden rounded-full border-2 border-[var(--juba-learning-border)] bg-[#f1f1f1]"><div className="h-full rounded-full transition-all duration-700" style={{ width: `${barWidth}%`, background: barColor }} /></div>}
      </button>

      {status.active && onStartLesson && (
        <div className="flex justify-end border-t-2 border-[var(--juba-learning-border)] bg-[#fcfcfc] px-5 py-4 sm:px-6">
          <button onClick={onStartLesson} className="min-h-11 rounded-[13px] border-2 border-[var(--juba-learning-green-dark)] bg-[var(--juba-learning-green)] px-5 py-2.5 text-xs font-black text-white shadow-[0_4px_0_var(--juba-learning-green-dark)] transition-transform hover:translate-y-0.5">{tCommon('start')} →</button>
        </div>
      )}
    </div>
  )
}
