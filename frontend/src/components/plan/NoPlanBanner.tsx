'use client'

import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { BookOpen } from 'lucide-react'

export default function NoPlanBanner() {
  const t = useTranslations('plan')
  const router = useRouter()

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-6 py-16 text-center">
      <div className="rounded-[28px] border-2 border-[var(--juba-learning-border)] bg-[var(--juba-learning-surface)] shadow-[var(--juba-learning-shadow)] w-full max-w-md p-8">
        <span className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-[var(--juba-learning-green-soft)] text-[var(--juba-learning-green-dark)]">
          <BookOpen className="h-6 w-6" aria-hidden="true" />
        </span>

        <p className="mb-2 text-xs font-bold tracking-wide text-[var(--juba-learning-muted)] uppercase">
          {t('noPlanLabel')}
        </p>
        <h2 className="mb-3 text-lg font-bold tracking-tight text-[var(--juba-learning-ink)]">
          {t('noPlanTitle')}
        </h2>
        <p className="mb-6 text-sm leading-relaxed text-[var(--juba-learning-muted)]">
          {t('noPlanDesc')}
        </p>

        <button
          onClick={() => router.push('/assessment')}
          className="rounded-2xl border-2 border-[var(--juba-learning-green-dark)] bg-[var(--juba-learning-green)] px-5 py-3 text-sm font-black text-white shadow-[3px_3px_0_var(--juba-learning-green-dark)] transition-transform hover:-translate-y-0.5 active:translate-y-0 w-full"
        >
          {t('startAssessment')}
        </button>

        <p className="mt-6 text-xs text-[var(--juba-learning-muted)]">
          {t('noPlanHint')}
        </p>
      </div>
    </div>
  )
}
