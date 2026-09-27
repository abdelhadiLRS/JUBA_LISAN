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
    <div className="rounded-[24px] border-2 border-[var(--juba-learning-border)] bg-[var(--juba-learning-surface)] shadow-[var(--juba-learning-shadow)] mt-2 overflow-hidden">
      <div className="flex items-center gap-3 border-b border-[var(--juba-learning-border)] px-5 py-4 sm:px-6">
        <span className="flex h-9 w-9 items-center justify-center rounded-full bg-[var(--juba-learning-yellow)] text-[var(--juba-learning-green-dark)]">
          <Award className="h-4.5 w-4.5" aria-hidden="true" />
        </span>
        <div>
          <p className="text-xs font-bold tracking-wide text-[var(--juba-learning-ink)] uppercase">
            {t('levelComplete', { level })}
          </p>
          <p className="mt-0.5 text-xs text-[var(--juba-learning-muted)]">
            {t('levelCompleteHint')}
          </p>
        </div>
      </div>
      <div className="space-y-4 p-5 sm:p-6">
        <p className="text-sm leading-relaxed text-[var(--juba-learning-muted)]">
          {t('levelCompleteDesc', { level })}
        </p>
        <button
          type="button"
          onClick={() => router.push(`/assessment/level-test?plan=${planId}`)}
          className="rounded-2xl border-2 border-[var(--juba-learning-green-dark)] bg-[var(--juba-learning-green)] px-5 py-3 text-sm font-black text-white shadow-[3px_3px_0_var(--juba-learning-green-dark)] transition-transform hover:-translate-y-0.5 active:translate-y-0"
        >
          {t('beginLevelTest')} →
        </button>
      </div>
    </div>
  )
}
