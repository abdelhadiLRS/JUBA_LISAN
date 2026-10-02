'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useTranslations } from 'next-intl'
import {
  LayoutDashboard,
  MessageSquareText,
  Settings,
  Star,
  Users,
} from 'lucide-react'

const items = [
  { href: '/admin', key: 'overview', icon: LayoutDashboard },
  { href: '/admin/users', key: 'users', icon: Users },
  { href: '/admin/feedback', key: 'feedback', icon: MessageSquareText },
  { href: '/admin/reviews', key: 'reviews', icon: Star },
  { href: '/admin/system', key: 'system', icon: Settings },
] as const

export function AdminNav() {
  const pathname = usePathname()
  const t = useTranslations('admin')

  return (
    <div className="juba-admin-nav flex flex-wrap items-center gap-1 rounded-[12px] border border-[var(--juba-border)] bg-[var(--juba-card,var(--duo-card))] p-1.5 shadow-sm">
      {items.map((item) => {
        const Icon = item.icon
        const active =
          pathname === item.href ||
          (item.href !== '/admin' && pathname.startsWith(`${item.href}/`))
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`juba-admin-nav-item text-[10px] flex min-h-9 items-center gap-2 rounded-[9px] px-3 py-2 font-semibold transition-colors ${
              active
                ? 'juba-admin-nav-active bg-[var(--juba-soft,var(--duo-soft))] text-[var(--juba-ink,var(--duo-ink))] border-s-2 border-[var(--juba-green,var(--duo-green))]'
                : 'text-[var(--juba-muted,var(--duo-muted))] hover:bg-[var(--juba-soft,var(--duo-soft))] hover:text-[var(--juba-ink,var(--duo-ink))] border-s-2 border-transparent'
            }`}
          >
            <Icon className="size-3.5" aria-hidden="true" />
            {t(item.key)}
          </Link>
        )
      })}
    </div>
  )
}
