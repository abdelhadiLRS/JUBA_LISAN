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
      <div className="juba-page-shell dash2" data-dashboard-version="reference-v2">
        {loadError && <div className="dash2-alert" role="alert"><span>{tError('body')}</span><button type="button" onClick={() => { setLoadError(false); setLoading(true); loadData() }}>{tError('retry')}</button></div>}
        <div className="dash2-layout">
          <main className="dash2-main">
            <section className="dash2-hero">
              <div className="dash2-hero-copy"><span className="dash2-eyebrow">JUBA LISAN · {t('today')}</span><h1>Welcome back, {user?.displayName || user?.username || ''}!</h1><p>{completedLessonCount}/{Math.max(1, todayLessons.length)} {t('today')} · {t('streak')} {streak}</p><div className="dash2-hero-tags"><span>{cefrLevel || 'A1'}</span><span>{currentDayDisplay}/{totalDays || 0}</span><span>{Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100))}% {t('todayGoal')}</span></div></div>
              <div className="dash2-level"><div className="dash2-level-ring" style={{'--progress': planCompletion} as React.CSSProperties}><strong>{cefrLevel || 'A1'}</strong><small>{planCompletion}%</small></div><span>{t('todayGoal')}</span></div>
            </section>

            <section className="dash2-performance">
              <div className="dash2-section-head"><div><span className="dash2-eyebrow">{t('recentPerformance')}</span><h2>{xp} XP</h2><p>{t('streak')} {streak} · {t('accuracy')} {accuracy}%</p></div><span className="dash2-period">{t('today')}</span></div>
              <div className="dash2-chart">
                {(progressBars.length ? progressBars : weekDays.map(day => ({day, value:0, active:false}))).map((bar,index,bars) => {
                  const max = Math.max(1, ...bars.map(item => item.value))
                  return <div className={'dash2-bar ' + (bar.active ? 'active' : '')} key={index} title={bar.day + ': ' + bar.value + ' XP'}><span style={{height: Math.max(8, Math.round((bar.value / max) * 100)) + '%'}} /><small>{bar.day}</small></div>
                })}
              </div>
              <div className="dash2-performance-meta"><span><small>{t('streak')}</small><b>{streak}</b></span><span><small>{t('accuracy')}</small><b>{accuracy}%</b></span><span><small>{t('xp')}</small><b>{chartEntries.reduce((sum, entry) => sum + entry.xp_earned, 0)}</b></span><span><small>{t('completedToday', { completed: completedLessonCount, total: Math.max(todayLessons.length, completedLessonCount) })}</small><b>{completedLessonCount}</b></span></div>
            </section>

            <section className="dash2-metrics">
              <article><div className="dash2-metric-head"><span>{t('todayGoal')}</span><Flame size={16}/></div><strong>{completedLessonCount}<small>/{Math.max(1, todayLessons.length)}</small></strong><div className="dash2-track"><span style={{width: Math.min(100, Math.round((completedLessonCount / Math.max(1, todayLessons.length)) * 100)) + '%'}} /></div><footer><span>{t('xp')} <b>{xp}</b></span><span>{t('streak')} <b>{streak}</b></span></footer></article>
              <article><div className="dash2-metric-head"><span>{t('vocabularyProgress', { level: vocabularyLevel || 'A1' })}</span><Library size={16}/></div><strong>{vocabularyMastered.toLocaleString()}<small>/{vocabularyTotal.toLocaleString()}</small></strong><div className="dash2-word-bars">{[20,34,48,62,76,90].map((height,index)=><i key={height} className={index===5?'active':''} style={{height: Math.max(12, Math.round(height * Math.max(0.18, vocabularyProgress))) + '%'}} />)}</div><footer><span>{vocabularyLevel || 'A1'}</span><b>{vocabularyProgressPct}%</b></footer></article>
            </section>

            <section className="dash2-course">
              <div className="dash2-course-head"><div><span className="dash2-eyebrow">{t('nextStep')}</span><h2>{cefrLevel || 'A1'} · {nextLesson?.title || t('startWithAssessment')}</h2><p>{nextLesson?.objectives?.[0] || t('goToMyPlan')}</p></div><Link href="/plan" className="dash2-link">{t('goToMyPlan')} <ArrowUpRight size={15}/></Link></div>
              <div className="dash2-progress"><span><b>{planCompletion}%</b> {t('nextStep')}</span><div><i style={{width: planCompletion + '%'}} /></div></div>
              <div className="dash2-progress-info"><span>{t('today')} <b>{completedLessonCount}/{Math.max(1,todayLessons.length)}</b></span><span>{t('streak')} <b>{streak}</b></span><span>{t('xp')} <b>{xp}</b></span></div>
              <div className="dash2-lessons">
                <div className="dash2-timeline-line" aria-hidden="true" />
                {todayLessons.length ? todayLessons.map((lesson,index) => {
                  const done = Boolean((lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted)
                  const current = !done && (!nextLesson || lesson.id === nextLesson.id)
                  return <div key={lesson.id ?? lesson.title} className={'dash2-lesson ' + (current ? 'current ' : '') + (done ? 'done' : '')} aria-current={current ? 'step' : undefined}>
                    <div className="dash2-node">{done ? <Check size={14}/> : current ? <Play size={12} fill="currentColor"/> : <span>{index+1}</span>}</div>
                    <div className="dash2-lesson-copy"><span>{lesson.lessonType || 'LESSON'} · {lesson.estimatedMinutes} min</span><strong>{lesson.title}</strong><small>{lesson.objectives?.[0] || ''}</small></div>
                    <div className="dash2-lesson-action">{current && lesson.id ? <Link href={'/lesson/' + lesson.id} className="dash2-start">{t('startLesson')}</Link> : done ? <span className="dash2-done"><Check size={13}/>{t('completedToday',{completed:1,total:1})}</span> : <span className="dash2-upcoming"><MoreHorizontal size={16}/></span>}</div>
                  </div>
                }) : <div className="dash2-empty"><BookOpen size={18}/><div><strong>{t('startWithAssessment')}</strong><span>{t('goToMyPlan')}</span></div><Link href="/plan" className="dash2-start">{t('goToMyPlan')}</Link></div>}
              </div>
            </section>
          </main>

          <aside className="dash2-side">
            <section className="dash2-profile"><div className="dash2-avatar"><AuthAvatarImage src={user?.avatarUrl} alt="" /><UserRound size={22}/></div><strong>{user?.displayName || user?.username || ''}</strong><span>{cefrLevel || 'A1'} · {activeLanguage ? tTarget(activeLanguage.code) : ''}</span><div className="dash2-profile-stats"><span><b>{streak}</b><small>{t('streak')}</small></span><span><b>{xp}</b><small>{t('xp')}</small></span><span><b>{completedLessonCount}</b><small>{t('today')}</small></span></div></section>
            <section className="dash2-side-card"><div className="dash2-side-title"><span>{t('todayGoal')}</span><Flame size={15}/></div><div className="dash2-goal-ring" style={{'--progress': Math.min(100, Math.round((completedLessonCount / Math.max(1,todayLessons.length))*100))} as React.CSSProperties}><strong>{Math.min(100, Math.round((completedLessonCount / Math.max(1,todayLessons.length))*100))}%</strong><small>{t('today')}</small></div><p>{completedLessonCount} / {Math.max(1,todayLessons.length)} {t('today')}</p></section>
            <section className="dash2-side-card"><div className="dash2-side-title"><span>{t('xp')}</span><Sparkles size={15}/></div><div className="dash2-xp"><strong>{xp}</strong><span>XP</span></div><div className="dash2-side-line"><span>{t('accuracy')}</span><b>{accuracy}%</b></div><div className="dash2-side-line"><span>{t('streak')}</span><b>{streak}</b></div></section>
            <section className="dash2-side-card"><div className="dash2-side-title"><span>{t('achievements')}</span><Trophy size={15}/></div><div className="dash2-badge"><Trophy size={20}/></div><strong>{nextLesson?.title || t('startWithAssessment')}</strong><span>{planCompletion}% · {cefrLevel || 'A1'}</span><div className="dash2-track"><span style={{width: planCompletion + '%'}} /></div></section>
            <section className="dash2-side-card dash2-tools"><div className="dash2-side-title"><span>{t('nextStep')}</span><LayoutDashboard size={15}/></div><Link href="/courses"><BookOpen size={15}/><span>{tNav('courses')}</span><ArrowUpRight size={13}/></Link><Link href="/vocabulary"><Library size={15}/><span>{t('vocabularyProgress',{level:vocabularyLevel || 'A1'})}</span><ArrowUpRight size={13}/></Link><Link href="/practice"><Headphones size={15}/><span>{t('recentPerformance')}</span><ArrowUpRight size={13}/></Link></section>
            <section className="dash2-side-card"><div className="dash2-side-title"><span><Users size={14}/> {t('friends')}</span><Link href="/friends">→</Link></div>{friends.length ? <div className="dash2-friends">{friends.map(friend => <Link href={'/profile/' + friend.username} key={friend.id}><span className="dash2-friend-avatar">{friend.avatar ? <img src={friend.avatar} alt="" /> : friend.display_name.slice(0,1).toUpperCase()}</span><span><b>{friend.display_name}</b><small>{friend.target_language || ''}</small></span><ArrowUpRight size={13}/></Link>)}</div> : <span className="dash2-muted">{t('friends')}</span>}</section>
            {showPremiumBanner && <section className="dash2-premium"><Sparkles size={18}/><strong>{tBilling('upgrade')}</strong><span>{freemiumTrialActive ? freemiumTrialDaysLeft + ' days' : tBilling('description')}</span>{paymentRecovery ? <button type="button" onClick={handleManageSubscription} disabled={portalLoading}>{portalLoading ? '...' : tBilling('manageSubscription')}</button> : <SubscriptionPlanButtons />}</section>}
          </aside>
        </div>

        <style>{`
          .dash2{--bg:transparent;--surface:var(--juba-card,var(--duo-card));--line:var(--juba-border,var(--duo-line));--text:var(--juba-ink,var(--duo-ink));--muted:var(--juba-muted,var(--duo-muted));--green:var(--juba-green,var(--duo-green));--green-dark:var(--juba-green-dark,var(--duo-green-dark));--soft:var(--juba-soft,var(--duo-soft));width:100%;max-width:none;margin:0;padding:0 0 52px;background:transparent;color:var(--text);font-family:inherit;min-height:100%;box-sizing:border-box}
          .dash2-alert{margin-top:14px;padding:9px 12px;border:1px solid var(--juba-border,var(--duo-line));background:var(--juba-card,var(--duo-card));border-radius:12px;color:var(--juba-muted,var(--duo-muted));display:flex;justify-content:space-between;font-size:9px}.dash2-alert button{border:0;background:none;color:var(--juba-green-dark,var(--duo-green-dark));font-weight:800}
          .dash2-layout{display:grid;grid-template-columns:minmax(0,1fr) 270px;gap:34px;padding-top:30px;align-items:start}.dash2-main{min-width:0;display:flex;flex-direction:column;gap:20px}.dash2-side{min-width:0;display:flex;flex-direction:column;gap:0;position:sticky;top:12px;border-inline-start:1px solid var(--line);padding-inline-start:18px}
          .dash2-hero{min-height:205px;padding:34px 8px 34px 4px;display:flex;align-items:center;justify-content:space-between;gap:30px;border:0;border-bottom:1px solid var(--line);border-radius:0;background:transparent;box-shadow:none}.dash2-hero-copy{min-width:0}.dash2-eyebrow{font-size:7px;text-transform:uppercase;letter-spacing:.14em;font-weight:900;color:var(--juba-muted,var(--duo-muted))}.dash2-hero h1{margin:9px 0 7px;font-size:34px;line-height:1.08;letter-spacing:-.045em;font-weight:650;color:var(--juba-ink,var(--duo-ink))}.dash2-hero p{margin:0;color:var(--juba-muted,var(--duo-muted));font-size:11px}.dash2-hero-tags{display:flex;gap:5px;margin-top:18px}.dash2-hero-tags span{padding:5px 8px;border:1px solid var(--juba-border,var(--duo-line));border-radius:12px;background:var(--juba-card,var(--duo-card));color:var(--juba-muted,var(--duo-muted));font-size:7px;font-weight:850}.dash2-hero-tags span:first-child{color:var(--juba-green-dark,var(--duo-green-dark));background:var(--soft);border-color:var(--juba-soft,var(--duo-soft))}
          .dash2-level{display:flex;flex-direction:column;align-items:center;gap:6px;flex:none}.dash2-level>span{font-size:7px;color:var(--juba-muted,var(--duo-muted))}.dash2-level-ring{--progress:0;width:104px;height:104px;border-radius:50%;display:grid;place-items:center;position:relative;background:conic-gradient(var(--green) calc(var(--progress)*1%),var(--juba-border,var(--duo-line)) 0);color:var(--juba-green-dark,var(--duo-green-dark))}.dash2-level-ring::after{content:"";position:absolute;inset:9px;background:var(--bg);border-radius:50%}.dash2-level-ring strong,.dash2-level-ring small{position:relative;z-index:1}.dash2-level-ring strong{font-size:21px}.dash2-level-ring small{position:absolute;bottom:27px;font-size:7px;color:var(--juba-muted,var(--duo-muted))}
          .dash2-performance,.dash2-course,.dash2-metrics article,.dash2-profile,.dash2-side-card,.dash2-premium{border:1px solid var(--line);background:var(--surface);border-radius:12px;box-shadow:0 1px 2px rgba(30,45,25,.018)}.dash2-performance{padding:22px 24px}.dash2-section-head,.dash2-course-head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px}.dash2-section-head h2,.dash2-course-head h2{margin:5px 0 0;font-size:16px;color:var(--juba-ink,var(--duo-ink));font-weight:700}.dash2-section-head>strong{font-size:11px;color:var(--juba-green-dark,var(--duo-green-dark));padding-top:4px}.dash2-chart{height:165px;margin-top:16px;padding:12px 2px 0;display:flex;align-items:flex-end;gap:15px;border-top:1px solid var(--juba-border,var(--duo-line));border-bottom:1px solid var(--juba-border,var(--duo-line));background:repeating-linear-gradient(to top,transparent 0,transparent 24%,var(--juba-border,var(--duo-line)) 24.5%,var(--juba-border,var(--duo-line)) 25%,transparent 25.5%)}.dash2-bar{height:100%;flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:7px}.dash2-bar>span{display:block;width:20px;max-width:100%;min-height:6px;border-radius:3px 3px 1px 1px;background:var(--duo-yellow,#f2bd28)}.dash2-bar.active>span{background:var(--green)}.dash2-bar small{font-size:7px;color:var(--juba-muted,var(--duo-muted))}.dash2-performance-meta{display:grid;grid-template-columns:repeat(4,1fr);margin-top:12px;padding-top:11px;border-top:1px solid var(--juba-border,var(--duo-line))}.dash2-performance-meta span{display:flex;flex-direction:column;gap:3px;padding:0 10px;border-inline-start:1px solid var(--juba-border,var(--duo-line))}.dash2-performance-meta span:first-child{border-inline-start:0;padding-inline-start:0}.dash2-performance-meta small{font-size:7px;color:var(--juba-muted,var(--duo-muted))}.dash2-performance-meta b{font-size:10px;color:var(--juba-ink,var(--duo-ink))}
          .dash2-metrics{display:grid;grid-template-columns:1.15fr .85fr;gap:20px}.dash2-metrics article{padding:20px 22px}.dash2-metric-head{display:flex;justify-content:space-between;color:var(--juba-muted,var(--duo-muted));font-size:8px;font-weight:850}.dash2-metric-head svg{color:var(--juba-muted,var(--duo-muted))}.dash2-metrics article>strong{display:block;margin:13px 0 9px;font-size:27px;color:var(--juba-ink,var(--duo-ink))}.dash2-metrics article>strong small{font-size:10px;color:var(--juba-muted,var(--duo-muted));margin-left:3px}.dash2-track{height:5px;background:var(--juba-border,var(--duo-line));border-radius:99px;overflow:hidden}.dash2-track>span{display:block;height:100%;background:var(--green);border-radius:inherit}.dash2-metrics footer{display:flex;justify-content:space-between;margin-top:9px;color:var(--juba-muted,var(--duo-muted));font-size:7px}.dash2-metrics footer b{color:var(--juba-green-dark,var(--duo-green-dark));margin-left:3px}.dash2-word-bars{height:34px;display:flex;align-items:flex-end;gap:4px}.dash2-word-bars i{display:block;flex:1;max-width:26px;background:var(--juba-border,var(--duo-line));border-radius:3px 3px 1px 1px}.dash2-word-bars i.active{background:var(--green)}
          .dash2-course{padding:22px 24px}.dash2-course-head{padding-bottom:16px;border-bottom:1px solid var(--juba-border,var(--duo-line))}.dash2-course-head h2{font-size:17px}.dash2-course-head p{margin:5px 0 0;color:var(--juba-muted,var(--duo-muted));font-size:8px}.dash2-link{padding:7px 10px;border:1px solid var(--juba-border,var(--duo-line));border-radius:12px;color:var(--juba-green-dark,var(--duo-green-dark));background:var(--juba-card,var(--duo-card));text-decoration:none;font-size:8px;font-weight:850}.dash2-link:hover{background:var(--soft)}.dash2-progress{display:flex;align-items:center;gap:12px;padding:14px 0 7px}.dash2-progress>span{font-size:7px;color:var(--juba-muted,var(--duo-muted));min-width:80px}.dash2-progress>span b{color:var(--juba-green-dark,var(--duo-green-dark));margin-right:3px}.dash2-progress>div{height:5px;flex:1;background:var(--juba-border,var(--duo-line));border-radius:99px;overflow:hidden}.dash2-progress>div i{display:block;height:100%;background:var(--green);border-radius:inherit}.dash2-progress-info{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:7px}.dash2-progress-info span{padding:6px 8px;background:var(--juba-soft,var(--duo-soft));color:var(--juba-muted,var(--duo-muted));font-size:7px;border-radius:12px}.dash2-progress-info b{float:right;color:var(--juba-ink,var(--duo-ink))}.dash2-lessons{border-top:1px solid var(--juba-border,var(--duo-line))}.dash2-lesson{display:grid;grid-template-columns:34px minmax(0,1fr) auto;gap:11px;align-items:center;min-height:67px;padding:9px 2px;border-bottom:1px solid var(--juba-border,var(--duo-line))}.dash2-lesson:last-child{border-bottom:0}.dash2-lesson.current{margin-inline:-8px;padding-inline:10px;background:var(--juba-soft,var(--duo-soft));border-inline-start:3px solid var(--green)}.dash2-node{width:28px;height:28px;border:1px solid var(--juba-border,var(--duo-line));border-radius:50%;display:grid;place-items:center;color:var(--juba-muted,var(--duo-muted));font-size:8px}.dash2-lesson.done .dash2-node{border-color:var(--juba-green,var(--duo-green));color:var(--juba-green-dark,var(--duo-green-dark))}.dash2-lesson.current .dash2-node{background:var(--green);border-color:var(--green);color:var(--juba-card,var(--duo-card))}.dash2-lesson-copy{min-width:0;display:flex;flex-direction:column}.dash2-lesson-copy>span{font-size:6px;color:var(--juba-muted,var(--duo-muted));text-transform:uppercase;letter-spacing:.06em}.dash2-lesson-copy strong{font-size:10px;color:var(--juba-ink,var(--duo-ink));margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.dash2-lesson-copy small{font-size:7px;color:var(--juba-muted,var(--duo-muted));margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.dash2-start{display:inline-flex;align-items:center;justify-content:center;min-height:28px;padding:0 11px;border-radius:12px;background:var(--green);color:var(--juba-card,var(--duo-card));text-decoration:none;font-size:7px;font-weight:900;box-shadow:0 2px 0 var(--green-dark)}.dash2-done,.dash2-upcoming{display:inline-flex;align-items:center;gap:4px;color:var(--juba-green-dark,var(--duo-green-dark));font-size:7px;font-weight:800}.dash2-upcoming{color:var(--juba-muted,var(--duo-muted))}.dash2-empty{display:flex;align-items:center;gap:9px;padding:20px 2px;color:var(--juba-muted,var(--duo-muted));font-size:8px}.dash2-empty div{display:flex;flex-direction:column;gap:2px;flex:1}.dash2-empty strong{color:var(--juba-ink,var(--duo-ink))}
          .dash2-lessons{position:relative;border-top:0;padding-top:4px}
          .dash2-lessons::before{content:"";position:absolute;inset-block:18px 18px;left:15px;width:1px;background:var(--juba-border,var(--duo-line))}
          .dash2-lesson{position:relative;grid-template-columns:32px minmax(0,1fr) auto;gap:14px;min-height:76px;padding:11px 0;border-bottom:0}
          .dash2-node{position:relative;z-index:1;width:30px;height:30px;border-radius:9px;background:var(--juba-card,var(--duo-card));border-color:var(--juba-border,var(--duo-line))}
          .dash2-lesson.done .dash2-node{background:var(--juba-soft,var(--duo-soft));border-color:var(--juba-green,var(--duo-green));color:var(--juba-green-dark,var(--duo-green-dark))}
          .dash2-lesson.current{margin-inline:0;padding-inline:0;background:transparent;border-inline-start:0}
          .dash2-lesson.current .dash2-node{border-radius:9px;box-shadow:0 0 0 4px var(--juba-soft,var(--duo-soft))}
          .dash2-lesson-copy strong{font-size:11px;color:var(--juba-ink,var(--duo-ink))}
          .dash2-lesson-copy>span{font-size:7px}
          .dash2-lesson-copy small{font-size:8px}
          .dash2-lesson-action{align-self:center}
          .dash2-done{padding-inline:7px;min-height:24px;border:1px solid var(--juba-border,var(--duo-line));border-radius:12px}
          .dash2-upcoming{width:26px;height:26px;justify-content:center;border:1px solid var(--juba-border,var(--duo-line));border-radius:12px}
          .dash2-start{min-height:30px;border-radius:12px;padding-inline:13px}

          .dash2-profile{padding:0 0 18px;text-align:start;border:0;border-radius:0;background:transparent;box-shadow:none}.dash2-avatar{width:42px;height:42px;margin:0 0 8px;border-radius:12px;overflow:hidden;background:var(--juba-border,var(--duo-line));color:var(--juba-muted,var(--duo-muted));display:grid;place-items:center}.dash2-avatar img{width:100%;height:100%;object-fit:cover}.dash2-profile>strong{display:block;font-size:12px;color:var(--juba-ink,var(--duo-ink))}.dash2-profile>span{display:block;margin-top:3px;font-size:7px;color:var(--juba-muted,var(--duo-muted))}.dash2-profile-stats{display:grid;grid-template-columns:repeat(3,1fr);margin-top:12px;padding-top:10px;border-top:1px solid var(--line)}.dash2-profile-stats span+span{border-inline-start:1px solid var(--juba-border,var(--duo-line))}.dash2-profile-stats span{display:flex;flex-direction:column;gap:2px}.dash2-profile-stats b{font-size:11px;color:var(--juba-ink,var(--duo-ink))}.dash2-profile-stats small{font-size:6px;color:var(--juba-muted,var(--duo-muted))}
          .dash2-side-card{padding:17px 0;border:0;border-bottom:1px solid var(--line);border-radius:0;background:transparent;box-shadow:none}.dash2-side-card:last-of-type{border-bottom:0}.dash2-side-title{display:flex;justify-content:space-between;align-items:center;color:var(--juba-muted,var(--duo-muted));font-size:8px;font-weight:850}.dash2-side-title span{display:flex;align-items:center;gap:4px}.dash2-goal-ring{--progress:0;width:68px;height:68px;margin:11px auto 8px;border-radius:50%;display:grid;place-items:center;position:relative;background:conic-gradient(var(--green) calc(var(--progress)*1%),var(--juba-border,var(--duo-line)) 0)}.dash2-goal-ring::after{content:"";position:absolute;inset:6px;background:var(--juba-card,var(--duo-card));border-radius:50%}.dash2-goal-ring strong,.dash2-goal-ring small{position:relative;z-index:1}.dash2-goal-ring strong{font-size:15px}.dash2-goal-ring small{position:absolute;bottom:15px;font-size:6px;color:var(--juba-muted,var(--duo-muted))}.dash2-side-card>p{text-align:center;margin:0;font-size:7px;color:var(--juba-muted,var(--duo-muted))}.dash2-xp{display:flex;align-items:baseline;gap:4px;margin:11px 0 8px}.dash2-xp strong{font-size:24px}.dash2-xp span{font-size:7px;color:var(--juba-muted,var(--duo-muted))}.dash2-side-line{display:flex;justify-content:space-between;padding-top:7px;margin-top:7px;border-top:1px solid var(--juba-border,var(--duo-line));font-size:7px;color:var(--juba-muted,var(--duo-muted))}.dash2-side-line b{color:var(--juba-ink,var(--duo-ink))}.dash2-badge{width:44px;height:44px;margin:11px auto 7px;border-radius:9px;background:color-mix(in_srgb,var(--duo-yellow,#f2bd28)_14%,var(--juba-card,var(--duo-card)));color:#e4a900;display:grid;place-items:center}.dash2-side-card>strong:not(.dash2-xp){display:block;text-align:center;font-size:9px;color:var(--juba-ink,var(--duo-ink))}.dash2-side-card>span{display:block;text-align:center;font-size:7px;color:var(--juba-muted,var(--duo-muted));margin-top:2px}.dash2-tools>a{min-height:32px;display:flex;align-items:center;gap:6px;padding:0 5px;color:var(--juba-muted,var(--duo-muted));text-decoration:none;border-radius:12px;font-size:8px}.dash2-tools>a:hover{background:var(--soft);color:var(--juba-green-dark,var(--duo-green-dark))}.dash2-tools>a span{flex:1}.dash2-friends{display:grid;gap:2px;margin-top:7px}.dash2-friends>a{display:flex;align-items:center;gap:6px;padding:4px;border-radius:12px;text-decoration:none}.dash2-friend-avatar{width:26px;height:26px;flex:none;border-radius:50%;overflow:hidden;background:var(--juba-border,var(--duo-line));display:grid;place-items:center;font-size:8px;color:var(--juba-muted,var(--duo-muted))}.dash2-friend-avatar img{width:100%;height:100%;object-fit:cover}.dash2-friends>a>span:nth-child(2){display:flex;flex-direction:column;gap:1px;flex:1;min-width:0}.dash2-friends b{font-size:7px;color:var(--juba-muted,var(--duo-muted));overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.dash2-friends small{font-size:6px;color:var(--juba-muted,var(--duo-muted))}.dash2-premium{padding:13px;background:color-mix(in_srgb,var(--duo-yellow,#f2bd28)_10%,var(--juba-card,var(--duo-card)));border-color:#e9e2bf;display:flex;flex-direction:column;gap:6px}.dash2-premium strong{font-size:9px;color:#67591f}.dash2-premium>span{font-size:7px;color:#9d9160;line-height:1.45}.dash2-premium button{border:0;border-radius:12px;background:#e7b000;color:var(--juba-card,var(--duo-card));padding:6px;font-size:7px;font-weight:850}
          @media (max-width:1100px){.dash2{padding-inline:0}.dash2-layout{grid-template-columns:minmax(0,1fr) 230px;gap:20px}}@media (max-width:850px){.dash2{padding:0 0 28px}.dash2-layout{grid-template-columns:1fr;padding-top:16px}.dash2-side{position:static}.dash2-hero{min-height:145px;padding:20px 4px}.dash2-hero h1{font-size:25px}.dash2-level-ring{width:78px;height:78px}.dash2-level-ring::after{inset:7px}.dash2-performance-meta{grid-template-columns:repeat(2,1fr);row-gap:9px}.dash2-performance-meta span:nth-child(3){border-inline-start:0;padding-inline-start:0}.dash2-metrics{grid-template-columns:1fr}.dash2-course-head{flex-direction:column}.dash2-link{width:100%;text-align:center}.dash2-lesson{grid-template-columns:32px minmax(0,1fr)}.dash2-lesson-action{grid-column:2}.dash2-start{margin-top:4px}.dash2-profile{order:-1}}@media (max-width:560px){.dash2{padding-inline:0}.dash2-hero{padding:17px 2px}.dash2-hero h1{font-size:21px}.dash2-level-ring{width:66px;height:66px}.dash2-level-ring strong{font-size:15px}.dash2-chart{height:145px;gap:6px}.dash2-bar>span{width:17px}.dash2-performance,.dash2-course{padding:15px}.dash2-progress-info{grid-template-columns:1fr}.dash2-lesson.current{margin-inline:-3px;padding-inline:7px}}
        `}</style>
      </div>
    </>
  )
}
