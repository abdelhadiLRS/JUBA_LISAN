'use client'

import { type ReactNode } from 'react'
import Link from 'next/link'
import { ChevronRight, type LucideIcon } from 'lucide-react'

interface SettingsPageHeaderProps {
  title: string
  eyebrow: string
  description?: string
}

export function SettingsPageHeader({
  title,
  eyebrow,
  description,
}: SettingsPageHeaderProps) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div className="min-w-0">
        <p className="text-fl-muted-3 mb-1.5 text-xs font-semibold tracking-wide uppercase">
          {eyebrow}
        </p>
        <h1 className="text-fl-fg text-2xl font-bold tracking-tight">
          {title}
        </h1>
        {description && (
          <p className="text-fl-muted-3 mt-2 max-w-2xl text-sm leading-relaxed">
            {description}
          </p>
        )}
      </div>
    </div>
  )
}

export function SettingsNav({
  items,
}: {
  items: { href: string; label: string; icon: LucideIcon }[]
}) {
  return (
    <nav className="border-fl-border bg-fl-surface flex flex-wrap items-center gap-1 rounded-2xl border p-1.5">
      {items.map((item) => {
        const Icon = item.icon
        return (
          <a
            key={item.href}
            href={item.href}
            className="text-fl-muted-2 hover:text-fl-fg focus:text-fl-fg flex min-h-9 items-center gap-2 rounded-xl px-3 py-2 text-xs font-medium transition-colors hover:bg-[var(--juba-surface-soft)] focus:bg-[var(--juba-surface-soft)] focus:outline-none focus-visible:ring-2"
            style={
              {
                '--tw-ring-color': 'var(--juba-primary)',
              } as React.CSSProperties
            }
          >
            <Icon className="size-3.5" aria-hidden="true" />
            {item.label}
          </a>
        )
      })}
    </nav>
  )
}

export function SettingsPanel({
  id,
  title,
  children,
}: {
  id?: string
  title?: string
  children: ReactNode
}) {
  return (
    <section id={id} className="scroll-mt-24 space-y-3">
      {title && (
        <div className="px-1">
          <h2 className="text-fl-muted-2 text-xs font-semibold tracking-wide uppercase">
            {title}
          </h2>
        </div>
      )}
      {children}
    </section>
  )
}

export function SettingsActionCard({
  href,
  label,
  description,
  icon: Icon,
}: {
  href: string
  label: string
  description: string
  icon: LucideIcon
}) {
  return (
    <Link
      href={href}
      className="border-fl-border bg-fl-surface hover:border-fl-border group block rounded-2xl border p-5 transition-all hover:shadow-[0_4px_16px_rgba(23,35,27,0.06)]"
    >
      <div className="mb-4 flex items-center justify-between gap-3">
        <span
          className="flex h-9 w-9 items-center justify-center rounded-xl"
          style={{
            color: 'var(--juba-primary)',
            background: 'var(--juba-primary-soft)',
          }}
        >
          <Icon className="size-4.5" aria-hidden="true" />
        </span>
        <ChevronRight
          className="text-fl-muted-4 group-hover:text-fl-muted-2 size-5 transition-all group-hover:translate-x-0.5 rtl:rotate-180 rtl:group-hover:-translate-x-0.5"
          aria-hidden="true"
        />
      </div>
      <p className="text-fl-fg text-sm font-semibold">{label}</p>
      <p className="text-fl-muted-2 mt-1.5 text-xs leading-relaxed">
        {description}
      </p>
    </Link>
  )
}
