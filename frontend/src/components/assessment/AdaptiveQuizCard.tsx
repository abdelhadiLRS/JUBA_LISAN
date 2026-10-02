'use client'

import { useTranslations } from 'next-intl'
import type { AssessmentQuestion } from '@/data/types'
import { TargetLanguageText } from '@/components/TargetLanguageText'

interface Props {
  question: AssessmentQuestion
  questionNumber: number
  totalQuestions: number
  onAnswer: (answer: string) => void
  languageCode?: string | null
}

export default function AdaptiveQuizCard({
  question,
  questionNumber,
  totalQuestions,
  onAnswer,
  languageCode,
}: Props) {
  const t = useTranslations('assessment')
  const progress = Math.round((questionNumber / totalQuestions) * 100)

  const skillLabelMap: Record<string, string> = {
    grammar: t('skills.grammar'),
    vocabulary: t('skills.vocabulary'),
    reading: t('skills.reading'),
  }

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center bg-[var(--juba-bg,var(--duo-bg))] p-4 sm:p-6">
      <div className="w-full max-w-2xl overflow-hidden rounded-[12px] border border-[var(--juba-border,var(--duo-line))] bg-[var(--juba-card,var(--duo-card))] shadow-[0_1px_2px_rgba(36,48,32,.025)]">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-[var(--juba-border,var(--duo-line))] bg-[var(--duo-bg)] px-5 py-4 sm:px-6">
          <div className="flex items-center gap-2">
            <span className="text-xs text-[var(--duo-muted)]">●</span>
            <span className="text-xs text-[var(--duo-muted)] font-semibold tracking-[0.12em] uppercase">
              {t('step2', { questionNumber, totalQuestions })}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-[var(--duo-muted)] border-[var(--juba-border,var(--duo-line))] rounded-full border px-2 py-1 font-semibold tracking-[0.12em] uppercase">
              {question.difficulty}
            </span>
            <span className="text-xs text-[var(--duo-muted)] border-[var(--juba-border,var(--duo-line))] rounded-full border px-2 py-1 font-semibold tracking-[0.12em] uppercase">
              {skillLabelMap[question.skill] ?? question.skill}
            </span>
          </div>
        </div>

        {/* Progress bar */}
        <div className="h-1 bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)]">
          <div
            className="h-1 bg-[var(--duo-green)] transition-colors duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Question */}
        <div className="space-y-7 p-6 sm:p-9">
          <TargetLanguageText
            as="p"
            languageCode={languageCode}
            className="text-[var(--duo-ink)]"
          >
            {question.question}
          </TargetLanguageText>

          {/* Options */}
          <div className="space-y-2">
            {question.options.map((option, i) => {
              const labels = ['A', 'B', 'C', 'D']
              return (
                <button
                  key={option}
                  onClick={() => onAnswer(option)}
                  className="flex w-full items-start gap-3 rounded-[12px] border border-[var(--juba-border,var(--duo-line))] bg-[var(--duo-bg)] px-4 py-3 text-left text-[var(--duo-ink)] transition-colors hover:border-[var(--duo-green)] hover:bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] hover:text-[var(--duo-green-dark)] "
                >
                  <span className="text-xs text-[var(--duo-muted)] shrink-0 font-sans">
                    {labels[i]}.
                  </span>
                  <TargetLanguageText languageCode={languageCode}>
                    {option}
                  </TargetLanguageText>
                </button>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
