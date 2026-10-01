'use client'

import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { BookOpen } from 'lucide-react'

export default function NoPlanBanner() {
  const t = useTranslations('plan')
  const router = useRouter()

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-6 py-16 text-center">
      <div className="w-full max-w-md rounded-[13px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-8 shadow-sm">
        <span className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-[13px] bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] text-[var(--duo-green-dark)]">
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
          className="bg-[var(--duo-green)] hover:bg-[var(--duo-green-dark)] text-white w-full rounded-xl px-5 py-3 text-xs font-bold shadow-[0_3px_0_var(--duo-green-dark)] transition-colors"
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
