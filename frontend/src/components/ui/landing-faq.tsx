'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'

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

export function LandingFAQ() {
  const t = useTranslations('faq')
  const [open, setOpen] = useState<number | null>(null)

  const strong = (chunks: React.ReactNode) => (
    <strong className="font-semibold text-[var(--juba-app-ink)]">{chunks}</strong>
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
        <ol className="list-none space-y-2">
          {steps.map((step, i) => (
            <li key={i} className="flex items-start gap-3">
              <span className="mt-0.5 flex size-5 shrink-0 items-center justify-center rounded-full bg-[var(--juba-app-green-soft)] text-xs font-semibold text-[var(--juba-app-green-dark)]">
                {i + 1}
              </span>
              <span>{step}</span>
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
    <div className="juba-ff-faq overflow-hidden p-0">
      {FAQ_KEYS.map((key, i) => (
        <div
          key={key}
          className={i < FAQ_KEYS.length - 1 ? 'juba-ff-faq-row border-b' : 'juba-ff-faq-row'}
        >
          <button
            onClick={() => setOpen(open === i ? null : i)}
            aria-expanded={open === i}
            className="juba-ff-faq-question flex w-full items-center justify-between px-5 py-4 text-left text-sm transition-colors"
          >
            <span className="juba-ff-faq-question-label pr-4 font-medium">{t(key)}</span>
            <span className="juba-ff-faq-toggle flex size-7 shrink-0 items-center justify-center rounded-full text-sm font-medium">
              {open === i ? '−' : '+'}
            </span>
          </button>
          {open === i && (
            <div className="juba-ff-faq-answer border-t px-5 pt-4 pb-5 text-sm leading-6">
              {renderAnswer(key)}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
