'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import { markLearningProgressUpdated } from '@/lib/learning-progress'

// ── Types ──────────────────────────────────────────────────────────────────────

interface LevelTestQuestion {
  id: string
  skill: string // grammar | vocabulary | reading
  difficulty: string
  question: string
  options: string[]
  correct: string
}

interface AnswerRecord {
  question_id: string
  skill: string
  difficulty: string
  correct: boolean
}

interface LevelTestResult {
  score: number // 0–1
  recommendation: 'advance' | 'extend' | 'repeat'
  next_level: string | null
}

interface SkillBreakdown {
  correct: number
  total: number
}

type FlowStep = 'loading' | 'quiz' | 'submitting' | 'result' | 'error'

// ── Helpers ────────────────────────────────────────────────────────────────────

function computeSkillBreakdown(
  questions: LevelTestQuestion[],
  answers: AnswerRecord[]
): Record<string, SkillBreakdown> {
  const map: Record<string, SkillBreakdown> = {}
  answers.forEach((a) => {
    const q = questions.find((q) => q.id === a.question_id)
    if (!q) return
    const skill = q.skill
    if (!map[skill]) map[skill] = { correct: 0, total: 0 }
    map[skill].total += 1
    if (a.correct) map[skill].correct += 1
  })
  return map
}

const SKILL_LABELS: Record<string, string> = {
  grammar: 'Grammar',
  vocabulary: 'Vocabulary',
  reading: 'Reading',
}

