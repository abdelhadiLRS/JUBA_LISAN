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
      <div className="w-full max-w-2xl overflow-hidden rounded-[26px] border-2 border-[var(--juba-app-green-soft)] bg-white shadow-[8px_8px_0_var(--juba-app-ink)]">
        {/* Header */}
        <div className="flex items-center justify-between border-b-2 border-[var(--juba-app-green-soft)] bg-[var(--juba-app-green-soft)]/40 px-5 py-4 sm:px-6">
          <div className="flex items-center gap-2">
            <span className="text-xs text-[var(--juba-app-muted)]">●</span>
            <span className="text-xs text-[var(--juba-app-muted)] font-semibold tracking-[0.12em] uppercase">
              {t('step2', { questionNumber, totalQuestions })}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-[var(--juba-app-muted)] border-[var(--juba-app-line)] border px-2 py-1 font-semibold tracking-[0.12em] uppercase">
              {question.difficulty}
            </span>
            <span className="text-xs text-[var(--juba-app-muted)] border-[var(--juba-app-line)] border px-2 py-1 font-semibold tracking-[0.12em] uppercase">
              {skillLabelMap[question.skill] ?? question.skill}
            </span>
          </div>
        </div>

        {/* Progress bar */}
        <div className="bg-[var(--juba-app-green-soft)] h-1">
          <div
            className="bg-[var(--juba-app-green)] h-1 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Question */}
        <div className="space-y-7 p-6 sm:p-9">
          <TargetLanguageText
            as="p"
            languageCode={languageCode}
            className="text-[var(--juba-app-ink)]"
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
                  className="border-[var(--juba-app-line)] text-[var(--juba-app-ink)] hover:border-2 hover:text-[var(--juba-app-green-dark)] hover:bg-[#f3f7ef] flex w-full items-start gap-3 border px-4 py-3 text-left transition-colors"
                >
                  <span className="text-xs text-[var(--juba-app-muted)] shrink-0 font-sans">
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
