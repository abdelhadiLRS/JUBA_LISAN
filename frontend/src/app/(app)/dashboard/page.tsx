'use client'

import { useEffect, useState, useCallback, type CSSProperties } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import {
  ArrowUpRight,
  BookOpen,
  Check,
  ChevronDown,
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
import './dashboard.module.css'

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
  const coursePathCompletedCount = todayLessons.filter((lesson) => (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted).length
  const coursePathCurrentIndex = todayLessons.findIndex((lesson) => {
    const done = (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
    return !done && (!nextLesson || lesson.id === nextLesson.id)
  })
  const coursePathCurrentLabel = coursePathCurrentIndex >= 0 ? `${coursePathCurrentIndex + 1}` : todayLessons.length ? `${todayLessons.length}` : '0'
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
              <div className="dashboard-progress-meta" style={{display:'grid',gridTemplateColumns:'repeat(3,minmax(0,1fr))',gap:8,marginTop:9}}>
                <span style={{display:'flex',flexDirection:'column',gap:2,padding:'7px 9px',border:'1px solid #ececec',borderRadius:7,background:'#fff'}}><small style={{fontSize:7,fontWeight:850,color:'#aaa',textTransform:'uppercase',letterSpacing:'.05em'}}>{t('today')}</small><b style={{fontSize:10,color:'#555'}}>{currentDayDisplay}/{totalDays || 0}</b></span>
                <span style={{display:'flex',flexDirection:'column',gap:2,padding:'7px 9px',border:'1px solid #ececec',borderRadius:7,background:'#fff'}}><small style={{fontSize:7,fontWeight:850,color:'#aaa',textTransform:'uppercase',letterSpacing:'.05em'}}>{t('completedToday',{completed:completedLessonCount,total:todayLessons.length})}</small><b style={{fontSize:10,color:'#58a91b'}}>{completedLessonCount}/{todayLessons.length}</b></span>
                <span style={{display:'flex',flexDirection:'column',gap:2,padding:'7px 9px',border:'1px solid #ececec',borderRadius:7,background:'#fff'}}><small style={{fontSize:7,fontWeight:850,color:'#aaa',textTransform:'uppercase',letterSpacing:'.05em'}}>{t('nextStep')}</small><b style={{fontSize:10,color:'#555'}}>{coursePathCurrentLabel}/{todayLessons.length || 0}</b></span>
              </div>
              <div className="dashboard-lessons dashboard-course-path" style={{ "--course-path-progress": String(coursePathProgress) } as React.CSSProperties}>
                {todayLessons.length ? todayLessons.map((lesson,index) => {
                  const done = (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
                  const current = !done && (!nextLesson || lesson.id === nextLesson.id)
                  return (
                    <div key={lesson.id ?? lesson.title} aria-current={current ? 'step' : undefined} data-checkpoint-state={done ? 'completed' : current ? 'current' : 'upcoming'} className={`dashboard-lesson ${current ? 'current' : ''} ${done ? 'done' : ''}`} style={current ? { background: '#fbfff8', boxShadow: 'inset 3px 0 0 #58cc02', minHeight: 72, borderBottomColor: '#e8eee4' } : done ? { background: '#fff' } : undefined}>
                      <div className="dashboard-path-rail" aria-hidden="true">
                        <span className={`dashboard-path-node ${done ? 'done' : current ? 'current' : ''}`} style={current ? { width: 34, height: 34, marginInlineStart: -2, boxShadow: '0 0 0 5px #f4faef', fontSize: 10 } : undefined}>
                          {done ? <Check size={14} strokeWidth={3} /> : current ? <Play size={13} fill="currentColor" /> : <span>{index + 1}</span>}
                        </span>
                      </div>
                      <div className="dashboard-lesson-copy">
                        <div style={{display:'flex',alignItems:'center',gap:7,minWidth:0}}>
                          <span style={{fontSize:8,fontWeight:950,color:done ? '#58a91b' : current ? '#58a91b' : '#b2b2b2',letterSpacing:'.05em',textTransform:'uppercase',whiteSpace:'nowrap'}}>CP {String(index + 1).padStart(2,'0')}</span>
                          <strong style={{overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{lesson.title}</strong>
                        </div>
                        <span>{tPlan('lessonTypes.' + lesson.lessonType)} · {lesson.estimatedMinutes} {t('minutes')}</span>
                      </div>
                      <div className="dashboard-lesson-action">
                        {current && lesson.id ? <div style={{display:'flex',alignItems:'center',gap:7}}><span style={{fontSize:8,fontWeight:900,color:'#58a91b',letterSpacing:'.04em',textTransform:'uppercase'}}>{t('today')}</span><Link href={'/lesson/' + lesson.id} className="dashboard-green-button">{t('startLesson')}</Link></div> : done ? <span className="dashboard-completed"><Check size={14} />{t('completedToday',{completed:1,total:1})}</span> : <span className="dashboard-locked"><MoreHorizontal size={17} /></span>}
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
                  {user?.avatar ? <img src={user.avatar} alt="" /> : <UserRound size={28} />}
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
    </>
  )
}
