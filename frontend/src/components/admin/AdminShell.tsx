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
        <h1 className="juba-admin-title text-[var(--juba-ink,var(--duo-ink))] text-xl font-black tracking-tight">
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
    <div className="juba-admin-panel rounded-[12px] border border-[var(--juba-border)] bg-[var(--juba-card,var(--duo-card))] shadow-sm">
      {(title || meta) && (
        <div className="juba-admin-panel-head border-[var(--juba-border)] flex flex-wrap items-center gap-2 border-b px-5 py-3.5">
          {title && (
            <>
              <span className="juba-admin-kicker-dot" aria-hidden="true">✦</span>
              <span className="juba-admin-panel-title">
                {title}
              </span>
            </>
          )}
          {meta && <div className="ms-auto">{meta}</div>}
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
    <div className="juba-admin-metric rounded-[12px] border border-[#e9eee5] bg-white shadow-sm flex items-center justify-between gap-3 px-4 py-3">
      <div className="min-w-0">
        <p className="juba-admin-metric-label text-[10px] text-[var(--juba-muted,var(--duo-muted))] mb-1 font-sans tracking-widest uppercase">
          {label}
        </p>
        <p className="juba-admin-metric-value text-[var(--juba-ink,var(--duo-ink))] truncate text-lg font-black">{value}</p>
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
    neutral: 'border-[var(--duo-line)] text-[var(--juba-muted,var(--duo-muted))]',
    info: 'border-[color-mix(in_srgb,var(--duo-blue)_40%,transparent)] text-[var(--duo-blue)]',
    success: 'border-[color-mix(in_srgb,var(--juba-green,var(--duo-green))_40%,transparent)] text-[var(--juba-green-dark,var(--duo-green-dark))]',
    warning: 'border-[color-mix(in_srgb,var(--duo-yellow)_40%,transparent)] text-[var(--duo-yellow)]',
    danger: 'border-[color-mix(in_srgb,var(--duo-red)_30%,transparent)] text-[var(--duo-red)]',
  }[tone]

  return (
    <span
      className={`juba-admin-badge text-[10px] inline-flex rounded-[7px] border px-2 py-0.5 font-sans tracking-widest uppercase ${toneClass}`}
    >
      {children}
    </span>
  )
}
