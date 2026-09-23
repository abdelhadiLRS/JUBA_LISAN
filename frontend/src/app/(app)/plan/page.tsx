'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { PageLoading } from '@/components/ui/page-loading'
import { apiFetch } from '@/lib/api'
import { getCurriculumUnits, type CurriculumUnit } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
import { useLearningProgressSync } from '@/hooks/use-learning-progress'
import UnitCard from '@/components/plan/UnitCard'
import UnitDrawer from '@/components/plan/UnitDrawer'
import LevelTestBanner from '@/components/plan/LevelTestBanner'
import NoPlanBanner from '@/components/plan/NoPlanBanner'
import type { CEFRLevel } from '@/data/grammar'

// ── Types ──────────────────────────────────────────────────────────────────────

interface PendingLesson {
  id: number
  title: string
  lesson_type: string
  week_number: number
  day_number: number
}

interface PlanLesson extends PendingLesson {
  unit_id: string | null
  is_completed: boolean
}

interface TodayLesson {
  id: number | null
  title: string
  lesson_type: string
  week: number
  day: number
  unit_id?: string
  is_completed?: boolean
}

type LessonAction = 'start' | 'continue' | 'review'

interface Lesson {
  id: number | null
  title: string
  lesson_type: string
  week: number
  day: number
  unit_id?: string
  completed?: boolean
  action?: LessonAction
}

interface StudyPlan {
  id: number
  cefr_level: string
  duration_weeks: number
  days_per_week: number
  current_unit: string
  completion_test_taken: boolean
  completion_test_score: number | null
  completion_test_recommendation: string | null
  generated_plan: {
    weekly_plan: {
      week: number
      days: {
        day: number
        title: string
        lesson_type: string
        unit_id: string
      }[]
    }[]
  }
}

interface CompetencyMap {
  [unitId: string]: number // 0–1
}

