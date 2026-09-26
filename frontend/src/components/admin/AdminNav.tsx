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
    <div className="juba-admin-nav juba-card rounded-[20px] border border-[rgba(7,7,9,.08)] bg-[#fff] shadow-[0_12px_30px_rgba(43,45,90,.055)] flex flex-wrap items-center gap-1 border p-1.5">
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
                ? 'juba-admin-nav-active bg-[#ededff] text-[#202127] border-l border-[#5862e2]'
                : 'text-[rgba(32,33,39,.52)] hover:bg-[#ededff] hover:text-[#202127] border-l border-transparent'
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
