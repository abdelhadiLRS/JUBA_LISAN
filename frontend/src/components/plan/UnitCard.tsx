'use client'

import { type ReactNode } from 'react'
import { useTranslations } from 'next-intl'
import { Check, Circle, Lock, Play, Ribbon, Sparkles } from 'lucide-react'

interface UnitStatus { completed: boolean; active: boolean; locked: boolean; isLevelTest: boolean }
interface Props { title: string; index: number; lessonCount: number; grammarCount: number; competency: number; status: UnitStatus; onClick: () => void; onStartLesson?: () => void }

function StatusBadge({ status, index }: { status: UnitStatus; index: number }): ReactNode {
  const palettes = [
    { bg: 'color-mix(in_srgb,var(--juba-green)_10%,transparent)', fg: 'var(--juba-green-dark)' },
    { bg: 'color-mix(in_srgb,var(--juba-green)_10%,transparent)', fg: 'var(--juba-green-dark)' },
    { bg: 'var(--juba-yellow)', fg: 'var(--juba-green-dark)' },
    { bg: 'color-mix(in_srgb,var(--juba-green)_10%,transparent)', fg: 'var(--juba-green-dark)' },
    { bg: 'color-mix(in_srgb,var(--juba-red)_12%,transparent)', fg: 'var(--juba-green-dark)' },
  ]
  const palette = palettes[index % palettes.length]
  if (status.isLevelTest) return <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-[12px] border border-[var(--juba-border,var(--duo-line))] bg-[color-mix(in_srgb,var(--juba-green)_10%,transparent)] text-[var(--juba-green-dark)]"><Ribbon className="h-6 w-6" /></span>
  if (status.completed) return <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-[12px] bg-[var(--juba-green)] text-white shadow-[0_1px_2px_rgba(36,48,32,.025)]"><Check className="h-6 w-6" strokeWidth={3} /></span>
  if (status.active) return <span className="relative flex h-14 w-14 shrink-0 items-center justify-center rounded-[12px] border border-[var(--juba-border,var(--duo-line))] text-[var(--juba-green-dark)] shadow-[0_1px_2px_rgba(36,48,32,.025)]" style={{ background: palette.bg }}><span className="absolute -end-1 -top-1 flex h-6 w-6 items-center justify-center rounded-full border border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-card,var(--duo-card))] text-[var(--juba-green)] shadow-[0_1px_2px_rgba(36,48,32,.025)]"><Sparkles className="h-3.5 w-3.5" /></span><Play className="h-6 w-6 fill-current" /></span>
  if (status.locked) return <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-[12px] border border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-bg,var(--duo-bg))] text-[var(--juba-muted,var(--duo-muted))]"><Lock className="h-5 w-5" /></span>
  return <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-[12px] border border-[var(--juba-border,var(--duo-line))] text-[var(--juba-green-dark)]" style={{ background: palette.bg }}><Circle className="h-5 w-5" /></span>
}

export default function UnitCard({ title, index, lessonCount, grammarCount, competency, status, onClick, onStartLesson }: Props) {
  const t = useTranslations('plan'); const tCommon = useTranslations('common'); const barWidth = Math.round(competency * 100)
  const barColor = status.completed ? 'var(--juba-green)' : status.active ? 'var(--juba-yellow)' : 'color-mix(in_srgb,var(--juba-green)_10%,transparent)'
  return (<div className={`juba-ff-unit-card group overflow-hidden rounded-[12px] border border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-card,var(--duo-card))] shadow-[0_1px_2px_rgba(36,48,32,.025)] transition-shadow hover:shadow-[0_4px_12px_rgba(36,48,32,.06)] ${status.locked ? 'juba-ff-unit-locked' : status.active ? 'juba-ff-unit-active' : ''}`}>
    <button onClick={onClick} disabled={status.locked} className={`w-full rounded-none p-5 text-start transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-green)] focus-visible:ring-inset sm:p-6 ${status.locked ? 'cursor-default' : ''}`} aria-label={t('unitAriaLabel', { index: index + 1, title })}>
      <div className="flex items-center gap-4"><StatusBadge status={status} index={index} /><div className="min-w-0 flex-1"><div className="mb-1 flex items-center gap-2"><span className="juba-ff-unit-index rounded-full px-2.5 py-1 text-[10px] font-black">{String(index + 1).padStart(2, '0')}</span>{status.active && <span className="juba-ff-unit-start rounded-full px-2.5 py-1 text-[10px] font-black">{tCommon('start')}</span>}</div><h3 className={`juba-ff-unit-title truncate text-lg font-black tracking-tight ${status.locked ? 'juba-ff-unit-title-locked' : ''}`}>{title}</h3><div className="juba-ff-unit-meta mt-1.5 flex flex-wrap items-center gap-2 text-xs font-semibold"><span>{t('nLessons', { count: lessonCount })}</span>{grammarCount > 0 && <><span aria-hidden="true">•</span><span>{t('nGrammar', { count: grammarCount })}</span></>}{status.isLevelTest && <span className="rounded-full bg-[color-mix(in_srgb,var(--juba-green)_10%,transparent)] px-2 py-0.5 text-[10px] font-black text-[var(--juba-green-dark)]">{t('levelTestLabel')}</span>}</div></div>{!status.locked && <div className="juba-ff-unit-percent hidden shrink-0 rounded-full px-3 py-1.5 text-xs font-black sm:block">{barWidth}%</div>}</div>
      {!status.locked && <div className="juba-ff-unit-progress mt-5 h-2 overflow-hidden rounded-full"><div className="h-full rounded-full transition-colors duration-700" style={{ width: `${barWidth}%`, background: barColor }} /></div>}
    </button>
    {status.active && onStartLesson && <div className="juba-ff-unit-action flex justify-end px-5 pb-5 sm:px-6"><button onClick={onStartLesson} className="rounded-full bg-[var(--juba-green)] px-5 py-2.5 text-xs font-bold text-white shadow-[0_1px_2px_rgba(36,48,32,.025)] transition-colors hover:bg-[var(--juba-green-dark)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-green)] focus-visible:ring-offset-2">{tCommon('start')} →</button></div>}
  </div>)
}
