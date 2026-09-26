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

      <div className="container-xl">
        <div className="page-header d-print-none">
          <div className="row align-items-center">
            <div className="col">
              <div className="page-pretitle">{activeLanguage ? tTarget(activeLanguage.code) : 'JUBA LISAN'}</div>
              <h2 className="page-title">{t('welcomeBack')}, {user?.displayName || user?.username}</h2>
            </div>
            <div className="col-auto ms-auto d-print-none">
              <button type="button" className="btn btn-outline-secondary" onClick={refreshDashboardData} disabled={refreshing}>
                <i className={`ti ti-refresh me-2 ${refreshing ? 'ti-spin' : ''}`} aria-hidden="true" />
                {t('refresh')}
              </button>
            </div>
          </div>
        </div>

        {loadError && (
          <div className="alert alert-danger" role="alert">
            <div>{tError('body')}</div>
            <button type="button" className="btn btn-sm btn-outline-danger mt-2" onClick={() => { setLoadError(false); setLoading(true); loadData() }}>
              {tError('retry')}
            </button>
          </div>
        )}

        <div className="row row-cards">
          <div className="col-12">
            <div className="card">
              <div className="card-body">
                <div className="row align-items-center">
                  <div className="col-auto">
                    <span className="avatar avatar-lg bg-primary-lt text-primary">
                      <i className="ti ti-school icon" aria-hidden="true" />
                    </span>
                  </div>
                  <div className="col">
                    <h3 className="card-title mb-1">{t('nextStep')}</h3>
                    <div className="text-secondary">
                      {cefrLevel ? cefrLevel + ' · ' : ''}{nextLesson?.title || t('startWithAssessment')}
                    </div>
                    <div className="mt-3 d-flex flex-wrap gap-2">
                      <Link href={nextLesson?.id ? '/lesson/' + nextLesson.id : '/assessment'} className="btn btn-primary">
                        <i className="ti ti-player-play me-2" aria-hidden="true" />
                        {nextLesson ? t('startLesson') : tNav('assessment')}
                      </Link>
                      <Link href="/plan" className="btn btn-outline-secondary">
                        {t('goToMyPlan')}
                      </Link>
                    </div>
                  </div>
                  <div className="col-auto d-none d-md-block">
                    <span className="badge bg-primary-lt text-primary">{streak} {t('streak')}</span>
                    <div className="text-secondary text-end mt-2">{xp} XP</div>
                  </div>
                </div>
              </div>
              <div className="card-footer">
                <div className="row text-center">
                  <div className="col"><div className="text-secondary">{t('lessonsCompleted')}</div><div className="h2 mb-0">{totalLessons}</div></div>
                  <div className="col"><div className="text-secondary">{t('accuracy')}</div><div className="h2 mb-0">{accuracy}%</div></div>
                  <div className="col"><div className="text-secondary">{t('streak')}</div><div className="h2 mb-0">{streak}</div></div>
                  <div className="col"><div className="text-secondary">{t('daysRemaining')}</div><div className="h2 mb-0">{Math.max(totalDays - progressDay, 0)}</div></div>
                </div>
              </div>
            </div>
          </div>

          <div className="col-lg-8">
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">{t('recentPerformance')}</h3>
                <div className="card-actions">
                  {(['week', 'month', 'all'] as const).map((range) => (
                    <button key={range} type="button" onClick={() => changeHistoryRange(range)} className={`btn btn-sm ${historyRange === range ? 'btn-primary' : 'btn-ghost-secondary'}`}>
                      {range}
                    </button>
                  ))}
                </div>
              </div>
              <div className="card-body">
                <div className="row row-cards">
                  <div className="col-sm-4">
                    <div className="subheader">{t('accuracy')}</div>
                    <div className="h1 mb-2">{accuracy}%</div>
                    <div className="progress progress-sm">
                      <div className="progress-bar" style={{ width: accuracy + '%' }} />
                    </div>
                    <div className="text-secondary mt-2">{getPerformanceLabel(accuracy / 100)}</div>
                  </div>
                  <div className="col-sm-8">
                    <div className="chart-placeholder border rounded p-3">
                      <div className="d-flex align-items-end gap-2" style={{ minHeight: 140 }}>
                        {performanceValues.length ? performanceValues.map((value, index) => (
                          <div key={index} className="flex-fill text-center">
                            <div className="bg-primary rounded-top" style={{ height: Math.max(8, Math.round(value * 1.2)), minHeight: 8 }} />
                            <div className="text-secondary small mt-1">{index + 1}</div>
                          </div>
                        )) : <div className="text-secondary">{t('noSkills')}</div>}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="card mt-3">
              <div className="card-header">
                <h3 className="card-title">{t('lessonReady')}</h3>
                <div className="card-actions"><span className="badge bg-blue-lt text-blue">{completedLessonCount}/{todayLessons.length || 0}</span></div>
              </div>
              <div className="list-group list-group-flush">
                {todayLessons.map((lesson) => {
                  const done = (lesson.id && completedToday.includes(lesson.id)) || lesson.isCompleted
                  return (
                    <div key={lesson.id ?? lesson.title} className="list-group-item">
                      <div className="row align-items-center">
                        <div className="col-auto"><span className={`avatar avatar-sm ${done ? 'bg-success-lt text-success' : 'bg-primary-lt text-primary'}`}><i className={`ti ${done ? 'ti-check' : 'ti-book'}`} aria-hidden="true" /></span></div>
                        <div className="col text-truncate">
                          <div className="text-reset">{lesson.title}</div>
                          <div className="text-secondary text-truncate">{tPlan('lessonTypes.' + lesson.lessonType)} · {lesson.estimatedMinutes} min</div>
                        </div>
                        <div className="col-auto">
                          {lesson.id && !done ? <Link href={'/lesson/' + lesson.id} className="btn btn-sm btn-primary">{t('startLesson')}</Link> : <span className="badge bg-success-lt text-success"><i className="ti ti-check me-1" />{t('completedToday', { completed: 1, total: 1 })}</span>}
                        </div>
                      </div>
                    </div>
                  )
                })}
                {todayLessons.length === 0 && (
                  <div className="empty">
                    <div className="empty-icon"><i className="ti ti-book-off" /></div>
                    <p className="empty-title">{t('startWithAssessment')}</p>
                    <Link href="/assessment" className="btn btn-primary">{tNav('assessment')}</Link>
                  </div>
                )}
              </div>
              {hasPlan && (
                <div className="card-footer d-flex justify-content-between align-items-center">
                  <span className="text-secondary">{pendingCount} {t('pendingLessons')}</span>
                  <button type="button" onClick={skipDay} disabled={skipping} className="btn btn-outline-secondary btn-sm">{skipping ? '…' : t('skipDay')}</button>
                </div>
              )}
              {skipError && <div className="card-footer text-danger">{tError('body')}</div>}
            </div>
          </div>

          <div className="col-lg-4">
            <div className="card">
              <div className="card-header"><h3 className="card-title">{t('lessonReady')}</h3></div>
              <div className="card-body">
                <div className="datagrid">
                  {progressBars.length ? progressBars.map(({ day, value, active }) => (
                    <div className="datagrid-item" key={day}><div className="datagrid-title">{day}</div><div className="datagrid-content"><span className={`badge ${active ? 'bg-success-lt text-success' : 'bg-primary-lt text-primary'}`}>{value} XP</span></div></div>
                  )) : <div className="text-secondary">{t('noSkills')}</div>}
                </div>
              </div>
            </div>

            <div className="card mt-3">
              <div className="card-header"><h3 className="card-title">{tNav('resources')}</h3></div>
              <div className="list-group list-group-flush">
                <Link href="/reading" className="list-group-item list-group-item-action"><i className="ti ti-book me-2" />{tNav('reading')}<span className="ms-auto"><i className="ti ti-chevron-right" /></span></Link>
                <Link href="/courses" className="list-group-item list-group-item-action"><i className="ti ti-school me-2" />{tNav('courses')}<span className="ms-auto"><i className="ti ti-chevron-right" /></span></Link>
                <Link href="/flashcards" className="list-group-item list-group-item-action"><i className="ti ti-cards me-2" />{tNav('flashcards')}<span className="ms-auto"><i className="ti ti-chevron-right" /></span></Link>
                <Link href="/chat" className="list-group-item list-group-item-action"><i className="ti ti-message me-2" />{tNav('tutor')}<span className="ms-auto"><i className="ti ti-chevron-right" /></span></Link>
              </div>
            </div>

            <div className="card mt-3">
              <div className="card-header"><h3 className="card-title">{t('vocabularyProgress', { level: vocabularyLevel || '—' })}</h3></div>
              <div className="card-body">
                <div className="d-flex justify-content-between mb-2"><span className="text-secondary">{t('vocabularyWords', { mastered: vocabularyMastered, total: vocabularyTotal })}</span><span>{vocabularyProgressPct}%</span></div>
                <div className="progress"><div className="progress-bar bg-success" style={{ width: vocabularyProgressPct + '%' }} /></div>
              </div>
            </div>
          </div>

          {showPremiumBanner && (
            <div className="col-12">
              <div className="card">
                <div className="card-status-start bg-warning" />
                <div className="card-body">
                  <div className="row align-items-center">
                    <div className="col-auto"><span className="avatar bg-warning-lt text-warning"><i className="ti ti-star" /></span></div>
                    <div className="col">
                      <h3 className="card-title">{freemiumTrialActive ? t('freemiumTrialTitle', { days: freemiumTrialDaysLeft }) : t(paymentRecovery ? 'premiumBannerPastDueTitle' : 'premiumBannerTitle')}</h3>
                      <div className="text-secondary">{freemiumTrialActive ? t('freemiumTrialDesc', { days: freemiumTrialDaysLeft }) : paymentRecovery ? t('premiumBannerPastDueDesc') : t(trialEligible ? 'premiumBannerDesc' : 'premiumBannerDescTrialUsed')}</div>
                    </div>
                    <div className="col-auto">
                      {paymentRecovery ? <button onClick={handleManageSubscription} disabled={portalLoading} className="btn btn-warning">{portalLoading ? '…' : tBilling('updatePayment')}</button> : !freemiumTrialActive ? <SubscriptionPlanButtons /> : null}
                    </div>
                  </div>
                  {portalError && <div className="text-danger mt-3">{portalError}</div>}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
