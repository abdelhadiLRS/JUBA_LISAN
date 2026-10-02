'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import {
  ArrowUpRight,
  BookOpen,
  Check,
  Flame,
  Headphones,
  LayoutDashboard,
  Library,
  Mic2,
  MoreHorizontal,
  Play,
  RefreshCw,
  Trophy,
  UserRound,
  ChartNoAxesColumnIncreasing,
  Sparkles,
  Users,
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
import { AuthAvatarImage } from '@/components/AuthAvatarImage'

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

interface FriendItem {
  id: number
  username: string
  display_name: string
  avatar?: string | null
  target_language?: string
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
  const [friends, setFriends] = useState<FriendItem[]>([])

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
      const [progRes, planRes, historyRes, friendsRes] = await Promise.all([
        apiFetch('/api/progress/summary'),
        apiFetch('/api/study-plan/today'),
        apiFetch('/api/progress/history?range=' + historyRange),
        apiFetch('/api/social/friends'),
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

      if (friendsRes.ok) {
        const socialFriends = await friendsRes.json()
        setFriends(Array.isArray(socialFriends) ? socialFriends.slice(0, 6) : [])
      } else {
        setFriends([])
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
  const coursePathProgress = todayLessons.length > 1
    ? Math.min(1, completedLessonCount / (todayLessons.length - 1))
    : completedLessonCount > 0 ? 1 : 0
  const coursePathCurrentIndex = todayLessons.findIndex((lesson) => {
    const done = (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
    return !done && (!nextLesson || lesson.id === nextLesson.id)
  })
  const coursePathCurrentLabel = coursePathCurrentIndex >= 0 ? `${coursePathCurrentIndex + 1}` : todayLessons.length ? `${todayLessons.length}` : '0'
  const vocabularyProgressPct = Math.round(vocabularyProgress * 100)
  const paymentRecovery = needsPaymentRecovery(user)
  const showPremiumBanner = stripeEnabled && !isSubscribed(user, stripeEnabled)

  const chartEntries = historyEntries.slice(-7)
  const chartAverage = chartEntries.length
    ? Math.round(chartEntries.reduce((sum, entry) => sum + (entry.exercises_total > 0 ? (entry.exercises_correct / entry.exercises_total) * 100 : 0), 0) / chartEntries.length)
    : 0
  const progressBars = chartEntries.map((entry) => ({
    day: new Date(entry.date + 'T00:00:00').toLocaleDateString(undefined, { weekday: 'short' }),
    value: entry.xp_earned,
    active: entry.date === new Date().toISOString().slice(0, 10),
  }))

  return (
    <>
      <OnboardingTour />
      <WhatsNew />
      <div className="dashboard-dashboard dashboard-v3" data-dashboard-version="clean-v1">
        <header className="dashboard-topbar">
          <div className="dashboard-topbar-title">
            <span className="dashboard-dot" aria-hidden="true">JL</span>
            <nav className="dashboard-reference-nav" aria-label={tNav('navigation')}>
              <Link href="/dashboard" className="is-active">{tNav('home')}</Link>
              <Link href="/plan">{tNav('myPlan')}</Link>
              <Link href="/courses">{tNav('courses')}</Link>
            </nav>
          </div>
          <div className="dashboard-topbar-actions">
            <span className="dashboard-course-selector">
              <span>{tNav('switchLanguage')}</span>
              <strong>{activeLanguage ? tTarget(activeLanguage.code) : t('today')}</strong>
            </span>
            <button type="button" className="dashboard-icon-button" onClick={refreshDashboardData} disabled={refreshing} aria-label={tError('retry')} title={tError('retry')}>
              <RefreshCw size={15} className={refreshing ? 'animate-spin' : ''} />
            </button>
          </div>
        </header>


        {loadError && (
          <div className="dashboard-alert" role="alert">
            <span>{tError('body')}</span>
            <button type="button" onClick={() => { setLoadError(false); setLoading(true); loadData() }}>{tError('retry')}</button>
          </div>
        )}

        <section className="dashboard-v3-grid">
          <main className="dashboard-v3-main">
            <section className="dashboard-v3-welcome">
              <div className="dashboard-welcome-copy">
                <span className="dashboard-section-label">JUBA LISAN</span>
                <h2>Welcome back, {user?.displayName || user?.username || ''}!</h2>
                <p>{completedLessonCount}/{Math.max(1, todayLessons.length)} {t('today')}</p>
                <div className="dashboard-welcome-meta">
                  <span>{Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100))}% {t('todayGoal')}</span>
                  <i aria-hidden="true" />
                  <span>{cefrLevel || 'A1'}</span>
                  <i aria-hidden="true" />
                  <span>{currentDayDisplay}/{totalDays || 0}</span>
                </div>
              </div>
              <div className="dashboard-v3-level" style={{'--level-progress': planCompletion} as React.CSSProperties} aria-label={(cefrLevel || 'A1') + ' ' + planCompletion + '%'}>
                <span>{cefrLevel || 'A1'}</span>
                <small>{planCompletion}%</small>
              </div>
            </section>

            <section className="dashboard-v3-card dashboard-daily">
              <div className="dashboard-v3-card-head">
                <div>
                  <span className="dashboard-section-label">{t('xp')}</span>
                  <h2>{t('recentPerformance')}</h2>
                </div>
                <strong>{xp} XP</strong>
              </div>
              <div className="dashboard-v3-chart">
                {(progressBars.length ? progressBars : weekDays.map(day => ({day, value:0, active:false}))).map((bar,index,bars) => {
                  const max = Math.max(1, ...bars.map(item => item.value))
                  return (
                    <div key={index} className={`dashboard-v3-chart-col ${bar.active ? 'active' : ''}`}>
                      <span style={{height: Math.max(8, Math.round((bar.value / max) * 100)) + '%'}} />
                      <small>{bar.day}</small>
                    </div>
                  )
                })}
              </div>
              <div className="dashboard-v3-chart-footer">
                <span>{t('streak')}: <b>{streak}</b></span>
                <span>{t('accuracy')}: <b>{accuracy}%</b></span>
              </div>
              <div className="dashboard-chart-summary">
                <span><small>{t('xp')}</small><b>{chartEntries.reduce((sum, entry) => sum + entry.xp_earned, 0)}</b></span>
                <span><small>{t('accuracy')}</small><b>{chartAverage}%</b></span>
                <span><small>{t('completedToday', { completed: completedLessonCount, total: Math.max(todayLessons.length, completedLessonCount) })}</small><b>{completedLessonCount}</b></span>
              </div>
            </section>

            <section className="dashboard-reference-insights">
              <div className="dashboard-v3-card dashboard-insight-card">
                <div className="dashboard-v3-card-head">
                  <div><span className="dashboard-section-label">{t('today')}</span><h3>{t('todayGoal')}</h3></div>
                  <Flame size={18} />
                </div>
                <div className="dashboard-insight-value"><strong>{completedLessonCount}</strong><span>/{Math.max(1, todayLessons.length)} {t('today')}</span></div>
                <div className="dashboard-insight-track"><span style={{width: Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100)) + '%'}} /></div>
                <div className="dashboard-insight-footer"><span>{t('xp')}</span><b>{xp}</b><span>{t('streak')}</span><b>{streak}</b></div>
              </div>
              <div className="dashboard-v3-card dashboard-insight-card">
                <div className="dashboard-v3-card-head">
                  <div><span className="dashboard-section-label">{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</span><h3>{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</h3></div>
                  <Library size={18} />
                </div>
                <div className="dashboard-words-value"><strong>{vocabularyMastered.toLocaleString()}</strong><span>/ {vocabularyTotal.toLocaleString()}</span></div>
                <div className="dashboard-word-bars" aria-hidden="true">
                  {[20, 34, 48, 62, 76, 90].map((height, index) => (
                    <span key={height} style={{height: Math.max(12, Math.round(height * Math.max(0.18, vocabularyProgress))) + '%'}} className={index === 5 ? 'active' : ''} />
                  ))}
                </div>
                <div className="dashboard-insight-footer"><span>{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</span><b>{vocabularyProgressPct}%</b><span>{vocabularyLevel || 'A1'}</span></div>
              </div>
            </section>

            <section className="dashboard-reference-stats">
              <div className="dashboard-v3-card dashboard-stat-card">
                <div className="dashboard-v3-card-head">
                  <div><span className="dashboard-section-label">{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</span><h3>{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</h3></div>
                  <Library size={18} />
                </div>
                <div className="dashboard-stat-value">{vocabularyMastered.toLocaleString()}</div>
                <div className="dashboard-stat-caption">{vocabularyTotal.toLocaleString()} · {vocabularyProgressPct}%</div>
                <div className="dashboard-stat-track"><span style={{width: vocabularyProgressPct + '%'}} /></div>
              </div>
              <div className="dashboard-v3-card dashboard-stat-card">
                <div className="dashboard-v3-card-head">
                  <div><span className="dashboard-section-label">{t('xp')}</span><h3>{t('recentPerformance')}</h3></div>
                  <ChartNoAxesColumnIncreasing size={18} />
                </div>
                <div className="dashboard-stat-breakdown">
                  <span><i />{t('today')}<b>{historyEntries[historyEntries.length - 1]?.xp_earned ?? 0} XP</b></span>
                  <span><i />{t('streak')}<b>{streak}</b></span>
                  <span><i />{t('accuracy')}<b>{accuracy}%</b></span>
                </div>
              </div>
            </section>

            <section className="dashboard-v3-card dashboard-achievement-strip">
              <div className="dashboard-achievement-strip-icon"><Trophy size={20}/></div>
              <div className="dashboard-achievement-strip-copy">
                <span className="dashboard-section-label">{t('nextStep')}</span>
                <strong>{nextLesson?.title || t('startWithAssessment')}</strong>
                <small>{cefrLevel || 'A1'} · {planCompletion}%</small>
              </div>
              <div className="dashboard-achievement-strip-progress"><span style={{width: planCompletion + '%'}} /></div>
            </section>
            <section className="dashboard-v3-card dashboard-course">
              <div className="dashboard-card-header">
                <div>
                  <span className="dashboard-section-label">{t('nextStep')}</span>
                  <h2>{cefrLevel || 'A1'} · {nextLesson?.title || t('startWithAssessment')}</h2>
                  <p>{nextLesson?.objectives?.[0] || t('goToMyPlan')}</p>
                </div>
                <Link href="/plan" className="dashboard-outline-button">{t('goToMyPlan')} <ArrowUpRight size={15} /></Link>
              </div>
              <div className="dashboard-progress-row"><div className="dashboard-progress-track"><span style={{width: planCompletion + '%'}} /></div><strong>{planCompletion}%</strong></div>
              <div className="dashboard-progress-meta">
                <span className="dashboard-progress-meta-cell"><small>{t('today')}</small><b>{currentDayDisplay}/{totalDays || 0}</b></span>
                <span className="dashboard-progress-meta-cell is-green"><small>{t('completedToday',{completed:completedLessonCount,total:todayLessons.length})}</small><b>{completedLessonCount}/{todayLessons.length}</b></span>
                <span className="dashboard-progress-meta-cell"><small>{t('nextStep')}</small><b>{coursePathCurrentLabel}/{todayLessons.length || 0}</b></span>
              </div>
              <div className="dashboard-lessons dashboard-course-path" style={{ "--course-path-progress": String(coursePathProgress) } as React.CSSProperties}>
                {todayLessons.length ? todayLessons.map((lesson,index) => {
                  const done = (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
                  const current = !done && (!nextLesson || lesson.id === nextLesson.id)
                  return (
                    <div key={lesson.id ?? lesson.title} aria-current={current ? 'step' : undefined} data-checkpoint-state={done ? 'completed' : current ? 'current' : 'upcoming'} className={`dashboard-lesson ${current ? 'current' : ''} ${done ? 'done' : ''}`} >
                      <div className="dashboard-path-rail" aria-hidden="true">
                        <span className={`dashboard-path-node ${done ? 'done' : current ? 'current' : ''}`} >
                          {done ? <Check size={14} strokeWidth={3} /> : current ? <Play size={13} fill="currentColor" /> : <span>{index + 1}</span>}
                        </span>
                      </div>
                      <div className="dashboard-lesson-copy">
                        <div className="dashboard-lesson-title">
                          <span className="dashboard-lesson-code">CP {String(index + 1).padStart(2,'0')}</span>
                          <strong>{lesson.title}</strong>
                        </div>
                        <span>{tPlan('lessonTypes.' + lesson.lessonType)} · {lesson.estimatedMinutes} {t('minutes')}</span>
                      </div>
                      <div className="dashboard-lesson-action">
                        {current && lesson.id ? <div className="dashboard-lesson-current-action"><span>{t('today')}</span><Link href={'/lesson/' + lesson.id} className="dashboard-green-button">{t('startLesson')}</Link></div> : done ? <span className="dashboard-completed"><Check size={14} />{t('completedToday',{completed:1,total:1})}</span> : <span className="dashboard-locked"><MoreHorizontal size={17} /></span>}
                      </div>
                    </div>
                  )
                }) : (
                  <div className="dashboard-empty"><BookOpen size={30}/><div><strong>{t('startWithAssessment')}</strong><span>{t('goToMyPlan')}</span></div><Link href="/assessment" className="dashboard-green-button">{tNav('assessment')}</Link></div>
                )}
              </div>
            </section>
          </main>

          <aside className="dashboard-v3-rail">
            <section className="dashboard-v3-card dashboard-profile-card">
              <div className="dashboard-profile-hero">
                <div className="dashboard-profile-photo">
                  {user?.avatar ? (
                    <AuthAvatarImage avatar={user.avatar} alt="" width={52} height={52} className="h-full w-full object-cover" />
                  ) : (
                    <UserRound size={28} />
                  )}
                </div>
                <strong>{user?.displayName || user?.username}</strong>
                <span>{cefrLevel || 'A1'} · {tTarget(activeLanguage?.code || 'en-US')}</span>
              </div>
              <div className="dashboard-profile-metrics">
                <span><b>{xp}</b><small>XP</small></span>
                <span><b>{streak}</b><small>{t('streak')}</small></span>
                <span><b>{accuracy}%</b><small>{t('accuracy')}</small></span>
              </div>
            </section>

            <section className="dashboard-v3-card dashboard-goal-card">
              <div className="dashboard-v3-card-head">
                <div><span className="dashboard-section-label">{t('today')}</span><h3>{t('todayGoal')}</h3></div>
                <Flame size={19} />
              </div>
              <div className="dashboard-goal-ring" style={{background: 'conic-gradient(#58cc02 0 ' + Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100)) + '%, #edf2e9 ' + Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100)) + '% 100%)'}}>
                <strong>{completedLessonCount}</strong><span>/{Math.max(1, todayLessons.length)}</span>
              </div>
              <div className="dashboard-goal-copy">
                <b>{Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100))}%</b>
                <span>{t('completedToday', { completed: completedLessonCount, total: Math.max(1, todayLessons.length) })}</span>
              </div>
              <div className="dashboard-small-progress"><span style={{width: Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100)) + '%'}} /></div>
            </section>
            <section className="dashboard-v3-card dashboard-xp-card">
              <div className="dashboard-v3-card-head"><div><span className="dashboard-section-label">{t('xp')}</span><h3>{t('recentPerformance')}</h3></div><ChartNoAxesColumnIncreasing size={18}/></div>
              <div className="dashboard-xp-list">
                <div><span>{t('today')}</span><b>{historyEntries[historyEntries.length - 1]?.xp_earned ?? 0} XP</b></div>
                <div><span>{t('streak')}</span><b>{streak}</b></div>
                <div><span>{t('accuracy')}</span><b>{accuracy}%</b></div>
              </div>
            </section>
            <section className="dashboard-v3-card dashboard-achievement-card">
              <div className="dashboard-v3-card-head"><div><span className="dashboard-section-label">{t('nextStep')}</span><h3>{t('startWithAssessment')}</h3></div><Trophy size={19} /></div>
              <div className="dashboard-achievement-icon"><Trophy size={29}/></div>
              <strong>{nextLesson?.title || t('startWithAssessment')}</strong>
              <span>{cefrLevel || 'A1'} · {planCompletion}%</span>
              <div className="dashboard-small-progress"><span style={{width:planCompletion + '%'}} /></div>
            </section>

            <section className="dashboard-v3-card dashboard-tools-card">
              <div className="dashboard-v3-card-head"><div><span className="dashboard-section-label">{tNav('courses')}</span><h3>{tNav('courses')}</h3></div><LayoutDashboard size={18}/></div>
              <Link href="/reading"><BookOpen size={17}/><span>{tNav('reading')}</span><ArrowUpRight size={14}/></Link>
              <Link href="/listening"><Headphones size={17}/><span>{tNav('listening')}</span><ArrowUpRight size={14}/></Link>
              <Link href="/flashcards"><Library size={17}/><span>{tNav('flashcards')}</span><ArrowUpRight size={14}/></Link>
              <Link href="/chat"><Mic2 size={17}/><span>{tNav('tutor')}</span><ArrowUpRight size={14}/></Link>
            </section>

            <section className="dashboard-v3-card dashboard-friends-card">
              <div className="dashboard-v3-card-head">
                <div><span className="dashboard-section-label"><Users size={13} /> {tNav('friends')}</span><h3>{tNav('friends')}</h3></div>
                <Link href="/friends" className="dashboard-mini-link">VIEW ALL</Link>
              </div>
              <div className="dashboard-friends-list">
                {friends.length ? friends.map((friend) => (
                  <Link key={friend.id} href={'/friends/chat/' + friend.id} className="dashboard-friend-row">
                    <span className="dashboard-friend-avatar">
                      {friend.avatar ? (
                        <AuthAvatarImage avatar={friend.avatar} alt="" width={34} height={34} className="h-full w-full object-cover" />
                      ) : (
                        (friend.display_name || friend.username || '?')[0].toUpperCase()
                      )}
                    </span>
                    <span className="dashboard-friend-copy">
                      <strong>{friend.display_name || friend.username}</strong>
                      <small>@{friend.username}</small>
                    </span>
                    <span className="dashboard-friend-arrow">›</span>
                  </Link>
                )) : (
                  <Link href="/friends" className="dashboard-friends-empty">{t('goToMyPlan')}</Link>
                )}
              </div>
            </section>

            {showPremiumBanner && (
              <section className="dashboard-premium">
                <div className="dashboard-premium-icon"><Sparkles size={20}/></div>
                <div><strong>{freemiumTrialActive ? t('freemiumTrialTitle',{days:freemiumTrialDaysLeft}) : t(paymentRecovery ? 'premiumBannerPastDueTitle' : 'premiumBannerTitle')}</strong><span>{freemiumTrialActive ? t('freemiumTrialDesc',{days:freemiumTrialDaysLeft}) : paymentRecovery ? t('premiumBannerPastDueDesc') : t(trialEligible ? 'premiumBannerDesc' : 'premiumBannerDescTrialUsed')}</span></div>
                {paymentRecovery ? <button onClick={handleManageSubscription} disabled={portalLoading}>{portalLoading ? '…' : tBilling('updatePayment')}</button> : !freemiumTrialActive ? <SubscriptionPlanButtons/> : null}
              </section>
            )}
          </aside>
        </section>
      </div>
      <style>{`.dashboard-dashboard,.dashboard-v3 {
    --dash-bg:#f7f9f6;
    --dash-surface:#fff;
    --dash-border:#e7ece4;
    --dash-border-strong:#dce4d8;
    --dash-text:#30362f;
    --dash-muted:#8b9289;
    --dash-green:#58cc02;
    --dash-green-dark:#46a302;
    --dash-green-soft:#eff9e9;
    --dash-yellow:#ffb900;
    min-height:100%;
    padding:0 24px 32px;
    background:var(--dash-bg);
    color:var(--dash-text);
    font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  }

  .dashboard-topbar {
    height:68px;
    max-width:1480px;
    margin:0 auto;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:24px;
    border-bottom:1px solid rgba(231,236,228,.72);
  }
  .dashboard-topbar-title,.dashboard-topbar-actions{display:flex;align-items:center}
  .dashboard-dot{
    width:34px;height:34px;flex:none;
    display:grid;place-items:center;
    border-radius:10px;
    background:var(--dash-green);
    color:#fff;
    font-size:11px;font-weight:950;
    letter-spacing:-.03em;
    box-shadow:0 2px 0 var(--dash-green-dark);
    user-select:none;
  }
  .dashboard-topbar-title{gap:18px}
  .dashboard-topbar-title nav{min-width:0}
  .dashboard-topbar-actions{gap:9px}
  .dashboard-reference-nav{display:flex;align-items:center;gap:4px;min-width:0}
  .dashboard-reference-nav a{
    position:relative;display:inline-flex;align-items:center;justify-content:center;
    min-height:34px;padding:0 11px;border-radius:8px;
    color:#8b9289;text-decoration:none;font-size:10px;font-weight:800;
    white-space:nowrap;transition:color .14s ease,background .14s ease;
  }
  .dashboard-reference-nav a:hover{color:#596058;background:#f5f8f3}
  .dashboard-reference-nav a.is-active{color:#4d534d}
  .dashboard-reference-nav a.is-active::after{
    content:"";position:absolute;left:11px;right:11px;bottom:1px;
    height:2px;border-radius:99px;background:var(--dash-green);
  }
  .dashboard-course-selector{
    min-height:36px;max-width:210px;min-width:0;
    display:flex;align-items:center;gap:8px;
    padding:0 11px;
    border:1px solid var(--dash-border);
    border-radius:9px;
    background:#fff;
    color:var(--dash-muted);
    font-size:10px;
  }
  .dashboard-course-selector span,.dashboard-course-selector strong{
    min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  }
  .dashboard-course-selector strong{color:#555;font-size:11px}
  .dashboard-icon-button{
    width:34px;height:34px;display:grid;place-items:center;
    border:1px solid var(--dash-border);border-radius:9px;background:#fff;
    color:#929991;cursor:pointer;
    transition:border-color .14s ease,color .14s ease,background .14s ease;
  }
  .dashboard-icon-button:hover{border-color:#d8e3d3;background:#f8fbf6;color:#58a91b}
  .dashboard-icon-button:disabled{opacity:.55;cursor:default}
  .dashboard-reference-nav a:focus-visible,
  .dashboard-icon-button:focus-visible,
  .dashboard-outline-button:focus-visible,
  .dashboard-green-button:focus-visible,
  .dashboard-tools-card>a:focus-visible,
  .dashboard-friend-row:focus-visible,
  .dashboard-mini-link:focus-visible,
  .dashboard-premium button:focus-visible{
    outline:2px solid #8bd85c;
    outline-offset:2px;
  }

  .dashboard-alert{
    max-width:1480px;margin:0 auto 14px;
    display:flex;align-items:center;justify-content:space-between;gap:12px;
    padding:10px 13px;border:1px solid #f0d7d7;border-radius:9px;
    background:#fff7f7;color:#8b5656;font-size:11px;
  }
  .dashboard-alert button{
    border:0;background:none;color:#4fa31c;font-weight:800;cursor:pointer;
  }

  .dashboard-v3-welcome,
  .dashboard-v3-card{overflow:hidden}
  .dashboard-v3-welcome{position:relative}
  .dashboard-v3-welcome::before{
    content:"";position:absolute;inset:0 auto 0 0;width:3px;
    background:var(--dash-green);border-radius:12px 0 0 12px;pointer-events:none;
  }
  .dashboard-welcome-meta span{transition:border-color .14s ease,background .14s ease}
  .dashboard-welcome-meta span:hover{border-color:#e0e8dc;background:#fbfdf9}
  .dashboard-progress-meta-cell{transition:border-color .14s ease,background .14s ease}
  .dashboard-progress-meta-cell:hover{border-color:#e0e8dc;background:#fbfdf9}
  .dashboard-course-path .dashboard-lesson:last-child{border-bottom:0}
  .dashboard-v3-grid{
    max-width:1480px;margin:0 auto;
    display:grid;
    grid-template-columns:minmax(0,1fr) 300px;
    gap:24px;align-items:start;
  }
  .dashboard-v3-main{min-width:0}
  .dashboard-v3-main>section{margin-bottom:16px}
  .dashboard-v3-card{
    background:var(--dash-surface);
    border:1px solid var(--dash-border);
    border-radius:12px;
    box-shadow:0 1px 4px rgba(35,55,25,.025);
  }

  .dashboard-v3-card-head svg{color:#a1a89e;flex:none}
  .dashboard-v3-card-head>div{min-width:0}

  .dashboard-v3-welcome{
    min-height:132px;
    display:flex;align-items:center;justify-content:space-between;gap:20px;
    padding:20px 20px;
    border:1px solid var(--dash-border);
    border-radius:12px;
    background:#fff;
    box-shadow:0 1px 4px rgba(35,55,25,.025);
  }
  .dashboard-welcome-copy{min-width:0;flex:1}
  .dashboard-section-label{
    display:inline-flex;align-items:center;gap:5px;
    color:#a0a69f;font-size:8px;font-weight:850;
    letter-spacing:.08em;text-transform:uppercase;
  }
  .dashboard-welcome-copy h2{
    margin:4px 0 7px;color:#4d534d;
    font-size:26px;line-height:1.15;font-weight:650;letter-spacing:-.035em;
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  }
  .dashboard-welcome-copy p{
    margin:0;color:#858c83;font-size:13px;
    max-width:68ch;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  }
  .dashboard-welcome-meta{
    display:flex;align-items:center;gap:7px;margin-top:11px;
    color:#55a51e;font-size:10px;font-weight:800;
  }
  .dashboard-welcome-meta span{
    display:inline-flex;align-items:center;min-height:22px;padding:0 8px;
    border:1px solid #edf1eb;border-radius:7px;background:#f8fbf6;
    white-space:nowrap;
  }
  .dashboard-welcome-meta i{width:3px;height:3px;flex:none;border-radius:50%;background:#d0d5cd}
  .dashboard-v3-level{
    --level-progress:0;
    position:relative;width:88px;min-width:88px;height:88px;
    display:grid;place-items:center;border-radius:50%;
    background:conic-gradient(var(--dash-green) calc(var(--level-progress) * 1%),#edf2e9 0);
    color:#55a51e;
  }
  .dashboard-v3-level::after{
    content:"";position:absolute;inset:7px;border-radius:50%;background:#fff;
  }
  .dashboard-v3-level span{position:relative;z-index:1;font-size:18px;font-weight:900}
  .dashboard-v3-level small{position:absolute;z-index:1;bottom:18px;color:#9aa197;font-size:7px;font-weight:850;line-height:1}

  .dashboard-v3-card-head{
    display:flex;align-items:center;justify-content:space-between;gap:10px;
    padding-bottom:2px;
  }
  .dashboard-v3-card-head h2{margin:0;color:#505650;font-size:16px;font-weight:800;letter-spacing:-.01em}
  .dashboard-v3-card-head h3{margin:3px 0 0;color:#565c55;font-size:12px;font-weight:850;letter-spacing:-.01em}
  .dashboard-v3-card-head>div{min-width:0}
  .dashboard-v3-card-head>div>h2{margin-top:3px}
  .dashboard-v3-card-head>div>h3{margin-top:3px}
  .dashboard-v3-card-head>div>span{line-height:1.2}
  .dashboard-v3-card-head span{color:#a0a69f;font-size:8px;font-weight:750}
  .dashboard-v3-card-head>strong{flex:none;color:#55a51e;font-size:10px;font-weight:850}
  .dashboard-v3-card-head h3,.dashboard-v3-card-head strong{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .dashboard-daily .dashboard-v3-card-head>strong{
    align-self:flex-start;
    color:#55a51e;font-size:12px;font-weight:900;
    white-space:nowrap;
    padding-top:3px;
  }
  .dashboard-v3-card-head>strong{color:#555;font-size:12px}
  .dashboard-daily{padding:19px}
  .dashboard-v3-chart{
    height:190px;margin-top:14px;padding:12px 4px 0;
    display:flex;align-items:flex-end;gap:13px;
    border-top:1px solid #f0f2ee;
    border-bottom:1px solid #f0f2ee;
    background-image:linear-gradient(to top,transparent 24.7%,#f4f5f2 24.8%,#f4f5f2 25%,transparent 25.1%,transparent 49.7%,#f4f5f2 49.8%,#f4f5f2 50%,transparent 50.1%,transparent 74.7%,#f4f5f2 74.8%,#f4f5f2 75%,transparent 75.1%);
  }
  .dashboard-v3-chart-col{
    flex:1;min-width:16px;height:100%;
    display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:8px;
  }
  .dashboard-v3-chart-col span{
    width:22px;max-width:100%;min-height:8px;
    display:block;border-radius:5px 5px 2px 2px;background:var(--dash-yellow);
    transform-origin:bottom;transition:height .22s ease,filter .14s ease,transform .14s ease;
  }
  .dashboard-v3-chart-col:hover span{
    filter:brightness(.98);
    transform:scaleX(1.03);
  }
  .dashboard-v3-chart-col small{
    display:block;min-width:24px;text-align:center;line-height:1;
  }
  .dashboard-v3-chart-col.active span{background:var(--dash-green)}
  .dashboard-v3-chart-col small{color:#929991;font-size:9px}
  .dashboard-v3-chart-col.active small{color:#58a91b;font-weight:800}
  .dashboard-insight-card,.dashboard-stat-card{
    transition:border-color .14s ease,box-shadow .14s ease;
  }
  .dashboard-insight-card:hover,.dashboard-stat-card:hover{
    border-color:#dfe8db;
    box-shadow:0 2px 7px rgba(35,55,25,.03);
  }
  .dashboard-v3-chart-footer,.dashboard-chart-footer,.dashboard-chart-summary{
    display:flex;justify-content:space-between;gap:10px;
    color:#858c83;font-size:10px;
  }
  .dashboard-v3-chart-footer span,
  .dashboard-chart-footer span{
    display:inline-flex;align-items:center;gap:4px;min-width:0;
  }
  .dashboard-v3-chart-footer,.dashboard-chart-footer{margin-top:10px}
  .dashboard-chart-footer b,.dashboard-chart-summary b{color:#55a51e}
  .dashboard-chart-summary{
    margin-top:10px;padding-top:10px;border-top:1px solid #f0f2ee;
  }
  .dashboard-chart-summary span{
    min-width:0;
  }
  .dashboard-chart-summary span{display:flex;flex-direction:column;gap:2px}
  .dashboard-chart-summary small{color:#a0a69f;font-size:8px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .dashboard-chart-summary b{font-size:11px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

  .dashboard-reference-insights,.dashboard-reference-stats{
    display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;
    align-items:stretch;
  }
  .dashboard-insight-card,.dashboard-stat-card{
    min-width:0;height:100%;padding:17px;
  }
  .dashboard-insight-card{display:flex;flex-direction:column}
  .dashboard-insight-card .dashboard-v3-card-head{min-height:38px}
  .dashboard-insight-card .dashboard-v3-card-head svg,
  .dashboard-stat-card .dashboard-v3-card-head svg{color:#a1a89e;flex:none}
  .dashboard-insight-value{display:flex;align-items:baseline;gap:7px;margin:14px 0 9px}
  .dashboard-insight-value strong{color:#555;font-size:29px}
  .dashboard-insight-value span{color:#999;font-size:10px}
  .dashboard-insight-track,.dashboard-small-progress,.dashboard-stat-track{
    height:6px;overflow:hidden;border-radius:99px;background:#eef1ed;
  }
  .dashboard-insight-track{margin-top:auto}
  .dashboard-insight-track span,.dashboard-small-progress span,.dashboard-stat-track span{
    display:block;height:100%;border-radius:inherit;background:var(--dash-yellow);
  }
  .dashboard-insight-footer{
    display:grid;grid-template-columns:auto 1fr auto 1fr;
    gap:7px;margin-top:11px;color:#999;font-size:9px;
  }
  .dashboard-insight-footer b{text-align:end;color:#555}
  .dashboard-words-value{display:flex;align-items:baseline;gap:7px;margin:14px 0 5px}
  .dashboard-words-value strong{color:#555;font-size:28px}
  .dashboard-words-value span{color:#999;font-size:10px}
  .dashboard-word-bars{height:58px;display:flex;align-items:flex-end;gap:7px}
  .dashboard-word-bars span{flex:1;max-width:18px;border-radius:4px 4px 0 0;background:var(--dash-yellow)}
  .dashboard-word-bars span.active{background:var(--dash-green)}
  .dashboard-stat-value{margin-top:13px;color:#555;font-size:27px;font-weight:800}
  .dashboard-stat-caption{margin:2px 0 8px;color:#999;font-size:9px}
  .dashboard-stat-breakdown{display:grid;gap:7px;margin-top:12px}
  .dashboard-stat-breakdown span{
    display:grid;grid-template-columns:7px 1fr auto;gap:8px;
    align-items:center;color:#888;font-size:9px;
  }
  .dashboard-stat-breakdown i{width:6px;height:6px;border-radius:50%;background:var(--dash-yellow)}
  .dashboard-stat-breakdown b{color:#555}

  .dashboard-achievement-strip{
    min-height:72px;display:flex;align-items:center;gap:12px;padding:13px 15px;
  }
  .dashboard-achievement-strip-icon{
    width:42px;height:42px;flex:none;display:grid;place-items:center;
    border-radius:9px;background:var(--dash-green-soft);color:#55a51e;
  }
  .dashboard-achievement-strip-copy{display:flex;flex-direction:column;min-width:0;gap:2px}
  .dashboard-achievement-strip-copy strong{color:#555;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .dashboard-achievement-strip-copy small{color:#999;font-size:8px}
  .dashboard-achievement-strip-progress{
    width:150px;height:6px;margin-inline-start:auto;overflow:hidden;
    border-radius:99px;background:#eef1ed;
  }
  .dashboard-achievement-strip-progress span{display:block;height:100%;border-radius:inherit;background:var(--dash-yellow);transition:width .2s ease}
  .dashboard-achievement-strip:hover .dashboard-achievement-strip-progress span{filter:brightness(.98)}

  .dashboard-course{padding:18px}
  .dashboard-card-header{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;min-width:0}
  .dashboard-card-header>div{min-width:0;flex:1}
  .dashboard-card-header>div>h2,.dashboard-card-header>div>p{overflow:hidden;text-overflow:ellipsis}
  .dashboard-card-header>div>h2{white-space:nowrap}
  .dashboard-card-header>div>p{white-space:nowrap}

  .dashboard-card-header h2{margin:3px 0;color:#505650;font-size:16px;font-weight:800;letter-spacing:-.01em}
  .dashboard-card-header p{margin:0;color:#999;font-size:10px;line-height:1.4}
  .dashboard-card-header .dashboard-outline-button{flex:none;margin-top:2px}
  .dashboard-outline-button,.dashboard-green-button{
    display:inline-flex;align-items:center;justify-content:center;gap:7px;
    padding:8px 12px;border-radius:8px;
    font-size:10px;font-weight:800;text-decoration:none;
    transition:transform .12s ease,filter .12s ease,background .12s ease;
  }
  .dashboard-green-button{
    border:1px solid var(--dash-green);
    background:var(--dash-green);color:#fff;
    box-shadow:0 2px 0 var(--dash-green-dark);
  }
  .dashboard-outline-button{
    border:1px solid #dce7d8;
    background:#fff;color:#55a51e;
    box-shadow:none;
  }
  .dashboard-outline-button:hover,.dashboard-green-button:hover{filter:brightness(.98)}
  .dashboard-outline-button:hover{background:#f7fbf4}
  .dashboard-progress-row{display:flex;align-items:center;gap:10px;margin-top:12px}
  .dashboard-progress-row>strong{min-width:30px;text-align:right;flex:none}

  .dashboard-course-path{position:relative;--course-path-progress:0}
  .dashboard-course-path::before{
    content:"";position:absolute;left:31px;top:25px;bottom:25px;
    width:2px;border-radius:99px;background:#edf1eb;
  }
  .dashboard-course-path::after{
    content:"";position:absolute;left:31px;top:25px;
    width:2px;height:calc(var(--course-path-progress, 0) * (100% - 50px));
    border-radius:99px;background:var(--dash-green);pointer-events:none;
  }
  .dashboard-lesson{position:relative;z-index:1}
  .dashboard-course-path > .dashboard-lesson{background:transparent}
  .dashboard-course-path > .dashboard-lesson.current{background:#fbfff8}
  .dashboard-lesson.current{z-index:2}

  .dashboard-progress-meta{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:9px}
  .dashboard-progress-meta-cell{display:flex;flex-direction:column;gap:2px;padding:7px 9px;border:1px solid #ecefec;border-radius:7px;background:#fff;min-width:0}
  .dashboard-progress-meta-cell small{font-size:7px;font-weight:850;color:#aaa;text-transform:uppercase;letter-spacing:.05em}
  .dashboard-progress-meta-cell b{font-size:10px;color:#555;line-height:1.25;min-width:0}
  .dashboard-progress-meta-cell.is-green b{color:#58a91b}
  .dashboard-progress-meta-cell small,
  .dashboard-progress-meta-cell b{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .dashboard-lesson.current{background:#fbfff8;box-shadow:inset 3px 0 0 #58cc02;min-height:72px;border-bottom-color:#e8eee4}
  .dashboard-lesson.done .dashboard-lesson-copy strong{color:#727971}
  .dashboard-lesson.done .dashboard-lesson-copy>span{color:#a1a69f}
  .dashboard-lesson-title{display:flex;align-items:center;gap:7px;min-width:0}
  .dashboard-lesson-title strong{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .dashboard-lesson-code{font-size:8px;font-weight:950;color:#b2b2b2;letter-spacing:.05em;text-transform:uppercase;white-space:nowrap}
  .dashboard-lesson.done .dashboard-lesson-code,.dashboard-lesson.current .dashboard-lesson-code{color:#58a91b}
  .dashboard-lesson.current .dashboard-path-node{width:34px;height:34px;margin-inline-start:-2px;box-shadow:0 0 0 5px #f4faef;font-size:10px}
  .dashboard-lesson-current-action{display:flex;align-items:center;gap:7px}
  .dashboard-lesson-current-action>span{font-size:8px;font-weight:900;color:#58a91b;letter-spacing:.04em;text-transform:uppercase}
  .dashboard-lesson-action{align-self:stretch;display:flex;align-items:center}
  .dashboard-completed,.dashboard-locked{display:inline-flex;align-items:center;justify-content:flex-end;gap:5px;min-width:112px;color:#a1a69f;font-size:8px;font-weight:800}
  .dashboard-completed svg{color:#58a91b}
  .dashboard-locked{color:#c0c5bd}

  .dashboard-progress-track{height:6px;flex:1;overflow:hidden;border-radius:99px;background:#eef1ed}
  .dashboard-progress-track span{display:block;height:100%;border-radius:inherit;background:var(--dash-yellow)}
  .dashboard-progress-row>strong{color:#55a51e;font-size:10px}
  .dashboard-course-path .dashboard-lesson-copy strong{font-weight:800}
  .dashboard-course-path .dashboard-lesson-copy>span{
    max-width:52ch;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  }
  .dashboard-course-path .dashboard-lesson-copy{min-width:0}

  .dashboard-course-path .dashboard-lesson-action{
    min-width:112px;display:flex;justify-content:flex-end;
  }
  .dashboard-course-path .dashboard-lesson-action .dashboard-completed,
  .dashboard-course-path .dashboard-lesson-action .dashboard-locked{
    min-width:112px;
  }
  .dashboard-course-path .dashboard-lesson-action svg{flex:none}
  .dashboard-course-path .dashboard-lesson-action span{white-space:nowrap}
  .dashboard-course-path .dashboard-lesson-action .dashboard-completed,
  .dashboard-course-path .dashboard-lesson-action .dashboard-locked{opacity:.92}
  .dashboard-lessons,.dashboard-course-path{margin-top:14px}
  .dashboard-lesson{
    display:grid;grid-template-columns:40px minmax(0,1fr) auto;
    gap:10px;align-items:center;min-height:66px;
    padding:10px 12px;border-bottom:1px solid #f0f2ee;background:#fff;
    transition:background .14s ease,box-shadow .14s ease;
  }
  .dashboard-lesson:not(.current):hover{
    background:#fbfdf9;
  }
  .dashboard-lesson.done:hover{
    background:#f9fbf7;
  }
  .dashboard-lesson:last-child{border-bottom:0}
  .dashboard-path-rail{display:flex;justify-content:center}
  .dashboard-path-node{
    width:27px;height:27px;display:grid;place-items:center;
    border:2px solid #e2e6e1;border-radius:50%;background:#fff;color:#aaa;
    font-size:9px;font-weight:900;
  }
  .dashboard-path-node.done{border-color:var(--dash-green);color:var(--dash-green)}
  .dashboard-path-node.current{border-color:var(--dash-green);background:var(--dash-green);color:#fff}
  .dashboard-lesson-copy{min-width:0}
  .dashboard-lesson-copy strong{color:#4f534f;font-size:12px}
  .dashboard-lesson-copy>span{display:block;margin-top:2px;color:#969b95;font-size:9px}
  .dashboard-empty{display:flex;align-items:center;gap:12px;padding:22px 0;color:#999}
  .dashboard-empty .dashboard-green-button{margin-inline-start:auto}
  .dashboard-empty div{display:flex;flex-direction:column;gap:3px}
  .dashboard-empty strong{color:#666;font-size:11px}
  .dashboard-empty span{font-size:9px}

  .dashboard-v3-rail{
    display:flex;flex-direction:column;gap:14px;min-width:0;
    position:sticky;top:14px;align-self:start;
  }
  .dashboard-v3-rail .dashboard-v3-card{
    transition:border-color .14s ease,box-shadow .14s ease;
  }
  .dashboard-v3-rail .dashboard-v3-card:hover{
    border-color:#dfe8db;
    box-shadow:0 2px 7px rgba(35,55,25,.035);
  }
  .dashboard-profile-card,.dashboard-goal-card,.dashboard-xp-card,
  .dashboard-achievement-card,.dashboard-tools-card,.dashboard-friends-card{padding:16px}
  .dashboard-v3-rail .dashboard-v3-card-head{min-height:34px}
  .dashboard-profile-metrics span+span{border-inline-start:1px solid #edf1eb}
  .dashboard-tools-card>a+a{border-top:1px solid #f1f3ef}
  .dashboard-profile-hero{
    display:flex;flex-direction:column;align-items:center;text-align:center;
    padding-bottom:13px;
  }
  .dashboard-profile-photo{
    width:52px;height:52px;overflow:hidden;border-radius:50%;
    display:grid;place-items:center;background:#f0f3ed;color:#7f877d;
    border:2px solid #eef2eb;
  }
  .dashboard-profile-photo img{width:100%;height:100%;object-fit:cover}
  .dashboard-profile-hero>strong{margin-top:8px;color:#4e544e;font-size:12px;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .dashboard-profile-hero>span{margin-top:2px;color:#929991;font-size:9px;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .dashboard-profile-metrics{
    display:grid;grid-template-columns:repeat(3,1fr);
    padding-top:12px;border-top:1px solid #edf1eb;
  }
  .dashboard-profile-metrics span{display:flex;flex-direction:column;align-items:center;gap:2px}
  .dashboard-profile-metrics b{color:#4f554f;font-size:13px}
  .dashboard-profile-metrics small{color:#999;font-size:8px}
  .dashboard-goal-ring{
    width:70px;height:70px;margin:15px auto 10px;
    display:flex;align-items:center;justify-content:center;
    flex-direction:column;border-radius:50%;position:relative;
  }
  .dashboard-goal-ring::after{
    content:"";position:absolute;inset:6px;border-radius:50%;background:#fff;
  }
  .dashboard-goal-ring strong,.dashboard-goal-ring span{position:relative;z-index:1}
  .dashboard-goal-ring strong{color:#555;font-size:17px}
  .dashboard-goal-ring span{color:#999;font-size:8px}
  .dashboard-goal-copy{display:flex;align-items:center;justify-content:center;gap:7px}
  .dashboard-goal-copy b{color:#55a51e;font-size:11px}
  .dashboard-goal-copy span{color:#999;font-size:8px}
  .dashboard-xp-list{display:grid;gap:7px;margin-top:13px}
  .dashboard-xp-list div{display:flex;justify-content:space-between;color:#8d948b;font-size:9px}
  .dashboard-xp-list b{color:#555}
  .dashboard-achievement-icon{
    width:58px;height:58px;margin:13px auto 9px;
    display:grid;place-items:center;border-radius:12px;
    background:#fff7d9;color:#e4a900;
  }
  .dashboard-achievement-card>strong{display:block;text-align:center;color:#555;font-size:11px}
  .dashboard-achievement-card>span{display:block;margin-top:3px;text-align:center;color:#999;font-size:8px}
  .dashboard-achievement-card .dashboard-small-progress{margin-top:10px}
  .dashboard-tools-card>a{
    min-height:36px;display:flex;align-items:center;gap:8px;
    padding:0 8px;border-radius:8px;color:#777;text-decoration:none;font-size:10px;
  }
  .dashboard-tools-card>a:hover{background:#f5f9f3;color:#55a51e}
  .dashboard-tools-card>a svg{color:#a1a89e;flex:none}
  .dashboard-friend-row{transition:background .14s ease}
  .dashboard-friend-arrow{transition:transform .14s ease}
  .dashboard-friend-row:hover .dashboard-friend-arrow{transform:translateX(2px)}
  .dashboard-tools-card>a span{flex:1}
  .dashboard-friends-list{display:grid;gap:3px;margin-top:10px}
  .dashboard-mini-link{color:#55a51e;font-size:8px;font-weight:800;text-decoration:none}
  .dashboard-friend-row{
    min-height:48px;display:flex;align-items:center;gap:8px;
    padding:5px 6px;border-radius:8px;text-decoration:none;
  }
  .dashboard-friend-row:hover{background:#f6f9f4}
  .dashboard-friend-avatar{
    width:34px;height:34px;flex:none;display:grid;place-items:center;
    overflow:hidden;border-radius:50%;background:#edf2e9;color:#687066;
    font-size:11px;font-weight:800;
  }
  .dashboard-friend-avatar img{width:100%;height:100%;object-fit:cover}
  .dashboard-friend-copy{min-width:0;display:flex;flex-direction:column;gap:2px;flex:1}
  .dashboard-friend-copy strong{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#555;font-size:10px}
  .dashboard-friend-copy small{color:#999;font-size:8px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .dashboard-friend-arrow{flex:none;color:#aaa;font-size:17px}
  .dashboard-friends-empty{display:block;padding:12px;color:#999;font-size:9px;text-decoration:none}
  .dashboard-premium{
    display:flex;flex-direction:column;gap:10px;padding:15px;
    border:1px solid #e7e3c8;border-radius:12px;background:#fffdf1;
    box-shadow:0 1px 4px rgba(35,55,25,.025);
  }
  .dashboard-premium-icon{color:#e2a800}
  .dashboard-premium>div:nth-child(2){display:flex;flex-direction:column;gap:3px}
  .dashboard-premium strong{color:#66571e;font-size:11px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .dashboard-premium span{color:#9b9060;font-size:8px;line-height:1.5;overflow:hidden}
  .dashboard-premium button{width:100%;padding:7px 9px;border:0;border-radius:7px;background:#e7b000;color:#fff;font-size:9px;font-weight:800;cursor:pointer;transition:filter .14s ease,transform .12s ease}
  .dashboard-premium button:hover{filter:brightness(.98)}
  .dashboard-premium button:active{transform:translateY(1px)}

  .dashboard-friends-card .dashboard-section-label{display:flex;align-items:center;gap:4px}
  .dashboard-friends-card .dashboard-section-label svg{flex:none}
  .dashboard-friends-card .dashboard-mini-link{white-space:nowrap}
  .dashboard-profile-photo .h-full{width:100%;height:100%}
  .dashboard-section-label{display:inline-flex;align-items:center;gap:5px;color:#a0a69f;font-size:8px;font-weight:850;letter-spacing:.08em;text-transform:uppercase}
  .dashboard-daily .dashboard-v3-card-head{padding-bottom:0}
  .dashboard-daily .dashboard-v3-card-head>strong{padding-top:2px}
  .dashboard-insight-footer{display:grid;grid-template-columns:auto auto auto auto;align-items:center;gap:5px 7px;margin-top:11px;color:#9a9f98;font-size:8px}
  .dashboard-insight-footer b{color:#555;font-size:9px;font-weight:850}
  .dashboard-insight-footer b:nth-of-type(2){color:#58a91b}
  .dashboard-topbar{position:relative}
  .dashboard-topbar-title{min-width:0}
  .dashboard-tools-card .dashboard-v3-card-head,.dashboard-friends-card .dashboard-v3-card-head{margin-bottom:4px}
  @media (max-width:1180px) and (min-width:901px){
    .dashboard-dashboard{padding-inline:18px}
    .dashboard-topbar{gap:14px}
    .dashboard-topbar-title{gap:12px}
    .dashboard-reference-nav{gap:2px}
    .dashboard-reference-nav a{padding-inline:9px}
    .dashboard-course-selector{max-width:170px}
    .dashboard-v3-grid{grid-template-columns:minmax(0,1fr) 250px;gap:18px}
    .dashboard-course{padding:16px}
    .dashboard-v3-chart{gap:10px}
    .dashboard-topbar{gap:18px}
  }
  @media (max-width:900px){
    .dashboard-dashboard{padding:10px 12px 24px;background:#fff}
    .dashboard-topbar{height:auto;min-height:54px;padding:8px 0;align-items:center}
    .dashboard-reference-nav{gap:0;min-width:0;overflow-x:auto;scrollbar-width:none}
    .dashboard-reference-nav::-webkit-scrollbar{display:none}
    .dashboard-reference-nav a{padding-inline:8px;font-size:10px}
    .dashboard-course-selector{display:none}
    .dashboard-v3-grid{grid-template-columns:1fr;gap:14px}
    .dashboard-v3-rail{position:static;margin-top:0}
    .dashboard-v3-welcome{min-height:118px;padding:17px;gap:12px}
    .dashboard-welcome-copy h2{font-size:22px}
    .dashboard-v3-level{width:68px;min-width:68px;height:68px}
    .dashboard-v3-level::after{inset:6px}
    .dashboard-v3-chart{height:170px;gap:9px;padding-inline:2px}
    .dashboard-v3-chart-col{min-width:0}
    .dashboard-v3-chart-col span{width:18px}
    .dashboard-v3-chart-col small{font-size:8px}
  }
  @media (max-width:620px){
    .dashboard-dashboard{padding-inline:10px}
    .dashboard-topbar{gap:8px}
    .dashboard-topbar-title{gap:7px;min-width:0;flex:1}
    .dashboard-dot{width:30px;height:30px;border-radius:8px;font-size:10px}
    .dashboard-topbar-actions{flex:none}
    .dashboard-reference-nav{width:100%;min-width:0}
    .dashboard-reference-nav a{flex:1;justify-content:center;padding-inline:4px}
    .dashboard-reference-nav a.is-active::after{left:4px;right:4px}
    .dashboard-icon-button{flex:none}
    .dashboard-welcome-meta{flex-wrap:wrap;gap:5px}
    .dashboard-welcome-meta i{display:none}
    .dashboard-welcome-meta span{min-height:21px;padding-inline:7px;font-size:9px}
    .dashboard-reference-insights,.dashboard-reference-stats{grid-template-columns:1fr}
    .dashboard-course-path::before{left:27px}
    .dashboard-empty{flex-wrap:wrap}
    .dashboard-achievement-strip{align-items:flex-start}
    .dashboard-achievement-strip-progress{display:none}
    .dashboard-card-header{flex-direction:column}
    .dashboard-card-header .dashboard-outline-button{margin-top:0;width:100%}
    .dashboard-outline-button{width:100%}
    .dashboard-lesson{grid-template-columns:32px minmax(0,1fr);gap:8px}
    .dashboard-lesson-action{grid-column:2;justify-self:start;min-width:0}
    .dashboard-course-path .dashboard-lesson-copy>span{max-width:none}
    .dashboard-course-path .dashboard-lesson-action{justify-content:flex-start;width:100%}
    .dashboard-course-path .dashboard-lesson-action .dashboard-completed,
    .dashboard-course-path .dashboard-lesson-action .dashboard-locked{min-width:0}
    .dashboard-progress-meta{gap:6px}
    .dashboard-progress-meta-cell{padding-inline:8px}
    .dashboard-lesson.current{padding-block:12px}
    .dashboard-lesson-current-action{min-height:28px}
  }`}</style>
    </>
  )
}
