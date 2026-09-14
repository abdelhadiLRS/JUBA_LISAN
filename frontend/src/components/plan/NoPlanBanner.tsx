'use client'

import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { BookOpen } from 'lucide-react'

export default function NoPlanBanner() {
  const t = useTranslations('plan')
  const router = useRouter()

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-6 py-16 text-center">
      <div className="juba-card w-full max-w-md p-8">
        <span className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-[var(--juba-primary-soft)] text-[var(--juba-primary-dark)]">
          <BookOpen className="h-6 w-6" aria-hidden="true" />
        </span>

        <p className="mb-2 text-xs font-bold tracking-wide text-[var(--juba-muted)] uppercase">
          {t('noPlanLabel')}
        </p>
        <h2 className="mb-3 text-lg font-bold tracking-tight text-[var(--juba-text)]">
          {t('noPlanTitle')}
        </h2>
        <p className="mb-6 text-sm leading-relaxed text-[var(--juba-muted)]">
          {t('noPlanDesc')}
        </p>

        <button
          onClick={() => router.push('/assessment')}
          className="w-full rounded-xl bg-[var(--juba-primary)] px-4 py-3 text-xs font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-dark)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-primary)] focus-visible:ring-offset-2"
        >
          {t('startAssessment')}
        </button>

        <p className="mt-6 text-xs text-[var(--juba-muted)]">
          {t('noPlanHint')}
        </p>
      </div>
    </div>
  )
}
