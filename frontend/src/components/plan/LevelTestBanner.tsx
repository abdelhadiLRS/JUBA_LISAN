'use client'

import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { Award } from 'lucide-react'

interface Props {
  planId: number
  level: string
}

export default function LevelTestBanner({ planId, level }: Props) {
  const t = useTranslations('plan')
  const router = useRouter()

  return (
    <div className="juba-card mt-2 overflow-hidden">
      <div className="flex items-center gap-3 border-b border-[var(--juba-border-soft)] px-5 py-4 sm:px-6">
        <span className="flex h-9 w-9 items-center justify-center rounded-full bg-[var(--juba-warm-soft)] text-[var(--juba-primary-dark)]">
          <Award className="h-4.5 w-4.5" aria-hidden="true" />
        </span>
        <div>
          <p className="text-xs font-bold tracking-wide text-[var(--juba-text)] uppercase">
            {t('levelComplete', { level })}
          </p>
          <p className="mt-0.5 text-xs text-[var(--juba-muted)]">
            {t('levelCompleteHint')}
          </p>
        </div>
      </div>
      <div className="space-y-4 p-5 sm:p-6">
        <p className="text-sm leading-relaxed text-[var(--juba-muted)]">
          {t('levelCompleteDesc', { level })}
        </p>
        <button
          onClick={() => router.push(`/assessment/level-test?plan=${planId}`)}
          className="rounded-xl bg-[var(--juba-primary)] px-5 py-3 text-xs font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-dark)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-primary)] focus-visible:ring-offset-2"
        >
          {t('beginLevelTest')} →
        </button>
      </div>
    </div>
  )
}