const SKILL_ICONS: Record<string, string> = {
  grammar: 'G',
  vocabulary: 'V',
  reading: 'R',
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function LevelTestPage() {
  const t = useTranslations('assessment')
  const router = useRouter()
  const searchParams = useSearchParams()
  const planId = searchParams.get('plan')

  // Bug #6 fix: gate loadQuestions until user confirms the start warning
  const [startConfirmed, setStartConfirmed] = useState(false)
  const [showStartWarning, setShowStartWarning] = useState(true)

  const [step, setStep] = useState<FlowStep>('loading')
  const [questions, setQuestions] = useState<LevelTestQuestion[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [answers, setAnswers] = useState<AnswerRecord[]>([])
  const [cefrLevel, setCefrLevel] = useState('')
  const [result, setResult] = useState<LevelTestResult | null>(null)
  const [error, setError] = useState('')
  const [selectedOption, setSelectedOption] = useState<string | null>(null)
  // Bug #1 fix: renamed to avoid confusion; this tracks whether the current answer is confirmed
  const [answerConfirmed, setAnswerConfirmed] = useState(false)

  // Bug #1 fix: ref holds the always-current answers array so handleNext never uses a stale closure
  const answersRef = useRef<AnswerRecord[]>([])

  // ── Load questions ────────────────────────────────────────────────────────

  const loadQuestions = useCallback(async () => {
    // Bug #6 fix: skip network call until the user has confirmed starting
    if (!startConfirmed) return

    // Bug #5 fix: validate planId before converting to number
    const planIdNum = Number(planId)
    if (!planId || !Number.isInteger(planIdNum) || planIdNum <= 0) {
      setError(
        'Invalid plan ID. Please access the level test from your plan page.'
      )
      setStep('error')
      return
    }

    try {
      const res = await apiFetch(
        `/api/assessment/level-test/questions/${planIdNum}`
      )
      if (!res.ok) {
        const d = await res.json().catch(() => ({}))
        throw new Error(
          (d as { detail?: string }).detail ?? `Error ${res.status}`
        )
      }
      const data = (await res.json()) as {
        plan_id: number
        cefr_level: string
        questions: LevelTestQuestion[]
      }
      if (!data.questions?.length) {
        throw new Error('No questions received from the server.')
      }
      setQuestions(data.questions)
      setCefrLevel(data.cefr_level)
      setStep('quiz')
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to load level test.'
      )
      setStep('error')
    }
  }, [planId, startConfirmed])

  useEffect(() => {
    void loadQuestions()
  }, [loadQuestions])

  // ── Answer handling ───────────────────────────────────────────────────────

  function handleSelectOption(option: string) {
    if (answerConfirmed) return
    setSelectedOption(option)
  }

  function handleConfirmAnswer() {
    if (!selectedOption || answerConfirmed) return
    const q = questions[currentIndex]
    const isCorrect = selectedOption === q.correct
    setAnswerConfirmed(true)
    const record: AnswerRecord = {
      question_id: q.id,
      skill: q.skill,
      difficulty: q.difficulty,
      correct: isCorrect,
    }
    // Bug #1 fix: build the new array eagerly and store it in both state and ref.
    // handleNext reads from the ref so it always has the latest array regardless of
    // when React schedules the state update.
    const newAnswers = [...answers, record]
    setAnswers(newAnswers)
    answersRef.current = newAnswers
  }

  function handleNext() {
    if (currentIndex + 1 >= questions.length) {
      // Bug #1 fix: use the ref instead of the stale `answers` closure
      void submitTest(answersRef.current)
      return
    }
    setCurrentIndex((i) => i + 1)
    setSelectedOption(null)
    setAnswerConfirmed(false)
  }

  async function submitTest(finalAnswers: AnswerRecord[]) {
    setStep('submitting')
    // Bug #5 fix: planId already validated above; Number() is safe here
    const planIdNum = Number(planId)
    try {
      const res = await apiFetch('/api/assessment/level-test/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan_id: planIdNum, answers: finalAnswers }),
      })
      if (!res.ok) {
        const d = await res.json().catch(() => ({}))
        throw new Error(
          (d as { detail?: string }).detail ?? `Error ${res.status}`
        )
      }
      const data = (await res.json()) as LevelTestResult
      setResult(data)
      markLearningProgressUpdated()
      setStep('result')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Submission failed.')
      setStep('error')
    }
  }

  // ── Renders ───────────────────────────────────────────────────────────────

  // Start warning dialog — shown before any loading begins
  if (showStartWarning) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <ConfirmDialog
          open={true}
          title={t('startWarningTitle')}
          message={t('startWarningMessageLevelTest')}
          confirmLabel={t('startWarningConfirm')}
          onConfirm={() => {
            setShowStartWarning(false)
            setStartConfirmed(true)
          }}
          onCancel={() => router.push('/plan')}
        />
      </div>
    )
  }

  if (step === 'loading' || step === 'submitting') {
    return (
      <PageLoading
        label={
          step === 'loading'
            ? t('levelTest.loadingTest')
            : t('levelTest.submittingTest')
        }
      />
    )
  }

  if (step === 'error') {
    return (
      <div className="flex min-h-[60vh] items-center justify-center p-6">
        <div className="border-[rgba(7,7,9,.08)] bg-white w-full max-w-md border">
          <div className="border-[rgba(7,7,9,.08)] flex items-center gap-2 border-b px-6 py-4">
            <span className="text-[#202127] text-[rgba(32,33,39,.52)]">●</span>
            <span className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
              Level Test
            </span>
          </div>
          <div className="space-y-6 p-8">
            <p className="text-sm leading-relaxed text-red-500">
              {error}
            </p>
            <button
              onClick={() => router.push('/plan')}
              className="border-[rgba(7,7,9,.08)] text-[rgba(32,33,39,.52)] hover:border-[#5862e2] hover:text-[#202127] w-full rounded-[14px] border py-3 text-sm tracking-widest uppercase transition-colors"
            >
              ← Back to Plan
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (step === 'result' && result) {
    const pct = Math.round(result.score * 100)
    const breakdown = computeSkillBreakdown(questions, answers)
    const weakAreas = Object.entries(breakdown)
      .filter(([, v]) => v.total > 0 && v.correct / v.total < 0.6)
      .map(([skill]) => SKILL_LABELS[skill] ?? skill)

    const recConfig: Record<
      LevelTestResult['recommendation'],
      {
        icon: string
        label: string
        message: string
        nextAction: string
        nextLabel: string
      }
    > = {
      advance: {
        icon: '🎉',
        label: `ADVANCE TO ${result.next_level ?? 'NEXT LEVEL'}`,
        message: `You demonstrated solid ${cefrLevel} mastery. Your ${result.next_level ?? 'next-level'} programme is ready!`,
        nextAction: result.next_level ? '/assessment' : '/plan',
        nextLabel: result.next_level
          ? `Start ${result.next_level} Programme →`
          : 'Go to Plan',
      },
      extend: {
        icon: '⚠',
        label: '4-WEEK EXTENSION',
        message: `Weak areas detected: ${weakAreas.join(', ') || 'Reading Comprehension'}. We recommend 4 extra weeks of focused practice.`,
        nextAction: '/plan',
        nextLabel: 'Accept Extension →',
      },
      repeat: {
        icon: '↺',
        label: `REPEAT ${cefrLevel}`,
        message: `Score below 55%. Several core ${cefrLevel} competencies need reinforcement. A fresh plan has been prepared.`,
        nextAction: '/plan',
        nextLabel: `Start New ${cefrLevel} Plan →`,
      },
    }

    const rec = recConfig[result.recommendation]

    return (
      <div className="flex min-h-[60vh] items-center justify-center p-6">
        <div className="border-[rgba(7,7,9,.08)] bg-white w-full max-w-lg border">
          {/* Header */}
          <div className="border-[rgba(7,7,9,.08)] flex items-center justify-between border-b px-6 py-4">
            <div className="flex items-center gap-2">
              <span className="text-[#202127] text-[rgba(32,33,39,.52)]">●</span>
              <span className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
                {cefrLevel} Level Test — Results
              </span>
            </div>
          </div>

          <div className="space-y-6 p-8">
            {/* Score */}
            <div className="space-y-2 text-center">
              <p className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
                Final Score
              </p>
              <p className="text-[#202127] font-mono text-7xl font-bold tracking-widest">
                {pct}%
              </p>
              <p className="text-[rgba(32,33,39,.52)] text-sm">
                {answers.filter((a) => a.correct).length} / {questions.length}{' '}
                correct
              </p>
            </div>

            {/* Skill breakdown */}
            <div className="space-y-2">
              {Object.entries(breakdown).map(([skill, v]) => {
                const skillPct =
                  v.total > 0 ? Math.round((v.correct / v.total) * 100) : 0
                const isWeak = skillPct < 60
                return (
                  <div key={skill} className="flex items-center gap-3">
                    <span className="text-[#202127] text-[rgba(32,33,39,.52)] w-6 text-center font-mono uppercase">
                      {SKILL_ICONS[skill] ?? skill[0].toUpperCase()}
                    </span>
                    <span className="text-[#202127] text-[rgba(32,33,39,.52)] w-24 font-semibold tracking-wide">
                      {SKILL_LABELS[skill] ?? skill}
                    </span>
                    <div className="bg-[#e1e1df] h-1.5 flex-1">
                      <div
                        className={`h-full transition-all ${isWeak ? 'bg-amber-500' : 'bg-[#5862e2]'}`}
                        style={{ width: `${skillPct}%` }}
                      />
                    </div>
                    <span
                      className={`text-[#202127] w-16 text-right font-mono ${isWeak ? 'text-amber-500' : 'text-[#202127]'}`}
                    >
                      {v.correct}/{v.total} ({skillPct}%)
                      {isWeak && ' ◂'}
                    </span>
                  </div>
                )
              })}
            </div>

            {/* Recommendation */}
            <div className="border-[rgba(7,7,9,.08)] space-y-3 rounded-[18px] border p-6">
              <div className="flex items-center gap-2">
                <span className="text-xl">{rec.icon}</span>
                <span className="text-[#202127] text-[#202127] font-mono font-bold tracking-widest uppercase">
                  Recommendation: {rec.label}
                </span>
              </div>
              <p className="text-[rgba(32,33,39,.52)] text-sm leading-relaxed">
                {rec.message}
              </p>
            </div>

            {/* Actions */}
            <div className="flex flex-col gap-2">
              <button
                onClick={() => router.push(rec.nextAction)}
                className="bg-[#5862e2] text-white hover:bg-[#5862e2]/90 w-full rounded-[14px] py-3.5 text-sm font-bold tracking-widest uppercase transition-colors"
              >
                {rec.nextLabel}
              </button>
              <button
                onClick={() => router.push('/plan')}
                className="border-[rgba(7,7,9,.08)] text-[rgba(32,33,39,.52)] hover:border-[#5862e2] hover:text-[#202127] w-full rounded-[14px] border py-3 text-sm tracking-widest uppercase transition-colors"
              >
                ← Back to Plan
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // ── Quiz step ─────────────────────────────────────────────────────────────

  const q = questions[currentIndex]
  if (!q) return null

  const progress = (currentIndex / questions.length) * 100
  const skillLabel = SKILL_LABELS[q.skill] ?? q.skill

  return (
    <div className="flex min-h-[60vh] items-center justify-center p-6">
      <div className="border-[rgba(7,7,9,.08)] bg-white w-full max-w-lg border">
        {/* Header */}
        <div className="border-[rgba(7,7,9,.08)] space-y-3 border-b px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-[#202127] text-[rgba(32,33,39,.52)]">●</span>
              <span className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
                {cefrLevel} Level Test
              </span>
            </div>
            <span className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
              {currentIndex + 1} / {questions.length}
            </span>
          </div>
          {/* Progress bar */}
          <div className="bg-[#e1e1df] h-0.5">
            <div
              className="bg-[#5862e2] h-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          {/* Skill badge */}
          <div className="flex items-center gap-2">
            <span className="border-[rgba(7,7,9,.08)] text-[#202127] text-[rgba(32,33,39,.52)] border-2 px-2 py-0.5 font-semibold tracking-wide">
              {skillLabel}
            </span>
            <span className="border-[rgba(7,7,9,.08)] text-[#202127] text-[rgba(32,33,39,.52)] border-2 px-2 py-0.5 font-semibold tracking-wide">
              {q.difficulty}
            </span>
          </div>
        </div>

        {/* Question */}
        <div className="space-y-6 p-8">
          <p className="text-[#202127] text-sm leading-relaxed">
            {q.question}
          </p>

          {/* Options */}
          <div className="space-y-2">
            {q.options.map((option, i) => {
              let style =
                'w-full text-left rounded-[14px] border text-sm tracking-wide py-3.5 px-4 transition-colors cursor-pointer'

              if (!answerConfirmed) {
                style +=
                  selectedOption === option
                    ? ' border-[#5862e2] text-[#202127] bg-white'
                    : ' border-[rgba(7,7,9,.08)] text-[rgba(32,33,39,.52)] hover:border-[#5862e2] hover:text-[#202127]'
              } else {
                if (option === q.correct) {
                  style +=
                    ' border-green-500 text-green-600 dark:text-green-400'
                } else if (option === selectedOption && option !== q.correct) {
                  style += ' border-red-500 text-red-500'
                } else {
                  style += ' border-[rgba(7,7,9,.08)] text-[rgba(32,33,39,.52)] opacity-50'
                }
              }

              const prefix = ['A', 'B', 'C', 'D'][i] ?? String(i + 1)

              return (
                <button
                  key={i}
                  onClick={() => handleSelectOption(option)}
                  disabled={answerConfirmed}
                  className={style}
                >
                  <span className="text-[rgba(32,33,39,.52)] mr-3">{prefix}.</span>
                  {option}
                </button>
              )
            })}
          </div>

          {/* Confirm / Next */}
          {!answerConfirmed ? (
            <button
              onClick={handleConfirmAnswer}
              disabled={!selectedOption}
              className="bg-[#5862e2] text-white hover:bg-[#5862e2]/90 w-full rounded-[14px] py-3.5 text-sm font-bold tracking-widest uppercase transition-colors disabled:cursor-not-allowed disabled:opacity-40"
            >
              Confirm Answer
            </button>
          ) : (
            <div className="space-y-3">
              <div
                className={`border-2 p-3 text-sm leading-relaxed ${
                  answers.at(-1)?.correct
                    ? 'border-green-500 text-green-600 dark:text-green-400'
                    : 'border-red-500 text-red-500'
                }`}
              >
                {answers.at(-1)?.correct
                  ? '✓ Correct'
                  : `✗ Incorrect — correct answer: ${q.correct}`}
              </div>
              <button
                onClick={handleNext}
                className="bg-[#5862e2] text-white hover:bg-[#5862e2]/90 w-full rounded-[14px] py-3.5 text-sm font-bold tracking-widest uppercase transition-colors"
              >
                {currentIndex + 1 >= questions.length
                  ? 'Submit Test →'
                  : 'Next Question →'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
