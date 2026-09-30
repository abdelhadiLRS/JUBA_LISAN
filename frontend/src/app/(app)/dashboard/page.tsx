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
    return (
    <>
      <OnboardingTour />
      <WhatsNew />
      <div className="juba-reference-dashboard" data-dashboard-version="reference-0">
        <header className="juba-reference-topbar">
          <div className="juba-reference-topbar-title">
            <span className="juba-reference-dot" aria-hidden="true">JL</span>
            <div><span className="juba-reference-overline">{activeLanguage ? tTarget(activeLanguage.code) : t('today')}</span><h1>{t('welcomeBack')}, {user?.displayName || user?.username}</h1></div>
          </div>
          <div className="juba-reference-topbar-actions">
            <button type="button" className="juba-reference-icon-button" onClick={refreshDashboardData} disabled={refreshing} aria-label={tError('retry')} title={tError('retry')}><RefreshCw size={17} className={refreshing ? 'animate-spin' : ''} /></button>
            <div className="juba-reference-profile">
              <div className="juba-reference-profile-avatar">{user?.avatar ? <img src={user.avatar} alt="" /> : <UserRound size={17} />}</div>
              <div><strong>{user?.displayName || user?.username}</strong><span>{cefrLevel || 'A1'}</span></div><ChevronDown size={15} />
            </div>
          </div>
        </header>

        {loadError && <div className="juba-reference-alert" role="alert"><span>{tError('body')}</span><button type="button" onClick={() => { setLoadError(false); setLoading(true); loadData() }}>{tError('retry')}</button></div>}

        <section className="juba-reference-stats" aria-label={tNav('dashboard')}>
          <article className="juba-reference-stat"><i className="green"><Flame size={19} /></i><div><span>{t('streak')}</span><strong>{streak}</strong><small>{t('today')}</small></div></article>
          <article className="juba-reference-stat"><i className="yellow"><Trophy size={19} /></i><div><span>{t('xp')}</span><strong>{xp}</strong><small>{t('recentPerformance')}</small></div></article>
          <article className="juba-reference-stat"><i className="blue"><ChartNoAxesColumnIncreasing size={19} /></i><div><span>{t('accuracy')}</span><strong>{accuracy}%</strong><small>{getPerformanceLabel(accuracy / 100)}</small></div></article>
          <article className="juba-reference-stat"><i className="purple"><BookOpen size={19} /></i><div><span>{t('vocabularyProgress', { level: vocabularyLevel || '—' })}</span><strong>{vocabularyProgressPct}%</strong><small>{t('vocabularyWords', { mastered: vocabularyMastered, total: vocabularyTotal })}</small></div></article>
        </section>

        <div className="juba-reference-layout">
          <main className="juba-reference-main">
            <section className="juba-reference-card juba-reference-course">
              <div className="juba-reference-card-header">
                <div><span className="juba-reference-section-label">{t('nextStep')}</span><h2>{cefrLevel || 'A1'} · {nextLesson?.title || t('startWithAssessment')}</h2><p>{nextLesson?.objectives?.[0] || t('goToMyPlan')}</p></div>
                <Link href="/plan" className="juba-reference-outline-button">{t('goToMyPlan')} <ArrowUpRight size={15} /></Link>
              </div>
              <div className="juba-reference-progress-row"><div className="juba-reference-progress-track"><span style={{ width: planCompletion + '%' }} /></div><strong>{planCompletion}%</strong></div>
              <div className="juba-reference-progress-meta"><span>{currentDayDisplay}/{totalDays || 0} {t('today')}</span><span>{pendingCount} {t('lessonReady')}</span></div>
              <div className="juba-reference-lessons">
                {todayLessons.length ? todayLessons.map((lesson,index)=>{
                  const done=(lesson.id && completedToday.includes(lesson.id))||lesson.isCompleted;
                  const current=!done&&(!nextLesson||lesson.id===nextLesson.id);
                  return <div key={lesson.id??lesson.title} className={`juba-reference-lesson ${current?'current':''} ${done?'done':''}`}>
                    <div className={`juba-reference-lesson-number ${done?'done':current?'current':''}`}>{done?<Check size={17} strokeWidth={3}/>:current?<Play size={17} fill="currentColor"/>:<span>{index+1}</span>}</div>
                    <div className="juba-reference-lesson-copy"><strong>{lesson.title}</strong><span>{tPlan('lessonTypes.'+lesson.lessonType)} · {lesson.estimatedMinutes} {t('minutes')}</span></div>
                    <div className="juba-reference-lesson-action">{current&&lesson.id?<Link href={'/lesson/'+lesson.id} className="juba-reference-green-button">{t('startLesson')}</Link>:done?<span className="juba-reference-completed"><Check size={14}/>{t('completedToday',{completed:1,total:1})}</span>:<span className="juba-reference-locked"><MoreHorizontal size={17}/></span>}</div>
                  </div>
                }):<div className="juba-reference-empty"><BookOpen size={30}/><div><strong>{t('startWithAssessment')}</strong><span>{t('goToMyPlan')}</span></div><Link href="/assessment" className="juba-reference-green-button">{tNav('assessment')}</Link></div>}
              </div>
            </section>

            <div className="juba-reference-chart-grid">
              <section className="juba-reference-card juba-reference-chart-card">
                <div className="juba-reference-chart-header"><div><span className="juba-reference-section-label">{t('xp')}</span><h3>{t('recentPerformance')}</h3></div><b>{xp}</b></div>
                <div className="juba-reference-bars">{(progressBars.length?progressBars:weekDays.map(day=>({day,value:0,active:false}))).map((bar,index)=>{const max=Math.max(1,...progressBars.map(x=>x.value),xp||0);return <div key={index} className={`juba-reference-bar-column ${bar.active?'active':''}`}><span style={{height:Math.max(8,Math.round((bar.value/max)*100))+'%'}}/><small>{bar.day}</small></div>})}</div>
              </section>
              <section className="juba-reference-card juba-reference-chart-card">
                <div className="juba-reference-chart-header"><div><span className="juba-reference-section-label">{t('accuracy')}</span><h3>{t('recentPerformance')}</h3></div><b>{chartAverage}%</b></div>
                <div className="juba-reference-bars performance">{(performanceValues.length?performanceValues:weekDays.map(()=>0)).map((value,index)=><div key={index} className="juba-reference-bar-column"><span style={{height:Math.max(8,value)+'%'}}/><small>{chartEntries[index]?new Date(chartEntries[index].date+'T00:00:00').toLocaleDateString(undefined,{weekday:'short'}):weekDays[index]}</small></div>)}</div>
              </section>
            </div>
          </main>

          <aside className="juba-reference-aside">
            <section className="juba-reference-card juba-reference-goal-card">
              <div className="juba-reference-aside-title"><h3>{t('streak')}</h3><Flame size={18}/></div>
              <div className="juba-reference-goal-ring"><div><strong>{streak}</strong><span>{t('today')}</span></div></div>
              <p>{t('completedToday',{completed:completedLessonCount,total:todayLessons.length||1})}</p>
            </section>
            <section className="juba-reference-card juba-reference-achievement-card">
              <div className="juba-reference-aside-title"><h3>{t('nextStep')}</h3><Trophy size={18}/></div>
              <div className="juba-reference-achievement-icon"><Trophy size={30}/></div>
              <strong>{nextLesson?.title||t('startWithAssessment')}</strong><span>{cefrLevel||'A1'} · {planCompletion}%</span>
              <div className="juba-reference-small-progress"><span style={{width:planCompletion+'%'}}/></div>
            </section>
            <section className="juba-reference-card juba-reference-tools-card">
              <div className="juba-reference-aside-title"><h3>{tNav('courses')}</h3><LayoutDashboard size={18}/></div>
              <Link href="/reading"><BookOpen size={17}/><span>{tNav('reading')}</span><ArrowUpRight size={14}/></Link>
              <Link href="/listening"><Headphones size={17}/><span>{tNav('listening')}</span><ArrowUpRight size={14}/></Link>
              <Link href="/flashcards"><Library size={17}/><span>{tNav('flashcards')}</span><ArrowUpRight size={14}/></Link>
              <Link href="/chat"><Mic2 size={17}/><span>{tNav('tutor')}</span><ArrowUpRight size={14}/></Link>
            </section>
            {showPremiumBanner&&<section className="juba-reference-premium"><div className="juba-reference-premium-icon"><Sparkles size={20}/></div><div><strong>{freemiumTrialActive?t('freemiumTrialTitle',{days:freemiumTrialDaysLeft}):t(paymentRecovery?'premiumBannerPastDueTitle':'premiumBannerTitle')}</strong><span>{freemiumTrialActive?t('freemiumTrialDesc',{days:freemiumTrialDaysLeft}):paymentRecovery?t('premiumBannerPastDueDesc'):t(trialEligible?'premiumBannerDesc':'premiumBannerDescTrialUsed')}</span></div>{paymentRecovery?<button onClick={handleManageSubscription} disabled={portalLoading}>{portalLoading?'…':tBilling('updatePayment')}</button>:!freemiumTrialActive?<SubscriptionPlanButtons/>:null}</section>}
          </aside>
        </div>
      </div>
    </>
  )
}
