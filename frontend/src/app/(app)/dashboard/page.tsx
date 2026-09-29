'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import {
  ArrowUpRight,
  BookOpen,
  CalendarDays,
  Check,
  ChevronDown,
  Flame,
  Headphones,
  LayoutDashboard,
  Library,
  ListChecks,
  Mic2,
  MoreHorizontal,
  Play,
  RefreshCw,
  Trophy,
  UserRound,
} from 'lucide-react'
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
import { subscribeToLearningProgressUpdated } from '@/lib/learning-progress'

interface TodayLessonItem {
  id: number | null
  title: string
  lesson_type: string
  week: number
  day: number
  objectives: string[]
  estimated_minutes: number
  is_completed: boolean
}

interface CompletionState {
  state: 'in_progress' | 'ready' | 'taken'
  score: number | null
  recommendation: string | null
  next_level: string | null
}

const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

export default function DashboardPage() {
  const t = useTranslations('dashboard')
  const tBilling = useTranslations('billing')
  const tNav = useTranslations('nav')
  const tPlan = useTranslations('plan')
  const tTarget = useTranslations('targetLanguages')
  const tError = useTranslations('error')

  const user = useAuthStore((s) => s.user)
  const accessToken = useAuthStore((s) => s.accessToken)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const trialEligible = !user?.trial_used
  const freemiumTrialActive = isFreemiumTrialActive(user, stripeEnabled)
  const [freemiumTrialDaysLeft, setFreemiumTrialDaysLeft] = useState(0)

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
  const [completion, setCompletion] = useState<CompletionState | null>(null)
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
  const [historyRange, setHistoryRange] = useState<'week' | 'month' | 'all'>('week')
  const [historyEntries, setHistoryEntries] = useState<Array<{
    date: string
    xp_earned: number
    lessons_completed: number
    exercises_correct: number
    exercises_total: number
    streak_day: number
    skills: Record<string, number>
  }>>([])
  const [historyLoading, setHistoryLoading] = useState(false)
  const [refreshing, setRefreshing] = useState(false)
  const [activeInsight, setActiveInsight] = useState<'next' | 'performance' | 'vocabulary' | null>(null)

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

  const loadData = useCallback(async () => {
    try {
      const [progRes, planRes, historyRes] = await Promise.all([
        apiFetch('/api/progress/summary'),
        apiFetch('/api/study-plan/today'),
        apiFetch('/api/progress/history?range=' + historyRange),
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

      if (historyRes.ok) {
        const history = await historyRes.json()
        setHistoryEntries(Array.isArray(history.entries) ? history.entries : [])
      } else {
        setHistoryEntries([])
      }

      if (planRes.ok) {
        const plan = await planRes.json()
        setCefrLevel(plan.cefr_level ?? null)
        setCompletion(plan.completion ?? null)
        setProgressDay(plan.progress_day ?? 0)
        setTotalDays(plan.total_days ?? 0)
        setPendingCount(plan.pending_count ?? 0)
        setTodayLessons(
          plan.lessons.map((l: TodayLessonItem) => ({
            id: l.id,
            title: l.title,
            lessonType: l.lesson_type,
            week: l.week,
            day: l.day,
            objectives: l.objectives || [],
            estimatedMinutes: l.estimated_minutes || 25,
            isCompleted: l.is_completed,
          }))
        )
        setHasPlan(true)
      } else {
        setCefrLevel(null)
        setCompletion(null)
        setProgressDay(0)
        setTotalDays(0)
        setPendingCount(0)
        setTodayLessons([])
        setHasPlan(false)
      }
    } catch {
      setLoadError(true)
    } finally {
      setLoading(false)
    }
  }, [setProgress, setTodayLessons, activeLanguage?.code, historyRange])

  useEffect(() => {
    if (!user || !accessToken) return
    loadData()
  }, [loadData, user, accessToken])

  const refreshDashboardData = useCallback(async () => {
    if (refreshing) return
    setRefreshing(true)
    setLoadError(false)
    try {
      await loadData()
    } finally {
      setRefreshing(false)
    }
  }, [loadData, refreshing])

  // Keep the dashboard synchronized after a lesson/assessment is completed
  // in another route, without requiring a full browser reload.
  useEffect(() => {
    if (!user || !accessToken) return

    const handleVisibility = () => {
      if (document.visibilityState === 'visible') {
        refreshDashboardData()
      }
    }
    const handleFocus = () => refreshDashboardData()

    window.addEventListener('focus', handleFocus)
    document.addEventListener('visibilitychange', handleVisibility)
    return () => {
      window.removeEventListener('focus', handleFocus)
      document.removeEventListener('visibilitychange', handleVisibility)
    }
  }, [user, accessToken, refreshDashboardData])

  useEffect(() => {
    if (!user || !accessToken) return
    return subscribeToLearningProgressUpdated(() => {
      void refreshDashboardData()
    })
  }, [user, accessToken, refreshDashboardData])

  async function changeHistoryRange(range: 'week' | 'month' | 'all') {
    if (range === historyRange) return
    setHistoryLoading(true)
    setHistoryRange(range)
    try {
      const res = await apiFetch('/api/progress/history?range=' + range)
      if (!res.ok) throw new Error('history')
      const history = await res.json()
      setHistoryEntries(Array.isArray(history.entries) ? history.entries : [])
    } catch {
      setHistoryEntries([])
    } finally {
      setHistoryLoading(false)
    }
  }

  async function skipDay() {
    if (skipping) return
    setSkipping(true)
    setSkipError(false)
    try {
      const res = await apiFetch('/api/study-plan/skip-day', { method: 'POST' })
      if (!res.ok) throw new Error('skip-day')
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
      setPortalError(err instanceof Error ? err.message : tBilling('portalError'))
      setPortalLoading(false)
    }
  }

  if (loading) {
    return <PageLoading label={t('loadingProgress')} minHeight="min-h-screen" />
  }

  const skillEntries = Object.entries(skills)
    .map(([skill, value]) => ({ skill, value: value as number }))
    .sort((a, b) => a.value - b.value)

  const completedLessonCount = todayLessons.filter(
    (lesson) => (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
  ).length

  const nextLesson = todayLessons.find(
    (lesson) => lesson.id && !completedToday.includes(lesson.id) && !lesson.isCompleted
  )

  const planPositionComplete = completion?.state === 'ready' || completion?.state === 'taken'
  const planCompletion = hasPlan && totalDays > 0
    ? planPositionComplete ? 100 : Math.min(100, Math.round((progressDay / totalDays) * 100))
    : 0
  const currentDayDisplay = planPositionComplete ? totalDays : Math.min(progressDay + 1, totalDays)
  const vocabularyProgressPct = Math.round(vocabularyProgress * 100)
  const paymentRecovery = needsPaymentRecovery(user)
  const showPremiumBanner = stripeEnabled && !isSubscribed(user, stripeEnabled)

  const chartEntries = historyEntries.slice(-7)
  const performanceValues = chartEntries.map((entry) =>
    entry.exercises_total > 0 ? Math.round((entry.exercises_correct / entry.exercises_total) * 100) : 0
  )
  const chartMax = Math.max(100, ...performanceValues)
  const chartAverage = chartEntries.length
    ? Math.round(chartEntries.reduce((sum, entry) => sum + (entry.exercises_total > 0 ? (entry.exercises_correct / entry.exercises_total) * 100 : 0), 0) / chartEntries.length)
    : 0
  const progressBars = chartEntries.map((entry) => ({
    day: new Date(entry.date + 'T00:00:00').toLocaleDateString(undefined, { weekday: 'short' }),
    value: entry.xp_earned,
    active: entry.date === new Date().toISOString().slice(0, 10),
  }))

  function getPerformanceLabel(value: number) {
    if (value < 0.5) return t('performanceNeedsPractice')
    if (value < 0.8) return t('performanceInProgress')
    return t('performanceStrong')
  }

  return (
    <>
      <OnboardingTour />
      <WhatsNew />
      <div className="juba-duo-home juba-busuu-dashboard">
        <section className="juba-duo-welcome">
          <div>
            <span className="juba-duo-eyebrow">{activeLanguage ? tTarget(activeLanguage.code) : t('today')}</span>
            <h1>{t('welcomeBack')}, {user?.displayName || user?.username}</h1>
            <p>{cefrLevel ? cefrLevel + ' · ' : ''}{nextLesson?.title || t('startWithAssessment')}</p>
          </div>
          <div className="juba-duo-top-stats">
            <div><Flame size={20} /><strong>{streak}</strong><span>{t('streak')}</span></div>
            <div><Trophy size={20} /><strong>{xp}</strong><span>{t('xp')}</span></div>
          </div>
        </section>

        {loadError && (
          <div className="juba-duo-alert" role="alert">
            <span>{tError('body')}</span>
            <button type="button" onClick={() => { setLoadError(false); setLoading(true); loadData() }}>{tError('retry')}</button>
          </div>
        )}

        <div className="juba-duo-grid">
          <main className="juba-duo-course">
            <section className="juba-duo-unit">
              <div className="juba-duo-unit-head">
                <div>
                  <span className="juba-duo-unit-kicker">{t('nextStep')}</span>
                  <h2>{cefrLevel || 'A1'} · {nextLesson?.title || t('startWithAssessment')}</h2>
                </div>
                <Link href="/plan" className="juba-duo-guide">{t('goToMyPlan')}</Link>
              </div>
              <div className="juba-duo-progress">
                <span style={{ width: planCompletion + '%' }} />
              </div>
              <div className="juba-duo-progress-meta">
                <span>{currentDayDisplay}/{totalDays || 0}</span>
                <span>{planCompletion}%</span>
              </div>
            </section>

            <section className="juba-duo-path" aria-label={t('lessonReady')}>
              {todayLessons.length ? todayLessons.map((lesson, index) => {
                const done = (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
                const current = !done && (!nextLesson || lesson.id === nextLesson.id)
                return (
                  <div key={lesson.id ?? lesson.title} className={`juba-duo-node-row ${index % 2 ? 'is-offset' : ''}`}>
                    <div className={`juba-duo-node ${done ? 'is-done' : current ? 'is-current' : ''}`}>
                      {done ? <Check size={28} strokeWidth={3} /> : current ? <Play size={27} fill="currentColor" /> : <BookOpen size={25} />}
                    </div>
                    <div className="juba-duo-node-copy">
                      <strong>{lesson.title}</strong>
                      <span>{tPlan('lessonTypes.' + lesson.lessonType)} · {lesson.estimatedMinutes} {t('minutes')}</span>
                      {current && lesson.id ? <Link href={'/lesson/' + lesson.id} className="juba-duo-cta">{t('startLesson')}</Link> : done ? <span className="juba-duo-complete"><Check size={15} />{t('completedToday', { completed: 1, total: 1 })}</span> : null}
                    </div>
                  </div>
                )
              }) : (
                <div className="juba-duo-empty">
                  <BookOpen size={34} />
                  <h3>{t('startWithAssessment')}</h3>
                  <Link href="/assessment" className="juba-duo-cta">{tNav('assessment')}</Link>
                </div>
              )}
            </section>
          </main>

          <aside className="juba-duo-side">
            <section className="juba-duo-card juba-duo-streak-card">
              <div className="juba-duo-card-icon"><Flame size={24} /></div>
              <div><span>{t('streak')}</span><strong>{streak}</strong><small>{t('today')}</small></div>
            </section>

            <section className="juba-duo-card">
              <div className="juba-duo-card-head"><h3>{t('accuracy')}</h3><span>{accuracy}%</span></div>
              <div className="juba-duo-meter"><span style={{ width: accuracy + '%' }} /></div>
              <p>{getPerformanceLabel(accuracy / 100)}</p>
            </section>

            <section className="juba-duo-card">
              <div className="juba-duo-card-head"><h3>{t('vocabularyProgress', { level: vocabularyLevel || '—' })}</h3><span>{vocabularyProgressPct}%</span></div>
              <div className="juba-duo-meter"><span style={{ width: vocabularyProgressPct + '%' }} /></div>
              <p>{t('vocabularyWords', { mastered: vocabularyMastered, total: vocabularyTotal })}</p>
              <Link href="/vocabulary" className="juba-duo-card-link">{tNav('vocabulary')} <ArrowUpRight size={16} /></Link>
            </section>

            <section className="juba-duo-card">
              <div className="juba-duo-card-head"><h3>{t('recentPerformance')}</h3><span>{chartAverage}%</span></div>
              <div className="juba-duo-mini-bars">
                {performanceValues.length ? performanceValues.map((value, index) => <span key={index} style={{ height: Math.max(10, value) + '%' }} />) : <i>{t('noSkills')}</i>}
              </div>
            </section>

            <section className="juba-duo-links">
              <Link href="/reading"><BookOpen size={18} />{tNav('reading')}</Link>
              <Link href="/listening"><Headphones size={18} />{tNav('listening')}</Link>
              <Link href="/flashcards"><Library size={18} />{tNav('flashcards')}</Link>
              <Link href="/chat"><Mic2 size={18} />{tNav('tutor')}</Link>
            </section>
          </aside>
        </div>

        {showPremiumBanner && (
          <section className="juba-duo-premium">
            <Trophy size={24} />
            <div><strong>{freemiumTrialActive ? t('freemiumTrialTitle', { days: freemiumTrialDaysLeft }) : t(paymentRecovery ? 'premiumBannerPastDueTitle' : 'premiumBannerTitle')}</strong><span>{freemiumTrialActive ? t('freemiumTrialDesc', { days: freemiumTrialDaysLeft }) : paymentRecovery ? t('premiumBannerPastDueDesc') : t(trialEligible ? 'premiumBannerDesc' : 'premiumBannerDescTrialUsed')}</span></div>
            {paymentRecovery ? <button onClick={handleManageSubscription} disabled={portalLoading}>{portalLoading ? '…' : tBilling('updatePayment')}</button> : !freemiumTrialActive ? <SubscriptionPlanButtons /> : null}
          </section>
        )}
      </div>
    </>
  )
}
