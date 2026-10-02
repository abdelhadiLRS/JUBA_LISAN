'use client'

import { type ReactNode } from 'react'
import Link from 'next/link'
import type { LucideIcon } from 'lucide-react'

interface SettingsPageHeaderProps { title: string; eyebrow: string; description?: string }

export function SettingsPageHeader({ title, eyebrow, description }: SettingsPageHeaderProps) {
  return <div className="flex flex-wrap items-end justify-between gap-4"><div className="min-w-0"><p className="mb-1.5 text-[10px] font-bold uppercase tracking-[0.12em] text-[var(--duo-green-dark)]">{eyebrow}</p><h1 className="text-2xl font-extrabold tracking-tight text-[var(--duo-ink)]">{title}</h1>{description && <p className="mt-2 max-w-2xl text-sm leading-relaxed text-[var(--duo-muted)]">{description}</p>}</div></div>
}

export function SettingsNav({ items }: { items: { href: string; label: string; icon: LucideIcon }[] }) {
  return <nav className="flex flex-wrap items-center gap-1 rounded-[12px] border border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-card,var(--duo-card))] p-1.5 shadow-sm">
    {items.map((item) => { const Icon = item.icon; return <a key={item.href} href={item.href} className="flex min-h-9 items-center gap-2 rounded-[10px] px-3 py-2 text-xs font-bold text-[var(--duo-muted)] transition-colors hover:bg-[color-mix(in_srgb,var(--duo-green)_8%,transparent)] hover:text-[var(--duo-ink)] focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-green)]"><Icon className="h-4 w-4 shrink-0" aria-hidden="true" />{item.label}</a> })}
  </nav>
}

export function SettingsPanel({ id, title, children }: { id?: string; title?: string; children: ReactNode }) {
  return <section id={id} className="scroll-mt-24 space-y-3">{title && <div className="px-1"><h2 className="text-[10px] font-bold uppercase tracking-[0.12em] text-[var(--duo-muted)]">{title}</h2></div>}{children}</section>
}

export function SettingsActionCard({ href, label, description, icon: Icon }: { href: string; label: string; description: string; icon: LucideIcon }) {
  return <Link href={href} className="group block rounded-[10px] border border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-card,var(--duo-card))] p-5 shadow-sm transition-colors hover:border-[var(--duo-green)]">
    <div className="mb-4 flex items-center justify-between gap-3"><span className="flex h-9 w-9 items-center justify-center rounded-[10px] bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] text-[var(--duo-green-dark)]"><Icon className="h-[18px] w-[18px]" aria-hidden="true" /></span><span className="text-[var(--duo-muted)] transition-colors group-hover:text-[var(--duo-green-dark)] rtl:rotate-180 rtl:group-hover:-translate-x-0.5" aria-hidden="true">→</span></div>
    <p className="text-sm font-bold text-[var(--duo-ink)]">{label}</p><p className="mt-1.5 text-xs leading-relaxed text-[var(--duo-muted)]">{description}</p>
  </Link>
}
