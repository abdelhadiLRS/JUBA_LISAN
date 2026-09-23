'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { apiFetch, fetchNextLessonSkillMastery } from '@/lib/api'
import { useProgressStore } from '@/store/progress'
import { useLanguageStore } from '@/store/language'
import { useAuthStore, isSubscribed, isFreemiumTrialActive } from '@/store/auth'
import { getGrammarTopics } from '@/data/grammar'
import { WordTooltip, useWordSave } from '@/components/ui/WordTooltip'
import { PageLoading } from '@/components/ui/page-loading'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { useFreemiumStore } from '@/store/freemium'
import { useConfigStore } from '@/store/config'
import { cn } from '@/lib/utils'
import type { SkillMastery } from '@/types/api'
import { markLearningProgressUpdated } from '@/lib/learning-progress'
import {
  hasAdaptiveTarget,
  isAdaptiveAdvanceAction,
  isAdaptiveReinforcementAction,
  isAdaptiveRetryAction,
  mergeAdaptiveRecommendations,
  normaliseAdaptiveAction,
  type AdaptiveExerciseRecommendation,
  fetchNextMasteryExercise,
  fetchNextSkillMasteryExercise,
  type LessonMasteryNextResponse,
} from '@/lib/adaptive-exercise'

interface ExerciseItem { id: number; exercise_type: string; question: string; options: string[] | null; correct_answer: string; explanation: string | null; native_explanation: string | null; user_answer: string | null; score: number | null; feedback: string | null; native_hint: string | null; content_id?: string | null; variant?: string | null; accepted_answers?: string[] | null; metadata?: Record<string, string> | null; skills?: string[] | null; recommended_action?: string; recommended_variant?: string | null; mastery_score?: number; mastery_state?: string; mastery_variants?: number }
interface LessonData { id: number; title: string; lesson_type: string; cefr_level: string; content: Record<string, unknown>; is_completed: boolean }
interface SkillMasteryNext { skill: SkillMastery; reason: 'struggling' | 'unseen' | 'lowest_mastery' }
interface LessonMasterySnapshot { mastery_state: 'unseen' | 'struggling' | 'learning' | 'mastered'; total_exercises: number; attempted_exercises: number; mastered_exercises: number; learning_exercises: number; struggling_exercises: number; unseen_exercises: number; average_mastery_score: number; attempt_rate: number; mastery_rate: number; covered_variants: number; skills: SkillMastery[] }
interface LessonVocabularyItem { word?: string; definition?: string; translation?: string | null; example?: string; example_translation?: string | null; note?: string | null; reading?: string | null }
interface ExerciseAttempt { id: number; exercise_id: number; lesson_id: number; content_id?: string | null; variant?: string | null; attempt_number: number; user_answer: string; score: number; feedback: string; answered_at: string }
type ExerciseAttemptSummary = AdaptiveExerciseRecommendation & { attempts: number; best_score: number; latest_score: number; first_score: number; improvement: number; mastered: boolean; needs_retry: boolean; mastery_score?: number; mastery_state?: string; mastery_variants?: number; latest_variant?: string | null; latest_answered_at: string }

