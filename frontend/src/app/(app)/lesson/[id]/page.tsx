'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useProgressStore } from '@/store/progress'
import { useLanguageStore } from '@/store/language'
import { useAuthStore, isSubscribed, isFreemiumTrialActive } from '@/store/auth'
import { getGrammarTopics, type GrammarTopic } from '@/data/grammar'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { VoiceRecorder } from '@/components/ui/VoiceRecorder'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { WordTooltip, useWordSave } from '@/components/ui/WordTooltip'
import { PageLoading } from '@/components/ui/page-loading'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { useFreemiumStore } from '@/store/freemium'
import { useConfigStore } from '@/store/config'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { ReviewPrompt, getReviewPromptDismissal } from '@/components/reviews/ReviewPrompt'
import { shouldShowUnitReviewPrompt } from '@/lib/review-prompt-triggers'
import { cn } from '@/lib/utils'
import { formatLanguageName, getTargetLanguageTextClass } from '@/lib/target-languages'

interface ExerciseItem { id: number; exercise_type: string; question: string; options: string[] | null; correct_answer: string; explanation: string | null; native_explanation: string | null; user_answer: string | null; score: number | null; feedback: string | null; native_hint: string | null }
interface LessonData { id: number; title: string; lesson_type: string; cefr_level: string; content: Record<string, unknown>; is_completed: boolean }
interface LessonVocabularyItem { word?: string; definition?: string; translation?: string | null; example?: string; example_translation?: string | null; note?: string | null; reading?: string | null }
function getLessonUnitId(lesson: LessonData | null): string | null { const unitId = lesson?.content?.unit_id; return typeof unitId === 'string' && unitId ? unitId : null }

