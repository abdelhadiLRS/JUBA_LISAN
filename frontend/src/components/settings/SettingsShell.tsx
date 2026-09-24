'use client'

import { type CSSProperties, type ReactNode } from 'react'
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
        <p className="text-[var(--juba-app-muted)] mb-1.5 text-xs font-semibold tracking-wide uppercase">
          {eyebrow}
        </p>
        <h1 className="text-[var(--juba-app-ink)] text-2xl font-bold tracking-tight">
          {title}
        </h1>
        {description && (
          <p className="text-[var(--juba-app-muted)] mt-2 max-w-2xl text-sm leading-relaxed">
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
    <nav className="border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] flex flex-wrap items-center gap-1 rounded-2xl border p-1.5">
      {items.map((item) => {
        const Icon = item.icon
        return (
          <a
            key={item.href}
            href={item.href}
            className="text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] focus:text-[var(--juba-app-ink)] flex min-h-9 items-center gap-2 rounded-xl px-3 py-2 text-xs font-medium transition-colors hover:bg-[#f3f7ef] focus:bg-[#f3f7ef] focus:outline-none focus-visible:ring-2"
            style={
              {
                '--tw-ring-color': 'var(--juba-app-green)',
              } as CSSProperties
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
          <h2 className="text-[var(--juba-app-muted)] text-xs font-semibold tracking-wide uppercase">
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
      className="border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] group block rounded-2xl border p-5 transition-all hover:shadow-[var(0 4px 12px rgba(24,37,27,.05))]"
    >
      <div className="mb-4 flex items-center justify-between gap-3">
        <span
          className="flex h-9 w-9 items-center justify-center rounded-xl"
          style={{
            color: 'var(--juba-app-green)',
            background: 'var(--juba-app-green-soft)',
          }}
        >
          <Icon className="size-4.5" aria-hidden="true" />
        </span>
        <ChevronRight
          className="text-[var(--juba-app-muted)] group-hover:text-[var(--juba-app-muted)] size-5 transition-all group-hover:translate-x-0.5 rtl:rotate-180 rtl:group-hover:-translate-x-0.5"
          aria-hidden="true"
        />
      </div>
      <p className="text-[var(--juba-app-ink)] text-sm font-semibold">{label}</p>
      <p className="text-[var(--juba-app-muted)] mt-1.5 text-xs leading-relaxed">
        {description}
      </p>
    </Link>
  )
}