export default function LessonPage() {
  const t = useTranslations('lesson')
  const params = useParams()
  const router = useRouter()
  const id = params.id as string
  const completeLesson = useProgressStore((s) => s.completeLesson)
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const fetchFreemium = useFreemiumStore((s) => s.fetchStatus)
  const freemiumStatus = useFreemiumStore((s) => s.status)
  const freemiumExhausted = stripeEnabled && !isSubscribed(user, stripeEnabled) && !isFreemiumTrialActive(user, stripeEnabled) && freemiumStatus && freemiumStatus.lessons_remaining <= 0
  const { selectedWord, tooltipPos, saveState, handleTextSelection, handleSaveWord, dismissTooltip } = useWordSave()
  const [lesson, setLesson] = useState<LessonData | null>(null)
  const [exercises, setExercises] = useState<ExerciseItem[]>([])
  const [currentExercise, setCurrentExercise] = useState(0)
  const [answer, setAnswer] = useState('')
  const [evaluating, setEvaluating] = useState(false)
  const [completed, setCompleted] = useState(false)
  const [dayComplete, setDayComplete] = useState(false)
  const [attempts, setAttempts] = useState<ExerciseAttempt[]>([])
  const [attemptSummary, setAttemptSummary] = useState<ExerciseAttemptSummary[]>([])
  const [lessonMastery, setLessonMastery] = useState<LessonMasterySnapshot | null>(null)
  const [skillMastery, setSkillMastery] = useState<SkillMastery[]>([])
  const [nextSkillMastery, setNextSkillMastery] = useState<SkillMasteryNext | null>(null)

const skillMasteryPriority: Record<SkillMastery['mastery_state'], number> = { struggling: 0, unseen: 1, learning: 2, mastered: 3 }
  const [masteryNext, setMasteryNext] = useState<LessonMasteryNextResponse | null>(null)
  const [loadingMasteryNext, setLoadingMasteryNext] = useState(false)
  const [masteryReviewMode, setMasteryReviewMode] = useState(false)
  const [masteryReviewCompleted, setMasteryReviewCompleted] = useState(0)
  const [masteryReviewInitialRate, setMasteryReviewInitialRate] = useState<number | null>(null)
  const [masteryReviewFinalRate, setMasteryReviewFinalRate] = useState<number | null>(null)
  const [masteryReviewImproved, setMasteryReviewImproved] = useState(false)
  const [masteryReviewExhausted, setMasteryReviewExhausted] = useState(false)
  const [masteryReviewSkill, setMasteryReviewSkill] = useState<string | null>(null)
  const [attemptsOpen, setAttemptsOpen] = useState(false)
  const [nativeHint, setNativeHint] = useState<string | null>(null)
  const [nativeExplanation, setNativeExplanation] = useState<string | null>(null)
  const [loadingHint, setLoadingHint] = useState(false)
  const [loadingExplanation, setLoadingExplanation] = useState(false)
  const [audioLoadFailed, setAudioLoadFailed] = useState(false)
  const [audioLoading, setAudioLoading] = useState(false)
  const allSkillsMastered = skillMastery.length > 0 && skillMastery.every((item) => item.mastery_state === 'mastered')

  const loadLessonMastery = useCallback(async (lessonId: number) => {
    try {
      const res = await apiFetch(`/api/lessons/${lessonId}/mastery`)
      if (!res.ok) return
      const data: LessonMasterySnapshot = await res.json()
      setLessonMastery(data)
      setSkillMastery(data.skills ?? [])
      try {
        setNextSkillMastery(await fetchNextLessonSkillMastery(lessonId))
      } catch {
        setNextSkillMastery(null)
      }
    } catch { /* aggregate mastery is optional UI */ }
  }, [])

  const loadNextMasteryExercise = useCallback(async (lessonId: number) => {
    try {
      const next = await fetchNextMasteryExercise(lessonId)
      setMasteryNext(next)
    } catch {
      setMasteryNext(null)
    }
  }, [])

  const loadAttemptSummary = useCallback(async (lessonId: number): Promise<ExerciseAttemptSummary[] | null> => {
    try {
      const res = await apiFetch(`/api/lessons/${lessonId}/attempt-summary`)
      if (!res.ok) return null
      const data: ExerciseAttemptSummary[] = await res.json()
      setAttemptSummary(data)
      setExercises((prev) => mergeAdaptiveRecommendations(prev, data))
      return data
    } catch { /* summary is optional UI */ return null }
  }, [])

  useEffect(() => { void getGrammarTopics(activeLanguage?.code ?? 'en-GB').catch(() => undefined) }, [activeLanguage?.code])
  useEffect(() => { void fetchFreemium().catch(() => undefined) }, [fetchFreemium])
  useEffect(() => {
    let cancelled = false
    apiFetch(`/api/lessons/${id}`).then(async (res) => { if (!res.ok) throw new Error('lesson_fetch_failed'); return res.json() }).then((data: { lesson: LessonData; exercises: ExerciseItem[] }) => {
      if (!cancelled) { setLesson(data.lesson); setExercises(data.exercises || []); setCompleted(!!data.lesson.is_completed); void loadAttemptSummary(data.lesson.id); void loadLessonMastery(data.lesson.id); void loadNextMasteryExercise(data.lesson.id) }
    }).catch(() => { if (!cancelled) router.replace('/plan') })
    return () => { cancelled = true }
  }, [id, router, loadAttemptSummary, loadLessonMastery, loadNextMasteryExercise])

  const attemptStats = useMemo(() => {
    if (!attemptSummary.length) return null
    const totalAttempts = attemptSummary.reduce((sum, item) => sum + item.attempts, 0)
    const bestScore = Math.max(...attemptSummary.map((item) => item.best_score))
    const latest = attemptSummary.reduce((current, item) =>
      new Date(item.latest_answered_at).getTime() > new Date(current.latest_answered_at).getTime() ? item : current
    )
    return { totalAttempts, bestScore, latestScore: latest.latest_score }
  }, [attemptSummary])

  const exercise = exercises[currentExercise]
  const currentVariant = exercise?.variant ?? exercise?.exercise_type ?? ''
  const variantLabel = currentVariant.replace(/[_-]+/g, ' ').trim()
  const normalizedExerciseType = currentVariant.toLowerCase().replace(/[_-]+/g, ' ')
  const isLongFormExercise = /free write|free text|writing|open text|long text|essay|sentence/.test(normalizedExerciseType)
  const isChoiceExercise = Boolean(exercise?.options?.length)
  const isShortAnswerExercise = !isChoiceExercise && !isLongFormExercise
  const isListeningExercise = /listen|listening|audio/.test(normalizedExerciseType)
  const selectedChoice = exercise?.user_answer ?? (exercise?.feedback ? '' : answer)
  const choiceIsCorrect = exercise?.feedback && exercise.score !== null && exercise.score >= 0.5
  const exerciseAudioUrl = useMemo(() => {
    const metadata = exercise?.metadata
    if (!metadata) return null
    const candidate = metadata.audio_url ?? metadata.audioUrl ?? metadata.audio_src ?? metadata.audioSource ?? metadata.audio
    if (!candidate?.trim()) return null
    const value = candidate.trim()
    if (value.startsWith('/') || value.startsWith('https://') || value.startsWith('http://')) return value
    return null
  }, [exercise?.metadata])

  useEffect(() => { setAudioLoadFailed(false); setAudioLoading(Boolean(exerciseAudioUrl)) }, [exercise?.id, exerciseAudioUrl])

  const exerciseTranscript = useMemo(() => {
    const metadata = exercise?.metadata
    if (!metadata) return null
    const candidate = metadata.transcript ?? metadata.transcript_text ?? metadata.transcriptText ?? metadata.caption ?? metadata.captions
    const value = candidate?.trim()
    return value || null
  }, [exercise?.metadata])
  const currentMastery = exercise ? attemptSummary.find((item) => item.exercise_id === exercise.id) : undefined
  const masteryScore = currentMastery?.mastery_score ?? exercise?.mastery_score ?? 0
  const masteryState = currentMastery?.mastery_state ?? exercise?.mastery_state ?? 'unseen'
  const masteryVariants = currentMastery?.mastery_variants ?? exercise?.mastery_variants ?? 0
  const progress = exercises.length ? Math.min(100, Math.round(((currentExercise + (completed || !!exercise?.feedback ? 1 : 0)) / exercises.length) * 100)) : 0
  const contentItems = useMemo(() => { const value = lesson?.content?.vocabulary; return Array.isArray(value) ? value as LessonVocabularyItem[] : [] }, [lesson])
  const finishLesson = useCallback(async () => {
    if (!lesson || completed) return
    setEvaluating(true)
    try {
      const res = await apiFetch(`/api/lessons/${lesson.id}/complete`, { method: 'POST' })
      if (!res.ok) throw new Error('complete_failed')
      const updated: LessonData = await res.json()
      setLesson(updated); setCompleted(true); completeLesson(lesson.id); setDayComplete(true)
      markLearningProgressUpdated()
    } catch { /* keep lesson active so the user can retry */ } finally { setEvaluating(false) }
  }, [lesson, completed, completeLesson])
  const loadAttempts = useCallback(async (exerciseId: number) => {
    try {
      const res = await apiFetch(`/api/lessons/exercises/${exerciseId}/attempts`)
      if (!res.ok) return
      const data: ExerciseAttempt[] = await res.json()
      setAttempts(data)
    } catch { /* attempt history is optional UI */ }
  }, [])

  const loadNativeHint = async () => {
    if (!exercise || loadingHint) return
    setLoadingHint(true)
    try {
      const res = await apiFetch(`/api/lessons/exercises/${exercise.id}/native-hint`, { method: 'POST' })
      if (!res.ok) throw new Error('hint_failed')
      const data: { native_hint: string } = await res.json()
      setNativeHint(data.native_hint)
    } catch { /* keep exercise usable when hint generation is unavailable */ } finally { setLoadingHint(false) }
  }

  const loadNativeExplanation = async () => {
    if (!exercise || loadingExplanation) return
    setLoadingExplanation(true)
    try {
      const res = await apiFetch(`/api/lessons/exercises/${exercise.id}/native-explanation`, { method: 'POST' })
      if (!res.ok) throw new Error('explanation_failed')
      const data: { native_explanation: string } = await res.json()
      setNativeExplanation(data.native_explanation)
    } catch { /* keep exercise usable when explanation generation is unavailable */ } finally { setLoadingExplanation(false) }
  }

  useEffect(() => {
    setAttempts([]); setAttemptsOpen(false); setNativeHint(null); setNativeExplanation(null)
    if (exercise) void loadAttempts(exercise.id)
  }, [exercise?.id, loadAttempts])

  const openMasteryCandidate = async (skillOverride?: string | null) => {
    if (!lesson || loadingMasteryNext) return
    setLoadingMasteryNext(true)
    try {
      const activeSkill = skillOverride === undefined ? masteryReviewSkill : skillOverride
      const reviewSessionActive = masteryReviewMode || skillOverride !== undefined
      const next = activeSkill
        ? await fetchNextSkillMasteryExercise(lesson.id, activeSkill)
        : await fetchNextMasteryExercise(lesson.id)
      if (!next) {
        setMasteryNext(null)
        if (reviewSessionActive) {
          setMasteryReviewExhausted(true)
          setMasteryReviewMode(false)
        }
        return
      }
      setMasteryReviewExhausted(false)
      setMasteryNext(next)
      const targetIndex = exercises.findIndex((item) => item.id === next.exercise.id)
      setExercises((prev) => {
        const index = prev.findIndex((item) => item.id === next.exercise.id)
        if (index < 0) return [...prev, next.exercise]
        return prev.map((item) => item.id === next.exercise.id ? { ...item, ...next.exercise } : item)
      })
      setCurrentExercise(targetIndex >= 0 ? targetIndex : exercises.length)
      setCompleted(false)
      setDayComplete(false)
      setAnswer('')
      setNativeHint(null)
      setNativeExplanation(null)
      void loadAttempts(next.exercise.id)
    } catch {
      setMasteryNext(null)
    } finally {
      setLoadingMasteryNext(false)
    }
  }

  const startMasteryReview = async () => {
    if (!lesson || loadingMasteryNext || !lessonMastery) return
    setMasteryReviewMode(true)
    setMasteryReviewCompleted(0)
    setMasteryReviewInitialRate(lessonMastery.mastery_rate)
    setMasteryReviewFinalRate(null)
    setMasteryReviewImproved(false)
    setMasteryReviewExhausted(false)
    setMasteryReviewSkill(null)
    await openMasteryCandidate(null)
  }

  const startSkillMasteryReview = async (skill: string) => {
    if (!lesson || loadingMasteryNext || !lessonMastery || !skill.trim()) return
    const selectedSkill = lessonMastery.skills.find((item) => item.skill === skill)
    setMasteryReviewMode(true)
    setMasteryReviewCompleted(0)
    setMasteryReviewInitialRate(selectedSkill?.mastery_rate ?? null)
    setMasteryReviewFinalRate(null)
    setMasteryReviewImproved(false)
    setMasteryReviewExhausted(false)
    setMasteryReviewSkill(skill)
    await openMasteryCandidate(skill)
  }

  const finishMasteryReview = () => {
    setMasteryReviewMode(false)
    setMasteryReviewSkill(null)
    setMasteryReviewExhausted(false)
    setLoadingMasteryNext(false)
  }

  const continueMasteryReview = async () => {
    if (!masteryReviewMode || masteryReviewImproved || loadingMasteryNext) return
    await openMasteryCandidate()
  }

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null
      if (target?.tagName === 'INPUT' || target?.tagName === 'TEXTAREA' || target?.isContentEditable) return
      if (event.key === 'Enter' && exercise?.feedback && !evaluating) {
        event.preventDefault()
        if (masteryReviewMode) void continueMasteryReview()
        else if (currentExercise + 1 < exercises.length) setCurrentExercise((value) => value + 1)
        else void finishLesson()
        return
      }
      if (event.key === ' ' && exercise && !exercise.feedback && !evaluating && !exercise.options) {
        event.preventDefault()
        const input = document.querySelector<HTMLInputElement>('input[placeholder]')
        input?.focus()
      }
      if (exercise?.options?.length && !exercise.feedback && !evaluating && /^[1-9]$/.test(event.key)) {
        const optionIndex = Number(event.key) - 1
        if (optionIndex < exercise.options.length) {
          event.preventDefault()
          setAnswer(exercise.options[optionIndex])
        }
      }
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [currentExercise, evaluating, exercise, exercises.length, finishLesson, masteryReviewMode, continueMasteryReview])

  const adaptiveNextExercise = async () => {
    if (!exercise || evaluating || !exercise.feedback || !hasAdaptiveTarget(exercise) || !isAdaptiveRetryAction(exercise.recommended_action)) return
    setEvaluating(true)
    try {
      const res = await apiFetch(`/api/lessons/exercises/${exercise.id}/adaptive-next`, { method: 'POST' })
      if (!res.ok) throw new Error('adaptive_next_failed')
      const payload: { action: string; recommended_variant?: string | null; exercise: ExerciseItem } = await res.json()
      const result: ExerciseItem = { ...payload.exercise, recommended_action: undefined, recommended_variant: null }
      const targetIndex = exercises.findIndex((item) => item.id === result.id)
      const nextIndex = targetIndex >= 0 ? targetIndex : exercises.length
      setExercises((prev) => {
        const index = prev.findIndex((item) => item.id === result.id)
        if (index < 0) return [...prev, result]
        return prev.map((item) => item.id === result.id ? { ...item, ...result } : item)
      })
      setCurrentExercise(nextIndex)
      setCompleted(false)
      setDayComplete(false)
      setAnswer('')
      setNativeHint(null)
      setNativeExplanation(null)
      void loadAttempts(result.id)
      if (lesson) { void loadAttemptSummary(lesson.id); void loadLessonMastery(lesson.id); if (!masteryReviewMode) void loadNextMasteryExercise(lesson.id) }
    } catch { /* keep the answered exercise visible when no adaptive variant is available */ } finally { setEvaluating(false) }
  }

  const retryExercise = async () => {
    if (!exercise || evaluating || !exercise.feedback) return
    if (exercise.recommended_variant) {
      await adaptiveNextExercise()
      return
    }
    setEvaluating(true)
    try {
      const res = await apiFetch(`/api/lessons/exercises/${exercise.id}/retry`, { method: 'POST' })
      if (!res.ok) throw new Error('retry_failed')
      const result: ExerciseItem = await res.json()
      const targetIndex = exercises.findIndex((item) => item.id === result.id)
      const nextIndex = targetIndex >= 0 ? targetIndex : exercises.length
      setExercises((prev) => {
        const index = prev.findIndex((item) => item.id === result.id)
        if (index < 0) return [...prev, result]
        return prev.map((item) => item.id === result.id ? { ...item, ...result } : item)
      })
      setCurrentExercise(nextIndex)
      setCompleted(false)
      setDayComplete(false)
      setAnswer('')
      void loadAttempts(result.id)
      if (lesson) { void loadAttemptSummary(lesson.id); void loadLessonMastery(lesson.id); if (!masteryReviewMode) void loadNextMasteryExercise(lesson.id) }
    } catch { /* keep the failed exercise visible so the user can retry later */ } finally { setEvaluating(false) }
  }

  const submitAnswer = async () => {
    if (!exercise || !answer.trim() || evaluating || exercise.feedback) return
    setEvaluating(true)
    try {
      const res = await apiFetch(`/api/lessons/exercises/${exercise.id}/answer`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ answer: answer.trim() }) })
      if (!res.ok) throw new Error('answer_failed')
      const result = await res.json()
      setExercises((prev) => prev.map((item) => item.id === exercise.id ? { ...item, ...result } : item))
      setAnswer('')
      if (masteryReviewMode) setMasteryReviewCompleted((value) => value + 1)
      void loadAttempts(exercise.id)
      if (lesson) {
        const refreshedSummary = await loadAttemptSummary(lesson.id)
        if (masteryReviewMode) {
          try {
            const currentSummary = refreshedSummary?.find((item) => item.exercise_id === exercise.id)
            if (currentSummary) {
              setExercises((prev) => prev.map((item) => item.id === exercise.id ? {
                ...item,
                mastery_score: currentSummary.mastery_score,
                mastery_state: currentSummary.mastery_state,
                mastery_variants: currentSummary.mastery_variants,
              } : item))
            }
            const candidateMastered = currentSummary?.mastery_state === 'mastered' || currentSummary?.mastered
            const masteryRes = await apiFetch(`/api/lessons/${lesson.id}/mastery`)
            if (masteryRes.ok) {
              const refreshedMastery: LessonMasterySnapshot = await masteryRes.json()
              setLessonMastery(refreshedMastery)
              setSkillMastery(refreshedMastery.skills ?? [])
              try {
                setNextSkillMastery(await fetchNextLessonSkillMastery(lesson.id))
              } catch {
                setNextSkillMastery(null)
              }
              const activeSkill = masteryReviewSkill
                ? refreshedMastery.skills.find((item) => item.skill === masteryReviewSkill)
                : null
              const reviewMastered = masteryReviewSkill
                ? activeSkill?.mastery_state === 'mastered'
                : candidateMastered
              const reviewRate = masteryReviewSkill
                ? activeSkill?.mastery_rate ?? null
                : refreshedMastery.mastery_rate
              if (
                reviewMastered ||
                (masteryReviewInitialRate !== null &&
                  reviewRate !== null &&
                  reviewRate > masteryReviewInitialRate)
              ) {
                setMasteryReviewFinalRate(reviewRate)
                setMasteryReviewImproved(true)
                setMasteryReviewMode(false)
              } else if (masteryReviewMode && result.score !== null && result.score < 0.5) {
                setMasteryNext(null)
              } else {
                // Keep skill-focused sessions scoped to the selected skill.
                void openMasteryCandidate()
              }
            }
          } catch { /* keep the review session usable when mastery refresh is unavailable */ }
        } else {
          void loadLessonMastery(lesson.id)
          void loadNextMasteryExercise(lesson.id)
        }
      }
      markLearningProgressUpdated()
    } catch { /* keep answer so the user can retry */ } finally { setEvaluating(false) }
  }

  if (!lesson) return <PageLoading />
  return (
    <main className="min-h-screen bg-[var(--juba-bg)] px-4 py-5 text-[var(--juba-text)] sm:px-7 lg:px-10">
      <div className="mx-auto max-w-5xl">
        <header className="sticky top-0 z-20 mb-5 rounded-[24px] border border-[var(--juba-border)] bg-[color:var(--juba-surface)]/95 p-3 shadow-[var(--juba-shadow)] backdrop-blur sm:p-4">
          <div className="flex items-center gap-3 sm:gap-4">
            <Link href="/courses" aria-label={t('backToPlan')} className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] text-lg font-bold text-[var(--juba-text)] transition-all hover:-translate-y-0.5 hover:bg-[var(--juba-primary-soft)]">←</Link>
            <div className="min-w-0 flex-1">
              <div className="flex items-center justify-between gap-3">
                <div className="min-w-0">
                  <p className="truncate text-[11px] font-extrabold uppercase tracking-[.16em] text-[var(--juba-muted)]">{lesson.cefr_level} · {lesson.lesson_type}</p>
                  <p className="mt-0.5 truncate text-sm font-extrabold sm:text-base">{lesson.title}</p>
                </div>
                <span className="shrink-0 rounded-full bg-[var(--juba-primary-soft)] px-3 py-1 text-xs font-extrabold text-[var(--juba-primary-dark)]">{progress}%</span>
              </div>
              <div className="mt-2 h-2.5 overflow-hidden rounded-full bg-[var(--juba-surface-soft)]" aria-hidden="true">
                <div role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress} aria-label={t('lessonProgress')} className="h-full rounded-full bg-[var(--juba-primary)] transition-[width] duration-500" style={{ width: `${progress}%` }} />
              </div>
            </div>
          </div>
        </header>
        {freemiumExhausted && <div className="mb-5"><FreemiumQuotaBanner feature="lessons" /></div>}
        {dayComplete && <div className="juba-card mb-5 border-[var(--juba-border)] bg-[var(--juba-warm-soft)] p-4 font-bold text-[var(--juba-text)]">{t('dailyGoalComplete')}</div>}
        <section className="juba-card rounded-[28px] p-6 sm:p-9">
          <div className="mb-8 rounded-[24px] border border-[var(--juba-border)] bg-[linear-gradient(135deg,var(--juba-primary-soft),var(--juba-surface))] p-5 sm:p-7">
            <div className="flex flex-wrap items-start justify-between gap-5">
              <div className="max-w-2xl">
                <p className="text-xs font-extrabold uppercase tracking-[.18em] text-[var(--juba-primary-dark)]">{t('lessonLabel')} {id}</p>
                <h1 className="mt-2 text-3xl font-black tracking-tight sm:text-5xl">{lesson.title}</h1>
                <p className="mt-3 font-medium leading-7 text-[var(--juba-muted)]">{t('lessonFlowHint')}</p>
              </div>
              <div className="rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-3 text-center shadow-sm">
                <p className="text-[11px] font-extrabold uppercase tracking-wider text-[var(--juba-muted)]">{t('exerciseProgress', { current: Math.min(currentExercise + 1, Math.max(exercises.length, 1)), total: Math.max(exercises.length, 1) })}</p>
                <p className="mt-1 text-2xl font-black text-[var(--juba-primary-dark)]">{progress}%</p>
              </div>
            </div>
          </div>
          {contentItems.length > 0 && <div className="mb-9 grid gap-4 sm:grid-cols-2">{contentItems.slice(0, 4).map((item, i) => <article key={`${item.word}-${i}`} onMouseUp={() => handleTextSelection(item.example ?? '', lesson.cefr_level)} className="rounded-[20px] border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-5"><p className="text-2xl font-bold">{item.word}</p>{item.translation && <p className="mt-2 font-semibold text-[var(--juba-primary-dark)]">{item.translation}</p>}{item.example && <p className="mt-4 text-sm font-medium text-[var(--juba-text)]">“{item.example}”</p>}{item.word && <button type="button" onClick={() => { window.getSelection()?.removeAllRanges(); handleTextSelection(item.example ?? '', lesson.cefr_level); setTimeout(() => handleSaveWord(), 0) }} className="mt-4 rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-xs font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)]">{t('saveWord')}</button>}</article>)}</div>}
          {masteryReviewMode && <div className="mb-5 rounded-2xl border border-[var(--juba-primary)] bg-[var(--juba-primary-soft)] p-4" role="status" aria-live="polite"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="text-xs font-bold uppercase tracking-[.12em] text-[var(--juba-muted)]">{t('masteryReviewSession')}</p><p className="mt-1 text-sm font-semibold">{t('masteryReviewProgress', { count: masteryReviewCompleted })}</p>{masteryReviewSkill && <p className="mt-1 text-xs font-extrabold text-[var(--juba-primary-dark)]">{t('skillMastery')}: {masteryReviewSkill}</p>}{masteryNext && <p className="mt-1 text-xs font-medium text-[var(--juba-muted)]">{masteryNext.reason === 'struggling' ? t('masteryStruggling') : masteryNext.reason === 'unseen' ? t('masteryUnseen') : t('masteryReviewLowest')}</p>}</div><button type="button" onClick={finishMasteryReview} disabled={loadingMasteryNext} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-xs font-bold disabled:opacity-40">{t('masteryReviewFinish')}</button></div></div>}
          {masteryReviewImproved && <div className="mb-5 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-warm-soft)] p-4" role="status" aria-live="polite"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="font-extrabold">{t('masteryReviewImproved')}</p><p className="mt-1 text-sm font-medium text-[var(--juba-muted)]">{t('masteryReviewImprovedDesc')}</p></div>{masteryReviewInitialRate !== null && masteryReviewFinalRate !== null && <span className="rounded-full bg-[var(--juba-surface)] px-3 py-1 text-sm font-extrabold">Δ +{Math.max(0, Math.round((masteryReviewFinalRate - masteryReviewInitialRate) * 100))}%</span>}</div><button type="button" onClick={() => setMasteryReviewImproved(false)} className="mt-3 rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-xs font-bold">{t('masteryReviewFinish')}</button></div>}
          {lessonMastery && <div className="mb-9 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-5"><div className="mb-5 flex flex-wrap items-center justify-between gap-3"><div><p className="text-xs font-bold uppercase tracking-[.12em] text-[var(--juba-muted)]">{t('masteryReview')}</p><p className="mt-1 text-sm font-medium text-[var(--juba-muted)]">{masteryNext ? (masteryNext.reason === 'struggling' ? t('masteryStruggling') : masteryNext.reason === 'unseen' ? t('masteryUnseen') : t('masteryReviewLowest')) : t('masteryReviewReady')}</p></div><button type="button" onClick={() => void startMasteryReview()} disabled={loadingMasteryNext || lessonMastery.total_exercises === lessonMastery.mastered_exercises} className="rounded-full bg-[var(--juba-primary)] px-5 py-2.5 text-sm font-bold text-[var(--juba-text)] transition-transform hover:-translate-y-0.5 disabled:opacity-40">{loadingMasteryNext ? t('masteryReviewLoading') : t('masteryReviewAction')}</button></div><div className="flex flex-wrap gap-2 text-xs font-semibold text-[var(--juba-muted)]"><span>{t('masteryStruggling')}: {lessonMastery.struggling_exercises}</span><span>·</span><span>{t('masteryUnseen')}: {lessonMastery.unseen_exercises}</span><span>·</span><span>{t('masteryLearning')}: {lessonMastery.learning_exercises}</span></div></div>}
          {nextSkillMastery && <div className="mb-4 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-primary-soft)] p-4" role="status" aria-live="polite"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="text-xs font-bold uppercase tracking-[.12em] text-[var(--juba-muted)]">{t('skillMastery')}</p><p className="mt-1 font-extrabold">{nextSkillMastery.skill.skill}</p><p className="mt-1 text-xs font-medium text-[var(--juba-muted)]">{nextSkillMastery.reason === 'struggling' ? t('masteryStruggling') : nextSkillMastery.reason === 'unseen' ? t('masteryUnseen') : t('masteryReviewLowest')}</p></div><div className="flex items-center gap-3 text-right"><div><span className="rounded-full bg-[var(--juba-surface)] px-3 py-1 text-xs font-bold">{t(`masteryStates.${nextSkillMastery.skill.mastery_state}`)}</span><p className="mt-1 text-sm font-extrabold">{Math.round(nextSkillMastery.skill.mastery_rate * 100)}%</p></div><button type="button" aria-label={`${t('skillMasteryPractice')}: ${nextSkillMastery.skill.skill}`} onClick={() => void startSkillMasteryReview(nextSkillMastery.skill.skill)} disabled={loadingMasteryNext} className="rounded-xl border border-[var(--juba-border)] bg-[var(--juba-surface)] px-3 py-2 text-xs font-extrabold disabled:opacity-50">{t('skillMasteryPractice')}</button></div></div></div>}
          {allSkillsMastered && <div className="mb-4 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-warm-soft)] p-4" role="status" aria-live="polite"><p className="font-extrabold">{t('skillMasteryComplete')}</p><p className="mt-1 text-sm font-medium text-[var(--juba-muted)]">{t('skillMasteryCompleteDesc')}</p></div>}
          {skillMastery.length > 0 && <section className="mb-9 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-5" aria-label={t('skillMastery')}><div className="mb-4"><p className="text-xs font-bold uppercase tracking-[.12em] text-[var(--juba-muted)]">{t('skillMastery')}</p><p className="mt-1 text-sm font-medium text-[var(--juba-muted)]">{t('skillMasteryDesc')}</p></div><div className="grid gap-3 sm:grid-cols-2">{[...skillMastery].sort((a, b) => skillMasteryPriority[a.mastery_state] - skillMasteryPriority[b.mastery_state] || a.mastery_rate - b.mastery_rate || a.skill.localeCompare(b.skill)).map((item) => <div key={item.skill} className="rounded-xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4"><div className="flex items-center justify-between gap-3"><div className="flex min-w-0 items-center gap-2"><span className="font-bold">{item.skill}</span><span className="rounded-full bg-[var(--juba-primary-soft)] px-2 py-0.5 text-[10px] font-bold text-[var(--juba-primary-dark)]">{t(`masteryStates.${item.mastery_state}`)}</span></div><div className="flex items-center gap-2"><span className="text-sm font-extrabold">{Math.round(item.mastery_rate * 100)}%</span>{item.mastery_state !== 'mastered' && <button type="button" aria-label={`${t('skillMasteryPractice')}: ${item.skill}`} onClick={() => void startSkillMasteryReview(item.skill)} disabled={loadingMasteryNext} className="rounded-lg border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] px-2.5 py-1.5 text-[10px] font-extrabold transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-50">{t('skillMasteryPractice')}</button>}</div></div><div className="mt-2 h-2 overflow-hidden rounded-full bg-[var(--juba-surface-soft)]"><div className="h-full rounded-full bg-[var(--juba-primary)]" style={{ width: `${Math.min(100, Math.round(item.mastery_rate * 100))}%` }} /></div><div className="mt-3 grid grid-cols-2 gap-2 text-center text-[11px] font-semibold text-[var(--juba-muted)] sm:grid-cols-4"><span>{item.mastered_exercises} {t('mastered')}</span><span>{item.learning_exercises} {t('masteryLearning')}</span><span>{item.struggling_exercises} {t('masteryStruggling')}</span><span>{item.unseen_exercises} {t('masteryUnseen')}</span></div><div className="mt-2 flex flex-wrap gap-2 text-xs font-semibold text-[var(--juba-muted)]"><span>{item.mastered_exercises}/{item.total_exercises} {t('skillMasteryMastered')}</span><span>·</span><span>{t('skillMasteryAttemptRate', { rate: Math.round(item.attempt_rate * 100) })}</span><span>·</span><span>{t('mastery', {})}: {Math.round(item.average_mastery_score * 100)}%</span><span>·</span><span>{item.covered_variants} {t('skillMasteryVariants')}</span></div></div>)}</div></section>}
          {lessonMastery && <div className="mb-9 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-5"><div className="flex flex-wrap items-end justify-between gap-3"><div><p className="text-xs font-bold uppercase tracking-[.12em] text-[var(--juba-muted)]">{t('masteryOverview')}</p><div className="mt-1 flex flex-wrap items-center gap-2"><p className="text-3xl font-extrabold">{Math.round(lessonMastery.average_mastery_score * 100)}%</p><span className="rounded-full bg-[var(--juba-primary-soft)] px-3 py-1 text-xs font-extrabold text-[var(--juba-primary-dark)]">{t(`masteryStates.${lessonMastery.mastery_state}`)}</span></div></div><div className="flex flex-wrap gap-2 text-xs font-semibold text-[var(--juba-muted)]"><span>{t('masteryCoverage', { covered: lessonMastery.covered_variants })}</span><span>·</span><span>{t('masteryAttemptRate', { rate: Math.round(lessonMastery.attempt_rate * 100) })}</span><span>·</span><span>{t('masteryRate', { rate: Math.round(lessonMastery.mastery_rate * 100) })}</span></div></div><div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-5"><div><p className="text-xs text-[var(--juba-muted)]">{t('masteryAttempted')}</p><p className="font-extrabold">{lessonMastery.attempted_exercises}</p></div><div><p className="text-xs text-[var(--juba-muted)]">{t('mastered')}</p><p className="font-extrabold">{lessonMastery.mastered_exercises}</p></div><div><p className="text-xs text-[var(--juba-muted)]">{t('masteryLearning')}</p><p className="font-extrabold">{lessonMastery.learning_exercises}</p></div><div><p className="text-xs text-[var(--juba-muted)]">{t('masteryStruggling')}</p><p className="font-extrabold">{lessonMastery.struggling_exercises}</p></div><div><p className="text-xs text-[var(--juba-muted)]">{t('masteryUnseen')}</p><p className="font-extrabold">{lessonMastery.unseen_exercises}</p></div></div><div className="mt-4 space-y-3"><div><div className="mb-1 flex items-center justify-between text-xs font-semibold text-[var(--juba-muted)]"><span>{t('masteryAttempted')}</span><span>{Math.round(lessonMastery.attempt_rate * 100)}%</span></div><div className="h-2 overflow-hidden rounded-full bg-[var(--juba-surface)]"><div className="h-full rounded-full bg-[var(--juba-primary)] transition-all" style={{ width: `${Math.min(100, Math.max(0, Math.round(lessonMastery.attempt_rate * 100)))}%` }} /></div></div><div><div className="mb-1 flex items-center justify-between text-xs font-semibold text-[var(--juba-muted)]"><span>{t('mastery')}</span><span>{Math.round(lessonMastery.mastery_rate * 100)}%</span></div><div className="h-2 overflow-hidden rounded-full bg-[var(--juba-surface)]"><div className="h-full rounded-full bg-[var(--juba-primary)] transition-all" style={{ width: `${Math.min(100, Math.max(0, Math.round(lessonMastery.mastery_rate * 100)))}%` }} /></div></div></div></div>}
          {attemptStats && <div className="mb-9 grid gap-3 sm:grid-cols-3"><div className="rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-4"><p className="text-xs font-bold text-[var(--juba-muted)]">{t('attemptsLabel')}</p><p className="mt-1 text-2xl font-extrabold">{attemptStats.totalAttempts}</p></div><div className="rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-4"><p className="text-xs font-bold text-[var(--juba-muted)]">{t('best')}</p><p className="mt-1 text-2xl font-extrabold">{Math.round(attemptStats.bestScore * 100)}%</p></div><div className="rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-4"><p className="text-xs font-bold text-[var(--juba-muted)]">{t('latest')}</p><p className="mt-1 text-2xl font-extrabold">{Math.round(attemptStats.latestScore * 100)}%</p></div></div>}{exercise && <div className="mb-9 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-4"><div className="flex flex-wrap items-center justify-between gap-3"><p className="text-xs font-bold uppercase tracking-[.12em] text-[var(--juba-muted)]">{t('mastery')}</p><span className="rounded-full bg-[var(--juba-primary-soft)] px-3 py-1 text-xs font-extrabold text-[var(--juba-primary-dark)]">{t(`masteryStates.${masteryState}`)}</span></div><div className="mt-3 flex items-end justify-between gap-4"><p className="text-2xl font-extrabold">{Math.round(masteryScore * 100)}%</p><p className="text-xs font-semibold text-[var(--juba-muted)]">{t('masteryVariants', { count: masteryVariants })}</p></div><div className="mt-3 h-2 overflow-hidden rounded-full bg-[var(--juba-surface)]"><div className="h-full rounded-full bg-[var(--juba-primary)] transition-all" style={{ width: `${Math.min(100, Math.max(0, Math.round(masteryScore * 100)))}%` }} /></div>{exercise.skills && exercise.skills.length > 0 && <div className="mt-4 flex flex-wrap items-center gap-2" aria-label={t('skillMastery')}><span className="text-xs font-extrabold text-[var(--juba-muted)]">{t('skillMastery')}:</span>{exercise.skills.map((skill) => <span key={skill} className="rounded-full bg-[var(--juba-primary-soft)] px-2.5 py-1 text-[11px] font-bold text-[var(--juba-primary-dark)]">{skill}</span>)}</div>}</div>}          {!completed && exercises.length > 1 && !masteryReviewMode && (
            <nav className="mb-4 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-3" aria-label={t('exerciseProgress', { current: currentExercise + 1, total: exercises.length })}>
              <div className="flex items-center justify-between gap-3">
                <p className="text-xs font-bold uppercase tracking-[.12em] text-[var(--juba-muted)]">{t('exerciseProgress', { current: currentExercise + 1, total: exercises.length })}</p>
                <span className="text-xs font-semibold text-[var(--juba-muted)]">{exercises.filter((item) => !!item.feedback).length}/{exercises.length}</span>
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                {exercises.map((item, index) => {
                  const answered = !!item.feedback
                  const active = index === currentExercise
                  const reachable = index <= currentExercise
                  return (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => reachable && setCurrentExercise(index)}
                      disabled={!reachable || evaluating}
                      aria-current={active ? 'step' : undefined}
                      aria-label={'Exercise ' + (index + 1) + (answered ? ' completed' : '')}
                      className={cn(
                        'flex h-9 min-w-9 items-center justify-center rounded-full border px-3 text-xs font-extrabold transition-colors disabled:cursor-not-allowed disabled:opacity-45',
                        active
                          ? 'border-[var(--juba-primary-dark)] bg-[var(--juba-primary)] text-[var(--juba-text)]'
                          : answered
                            ? 'border-[var(--juba-border)] bg-[var(--juba-surface)] text-[var(--juba-primary-dark)] hover:bg-[var(--juba-primary-soft)]'
                            : 'border-[var(--juba-border)] bg-[var(--juba-surface)] text-[var(--juba-muted)] hover:bg-[var(--juba-primary-soft)]',
                      )}
                    >
                      {answered ? '✓' : index + 1}
                    </button>
                  )
                })}
              </div>
            </nav>
          )}
          {!completed && exercise && <div className="rounded-[24px] border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-6 sm:p-8"><div className="flex items-center justify-between gap-4"><span className="rounded-full bg-[var(--juba-primary-soft)] px-3 py-1 text-xs font-bold text-[var(--juba-primary-dark)]">{t('exerciseProgress', { current: currentExercise + 1, total: exercises.length })}</span><span className="text-xs font-bold text-[var(--juba-muted)]">{variantLabel}</span></div><div className="mt-4 h-1.5 overflow-hidden rounded-full bg-[var(--juba-surface)]" aria-hidden="true"><div className="h-full rounded-full bg-[var(--juba-primary)] transition-[width] duration-300" style={{ width: `${Math.max(4, progress)}%` }} /></div><div className="mt-6 flex flex-wrap gap-2" aria-label={variantLabel}>
              <span className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-3 py-1 text-[11px] font-extrabold text-[var(--juba-muted)]">{variantLabel}</span>
            </div>
            <h2 className="mt-5 text-2xl font-bold sm:text-3xl">{exercise.question}</h2>
            {isListeningExercise && <Link href="/listening" className="mt-5 inline-flex items-center rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-sm font-bold text-[var(--juba-text)] transition-colors hover:border-[var(--juba-primary)] hover:bg-[var(--juba-primary-soft)]">{t('listeningPractice')}</Link>}
            {(exerciseAudioUrl || exerciseTranscript) && <div className="mt-5 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4" role="region" aria-label={t('listen')}>
              {exerciseAudioUrl && <div>
                <div className="mb-2 flex items-center justify-between gap-3">
                  <span className="text-sm font-extrabold text-[var(--juba-text)]">{t('listen')}</span>
                </div>
                <audio
                  controls
                  preload="metadata"
                  src={exerciseAudioUrl}
                  className="w-full"
                  aria-label={t('listen')}
                  onLoadStart={() => { setAudioLoadFailed(false); setAudioLoading(true) }}
                  onCanPlay={() => setAudioLoading(false)}
                  onLoadedMetadata={() => setAudioLoading(false)}
                  onError={() => { setAudioLoading(false); setAudioLoadFailed(true) }}
                />
                {audioLoading && !audioLoadFailed && <p className="mt-2 text-xs font-semibold text-[var(--juba-muted)]" role="status" aria-live="polite">{t('loading')}</p>}
                {audioLoadFailed && <p className="mt-2 text-xs font-semibold text-[var(--juba-muted)]" role="status" aria-live="polite">{t('audioLoadError')}</p>}
              </div>}
              {exerciseTranscript && <details className={cn('text-sm font-medium text-[var(--juba-muted)]', exerciseAudioUrl && 'mt-4 border-t border-[var(--juba-border)] pt-4')}>
                <summary className="cursor-pointer font-extrabold text-[var(--juba-text)]">{t('transcriptLabel')}</summary>
                <p className="mt-3 whitespace-pre-wrap leading-7">{exerciseTranscript}</p>
              </details>}
            </div>}
            {isChoiceExercise && <div className="mt-6" role="group" aria-label={variantLabel}>
              <p className="mb-3 text-xs font-bold text-[var(--juba-muted)]">{t('choiceKeyboardHint')}</p>
              <div className="grid gap-3 sm:grid-cols-2">{exercise.options?.map((option, optionIndex) => {
                const isSelected = selectedChoice === option
                const isCorrectOption = !!exercise.feedback && option === exercise.correct_answer
                const isWrongSelected = !!exercise.feedback && isSelected && !isCorrectOption
                return <button type="button" key={option} aria-pressed={isSelected} aria-keyshortcuts={String(optionIndex + 1)} onClick={() => !exercise.feedback && !evaluating && setAnswer(option)} disabled={evaluating || !!exercise.feedback} className={cn(
                  'group flex min-h-16 items-center gap-3 rounded-2xl border p-4 text-left font-semibold text-[var(--juba-text)] transition-all',
                  !exercise.feedback && 'border-[var(--juba-border)] bg-[var(--juba-surface)] hover:-translate-y-0.5 hover:border-[var(--juba-primary)] hover:bg-[var(--juba-primary-soft)]',
                  !exercise.feedback && isSelected && 'border-[var(--juba-primary-dark)] bg-[var(--juba-primary-soft)] shadow-sm',
                  isCorrectOption && 'border-[var(--juba-primary)] bg-[var(--juba-primary-soft)]',
                  isWrongSelected && 'border-[var(--juba-border)] bg-[var(--juba-warm-soft)]',
                  'disabled:cursor-not-allowed disabled:opacity-100',
                )}>
                  <span className={cn('flex h-8 w-8 shrink-0 items-center justify-center rounded-full border text-xs font-extrabold', isCorrectOption && 'border-[var(--juba-primary)]', isWrongSelected && 'border-[var(--juba-border)]')}>{optionIndex + 1}</span>
                  <span className="flex-1">{option}</span>
                  {isCorrectOption && <span aria-label={t('correct')} className="font-extrabold">✓</span>}
                  {isWrongSelected && <span aria-label={t('incorrect')} className="font-extrabold">×</span>}
                  {!exercise.feedback && isSelected && <span aria-hidden="true" className="font-extrabold">✓</span>}
                </button>
              })}</div>
              {exercise.feedback && !choiceIsCorrect && <p className="mt-3 text-xs font-semibold text-[var(--juba-muted)]">{t('incorrect')}: {exercise.correct_answer}</p>}
            </div>}
            {isLongFormExercise && <textarea value={answer} onChange={(e) => setAnswer(e.target.value)} className="mt-6 min-h-36 w-full resize-y rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4 font-semibold leading-7 text-[var(--juba-text)] outline-none transition-shadow focus:ring-2 focus:ring-[var(--juba-primary)]" placeholder={t('typeAnswer')} aria-label={t('typeAnswer')} disabled={evaluating || !!exercise.feedback} />}
            {isShortAnswerExercise && <input value={answer} onChange={(e) => setAnswer(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') void submitAnswer() }} className="mt-6 w-full rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4 font-semibold text-[var(--juba-text)] outline-none transition-shadow focus:ring-2 focus:ring-[var(--juba-primary)]" placeholder={t('typeAnswer')} aria-label={t('typeAnswer')} disabled={evaluating || !!exercise.feedback} />}{exercise.feedback && <div className={cn(
              'mt-5 rounded-[22px] border p-5 font-semibold',
              exercise.score !== null && exercise.score >= 0.5
                ? 'border-[var(--juba-primary)] bg-[var(--juba-primary-soft)]'
                : 'border-[var(--juba-border)] bg-[var(--juba-warm-soft)]',
            )} role="status" aria-live="polite">
              <div className="flex flex-wrap items-center gap-3">
                <span className={cn(
                  'inline-flex h-9 items-center rounded-full px-3 text-xs font-black',
                  exercise.score !== null && exercise.score >= 0.5
                    ? 'bg-[var(--juba-primary)] text-[var(--juba-text)]'
                    : 'bg-[var(--juba-surface)] text-[var(--juba-text)]',
                )}>{exercise.score !== null && exercise.score >= 0.5 ? t('correct') : t('incorrect')}</span>
                {exercise.score !== null && <span className="rounded-full bg-[var(--juba-surface)] px-3 py-1 text-xs font-extrabold">{Math.round(exercise.score * 100)}%</span>}
              </div>
              <p className="mt-3 text-base font-extrabold leading-7">{exercise.feedback}</p>
              {exercise.score !== null && exercise.score < 0.5 && <p className="mt-2 text-sm font-medium text-[var(--juba-muted)]">{t('answerFeedbackRetry')}</p>}
            </div>}<div className="mt-5 flex flex-wrap gap-3"><button type="button" onClick={() => void loadNativeHint()} disabled={loadingHint} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-sm font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-40">{loadingHint ? t('loadingHint') : t('hint')}</button><button type="button" onClick={() => void loadNativeExplanation()} disabled={loadingExplanation} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-sm font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-40">{loadingExplanation ? t('loadingExplanation') : t('explain')}</button><button type="button" aria-expanded={attemptsOpen} onClick={() => setAttemptsOpen((value) => !value)} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-sm font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)]">{attemptsOpen ? t('hideAttempts') : t('attempts', { count: attempts.length })}</button></div>{nativeHint && <div className="mt-4 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-primary-soft)] p-4 font-semibold text-[var(--juba-text)]" role="status" aria-live="polite"><span className="font-extrabold">{t('hintPrefix')}</span>{nativeHint}</div>}{nativeExplanation && <div className="mt-4 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4 font-medium text-[var(--juba-text)]" role="status" aria-live="polite"><p className="font-extrabold">{t('explanation')}</p><p className="mt-2 whitespace-pre-wrap">{nativeExplanation}</p></div>}{attemptsOpen && <div className="mt-4 overflow-hidden rounded-2xl border border-[var(--juba-border)]"><div className="bg-[var(--juba-surface)] px-4 py-3 text-sm font-extrabold">{t('attemptHistory')}</div><div className="grid grid-cols-3 gap-2 border-b border-[var(--juba-border)] p-3 text-center text-xs"><div><p className="text-[var(--juba-muted)]">{t('attemptsLabel')}</p><p className="mt-1 text-base font-extrabold">{attempts.length}</p></div><div><p className="text-[var(--juba-muted)]">{t('best')}</p><p className="mt-1 text-base font-extrabold">{attempts.length ? Math.round(Math.max(...attempts.map((item) => item.score)) * 100) : 0}%</p></div><div><p className="text-[var(--juba-muted)]">{t('latest')}</p><p className="mt-1 text-base font-extrabold">{attempts.length ? Math.round(attempts[attempts.length - 1].score * 100) : 0}%</p></div></div>{attempts.length === 0 ? <p className="p-4 text-sm font-medium text-[var(--juba-muted)]">{t('noAttempts')}</p> : <div className="divide-y divide-[var(--juba-border)]">{attempts.map((item) => <div key={item.id} className="flex flex-wrap items-center justify-between gap-3 p-4 text-sm"><div><span className="font-extrabold">#{item.attempt_number}</span><span className="ml-2 text-[var(--juba-muted)]">{(item.variant ?? t('exercise')).replace(/[_-]+/g, ' ')}</span></div><span className="font-extrabold">{Math.round(item.score * 100)}%</span></div>)}</div>}</div>}<div className="mt-6 flex flex-wrap gap-3">{!masteryReviewMode && currentExercise > 0 && <button type="button" onClick={() => setCurrentExercise((value) => Math.max(0, value - 1))} disabled={evaluating} aria-label={t('backToPlan')} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-6 py-3 font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-40">←</button>}{exercise.feedback && hasAdaptiveTarget(exercise) && isAdaptiveRetryAction(exercise.recommended_action) && <button type="button" onClick={() => void adaptiveNextExercise()} disabled={evaluating} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-6 py-3 font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-40">{normaliseAdaptiveAction(exercise.recommended_action) === 'advance_harder' ? t('retryHarderVariant') : t('retryEasierVariant')}</button>}{exercise.feedback && isAdaptiveAdvanceAction(exercise.recommended_action) && <button type="button" onClick={() => masteryReviewMode ? void continueMasteryReview() : currentExercise + 1 < exercises.length ? setCurrentExercise(currentExercise + 1) : void finishLesson()} disabled={evaluating} className="rounded-full bg-[var(--juba-primary-soft)] px-6 py-3 font-bold text-[var(--juba-text)] transition-colors hover:opacity-90 disabled:opacity-40">{t('advance')}</button>}{exercise.feedback && exercise.score !== null && exercise.score < 0.5 && !hasAdaptiveTarget(exercise) && !isAdaptiveReinforcementAction(exercise.recommended_action) && <button type="button" onClick={() => void retryExercise()} disabled={evaluating} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-6 py-3 font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-40">{t('retryEasier')}</button>}<button type="button" aria-keyshortcuts="Enter" onClick={() => void submitAnswer()} disabled={!answer.trim() || evaluating || !!exercise.feedback} className="rounded-full bg-[var(--juba-primary)] px-6 py-3 font-bold text-[var(--juba-text)] transition-transform hover:-translate-y-0.5 disabled:opacity-40">{evaluating ? t('checking') : t('checkAnswer')}</button>{exercise.feedback && <button type="button" aria-keyshortcuts="Enter" onClick={() => masteryReviewMode ? void continueMasteryReview() : currentExercise + 1 < exercises.length ? setCurrentExercise(currentExercise + 1) : void finishLesson()} disabled={evaluating || loadingMasteryNext} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-6 py-3 font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-40">{masteryReviewMode ? (loadingMasteryNext ? t('masteryReviewLoading') : t('masteryReviewNext')) : currentExercise + 1 < exercises.length ? t('next') : t('finish')}</button>}</div></div>}
          {masteryReviewExhausted && !masteryReviewMode && !masteryReviewImproved && <div className="mb-5 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-primary-soft)] p-5" role="status" aria-live="polite"><p className="font-extrabold">{masteryReviewSkill ? t('skillMasteryExhausted') : t('masteryReviewExhausted')}</p><p className="mt-1 text-sm font-medium text-[var(--juba-muted)]">{masteryReviewSkill ? t('skillMasteryExhaustedDesc', { skill: masteryReviewSkill }) : t('masteryReviewExhaustedDesc')}</p><button type="button" onClick={finishMasteryReview} className="mt-4 rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-5 py-2 font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)]">{t('masteryReviewFinish')}</button></div>}
          {completed && <div className="overflow-hidden rounded-[28px] border border-[var(--juba-border)] bg-[linear-gradient(135deg,var(--juba-primary-soft),var(--juba-warm-soft))] p-8 text-center shadow-[var(--juba-shadow)] sm:p-10">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full border-4 border-[var(--juba-primary)] bg-[var(--juba-surface)] text-2xl font-black text-[var(--juba-primary-dark)] shadow-sm" aria-hidden="true">✓</div>
            <p className="text-xs font-bold uppercase tracking-[.18em] text-[var(--juba-muted)]">{t('completed')}</p>
            <h2 className="mt-2 text-4xl font-bold">{t('niceWork')}</h2>
            <p className="mt-3 font-medium text-[var(--juba-muted)]">{t('keepLearning')}</p>
            {attemptStats && <div className="mx-auto mt-6 grid max-w-xl grid-cols-3 gap-3">
              <div className="rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4"><p className="text-xs font-bold text-[var(--juba-muted)]">{t('attemptsLabel')}</p><p className="mt-1 text-2xl font-extrabold">{attemptStats.totalAttempts}</p></div>
              <div className="rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4"><p className="text-xs font-bold text-[var(--juba-muted)]">{t('best')}</p><p className="mt-1 text-2xl font-extrabold">{Math.round(attemptStats.bestScore * 100)}%</p></div>
              <div className="rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4"><p className="text-xs font-bold text-[var(--juba-muted)]">{t('latest')}</p><p className="mt-1 text-2xl font-extrabold">{Math.round(attemptStats.latestScore * 100)}%</p></div>
            </div>}
            <div className="mt-6 flex flex-wrap justify-center gap-3"><Link href="/review" className="rounded-full bg-[var(--juba-primary)] px-6 py-3 font-bold text-[var(--juba-text)] transition-transform hover:-translate-y-0.5">{t('reviewNow')}</Link><Link href="/courses" className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-6 py-3 font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)]">{t('nextCourse')}</Link></div>
          </div>}
        </section>
      </div>
      {selectedWord && <WordTooltip word={selectedWord} pos={tooltipPos} saveState={saveState} onSave={() => void handleSaveWord()} onDismiss={dismissTooltip} labels={{ saveWord: t('saveWord'), wordSaved: t('saved'), wordSaveError: t('saveError') }} />}
    </main>
  )
}