export default function LessonPage() {
  const t = useTranslations('lesson'); const tCommon = useTranslations('common'); const tPlan = useTranslations('plan'); const tError = useTranslations('error'); const tLang = useTranslations('languages'); const locale = useLocale(); const params = useParams(); const router = useRouter(); const id = params.id as string
  const completeLesson = useProgressStore((s) => s.completeLesson); const activeLanguage = useLanguageStore((s) => s.activeLanguage); const user = useAuthStore((s) => s.user); const stripeEnabled = useConfigStore((s) => s.stripeEnabled); const fetchFreemium = useFreemiumStore((s) => s.fetchStatus); const freemiumStatus = useFreemiumStore((s) => s.status)
  const freemiumExhausted = stripeEnabled && !isSubscribed(user, stripeEnabled) && !isFreemiumTrialActive(user, stripeEnabled) && freemiumStatus && freemiumStatus.lessons_remaining <= 0
  const nativeLanguageName = user?.native_language ? formatLanguageName(tLang(user.native_language), locale) : ''; const langAtLoad = useRef(activeLanguage?.code ?? null)
  const { selectedWord, tooltipPos, saveState, handleTextSelection, handleSaveWord, dismissTooltip } = useWordSave()
  const [lesson, setLesson] = useState<LessonData | null>(null); const [exercises, setExercises] = useState<ExerciseItem[]>([]); const [currentExercise, setCurrentExercise] = useState(0); const [answer, setAnswer] = useState(''); const [evaluating, setEvaluating] = useState(false); const [completed, setCompleted] = useState(false); const [dayComplete, setDayComplete] = useState(false); const [reviewPromptOpen, setReviewPromptOpen] = useState(false); const [progressDayAtStart, setProgressDayAtStart] = useState(-1); const [grammarTopics, setGrammarTopics] = useState<GrammarTopic[]>([])

  useEffect(() => { getGrammarTopics(activeLanguage?.code ?? 'en-GB').then(setGrammarTopics).catch(() => setGrammarTopics([])) }, [activeLanguage?.code])
  useEffect(() => { fetchFreemium().catch(() => undefined) }, [fetchFreemium])

  const exercise = exercises[currentExercise]; const progress = exercises.length ? Math.round(((currentExercise + (completed ? 1 : 0)) / exercises.length) * 100) : 0
  const contentItems = useMemo(() => { const value = lesson?.content?.vocabulary; return Array.isArray(value) ? value as LessonVocabularyItem[] : [] }, [lesson])

  const finishLesson = useCallback(() => { if (!lesson) return; setCompleted(true); completeLesson(lesson.id); setDayComplete(true) }, [lesson, completeLesson])
  const submitAnswer = async () => {
    if (!exercise || !answer.trim() || evaluating) return; setEvaluating(true)
    try { const result = await apiFetch(`/lessons/${id}/exercises/${exercise.id}/answer`, { method: 'POST', body: JSON.stringify({ answer: answer.trim() }) }); setExercises((prev) => prev.map((item) => item.id === exercise.id ? { ...item, ...result } : item)); setAnswer('') } catch { setAnswer('') } finally { setEvaluating(false) }
  }

  if (!lesson) return <PageLoading />
  return (
    <main className="min-h-screen bg-[var(--juba-paper,#f7f4ea)] px-4 py-5 sm:px-7 lg:px-10">
      <div className="mx-auto max-w-5xl">
        <header className="sticky top-0 z-20 mb-5 rounded-[24px] border-2 border-neutral-950 bg-white/95 p-4 shadow-[5px_5px_0_rgba(17,17,17,.9)] backdrop-blur dark:bg-neutral-900/95">
          <div className="flex items-center gap-4"><Link href="/courses" className="rounded-full border-2 border-neutral-950 px-3 py-2 text-sm font-black">←</Link><div className="min-w-0 flex-1"><div className="flex items-center justify-between gap-3"><p className="truncate text-xs font-black uppercase tracking-[.18em] text-neutral-500">{lesson.cefr_level} · {lesson.lesson_type}</p><span className="text-sm font-black">{progress}%</span></div><div className="mt-2 h-3 overflow-hidden rounded-full border-2 border-neutral-950 bg-white"><div className="h-full rounded-full bg-[#d8f53f] transition-all" style={{ width: `${progress}%` }} /></div></div></div>
        </header>

        {freemiumExhausted && <div className="mb-5"><FreemiumQuotaBanner /></div>}
        {dayComplete && <div className="mb-5 rounded-[24px] border-2 border-neutral-950 bg-[#d8f53f] p-4 font-black shadow-[4px_4px_0_rgba(17,17,17,.9)]">Daily goal complete — keep your streak alive.</div>}

        <section className="rounded-[32px] border-2 border-neutral-950 bg-white p-6 shadow-[8px_8px_0_rgba(17,17,17,.9)] dark:bg-neutral-900 sm:p-9">
          <div className="mb-8"><p className="text-xs font-black uppercase tracking-[.2em] text-neutral-500">LESSON {id}</p><h1 className="mt-2 text-3xl font-black tracking-tight sm:text-5xl">{lesson.title}</h1><p className="mt-3 max-w-2xl font-semibold text-neutral-600 dark:text-neutral-300">Learn → practice → recall. Stay active and make every answer count.</p></div>

          {contentItems.length > 0 && <div className="mb-9 grid gap-4 sm:grid-cols-2">{contentItems.slice(0, 4).map((item, i) => <article key={`${item.word}-${i}`} onMouseUp={handleTextSelection} className="rounded-[24px] border-2 border-neutral-950 bg-[#f7f4ea] p-5 dark:bg-neutral-800"><p className="text-2xl font-black">{item.word}</p>{item.translation && <p className="mt-2 font-bold text-neutral-600 dark:text-neutral-300">{item.translation}</p>}{item.example && <p className="mt-4 text-sm font-semibold">“{item.example}”</p>}<button onClick={() => item.word && handleSaveWord(item.word)} className="mt-4 rounded-full border-2 border-neutral-950 bg-white px-4 py-2 text-xs font-black">+ Save</button></article>)}</div>}

          {!completed && exercise && <div className="rounded-[28px] border-2 border-neutral-950 p-6 sm:p-8"><div className="flex items-center justify-between gap-4"><span className="rounded-full bg-neutral-950 px-3 py-1 text-xs font-black text-white">Exercise {currentExercise + 1}/{exercises.length}</span><span className="text-xs font-black text-neutral-500">Active recall</span></div><h2 className="mt-6 text-2xl font-black sm:text-3xl">{exercise.question}</h2>{exercise.options && <div className="mt-6 grid gap-3 sm:grid-cols-2">{exercise.options.map((option) => <button key={option} onClick={() => setAnswer(option)} className={cn('rounded-2xl border-2 border-neutral-950 p-4 text-left font-bold', answer === option && 'bg-[#d8f53f]')}>{option}</button>)}</div>}{!exercise.options && <input value={answer} onChange={(e) => setAnswer(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') submitAnswer() }} className="mt-6 w-full rounded-2xl border-2 border-neutral-950 bg-white p-4 font-bold outline-none" placeholder="Type your answer…" />}{exercise.feedback && <div className="mt-5 rounded-2xl border-2 border-neutral-950 bg-[#d8f53f] p-4 font-semibold">{exercise.feedback}</div>}<div className="mt-6 flex flex-wrap gap-3"><button onClick={submitAnswer} disabled={!answer.trim() || evaluating} className="rounded-full border-2 border-neutral-950 bg-[#d8f53f] px-6 py-3 font-black disabled:opacity-40">{evaluating ? 'Checking…' : 'Check answer'}</button>{exercise.feedback && <button onClick={() => currentExercise + 1 < exercises.length ? setCurrentExercise(currentExercise + 1) : finishLesson()} className="rounded-full border-2 border-neutral-950 bg-white px-6 py-3 font-black">{currentExercise + 1 < exercises.length ? 'Next' : 'Finish lesson'}</button>}</div></div>}
          {completed && <div className="rounded-[28px] border-2 border-neutral-950 bg-[#d8f53f] p-8 text-center"><p className="text-xs font-black uppercase tracking-[.2em]">Completed</p><h2 className="mt-2 text-4xl font-black">Nice work. You remembered.</h2><p className="mt-3 font-semibold">Keep the momentum going with a review.</p><div className="mt-6 flex flex-wrap justify-center gap-3"><Link href="/review" className="rounded-full border-2 border-neutral-950 bg-white px-6 py-3 font-black">Review now</Link><Link href="/courses" className="rounded-full border-2 border-neutral-950 px-6 py-3 font-black">Next course</Link></div></div>}
        </section>
      </div>
      {selectedWord && <WordTooltip word={selectedWord} position={tooltipPos} saveState={saveState} onSave={handleSaveWord} onDismiss={dismissTooltip} />}
    </main>
  )
}
