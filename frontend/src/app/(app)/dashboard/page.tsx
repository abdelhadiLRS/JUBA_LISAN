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
      <main className="min-h-screen bg-[#e9eaf8] px-3 py-4 text-[#20232a] sm:px-5 sm:py-6 lg:px-8">
        <div className="mx-auto max-w-[1600px] overflow-hidden rounded-[34px] border border-black/10 bg-[#f8f8f7] shadow-[0_24px_80px_rgba(31,35,55,.12)]">
          <header className="flex flex-wrap items-center justify-between gap-4 bg-[#25282e] px-5 py-4 text-white sm:px-7">
            <Link href="/dashboard" className="flex items-center gap-3 font-bold tracking-tight">
              <span className="grid size-11 place-items-center rounded-full bg-[#8584e6] text-white"><LayoutDashboard className="size-5" /></span>
              <span className="text-lg">JUBA LISAN</span>
            </Link>
            <nav aria-label="Dashboard navigation" className="flex flex-wrap items-center justify-center gap-1 rounded-full bg-black/25 p-1">
              <Link href="/dashboard" aria-current="page" className="inline-flex items-center gap-2 rounded-full bg-black px-4 py-2.5 text-xs font-bold text-white"><LayoutDashboard className="size-4 text-[#aaa9ff]" />{t('today')}</Link>
              <Link href="/plan" className="inline-flex items-center gap-2 rounded-full px-3 py-2.5 text-xs font-semibold text-white/70 transition hover:bg-white/10 hover:text-white"><ListChecks className="size-4" />{t('goToMyPlan')}</Link>
              <Link href="/progress" className="inline-flex items-center gap-2 rounded-full px-3 py-2.5 text-xs font-semibold text-white/70 transition hover:bg-white/10 hover:text-white"><Trophy className="size-4" />{t('recentPerformance')}</Link>
              <Link href="/reading" className="inline-flex items-center gap-2 rounded-full px-3 py-2.5 text-xs font-semibold text-white/70 transition hover:bg-white/10 hover:text-white"><BookOpen className="size-4" />{tNav('reading')}</Link>
            </nav>
            <div className="flex items-center gap-3">
              <div className="hidden text-right sm:block">
                <p className="text-sm font-bold">{t('welcomeBack')}, {user?.displayName || user?.username}</p>
                <p className="mt-1 text-[11px] text-white/60">{t('streak')}: {streak} · {xp} XP</p>
              </div>
              <span className="grid size-11 place-items-center rounded-full border border-white/20 bg-[#aaa9ef] text-lg font-bold text-[#25282e]"><UserRound className="size-5" /></span>
            </div>
          </header>

          <div className="grid gap-5 p-4 sm:p-6 lg:grid-cols-[minmax(260px,.95fr)_minmax(420px,1.4fr)_minmax(270px,.85fr)] lg:gap-6 lg:p-7">
            <section className="min-w-0 space-y-5">
              <div className="relative min-h-[245px] overflow-hidden rounded-[30px] bg-[#8584e6] p-6 text-white">
                <div className="absolute -right-8 -top-10 size-44 rounded-full border-[20px] border-white/10" />
                <div className="absolute -bottom-14 -left-8 size-44 rounded-full bg-[#7372d1]" />
                <div className="relative z-10">
                  <span className="inline-flex rounded-full bg-white/15 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[.14em]">{activeLanguage ? tTarget(activeLanguage.code) : "JUBA LISAN"}</span>
                  <h1 className="mt-5 max-w-[260px] text-3xl font-black leading-[1.04] tracking-tight">{t('welcomeBack')}, {user?.displayName || user?.username}</h1>
                  <p className="mt-3 max-w-[245px] text-sm leading-relaxed text-white/80">{cefrLevel ? `${cefrLevel} · ` : ""}{t('nextStep')}</p>
                  <Link href={nextLesson?.id ? `/lesson/${nextLesson.id}` : "/assessment"} aria-label={t('startLesson')} className="mt-6 inline-flex size-12 items-center justify-center rounded-full border-2 border-white/70 bg-[#25282e] transition hover:scale-105"><Play className="ml-0.5 size-4 fill-white" /></Link>
                </div>
                <span className="absolute bottom-5 right-6 text-6xl font-black text-white/20">✦</span>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-[24px] border-2 border-[#ffad68] bg-white p-5">
                  <div className="flex items-center gap-2 text-xs font-bold text-[#50515a]"><span className="grid size-8 place-items-center rounded-full bg-[#ffad68]/25"><ListChecks className="size-4" /></span>{t('lessonsCompleted')}</div>
                  <p className="mt-4 text-4xl font-black tracking-tight">{totalLessons}</p>
                </div>
                <div className="rounded-[24px] border-2 border-[#9291eb] bg-[#eeedff] p-5">
                  <div className="flex items-center gap-2 text-xs font-bold text-[#50515a]"><span className="grid size-8 place-items-center rounded-full bg-[#9291eb]/20"><Flame className="size-4" /></span>{t('streak')}</div>
                  <p className="mt-4 text-4xl font-black tracking-tight">{streak}</p>
                </div>
              </div>

              <div className="flex flex-wrap gap-2">
                {[
                  { icon: BookOpen, label: tNav('flashcards'), href: "/flashcards" },
                  { icon: Mic2, label: tNav('tutor'), href: "/chat" },
                  { icon: Headphones, label: tNav('listening'), href: "/listening" },
                ].map(({ icon: Icon, label, href }) => <Link key={href} href={href} className="inline-flex items-center gap-2 rounded-full bg-white px-4 py-3 text-xs font-bold shadow-sm ring-1 ring-black/5 transition hover:-translate-y-0.5"><Icon className="size-4 text-[#7776d8]" />{label}</Link>)}
              </div>

              <div className="rounded-[28px] bg-[#25282e] p-5 text-white">
                <div className="flex items-start justify-between gap-3">
                  <div><p className="text-[10px] font-bold uppercase tracking-[.15em] text-[#ffb16c]">{t('recentPerformance')}</p><h2 className="mt-3 text-xl font-black leading-tight">{skillEntries.length ? getPerformanceLabel(skillEntries[skillEntries.length - 1].value) : t('noSkills')}</h2></div>
                  <Link href="/progress" aria-label={t('recentPerformance')} className="grid size-10 place-items-center rounded-full bg-white/10 hover:bg-white/20"><ChevronDown className="size-4 -rotate-90" /></Link>
                </div>
                <div className="mt-5 flex items-end gap-2">
                  {skillEntries.slice(-6).map(({ skill, value }, i) => <div key={skill || i} className="flex flex-1 flex-col items-center gap-2"><div className="flex h-24 w-full items-end rounded-xl bg-white/5 p-1.5"><div className="w-full rounded-lg bg-[#9291eb]" style={{ height: `${Math.max(12, value * 100)}%` }} /></div><span className="text-[9px] text-white/55">{Math.round(value * 100)}%</span></div>)}
                  {skillEntries.length === 0 && <div className="h-24 w-full rounded-xl bg-white/5" />}
                </div>
              </div>
            </section>

            <section className="min-w-0 space-y-5">
              <div className="rounded-[30px] bg-white p-5 shadow-sm ring-1 ring-black/5 sm:p-6">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div><p className="text-xs font-bold uppercase tracking-[.14em] text-black/45">{t('planProgress')}</p><h2 className="mt-1 text-3xl font-black tracking-tight">{planCompletion}%</h2></div>
                  <span className="inline-flex items-center gap-2 rounded-full bg-[#f3f3f7] px-4 py-2.5 text-xs font-bold"><BookOpen className="size-4 text-[#7776d8]" />{activeLanguage ? tTarget(activeLanguage.code) : t('today')}</span>
                </div>
                <div className="mt-5 rounded-[28px] bg-[#ffad68] p-5 sm:p-6">
                  <div className="flex items-start justify-between gap-3">
                    <div><p className="text-4xl font-black tracking-tight">{completedLessonCount}<span className="ml-2 text-base font-semibold">{t('lessonsCompleted')}</span></p><p className="mt-2 text-xs font-semibold text-[#754d2c]">{t('completedToday', { completed: completedLessonCount, total: todayLessons.length || 0 })}</p></div>
                    <span className="rounded-full bg-[#25282e] px-3 py-2 text-[10px] font-bold text-white">{totalDays > 0 ? `${currentDayDisplay}/${totalDays}` : t('today')}</span>
                  </div>
                  <div className="mt-7 grid grid-cols-5 items-end gap-2 sm:gap-3">
                    {[0,1,2,3,4].map((_, i) => {
                      const vals = [39,14,48,24,32]
                      const value = Math.max(10, Math.min(100, vals[i] + Math.round(planCompletion / 10)))
                      const label = ["Mon","Tue","Wed","Thu","Fri"][i]
                      return <div key={label} className="text-center"><div className="flex h-32 items-end justify-center rounded-2xl border border-dashed border-black/15"><div className="relative w-9 rounded-t-full bg-[#8b542e]/70 sm:w-11" style={{height:`${value}%`}}><span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[10px] font-black">{value}</span></div></div><span className="mt-2 block text-[10px] font-bold text-black/60">{label}</span></div>
                    })}
                  </div>
                </div>
                <div className="mt-4 flex items-center justify-between gap-3 rounded-full bg-[#f0f0f2] px-4 py-3">
                  <div className="flex items-center gap-3"><span className="grid size-9 place-items-center rounded-full bg-[#ffcf58]"><Trophy className="size-4" /></span><div><p className="text-xs font-black">{t('recentPerformance')}</p><p className="text-[10px] text-black/50">{t('accuracy')}: {accuracy}%</p></div></div>
                  <span className="rounded-full bg-white px-3 py-1.5 text-xs font-black">{xp} XP</span>
                </div>
              </div>

              <div className="rounded-[30px] bg-white p-5 shadow-sm ring-1 ring-black/5 sm:p-6">
                <div className="mb-4 flex items-center justify-between gap-3"><div><p className="text-xs font-bold uppercase tracking-[.14em] text-black/40">{t('today')}</p><h2 className="mt-1 text-2xl font-black tracking-tight">{t('nextStep')}</h2></div>{hasPlan && totalDays > 0 && <span className="rounded-full bg-[#ecebff] px-3 py-1.5 text-xs font-black text-[#6665c8]">{currentDayDisplay}/{totalDays}</span>}</div>
                <div className="space-y-2.5">
                  {todayLessons.slice(0,5).map((lesson,i) => {
                    const done = (Boolean(lesson.id) && completedToday.includes(lesson.id as number)) || lesson.isCompleted
                    const isNext = nextLesson?.id === lesson.id
                    return <div key={lesson.id ?? i} className={`flex items-center gap-3 rounded-[20px] border p-3 transition ${isNext ? "border-[#8988e6] bg-[#f0efff]" : "border-black/5 bg-[#fafafa]"}`}><span className={`grid size-10 shrink-0 place-items-center rounded-full ${done ? "bg-[#dcefd0] text-[#4e8a3f]" : isNext ? "bg-[#8584e6] text-white" : "bg-[#ececef] text-black/45"}`}>{done ? <Check className="size-4" /> : <BookOpen className="size-4" />}</span><div className="min-w-0 flex-1"><p className="truncate text-sm font-black">{lesson.title}</p><p className="mt-1 text-[10px] text-black/45">{tPlan(`lessonTypes.${lesson.lessonType}`)} · {lesson.estimatedMinutes} min</p></div>{lesson.id && !done && <Link href={`/lesson/${lesson.id}`} className="rounded-full bg-[#25282e] px-3 py-2 text-[10px] font-bold text-white">{t('startLesson')}</Link>}{done && <Check className="size-4 text-[#5c9b4c]" />}</div>
                  })}
                  {todayLessons.length === 0 && <div className="rounded-[20px] bg-[#f4f4f5] p-5 text-sm text-black/55">{t('startWithAssessment')}<div className="mt-4"><Link href="/assessment" className="inline-flex rounded-full bg-[#25282e] px-4 py-2.5 text-xs font-bold text-white">{tNav('assessment')}</Link></div></div>}
                </div>
                {hasPlan && <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-black/5 pt-4"><span className="text-xs text-black/50">{pendingCount} {t('pendingLessons')}</span><button type="button" onClick={skipDay} disabled={skipping} className="rounded-full border border-black/10 px-4 py-2.5 text-xs font-bold transition hover:bg-black/5 disabled:opacity-50">{skipping ? "…" : t('skipDay')}</button></div>}
                {skipError && <p className="mt-3 text-xs text-red-600">{tError('body')}</p>}
              </div>
            </section>

            <aside className="min-w-0 space-y-5">
              <div className="rounded-[28px] bg-white p-5 shadow-sm ring-1 ring-black/5">
                <div className="flex items-start justify-between gap-3"><div><h2 className="text-xl font-black leading-tight">{t('lessonReady')} 📚</h2><p className="mt-2 text-xs text-black/45">{t('completedToday', { completed: completedLessonCount, total: todayLessons.length || 0 })}</p></div><BookOpen className="size-6 text-[#d87822]" /></div>
                <div className="mt-5 grid grid-cols-5 gap-1.5">{["Mon","Tue","Wed","Thu","Fri"].map((day,i)=><div key={day} className="rounded-[16px] bg-[#f4f4f6] p-2 text-center"><span className="text-[9px] font-bold text-black/45">{day}</span><span className="mt-1 block text-sm font-black">{20+i}</span><span className={`mx-auto mt-2 block size-3 rounded-full ${i < completedLessonCount ? "bg-[#78bb65]" : "bg-[#efad68]"}`} /></div>)}</div>
              </div>

              <div className="rounded-[28px] bg-white p-5 shadow-sm ring-1 ring-black/5">
                <div className="mb-4 flex items-center justify-between"><h3 className="text-lg font-black tracking-tight">{t('recentPerformance')}</h3><Link href="/progress" aria-label={t('recentPerformance')} className="rounded-full px-2 py-1 text-lg leading-none text-black/45 hover:bg-black/5">•••</Link></div>
                <div className="h-28 overflow-hidden rounded-[20px] bg-[#f0f0f3] p-4"><div className="flex h-full items-end gap-2">{[.45,.62,.78,.58,.9,.72,.84].map((v,i)=><div key={i} className="flex-1 rounded-t-lg bg-[#9695e9]" style={{height:`${v*100}%`}} />)}</div></div>
                <div className="mt-3 flex items-center justify-between text-[10px] text-black/45"><span>{t('accuracy')}</span><span>{accuracy}%</span></div>
              </div>

              <div className="rounded-[26px] bg-[#8584e6] p-5 text-white">
                <div className="flex items-center justify-between gap-3"><div><p className="text-[10px] font-bold uppercase tracking-[.14em] text-white/70">{t('streak')}</p><p className="mt-1 text-xl font-black">{streak}</p></div><span className="grid size-11 place-items-center rounded-full bg-white/15"><Flame className="size-5" /></span></div>
                <p className="mt-3 text-xs leading-relaxed text-white/80">{t('recentPerformanceDescription')}</p>
              </div>

              <div className="rounded-[28px] bg-white p-5 shadow-sm ring-1 ring-black/5">
                <div className="mb-4 flex items-center justify-between"><h3 className="text-lg font-black tracking-tight">{tNav('resources')}</h3><span className="text-lg text-black/40">•••</span></div>
                <div className="grid grid-cols-2 gap-3">
                  <Link href="/reading" className="relative min-h-[142px] overflow-hidden rounded-[20px] bg-[#ffcf67] p-4 transition hover:-translate-y-0.5"><BookOpen className="size-7 text-[#9a5b16]" /><p className="absolute bottom-3 left-3 right-3 text-xs font-black leading-tight">{tNav('reading')}</p></Link>
                  <Link href="/courses" className="relative min-h-[142px] overflow-hidden rounded-[20px] bg-[#8584e6] p-4 text-white transition hover:-translate-y-0.5"><Library className="size-7" /><p className="absolute bottom-3 left-3 right-3 text-xs font-black leading-tight">{tNav('courses')}</p></Link>
                </div>
              </div>
            </aside>
          </div>

          {showPremiumBanner && <section className="mx-4 mb-5 rounded-[26px] border border-[#e7e5f4] bg-white p-5 sm:mx-7 sm:p-6"><div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between"><div className="flex gap-3"><span className="grid size-10 shrink-0 place-items-center rounded-full bg-[#ffcf67] text-sm">★</span><div><p className="text-xs font-black uppercase tracking-[.12em] text-black/45">{freemiumTrialActive ? t('freemiumTrialTitle', { days: freemiumTrialDaysLeft }) : t(paymentRecovery ? 'premiumBannerPastDueTitle' : 'premiumBannerTitle')}</p><p className="mt-2 max-w-2xl text-xs leading-relaxed text-black/50">{freemiumTrialActive ? t('freemiumTrialDesc', { days: freemiumTrialDaysLeft }) : paymentRecovery ? t('premiumBannerPastDueDesc') : t(trialEligible ? 'premiumBannerDesc' : 'premiumBannerDescTrialUsed')}</p></div></div>{!freemiumTrialActive && <span className="self-start rounded-full border border-[#7776df]/30 px-4 py-2 text-xs font-black text-[#5f5ec5]">{paymentRecovery ? t('premiumBannerPastDueCta') : t(trialEligible ? 'premiumBannerCta' : 'premiumBannerCtaTrialUsed')}</span>}</div>{!freemiumTrialActive && (paymentRecovery ? <div className="mt-4 border-t border-black/5 pt-4"><button onClick={handleManageSubscription} disabled={portalLoading} className="rounded-full bg-[#25282e] px-5 py-3 text-xs font-black text-white disabled:opacity-50">{portalLoading ? "…" : tBilling('updatePayment')}</button>{portalError && <p className="mt-3 text-xs text-red-500">{portalError}</p>}</div> : <SubscriptionPlanButtons className="mt-4 border-t border-black/5 pt-4" />)}</section>}

          <footer className="flex flex-wrap items-center gap-2 border-t border-black/5 bg-[#f3f3f2] px-5 py-5 sm:px-7">
            <Link href="/plan" className="rounded-full bg-[#25282e] px-5 py-3 text-xs font-bold text-white">{t('goToMyPlan')}</Link>
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
