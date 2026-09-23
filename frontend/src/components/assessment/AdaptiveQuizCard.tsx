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
    <div className="flex min-h-[60vh] flex-col items-center justify-center p-4 sm:p-6">
      <div className="w-full max-w-2xl overflow-hidden rounded-[30px] border-2 border-[var(--juba-lilac)] bg-white shadow-[0_22px_55px_rgba(61,42,130,0.12)]">
        {/* Header */}
        <div className="flex items-center justify-between border-b-2 border-[var(--juba-lilac)] bg-[var(--juba-lilac)]/40 px-5 py-4 sm:px-6">
          <div className="flex items-center gap-2">
            <span className="text-xs text-[var(--juba-muted)]">●</span>
            <span className="text-xs text-[var(--juba-muted)] font-semibold tracking-[0.12em] uppercase">
              {t('step2', { questionNumber, totalQuestions })}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-[var(--juba-muted)] border-[var(--juba-border)] border px-2 py-1 font-semibold tracking-[0.12em] uppercase">
              {question.difficulty}
            </span>
            <span className="text-xs text-[var(--juba-muted)] border-[var(--juba-border)] border px-2 py-1 font-semibold tracking-[0.12em] uppercase">
              {skillLabelMap[question.skill] ?? question.skill}
            </span>
          </div>
        </div>

        {/* Progress bar */}
        <div className="bg-[var(--juba-lilac)] h-1">
          <div
            className="bg-[var(--juba-violet)] h-1 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Question */}
        <div className="space-y-7 p-6 sm:p-9">
          <TargetLanguageText
            as="p"
            languageCode={languageCode}
            className="text-fl-fg"
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
                  className="border-[var(--juba-border)] text-[var(--juba-text)] hover:border-[var(--juba-border)]-2 hover:text-fl-fg hover:bg-fl-surface-2 flex w-full items-start gap-3 border px-4 py-3 text-left transition-colors"
                >
                  <span className="text-xs text-[var(--juba-muted)] shrink-0 font-mono">
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
