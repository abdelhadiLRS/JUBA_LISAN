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

  // Lesson and assessment routes publish a progress event after a successful
  // completion. Revalidate immediately so XP, streak, accuracy, plan state,
  // vocabulary and the activity chart stay in sync without navigation/reload.
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
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-[#e9e8fa]">
        <p className="font-sans text-sm text-[#55566a]">{tError('body')}</p>
        <button
          type="button"
          onClick={() => {
            setLoadError(false)
            setLoading(true)
            loadData()
          }}
          className="font-sans text-xs font-bold uppercase tracking-widest text-[#373fb8] underline"
        >
          {tError('retry')}
        </button>
      </div>
    )
  }

  const skillEntries = Object.entries(skills)
    .map(([skill, value]) => ({ skill, value: value as number }))
    .sort((a, b) => a.value - b.value)

  const completedLessonCount = todayLessons.filter(
    (lesson) =>
      (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
  ).length

  const nextLesson = todayLessons.find(
    (lesson) =>
      lesson.id && !completedToday.includes(lesson.id) && !lesson.isCompleted
  )

  const planPositionComplete =
    completion?.state === 'ready' || completion?.state === 'taken'

  const planCompletion =
    hasPlan && totalDays > 0
      ? planPositionComplete
        ? 100
        : Math.min(100, Math.round((progressDay / totalDays) * 100))
      : 0

  const currentDayDisplay = planPositionComplete
    ? totalDays
    : Math.min(progressDay + 1, totalDays)

  const vocabularyProgressPct = Math.round(vocabularyProgress * 100)
  const paymentRecovery = needsPaymentRecovery(user)
  const showPremiumBanner = stripeEnabled && !isSubscribed(user, stripeEnabled)

  const chartEntries = historyEntries.slice(-7)
  const performanceValues = chartEntries.map((entry) =>
    entry.exercises_total > 0
      ? Math.round((entry.exercises_correct / entry.exercises_total) * 100)
      : 0
  )
  const chartMax = Math.max(100, ...performanceValues)
  const chartAverage = chartEntries.length
    ? Math.round(
        chartEntries.reduce((sum, entry) => sum + (
          entry.exercises_total > 0
            ? (entry.exercises_correct / entry.exercises_total) * 100
            : 0
        ), 0) / chartEntries.length
      )
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

      <main className="min-h-screen bg-[#dfe0f7] p-2 text-[#202127] sm:p-4 lg:p-6">
        <div className="mx-auto max-w-[1640px] overflow-hidden rounded-[30px] bg-[#f4f4f2] shadow-[0_30px_90px_rgba(43,45,90,.18)]">
          <header className="flex min-h-[72px] items-center justify-between gap-4 bg-[#070709] px-4 py-3 text-white sm:px-7">
            <Link href="/dashboard" className="flex shrink-0 items-center gap-3">
              <span className="grid size-10 place-items-center rounded-[12px] bg-[#373fb8] text-white shadow-[0_8px_25px_rgba(55,63,184,.35)]">
                <LayoutDashboard className="size-5" />
              </span>
              <span className="text-sm font-black tracking-tight sm:text-base">JUBA LISAN</span>
            </Link>

            <nav className="hidden items-center gap-1 rounded-full bg-white/[0.06] p-1 lg:flex">
              {[
                { href: '/dashboard', label: t('today'), icon: LayoutDashboard, active: true },
                { href: '/courses', label: tNav('courses'), icon: BookOpen },
                { href: '/plan', label: t('goToMyPlan'), icon: ListChecks },
                { href: '/progress', label: t('recentPerformance'), icon: Trophy },
                { href: '/reading', label: tNav('reading'), icon: Library },
              ].map(({ href, label, icon: Icon, active }) => (
                <Link
                  key={href}
                  href={href}
                  className={
                    active
                      ? 'inline-flex items-center gap-2 rounded-full bg-white px-4 py-2 text-[11px] font-black text-[#070709]'
                      : 'inline-flex items-center gap-2 rounded-full px-3 py-2 text-[11px] font-bold text-white/55 transition hover:bg-white/10 hover:text-white'
                  }
                >
                  <Icon className="size-3.5" />
                  {label}
                </Link>
              ))}
            </nav>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={refreshDashboardData}
                disabled={refreshing}
                title={t('refresh')}
                aria-label={t('refresh')}
                className="grid size-9 place-items-center rounded-full bg-white/[0.06] text-white/65 transition hover:bg-white/10 hover:text-white disabled:opacity-50"
              >
                <RefreshCw className={`size-4 ${refreshing ? 'animate-spin' : ''}`} />
              </button>
              <div className="hidden text-right sm:block">
                <p className="text-xs font-black">
                  {t('welcomeBack')}, {user?.displayName || user?.username}
                </p>
                <p className="mt-0.5 text-[10px] text-white/45">
                  {streak} {t('streak')} · {xp} XP
                </p>
              </div>
              <span className="grid size-10 place-items-center rounded-full bg-[#9a9ff3] text-[#070709] ring-2 ring-white/10">
                <UserRound className="size-5" />
              </span>
            </div>
          </header>

          <div className="grid gap-4 p-3 sm:p-5 lg:grid-cols-[1.05fr_1.42fr_1fr] lg:gap-5 lg:p-6">
            <section className="space-y-4">
              <div className="relative min-h-[255px] overflow-hidden rounded-[26px] bg-[#9a9ff3] p-5 text-white">
                <div className="absolute -right-12 -top-16 size-44 rounded-full border-[26px] border-white/10" />
                <div className="absolute -bottom-24 -left-16 size-56 rounded-full bg-[#858be9]" />
                <div className="absolute right-8 top-12 grid size-16 rotate-12 place-items-center rounded-[18px] bg-[#373fb8]/30">
                  <Trophy className="size-8 text-white/85" />
                </div>
                <div className="relative z-10">
                  <span className="inline-flex rounded-full bg-[#070709]/85 px-3 py-1.5 text-[9px] font-black uppercase tracking-[.14em]">
                    {activeLanguage ? tTarget(activeLanguage.code) : 'JUBA LISAN'}
                  </span>
                  <h1 className="mt-6 max-w-[290px] text-[32px] font-black leading-[.98] tracking-[-.04em]">
                    {t('welcomeBack')}, {user?.displayName || user?.username}
                  </h1>
                  <p className="mt-4 max-w-[265px] text-xs font-medium leading-relaxed text-white/75">
                    {cefrLevel ? cefrLevel + ' · ' : ''}
                    {t('nextStep')}
                  </p>
                  <Link
                    href={nextLesson?.id ? '/lesson/' + nextLesson.id : '/assessment'}
                    aria-label={t('startLesson')}
                    className="mt-6 inline-flex size-11 items-center justify-center rounded-full bg-[#070709] shadow-lg transition hover:scale-105"
                  >
                    <Play className="ml-0.5 size-4 fill-white" />
                  </Link>
                </div>
                <div className="absolute bottom-4 right-6 text-5xl font-black text-white/15">✦</div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-[21px] border border-[#ffad68]/70 bg-white p-4">
                  <div className="flex items-center justify-between gap-2">
                    <span className="grid size-8 place-items-center rounded-full bg-[#ffad68]/20">
                      <ListChecks className="size-4 text-[#f07b28]" />
                    </span>
                    <span className="text-[9px] font-bold uppercase tracking-widest text-black/35">
                      {t('lessonsCompleted')}
                    </span>
                  </div>
                  <p className="mt-5 text-[32px] font-black tracking-tight">{totalLessons}</p>
                </div>
                <div className="rounded-[21px] border border-[#9a9ff3] bg-[#e9e9ff] p-4">
                  <div className="flex items-center justify-between gap-2">
                    <span className="grid size-8 place-items-center rounded-full bg-white/70">
                      <Flame className="size-4 text-[#373fb8]" />
                    </span>
                    <span className="text-[9px] font-bold uppercase tracking-widest text-black/35">
                      {t('streak')}
                    </span>
                  </div>
                  <p className="mt-5 text-[32px] font-black tracking-tight">{streak}</p>
                </div>
              </div>

              <div className="rounded-[25px] bg-[#070709] p-5 text-white">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <span className="text-[9px] font-black uppercase tracking-[.16em] text-[#ff9a5d]">
                      {t('recentPerformance')}
                    </span>
                    <h2 className="mt-2 text-xl font-black tracking-tight">
                      {skillEntries.length
                        ? getPerformanceLabel(skillEntries[skillEntries.length - 1].value)
                        : t('noSkills')}
                    </h2>
                  </div>
                  <Link
                    href="/progress"
                    className="grid size-9 place-items-center rounded-full bg-white/10 transition hover:bg-white/15"
                    aria-label={t('recentPerformance')}
                  >
                    <ArrowUpRight className="size-4" />
                  </Link>
                </div>
                <div className="mt-4 flex items-center justify-between gap-2">
                  <div className="flex items-center gap-1 rounded-full bg-white/[0.06] p-1">
                    {(['week', 'month', 'all'] as const).map((range) => (
                      <button key={range} type="button" onClick={() => changeHistoryRange(range)} className={historyRange === range ? 'rounded-full bg-white px-2.5 py-1.5 text-[8px] font-black text-[#070709]' : 'rounded-full px-2.5 py-1.5 text-[8px] font-black text-white/45 hover:text-white'}>
                        {range === 'week' ? '7D' : range === 'month' ? '30D' : 'ALL'}
                      </button>
                    ))}
                  </div>
                  <span className="text-[9px] font-bold text-white/40">{historyLoading ? '…' : chartEntries.length + ' days'} · {chartAverage}%</span>
                </div>
                <div className="mt-3 grid grid-cols-7 items-end gap-2">
                  {performanceValues.length ? performanceValues.map((value, index) => (
                    <div key={index} className="flex flex-col items-center gap-1.5">
                      <div className="flex h-20 w-full items-end rounded-[10px] bg-white/[0.05] p-1">
                        <div
                          className="w-full rounded-[7px] bg-[#5862e2]"
                          style={{ height: Math.max(4, Math.round((value / chartMax) * 100)) + '%' }}
                        />
                      </div>
                      <span className="text-[8px] font-bold text-white/35">{value}%</span>
                    </div>
                  )) : Array.from({ length: 7 }).map((_, index) => (
                    <div key={index} className="flex flex-col items-center gap-1.5">
                      <div className="flex h-20 w-full items-end rounded-[10px] bg-white/[0.05] p-1" />
                      <span className="text-[8px] font-bold text-white/20">—</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="relative overflow-hidden rounded-[25px] bg-[#373fb8] p-5 text-white">
                <div className="absolute -right-8 -top-10 size-32 rounded-full border-[18px] border-white/10" />
                <div className="relative z-10 flex items-center justify-between gap-4">
                  <div>
                    <p className="text-[9px] font-black uppercase tracking-[.16em] text-white/55">
                      {tNav('resources')}
                    </p>
                    <p className="mt-2 max-w-[180px] text-sm font-black leading-tight">
                      {t('recentPerformanceDescription')}
                    </p>
                  </div>
                  <Link href="/flashcards" className="grid size-10 shrink-0 place-items-center rounded-full bg-white text-[#373fb8]">
                    <ArrowUpRight className="size-4" />
                  </Link>
                </div>
              </div>
            </section>

            <section className="space-y-4">
              <div className="rounded-[27px] bg-white p-5 shadow-sm ring-1 ring-black/[0.04] sm:p-6">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-[10px] font-black uppercase tracking-[.15em] text-black/35">{t('planProgress')}</p>
                    <h2 className="mt-1 text-[34px] font-black tracking-[-.04em]">{planCompletion}%</h2>
                  </div>
                  <button type="button" className="inline-flex items-center gap-2 rounded-full bg-[#f3f2f3] px-3 py-2 text-[10px] font-black">
                    {activeLanguage ? tTarget(activeLanguage.code) : t('today')}
                    <ChevronDown className="size-3" />
                  </button>
                </div>

                <div className="mt-4 overflow-hidden rounded-[25px] bg-[#f95d22] p-5">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="text-[38px] font-black leading-none tracking-[-.05em]">{completedLessonCount}</p>
                      <p className="mt-2 text-[10px] font-black text-[#713619]">
                        {t('completedToday', { completed: completedLessonCount, total: todayLessons.length || 0 })}
                      </p>
                    </div>
                    <div className="rounded-full bg-[#070709] px-3 py-1.5 text-[9px] font-black text-white">
                      {totalDays > 0 ? currentDayDisplay + '/' + totalDays : t('today')}
                    </div>
                  </div>

                  <div className="mt-6 grid grid-cols-5 gap-2">
                    {progressBars.map(({ day, value, active }) => (
                      <div key={day} className="text-center">
                        <div className="relative flex h-[138px] items-end justify-center overflow-hidden rounded-[17px] bg-white/20 p-2">
                          <div
                            className="relative w-full max-w-[48px] rounded-t-[18px] bg-[#442e3b]/70"
                            style={{ height: value + '%' }}
                          >
                            <span className="absolute -top-5 left-1/2 -translate-x-1/2 text-[9px] font-black text-[#442e3b]">{value}</span>
                            {active && (
                              <span className="absolute left-1/2 top-2 grid size-5 -translate-x-1/2 place-items-center rounded-full bg-white/90">
                                <Check className="size-3 text-[#f95d22]" />
                              </span>
                            )}
                          </div>
                        </div>
                        <span className="mt-2 block text-[9px] font-black text-[#713619]">{day}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mt-4 flex items-center justify-between rounded-[17px] bg-[#f3f2f3] px-4 py-3">
                  <div className="flex items-center gap-3">
                    <span className="grid size-9 place-items-center rounded-full bg-[#ffcf58]">
                      <Trophy className="size-4" />
                    </span>
                    <div>
                      <p className="text-[10px] font-black">{t('recentPerformance')}</p>
                      <p className="mt-0.5 text-[9px] text-black/40">{t('accuracy')}: {accuracy}%</p>
                    </div>
                  </div>
                  <span className="rounded-full bg-white px-3 py-1.5 text-[10px] font-black">{xp} XP</span>
                </div>
              </div>

              <div className="rounded-[27px] bg-white p-5 shadow-sm ring-1 ring-black/[0.04] sm:p-6">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-[10px] font-black uppercase tracking-[.15em] text-black/35">{t('today')}</p>
                    <h2 className="mt-1 text-[24px] font-black tracking-tight">{t('lessonReady')}</h2>
                  </div>
                  <Link href="/plan" className="grid size-9 place-items-center rounded-full bg-[#f3f2f3]" aria-label={t('goToMyPlan')}>
                    <ArrowUpRight className="size-4" />
                  </Link>
                </div>

                <div className="mt-4 space-y-2">
                  {todayLessons.slice(0, 5).map((lesson, index) => {
                    const done =
                      (Boolean(lesson.id) && completedToday.includes(lesson.id as number)) ||
                      lesson.isCompleted
                    const isNext = nextLesson?.id === lesson.id

                    return (
                      <div
                        key={lesson.id ?? index}
                        className={
                          isNext
                            ? 'flex items-center gap-3 rounded-[17px] bg-[#f3f2f3] p-3'
                            : 'flex items-center gap-3 rounded-[17px] border border-black/[0.05] bg-white p-3'
                        }
                      >
                        <span
                          className={
                            done
                              ? 'grid size-9 shrink-0 place-items-center rounded-full bg-[#dfeecf] text-[#4f8b42]'
                              : isNext
                                ? 'grid size-9 shrink-0 place-items-center rounded-full bg-[#5862e2] text-white'
                                : 'grid size-9 shrink-0 place-items-center rounded-full bg-[#efeff2] text-black/35'
                          }
                        >
                          {done ? <Check className="size-4" /> : <BookOpen className="size-4" />}
                        </span>
                        <div className="min-w-0 flex-1">
                          <p className="truncate text-[11px] font-black">{lesson.title}</p>
                          <p className="mt-1 truncate text-[9px] text-black/40">
                            {tPlan('lessonTypes.' + lesson.lessonType)} · {lesson.estimatedMinutes} min
                          </p>
                        </div>
                        {lesson.id && !done && (
                          <Link href={'/lesson/' + lesson.id} className="rounded-full bg-[#070709] px-3 py-2 text-[9px] font-black text-white">
                            {t('startLesson')}
                          </Link>
                        )}
                        {done && <Check className="size-4 text-[#5c9b4c]" />}
                      </div>
                    )
                  })}

                  {todayLessons.length === 0 && (
                    <div className="rounded-[18px] bg-[#f3f2f3] p-5 text-xs text-black/50">
                      {t('startWithAssessment')}
                      <div className="mt-4">
                        <Link href="/assessment" className="inline-flex rounded-full bg-[#070709] px-4 py-2.5 text-[10px] font-black text-white">
                          {tNav('assessment')}
                        </Link>
                      </div>
                    </div>
                  )}
                </div>

                {hasPlan && (
                  <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-black/[0.06] pt-4">
                    <span className="text-[9px] font-bold text-black/40">{pendingCount} {t('pendingLessons')}</span>
                    <button
                      type="button"
                      onClick={skipDay}
                      disabled={skipping}
                      className="rounded-full border border-black/10 px-4 py-2 text-[9px] font-black transition hover:bg-black/[0.04] disabled:opacity-50"
                    >
                      {skipping ? '…' : t('skipDay')}
                    </button>
                  </div>
                )}
                {skipError && <p className="mt-3 text-[9px] text-red-600">{tError('body')}</p>}
              </div>
            </section>

            <aside className="space-y-4">
              <div className="rounded-[26px] bg-white p-5 shadow-sm ring-1 ring-black/[0.04]">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h2 className="text-[20px] font-black tracking-tight">{t('lessonReady')} 📚</h2>
                    <p className="mt-1.5 text-[9px] text-black/40">
                      {t('completedToday', { completed: completedLessonCount, total: todayLessons.length || 0 })}
                    </p>
                  </div>
                  <CalendarDays className="size-5 text-[#373fb8]" />
                </div>
                <div className="mt-5 grid grid-cols-5 gap-1.5">
                  {progressBars.length ? progressBars.map(({ day, value, active }) => (
                    <div key={day} className="rounded-[14px] bg-[#f3f2f3] px-1.5 py-2 text-center">
                      <span className="text-[8px] font-black text-black/35">{day}</span>
                      <span className="mt-1 block text-[13px] font-black">{20 + index}</span>
                      <span className={active ? 'mx-auto mt-2 block size-3 rounded-full bg-[#78bb65]' : 'mx-auto mt-2 block size-3 rounded-full bg-[#9a9ff3]'} />
                    </div>
                  )) : Array.from({ length: 5 }).map((_, index) => (
                    <div key={index} className="rounded-[14px] bg-[#f3f2f3] px-1.5 py-2 text-center">
                      <span className="text-[8px] font-black text-black/20">—</span>
                      <span className="mt-1 block text-[13px] font-black text-black/20">—</span>
                      <span className="mx-auto mt-2 block size-3 rounded-full bg-[#e2e2e6]" />
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-[26px] bg-white p-5 shadow-sm ring-1 ring-black/[0.04]">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-[18px] font-black tracking-tight">{t('recentPerformance')}</h3>
                    <p className="mt-1 text-[9px] text-black/35">{t('accuracy')}: {accuracy}%</p>
                  </div>
                  <Link href="/progress" className="grid size-8 place-items-center rounded-full bg-[#f3f2f3]" aria-label={t('recentPerformance')}>
                    <MoreHorizontal className="size-4" />
                  </Link>
                </div>
                <div className="mt-4 h-[118px] rounded-[20px] bg-[#eeedff] p-3">
                  <div className="flex h-full items-end gap-2">
                    {performanceValues.map((value, index) => (
                      <div key={index} className="flex h-full flex-1 items-end">
                        <div className="w-full rounded-t-[9px] bg-[#5862e2]" style={{ height: Math.max(12, value) + '%' }} />
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="rounded-[25px] bg-[#f95d22] p-5">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-[9px] font-black uppercase tracking-[.15em] text-[#713619]">{t('streak')}</p>
                    <p className="mt-1 text-[29px] font-black tracking-tight text-[#070709]">{streak}</p>
                  </div>
                  <span className="grid size-11 place-items-center rounded-full bg-white/25">
                    <Flame className="size-5 text-[#070709]" />
                  </span>
                </div>
                <p className="mt-3 text-[10px] font-semibold leading-relaxed text-[#713619]">
                  {t('recentPerformanceDescription')}
                </p>
              </div>

              <div className="rounded-[26px] bg-white p-5 shadow-sm ring-1 ring-black/[0.04]">
                <div className="mb-4 flex items-center justify-between">
                  <h3 className="text-[18px] font-black tracking-tight">{tNav('resources')}</h3>
                  <MoreHorizontal className="size-4 text-black/30" />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <Link href="/reading" className="group relative min-h-[145px] overflow-hidden rounded-[20px] bg-[#9a9ff3] p-4 text-white transition hover:-translate-y-0.5">
                    <BookOpen className="size-6" />
                    <div className="absolute -right-8 -top-7 size-24 rounded-full border-[13px] border-white/10" />
                    <p className="absolute bottom-4 left-4 right-3 text-[11px] font-black leading-tight">{tNav('reading')}</p>
                    <ArrowUpRight className="absolute bottom-3 right-3 size-4 opacity-0 transition group-hover:opacity-100" />
                  </Link>
                  <Link href="/courses" className="group relative min-h-[145px] overflow-hidden rounded-[20px] bg-[#373fb8] p-4 text-white transition hover:-translate-y-0.5">
                    <Library className="size-6" />
                    <div className="absolute -bottom-10 -right-8 size-28 rounded-full bg-white/10" />
                    <p className="absolute bottom-4 left-4 right-3 text-[11px] font-black leading-tight">{tNav('courses')}</p>
                    <ArrowUpRight className="absolute bottom-3 right-3 size-4 opacity-0 transition group-hover:opacity-100" />
                  </Link>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2">
                {[
                  { href: '/flashcards', icon: BookOpen, label: tNav('flashcards') },
                  { href: '/chat', icon: Mic2, label: tNav('tutor') },
                  { href: '/listening', icon: Headphones, label: tNav('listening') },
                ].map(({ href, icon: Icon, label }) => (
                  <Link key={href} href={href} className="flex min-h-[72px] flex-col items-center justify-center gap-2 rounded-[18px] bg-white text-center text-[9px] font-black shadow-sm ring-1 ring-black/[0.04] transition hover:-translate-y-0.5">
                    <Icon className="size-4 text-[#5862e2]" />
                    {label}
                  </Link>
                ))}
              </div>
            </aside>
          </div>

          <section className="grid gap-3 border-t border-black/[0.06] bg-[#f0f0ee] px-4 py-4 sm:grid-cols-3 sm:px-6">
            <button type="button" onClick={() => setActiveInsight('next')} className="group w-full rounded-[21px] bg-[#070709] p-4 text-left text-white transition hover:-translate-y-0.5">
              <div className="flex items-center justify-between gap-3"><span className="text-[9px] font-black uppercase tracking-[.15em] text-white/40">{t('nextStep')}</span><span className="grid size-8 place-items-center rounded-full bg-white/10 transition group-hover:bg-[#5862e2]"><Play className="size-3.5 fill-white" /></span></div>
              <p className="mt-3 truncate text-sm font-black">{nextLesson?.title || t('startWithAssessment')}</p>
              <p className="mt-1 text-[9px] text-white/40">{nextLesson ? nextLesson.estimatedMinutes + ' min' : tNav('assessment')}</p>
            </button>
            <button type="button" onClick={() => setActiveInsight('performance')} className="group w-full rounded-[21px] bg-[#9a9ff3] p-4 text-left text-white transition hover:-translate-y-0.5">
              <div className="flex items-center justify-between gap-3"><span className="text-[9px] font-black uppercase tracking-[.15em] text-white/55">{t('recentPerformance')}</span><span className="grid size-8 place-items-center rounded-full bg-white/15 transition group-hover:bg-white/25"><ArrowUpRight className="size-3.5" /></span></div>
              <div className="mt-3 flex items-end justify-between gap-4"><p className="text-[30px] font-black leading-none">{accuracy}%</p><p className="text-right text-[9px] font-bold text-white/60">{totalExercises} · {t('accuracy')}</p></div>
            </button>
            <button type="button" onClick={() => setActiveInsight('vocabulary')} className="group w-full rounded-[21px] bg-[#ffcf58] p-4 text-left text-[#070709] transition hover:-translate-y-0.5">
              <div className="flex items-center justify-between gap-3"><span className="text-[9px] font-black uppercase tracking-[.15em] text-black/40">{t('vocabularyProgress', { level: vocabularyLevel || '—' })}</span><span className="grid size-8 place-items-center rounded-full bg-white/40 transition group-hover:bg-white/60"><BookOpen className="size-3.5" /></span></div>
              <div className="mt-3 flex items-end justify-between gap-4"><p className="text-[24px] font-black leading-none">{vocabularyMastered}</p><p className="text-right text-[9px] font-bold text-black/45">{t('vocabularyWords', { mastered: vocabularyMastered, total: vocabularyTotal })}</p></div>
              <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-black/10"><div className="h-full rounded-full bg-[#070709]" style={{ width: vocabularyProgressPct + '%' }} /></div>
            </button>
          </section>

          {activeInsight && (
            <div className="border-t border-black/[0.06] bg-[#070709] px-4 py-5 text-white sm:px-6">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-[9px] font-black uppercase tracking-[.16em] text-white/40">
                    {activeInsight === 'next' ? t('nextStep') : activeInsight === 'performance' ? t('recentPerformance') : t('vocabularyProgress', { level: vocabularyLevel || '—' })}
                  </p>
                  <h3 className="mt-1 text-lg font-black">
                    {activeInsight === 'next' ? (nextLesson?.title || t('startWithAssessment')) : activeInsight === 'performance' ? accuracy + '% ' + t('accuracy') : vocabularyMastered + ' / ' + vocabularyTotal}
                  </h3>
                  <p className="mt-1 text-[10px] text-white/50">
                    {activeInsight === 'next' ? (nextLesson ? nextLesson.estimatedMinutes + ' min' : tNav('assessment')) : activeInsight === 'performance' ? totalExercises + ' ' + t('exerciseStats', { correct: exercisesCorrect, total: totalExercises }).split(' ').slice(-1).join(' ') : t('vocabularyWords', { mastered: vocabularyMastered, total: vocabularyTotal })}
                  </p>
                </div>
                <button type="button" onClick={() => setActiveInsight(null)} className="rounded-full bg-white/10 px-3 py-1.5 text-[9px] font-black" aria-label="Close">×</button>
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                {activeInsight === 'next' && (
                  <Link href={nextLesson?.id ? '/lesson/' + nextLesson.id : '/assessment'} className="rounded-full bg-[#5862e2] px-4 py-2.5 text-[10px] font-black">{nextLesson ? t('nextStep') : tNav('assessment')} <ArrowUpRight className="ml-1 inline size-3" /></Link>
                )}
                {activeInsight === 'performance' && <Link href="/progress" className="rounded-full bg-[#5862e2] px-4 py-2.5 text-[10px] font-black">{tNav('progress')} <ArrowUpRight className="ml-1 inline size-3" /></Link>}
                {activeInsight === 'vocabulary' && <Link href="/flashcards" className="rounded-full bg-[#5862e2] px-4 py-2.5 text-[10px] font-black">{tNav('flashcards')} <ArrowUpRight className="ml-1 inline size-3" /></Link>}
              </div>
            </div>
          )}

          {(vocabularyTotal > 0 || totalExercises > 0) && (
            <div className="grid gap-3 border-t border-black/[0.06] bg-[#f0f0ee] px-4 py-4 sm:grid-cols-3 sm:px-6">
              <div className="rounded-[19px] bg-white p-4">
                <p className="text-[9px] font-black uppercase tracking-widest text-black/35">
                  {t('vocabularyProgress', { level: vocabularyLevel || '—' })}
                </p>
                <div className="mt-3 h-2 rounded-full bg-[#eeedff]">
                  <div className="h-full rounded-full bg-[#5862e2]" style={{ width: vocabularyProgressPct + '%' }} />
                </div>
                <p className="mt-2 text-[9px] font-bold text-black/40">
                  {t('vocabularyWords', { mastered: vocabularyMastered, total: vocabularyTotal })}
                </p>
              </div>
              <div className="rounded-[19px] bg-white p-4">
                <p className="text-[9px] font-black uppercase tracking-widest text-black/35">
                  {t('exerciseStats', { correct: exercisesCorrect, total: totalExercises })}
                </p>
                <p className="mt-2 text-[26px] font-black">{accuracy}%</p>
              </div>
              <div className="rounded-[19px] bg-[#070709] p-4 text-white">
                <p className="text-[9px] font-black uppercase tracking-widest text-white/35">{t('daysRemaining')}</p>
                <p className="mt-2 text-[26px] font-black">{Math.max(totalDays - progressDay, 0)}</p>
              </div>
            </div>
          )}

          {showPremiumBanner && (
            <section className="mx-3 mb-4 rounded-[24px] border border-[#e4e2f0] bg-white p-5 sm:mx-6">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div className="flex gap-3">
                  <span className="grid size-10 shrink-0 place-items-center rounded-full bg-[#ffcf67] text-sm">★</span>
                  <div>
                    <p className="text-[10px] font-black uppercase tracking-[.12em] text-black/45">
                      {freemiumTrialActive
                        ? t('freemiumTrialTitle', { days: freemiumTrialDaysLeft })
                        : t(paymentRecovery ? 'premiumBannerPastDueTitle' : 'premiumBannerTitle')}
                    </p>
                    <p className="mt-2 max-w-2xl text-xs leading-relaxed text-black/50">
                      {freemiumTrialActive
                        ? t('freemiumTrialDesc', { days: freemiumTrialDaysLeft })
                        : paymentRecovery
                          ? t('premiumBannerPastDueDesc')
                          : t(trialEligible ? 'premiumBannerDesc' : 'premiumBannerDescTrialUsed')}
                    </p>
                  </div>
                </div>
                {!freemiumTrialActive && (
                  <span className="self-start rounded-full border border-[#7776df]/30 px-4 py-2 text-[10px] font-black text-[#5f5ec5]">
                    {paymentRecovery
                      ? t('premiumBannerPastDueCta')
                      : t(trialEligible ? 'premiumBannerCta' : 'premiumBannerCtaTrialUsed')}
                  </span>
                )}
              </div>

              {!freemiumTrialActive &&
                (paymentRecovery ? (
                  <div className="mt-4 border-t border-black/5 pt-4">
                    <button
                      onClick={handleManageSubscription}
                      disabled={portalLoading}
                      className="rounded-full bg-[#070709] px-5 py-3 text-xs font-black text-white disabled:opacity-50"
                    >
                      {portalLoading ? '…' : tBilling('updatePayment')}
                    </button>
                    {portalError && <p className="mt-3 text-xs text-red-500">{portalError}</p>}
                  </div>
                ) : (
                  <SubscriptionPlanButtons className="mt-4 border-t border-black/5 pt-4" />
                ))}
            </section>
          )}

          <footer className="flex flex-wrap items-center gap-2 border-t border-black/[0.06] bg-[#f0f0ee] px-4 py-4 sm:px-6">
            <Link href="/plan" className="rounded-full bg-[#070709] px-5 py-3 text-[10px] font-black text-white">{t('goToMyPlan')}</Link>
            {pendingCount > 0 && (
              <Link href="/plan" className="rounded-full bg-white px-5 py-3 text-[10px] font-black ring-1 ring-black/10">
                {pendingCount} {t('pendingLessons')} →
              </Link>
            )}
            <Link href="/flashcards" className="rounded-full bg-white px-5 py-3 text-[10px] font-black ring-1 ring-black/10">{tNav('flashcards')}</Link>
            <Link href="/chat" className="rounded-full bg-white px-5 py-3 text-[10px] font-black ring-1 ring-black/10">{tNav('tutor')}</Link>
            <Link href="/assessment" className="rounded-full bg-white px-5 py-3 text-[10px] font-black ring-1 ring-black/10">{tNav('assessment')}</Link>
          </footer>
        </div>
      </main>
    </>
  )
}
