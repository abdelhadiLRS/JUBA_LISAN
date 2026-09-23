'use client'

import Link from 'next/link'
import { useTranslations } from 'next-intl'

export default function BillingCanceledPage() {
  const t = useTranslations('billing')

  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--juba-bg)] px-4">
      <div className="border-[var(--juba-border)] bg-[var(--juba-surface)] w-full max-w-sm space-y-5 border-2 border-[var(--juba-border)] p-8 text-center">
        <div className="text-[var(--juba-muted)] text-2xl">△</div>
        <p className="text-[var(--juba-text)] text-[var(--juba-muted)] font-semibold tracking-wide">
          {t('canceledLabel')}
        </p>
        <h1 className="text-[var(--juba-text)] font-sans text-base font-bold">
          {t('canceledTitle')}
        </h1>
        <p className="text-[var(--juba-muted)] font-sans text-xs leading-relaxed">
          {t('canceledDesc')}
        </p>
        <div className="flex flex-col gap-2">
          <Link
            href="/dashboard"
            className="bg-[var(--juba-violet)] text-white hover:bg-[var(--juba-violet)]/90 block py-3 font-sans text-xs font-bold tracking-wide transition-colors"
          >
            {t('canceledCtaDashboard')}
          </Link>
          <Link
            href="/settings"
            className="border-[var(--juba-border)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)] block border py-3 font-sans text-xs tracking-wide transition-colors"
          >
            {t('canceledCtaSettings')}
          </Link>
        </div>
        <p className="text-[var(--juba-muted)] text-[var(--juba-muted)] font-semibold tracking-wide">
          {t('canceledNoCharge')}
        </p>
      </div>
    </div>
  )
}
