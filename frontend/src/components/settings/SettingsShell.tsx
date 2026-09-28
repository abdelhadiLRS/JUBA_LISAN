'use client'

import { type ReactNode } from 'react'
import Link from 'next/link'
import type { LucideIcon } from 'lucide-react'

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
        <p className="text-[var(--duo-muted)] mb-1.5 text-xs font-semibold tracking-wide uppercase">
          {eyebrow}
        </p>
        <h1 className="text-[var(--duo-ink)] text-2xl font-bold tracking-tight">
          {title}
        </h1>
        {description && (
          <p className="text-[var(--duo-muted)] mt-2 max-w-2xl text-sm leading-relaxed">
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
    <nav className="flex flex-wrap items-center gap-1 rounded-[20px] border-2 border-[var(--duo-line)] bg-[var(--duo-card)] p-1.5">
      {items.map((item) => {
        const Icon = item.icon
        return (
          <a
            key={item.href}
            href={item.href}
            className="flex min-h-10 items-center gap-2 rounded-xl px-3 py-2 text-xs font-bold text-[var(--duo-muted)] transition-colors hover:bg-[color-mix(in_srgb,var(--duo-green)_8%,transparent)] hover:text-[var(--duo-ink)] focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-blue)]"
          >
            <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
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
          <h2 className="text-[var(--duo-muted)] text-xs font-semibold tracking-wide uppercase">
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
      className="group block rounded-[20px] border-2 border-[var(--duo-line)] bg-[var(--duo-card)] p-5 transition-all hover:-translate-y-0.5 hover:border-[var(--duo-green)] hover:shadow-[0_4px_0_var(--duo-line)]"
    >
      <div className="mb-4 flex items-center justify-between gap-3">
        <span
          className="flex h-9 w-9 items-center justify-center rounded-xl"
          style={{
            color: 'var(--duo-green-dark)',
            background: 'rgba(88,204,2,.12)',
          }}
        >
          <Icon className="h-[18px] w-[18px]" aria-hidden="true" />
        </span>
        <span className="text-[var(--duo-muted)] transition-transform group-hover:translate-x-0.5 rtl:rotate-180 rtl:group-hover:-translate-x-0.5" aria-hidden="true">→</span>
      </div>
      <p className="text-[var(--duo-ink)] text-sm font-bold">{label}</p>
      <p className="text-[var(--duo-muted)] mt-1.5 text-xs leading-relaxed">
        {description}
      </p>
    </Link>
  )
}
