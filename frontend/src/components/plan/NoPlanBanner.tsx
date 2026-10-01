'use client'

import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { BookOpen } from 'lucide-react'

export default function NoPlanBanner() {
  const t = useTranslations('plan')
  const router = useRouter()

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-6 py-16 text-center">
      <div className="w-full max-w-md rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-8 shadow-sm">
        <span className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-[10px] bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] text-[var(--duo-green-dark)]">
          <BookOpen className="h-6 w-6" aria-hidden="true" />
        </span>

        <p className="mb-2 text-xs font-bold tracking-wide text-[var(--duo-muted)] uppercase">
          {t('noPlanLabel')}
        </p>
        <h2 className="mb-3 text-lg font-bold tracking-tight text-[var(--duo-ink)]">
          {t('noPlanTitle')}
        </h2>
        <p className="mb-6 text-sm leading-relaxed text-[var(--duo-muted)]">
          {t('noPlanDesc')}
        </p>

        <button
          onClick={() => router.push('/assessment')}
          className="w-full rounded-[10px] border border-[var(--duo-green-dark)] bg-[var(--duo-green)] px-5 py-3 text-xs font-bold text-white shadow-sm transition-colors hover:bg-[var(--duo-green-dark)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-green)] focus-visible:ring-offset-2"
        >
          {t('startAssessment')}
        </button>

        <p className="mt-6 text-xs text-[var(--duo-muted)]">
          {t('noPlanHint')}
        </p>
      </div>
    </div>
  )
}
