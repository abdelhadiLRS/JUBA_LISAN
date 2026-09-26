'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { MaintenanceGate } from '@/components/billing/MaintenanceBanner'
import { type ReadingExercise } from '@/types/api'
import { WordTooltip, useWordSave } from '@/components/ui/WordTooltip'
import { PageLoading } from '@/components/ui/page-loading'
import { Pagination } from '@/components/ui/pagination'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import {
  ReviewPrompt,
  getReviewPromptDismissal,
} from '@/components/reviews/ReviewPrompt'
import { shouldShowExerciseReviewPrompt } from '@/lib/review-prompt-triggers'
import { markLearningProgressUpdated } from '@/lib/learning-progress'
import { useFreemiumStore } from '@/store/freemium'
import { useConfigStore } from '@/store/config'
import { useAuthStore, isSubscribed, isFreemiumTrialActive } from '@/store/auth'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface CorrectAnswer {
  index: number
  correct: string
}

interface SubmitResult {
  score: number
  xp_earned: number
  correct_answers: CorrectAnswer[]
}

interface AttemptItem {
  id: number
  score: number
  xp_earned: number
  completed_at: string
  exercise: ReadingExercise
  answers: Record<string, string>
  correct_answers: CorrectAnswer[]
}

type PageState =
  | 'loading'
  | 'idle'
  | 'generating'
  | 'exercise'
  | 'results'
  | 'history'

const HISTORY_PAGE_SIZE = 10

// ---------------------------------------------------------------------------
// Main page logic
// ---------------------------------------------------------------------------

