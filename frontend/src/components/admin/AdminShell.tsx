'use client'

import { type ReactNode } from 'react'
import { type LucideIcon } from 'lucide-react'

interface AdminPageHeaderProps {
  title: string
  eyebrow: string
  actions?: ReactNode
}

export function AdminPageHeader({
  title,
  eyebrow,
  actions,
}: AdminPageHeaderProps) {
  return (
    <div className="juba-admin-page-header flex flex-wrap items-center justify-between gap-4">
      <div className="min-w-0">
        <div className="mb-2 flex items-center gap-2">
          <span className="juba-admin-kicker-dot" aria-hidden="true">✦</span>
          <span className="juba-admin-kicker">
            {eyebrow}
          </span>
        </div>
        <h1 className="juba-admin-title text-[var(--juba-app-ink)] text-xl font-black tracking-tight">
          {title}
        </h1>
      </div>
      {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
    </div>
  )
}

export function AdminPanel({
  title,
  meta,
  children,
}: {
  title?: string
  meta?: ReactNode
  children: ReactNode
}) {
  return (
    <div className="juba-admin-panel juba-card border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] border">
      {(title || meta) && (
        <div className="juba-admin-panel-head border-[var(--juba-app-line)] flex flex-wrap items-center gap-2 border-b px-5 py-4">
          {title && (
            <>
              <span className="juba-admin-kicker-dot" aria-hidden="true">✦</span>
              <span className="juba-admin-panel-title">
                {title}
              </span>
            </>
          )}
          {meta && <div className="ml-auto">{meta}</div>}
        </div>
      )}
      {children}
    </div>
  )
}

export function AdminMetric({
  label,
  value,
  icon: Icon,
}: {
  label: string
  value: ReactNode
  icon: LucideIcon
}) {
  return (
    <div className="juba-admin-metric juba-card border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] flex items-center justify-between gap-3 border px-4 py-3">
      <div className="min-w-0">
        <p className="juba-admin-metric-label text-[10px] text-[var(--juba-app-muted)] mb-1 font-sans tracking-widest uppercase">
          {label}
        </p>
        <p className="juba-admin-metric-value text-[var(--juba-app-ink)] truncate text-lg font-black">{value}</p>
      </div>
      <span className="juba-admin-metric-icon"><Icon className="size-5 shrink-0" aria-hidden="true" /></span>
    </div>
  )
}

export function AdminBadge({
  children,
  tone = 'neutral',
}: {
  children: ReactNode
  tone?: 'neutral' | 'info' | 'success' | 'warning' | 'danger'
}) {
  const toneClass = {
    neutral: 'border-[var(--juba-app-line)] text-[var(--juba-app-muted)]',
    info: 'border-blue-500/40 text-blue-400',
    success: 'border-green-500/40 text-green-400',
    warning: 'border-yellow-500/40 text-yellow-400',
    danger: 'border-red-500/30 text-[var(--juba-app-error)]',
  }[tone]

  return (
    <span
      className={`juba-admin-badge text-[10px] inline-flex border px-2 py-0.5 font-sans tracking-widest uppercase ${toneClass}`}
    >
      {children}
    </span>
  )
}
