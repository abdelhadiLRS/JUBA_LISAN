'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
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

interface ExerciseItem { id: number; exercise_type: string; question: string; options: string[] | null; correct_answer: string; explanation: string | null; native_explanation: string | null; user_answer: string | null; score: number | null; feedback: string | null; native_hint: string | null; content_id?: string | null; variant?: string | null; accepted_answers?: string[] | null; metadata?: Record<string, string> | null }
interface LessonData { id: number; title: string; lesson_type: string; cefr_level: string; content: Record<string, unknown>; is_completed: boolean }
interface LessonVocabularyItem { word?: string; definition?: string; translation?: string | null; example?: string; example_translation?: string | null; note?: string | null; reading?: string | null }
interface ExerciseAttempt { id: number; exercise_id: number; lesson_id: number; content_id?: string | null; variant?: string | null; attempt_number: number; user_answer: string; score: number; feedback: string; answered_at: string }
interface ExerciseAttemptSummary { exercise_id: number; attempts: number; best_score: number; latest_score: number; latest_variant?: string | null }

export default function LessonPage() {
  const t = useTranslations('lesson')
  const tCommon = useTranslations('common')
  const tPlan = useTranslations('plan')
  const tError = useTranslations('error')
  const locale = useLocale()
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
  const langAtLoad = useRef(activeLanguage?.code ?? null)
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
  const [attemptsOpen, setAttemptsOpen] = useState(false)
  const [nativeHint, setNativeHint] = useState<string | null>(null)
  const [nativeExplanation, setNativeExplanation] = useState<string | null>(null)
  const [loadingHint, setLoadingHint] = useState(false)
  const [loadingExplanation, setLoadingExplanation] = useState(false)

  useEffect(() => { void getGrammarTopics(activeLanguage?.code ?? 'en-GB').catch(() => undefined) }, [activeLanguage?.code])
  useEffect(() => { void fetchFreemium().catch(() => undefined) }, [fetchFreemium])
  useEffect(() => {
    let cancelled = false
    apiFetch(`/api/lessons/${id}`).then(async (res) => { if (!res.ok) throw new Error('lesson_fetch_failed'); return res.json() }).then((data: { lesson: LessonData; exercises: ExerciseItem[] }) => {
      if (!cancelled) { setLesson(data.lesson); setExercises(data.exercises || []); setCompleted(!!data.lesson.is_completed); void loadAttemptSummary(data.lesson.id) }
    }).catch(() => { if (!cancelled) router.replace('/plan') })
    return () => { cancelled = true }
  }, [id, router, loadAttemptSummary])

  const exercise = exercises[currentExercise]
  const currentVariant = exercise?.variant ?? exercise?.exercise_type ?? ''
  const progress = exercises.length ? Math.round(((currentExercise + (completed ? 1 : 0)) / exercises.length) * 100) : 0
  const contentItems = useMemo(() => { const value = lesson?.content?.vocabulary; return Array.isArray(value) ? value as LessonVocabularyItem[] : [] }, [lesson])
  const finishLesson = useCallback(async () => {
    if (!lesson || completed) return
    setEvaluating(true)
    try {
      const res = await apiFetch(`/api/lessons/${lesson.id}/complete`, { method: 'POST' })
      if (!res.ok) throw new Error('complete_failed')
      const updated: LessonData = await res.json()
      setLesson(updated); setCompleted(true); completeLesson(lesson.id); setDayComplete(true)
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

  const loadAttemptSummary = useCallback(async (lessonId: number) => {
    try {
      const res = await apiFetch(`/api/lessons/lessons/${lessonId}/attempt-summary`)
      if (!res.ok) return
      const data: ExerciseAttemptSummary[] = await res.json()
      setAttemptSummary(data)
    } catch { /* summary is optional UI */ }
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

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null
      if (target?.tagName === 'INPUT' || target?.tagName === 'TEXTAREA' || target?.isContentEditable) return
      if (event.key === 'Enter' && exercise?.feedback && !evaluating) {
        event.preventDefault()
        if (currentExercise + 1 < exercises.length) setCurrentExercise((value) => value + 1)
        else void finishLesson()
        return
      }
      if (event.key === ' ' && exercise && !exercise.feedback && !evaluating && !exercise.options) {
        event.preventDefault()
        const input = document.querySelector<HTMLInputElement>('input[placeholder]')
        input?.focus()
      }
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [currentExercise, evaluating, exercise, exercises.length, finishLesson])

  const retryExercise = async () => {
    if (!exercise || evaluating || !exercise.feedback) return
    setEvaluating(true)
    try {
      const res = await apiFetch(`/api/lessons/exercises/${exercise.id}/retry`, { method: 'POST' })
      if (!res.ok) throw new Error('retry_failed')
      const result: ExerciseItem = await res.json()
      setExercises((prev) => {
        const index = prev.findIndex((item) => item.id === result.id)
        if (index < 0) return [...prev, result]
        return prev.map((item) => item.id === result.id ? { ...item, ...result } : item)
      })
      const targetIndex = exercises.findIndex((item) => item.id === result.id)
      setCurrentExercise(targetIndex >= 0 ? targetIndex : exercises.length)
      setAnswer('')
      void loadAttempts(result.id)
    } catch { /* keep the failed exercise visible so the user can retry later */ } finally { setEvaluating(false) }
  }

  const submitAnswer = async () => {
    if (!exercise || !answer.trim() || evaluating || exercise.feedback) return
    setEvaluating(true)
    try {
      const res = await apiFetch(`/api/lessons/exercises/${exercise.id}/answer`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ answer: answer.trim() }) })
      if (!res.ok) throw new Error('answer_failed')
      const result = await res.json()
      setExercises((prev) => prev.map((item) => item.id === exercise.id ? { ...item, ...result } : item)); setAnswer(''); void loadAttempts(exercise.id)
    } catch { /* keep answer so the user can retry */ } finally { setEvaluating(false) }
  }

  if (!lesson) return <PageLoading />
  return (
    <main className="min-h-screen bg-[var(--juba-bg)] px-4 py-5 text-[var(--juba-text)] sm:px-7 lg:px-10">
      <div className="mx-auto max-w-5xl">
        <header className="sticky top-0 z-20 mb-5 rounded-[22px] border border-[var(--juba-border)] bg-[color:var(--juba-surface)]/95 p-4 shadow-[var(--juba-shadow)] backdrop-blur"><div className="flex items-center gap-4"><Link href="/courses" className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] px-3 py-2 text-sm font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)]">←</Link><div className="min-w-0 flex-1"><div className="flex items-center justify-between gap-3"><p className="truncate text-xs font-bold uppercase tracking-[.16em] text-[var(--juba-muted)]">{lesson.cefr_level} · {lesson.lesson_type}</p><span className="text-sm font-bold text-[var(--juba-text)]">{progress}%</span></div><div className="mt-2 h-2 overflow-hidden rounded-full bg-[var(--juba-surface-soft)]"><div className="h-full rounded-full bg-[var(--juba-primary)] transition-all" style={{ width: `${progress}%` }} /></div></div></div></header>
        {freemiumExhausted && <div className="mb-5"><FreemiumQuotaBanner feature="lessons" /></div>}
        {dayComplete && <div className="juba-card mb-5 border-[var(--juba-border)] bg-[var(--juba-warm-soft)] p-4 font-bold text-[var(--juba-text)]">Daily goal complete — keep your streak alive.</div>}
        <section className="juba-card rounded-[28px] p-6 sm:p-9">
          <div className="mb-8"><p className="text-xs font-bold uppercase tracking-[.18em] text-[var(--juba-muted)]">LESSON {id}</p><h1 className="mt-2 text-3xl font-bold tracking-tight sm:text-5xl">{lesson.title}</h1><p className="mt-3 max-w-2xl font-medium text-[var(--juba-muted)]">Learn → practice → recall. Stay active and make every answer count.</p></div>
          {contentItems.length > 0 && <div className="mb-9 grid gap-4 sm:grid-cols-2">{contentItems.slice(0, 4).map((item, i) => <article key={`${item.word}-${i}`} onMouseUp={() => handleTextSelection(item.example ?? '', lesson.cefr_level)} className="rounded-[20px] border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-5"><p className="text-2xl font-bold">{item.word}</p>{item.translation && <p className="mt-2 font-semibold text-[var(--juba-primary-dark)]">{item.translation}</p>}{item.example && <p className="mt-4 text-sm font-medium text-[var(--juba-text)]">“{item.example}”</p>}{item.word && <button onClick={() => { window.getSelection()?.removeAllRanges(); handleTextSelection(item.example ?? '', lesson.cefr_level); setTimeout(() => handleSaveWord(), 0) }} className="mt-4 rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-xs font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)]">{t('saveWord')}</button>}</article>)}</div>}
          {attemptSummary.length > 0 && stats}          {!completed && exercise && <div className="rounded-[24px] border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] p-6 sm:p-8"><div className="flex items-center justify-between gap-4"><span className="rounded-full bg-[var(--juba-primary-soft)] px-3 py-1 text-xs font-bold text-[var(--juba-primary-dark)]">Exercise {currentExercise + 1}/{exercises.length}</span><span className="text-xs font-bold text-[var(--juba-muted)]">{currentVariant.replace('_', ' ')}</span></div><h2 className="mt-6 text-2xl font-bold sm:text-3xl">{exercise.question}</h2>{exercise.options && <div className="mt-6 grid gap-3 sm:grid-cols-2">{exercise.options.map((option) => <button key={option} onClick={() => setAnswer(option)} className={cn('rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4 text-left font-semibold text-[var(--juba-text)] transition-colors hover:border-[var(--juba-primary)] hover:bg-[var(--juba-primary-soft)]', answer === option && 'border-[var(--juba-primary-dark)] bg-[var(--juba-primary-soft)]')}>{option}</button>)}</div>}{!exercise.options && <input value={answer} onChange={(e) => setAnswer(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') void submitAnswer() }} className="mt-6 w-full rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4 font-semibold text-[var(--juba-text)] outline-none transition-shadow focus:ring-2 focus:ring-[var(--juba-primary)]" placeholder={t('typeAnswer')} aria-label={t('typeAnswer')} disabled={evaluating || !!exercise.feedback} />}{exercise.feedback && <div className="mt-5 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-warm-soft)] p-4 font-semibold text-[var(--juba-text)]">{exercise.feedback}</div>}<div className="mt-5 flex flex-wrap gap-3"><button onClick={() => void loadNativeHint()} disabled={loadingHint} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-sm font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-40">{loadingHint ? t('loadingHint') : t('hint')}</button><button onClick={() => void loadNativeExplanation()} disabled={loadingExplanation} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-sm font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-40">{loadingExplanation ? t('loadingExplanation') : t('explain')}</button><button onClick={() => setAttemptsOpen((value) => !value)} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2 text-sm font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)]">{attemptsOpen ? t('hideAttempts') : t('attempts', { count: attempts.length })}</button></div>{nativeHint && <div className="mt-4 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-primary-soft)] p-4 font-semibold text-[var(--juba-text)]"><span className="font-extrabold">{t('hintPrefix')}</span>{nativeHint}</div>}{nativeExplanation && <div className="mt-4 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] p-4 font-medium text-[var(--juba-text)]"><p className="font-extrabold">{t('explanation')}</p><p className="mt-2 whitespace-pre-wrap">{nativeExplanation}</p></div>}{attemptsOpen && <div className="mt-4 overflow-hidden rounded-2xl border border-[var(--juba-border)]"><div className="bg-[var(--juba-surface)] px-4 py-3 text-sm font-extrabold">{t('attemptHistory')}</div><div className="grid grid-cols-3 gap-2 border-b border-[var(--juba-border)] p-3 text-center text-xs"><div><p className="text-[var(--juba-muted)]">{t('attemptsLabel')}</p><p className="mt-1 text-base font-extrabold">{attempts.length}</p></div><div><p className="text-[var(--juba-muted)]">{t('best')}</p><p className="mt-1 text-base font-extrabold">{attempts.length ? Math.round(Math.max(...attempts.map((item) => item.score)) * 100) : 0}%</p></div><div><p className="text-[var(--juba-muted)]">{t('latest')}</p><p className="mt-1 text-base font-extrabold">{attempts.length ? Math.round(attempts[attempts.length - 1].score * 100) : 0}%</p></div></div>{attempts.length === 0 ? <p className="p-4 text-sm font-medium text-[var(--juba-muted)]">{t('noAttempts')}</p> : <div className="divide-y divide-[var(--juba-border)]">{attempts.map((item) => <div key={item.id} className="flex flex-wrap items-center justify-between gap-3 p-4 text-sm"><div><span className="font-extrabold">#{item.attempt_number}</span><span className="ml-2 text-[var(--juba-muted)]">{item.variant ?? 'exercise'}</span></div><span className="font-extrabold">{Math.round(item.score * 100)}%</span></div>)}</div>}</div>}<div className="mt-6 flex flex-wrap gap-3">{exercise.feedback && exercise.score !== null && exercise.score < 0.5 && <button onClick={() => void retryExercise()} disabled={evaluating} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-6 py-3 font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-40">{t('retryEasier')}</button>}<button onClick={() => void submitAnswer()} disabled={!answer.trim() || evaluating || !!exercise.feedback} className="rounded-full bg-[var(--juba-primary)] px-6 py-3 font-bold text-[var(--juba-text)] transition-transform hover:-translate-y-0.5 disabled:opacity-40">{evaluating ? t('checking') : t('checkAnswer')}</button>{exercise.feedback && <button onClick={() => currentExercise + 1 < exercises.length ? setCurrentExercise(currentExercise + 1) : void finishLesson()} disabled={evaluating} className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-6 py-3 font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)] disabled:opacity-40">{currentExercise + 1 < exercises.length ? t('next') : t('finish')}</button>}</div></div>}
          {completed && <div className="rounded-[24px] border border-[var(--juba-border)] bg-[var(--juba-warm-soft)] p-8 text-center"><p className="text-xs font-bold uppercase tracking-[.18em] text-[var(--juba-muted)]">{t('completed')}</p><h2 className="mt-2 text-4xl font-bold">{t('niceWork')}</h2><p className="mt-3 font-medium text-[var(--juba-muted)]">{t('keepLearning')}</p><div className="mt-6 flex flex-wrap justify-center gap-3"><Link href="/review" className="rounded-full bg-[var(--juba-primary)] px-6 py-3 font-bold text-[var(--juba-text)] transition-transform hover:-translate-y-0.5">{t('reviewNow')}</Link><Link href="/courses" className="rounded-full border border-[var(--juba-border)] bg-[var(--juba-surface)] px-6 py-3 font-bold text-[var(--juba-text)] transition-colors hover:bg-[var(--juba-primary-soft)]">{t('nextCourse')}</Link></div></div>}
        </section>
      </div>
      {selectedWord && <WordTooltip word={selectedWord} pos={tooltipPos} saveState={saveState} onSave={() => void handleSaveWord()} onDismiss={dismissTooltip} labels={{ saveWord: t('saveWord'), wordSaved: t('saved'), wordSaveError: t('saveError') }} />}
    </main>
  )
}
