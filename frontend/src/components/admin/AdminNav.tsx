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
    <div className="juba-admin-nav juba-card border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] flex flex-wrap items-center gap-1 border p-1.5">
      {items.map((item) => {
        const Icon = item.icon
        const active =
          pathname === item.href ||
          (item.href !== '/admin' && pathname.startsWith(`${item.href}/`))
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`juba-admin-nav-item text-[10px] flex min-h-9 items-center gap-2 px-3 py-2 font-semibold transition-colors ${
              active
                ? 'juba-admin-nav-active bg-[var(--juba-app-green-soft)] text-[var(--juba-app-ink)] border-l-2 border-[var(--juba-app-green)]'
                : 'text-[var(--juba-app-muted)] hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-ink)] border-l-2 border-transparent'
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
