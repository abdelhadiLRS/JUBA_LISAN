'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { BookOpen, Flame, Sparkles, Target, ArrowRight } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import {
  isSubscribed,
  needsPaymentRecovery,
  isFreemiumTrialActive,
  useAuthStore,
} from '@/store/auth'
import { useProgressStore } from '@/store/progress'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'
import OnboardingTour from '@/components/tour/OnboardingTour'
import WhatsNew from '@/components/whats-new/WhatsNew'
import { PageLoading } from '@/components/ui/page-loading'
import { SubscriptionPlanButtons } from '@/components/billing/SubscriptionPlanButtons'
import { DashboardAnnouncement } from '@/components/dashboard/DashboardAnnouncement'

interface TodayLessonItem {
  id: number | null
  title: string
  lessonType: string
  week: number
  day: number
  objectives: string[]
  estimatedMinutes: number
  isCompleted: boolean
}

const SUPPORTED_LESSON_TYPES = new Set([
  'grammar',
  'vocabulary',
  'reading',
  'writing',
  'listening',
  'conversation',
  'review',
  'level_test',
])

function normalizeLessonType(value: unknown): string {
  if (typeof value !== 'string') return 'review'
  const normalized = value.trim().toLowerCase()
  return SUPPORTED_LESSON_TYPES.has(normalized) ? normalized : 'review'
}

function getLessonTypeLabelKey(value: unknown): string {
  return `lessonTypes.${normalizeLessonType(value)}`
}

function normalizeDashboardLessons(value: unknown): TodayLessonItem[] {
  if (!Array.isArray(value)) return []

  return value
    .filter(
      (item): item is Record<string, unknown> =>
        Boolean(item && typeof item === 'object' && !Array.isArray(item))
    )
    .map((item) => ({
      id: typeof item.id === 'number' && Number.isFinite(item.id) ? item.id : null,
      title:
        typeof item.title === 'string' && item.title.trim()
          ? item.title
          : 'Lesson',
      lessonType: normalizeLessonType((item as any).lesson_type || item.lessonType),
      week:
        typeof item.week === 'number' && Number.isFinite(item.week)
          ? item.week
          : 0,
      day:
        typeof item.day === 'number' && Number.isFinite(item.day)
          ? item.day
          : 0,
      objectives: Array.isArray(item.objectives)
        ? item.objectives.filter(
            (objective): objective is string => typeof objective === 'string'
          )
        : [],
      estimatedMinutes:
        typeof (item as any).estimated_minutes === 'number' &&
        Number.isFinite((item as any).estimated_minutes)
          ? (item as any).estimated_minutes
          : typeof item.estimatedMinutes === 'number' &&
            Number.isFinite(item.estimatedMinutes) &&
            item.estimatedMinutes > 0
            ? item.estimatedMinutes
            : 25,
      isCompleted: typeof (item as any).is_completed === 'boolean' ? (item as any).is_completed : Boolean(item.isCompleted),
    }))
}

const btnPrimary =
  'inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold text-white transition-colors disabled:opacity-50'
const btnSecondary =
  'inline-flex items-center justify-center gap-2 rounded-xl border border-fl-border px-4 py-2.5 text-sm font-medium transition-colors hover:bg-[var(--juba-surface-soft)]'

