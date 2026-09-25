'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { BookOpen, BookOpenCheck, Check, ChevronDown, Flame, Headphones, LayoutDashboard, Library, ListChecks, MessageCircle, Mic2, Play, Settings, Target, Trophy, UserRound, Zap, Bell } from 'lucide-react'
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

export default function DashboardPage() {
  const t = useTranslations('dashboard')
  const tAssessment = useTranslations('assessment')
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
  const [planId, setPlanId] = useState<number | null>(null)
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

  const loadData = useCallback(async () => {
    try {
      const [progRes, planRes] = await Promise.all([
        apiFetch('/api/progress/summary'),
        apiFetch('/api/study-plan/today'),
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
      if (planRes.ok) {
        const plan = await planRes.json()
        setCefrLevel(plan.cefr_level ?? null)
        setPlanId(plan.plan_id ?? null)
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
        setPlanId(null)
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
    // eslint-disable-next-line react-hooks/exhaustive-deps -- re-fetch when active language changes
  }, [setProgress, setTodayLessons, activeLanguage?.code])

  useEffect(() => {
    // AppLayout establishes the authenticated session before the dashboard
    // starts protected API requests. Avoid transient 401s while auth boots.
    if (!user || !accessToken) return
    loadData()
  }, [loadData, user, accessToken])

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
      <div className="flex min-h-screen flex-col items-center justify-center gap-4">
        <p className="text-[var(--juba-app-muted)] font-sans text-sm">{tError('body')}</p>
        <button
          type="button"
          onClick={() => {
            setLoadError(false)
            setLoading(true)
            loadData()
          }}
          className="text-[var(--juba-app-green-dark)] font-sans text-xs tracking-widest uppercase underline"
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
  const daysRemaining = hasPlan
    ? planPositionComplete
      ? 0
      : Math.max(totalDays - progressDay, 0)
    : 0
  const currentDayDisplay = planPositionComplete
    ? totalDays
    : Math.min(progressDay + 1, totalDays)
  const vocabularyProgressPct = Math.round(vocabularyProgress * 100)
  const paymentRecovery = needsPaymentRecovery(user)
  const showPremiumBanner = stripeEnabled && !isSubscribed(user, stripeEnabled)

  function getPerformanceLabel(value: number) {
    if (value < 0.5) return t('performanceNeedsPractice')
    if (value < 0.8) return t('performanceInProgress')
    return t('performanceStrong')
  }

                  return (
    <>
      <OnboardingTour />
      <WhatsNew />
      <main className="min-h-screen bg-[#dfe3ff] px-3 py-3 sm:px-5 sm:py-5 lg:px-7">
        <div className="mx-auto max-w-[1500px] overflow-hidden rounded-[38px] border border-black/10 bg-[#f6f6f4] shadow-[0_35px_100px_-35px_rgba(24,28,46,.55)]">
          {/* EduView-style member shell */}
          <header className="flex min-h-[92px] items-center gap-4 bg-[#24272b] px-5 py-4 text-white sm:px-7 lg:px-9">
            <Link href="/dashboard" className="flex shrink-0 items-center gap-3">
              <span className="grid size-12 place-items-center rounded-full bg-[#7776df] shadow-inner shadow-white/20">
                <BookOpenCheck className="size-6" />
              </span>
              <span className="hidden text-xl font-black tracking-[-.04em] sm:inline">JUBA LISAN</span>
            </Link>

            <nav className="mx-auto flex items-center gap-1 rounded-full bg-[#17191c] p-1.5 shadow-inner shadow-black/30">
              {[
                { href: "/dashboard", icon: LayoutDashboard, label: t('today') },
                { href: "/plan", icon: ListChecks, label: t('planProgress') },
                { href: "/progress", icon: Trophy, label: t('recentPerformance') },
                { href: "/courses", icon: Library, label: tNav('courses') },
                { href: "/settings", icon: Settings, label: tNav('settings') },
              ].map((item, index) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    title={item.label}
                    className={`grid size-11 place-items-center rounded-full transition ${index === 0 ? "bg-black text-white shadow-lg" : "text-white/55 hover:bg-white/10 hover:text-white"}`}
                  >
                    <Icon className="size-[18px]" />
                  </Link>
                )
              })}
            </nav>

            <div className="hidden items-center gap-3 sm:flex">
              <div className="text-right">
                <p className="text-sm font-black">{user?.displayName || user?.username}</p>
                <p className="mt-0.5 text-xs text-white/65">
                  {t('planProgress')}: {planCompletion}%
                </p>
              </div>
              <div className="grid size-12 place-items-center overflow-hidden rounded-full bg-[#d8c9a9] text-[#25272b]">
                <UserRound className="size-7" />
              </div>
              <button type="button" className="relative grid size-11 place-items-center rounded-full border border-white/10 text-white/75 hover:bg-white/10" aria-label="Notifications">
                <Bell className="size-5" />
                <span className="absolute right-2 top-2 size-2 rounded-full bg-[#f26b69]" />
              </button>
            </div>
          </header>

          <div className="grid gap-5 p-4 sm:p-6 lg:grid-cols-[minmax(260px,1fr)_minmax(430px,1.45fr)_minmax(280px,.85fr)] lg:gap-5 lg:p-6">
            {/* LEFT COLUMN */}
            <section className="space-y-5">
              <div className="relative min-h-[245px] overflow-hidden rounded-[34px] bg-[#7978db] p-6 text-white shadow-[inset_0_-20px_50px_rgba(45,46,130,.18)]">
                <div className="absolute -right-8 -top-10 size-40 rounded-full border-[18px] border-white/10" />
                <div className="absolute bottom-[-55px] left-[-30px] size-44 rounded-full bg-[#6a69c9]" />
                <div className="relative z-10">
                  <span className="inline-flex rounded-full bg-white/15 px-3 py-1 text-[10px] font-bold uppercase tracking-[.16em]">
                    {activeLanguage ? tTarget(activeLanguage.code) : "JUBA LISAN"}
                  </span>
                  <h1 className="mt-5 max-w-[230px] text-3xl font-black leading-[.98] tracking-[-.055em]">
                    {t('welcomeBack')}, {user?.displayName || user?.username}
                  </h1>
                  <p className="mt-3 max-w-[235px] text-sm leading-relaxed text-white/75">
                    {cefrLevel ? `${cefrLevel} · ` : ""}{t('nextStep')}
                  </p>
                  <Link href={nextLesson?.id ? `/lesson/${nextLesson.id}` : "/assessment"} className="mt-7 inline-flex size-12 items-center justify-center rounded-full border-2 border-white/70 bg-[#26282c] transition hover:scale-105">
                    <Play className="ml-0.5 size-4 fill-white" />
                  </Link>
                </div>
                <div className="absolute bottom-5 right-5 text-7xl opacity-20">✦</div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-[28px] border-2 border-[#ffad63] bg-white p-5">
                  <div className="flex items-center gap-2 text-xs font-bold text-[#4b4b4b]">
                    <span className="grid size-7 place-items-center rounded-full bg-[#ffad63]/25"><ListChecks className="size-3.5" /></span>
                    {t('lessonsCompleted')}
                  </div>
                  <p className="mt-5 text-4xl font-black tracking-[-.06em]">{totalLessons}</p>
                </div>
                <div className="rounded-[28px] border-2 border-[#8d8be7] bg-white p-5">
                  <div className="flex items-center gap-2 text-xs font-bold text-[#4b4b4b]">
                    <span className="grid size-7 place-items-center rounded-full bg-[#8d8be7]/20"><Flame className="size-3.5" /></span>
                    {t('streak')}
                  </div>
                  <p className="mt-5 text-4xl font-black tracking-[-.06em]">{streak}</p>
                </div>
              </div>

              <div className="flex flex-wrap gap-2">
                {[
                  { icon: BookOpen, label: tNav('flashcards'), href: "/flashcards" },
                  { icon: Mic2, label: tNav('tutor'), href: "/chat" },
                  { icon: Headphones, label: tNav('listening'), href: "/listening" },
                ].map(({ icon: Icon, label, href }) => (
                  <Link key={href} href={href} className="inline-flex items-center gap-2 rounded-full bg-white px-4 py-2.5 text-xs font-bold text-[#292b2f] shadow-sm ring-1 ring-black/5 transition hover:-translate-y-0.5">
                    <Icon className="size-4 text-[#6f70d8]" />
                    {label}
                  </Link>
                ))}
              </div>

              <div className="rounded-[32px] bg-[#292c30] p-6 text-white shadow-lg">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-[.16em] text-[#ffb06b]">{t('recentPerformance')}</p>
                    <h2 className="mt-3 text-xl font-black leading-tight">
                      {skillEntries.length > 0 ? getPerformanceLabel(skillEntries[skillEntries.length - 1].value) : t('noSkills')}
                    </h2>
                  </div>
                  <Link href="/progress" className="grid size-10 place-items-center rounded-full bg-white/10 hover:bg-white/15"><ChevronDown className="size-4 -rotate-90" /></Link>
                </div>
                <div className="mt-6 flex items-end gap-1">
                  {skillEntries.slice(-6).map(({ skill, value }, i) => (
                    <div key={skill || i} className="flex flex-1 flex-col items-center gap-2">
                      <div className="flex h-28 w-full items-end justify-center rounded-2xl bg-white/5 p-2">
                        <div className="w-full rounded-xl bg-[#8c8be5]" style={{ height: `${Math.max(16, value * 100)}%` }} />
                      </div>
                      <span className="text-[9px] text-white/45">{Math.round(value * 100)}%</span>
                    </div>
                  ))}
                  {skillEntries.length === 0 && <div className="h-28 w-full rounded-2xl bg-white/5" />}
                </div>
              </div>
            </section>

            {/* CENTER COLUMN */}
            <section className="space-y-5">
              <div className="rounded-[34px] bg-white p-5 shadow-sm ring-1 ring-black/5 sm:p-6">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-[.15em] text-black/45">{t('planProgress')}</p>
                    <h2 className="mt-1 text-3xl font-black tracking-[-.06em]">{planCompletion}%</h2>
                  </div>
                  <button type="button" className="flex items-center gap-2 rounded-full bg-[#f5f5f5] px-4 py-2.5 text-xs font-bold">
                    {activeLanguage ? tTarget(activeLanguage.code) : t('today')}
                    <ChevronDown className="size-3.5" />
                  </button>
                </div>

                <div className="mt-5 overflow-hidden rounded-[30px] bg-[#ffab63] p-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-4xl font-black tracking-[-.06em]">{totalLessons}</p>
                      <p className="mt-1 text-sm font-bold">{t('lessonsCompleted')}</p>
                    </div>
                    <div className="rounded-full bg-[#1e2024] p-1">
                      <span className="inline-flex rounded-full bg-[#ffab63] px-3 py-1.5 text-xs font-black">{totalDays > 0 ? t('planProgress') : t('today')}</span>
                    </div>
                  </div>
                  <div className="mt-8 grid grid-cols-5 items-end gap-3">
                    {[0,1,2,3,4].map((_, i) => {
                      const dayValue = Math.max(10, Math.min(100, [39, 14, 48, 24, 32][i] + Math.round(planCompletion / 10)))
                      return (
                        <div key={i} className="text-center">
                          <div className="flex h-32 items-end justify-center rounded-2xl border border-dashed border-black/10">
                            <div className="relative w-11 rounded-t-full bg-[#7a4929]/65" style={{ height: `${dayValue}%` }}>
                              <span className="absolute -top-7 left-1/2 -translate-x-1/2 text-[11px] font-black">{dayValue}</span>
                            </div>
                          </div>
                          <span className="mt-2 block text-[10px] font-bold text-black/55">{i === 0 ? "Mon" : i === 1 ? "Tue" : i === 2 ? "Wed" : i === 3 ? "Thu" : "Fri"}</span>
                        </div>
                      )
                    })}
                  </div>
                </div>

                <div className="mt-4 flex items-center justify-between rounded-full bg-[#ececed] px-4 py-3">
                  <div className="flex items-center gap-3">
                    <span className="grid size-9 place-items-center rounded-full bg-[#ffcd58]"><Trophy className="size-4" /></span>
                    <div>
                      <p className="text-xs font-black">{t('recentPerformance')}</p>
                      <p className="text-[10px] text-black/45">{t('accuracy')}</p>
                    </div>
                  </div>
                  <div className="flex -space-x-2">
                    {[0,1,2].map((i) => <span key={i} className="grid size-8 place-items-center rounded-full border-2 border-white bg-[#b8b7ee] text-xs font-bold">{i + 1}</span>)}
                  </div>
                </div>
              </div>

              <div className="rounded-[34px] bg-white p-5 shadow-sm ring-1 ring-black/5 sm:p-6">
                <div className="mb-4 flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-[.15em] text-black/40">{t('today')}</p>
                    <h2 className="mt-1 text-2xl font-black tracking-[-.05em]">{t('nextStep')}</h2>
                  </div>
                  {hasPlan && totalDays > 0 && <span className="rounded-full bg-[#ececff] px-3 py-1 text-xs font-black text-[#6565c9]">{currentDayDisplay}/{totalDays}</span>}
                </div>

                <div className="space-y-2.5">
                  {todayLessons.slice(0, 5).map((lesson, i) => {
                    const isDone = (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
                    const isNext = nextLesson?.id === lesson.id
                    return (
                      <div key={i} className={`flex items-center gap-3 rounded-[22px] border p-3.5 transition ${isNext ? "border-[#8b8ae5] bg-[#f1f0ff]" : "border-black/5 bg-[#fafafa]"}`}>
                        <span className={`grid size-11 shrink-0 place-items-center rounded-full ${isDone ? "bg-[#dcefd0] text-[#4e8a3f]" : isNext ? "bg-[#8d8ce5] text-white" : "bg-[#e9e9ea] text-black/40"}`}>
                          {isDone ? <Check className="size-4" /> : <BookOpen className="size-4" />}
                        </span>
                        <div className="min-w-0 flex-1">
                          <p className="truncate text-sm font-black">{lesson.title}</p>
                          <p className="mt-0.5 text-[10px] text-black/45">{tPlan(`lessonTypes.${lesson.lessonType}`)} · {lesson.estimatedMinutes}min</p>
                        </div>
                        {lesson.id && !isDone && <Link href={`/lesson/${lesson.id}`} className="rounded-full bg-[#27292d] px-3 py-2 text-[10px] font-black text-white">{t('startLesson')}</Link>}
                        {isDone && <span className="text-[10px] font-black text-black/40">✓</span>}
                      </div>
                    )
                  })}
                  {todayLessons.length === 0 && (
                    <div className="rounded-[22px] bg-[#f5f5f5] p-5 text-sm text-black/50">{t('startWithAssessment')}</div>
                  )}
                </div>
              </div>
            </section>

            {/* RIGHT COLUMN */}
            <aside className="space-y-5">
              <div className="rounded-[32px] bg-white p-5 shadow-sm ring-1 ring-black/5">
                <div className="flex items-start justify-between">
                  <div>
                    <h2 className="text-2xl font-black leading-none tracking-[-.055em]">{t('lessonReady')} 📚</h2>
                    <p className="mt-2 text-xs text-black/45">{t('completedToday', { completed: completedLessonCount, total: todayLessons.length || 0 })}</p>
                  </div>
                  <BookOpen className="size-6 text-[#d87822]" />
                </div>

                <div className="mt-5 grid grid-cols-5 gap-1.5">
                  {["Mon","Tue","Wed","Thu","Fri"].map((day, i) => (
                    <div key={day} className="rounded-[18px] bg-[#f5f5f5] p-2 text-center">
                      <span className="text-[9px] font-bold text-black/40">{day}</span>
                      <span className="mt-1 block text-sm font-black">{20 + i}</span>
                      <span className={`mx-auto mt-2 block size-3 rounded-full ${i < 2 ? "bg-[#ef6c6c]" : "bg-[#78bb65]"}`} />
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-[32px] bg-white p-5 shadow-sm ring-1 ring-black/5">
                <div className="mb-4 flex items-center justify-between">
                  <h3 className="text-lg font-black tracking-[-.03em]">{t('recentPerformance')}</h3>
                  <span className="text-lg">•••</span>
                </div>
                <div className="h-28 overflow-hidden rounded-[22px] bg-[#efefef] p-4">
                  <div className="flex h-full items-end gap-2">
                    {[.45,.62,.78,.58,.9,.72,.84].map((v,i) => (
                      <div key={i} className="flex-1 rounded-t-lg bg-[#9a99e8]" style={{height:`${v*100}%`}} />
                    ))}
                  </div>
                </div>
                <div className="mt-3 flex items-center justify-between text-[10px] text-black/45">
                  <span>June</span><span>July</span><span>August</span>
                </div>
              </div>

              <div className="rounded-[30px] bg-[#8180df] p-5 text-white shadow-sm">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-[.15em] text-white/70">{t('streak')}</p>
                    <p className="mt-1 text-lg font-black">{streak} days</p>
                  </div>
                  <span className="grid size-11 place-items-center rounded-full bg-white/15"><Flame className="size-5" /></span>
                </div>
                <p className="mt-4 text-xs leading-relaxed text-white/75">{t('recentPerformanceDescription')}</p>
              </div>

              <div className="rounded-[32px] bg-white p-5 shadow-sm ring-1 ring-black/5">
                <div className="mb-4 flex items-center justify-between">
                  <h3 className="text-lg font-black tracking-[-.03em]">{tNav('resources')}</h3>
                  <span className="text-lg">•••</span>
                </div>
                <div className="grid grid-cols-2 gap-2.5">
                  <Link href="/reading" className="group relative min-h-[150px] overflow-hidden rounded-[22px] bg-[#ffcf67] p-4">
                    <BookOpen className="size-7 text-[#9a5b16]" />
                    <p className="absolute bottom-3 left-3 right-3 text-xs font-black leading-tight">{tNav('reading')}</p>
                  </Link>
                  <Link href="/courses" className="group relative min-h-[150px] overflow-hidden rounded-[22px] bg-[#8d8ce5] p-4 text-white">
                    <Library className="size-7" />
                    <p className="absolute bottom-3 left-3 right-3 text-xs font-black leading-tight">{tNav('courses')}</p>
                  </Link>
                </div>
              </div>
            </aside>
          </div>

          {showPremiumBanner && (
            <div className="mx-4 mb-4 rounded-[28px] border border-[#ece8f8] bg-white p-5 shadow-sm sm:mx-6">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div className="flex gap-3">
                  <span className="grid size-10 place-items-center rounded-full bg-[#ffcf67] text-sm">★</span>
                  <div>
                    <p className="text-xs font-black uppercase tracking-[.12em] text-black/45">
                      {freemiumTrialActive ? t('freemiumTrialTitle', { days: freemiumTrialDaysLeft }) : t(paymentRecovery ? 'premiumBannerPastDueTitle' : 'premiumBannerTitle')}
                    </p>
                    <p className="mt-2 max-w-2xl text-xs leading-relaxed text-black/50">
                      {freemiumTrialActive ? t('freemiumTrialDesc', { days: freemiumTrialDaysLeft }) : paymentRecovery ? t('premiumBannerPastDueDesc') : t(trialEligible ? 'premiumBannerDesc' : 'premiumBannerDescTrialUsed')}
                    </p>
                  </div>
                </div>
                {!freemiumTrialActive && <span className="self-start rounded-full border border-[#7776df]/30 px-4 py-2 text-xs font-black text-[#5f5ec5]">{paymentRecovery ? t('premiumBannerPastDueCta') : t(trialEligible ? 'premiumBannerCta' : 'premiumBannerCtaTrialUsed')}</span>}
              </div>
              {!freemiumTrialActive && (paymentRecovery ? (
                <div className="mt-4 border-t border-black/5 pt-4">
                  <button onClick={handleManageSubscription} disabled={portalLoading} className="rounded-full bg-[#292c30] px-5 py-3 text-xs font-black text-white disabled:opacity-50">{portalLoading ? '...' : tBilling('updatePayment')}</button>
                  {portalError && <p className="mt-3 text-xs text-red-500">{portalError}</p>}
                </div>
              ) : (
                <SubscriptionPlanButtons className="mt-4 border-t border-black/5 pt-4" />
              ))}
            </div>
          )}

          <footer className="flex flex-wrap items-center gap-2 border-t border-black/5 bg-[#f6f6f4] px-5 py-5 sm:px-7">
            <Link href="/plan" className="rounded-full bg-[#292c30] px-5 py-3 text-xs font-black text-white">{t('goToMyPlan')}</Link>
            {pendingCount > 0 && <Link href="/plan" className="rounded-full bg-white px-5 py-3 text-xs font-bold ring-1 ring-black/10">{pendingCount} {t('pendingLessons')} →</Link>}
            <Link href="/flashcards" className="rounded-full bg-white px-5 py-3 text-xs font-bold ring-1 ring-black/10">{tNav('flashcards')}</Link>
            <Link href="/chat" className="rounded-full bg-white px-5 py-3 text-xs font-bold ring-1 ring-black/10">{tNav('tutor')}</Link>
            <Link href="/assessment" className="rounded-full bg-white px-5 py-3 text-xs font-bold ring-1 ring-black/10">{tNav('assessment')}</Link>
          </footer>
        </div>
      </main>
    </>
  )

}
