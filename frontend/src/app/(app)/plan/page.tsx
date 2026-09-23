'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { PageLoading } from '@/components/ui/page-loading'
import { apiFetch } from '@/lib/api'
import { getCurriculumUnits, type CurriculumUnit } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
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

  const loadPlan = useCallback(async () => {
    setLoading(true)
    setError('')
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

      if (!planRes.ok) {
        if (planRes.status === 404) {
          router.push('/assessment')
          return
        }
        throw new Error(`Failed to load plan (${planRes.status})`)
      }

      const planData = (await planRes.json()) as StudyPlan
      setPlan(planData)

      if (journeyRes?.ok) {
        const journey = (await journeyRes.json()) as LearningJourneyResponse
        if (journey.next_lesson_id != null) {
          setActiveLessonId(journey.next_lesson_id)
        }
        const journeyMap: CompetencyMap = {}
        for (const section of journey.sections) {
          for (const unit of section.units) {
            journeyMap[unit.id] = unit.progress
          }
        }
        if (Object.keys(journeyMap).length > 0) {
          setCompetencies(journeyMap)
        }
      }

      // Learning Journey is the authoritative progression snapshot.
      // Use the legacy competency endpoint only if the journey request failed.
      if (compRes?.ok && !journeyRes?.ok) {
        const compData = await compRes.json()
        if (Array.isArray(compData)) {
          const map: CompetencyMap = {}
          for (const item of compData as { unit_id: string; score: number }[]) {
            map[item.unit_id] = item.score
          }
          setCompetencies(map)
        } else {
          setCompetencies(compData as CompetencyMap)
        }
      }

      const states: Record<
        string,
        Pick<Lesson, 'id' | 'completed' | 'action'>
      > = {}

      if (lessonsRes?.ok) {
        const generatedLessons = (await lessonsRes.json()) as PlanLesson[]
        for (const lesson of generatedLessons) {
          states[
            lessonKey(lesson.week_number, lesson.day_number, lesson.title)
          ] = {
            id: lesson.id,
            completed: lesson.is_completed,
            action: lesson.is_completed ? 'review' : undefined,
          }
        }
      }

      if (pendingRes?.ok) {
        const pendingData = (await pendingRes.json()) as PendingLesson[]
        setPendingLessons(pendingData)
        for (const lesson of pendingData) {
          states[
            lessonKey(lesson.week_number, lesson.day_number, lesson.title)
          ] = {
            id: lesson.id,
            completed: false,
            action: 'continue',
          }
        }
      }

      if (todayRes?.ok) {
        const todayData = (await todayRes.json()) as {
          lessons: TodayLesson[]
        }
        const nextLesson = todayData.lessons.find(
          (l) => l.id != null && !l.is_completed
        )
        setActiveLessonId(nextLesson?.id ?? null)
        for (const lesson of todayData.lessons) {
          if (lesson.id == null) continue
          states[lessonKey(lesson.week, lesson.day, lesson.title)] = {
            id: lesson.id,
            completed: lesson.is_completed ?? false,
            action: lesson.is_completed ? 'review' : 'start',
          }
        }
      }

      setLessonStates(states)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load')
    } finally {
      setLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- re-fetch when active language changes
  }, [router, activeLanguage?.code])

  useEffect(() => {
    void loadPlan()
  }, [loadPlan])

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
    if (plan?.cefr_level && activeLanguage?.code) {
      getCurriculumUnits(plan.cefr_level, activeLanguage.code)
        .then(setUnits)
        .catch(() => setUnits([]))
    }
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
    <div className="juba-mobile-plan mx-auto max-w-6xl space-y-8 px-3 py-5 sm:px-6 sm:py-8">
      {/* Hero */}
      <section className="relative overflow-hidden rounded-[32px] bg-[var(--juba-violet)] px-6 py-7 text-white shadow-[0_18px_50px_rgba(108,69,245,0.22)] sm:px-9 sm:py-9">
        <div className="pointer-events-none absolute -end-8 -top-12 h-40 w-40 rounded-full bg-[var(--juba-yellow)] opacity-95" />
        <div className="pointer-events-none absolute -bottom-16 start-1/3 h-32 w-32 rounded-full bg-[var(--juba-coral)] opacity-80" />
        <div className="pointer-events-none absolute bottom-5 end-1/4 h-12 w-12 rotate-12 rounded-[18px] bg-[var(--juba-mint)]" />
        <div className="relative z-10 max-w-3xl">
          <div className="mb-5 flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-white/15 px-3 py-1.5 text-xs font-black tracking-wide backdrop-blur-sm">
              {t('learningRoadmap')}
            </span>
            <span className="rounded-full bg-[var(--juba-yellow)] px-3 py-1.5 text-xs font-black text-[#242033]">
              {level}
            </span>
          </div>
          <h1 className="max-w-2xl text-3xl font-black tracking-[-0.045em] sm:text-5xl">
            {langName ? `${langName} · ${t('level')}` : t('level')}
          </h1>
          <p className="mt-3 max-w-xl text-sm font-medium leading-6 text-white/80 sm:text-base">
            {t('durationDetail', { weeks: plan.duration_weeks, days: plan.days_per_week })}
          </p>
          <div className="mt-7 flex flex-wrap gap-3">
            <div className="rounded-2xl bg-white/12 px-4 py-3 backdrop-blur-sm">
              <p className="text-[11px] font-bold text-white/65">{t('unitsLabel')}</p>
              <p className="mt-0.5 text-xl font-black">{units.length}</p>
            </div>
            <div className="rounded-2xl bg-white/12 px-4 py-3 backdrop-blur-sm">
              <p className="text-[11px] font-bold text-white/65">{t('pendingLessons')}</p>
              <p className="mt-0.5 text-xl font-black">{pendingLessons.length}</p>
            </div>
            <div className="rounded-2xl bg-white/12 px-4 py-3 backdrop-blur-sm">
              <p className="text-[11px] font-bold text-white/65">{t('level')}</p>
              <p className="mt-0.5 text-xl font-black">{Math.round((competencies[currentUnitId] ?? 0) * 100)}%</p>
            </div>
          </div>
        </div>
      </section>

      {/* Resume */}
      {activeLessonId != null && (
        <section className="relative overflow-hidden rounded-[28px] bg-[var(--juba-yellow)] px-5 py-5 shadow-[0_14px_32px_rgba(39,28,72,0.08)] sm:px-7">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs font-black uppercase tracking-[0.12em] text-[#6b5920]">{t('learningRoadmap')}</p>
              <h2 className="mt-1 text-xl font-black tracking-tight text-[#242033]">{t('resume')}</h2>
              <p className="mt-1 text-sm font-medium text-[#6b5920]">{t('durationDetail', { weeks: plan.duration_weeks, days: plan.days_per_week })}</p>
            </div>
            <button
              onClick={() => void launchLesson(activeLessonId)}
              className="rounded-2xl bg-[var(--juba-violet)] px-6 py-3 text-sm font-black text-white shadow-[0_5px_0_var(--juba-violet-dark)] transition-transform hover:-translate-y-0.5 active:translate-y-1"
            >
              {t('resume')} →
            </button>
          </div>
        </section>
      )}

      {/* Pending lessons */}
      {pendingLessons.length > 0 && (
        <section>
          <div className="mb-4 flex items-end justify-between gap-4 px-1">
            <div>
              <p className="text-xs font-black uppercase tracking-[0.12em] text-[var(--juba-violet)]">{t('pendingLessons')}</p>
              <h2 className="mt-1 text-2xl font-black tracking-tight text-[#242033]">{t('learningRoadmap')}</h2>
            </div>
            <span className="rounded-full bg-[var(--juba-lilac)] px-3 py-1 text-xs font-black text-[var(--juba-violet-dark)]">{pendingLessons.length}</span>
          </div>
          <div className="grid gap-3 md:grid-cols-2">
            {pendingLessons.map((lesson, i) => (
              <button
                key={lesson.id}
                onClick={() => void launchLesson(lesson.id)}
                className="group flex items-center gap-4 rounded-[24px] border-2 border-[#ebe7f5] bg-white p-4 text-start shadow-[0_12px_28px_rgba(39,28,72,0.06)] transition-all hover:-translate-y-1 hover:border-[var(--juba-violet)]"
              >
                <span className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-[17px] text-sm font-black ${i % 2 === 0 ? 'bg-[var(--juba-mint)]' : 'bg-[var(--juba-sky)]'} text-[#242033]`}>
                  {String(i + 1).padStart(2, '0')}
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-black text-[#242033]">{lesson.title}</span>
                  <span className="mt-1 block text-xs font-semibold text-[#938da2]">W{lesson.week_number} · D{lesson.day_number} · {lesson.lesson_type}</span>
                </span>
                <span className="text-xl font-black text-[var(--juba-violet)] transition-transform group-hover:translate-x-1">→</span>
              </button>
            ))}
          </div>
        </section>
      )}

      {/* Path */}
      <section>
        <div className="mb-5 px-1">
          <p className="text-xs font-black uppercase tracking-[0.12em] text-[var(--juba-violet)]">{t('learningRoadmap')}</p>
          <h2 className="mt-1 text-2xl font-black tracking-tight text-[#242033]">{langName || t('level')} · {level}</h2>
        </div>

        <div className="relative space-y-4">
          <div className="pointer-events-none absolute start-[28px] top-8 bottom-8 hidden w-1 rounded-full bg-[var(--juba-lilac)] sm:block" />
          {units.length === 0 && (
            <div className="rounded-[28px] border-2 border-[#ebe7f5] bg-white px-6 py-12 text-center shadow-[0_14px_32px_rgba(39,28,72,0.06)]">
              <p className="text-sm font-black text-[#777087]">{t('noUnitsForLevel', { level })}</p>
              <p className="mt-2 text-xs font-medium text-[#aaa4b5]">{t('noUnitsDesc')}</p>
            </div>
          )}
          {units.map((unit, i) => {
            const unitLessons = byUnit[unit.id] ?? []
            const completedLessons = unitLessons.filter((l) => l.completed).length
            const isActive = unit.id === currentUnitId
            const unitComp = competencies[unit.id] ?? 0
            const isCompleted = unitComp >= 0.8 || (completedLessons > 0 && completedLessons === unitLessons.length)
            const prereqUnit = unit.prerequisite_unit
            const prereqCompleted = prereqUnit ? (competencies[prereqUnit] ?? 0) >= 0.8 : true
            const isLocked = !isActive && !isCompleted && !prereqCompleted && i > 0

            return (
              <div key={unit.id} className="relative sm:ps-16">
                <div className="absolute start-3 top-5 z-10 hidden h-8 w-8 items-center justify-center rounded-full border-4 border-[#fbfaff] bg-[var(--juba-violet)] shadow-sm sm:flex">
                  <span className="text-[10px] font-black text-white">{i + 1}</span>
                </div>
                <UnitCard
                  title={unit.title}
                  index={i}
                  lessonCount={unitLessons.length || unit.lesson_types.length}
                  grammarCount={unit.grammar_points.length}
                  competency={unitComp}
                  status={{ completed: isCompleted, active: isActive, locked: isLocked, isLevelTest: false }}
                  onClick={() => setActiveDrawer(unit)}
                  onStartLesson={isActive && activeLessonId != null ? () => void launchLesson(activeLessonId) : undefined}
                />
              </div>
            )
          })}

          {units.length > 0 && (
            <div className="relative sm:ps-16">
              <UnitCard
                title={t('completionTestTitle', { level })}
                index={units.length}
                lessonCount={1}
                grammarCount={0}
                competency={plan.completion_test_score ?? 0}
                status={{
                  completed: plan.completion_test_taken,
                  active: allUnitsCompleted && !plan.completion_test_taken,
                  locked: !allUnitsCompleted,
                  isLevelTest: true,
                }}
                onClick={() => {
                  if (allUnitsCompleted && !plan.completion_test_taken) router.push(`/assessment/level-test?plan=${plan.id}`)
                }}
              />
            </div>
          )}
        </div>
      </section>

      {allUnitsCompleted && !plan.completion_test_taken && <LevelTestBanner planId={plan.id} level={level} />}

      {plan.completion_test_taken && (
        <section className="rounded-[28px] border-2 border-[#ebe7f5] bg-white px-5 py-5 shadow-[0_14px_32px_rgba(39,28,72,0.06)] sm:px-7">
          <p className="text-xs font-black uppercase tracking-[0.12em] text-[var(--juba-violet)]">{t('levelTestResult')}</p>
          <p className="mt-2 text-sm font-semibold text-[#5f596e]">
            {t('testScore')} <span className="font-black text-[#242033]">{plan.completion_test_score != null ? `${Math.round(plan.completion_test_score * 100)}%` : 'n/a'}</span>
          </p>
          {plan.completion_test_recommendation && <p className="mt-2 text-sm text-[#777087]">{plan.completion_test_recommendation}</p>}
        </section>
      )}

      {activeDrawer && (
        <UnitDrawer
          unit={activeDrawer}
          lessons={(byUnit[activeDrawer.id] ?? []).map((l) => ({ ...l, completed: l.completed ?? false }))}
          onClose={() => setActiveDrawer(null)}
          onStartLesson={(lessonId) => {
            setActiveDrawer(null)
            void launchLesson(lessonId)
          }}
        />
      )}
    </div>
  )
}
