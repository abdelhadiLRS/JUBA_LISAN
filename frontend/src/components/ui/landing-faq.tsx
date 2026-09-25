'use client'

import { useState } from 'react'
import type { ReactNode } from 'react'
import { useTranslations } from 'next-intl'
import { ChevronDown } from 'lucide-react'

const FAQ_KEYS = [
  'q_start',
  'q_workflow',
  'q_language',
  'q_assessment',
  'q_studyPlan',
  'q_resources',
  'q_flashcards',
  'q_vocabulary',
  'q_tutor',
  'q_voice',
  'q_listening',
  'q_reading',
]

export function LandingFAQ({ dir = 'ltr' }: { dir?: 'ltr' | 'rtl' }) {
  const t = useTranslations('faq')
  const [open, setOpen] = useState<number | null>(0)

  const strong = (chunks: React.ReactNode) => (
    <strong className="font-bold text-[var(--juba-app-ink)]">{chunks}</strong>
  )

  const renderAnswer = (key: string) => {
    const answerKey = `a_${key.replace('q_', '')}`

    if (key === 'q_workflow') {
      const steps = [
        t('workflowStep1'),
        t('workflowStep2'),
        t('workflowStep3'),
        t('workflowStep4'),
        t('workflowStep5'),
        t('workflowStep6'),
      ]
      return (
        <ol className="list-none space-y-2.5">
          {steps.map((step, i) => (
            <li key={i} className="flex items-start gap-3">
              <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-[var(--juba-app-ink)] bg-[var(--juba-app-green-soft)] text-xs font-black text-[var(--juba-app-ink)]">
                {i + 1}
              </span>
              <span className="text-sm font-semibold leading-6 text-[var(--juba-app-ink)]">{step}</span>
            </li>
          ))}
        </ol>
      )
    }

    if (
      [
        'q_start',
        'q_studyPlan',
        'q_resources',
        'q_flashcards',
        'q_vocabulary',
        'q_voice',
        'q_listening',
        'q_reading',
      ].includes(key)
    ) {
      return t.rich(answerKey, { strong })
    }

    return t(answerKey)
  }

  return (
    <div dir={dir} className="mx-auto max-w-4xl space-y-3 px-4">
      {FAQ_KEYS.map((key, i) => {
        const isOpen = open === i
        return (
          <div
            key={key}
            className={`rounded-2xl border-2 border-[var(--juba-app-ink)] bg-white transition-all duration-200 ${
              isOpen
                ? 'shadow-[5px_5px_0_var(--juba-app-ink)] bg-[#fcfbf7]'
                : 'shadow-[3px_3px_0_var(--juba-app-ink)] hover:translate-x-0.5 hover:translate-y-0.5'
            }`}
          >
            <button
              type="button"
              onClick={() => setOpen(isOpen ? null : i)}
              aria-expanded={isOpen}
              className="flex w-full items-center justify-between p-5 text-start font-black text-base text-[var(--juba-app-ink)]"
            >
              <span className="pr-4">{t(key)}</span>
              <span
                className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border-2 border-[var(--juba-app-ink)] bg-[var(--juba-app-green-soft)] transition-transform duration-200 ${
                  isOpen ? 'rotate-180 bg-[var(--juba-app-yellow)]' : ''
                }`}
              >
                <ChevronDown className="h-4 w-4 text-[var(--juba-app-ink)]" />
              </span>
            </button>
            {isOpen && (
              <div className="border-t-2 border-[var(--juba-app-line)] px-5 pt-4 pb-6 text-sm font-medium leading-7 text-[var(--juba-app-muted)] animate-in fade-in duration-150">
                {renderAnswer(key)}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
