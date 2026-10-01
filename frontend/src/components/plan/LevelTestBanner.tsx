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
    <div className="mt-2 overflow-hidden rounded-[13px] border border-[var(--duo-line)] bg-[var(--duo-card)] shadow-sm">
      <div className="flex items-center gap-3 border-b border-[var(--duo-line)] px-5 py-4 sm:px-6">
        <span className="flex h-9 w-9 items-center justify-center rounded-full bg-[var(--duo-yellow)] text-[var(--duo-green-dark)]">
          <Award className="h-4.5 w-4.5" aria-hidden="true" />
        </span>
        <div>
          <p className="text-xs font-bold tracking-wide text-[var(--duo-ink)] uppercase">
            {t('levelComplete', { level })}
          </p>
          <p className="mt-0.5 text-xs text-[var(--duo-muted)]">
            {t('levelCompleteHint')}
          </p>
        </div>
      </div>
      <div className="space-y-4 p-5 sm:p-6">
        <p className="text-sm leading-relaxed text-[var(--duo-muted)]">
          {t('levelCompleteDesc', { level })}
        </p>
        <button
          type="button"
          onClick={() => router.push(`/assessment/level-test?plan=${planId}`)}
          className="bg-[var(--duo-green)] hover:bg-[var(--duo-green-dark)] text-white rounded-xl px-5 py-2.5 text-xs font-bold shadow-[0_3px_0_var(--duo-green-dark)] transition-colors"
        >
          {t('beginLevelTest')} →
        </button>
      </div>
    </div>
  )
}