interface LearningJourneyResponse {
  next_lesson_id: number | null
  next_unit_id: string | null
  sections: {
    units: {
      id: string
      progress: number
      state: string
      lessons: {
        id: number | null
        state: string
        is_completed: boolean
      }[]
    }[]
  }[]
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function flattenLessons(plan: StudyPlan): Lesson[] {
  const result: Lesson[] = []
  for (const week of plan.generated_plan.weekly_plan) {
    for (const day of week.days) {
      result.push({
        id: null,
        title: day.title,
        lesson_type: day.lesson_type,
        week: week.week,
        day: day.day,
        unit_id: day.unit_id,
        completed: false,
      })
    }
  }
  return result
}

function lessonsByUnit(lessons: Lesson[]): Record<string, Lesson[]> {
  const map: Record<string, Lesson[]> = {}
  for (const l of lessons) {
    const key = l.unit_id ?? '__unassigned'
    if (!map[key]) map[key] = []
    map[key].push(l)
  }
  return map
}

function lessonKey(week: number, day: number, title: string): string {
  return `${week}:${day}:${title}`
}

async function readJsonOrNull<T>(response: Response | null): Promise<T | null> {
  if (!response?.ok) return null
  try {
    return (await response.json()) as T
  } catch {
    return null
  }
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function PlanPage() {
  const t = useTranslations('plan')
  const router = useRouter()
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const langName = activeLanguage?.name ?? ''

  const [plan, setPlan] = useState<StudyPlan | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [competencies, setCompetencies] = useState<CompetencyMap>({})
  const [activeDrawer, setActiveDrawer] = useState<CurriculumUnit | null>(null)
  const [activeLessonId, setActiveLessonId] = useState<number | null>(null)
  const [pendingLessons, setPendingLessons] = useState<PendingLesson[]>([])
  const [lessonStates, setLessonStates] = useState<
    Record<string, Pick<Lesson, 'id' | 'completed' | 'action'>>
  >({})
  const [units, setUnits] = useState<CurriculumUnit[]>([])
  const loadRequestRef = useRef(0)

  const loadPlan = useCallback(async () => {
    const requestId = ++loadRequestRef.current
    let cancelled = false
    setLoading(true)
    setError('')
    setPendingLessons([])
    setLessonStates({})
    setActiveLessonId(null)
    setCompetencies({})
    try {
      const [planRes, journeyRes, compRes, todayRes, pendingRes, lessonsRes] =
        await Promise.all([
          apiFetch('/api/study-plan/current'),
          apiFetch('/api/study-plan/learning-path').catch(() => null),
          apiFetch('/api/progress/competencies').catch(() => null),
          apiFetch('/api/study-plan/today').catch(() => null),
          apiFetch('/api/study-plan/pending-lessons').catch(() => null),
          apiFetch('/api/study-plan/lessons').catch(() => null),
        ])

      if (cancelled || requestId !== loadRequestRef.current) return

      if (!planRes.ok) {
        if (planRes.status === 404) {
          if (!cancelled && requestId === loadRequestRef.current) {
            router.push('/assessment')
          }
          return
        }
        throw new Error(`Failed to load plan (${planRes.status})`)
      }

      const [planData, journey, compData, todayData, pendingData, generatedLessons] = await Promise.all([
        readJsonOrNull<StudyPlan>(planRes),
        readJsonOrNull<LearningJourneyResponse>(journeyRes),
        readJsonOrNull<unknown>(compRes),
        readJsonOrNull<{ lessons: TodayLesson[] }>(todayRes),
        readJsonOrNull<PendingLesson[]>(pendingRes),
        readJsonOrNull<PlanLesson[]>(lessonsRes),
      ])

      if (!planData) {
        throw new Error('Failed to parse learning plan') 
      }

      if (cancelled || requestId !== loadRequestRef.current) return

      let competencySnapshot: CompetencyMap = {}
      let nextLessonId: number | null = null

      if (journey) {
        nextLessonId = journey.next_lesson_id
        for (const section of journey.sections) {
          for (const unit of section.units) {
            competencySnapshot[unit.id] = unit.progress
          }
        }
      }

      if (Object.keys(competencySnapshot).length === 0) {
        if (Array.isArray(compData)) {
          for (const item of compData as { unit_id: string; score: number }[]) {
            competencySnapshot[item.unit_id] = item.score
          }
        } else if (compData && typeof compData === 'object') {
          competencySnapshot = compData as CompetencyMap
        }
      }

      const states: Record<
        string,
        Pick<Lesson, 'id' | 'completed' | 'action'>
      > = {}

      if (generatedLessons) {
        for (const lesson of generatedLessons) {
          states[lessonKey(lesson.week_number, lesson.day_number, lesson.title)] = {
            id: lesson.id,
            completed: lesson.is_completed,
            action: lesson.is_completed ? 'review' : undefined,
          }
        }
      }

      if (pendingData) {
        for (const lesson of pendingData) {
          states[lessonKey(lesson.week_number, lesson.day_number, lesson.title)] = {
            id: lesson.id,
            completed: false,
            action: 'continue',
          }
        }
      }

      if (todayData) {
        const nextLesson = todayData.lessons.find(
          (l) => l.id != null && !l.is_completed,
        )
        nextLessonId = nextLesson?.id ?? null
        for (const lesson of todayData.lessons) {
          if (lesson.id == null) continue
          states[lessonKey(lesson.week, lesson.day, lesson.title)] = {
            id: lesson.id,
            completed: lesson.is_completed ?? false,
            action: lesson.is_completed ? 'review' : 'start',
          }
        }
      }

      if (cancelled || requestId !== loadRequestRef.current) return

      setPlan(planData)
      setCompetencies(competencySnapshot)
      setActiveLessonId(nextLessonId)
      setPendingLessons(pendingData ?? [])
      setActiveLessonId(nextLessonId)
      setLessonStates(states)
    } catch (err) {
      if (!cancelled && requestId === loadRequestRef.current) setError(err instanceof Error ? err.message : 'Failed to load')
    } finally {
      if (!cancelled && requestId === loadRequestRef.current) setLoading(false)
    }
    // The effect owns cancellation through loadRequestRef; do not return a cleanup
    // function from the async loader itself.
  }, [router, activeLanguage?.code])

  useEffect(() => {
    void loadPlan()
    return () => {
      loadRequestRef.current += 1
    }
  }, [loadPlan])

  useLearningProgressSync(() => loadPlan(), { refreshOnPageShow: false, refreshOnVisibility: false })

  const launchLesson = useCallback(
    async (lessonId: number) => {
      try {
        const response = await apiFetch('/api/study-plan/launch-lesson', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ lesson_id: lessonId }),
        })
        if (!response.ok) {
          if (response.status === 409) {
            setError(t('lessonLocked'))
            return
          }
          throw new Error(`Failed to launch lesson (${response.status})`)
        }
        router.push(`/lesson/${lessonId}`)
      } catch (err) {
        setError(err instanceof Error ? err.message : t('lessonLaunchFailed'))
      }
    },
    [router, t],
  )

  useEffect(() => {
    let cancelled = false
    if (plan?.cefr_level && activeLanguage?.code) {
      getCurriculumUnits(plan.cefr_level, activeLanguage.code)
        .then((nextUnits) => { if (!cancelled) setUnits(nextUnits) })
        .catch(() => { if (!cancelled) setUnits([]) })
    } else {
      setUnits([])
    }
    return () => { cancelled = true }
  }, [plan?.cefr_level, activeLanguage?.code])

  if (loading) {
    return <PageLoading />
  }

  if (error || !plan) {
    return <NoPlanBanner />
  }

  const level = plan.cefr_level as CEFRLevel
  const allLessons = flattenLessons(plan).map((lesson) => ({
    ...lesson,
    ...lessonStates[lessonKey(lesson.week, lesson.day, lesson.title)],
  }))
  const byUnit = lessonsByUnit(allLessons)
  const currentUnitId = plan.current_unit

  const allUnitsCompleted =
    units.length > 0 && units.every((u) => (competencies[u.id] ?? 0) >= 0.8)

  return (
    <div className="mx-auto max-w-4xl space-y-6 px-4 py-8">
      {/* ── Header ── */}
      <div className="border-fl-border bg-fl-surface rounded-2xl border p-5 sm:p-6">
        <p className="text-fl-muted-2 mb-3 text-xs font-semibold tracking-wide uppercase">
          {t('learningRoadmap')}
        </p>
        <div className="flex flex-wrap items-center gap-x-8 gap-y-4">
          <div>
            <p className="text-fl-muted-3 text-xs font-medium">
              {langName ? `${langName} — ${t('level')}` : t('level')}
            </p>
            <p
              className="text-3xl font-black tracking-tight"
              style={{ color: 'var(--juba-primary)' }}
            >
              {level}
            </p>
          </div>
          <div>
            <p className="text-fl-muted-3 text-xs font-medium">
              {t('duration')}
            </p>
            <p className="text-fl-muted-1 text-sm font-medium">
              {t('durationDetail', {
                weeks: plan.duration_weeks,
                days: plan.days_per_week,
              })}
            </p>
          </div>
          <div>
            <p className="text-fl-muted-3 text-xs font-medium">
              {t('unitsLabel')}
            </p>
            <p className="text-fl-muted-1 text-sm font-semibold">
              {units.length}
            </p>
          </div>
        </div>
      </div>

      {/* ── Pending lessons ── */}
      {pendingLessons.length > 0 && (
        <div
          className="rounded-2xl border p-5"
          style={{
            borderColor:
              'color-mix(in srgb, var(--juba-warm) 40%, var(--juba-border))',
            background: 'var(--juba-warm-soft)',
          }}
        >
          <p
            className="mb-3 text-xs font-bold tracking-wide uppercase"
            style={{ color: 'var(--juba-warm)' }}
          >
            {pendingLessons.length} {t('pendingLessons')}
          </p>
          <div className="space-y-2">
            {pendingLessons.map((lesson) => (
              <div
                key={lesson.id}
                className="border-fl-border bg-fl-surface flex items-center justify-between gap-3 rounded-xl border px-4 py-3"
              >
                <div className="min-w-0">
                  <p className="text-fl-fg truncate text-sm font-medium">
                    {lesson.title}
                  </p>
                  <p className="text-fl-muted-3 mt-0.5 text-xs">
                    W{lesson.week_number} D{lesson.day_number} ·{' '}
                    {lesson.lesson_type}
                  </p>
                </div>
                <button
                  onClick={() => void launchLesson(lesson.id)}
                  className="shrink-0 rounded-lg bg-[var(--juba-primary)] px-3 py-1.5 text-xs font-semibold text-white transition-colors hover:bg-[var(--juba-primary-dark)]"
                >
                  {t('resume')}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Unit list ── */}
      <div className="space-y-2">
        {units.length === 0 && (
          <div className="border-fl-border bg-fl-surface space-y-2 rounded-2xl border px-6 py-10 text-center">
            <p className="text-fl-muted-2 text-sm font-medium">
              {t('noUnitsForLevel', { level })}
            </p>
            <p className="text-fl-muted-4 text-xs">{t('noUnitsDesc')}</p>
          </div>
        )}
        {units.map((unit, i) => {
          const unitLessons = byUnit[unit.id] ?? []
          const completedLessons = unitLessons.filter((l) => l.completed).length
          const isActive = unit.id === currentUnitId
          const unitComp = competencies[unit.id] ?? 0
          const isCompleted =
            unitComp >= 0.8 ||
            (completedLessons > 0 && completedLessons === unitLessons.length)

          // A unit is locked if its prerequisite is not completed
          const prereqUnit = unit.prerequisite_unit
          const prereqCompleted = prereqUnit
            ? (competencies[prereqUnit] ?? 0) >= 0.8
            : true
          const isLocked =
            !isActive && !isCompleted && !prereqCompleted && i > 0

          return (
            <UnitCard
              key={unit.id}
              title={unit.title}
              index={i}
              lessonCount={unitLessons.length || unit.lesson_types.length}
              grammarCount={unit.grammar_points.length}
              competency={unitComp}
              status={{
                completed: isCompleted,
                active: isActive,
                locked: isLocked,
                isLevelTest: false,
              }}
              onClick={() => setActiveDrawer(unit)}
              onStartLesson={
                isActive && activeLessonId != null
                  ? () => void launchLesson(activeLessonId)
                  : undefined
              }
            />
          )
        })}

        {/* Level test pseudo-unit */}
        {units.length > 0 && (
          <UnitCard
            title={t('completionTestTitle', { level })}
            index={units.length}
            lessonCount={1}
            grammarCount={0}
            competency={
              plan.completion_test_score != null
                ? plan.completion_test_score
                : 0
            }
            status={{
              completed: plan.completion_test_taken,
              active: allUnitsCompleted && !plan.completion_test_taken,
              locked: !allUnitsCompleted,
              isLevelTest: true,
            }}
            onClick={() => {
              if (allUnitsCompleted && !plan.completion_test_taken) {
                router.push(`/assessment/level-test?plan=${plan.id}`)
              }
            }}
          />
        )}
      </div>

      {/* ── Level test banner ── */}
      {allUnitsCompleted && !plan.completion_test_taken && (
        <LevelTestBanner planId={plan.id} level={level} />
      )}

      {/* ── Completion test result ── */}
      {plan.completion_test_taken && (
        <div className="border-fl-border bg-fl-surface space-y-2 rounded-2xl border px-5 py-5 sm:px-6">
          <p className="text-fl-muted-3 text-xs font-semibold tracking-wide uppercase">
            {t('levelTestResult')}
          </p>
          <p className="text-fl-fg text-sm">
            {t('testScore')}{' '}
            <span className="font-bold">
              {plan.completion_test_score != null
                ? `${Math.round(plan.completion_test_score * 100)}%`
                : 'n/a'}
            </span>
          </p>
          {plan.completion_test_recommendation && (
            <p className="text-fl-muted-1 text-sm">
              {plan.completion_test_recommendation}
            </p>
          )}
        </div>
      )}

      {/* ── Active drawer ── */}
      {activeDrawer && (
        <UnitDrawer
          unit={activeDrawer}
          lessons={(byUnit[activeDrawer.id] ?? []).map((l) => ({
            ...l,
            completed: l.completed ?? false,
          }))}
          onClose={() => setActiveDrawer(null)}
          onStartLesson={(lessonId) => {
            setActiveDrawer(null)
            void launchLesson(lessonId)
          }}
        />
      )}
    </div>
  )
}async function readJsonOrNull<T>(response: Response | null): Promise<T | null> {
  if (!response?.ok) return null
  try {
    return (await response.json()) as T
  } catch {
    return null
  }
}


