'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { BookOpen, Flame, Sparkles, Target } from 'lucide-react'
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
      <div className="flex min-h-screen flex-col items-center justify-center gap-4">
        <p className="text-fl-muted-2 text-sm">{tError('body')}</p>
        <button
          onClick={() => {
            setLoadError(false)
            setLoading(true)
            loadData()
          }}
          className="text-fl-accent text-sm font-medium underline transition-all hover:no-underline"
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
  const planCompletion =
    hasPlan && totalDays > 0
      ? Math.min(100, Math.round((progressDay / totalDays) * 100))
      : 0
  const daysRemaining = hasPlan ? Math.max(totalDays - progressDay, 0) : 0
  const vocabularyProgressPct = Math.round(vocabularyProgress * 100)
  const paymentRecovery = needsPaymentRecovery(user)
  const showPremiumBanner = stripeEnabled && !isSubscribed(user, stripeEnabled)

  function getPerformanceLabel(value: number) {
    if (value < 0.5) return t('performanceNeedsPractice')
    if (value < 0.8) return t('performanceInProgress')
    return t('performanceStrong')
  }

  const stats = [
    {
      label: t('streak'),
      value: `${streak}d`,
      Icon: Flame,
      highlight: streak > 0,
    },
    { label: t('xp'), value: xp, Icon: Sparkles, highlight: false },
    {
      label: t('lessonsCompleted'),
      value: totalLessons,
      Icon: BookOpen,
      highlight: false,
    },
    {
      label: t('accuracy'),
      value: totalExercises > 0 ? `${Math.round(accuracy * 100)}%` : '—',
      Icon: Target,
      highlight: false,
      detail:
        totalExercises > 0
          ? t('exerciseStats', {
              correct: exercisesCorrect,
              total: totalExercises,
            })
          : t('noExercisesYet'),
    },
  ]

  return (
    <>
      <OnboardingTour />
      <WhatsNew />
      <div className="mx-auto max-w-5xl px-4 py-6 sm:px-6 md:py-8">
        {/* Header */}
        <div className="mb-6">
          <p className="text-fl-muted-2 mb-1 text-sm">{t('welcomeBack')}</p>
          <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-end">
            <div>
              <h1 className="text-fl-fg text-2xl font-bold tracking-tight sm:text-3xl">
                {user?.displayName || user?.username}
              </h1>
              {activeLanguage && (
                <p className="text-fl-muted-1 mt-1 text-sm">
                  {tTarget(activeLanguage.code)}
                  {cefrLevel ? ` · ${cefrLevel}` : ''}
                </p>
              )}
            </div>
            {hasPlan && totalDays > 0 && (
              <p className="text-fl-muted-2 text-sm font-medium">
                {t('dayProgress', {
                  current: Math.min(progressDay + 1, totalDays),
                  total: totalDays,
                })}
              </p>
            )}
          </div>
        </div>

        <DashboardAnnouncement />

        {/* Next step — hero card */}
        <section
          className="juba-card mb-6 p-5 sm:p-6"
          aria-label={t('nextStep')}
        >
          <p className="text-fl-muted-2 mb-4 text-xs font-semibold tracking-wide uppercase">
            {t('nextStep')}
          </p>
          {!hasPlan ? (
            <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h2 className="text-fl-fg text-xl font-bold tracking-tight">
                  {t('startWithAssessment')}
                </h2>
                <p className="text-fl-muted-2 mt-2 max-w-xl text-sm">
                  {t('assessmentCreatesPlan')}
                </p>
              </div>
              <Link href="/assessment">
                <button
                  className={`${btnPrimary} bg-[var(--juba-primary)] hover:bg-[var(--juba-primary-dark)]`}
                >
                  {t('takeAssessmentArrow')}
                </button>
              </Link>
            </div>
          ) : nextLesson ? (
            <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <p className="text-fl-muted-3 mb-2 text-xs font-medium tracking-wide uppercase">
                  {t('lessonReady')}
                </p>
                <h2 className="text-fl-fg text-xl font-bold tracking-tight">
                  {nextLesson.title}
                </h2>
                <p className="text-fl-muted-2 mt-2 text-sm">
                  {tPlan(`lessonTypes.${nextLesson.lessonType}`)} ·{' '}
                  {nextLesson.estimatedMinutes}min
                </p>
              </div>
              <Link href={`/lesson/${nextLesson.id}`}>
                <button
                  className={`${btnPrimary} bg-[var(--juba-primary)] hover:bg-[var(--juba-primary-dark)]`}
                >
                  {t('startLesson')}
                </button>
              </Link>
            </div>
          ) : (
            <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h2 className="text-fl-fg text-xl font-bold tracking-tight">
                  {t('allCaughtUp')}
                </h2>
                <p className="text-fl-muted-2 mt-2 text-sm">
                  {pendingCount > 0
                    ? t('pendingStillAvailable', { count: pendingCount })
                    : t('noPendingToday')}
                </p>
              </div>
              <Link href="/plan">
                <button className={btnSecondary}>{t('goToMyPlan')}</button>
              </Link>
            </div>
          )}
        </section>

        {/* Stats row */}
        <div className="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
          {stats.map((stat) => (
            <div
              key={stat.label}
              className="border-fl-border bg-fl-surface rounded-2xl border p-4 sm:p-5"
            >
              <div className="mb-2 flex items-center gap-2">
                <span
                  className={`flex h-7 w-7 items-center justify-center rounded-lg ${
                    stat.highlight
                      ? 'bg-[var(--juba-warm-soft)] text-[var(--juba-warm)]'
                      : 'bg-[var(--juba-primary-soft)] text-[var(--juba-primary)]'
                  }`}
                >
                  <stat.Icon className="h-4 w-4" aria-hidden="true" />
                </span>
                <p className="text-fl-muted-2 truncate text-xs font-medium">
                  {stat.label}
                </p>
              </div>
              <p
                className={`text-2xl font-bold tracking-tight sm:text-3xl ${
                  stat.highlight ? 'text-[var(--juba-warm)]' : 'text-fl-fg'
                }`}
              >
                {stat.value}
              </p>
              {'detail' in stat && stat.detail && (
                <p className="text-fl-muted-3 mt-1 text-xs">{stat.detail}</p>
              )}
            </div>
          ))}
        </div>

        <div className="mb-6 grid gap-4 lg:grid-cols-2">
          {/* Plan progress */}
          <section
            className="border-fl-border bg-fl-surface rounded-2xl border p-5"
            aria-label={t('planProgress')}
          >
            <div className="mb-4 flex items-center justify-between gap-4">
              <h3 className="text-fl-fg text-sm font-semibold">
                {t('planProgress')}
              </h3>
              {hasPlan && totalDays > 0 && (
                <span className="text-fl-muted-2 text-sm font-semibold">
                  {planCompletion}%
                </span>
              )}
            </div>
            {hasPlan && totalDays > 0 ? (
              <>
                <div className="bg-fl-surface-2 mb-4 h-2 w-full overflow-hidden rounded-full">
                  <div
                    className="h-full rounded-full transition-all duration-500"
                    style={{
                      width: `${planCompletion}%`,
                      background: 'var(--juba-primary)',
                    }}
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-fl-surface-2 rounded-xl p-3">
                    <p className="text-fl-muted-2 mb-1 text-xs font-medium">
                      {t('currentDay')}
                    </p>
                    <p className="text-fl-fg text-lg font-bold">
                      {Math.min(progressDay + 1, totalDays)} / {totalDays}
                    </p>
                  </div>
                  <div className="bg-fl-surface-2 rounded-xl p-3">
                    <p className="text-fl-muted-2 mb-1 text-xs font-medium">
                      {t('daysRemaining')}
                    </p>
                    <p className="text-fl-fg text-lg font-bold">
                      {daysRemaining}
                    </p>
                  </div>
                </div>
                {vocabularyTotal > 0 && (
                  <div className="mt-5">
                    <div className="flex items-center justify-between gap-3">
                      <p className="text-fl-muted-2 text-xs font-medium">
                        {t('vocabularyProgress', {
                          level: vocabularyLevel ?? cefrLevel ?? '',
                        })}
                      </p>
                      <p className="text-fl-muted-1 text-xs font-semibold">
                        {vocabularyProgressPct}%
                      </p>
                    </div>
                    <p className="text-fl-muted-3 mt-1 text-xs">
                      {t('vocabularyWords', {
                        mastered: vocabularyMastered,
                        total: vocabularyTotal,
                      })}
                    </p>
                    <div className="bg-fl-surface-2 mt-2 h-2 w-full overflow-hidden rounded-full">
                      <div
                        className="h-full rounded-full transition-all duration-500"
                        style={{
                          width: `${vocabularyProgressPct}%`,
                          background: 'var(--juba-primary)',
                        }}
                      />
                    </div>
                  </div>
                )}
              </>
            ) : (
              <p className="text-fl-muted-2 text-sm">
                {t('startWithAssessment')}
              </p>
            )}
          </section>

          {/* Today's lessons */}
          <section
            className="border-fl-border bg-fl-surface rounded-2xl border p-5"
            aria-label={t('today')}
          >
            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-fl-fg text-sm font-semibold">{t('today')}</h3>
              {todayLessons.length > 0 && (
                <span className="text-fl-muted-3 text-xs font-medium">
                  {t('completedToday', {
                    completed: completedLessonCount,
                    total: todayLessons.length,
                  })}
                </span>
              )}
            </div>

            {todayLessons.length > 0 ? (
              <div className="space-y-2">
                {todayLessons.map((lesson, i) => {
                  const isDone =
                    (lesson.id && completedToday.includes(lesson.id)) ||
                    lesson.isCompleted
                  const isNext = nextLesson?.id === lesson.id

                  return (
                    <div
                      key={i}
                      className={`rounded-xl border px-4 py-3 transition-colors ${
                        isNext
                          ? 'border-[color-mix(in_srgb,var(--juba-primary)_45%,var(--juba-border))] bg-[var(--juba-primary-soft)]'
                          : 'border-fl-border'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-3">
                        <div className="min-w-0">
                          <p className="text-fl-fg truncate text-sm font-medium">
                            {lesson.title}
                          </p>
                          <p className="text-fl-muted-2 mt-0.5 text-xs">
                            {tPlan(`lessonTypes.${lesson.lessonType}`)} ·{' '}
                            {lesson.estimatedMinutes}min
                          </p>
                        </div>
                        {isDone ? (
                          <span className="text-fl-muted-2 shrink-0 text-xs font-medium">
                            ✓ {t('lessonDone')}
                          </span>
                        ) : lesson.id ? (
                          <Link
                            href={`/lesson/${lesson.id}`}
                            className="shrink-0"
                          >
                            <button
                              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                                isNext
                                  ? 'bg-[var(--juba-primary)] text-white hover:bg-[var(--juba-primary-dark)]'
                                  : 'border-fl-border text-fl-fg border hover:bg-[var(--juba-surface-soft)]'
                              }`}
                            >
                              {t('startLesson')}
                            </button>
                          </Link>
                        ) : null}
                      </div>
                    </div>
                  )
                })}
                <div className="pt-1">
                  <button
                    onClick={skipDay}
                    disabled={skipping}
                    className="text-fl-muted-3 hover:text-fl-muted-1 text-xs font-medium transition-colors disabled:opacity-40"
                  >
                    {skipping ? '...' : t('skipDay')}
                  </button>
                  {skipError && (
                    <p className="text-fl-error mt-1 text-xs">
                      {tError('title')}
                    </p>
                  )}
                </div>
              </div>
            ) : (
              <div className="space-y-3">
                <p className="text-fl-muted-2 text-sm">
                  {hasPlan ? t('allCaughtUp') : t('startWithAssessment')}
                </p>
                {!hasPlan && (
                  <Link href="/assessment">
                    <button
                      className={`${btnPrimary} bg-[var(--juba-primary)] hover:bg-[var(--juba-primary-dark)]`}
                    >
                      {t('takeAssessmentArrow')}
                    </button>
                  </Link>
                )}
              </div>
            )}
          </section>

          {/* Recent performance */}
          <section
            className="border-fl-border bg-fl-surface rounded-2xl border p-5 lg:col-span-2"
            aria-label={t('recentPerformance')}
          >
            <div className="mb-4">
              <h3 className="text-fl-fg text-sm font-semibold">
                {t('recentPerformance')}
              </h3>
              <p className="text-fl-muted-3 mt-1 text-xs">
                {t('recentPerformanceDescription')}
              </p>
            </div>
            {skillEntries.length > 0 ? (
              <div className="grid gap-x-8 gap-y-4 sm:grid-cols-2">
                {skillEntries.map(({ skill, value }) => (
                  <div key={skill}>
                    <div className="mb-1.5 flex items-center justify-between gap-2">
                      <span className="text-fl-muted-1 truncate text-xs font-medium">
                        {tPlan(`lessonTypes.${skill}`)}
                      </span>
                      <span className="text-fl-muted-2 shrink-0 text-xs font-semibold">
                        {getPerformanceLabel(value)} · {Math.round(value * 100)}
                        %
                      </span>
                    </div>
                    <div className="bg-fl-surface-2 h-2 w-full overflow-hidden rounded-full">
                      <div
                        className="h-full rounded-full transition-all duration-500"
                        style={{
                          width: `${value * 100}%`,
                          background:
                            value < 0.5
                              ? 'var(--juba-warm)'
                              : 'var(--juba-primary)',
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-fl-muted-2 text-sm">{t('noSkills')}</p>
            )}
          </section>
        </div>

        {showPremiumBanner && (
          <div className="border-fl-border bg-fl-surface mb-6 rounded-2xl border p-5">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div className="flex gap-3">
                <span
                  className="mt-0.5 text-sm leading-none"
                  style={{ color: 'var(--juba-warm)' }}
                  aria-hidden="true"
                >
                  ★
                </span>
                <div>
                  <p className="text-fl-fg mb-1 text-sm font-semibold">
                    {freemiumTrialActive
                      ? t('freemiumTrialTitle', { days: freemiumTrialDaysLeft })
                      : t(
                          paymentRecovery
                            ? 'premiumBannerPastDueTitle'
                            : 'premiumBannerTitle'
                        )}
                  </p>
                  <p className="text-fl-muted-2 text-sm leading-relaxed">
                    {freemiumTrialActive
                      ? t('freemiumTrialDesc', { days: freemiumTrialDaysLeft })
                      : paymentRecovery
                        ? t('premiumBannerPastDueDesc')
                        : t(
                            trialEligible
                              ? 'premiumBannerDesc'
                              : 'premiumBannerDescTrialUsed'
                          )}
                  </p>
                </div>
              </div>
              {!freemiumTrialActive && (
                <span
                  className="shrink-0 rounded-full px-3 py-1.5 text-xs font-semibold whitespace-nowrap"
                  style={{
                    color: 'var(--juba-warm)',
                    background: 'var(--juba-warm-soft)',
                  }}
                >
                  {paymentRecovery
                    ? t('premiumBannerPastDueCta')
                    : t(
                        trialEligible
                          ? 'premiumBannerCta'
                          : 'premiumBannerCtaTrialUsed'
                      )}
                </span>
              )}
            </div>
            {!freemiumTrialActive &&
              (paymentRecovery ? (
                <div className="border-fl-border mt-4 border-t pt-4">
                  <button
                    onClick={handleManageSubscription}
                    disabled={portalLoading}
                    className={`${btnPrimary} bg-[var(--juba-primary)] hover:bg-[var(--juba-primary-dark)] sm:w-auto`}
                  >
                    {portalLoading ? '...' : tBilling('updatePayment')}
                  </button>
                  {portalError && (
                    <p className="mt-3 text-xs text-[var(--juba-danger)]">
                      {portalError}
                    </p>
                  )}
                </div>
              ) : (
                <SubscriptionPlanButtons className="border-fl-border mt-4 border-t pt-4" />
              ))}
          </div>
        )}

        {/* Quick actions */}
        <div className="flex flex-wrap gap-2">
          {hasPlan && (
            <Link href="/plan">
              <button
                className={`${btnPrimary} bg-[var(--juba-primary)] hover:bg-[var(--juba-primary-dark)]`}
              >
                {t('goToMyPlan')}
              </button>
            </Link>
          )}
          {pendingCount > 0 && (
            <Link href="/plan">
              <button
                className="rounded-xl border px-4 py-2.5 text-sm font-medium transition-colors"
                style={{
                  borderColor:
                    'color-mix(in srgb, var(--juba-primary) 45%, var(--juba-border))',
                  color: 'var(--juba-primary-dark)',
                }}
              >
                {pendingCount} {t('pendingLessons')} →
              </button>
            </Link>
          )}
          <Link href="/flashcards">
            <button className={btnSecondary}>{tNav('flashcards')}</button>
          </Link>
          <Link href="/chat">
            <button className={btnSecondary}>{tNav('tutor')}</button>
          </Link>
          <Link href="/assessment">
            <button className={btnSecondary}>{tNav('assessment')}</button>
          </Link>
        </div>
      </div>
    </>
  )
}
