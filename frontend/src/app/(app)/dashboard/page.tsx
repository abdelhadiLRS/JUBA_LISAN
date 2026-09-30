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
      <style>{`
        /* JUBA LISAN — strict reference UI system (dashboard only) */
        .juba-reference-shell{background:#fff!important;color:#4b4b4b}
        .juba-reference-shell .juba-duo-sidebar{width:220px!important;background:#fff!important;border-right:1px solid #f0f0f0!important;box-shadow:none!important}
        .juba-reference-shell .juba-duo-main{background:#fff!important}
        .juba-reference-shell .juba-duo-logo-mark{width:42px!important;height:42px!important;border:0!important;border-radius:14px!important;background:#58cc02!important;color:#fff!important;display:grid!important;place-items:center!important;font-weight:900!important;font-size:13px!important;box-shadow:0 3px 0 #46a302!important}
        .juba-reference-shell .juba-duo-nav{padding:12px 12px 0!important}
        .juba-reference-shell .juba-duo-nav-link{min-height:46px!important;border:0!important;border-radius:10px!important;padding:8px 12px!important;margin:3px 0!important;color:#777!important;font-size:13px!important;font-weight:700!important;letter-spacing:0!important;text-transform:none!important}
        .juba-reference-shell .juba-duo-nav-link:hover{background:#f6fbf3!important;color:#58a91b!important}
        .juba-reference-shell .juba-duo-nav-link.is-active{background:#f0fae9!important;color:#58a91b!important;box-shadow:none!important}
        .juba-reference-shell .juba-duo-resource-toggle{min-height:40px!important;padding:8px 12px!important;color:#999!important;font-size:11px!important;font-weight:800!important}
        .juba-reference-shell .juba-duo-user{border-top:1px solid #f1f1f1!important;background:#fff!important;padding:14px!important}
        .juba-reference-shell .juba-duo-user-action{color:#888!important}
        .juba-reference-shell .juba-duo-page-frame{background:#fff!important}
        .juba-reference-shell .juba-duo-mobile-bar{display:none!important}

        .juba-reference-v3{min-height:100%;background:#fff!important;padding:0 22px 30px!important;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
        .juba-reference-v3 .juba-reference-topbar{height:72px!important;max-width:1390px;margin:0 auto!important;border-bottom:0!important;background:#fff!important;display:flex!important;align-items:center!important;justify-content:space-between!important;gap:24px!important}
        .juba-reference-v3 .juba-reference-topbar-title{display:flex!important;align-items:center!important;gap:26px!important}
        .juba-reference-v3 .juba-reference-dot{display:none!important}
        .juba-reference-v3 .juba-reference-reference-nav{display:flex!important;align-items:center!important;gap:34px!important}
        .juba-reference-v3 .juba-reference-reference-nav a{position:relative!important;color:#777!important;font-size:12px!important;font-weight:800!important;text-transform:uppercase!important;letter-spacing:.01em!important;padding:28px 0 24px!important}
        .juba-reference-v3 .juba-reference-reference-nav a:hover{color:#58a91b!important}
        .juba-reference-v3 .juba-reference-reference-nav a.is-active{color:#58a91b!important}
        .juba-reference-v3 .juba-reference-reference-nav a.is-active:after{content:""!important;position:absolute!important;left:0!important;right:0!important;bottom:15px!important;height:2px!important;background:#58cc02!important;border-radius:99px!important}
        .juba-reference-v3 .juba-reference-topbar-actions{display:flex!important;align-items:center!important;gap:12px!important}
        .juba-reference-v3 .juba-reference-course-selector{display:flex!important;align-items:center!important;gap:10px!important;color:#777!important;font-size:11px!important}
        .juba-reference-v3 .juba-reference-course-selector strong{color:#555!important;font-size:12px!important}
        .juba-reference-v3 .juba-reference-icon-button{width:34px!important;height:34px!important;border:1px solid #ececec!important;border-radius:9px!important;background:#fff!important;color:#888!important}
        .juba-reference-v3 .juba-reference-v3-grid{max-width:1390px;margin:0 auto!important;display:grid!important;grid-template-columns:minmax(0,1fr) 284px!important;gap:26px!important;align-items:start!important}
        .juba-reference-v3 .juba-reference-v3-main{min-width:0!important}
        .juba-reference-v3 .juba-reference-v3-main>section{margin-bottom:18px!important}
        .juba-reference-v3 .juba-reference-v3-welcome{position:relative!important;min-height:142px!important;display:flex!important;align-items:center!important;justify-content:space-between!important;padding:24px 18px 18px 112px!important;border:0!important;border-radius:0!important;background:#fff!important;box-shadow:none!important}
        .juba-reference-v3 .juba-reference-v3-welcome:before{content:""!important;position:absolute!important;left:16px!important;top:30px!important;width:82px!important;height:82px!important;background:url('/logo_head.png') center/contain no-repeat!important}
        .juba-reference-v3 .juba-reference-welcome-copy{max-width:720px!important}
        .juba-reference-v3 .juba-reference-section-label{display:inline-flex!important;align-items:center!important;gap:6px!important;color:#8b8b8b!important;font-size:10px!important;font-weight:800!important;letter-spacing:.04em!important;text-transform:uppercase!important}
        .juba-reference-v3 .juba-reference-welcome-copy h2{margin:2px 0 7px!important;color:#505050!important;font-size:30px!important;line-height:1.15!important;font-weight:500!important;letter-spacing:-.03em!important}
        .juba-reference-v3 .juba-reference-welcome-copy h2::first-line{font-weight:700!important}
        .juba-reference-v3 .juba-reference-welcome-copy p{margin:0!important;color:#777!important;font-size:14px!important}
        .juba-reference-v3 .juba-reference-welcome-meta{display:flex!important;gap:10px!important;align-items:center!important;margin-top:11px!important;color:#58a91b!important;font-size:11px!important;font-weight:800!important}
        .juba-reference-v3 .juba-reference-welcome-meta i{width:4px!important;height:4px!important;border-radius:50%!important;background:#cfcfcf!important}
        .juba-reference-v3 .juba-reference-v3-level{min-width:92px!important;width:92px!important;height:92px!important;border-radius:50%!important;background:conic-gradient(#58cc02 calc(var(--level-progress,0) * 1%),#edf2e9 0)!important;display:grid!important;place-items:center!important;position:relative!important;color:#58a91b!important;box-shadow:none!important}
        .juba-reference-v3 .juba-reference-v3-level:after{content:""!important;position:absolute!important;inset:8px!important;border-radius:50%!important;background:#fff!important}
        .juba-reference-v3 .juba-reference-v3-level span,.juba-reference-v3 .juba-reference-v3-level small{position:relative!important;z-index:1!important}
        .juba-reference-v3 .juba-reference-v3-level span{font-size:18px!important;font-weight:900!important}
        .juba-reference-v3 .juba-reference-v3-level small{display:none!important}

        .juba-reference-v3 .juba-reference-v3-main>section{border:1px solid #edf0ea!important;background:#fff!important;border-radius:12px!important;box-shadow:0 2px 8px rgba(0,0,0,.025)!important}
        .juba-reference-v3 .juba-reference-v3-card{border:1px solid #edf0ea!important;background:#fff!important;border-radius:12px!important;box-shadow:none!important}
        .juba-reference-v3 .juba-reference-v3-card-head{display:flex!important;align-items:center!important;justify-content:space-between!important;gap:14px!important}
        .juba-reference-v3 .juba-reference-v3-card-head h2,.juba-reference-v3 .juba-reference-v3-card-head h3{margin:3px 0 0!important;color:#505050!important;font-size:16px!important;font-weight:800!important}
        .juba-reference-v3 .juba-reference-v3-card-head>strong{color:#555!important;font-size:13px!important}
        .juba-reference-v3 .juba-reference-daily{padding:20px!important}
        .juba-reference-v3 .juba-reference-v3-chart{height:155px!important;display:flex!important;align-items:flex-end!important;gap:14px!important;padding:12px 4px 0!important;border-top:1px solid #f0f0f0!important;margin-top:15px!important}
        .juba-reference-v3 .juba-reference-v3-chart-col{flex:1!important;min-width:18px!important;height:100%!important;display:flex!important;flex-direction:column!important;justify-content:flex-end!important;align-items:center!important;gap:8px!important}
        .juba-reference-v3 .juba-reference-v3-chart-col span{display:block!important;width:22px!important;max-width:100%!important;border-radius:5px 5px 2px 2px!important;background:#ffb900!important;box-shadow:none!important}
        .juba-reference-v3 .juba-reference-v3-chart-col small{color:#888!important;font-size:9px!important}
        .juba-reference-v3 .juba-reference-chart-footer,.juba-reference-v3 .juba-reference-chart-summary{display:flex!important;justify-content:space-between!important;gap:10px!important;color:#888!important;font-size:10px!important;margin-top:10px!important}
        .juba-reference-v3 .juba-reference-chart-footer b,.juba-reference-v3 .juba-reference-chart-summary b{color:#58a91b!important}
        .juba-reference-v3 .juba-reference-chart-summary{border-top:1px solid #f0f0f0!important;padding-top:10px!important}

        .juba-reference-v3 .juba-reference-reference-insights{display:grid!important;grid-template-columns:1fr 1fr!important;gap:14px!important;padding:0!important;border:0!important;background:transparent!important;box-shadow:none!important}
        .juba-reference-v3 .juba-reference-reference-insights .juba-reference-v3-card{padding:18px!important}
        .juba-reference-v3 .juba-reference-insight-value{display:flex!important;align-items:baseline!important;gap:7px!important;margin:14px 0 9px!important}
        .juba-reference-v3 .juba-reference-insight-value strong{font-size:30px!important;color:#555!important}
        .juba-reference-v3 .juba-reference-insight-value span{font-size:11px!important;color:#999!important}
        .juba-reference-v3 .juba-reference-insight-track,.juba-reference-v3 .juba-reference-small-progress,.juba-reference-v3 .juba-reference-stat-track{height:7px!important;background:#eef1ed!important;border-radius:99px!important;overflow:hidden!important}
        .juba-reference-v3 .juba-reference-insight-track span,.juba-reference-v3 .juba-reference-small-progress span,.juba-reference-v3 .juba-reference-stat-track span{display:block!important;height:100%!important;background:#ffb900!important;border-radius:99px!important}
        .juba-reference-v3 .juba-reference-insight-footer{display:grid!important;grid-template-columns:auto 1fr auto 1fr!important;gap:7px!important;margin-top:12px!important;font-size:9px!important;color:#999!important}
        .juba-reference-v3 .juba-reference-insight-footer b{text-align:end!important;color:#555!important}
        .juba-reference-v3 .juba-reference-words-value{display:flex!important;align-items:baseline!important;gap:7px!important;margin:15px 0 5px!important}
        .juba-reference-v3 .juba-reference-words-value strong{font-size:28px!important;color:#555!important}
        .juba-reference-v3 .juba-reference-words-value span{font-size:11px!important;color:#999!important}
        .juba-reference-v3 .juba-reference-word-bars{height:60px!important;display:flex!important;align-items:flex-end!important;gap:7px!important}
        .juba-reference-v3 .juba-reference-word-bars span{flex:1!important;background:#ffb900!important;border-radius:4px 4px 0 0!important;max-width:18px!important}
        .juba-reference-v3 .juba-reference-word-bars span.active{background:#58cc02!important}
        .juba-reference-v3 .juba-reference-reference-stats{display:grid!important;grid-template-columns:1fr 1fr!important;gap:14px!important;padding:0!important;border:0!important;background:transparent!important;box-shadow:none!important}
        .juba-reference-v3 .juba-reference-reference-stats .juba-reference-v3-card{padding:18px!important}
        .juba-reference-v3 .juba-reference-stat-value{margin-top:14px!important;color:#555!important;font-size:28px!important;font-weight:800!important}
        .juba-reference-v3 .juba-reference-stat-caption{margin:2px 0 8px!important;color:#999!important;font-size:10px!important}
        .juba-reference-v3 .juba-reference-stat-breakdown{display:grid!important;gap:7px!important;margin-top:13px!important}
        .juba-reference-v3 .juba-reference-stat-breakdown span{display:grid!important;grid-template-columns:8px 1fr auto!important;gap:8px!important;align-items:center!important;color:#888!important;font-size:10px!important}
        .juba-reference-v3 .juba-reference-stat-breakdown i{width:6px!important;height:6px!important;border-radius:50%!important;background:#ffb900!important}
        .juba-reference-v3 .juba-reference-stat-breakdown b{color:#555!important}

        .juba-reference-v3 .juba-reference-achievement-strip{display:flex!important;align-items:center!important;gap:13px!important;padding:14px 16px!important}
        .juba-reference-v3 .juba-reference-achievement-strip-icon{width:42px!important;height:42px!important;border-radius:9px!important;background:#eef9df!important;color:#58a91b!important;display:grid!important;place-items:center!important;flex:none!important}
        .juba-reference-v3 .juba-reference-achievement-strip-copy{display:flex!important;flex-direction:column!important;min-width:0!important;gap:2px!important}
        .juba-reference-v3 .juba-reference-achievement-strip-copy strong{color:#555!important;font-size:12px!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
        .juba-reference-v3 .juba-reference-achievement-strip-copy small{color:#999!important;font-size:9px!important}
        .juba-reference-v3 .juba-reference-achievement-strip-progress{margin-inline-start:auto!important;width:150px!important;height:6px!important;background:#eef1ed!important;border-radius:99px!important;overflow:hidden!important}
        .juba-reference-v3 .juba-reference-achievement-strip-progress span{display:block!important;height:100%!important;background:#ffb900!important}

        .juba-reference-v3 .juba-reference-course{padding:20px!important}
        .juba-reference-v3 .juba-reference-card-header{display:flex!important;align-items:flex-start!important;justify-content:space-between!important;gap:16px!important}
        .juba-reference-v3 .juba-reference-card-header h2{margin:3px 0!important;color:#555!important;font-size:17px!important}
        .juba-reference-v3 .juba-reference-card-header p{margin:0!important;color:#999!important;font-size:10px!important}
        .juba-reference-v3 .juba-reference-outline-button,.juba-reference-v3 .juba-reference-green-button{display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:7px!important;border:1px solid #58cc02!important;border-radius:7px!important;background:#58cc02!important;color:#fff!important;padding:8px 12px!important;font-size:10px!important;font-weight:800!important;box-shadow:0 2px 0 #46a302!important}
        .juba-reference-v3 .juba-reference-progress-row{display:flex!important;align-items:center!important;gap:10px!important;margin-top:13px!important}
        .juba-reference-v3 .juba-reference-progress-track{height:7px!important;flex:1!important;background:#eef1ed!important;border-radius:99px!important;overflow:hidden!important}
        .juba-reference-v3 .juba-reference-progress-track span{display:block!important;height:100%!important;background:#ffb900!important;border-radius:99px!important}
        .juba-reference-v3 .juba-reference-progress-row>strong{font-size:10px!important;color:#58a91b!important}
        .juba-reference-v3 .juba-reference-progress-meta span{border:1px solid #edf0ea!important;border-radius:7px!important}
        .juba-reference-v3 .juba-reference-lessons{margin-top:14px!important}
        .juba-reference-v3 .juba-reference-lesson{display:grid!important;grid-template-columns:40px minmax(0,1fr) auto!important;gap:10px!important;align-items:center!important;min-height:58px!important;border-bottom:1px solid #f0f0f0!important;padding:8px 0!important;background:#fff!important}
        .juba-reference-v3 .juba-reference-path-rail{display:flex!important;justify-content:center!important}
        .juba-reference-v3 .juba-reference-path-node{width:27px!important;height:27px!important;border-radius:50%!important;border:2px solid #e2e6e1!important;background:#fff!important;color:#aaa!important;display:grid!important;place-items:center!important;font-size:9px!important;font-weight:900!important}
        .juba-reference-v3 .juba-reference-path-node.done{border-color:#58cc02!important;color:#58cc02!important}
        .juba-reference-v3 .juba-reference-path-node.current{border-color:#58cc02!important;background:#58cc02!important;color:#fff!important}
        .juba-reference-v3 .juba-reference-lesson-copy strong{color:#555!important;font-size:11px!important}
        .juba-reference-v3 .juba-reference-lesson-copy>span{display:block!important;color:#aaa!important;font-size:9px!important;margin-top:2px!important}
        .juba-reference-v3 .juba-reference-completed{display:inline-flex!important;align-items:center!important;gap:5px!important;color:#58a91b!important;font-size:9px!important;font-weight:800!important}
        .juba-reference-v3 .juba-reference-locked{color:#bbb!important}
        .juba-reference-v3 .juba-reference-empty{display:flex!important;align-items:center!important;gap:12px!important;padding:22px 0!important;color:#999!important}

        .juba-reference-v3 .juba-reference-v3-rail{display:flex!important;flex-direction:column!important;gap:14px!important;align-self:start!important}
        .juba-reference-v3 .juba-reference-v3-rail>.juba-reference-v3-card{padding:16px!important}
        .juba-reference-v3 .juba-reference-profile-card{padding:0!important;overflow:hidden!important}
        .juba-reference-v3 .juba-reference-profile-hero{display:flex!important;flex-direction:column!important;align-items:center!important;padding:18px 14px 13px!important;text-align:center!important}
        .juba-reference-v3 .juba-reference-profile-photo{width:104px!important;height:104px!important;border-radius:50%!important;overflow:hidden!important;border:4px solid #fff!important;box-shadow:0 0 0 1px #e5e9e3!important;background:#f4f7f3!important;display:grid!important;place-items:center!important;color:#999!important}
        .juba-reference-v3 .juba-reference-profile-photo img{width:100%!important;height:100%!important;object-fit:cover!important}
        .juba-reference-v3 .juba-reference-profile-hero>strong{margin-top:9px!important;color:#555!important;font-size:15px!important}
        .juba-reference-v3 .juba-reference-profile-hero>span{margin-top:3px!important;color:#999!important;font-size:9px!important}
        .juba-reference-v3 .juba-reference-profile-metrics{display:grid!important;grid-template-columns:repeat(3,1fr)!important;border-top:1px solid #edf0ea!important}
        .juba-reference-v3 .juba-reference-profile-metrics span{display:flex!important;flex-direction:column!important;align-items:center!important;gap:2px!important;padding:10px 3px!important;border-right:1px solid #edf0ea!important}
        .juba-reference-v3 .juba-reference-profile-metrics span:last-child{border-right:0!important}
        .juba-reference-v3 .juba-reference-profile-metrics b{color:#58a91b!important;font-size:14px!important}
        .juba-reference-v3 .juba-reference-profile-metrics small{color:#999!important;font-size:8px!important}
        .juba-reference-v3 .juba-reference-goal-card{border-top:3px solid #ffb900!important}
        .juba-reference-v3 .juba-reference-xp-card,.juba-reference-v3 .juba-reference-achievement-card,.juba-reference-v3 .juba-reference-tools-card,.juba-reference-v3 .juba-reference-friends-card{border-top:3px solid #e5eee0!important}
        .juba-reference-v3 .juba-reference-goal-ring{width:92px!important;height:92px!important;margin:13px auto!important;border-radius:50%!important;position:relative!important;display:grid!important;place-items:center!important}
        .juba-reference-v3 .juba-reference-goal-ring:after{content:""!important;position:absolute!important;inset:9px!important;border-radius:50%!important;background:#fff!important}
        .juba-reference-v3 .juba-reference-goal-ring strong,.juba-reference-v3 .juba-reference-goal-ring span{position:relative!important;z-index:1!important}
        .juba-reference-v3 .juba-reference-goal-ring strong{font-size:24px!important;color:#555!important}
        .juba-reference-v3 .juba-reference-goal-ring span{font-size:9px!important;color:#999!important}
        .juba-reference-v3 .juba-reference-goal-copy{display:flex!important;justify-content:center!important;gap:8px!important;align-items:baseline!important}
        .juba-reference-v3 .juba-reference-goal-copy b{color:#58a91b!important;font-size:15px!important}
        .juba-reference-v3 .juba-reference-goal-copy span{color:#999!important;font-size:9px!important}
        .juba-reference-v3 .juba-reference-xp-list{display:grid!important;gap:9px!important;margin-top:12px!important}
        .juba-reference-v3 .juba-reference-xp-list div{display:flex!important;justify-content:space-between!important;color:#999!important;font-size:10px!important}
        .juba-reference-v3 .juba-reference-xp-list b{color:#555!important}
        .juba-reference-v3 .juba-reference-achievement-icon{width:52px!important;height:52px!important;margin:12px 0 9px!important;border-radius:12px!important;background:#eef9df!important;color:#58a91b!important;display:grid!important;place-items:center!important}
        .juba-reference-v3 .juba-reference-achievement-card>strong{display:block!important;color:#555!important;font-size:12px!important}
        .juba-reference-v3 .juba-reference-achievement-card>span{display:block!important;color:#999!important;font-size:9px!important;margin:3px 0 9px!important}
        .juba-reference-v3 .juba-reference-tools-card a{display:flex!important;align-items:center!important;gap:9px!important;padding:9px 0!important;border-top:1px solid #f0f0f0!important;color:#777!important;font-size:10px!important}
        .juba-reference-v3 .juba-reference-tools-card a:first-of-type{margin-top:9px!important}
        .juba-reference-v3 .juba-reference-tools-card a svg:last-child{margin-inline-start:auto!important}
        .juba-reference-v3 .juba-reference-mini-link{color:#888!important;font-size:9px!important;font-weight:800!important;text-transform:uppercase!important}
        .juba-reference-v3 .juba-reference-friends-list{margin-top:8px!important}
        .juba-reference-v3 .juba-reference-friend-row{display:flex!important;align-items:center!important;gap:9px!important;padding:8px 0!important;border-top:1px solid #f0f0f0!important}
        .juba-reference-v3 .juba-reference-friend-avatar{width:34px!important;height:34px!important;flex:none!important;border-radius:50%!important;overflow:hidden!important;background:#f1f3f0!important;display:grid!important;place-items:center!important;color:#888!important;font-size:10px!important;font-weight:800!important}
        .juba-reference-v3 .juba-reference-friend-copy{min-width:0!important;display:flex!important;flex-direction:column!important;gap:2px!important}
        .juba-reference-v3 .juba-reference-friend-copy strong{overflow:hidden!important;text-overflow:ellipsis!important;white-space:nowrap!important;color:#555!important;font-size:10px!important}
        .juba-reference-v3 .juba-reference-friend-copy small{color:#aaa!important;font-size:8px!important}
        .juba-reference-v3 .juba-reference-friend-arrow{margin-inline-start:auto!important;color:#aaa!important;font-size:18px!important}
        .juba-reference-v3 .juba-reference-friends-empty{display:block!important;padding:12px 0!important;color:#999!important;font-size:9px!important}
        .juba-reference-v3 .juba-reference-premium{border:1px solid #dcebd2!important;background:#f6fff1!important;border-radius:12px!important;padding:13px!important;display:flex!important;align-items:center!important;gap:10px!important}
        .juba-reference-v3 .juba-reference-premium-icon{width:38px!important;height:38px!important;border-radius:9px!important;background:#58cc02!important;color:#fff!important;display:grid!important;place-items:center!important;flex:none!important}
        .juba-reference-v3 .juba-reference-premium>div:nth-child(2){display:flex!important;flex-direction:column!important;gap:2px!important;min-width:0!important}
        .juba-reference-v3 .juba-reference-premium strong{color:#4d6e43!important;font-size:10px!important}
        .juba-reference-v3 .juba-reference-premium span{color:#7f9278!important;font-size:8px!important}
        .juba-reference-v3 .juba-reference-premium button{margin-inline-start:auto!important;flex:none!important}
        @media (max-width:1180px){
          .juba-reference-shell .juba-duo-sidebar{width:188px!important}
          .juba-reference-v3{padding-inline:14px!important}
          .juba-reference-v3 .juba-reference-v3-grid{grid-template-columns:minmax(0,1fr) 250px!important;gap:16px!important}
          .juba-reference-v3 .juba-reference-reference-nav{gap:18px!important}
        }
        @media (max-width:900px){
          .juba-reference-shell .juba-duo-sidebar{display:none!important}
          .juba-reference-shell .juba-duo-main{width:100%!important}
          .juba-reference-shell .juba-duo-mobile-bar{display:block!important}
          .juba-reference-v3{padding:58px 12px 20px!important}
          .juba-reference-v3 .juba-reference-topbar{height:auto!important;min-height:58px!important;align-items:flex-start!important}
          .juba-reference-v3 .juba-reference-topbar-actions{display:none!important}
          .juba-reference-v3 .juba-reference-reference-nav{gap:15px!important;overflow-x:auto!important}
          .juba-reference-v3 .juba-reference-reference-nav a{white-space:nowrap!important;padding:14px 0!important}
          .juba-reference-v3 .juba-reference-v3-grid{grid-template-columns:1fr!important}
          .juba-reference-v3 .juba-reference-v3-rail{display:grid!important;grid-template-columns:1fr 1fr!important}
          .juba-reference-v3 .juba-reference-v3-welcome{padding-left:96px!important}
        }
        @media (max-width:620px){
          .juba-reference-v3 .juba-reference-welcome-copy h2{font-size:23px!important}
          .juba-reference-v3 .juba-reference-v3-welcome{min-height:125px!important}
          .juba-reference-v3 .juba-reference-v3-welcome:before{width:66px!important;height:66px!important;left:10px!important}
          .juba-reference-v3 .juba-reference-v3-level{min-width:68px!important;width:68px!important;height:68px!important}
          .juba-reference-v3 .juba-reference-v3-level span{font-size:13px!important}
          .juba-reference-v3 .juba-reference-reference-insights,.juba-reference-v3 .juba-reference-reference-stats,.juba-reference-v3 .juba-reference-v3-rail{grid-template-columns:1fr!important}
          .juba-reference-v3 .juba-reference-lesson{grid-template-columns:32px minmax(0,1fr)!important}
          .juba-reference-v3 .juba-reference-lesson-action{grid-column:2!important;justify-self:start!important}
          .juba-reference-v3 .juba-reference-achievement-strip-progress{width:70px!important}
        }
      `}</style>
      <OnboardingTour />
      <WhatsNew />
      <div className="juba-reference-dashboard juba-reference-v3" data-dashboard-version="reference-3">
        <header className="juba-reference-topbar">
          <div className="juba-reference-topbar-title">
            <span className="juba-reference-dot" aria-hidden="true">JL</span>
            <nav className="juba-reference-reference-nav" aria-label={tNav('navigation')}>
              <Link href="/dashboard" className="is-active">{tNav('home')}</Link>
              <Link href="/plan">{tNav('myPlan')}</Link>
              <Link href="/courses">{tNav('courses')}</Link>
            </nav>
          </div>
          <div className="juba-reference-topbar-actions">
            <span className="juba-reference-course-selector">
              <span>{tNav('switchLanguage')}</span>
              <strong>{activeLanguage ? tTarget(activeLanguage.code) : t('today')}</strong>
            </span>
            <button type="button" className="juba-reference-icon-button" onClick={refreshDashboardData} disabled={refreshing} aria-label={tError('retry')} title={tError('retry')}>
              <RefreshCw size={15} className={refreshing ? 'animate-spin' : ''} />
            </button>
          </div>
        </header>


        {loadError && (
          <div className="juba-reference-alert" role="alert">
            <span>{tError('body')}</span>
            <button type="button" onClick={() => { setLoadError(false); setLoading(true); loadData() }}>{tError('retry')}</button>
          </div>
        )}

        <section className="juba-reference-v3-grid">
          <main className="juba-reference-v3-main">
            <section className="juba-reference-v3-welcome">
              <div className="juba-reference-welcome-copy">
                <span className="juba-reference-section-label">JUBA LISAN</span>
                <h2>Welcome back, {user?.displayName || user?.username || ''}!</h2>
                <p>{completedLessonCount}/{Math.max(1, todayLessons.length)} {t('today')}</p>
                <div className="juba-reference-welcome-meta">
                  <span>{Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100))}% {t('todayGoal')}</span>
                  <i aria-hidden="true" />
                  <span>{cefrLevel || 'A1'}</span>
                  <i aria-hidden="true" />
                  <span>{currentDayDisplay}/{totalDays || 0}</span>
                </div>
              </div>
              <div className="juba-reference-v3-level" style={{'--level-progress': planCompletion} as React.CSSProperties} aria-label="${cefrLevel || 'A1'} ${planCompletion}%">
                <span>{cefrLevel || 'A1'}</span>
                <small>{planCompletion}%</small>
              </div>
            </section>

            <section className="juba-reference-reference-insights">
              <div className="juba-reference-v3-card juba-reference-insight-card">
                <div className="juba-reference-v3-card-head">
                  <div><span className="juba-reference-section-label">{t('today')}</span><h3>{t('todayGoal')}</h3></div>
                  <Flame size={18} />
                </div>
                <div className="juba-reference-insight-value"><strong>{completedLessonCount}</strong><span>/{Math.max(1, todayLessons.length)} {t('today')}</span></div>
                <div className="juba-reference-insight-track"><span style={{width: Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100)) + '%'}} /></div>
                <div className="juba-reference-insight-footer"><span>{t('xp')}</span><b>{xp}</b><span>{t('streak')}</span><b>{streak}</b></div>
              </div>
              <div className="juba-reference-v3-card juba-reference-insight-card">
                <div className="juba-reference-v3-card-head">
                  <div><span className="juba-reference-section-label">{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</span><h3>{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</h3></div>
                  <Library size={18} />
                </div>
                <div className="juba-reference-words-value"><strong>{vocabularyMastered.toLocaleString()}</strong><span>/ {vocabularyTotal.toLocaleString()}</span></div>
                <div className="juba-reference-word-bars" aria-hidden="true">
                  {[20, 34, 48, 62, 76, 90].map((height, index) => (
                    <span key={height} style={{height: Math.max(12, Math.round(height * Math.max(0.18, vocabularyProgress))) + '%'}} className={index === 5 ? 'active' : ''} />
                  ))}
                </div>
                <div className="juba-reference-insight-footer"><span>{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</span><b>{vocabularyProgressPct}%</b><span>{vocabularyLevel || 'A1'}</span></div>
              </div>
            </section>

            <section className="juba-reference-reference-stats">
              <div className="juba-reference-v3-card juba-reference-stat-card">
                <div className="juba-reference-v3-card-head">
                  <div><span className="juba-reference-section-label">{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</span><h3>{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</h3></div>
                  <Library size={18} />
                </div>
                <div className="juba-reference-stat-value">{vocabularyMastered.toLocaleString()}</div>
                <div className="juba-reference-stat-caption">{vocabularyTotal.toLocaleString()} · {vocabularyProgressPct}%</div>
                <div className="juba-reference-stat-track"><span style={{width: vocabularyProgressPct + '%'}} /></div>
              </div>
              <div className="juba-reference-v3-card juba-reference-stat-card">
                <div className="juba-reference-v3-card-head">
                  <div><span className="juba-reference-section-label">{t('xp')}</span><h3>{t('recentPerformance')}</h3></div>
                  <ChartNoAxesColumnIncreasing size={18} />
                </div>
                <div className="juba-reference-stat-breakdown">
                  <span><i />{t('today')}<b>{historyEntries[historyEntries.length - 1]?.xp_earned ?? 0} XP</b></span>
                  <span><i />{t('streak')}<b>{streak}</b></span>
                  <span><i />{t('accuracy')}<b>{accuracy}%</b></span>
                </div>
              </div>
            </section>

            <section className="juba-reference-v3-card juba-reference-achievement-strip">
              <div className="juba-reference-achievement-strip-icon"><Trophy size={20}/></div>
              <div className="juba-reference-achievement-strip-copy">
                <span className="juba-reference-section-label">{t('nextStep')}</span>
                <strong>{nextLesson?.title || t('startWithAssessment')}</strong>
                <small>{cefrLevel || 'A1'} · {planCompletion}%</small>
              </div>
              <div className="juba-reference-achievement-strip-progress"><span style={{width: planCompletion + '%'}} /></div>
            </section>
            <section className="juba-reference-v3-card juba-reference-course">
              <div className="juba-reference-card-header">
                <div>
                  <span className="juba-reference-section-label">{t('nextStep')}</span>
                  <h2>{cefrLevel || 'A1'} · {nextLesson?.title || t('startWithAssessment')}</h2>
                  <p>{nextLesson?.objectives?.[0] || t('goToMyPlan')}</p>
                </div>
                <Link href="/plan" className="juba-reference-outline-button">{t('goToMyPlan')} <ArrowUpRight size={15} /></Link>
              </div>
              <div className="juba-reference-progress-row"><div className="juba-reference-progress-track"><span style={{width: planCompletion + '%'}} /></div><strong>{planCompletion}%</strong></div>
              <div className="juba-reference-progress-meta" style={{display:'grid',gridTemplateColumns:'repeat(3,minmax(0,1fr))',gap:8,marginTop:9}}>
                <span style={{display:'flex',flexDirection:'column',gap:2,padding:'7px 9px',border:'1px solid #ececec',borderRadius:7,background:'#fff'}}><small style={{fontSize:7,fontWeight:850,color:'#aaa',textTransform:'uppercase',letterSpacing:'.05em'}}>{t('today')}</small><b style={{fontSize:10,color:'#555'}}>{currentDayDisplay}/{totalDays || 0}</b></span>
                <span style={{display:'flex',flexDirection:'column',gap:2,padding:'7px 9px',border:'1px solid #ececec',borderRadius:7,background:'#fff'}}><small style={{fontSize:7,fontWeight:850,color:'#aaa',textTransform:'uppercase',letterSpacing:'.05em'}}>{t('completedToday',{completed:completedLessonCount,total:todayLessons.length})}</small><b style={{fontSize:10,color:'#58a91b'}}>{completedLessonCount}/{todayLessons.length}</b></span>
                <span style={{display:'flex',flexDirection:'column',gap:2,padding:'7px 9px',border:'1px solid #ececec',borderRadius:7,background:'#fff'}}><small style={{fontSize:7,fontWeight:850,color:'#aaa',textTransform:'uppercase',letterSpacing:'.05em'}}>{t('nextStep')}</small><b style={{fontSize:10,color:'#555'}}>{coursePathCurrentLabel}/{todayLessons.length || 0}</b></span>
              </div>
              <div className="juba-reference-lessons juba-reference-course-path" style={{ "--course-path-progress": String(coursePathProgress) } as React.CSSProperties}>
                {todayLessons.length ? todayLessons.map((lesson,index) => {
                  const done = (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
                  const current = !done && (!nextLesson || lesson.id === nextLesson.id)
                  return (
                    <div key={lesson.id ?? lesson.title} aria-current={current ? 'step' : undefined} data-checkpoint-state={done ? 'completed' : current ? 'current' : 'upcoming'} className={`juba-reference-lesson ${current ? 'current' : ''} ${done ? 'done' : ''}`} style={current ? { background: '#fbfff8', boxShadow: 'inset 3px 0 0 #58cc02', minHeight: 72, borderBottomColor: '#e8eee4' } : done ? { background: '#fff' } : undefined}>
                      <div className="juba-reference-path-rail" aria-hidden="true">
                        <span className={`juba-reference-path-node ${done ? 'done' : current ? 'current' : ''}`} style={current ? { width: 34, height: 34, marginInlineStart: -2, boxShadow: '0 0 0 5px #f4faef', fontSize: 10 } : undefined}>
                          {done ? <Check size={14} strokeWidth={3} /> : current ? <Play size={13} fill="currentColor" /> : <span>{index + 1}</span>}
                        </span>
                      </div>
                      <div className="juba-reference-lesson-copy">
                        <div style={{display:'flex',alignItems:'center',gap:7,minWidth:0}}>
                          <span style={{fontSize:8,fontWeight:950,color:done ? '#58a91b' : current ? '#58a91b' : '#b2b2b2',letterSpacing:'.05em',textTransform:'uppercase',whiteSpace:'nowrap'}}>CP {String(index + 1).padStart(2,'0')}</span>
                          <strong style={{overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{lesson.title}</strong>
                        </div>
                        <span>{tPlan('lessonTypes.' + lesson.lessonType)} · {lesson.estimatedMinutes} {t('minutes')}</span>
                      </div>
                      <div className="juba-reference-lesson-action">
                        {current && lesson.id ? <div style={{display:'flex',alignItems:'center',gap:7}}><span style={{fontSize:8,fontWeight:900,color:'#58a91b',letterSpacing:'.04em',textTransform:'uppercase'}}>{t('today')}</span><Link href={'/lesson/' + lesson.id} className="juba-reference-green-button">{t('startLesson')}</Link></div> : done ? <span className="juba-reference-completed"><Check size={14} />{t('completedToday',{completed:1,total:1})}</span> : <span className="juba-reference-locked"><MoreHorizontal size={17} /></span>}
                      </div>
                    </div>
                  )
                }) : (
                  <div className="juba-reference-empty"><BookOpen size={30}/><div><strong>{t('startWithAssessment')}</strong><span>{t('goToMyPlan')}</span></div><Link href="/assessment" className="juba-reference-green-button">{tNav('assessment')}</Link></div>
                )}
              </div>
            </section>
          </main>

          <aside className="juba-reference-v3-rail">
            <section className="juba-reference-v3-card juba-reference-profile-card">
              <div className="juba-reference-profile-hero">
                <div className="juba-reference-profile-photo">
                  {user?.avatar ? <img src={user.avatar} alt="" /> : <UserRound size={28} />}
                </div>
                <strong>{user?.displayName || user?.username}</strong>
                <span>{cefrLevel || 'A1'} · {tTarget(activeLanguage?.code || 'en-US')}</span>
              </div>
              <div className="juba-reference-profile-metrics">
                <span><b>{xp}</b><small>XP</small></span>
                <span><b>{streak}</b><small>{t('streak')}</small></span>
                <span><b>{accuracy}%</b><small>{t('accuracy')}</small></span>
              </div>
            </section>

            <section className="juba-reference-v3-card juba-reference-goal-card">
              <div className="juba-reference-v3-card-head">
                <div><span className="juba-reference-section-label">{t('today')}</span><h3>{t('todayGoal')}</h3></div>
                <Flame size={19} />
              </div>
              <div className="juba-reference-goal-ring" style={{background: 'conic-gradient(#58cc02 0 ' + Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100)) + '%, #edf2e9 ' + Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100)) + '% 100%)'}}>
                <strong>{completedLessonCount}</strong><span>/{Math.max(1, todayLessons.length)}</span>
              </div>
              <div className="juba-reference-goal-copy">
                <b>{Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100))}%</b>
                <span>{t('completedToday', { completed: completedLessonCount, total: Math.max(1, todayLessons.length) })}</span>
              </div>
              <div className="juba-reference-small-progress"><span style={{width: Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100)) + '%'}} /></div>
            </section>
            <section className="juba-reference-v3-card juba-reference-xp-card">
              <div className="juba-reference-v3-card-head"><div><span className="juba-reference-section-label">{t('xp')}</span><h3>{t('recentPerformance')}</h3></div><ChartNoAxesColumnIncreasing size={18}/></div>
              <div className="juba-reference-xp-list">
                <div><span>{t('today')}</span><b>{historyEntries[historyEntries.length - 1]?.xp_earned ?? 0} XP</b></div>
                <div><span>{t('streak')}</span><b>{streak}</b></div>
                <div><span>{t('accuracy')}</span><b>{accuracy}%</b></div>
              </div>
            </section>
            <section className="juba-reference-v3-card juba-reference-achievement-card">
              <div className="juba-reference-v3-card-head"><div><span className="juba-reference-section-label">{t('nextStep')}</span><h3>{t('startWithAssessment')}</h3></div><Trophy size={19} /></div>
              <div className="juba-reference-achievement-icon"><Trophy size={29}/></div>
              <strong>{nextLesson?.title || t('startWithAssessment')}</strong>
              <span>{cefrLevel || 'A1'} · {planCompletion}%</span>
              <div className="juba-reference-small-progress"><span style={{width:planCompletion + '%'}} /></div>
            </section>

            <section className="juba-reference-v3-card juba-reference-tools-card">
              <div className="juba-reference-v3-card-head"><div><span className="juba-reference-section-label">{tNav('courses')}</span><h3>{tNav('courses')}</h3></div><LayoutDashboard size={18}/></div>
              <Link href="/reading"><BookOpen size={17}/><span>{tNav('reading')}</span><ArrowUpRight size={14}/></Link>
              <Link href="/listening"><Headphones size={17}/><span>{tNav('listening')}</span><ArrowUpRight size={14}/></Link>
              <Link href="/flashcards"><Library size={17}/><span>{tNav('flashcards')}</span><ArrowUpRight size={14}/></Link>
              <Link href="/chat"><Mic2 size={17}/><span>{tNav('tutor')}</span><ArrowUpRight size={14}/></Link>
            </section>

            <section className="juba-reference-v3-card juba-reference-friends-card">
              <div className="juba-reference-v3-card-head">
                <div><span className="juba-reference-section-label"><Users size={13} /> {tNav('friends')}</span><h3>{tNav('friends')}</h3></div>
                <Link href="/friends" className="juba-reference-mini-link">VIEW ALL</Link>
              </div>
              <div className="juba-reference-friends-list">
                {friends.length ? friends.map((friend) => (
                  <Link key={friend.id} href={'/friends/chat/' + friend.id} className="juba-reference-friend-row">
                    <span className="juba-reference-friend-avatar">
                      {friend.avatar ? (
                        <AuthAvatarImage avatar={friend.avatar} alt="" width={34} height={34} className="h-full w-full object-cover" />
                      ) : (
                        (friend.display_name || friend.username || '?')[0].toUpperCase()
                      )}
                    </span>
                    <span className="juba-reference-friend-copy">
                      <strong>{friend.display_name || friend.username}</strong>
                      <small>@{friend.username}</small>
                    </span>
                    <span className="juba-reference-friend-arrow">›</span>
                  </Link>
                )) : (
                  <Link href="/friends" className="juba-reference-friends-empty">{t('goToMyPlan')}</Link>
                )}
              </div>
            </section>

            {showPremiumBanner && (
              <section className="juba-reference-premium">
                <div className="juba-reference-premium-icon"><Sparkles size={20}/></div>
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