export default function DashboardPage() {
  const t = useTranslations('dashboard')
  const tBilling = useTranslations('billing')
  const tNav = useTranslations('nav')
  const tPlan = useTranslations('plan')
  const tTarget = useTranslations('targetLanguages')
  const tError = useTranslations('error')
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const trialEligible = !user?.trial_used
  const freemiumTrialActive = isFreemiumTrialActive(user, stripeEnabled)
  const [freemiumTrialDaysLeft, setFreemiumTrialDaysLeft] = useState(0)
  
  // Daily Momentum State - answers three core questions
  const [nextAction, setNextAction] = useState<TodayLessonItem | null>(null) // What should I do now?
  const [reviewDueCount, setReviewDueCount] = useState(0) // What is due for review?
  const [goalProgress, setGoalProgress] = useState({ current: 0, target: 0 }) // How close to today's XP goal?

  useEffect(() => {
    if (freemiumTrialActive && user?.freemium_trial_ends_at) {
      const days = Math.max(
        1,
        Math.ceil(
          (new Date(user.freemium_trial_ends_at).getTime() - Date.now()) /
            86400000
        )
      )
      setFreemiumTrialDaysLeft(days)
    }
  }, [freemiumTrialActive, user?.freemium_trial_ends_at])

  const {
    streak,
    xp,
    skills,
    todayLessons,
    completedToday,
    setProgress,
    setTodayLessons,
  } = useProgressStore()
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [hasPlan, setHasPlan] = useState(false)
  const [cefrLevel, setCefrLevel] = useState<string | null>(null)
  const [progressDay, setProgressDay] = useState(0)
  const [totalDays, setTotalDays] = useState(0)
  const [pendingCount, setPendingCount] = useState(0)
  const [totalLessons, setTotalLessons] = useState(0)
  const [totalExercises, setTotalExercises] = useState(0)
  const [exercisesCorrect, setExercisesCorrect] = useState(0)
  const [accuracy, setAccuracy] = useState(0)
  const [vocabularyLevel, setVocabularyLevel] = useState<string | null>(null)
  const [vocabularyMastered, setVocabularyMastered] = useState(0)
  const [vocabularyTotal, setVocabularyTotal] = useState(0)
  const [vocabularyProgress, setVocabularyProgress] = useState(0)
  const [skipping, setSkipping] = useState(false)
  const [skipError, setSkipError] = useState(false)
  const [portalLoading, setPortalLoading] = useState(false)
  const [portalError, setPortalError] = useState<string | null>(null)

  const loadData = useCallback(async () => {
    try {
      const [progRes, planRes, goalRes] = await Promise.all([
        apiFetch('/api/progress/summary'),
        apiFetch('/api/study-plan/today'),
        apiFetch('/api/progress/goals'),
      ])
      if (progRes.ok) {
        const prog = await progRes.json()
        setProgress({
          streak: prog.current_streak ?? 0,
          xp: prog.total_xp ?? 0,
          skills: prog.skills ?? {},
        })
        setTotalLessons(prog.total_lessons ?? 0)
        setTotalExercises(prog.total_exercises ?? 0)
        setExercisesCorrect(prog.exercises_correct ?? 0)
        setAccuracy(prog.accuracy ?? 0)
        setVocabularyLevel(prog.vocabulary_level ?? null)
        setVocabularyMastered(prog.vocabulary_mastered ?? 0)
        setVocabularyTotal(prog.vocabulary_total ?? 0)
        setVocabularyProgress(prog.vocabulary_progress ?? 0)
        
        if (goalRes.ok) {
          const goal = await goalRes.json()
          setGoalProgress({
            current: Math.max(0, Number(goal.daily_xp) || 0),
            target: Math.max(1, Number(goal.daily_xp_target) || 50),
          })
        }
      } else {
        setProgress({ streak: 0, xp: 0, skills: {} })
        setTotalLessons(0)
        setTotalExercises(0)
        setExercisesCorrect(0)
        setAccuracy(0)
        setVocabularyLevel(null)
        setVocabularyMastered(0)
        setVocabularyTotal(0)
        setVocabularyProgress(0)
      }
      if (!goalRes.ok) {
        setGoalProgress((current) => ({
          current: current.current,
          target: current.target || 50,
        }))
      }
      if (planRes.ok) {
        const plan = await planRes.json()
        setCefrLevel(plan.cefr_level ?? null)
        setProgressDay(plan.progress_day ?? 0)
        setTotalDays(plan.total_days ?? 0)
        setPendingCount(plan.pending_count ?? 0)
        setReviewDueCount(
          typeof plan.review_due_count === 'number' && Number.isFinite(plan.review_due_count)
            ? Math.max(0, plan.review_due_count)
            : 0
        )
        const normalizedLessons = normalizeDashboardLessons(plan.lessons)
        setTodayLessons(normalizedLessons)
        
        // Daily Momentum: Set next action. Review count comes from the same
        // study-plan response so the dashboard has one consistent source of truth.
        const next = normalizedLessons.find(l => !l.isCompleted && l.id !== null) || null
        setNextAction(next)
        setHasPlan(true)
      } else {
        setCefrLevel(null)
        setProgressDay(0)
        setTotalDays(0)
        setPendingCount(0)
        setTodayLessons([])
        setNextAction(null)
        setReviewDueCount(0)
        setHasPlan(false)
      }
    } catch {
      setLoadError(true)
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- re-fetch when active language changes
  }, [setProgress, setTodayLessons, activeLanguage?.code])

  useEffect(() => {
    loadData()
  }, [loadData])

  async function skipDay() {
    if (skipping) return
    setSkipping(true)
    try {
      await apiFetch('/api/study-plan/skip-day', { method: 'POST' })
      await loadData()
    } catch {
      setSkipError(true)
    } finally {
      setSkipping(false)
    }
  }

  async function handleManageSubscription() {
    setPortalLoading(true)
    setPortalError(null)
    try {
      const res = await apiFetch('/api/billing/portal', { method: 'POST' })
      if (!res.ok) throw new Error(tBilling('portalError'))
      const { url } = await res.json()
      window.location.assign(url)
    } catch (err) {
      setPortalError(
        err instanceof Error ? err.message : tBilling('portalError')
      )
      setPortalLoading(false)
    }
  }

  if (loading) {
    return <PageLoading label={t('loadingProgress')} minHeight="min-h-screen" />
  }

  if (loadError) {
    return (
    <>
      <OnboardingTour />
      <WhatsNew />
      <div className="mx-auto max-w-[1180px] px-4 py-6 sm:px-6 lg:py-10">
        <section className="relative mb-7 overflow-hidden rounded-[34px] bg-[#6c45f5] px-6 py-7 text-white shadow-[0_18px_45px_rgba(108,69,245,.22)] sm:px-9 sm:py-9">
          <div className="pointer-events-none absolute -end-10 -top-16 h-48 w-48 rounded-full bg-[#ffd85a] opacity-90" />
          <div className="pointer-events-none absolute -bottom-24 start-1/3 h-48 w-48 rounded-full bg-[#ff8d79] opacity-70" />
          <div className="relative z-10 max-w-2xl">
            <p className="mb-2 text-sm font-bold tracking-wide text-white/75">{t('welcomeBack')}</p>
            <h1 className="text-3xl font-black tracking-[-.04em] sm:text-5xl">{user?.displayName || user?.username} 👋</h1>
            <p className="mt-3 max-w-xl text-sm leading-6 text-white/80 sm:text-base">
              {activeLanguage ? tTarget(activeLanguage.code) : ''}{cefrLevel ? ` · ${cefrLevel}` : ''}
            </p>
            {nextAction ? (
              <Link href={`/lesson/${nextAction.id}`} className="mt-6 inline-flex rounded-2xl bg-[#ffd85a] px-5 py-3 text-sm font-black text-[#242033] shadow-[0_5px_0_#c79e18] transition-transform hover:-translate-y-0.5">
                {t('startLesson')} <ArrowRight className="ms-2 h-4 w-4" />
              </Link>
            ) : !hasPlan ? (
              <Link href="/assessment" className="mt-6 inline-flex rounded-2xl bg-[#ffd85a] px-5 py-3 text-sm font-black text-[#242033] shadow-[0_5px_0_#c79e18]">
                {t('takeAssessmentArrow')}
              </Link>
            ) : null}
          </div>
        </section>

        <div className="mb-7 grid grid-cols-2 gap-3 md:grid-cols-4">
          {[
            { label: t('streak'), value: `${streak}d`, Icon: Flame, bg: '#fff0a8' },
            { label: t('xp'), value: xp, Icon: Sparkles, bg: '#e7ddff' },
            { label: t('lessonsCompleted'), value: totalLessons, Icon: BookOpen, bg: '#c9f5e3' },
            { label: t('accuracy'), value: totalExercises > 0 ? `${Math.round(accuracy * 100)}%` : '—', Icon: Target, bg: '#ffd9d0' },
          ].map(({ label, value, Icon, bg }) => (
            <div key={label} className="rounded-[24px] bg-white p-4 shadow-[0_12px_30px_rgba(39,28,72,.07)] sm:p-5">
              <span className="mb-3 flex h-10 w-10 items-center justify-center rounded-2xl" style={{ background: bg }}>
                <Icon className="h-5 w-5 text-[#242033]" />
              </span>
              <p className="text-xs font-bold text-[#8b849b]">{label}</p>
              <p className="mt-1 text-2xl font-black tracking-tight text-[#242033] sm:text-3xl">{value}</p>
            </div>
          ))}
        </div>

        <section className="mb-7 grid gap-5 lg:grid-cols-[1.45fr_.85fr]">
          <div className="rounded-[30px] bg-white p-6 shadow-[0_14px_35px_rgba(39,28,72,.07)] sm:p-7">
            <div className="mb-5 flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-black uppercase tracking-[.12em] text-[#91899f]">{t('dailyMomentum')}</p>
                <h2 className="mt-1 text-2xl font-black tracking-tight text-[#242033]">{nextAction?.title || t('allCaughtUp')}</h2>
              </div>
              <span className="rounded-2xl bg-[#eee8ff] px-3 py-2 text-sm font-black text-[#5b36db]">{goalProgress.current}/{goalProgress.target} XP</span>
            </div>
            <div className="h-3 overflow-hidden rounded-full bg-[#f0edf6]">
              <div className="h-full rounded-full bg-[#6c45f5] transition-all" style={{ width: `${Math.min(100, (goalProgress.current / goalProgress.target) * 100)}%` }} />
            </div>
            <div className="mt-5 grid gap-3 sm:grid-cols-3">
              <div className="rounded-2xl bg-[#f8f6fc] p-4"><p className="text-xs font-bold text-[#91899f]">{t('whatNow')}</p><p className="mt-1 font-black text-[#242033]">{nextAction ? `${tPlan(getLessonTypeLabelKey(nextAction.lessonType))} · ${nextAction.estimatedMinutes}min` : t('allCaughtUp')}</p></div>
              <div className="rounded-2xl bg-[#f8f6fc] p-4"><p className="text-xs font-bold text-[#91899f]">{t('dueForReview')}</p><p className="mt-1 text-2xl font-black text-[#6c45f5]">{reviewDueCount}</p></div>
              <div className="rounded-2xl bg-[#f8f6fc] p-4"><p className="text-xs font-bold text-[#91899f]">{t('completedToday', { completed: completedLessonCount, total: todayLessons.length })}</p><p className="mt-1 text-2xl font-black text-[#242033]">{completedLessonCount}</p></div>
            </div>
          </div>

          <div className="rounded-[30px] bg-[#ffd85a] p-6 shadow-[0_14px_35px_rgba(39,28,72,.07)] sm:p-7">
            <p className="text-xs font-black uppercase tracking-[.12em] text-[#705b12]">{t('planProgress')}</p>
            <p className="mt-2 text-4xl font-black text-[#242033]">{planCompletion}%</p>
            <div className="mt-4 h-3 overflow-hidden rounded-full bg-white/55"><div className="h-full rounded-full bg-[#242033]" style={{ width: `${planCompletion}%` }} /></div>
            <p className="mt-4 text-sm font-bold text-[#5f531f]">{hasPlan ? t('dayProgress', { current: Math.min(progressDay + 1, totalDays), total: totalDays }) : t('startWithAssessment')}</p>
            {hasPlan && <Link href="/plan" className="mt-5 inline-flex rounded-2xl bg-[#242033] px-4 py-3 text-sm font-black text-white">{t('goToMyPlan')}</Link>}
          </div>
        </section>

        <section className="rounded-[30px] bg-white p-6 shadow-[0_14px_35px_rgba(39,28,72,.07)] sm:p-7">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div><p className="text-xs font-black uppercase tracking-[.12em] text-[#91899f]">{t('today')}</p><h2 className="mt-1 text-2xl font-black text-[#242033]">{t('nextStep')}</h2></div>
            {hasPlan && <span className="rounded-full bg-[#c9f5e3] px-3 py-1.5 text-xs font-black text-[#247356]">{completedLessonCount}/{todayLessons.length}</span>}
          </div>
          {todayLessons.length ? (
            <div className="grid gap-3 md:grid-cols-2">
              {todayLessons.map((lesson, i) => {
                const done = (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
                const isNext = nextLesson?.id === lesson.id
                return <div key={i} className={`flex items-center justify-between gap-4 rounded-[22px] p-4 ${isNext ? 'bg-[#eee8ff]' : 'bg-[#f8f6fc]'}`}>
                  <div className="min-w-0"><p className="truncate font-black text-[#242033]">{lesson.title}</p><p className="mt-1 text-xs font-semibold text-[#91899f]">{tPlan(getLessonTypeLabelKey(lesson.lessonType))} · {lesson.estimatedMinutes}min</p></div>
                  {done ? <span className="shrink-0 rounded-full bg-[#c9f5e3] px-3 py-1.5 text-xs font-black text-[#247356]">✓ {t('lessonDone')}</span> : lesson.id ? <Link href={`/lesson/${lesson.id}`} className={`shrink-0 rounded-xl px-3 py-2 text-xs font-black ${isNext ? 'bg-[#6c45f5] text-white' : 'bg-white text-[#5b36db] shadow-sm'}`}>{t('startLesson')}</Link> : null}
                </div>
              })}
            </div>
          ) : <p className="text-sm font-semibold text-[#91899f]">{hasPlan ? t('allCaughtUp') : t('startWithAssessment')}</p>}
        </section>

        <section className="mt-5 rounded-[30px] bg-[#bdeaff] p-6 shadow-[0_14px_35px_rgba(39,28,72,.06)] sm:p-7" aria-label={t('recentPerformance')}>
          <div className="mb-5"><p className="text-xs font-black uppercase tracking-[.12em] text-[#46708a]">{t('recentPerformance')}</p><p className="mt-1 text-sm font-semibold text-[#3f657c]">{t('recentPerformanceDescription')}</p></div>
          {skillEntries.length ? <div className="grid gap-4 sm:grid-cols-2">{skillEntries.map(({skill,value}) => <div key={skill} className="rounded-2xl bg-white/70 p-4"><div className="mb-2 flex justify-between gap-3"><span className="truncate text-xs font-black text-[#242033]">{tPlan(getLessonTypeLabelKey(skill))}</span><span className="text-xs font-bold text-[#5d7280]">{Math.round(value*100)}%</span></div><div className="h-3 overflow-hidden rounded-full bg-white"><div className="h-full rounded-full bg-[#6c45f5]" style={{width:`${value*100}%`}} /></div></div>)}</div> : <p className="text-sm font-semibold text-[#3f657c]">{t('noSkills')}</p>}
        </section>

        {showPremiumBanner && <section className="mt-5 rounded-[30px] bg-[#fff0a8] p-6 shadow-[0_14px_35px_rgba(39,28,72,.06)]">
          <p className="font-black text-[#242033]">{freemiumTrialActive ? t('freemiumTrialTitle', { days: freemiumTrialDaysLeft }) : t(paymentRecovery ? 'premiumBannerPastDueTitle' : 'premiumBannerTitle')}</p>
          <p className="mt-2 text-sm font-semibold text-[#6d5e25]">{freemiumTrialActive ? t('freemiumTrialDesc', { days: freemiumTrialDaysLeft }) : paymentRecovery ? t('premiumBannerPastDueDesc') : t(trialEligible ? 'premiumBannerDesc' : 'premiumBannerDescTrialUsed')}</p>
          {!freemiumTrialActive && (paymentRecovery ? <button onClick={handleManageSubscription} disabled={portalLoading} className="mt-4 rounded-2xl bg-[#242033] px-5 py-3 text-sm font-black text-white">{portalLoading ? '...' : tBilling('updatePayment')}</button> : <SubscriptionPlanButtons className="mt-4" />)}
        </section>}

        <div className="mt-6 flex flex-wrap gap-2">
          {hasPlan && <Link href="/plan" className="rounded-2xl bg-[#6c45f5] px-5 py-3 text-sm font-black text-white shadow-[0_4px_0_#4f2bd1]">{t('goToMyPlan')}</Link>}
          <Link href="/flashcards" className="rounded-2xl bg-white px-5 py-3 text-sm font-bold text-[#5b36db] shadow-sm">{tNav('flashcards')}</Link>
          <Link href="/chat" className="rounded-2xl bg-white px-5 py-3 text-sm font-bold text-[#5b36db] shadow-sm">{tNav('tutor')}</Link>
          <Link href="/assessment" className="rounded-2xl bg-white px-5 py-3 text-sm font-bold text-[#5b36db] shadow-sm">{tNav('assessment')}</Link>
        </div>
      </div>
    </>
  )
