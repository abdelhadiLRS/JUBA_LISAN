'use client'

import { useTranslations } from 'next-intl'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { Wrench } from 'lucide-react'

export function MaintenanceBanner() {
  const t = useTranslations('maintenance')

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-6 py-16 text-center">
      <div className="w-full max-w-md juba-card border-2 border-[var(--juba-app-yellow)] bg-[var(--juba-app-surface)] p-8 shadow-[5px_5px_0_rgba(24,37,27,.12)]">
        <div className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-2xl border-2 border-[var(--juba-app-ink)] bg-[var(--juba-app-yellow)] shadow-[3px_3px_0_var(--juba-app-ink)]"><Wrench className="h-5 w-5" aria-hidden="true" /></div>

        <p className="juba-badge mb-3">
          {t('label')}
        </p>
        <h2 className="text-[var(--juba-app-ink)] mb-3 font-sans text-xl font-black tracking-tight">
          {t('title')}
        </h2>
        <p className="text-[var(--juba-app-muted)] font-sans text-sm leading-6">
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
