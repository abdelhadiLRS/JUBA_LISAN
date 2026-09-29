'use client'

import { useState } from 'react'
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
    <strong className="font-bold text-[var(--busuu-ink)]">{chunks}</strong>
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
              <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-[var(--busuu-line)] bg-[var(--busuu-soft)] text-xs font-black text-[var(--busuu-ink)]">
                {i + 1}
              </span>
              <span className="text-sm font-semibold leading-6 text-[var(--busuu-ink)]">{step}</span>
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
    <div dir={dir} className="mx-auto max-w-4xl">
      {FAQ_KEYS.map((key, i) => {
        const isOpen = open === i
        return (
          <div
            key={key}
            className={`juba-landing-faq-item ${isOpen ? 'is-open' : ''}`}
          >
            <button
              type="button"
              onClick={() => setOpen(isOpen ? null : i)}
              aria-expanded={isOpen}
              aria-controls={`landing-faq-answer-${key}`}
              id={`landing-faq-question-${key}`}
              className="juba-landing-faq-question flex w-full items-center justify-between p-5 text-start font-black text-base"
            >
              <span className="pe-4">{t(key)}</span>
              <span
                className={`juba-landing-faq-icon flex h-8 w-8 shrink-0 items-center justify-center transition-transform duration-200 ${
                  isOpen ? 'rotate-180' : ''
                }`}
              >
                <ChevronDown className="h-4 w-4 text-[var(--busuu-ink)]" />
              </span>
            </button>
            <div
              id={`landing-faq-answer-${key}`}
              role="region"
              aria-labelledby={`landing-faq-question-${key}`}
              hidden={!isOpen}
              className="juba-landing-faq-answer border-t px-5 pt-4 pb-6 text-sm font-medium leading-7 animate-in fade-in duration-150"
            >
              {renderAnswer(key)}
            </div>
          </div>
        )
      })}
    </div>
  )
}
