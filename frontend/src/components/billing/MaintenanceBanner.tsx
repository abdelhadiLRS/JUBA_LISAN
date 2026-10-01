'use client'

import { useTranslations } from 'next-intl'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { Wrench } from 'lucide-react'

export function MaintenanceBanner() {
  const t = useTranslations('maintenance')

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-6 py-16 text-center">
      <div className="w-full max-w-md rounded-[10px] border border-[var(--duo-yellow)] bg-[var(--duo-card)] p-8 shadow-sm">
        <div className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-[10px] border border-[var(--duo-ink)] bg-[var(--duo-yellow)] shadow-sm"><Wrench className="h-5 w-5" aria-hidden="true" /></div>

        <p className="mb-3 inline-flex items-center rounded-full border border-[var(--duo-line)] bg-[color-mix(in_srgb,var(--duo-yellow)_14%,transparent)] px-3 py-1 text-xs font-extrabold uppercase tracking-[.12em] text-[var(--duo-ink)]">
          {t('label')}
        </p>
        <h2 className="text-[var(--duo-ink)] mb-3 font-sans text-xl font-black tracking-tight">
          {t('title')}
        </h2>
        <p className="text-[var(--duo-muted)] font-sans text-sm leading-6">
          {t('description')}
        </p>
      </div>
    </div>
  )
}

/** Gate that renders a maintenance banner when maintenance mode is active. */
export function MaintenanceGate({ children }: { children: React.ReactNode }) {
  const maintenanceMode = useConfigStore((s) => s.maintenanceMode)
  const isAdmin = useAuthStore((s) => s.user?.role === 'admin')

  if (maintenanceMode && !isAdmin) return <MaintenanceBanner />
  return <>{children}</>
}