function ReadingPage() {
  const t = useTranslations('reading')
  const tCommon = useTranslations('common')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const {
    selectedWord,
    tooltipPos,
    saveState,
    handleTextSelection,
    handleSaveWord,
    dismissTooltip,
  } = useWordSave()

  const [pageState, setPageState] = useState<PageState>('loading')
  const [exercise, setExercise] = useState<ReadingExercise | null>(null)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [result, setResult] = useState<SubmitResult | null>(null)
  const [history, setHistory] = useState<AttemptItem[]>([])
  const [historyTotal, setHistoryTotal] = useState(0)
  const [historyPage, setHistoryPage] = useState(0)
  const [historyLoading, setHistoryLoading] = useState(false)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [reviewPromptOpen, setReviewPromptOpen] = useState(false)

  const textRef = useRef<HTMLDivElement>(null)
  const [isReplay, setIsReplay] = useState(false)
  const [generatingWarn, setGeneratingWarn] = useState(false)
  const generateAbortRef = useRef<AbortController | null>(null)
  const generatingTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const fetchFreemium = useFreemiumStore((s) => s.fetchStatus)
  const decrementFreemium = useFreemiumStore((s) => s.decrement)
  const freemiumStatus = useFreemiumStore((s) => s.status)
  const freemiumExhausted =
    stripeEnabled &&
    !isSubscribed(user, stripeEnabled) &&
    !isFreemiumTrialActive(user, stripeEnabled) &&
    freemiumStatus &&
    freemiumStatus.reading_remaining <= 0

  useEffect(() => {
    if (stripeEnabled && !isSubscribed(user, stripeEnabled)) {
      fetchFreemium()
    }
  }, [stripeEnabled, user, fetchFreemium])

  // Warn if exercise generation takes longer than 15 s
  useEffect(() => {
    if (pageState === 'generating') {
      setGeneratingWarn(false)
      generatingTimerRef.current = setTimeout(
        () => setGeneratingWarn(true),
        15_000
      )
    } else {
      if (generatingTimerRef.current) clearTimeout(generatingTimerRef.current)
      setGeneratingWarn(false)
    }
    return () => {
      if (generatingTimerRef.current) clearTimeout(generatingTimerRef.current)
    }
  }, [pageState])

  // Cancel in-flight long-poll on unmount
  useEffect(() => {
    return () => {
      generateAbortRef.current?.abort()
    }
  }, [])

  const loadNext = useCallback(async () => {
    setPageState('loading')
    setError('')
    dismissTooltip()
    try {
      const res = await apiFetch('/api/reading/next')
      if (!res.ok) {
        setPageState('idle')
        return
      }
      const data = (await res.json()) as {
        available: boolean
        exercise?: ReadingExercise
      }
      if (data.available && data.exercise) {
        setExercise(data.exercise)
        setAnswers({})
        setResult(null)
        setIsReplay(false)
        setPageState('exercise')
      } else {
        setPageState('idle')
      }
    } catch {
      setError(t('errorLoading'))
      setPageState('idle')
    }
  }, [t, dismissTooltip])

  useEffect(() => {
    loadNext()
  }, [loadNext, activeLanguage?.code])

  async function handleGenerate() {
    try {
      const res = await apiFetch('/api/reading/generate', { method: 'POST' })
      if (res.ok || res.status === 202) {
        setPageState('generating')
        const controller = new AbortController()
        generateAbortRef.current = controller
        const nextRes = await apiFetch('/api/reading/next?wait=true', {
          signal: controller.signal,
        })
        generateAbortRef.current = null
        if (nextRes.ok) {
          const data = (await nextRes.json()) as {
            available: boolean
            exercise?: ReadingExercise
          }
          if (data.available && data.exercise) {
            setExercise(data.exercise)
            setAnswers({})
            setResult(null)
            setIsReplay(false)
            setPageState('exercise')
            return
          }
        }
        setPageState('idle')
      } else {
        const d = (await res.json().catch(() => ({}))) as { detail?: string }
        setError(
          d.detail === 'No active study plan found'
            ? tCommon('noActivePlan')
            : t('errorLoading')
        )
      }
    } catch (err) {
      if (err instanceof Error && err.name === 'AbortError') return
      setPageState('idle')
    }
  }

  async function handleSubmit() {
    if (!exercise) return
    setSubmitting(true)
    setError('')
    try {
      const res = await apiFetch('/api/reading/attempt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          exercise_id: exercise.id,
          answers,
          replay: isReplay,
        }),
      })
      if (!res.ok) {
        const d = (await res.json().catch(() => ({}))) as { detail?: string }
        setError(
          d.detail === 'already_attempted'
            ? t('alreadyAttempted')
            : t('errorSubmit')
        )
        return
      }
      const data = (await res.json()) as SubmitResult
      markLearningProgressUpdated()
      setResult(data)
      dismissTooltip()
      if (
        !isSubscribed(user, stripeEnabled) &&
        !isFreemiumTrialActive(user, stripeEnabled)
      ) {
        decrementFreemium('reading_remaining')
      }
      setPageState('results')
      if (
        shouldShowExerciseReviewPrompt(getReviewPromptDismissal(), !isReplay)
      ) {
        setReviewPromptOpen(true)
      }
    } catch {
      setError(t('errorSubmit'))
    } finally {
      setSubmitting(false)
    }
  }

  async function loadHistory(pageIndex = 0) {
    setPageState('history')
    setHistoryPage(pageIndex)
    setHistoryLoading(true)
    try {
      const params = new URLSearchParams({
        skip: String(pageIndex * HISTORY_PAGE_SIZE),
        limit: String(HISTORY_PAGE_SIZE),
      })
      const res = await apiFetch(`/api/reading/history?${params.toString()}`)
      if (res.ok) {
        const data = (await res.json()) as {
          items: AttemptItem[]
          total: number
        }
        setHistory(data.items)
        setHistoryTotal(data.total)
      }
    } catch {
      setError(t('errorLoading'))
    } finally {
      setHistoryLoading(false)
    }
  }

  const allAnswered = exercise
    ? Object.keys(answers).length === exercise.questions.length
    : false
  const targetLanguageCode = activeLanguage?.code ?? 'en-GB'

  // ── Loading ──────────────────────────────────────────────────────────────
  if (pageState === 'loading') {
    return <PageLoading minHeight="min-h-[calc(100vh-56px)] md:min-h-screen" />
  }

  // ── Generating (long-poll) ────────────────────────────────────────────────
  if (pageState === 'generating') {
    return (
      <PageLoading
        label={t('generating')}
        subtext={
          generatingWarn
            ? `${t('generatingDesc')} ${t('generatingLong')}`
            : t('generatingDesc')
        }
        minHeight="min-h-[calc(100vh-56px)] md:min-h-screen"
      />
    )
  }

  // ── History ───────────────────────────────────────────────────────────────
  if (pageState === 'history') {
    return (
      <div className="container-xl page-body py-4">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[#202127] font-sans text-sm font-bold tracking-widest uppercase">
            {t('historyTitle')}
          </h1>
          <button
            onClick={loadNext}
            className="text-[rgba(32,33,39,.52)] hover:text-[#202127] font-sans text-xs tracking-widest uppercase transition-colors"
          >
            {t('practiceMore')}
          </button>
        </div>

        {historyLoading && history.length === 0 ? (
          <PageLoading fullScreen={false} className="block p-5" />
        ) : history.length === 0 ? (
          <div className="border-[rgba(7,7,9,.08)] bg-[#fff] border p-6 text-center">
            <p className="text-[rgba(32,33,39,.52)] font-sans text-xs tracking-wide">
              {t('historyEmpty')}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {history.map((item) => (
              <div
                key={item.id}
                className="border-[rgba(7,7,9,.08)] bg-[#fff] border p-4"
              >
                <div className="mb-3 flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <p className="text-[#202127] truncate font-sans text-xs font-bold tracking-wide">
                      {item.exercise.topic}
                    </p>
                    <p className="text-[rgba(32,33,39,.52)] mt-0.5 font-sans tracking-widest uppercase">
                      {item.exercise.level} · {item.exercise.exercise_type}
                    </p>
                  </div>
                  <div className="shrink-0 text-right">
                    <p className="text-[#202127] font-sans text-xs font-bold">
                      {item.score}/{item.exercise.questions.length}
                    </p>
                    <p className="text-[#202127] text-[#5862e2] font-sans">
                      +{item.xp_earned} XP
                    </p>
                  </div>
                </div>
                <TargetLanguageText
                  as="p"
                  languageCode={item.exercise.target_language}
                  className="text-[rgba(32,33,39,.52)] border-[rgba(7,7,9,.08)] mb-3 line-clamp-3 border-t pt-3"
                >
                  {item.exercise.text}
                </TargetLanguageText>
                <button
                  onClick={() => {
                    setExercise(item.exercise)
                    setAnswers({})
                    setResult(null)
                    setIsReplay(true)
                    setPageState('exercise')
                  }}
                  className="text-[rgba(32,33,39,.52)] hover:text-[#202127] font-sans text-xs tracking-widest uppercase transition-colors"
                >
                  {t('practiceAgain')}
                </button>
              </div>
            ))}
          </div>
        )}

        <Pagination
          page={historyPage}
          totalPages={Math.ceil(historyTotal / HISTORY_PAGE_SIZE)}
          loading={historyLoading}
          onPageChange={loadHistory}
          prevLabel={`← ${tCommon('back')}`}
          nextLabel={`${tCommon('next')} →`}
          className="mt-4"
        />
      </div>
    )
  }

  // ── Results ───────────────────────────────────────────────────────────────
  if (pageState === 'results' && result && exercise) {
    return (
      <div className="container-xl page-body py-4">
        {/* Score card */}
        <div className="border-[rgba(7,7,9,.08)] bg-[#fff] border p-5">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-[rgba(32,33,39,.52)] font-sans tracking-widest uppercase">
                {t('resultsLabel')}
              </p>
              <p className="text-[#202127] mt-1 font-sans text-2xl font-bold">
                {result.score}/{exercise.questions.length}
              </p>
            </div>
            <div className="text-right">
              <p className="text-[rgba(32,33,39,.52)] font-sans tracking-widest uppercase">
                XP
              </p>
              {isReplay ? (
                <p className="text-[rgba(32,33,39,.52)] mt-1 font-sans">
                  {t('replayNoXp')}
                </p>
              ) : (
                <p className="text-[#5862e2] mt-1 font-sans text-xl font-bold">
                  +{result.xp_earned}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Question review */}
        <div className="space-y-3">
          <p className="text-[rgba(32,33,39,.52)] font-sans tracking-widest uppercase">
            {t('review')}
          </p>
          {exercise.questions.map((q) => {
            const correctKey = result.correct_answers.find(
              (c) => c.index === q.index
            )?.correct
            const userAnswer = answers[String(q.index)]
            const isCorrect = userAnswer === correctKey
            return (
              <div
                key={q.index}
                className={`border p-4 ${
                  isCorrect
                    ? 'border-[#5862e2]/50 bg-[#ededff]/5'
                    : 'border-[#b33a32]/50 bg-[#b33a32]/5'
                }`}
              >
                <TargetLanguageText
                  as="p"
                  languageCode={targetLanguageCode}
                  className="text-[#202127] mb-3"
                >
                  {q.index + 1}. {q.question}
                </TargetLanguageText>
                <div className="space-y-1">
                  {Object.entries(q.options).map(([k, v]) => (
                    <div
                      key={k}
                      className={`px-3 py-1.5 ${
                        k === correctKey
                          ? 'text-[#5862e2] font-bold'
                          : k === userAnswer && !isCorrect
                            ? 'text-[#b33a32] line-through'
                            : 'text-[rgba(32,33,39,.52)]'
                      }`}
                    >
                      <span className="text-[#202127] font-sans font-bold">
                        {k}.
                      </span>{' '}
                      <TargetLanguageText languageCode={targetLanguageCode}>
                        {v}
                      </TargetLanguageText>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>

        {/* Actions */}
        <div className="flex gap-3 pt-1">
          <button
            onClick={loadNext}
            className="border-[rgba(7,7,9,.08)] bg-[#fff] text-[#202127] hover:bg-[#fff] flex-1 border py-3 font-sans text-sm tracking-widest uppercase transition-colors"
          >
            {t('nextExercise')}
          </button>
          <button
            onClick={() => loadHistory(0)}
            className="border-[rgba(7,7,9,.08)] bg-[#fff] text-[rgba(32,33,39,.52)] hover:text-[#202127] hover:bg-[#fff] border px-4 py-3 font-sans text-xs tracking-widest uppercase transition-colors"
          >
            {t('viewHistory')}
          </button>
        </div>
        <ReviewPrompt
          open={reviewPromptOpen}
          onClose={() => setReviewPromptOpen(false)}
          onSubmitted={() => setReviewPromptOpen(false)}
        />
      </div>
    )
  }

  // ── Idle (no exercises available) ─────────────────────────────────────────
  if (pageState === 'idle') {
    return (
      <div className="mx-auto max-w-4xl px-4 py-6 md:px-8">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[#202127] font-sans text-sm font-bold tracking-widest uppercase">
            {t('title')}
          </h1>
          <button
            onClick={() => loadHistory(0)}
            className="text-[rgba(32,33,39,.52)] hover:text-[#202127] font-sans text-xs tracking-widest uppercase transition-colors"
          >
            {t('history')}
          </button>
        </div>

        {error && (
          <p className="text-[rgba(32,33,39,.52)] text-[#b33a32] mb-4 font-sans">
            {error}
          </p>
        )}

        <FreemiumQuotaBanner feature="reading" className="mb-4" />

        {freemiumExhausted ? (
          <PaywallBanner feature="reading" compact />
        ) : (
          <div className="border-[rgba(7,7,9,.08)] bg-[#fff] flex flex-col items-center gap-5 border p-8 text-center">
            <p className="text-[rgba(32,33,39,.52)] font-sans text-xs tracking-wide">
              {t('noExercises')}
            </p>
            <button
              onClick={handleGenerate}
              className="border-[rgba(7,7,9,.08)] bg-[#fff] text-[#202127] hover:bg-[#fff] border px-8 py-3 font-sans text-sm tracking-widest uppercase transition-colors"
            >
              {t('generate')}
            </button>
          </div>
        )}
      </div>
    )
  }

  // ── Exercise ──────────────────────────────────────────────────────────────
  if (!exercise) return null

  return (
    <div className="container-xl page-body py-4">
      {/* Header */}
      <div className="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-[#202127] font-sans text-sm font-bold tracking-widest uppercase">
            {t('title')}
          </h1>
          <p className="text-[rgba(32,33,39,.52)] mt-0.5 font-sans tracking-widest uppercase">
            {exercise.level} · {exercise.exercise_type} · {exercise.topic}
          </p>
        </div>
        <button
          onClick={() => loadHistory(0)}
          className="text-[rgba(32,33,39,.52)] hover:text-[#202127] shrink-0 font-sans text-xs tracking-widest uppercase transition-colors"
        >
          {t('history')}
        </button>
      </div>

      <FreemiumQuotaBanner feature="reading" className="mb-4" />

      {freemiumExhausted ? (
        <PaywallBanner feature="reading" compact />
      ) : (
        <>
          {/* Two-column on desktop, stacked on mobile */}
          <div className="flex flex-col gap-5 md:grid md:grid-cols-[55fr_45fr] md:gap-6">
            {/* Left: reading text */}
            <div>
              <p className="text-[rgba(32,33,39,.52)] mb-2 font-sans tracking-widest uppercase">
                {t('textLabel')}
              </p>
              <div className="border-[rgba(7,7,9,.08)] bg-[#fff] relative border p-5">
                <div
                  ref={textRef}
                  onPointerUp={() =>
                    handleTextSelection(
                      exercise?.text ?? '',
                      exercise?.level ?? 'B1'
                    )
                  }
                >
                  <TargetLanguageText
                    as="p"
                    languageCode={exercise.target_language}
                    className="reading-text text-[#202127] word-selectable max-w-[70ch] cursor-text whitespace-pre-wrap select-text"
                  >
                    {exercise.text}
                  </TargetLanguageText>
                </div>
              </div>
              <p className="text-[rgba(32,33,39,.52)] mt-2 text-center font-sans leading-relaxed">
                {t('selectWordHint')}
              </p>
            </div>

            {/* Right: questions */}
            <div>
              <p className="text-[rgba(32,33,39,.52)] mb-2 font-sans tracking-widest uppercase">
                {t('questionsLabel')}
              </p>
              <div className="space-y-4">
                {exercise.questions.map((q) => (
                  <div
                    key={q.index}
                    className="border-[rgba(7,7,9,.08)] bg-[#fff] border p-4"
                  >
                    <TargetLanguageText
                      as="p"
                      languageCode={exercise.target_language}
                      onPointerUp={() =>
                        handleTextSelection(q.question, exercise.level)
                      }
                      className="text-[#202127] word-selectable mb-3 cursor-text select-text"
                    >
                      {q.index + 1}. {q.question}
                    </TargetLanguageText>
                    <div className="space-y-2">
                      {Object.entries(q.options).map(([k, v]) => {
                        const selected = answers[String(q.index)] === k
                        return (
                          <button
                            key={k}
                            onClick={() =>
                              setAnswers((prev) => ({
                                ...prev,
                                [String(q.index)]: k,
                              }))
                            }
                            className={`w-full border px-3 py-2 text-left transition-colors ${
                              selected
                                ? 'border-[#5862e2] text-[#202127] bg-[#fff]'
                                : 'border-[rgba(7,7,9,.08)] text-[rgba(32,33,39,.52)] hover:border-[rgba(7,7,9,.08)] hover:text-[#202127]'
                            }`}
                          >
                            <span className="text-[#202127] font-sans font-bold">
                              {k}.
                            </span>{' '}
                            <TargetLanguageText
                              languageCode={exercise.target_language}
                            >
                              {v}
                            </TargetLanguageText>
                          </button>
                        )
                      })}
                    </div>
                  </div>
                ))}
              </div>

              {error && (
                <p className="text-[rgba(32,33,39,.52)] text-[#b33a32] mt-3 font-sans">
                  {error}
                </p>
              )}

              <button
                onClick={handleSubmit}
                disabled={!allAnswered || submitting}
                className="border-[rgba(7,7,9,.08)] bg-[#202127] text-[#f4f4f2] hover:bg-[#202127]/90 focus-visible:outline-fl-fg mt-4 w-full border py-3 font-sans text-sm font-bold tracking-widest uppercase transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-40"
              >
                {submitting ? '...' : t('submit')}
              </button>
            </div>
          </div>

          {/* Word-save tooltip */}
          {selectedWord && (
            <WordTooltip
              word={selectedWord}
              pos={tooltipPos}
              saveState={saveState}
              onSave={() => handleSaveWord()}
              onDismiss={dismissTooltip}
              labels={{
                saveWord: tCommon('saveWord'),
                wordSaved: tCommon('wordSaved'),
                wordSaveError: tCommon('wordSaveError'),
              }}
            />
          )}
        </>
      )}
    </div>
  )
}

export default function ReadingPageWrapper() {
  return (
    <MaintenanceGate>
      <ReadingPage />
    </MaintenanceGate>
  )
}
