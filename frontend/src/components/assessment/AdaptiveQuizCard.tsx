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
    <div className="flex min-h-[60vh] flex-col items-center justify-center bg-[#f4f4f2] p-4 sm:p-6">
      <div className="w-full max-w-2xl overflow-hidden rounded-[26px] border border-[rgba(7,7,9,.08)] bg-white shadow-[0_12px_30px_rgba(43,45,90,.055)]">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-[rgba(7,7,9,.07)] bg-[#f4f4f2] px-5 py-4 sm:px-6">
          <div className="flex items-center gap-2">
            <span className="text-xs text-[rgba(32,33,39,.52)]">●</span>
            <span className="text-xs text-[rgba(32,33,39,.52)] font-semibold tracking-[0.12em] uppercase">
              {t('step2', { questionNumber, totalQuestions })}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-[rgba(32,33,39,.52)] border-[rgba(7,7,9,.08)] rounded-full border px-2 py-1 font-semibold tracking-[0.12em] uppercase">
              {question.difficulty}
            </span>
            <span className="text-xs text-[rgba(32,33,39,.52)] border-[rgba(7,7,9,.08)] rounded-full border px-2 py-1 font-semibold tracking-[0.12em] uppercase">
              {skillLabelMap[question.skill] ?? question.skill}
            </span>
          </div>
        </div>

        {/* Progress bar */}
        <div className="h-1 bg-[#ededff]">
          <div
            className="h-1 bg-[#5862e2] transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>

        {/* Question */}
        <div className="space-y-7 p-6 sm:p-9">
          <TargetLanguageText
            as="p"
            languageCode={languageCode}
            className="text-[#202127]"
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
                  className="flex w-full items-start gap-3 rounded-[16px] border border-[rgba(7,7,9,.08)] bg-[#f4f4f2] px-4 py-3 text-left text-[#202127] transition-all hover:border-[#5862e2] hover:bg-[#ededff] hover:text-[#373fb8] hover:shadow-[0_8px_18px_rgba(43,45,90,.05)]"
                >
                  <span className="text-xs text-[rgba(32,33,39,.52)] shrink-0 font-sans">
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
