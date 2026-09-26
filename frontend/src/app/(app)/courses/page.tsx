'use client'

import { useEffect, useMemo, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import Link from 'next/link'
import { apiFetch } from '@/lib/api'
import { subscribeToLearningProgressUpdated } from '@/lib/learning-progress'
import { CEFR_LEVELS, getCurriculumUnits, type CEFRLevel, type CurriculumUnit } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
import { CEFR_DESCRIPTORS, CEFR_SKILLS, type CEFRSkill } from '@/data/cefr-descriptors'

interface StudyPlan {
  cefr_level: CEFRLevel
  generated_plan?: { weekly_plan?: Array<{ days?: Array<{ unit_id: string }> }> }
}
interface CompetencyRecord { unit_id: string; score: number }

const skills = ['learn', 'listen', 'speak'] as const
const places = [
  { icon: '☕', key: 'cafe' },
  { icon: '🍽️', key: 'restaurant' },
  { icon: '✈️', key: 'travel' },
  { icon: '💼', key: 'work' },
] as const

function getPlanLessonCount(plan: StudyPlan | null): number {
  return plan?.generated_plan?.weekly_plan?.reduce((total, week) => total + (week.days?.length ?? 0), 0) ?? 0
}

export default function CoursesPage() {
  const t = useTranslations('courses')
  const locale = useLocale()
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const [plan, setPlan] = useState<StudyPlan | null>(null)
  const [competencies, setCompetencies] = useState<Record<string, number>>({})
  const [levelUnits, setLevelUnits] = useState<Record<CEFRLevel, CurriculumUnit[]>>({} as Record<CEFRLevel, CurriculumUnit[]>)
  const [journeyUnits, setJourneyUnits] = useState<Record<string, { id: string; progress: number; state: string; lessons?: Array<{ id: number; is_completed: boolean; state: string }> }>>({})
  const [loading, setLoading] = useState(true)
  const [refreshToken, setRefreshToken] = useState(0)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const language = activeLanguage?.code ?? 'en-GB'
        const [planRes, compRes, journeyRes, ...curriculumResponses] = await Promise.all([
          apiFetch('/api/study-plan/current').catch(() => null),
          apiFetch('/api/progress/competencies').catch(() => null),
          apiFetch('/api/study-plan/learning-path').catch(() => null),
          ...CEFR_LEVELS.map((level) => getCurriculumUnits(level, language).catch(() => [])),
        ])
        const nextPlan = planRes?.ok ? await planRes.json() as StudyPlan : null
        if (cancelled) return
        setPlan(nextPlan)
        if (compRes?.ok) {
          const raw = await compRes.json()
          const next: Record<string, number> = {}
          if (Array.isArray(raw)) {
            for (const item of raw as CompetencyRecord[]) next[item.unit_id] = item.score
          } else if (raw && typeof raw === 'object') Object.assign(next, raw as Record<string, number>)
          if (!cancelled) setCompetencies(next)
        }
        if (journeyRes?.ok) {
          const journey = await journeyRes.json()
          const nextJourney: Record<string, { id: string; progress: number; state: string; lessons?: Array<{ id: number; is_completed: boolean; state: string }> }> = {}
          for (const section of journey.sections ?? []) for (const unit of section.units ?? []) nextJourney[unit.id] = unit
          setJourneyUnits(nextJourney)
        }
        setLevelUnits(Object.fromEntries(CEFR_LEVELS.map((level, index) => [level, curriculumResponses[index] ?? []])) as Record<CEFRLevel, CurriculumUnit[]>)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    void load()
    return () => { cancelled = true }
  }, [activeLanguage?.code, refreshToken])

  useEffect(() => {
    return subscribeToLearningProgressUpdated(() => {
      setRefreshToken((value) => value + 1)
    })
  }, [])

  const currentLevel = plan?.cefr_level ?? null
  const currentIndex = currentLevel ? CEFR_LEVELS.indexOf(currentLevel) : 0
  const currentUnits = currentLevel ? (levelUnits[currentLevel] ?? []) : []
  const currentProgress = useMemo(() => {
    if (!currentUnits.length) return 0
    const journeyScores = currentUnits.map((unit) => journeyUnits[unit.id]?.progress).filter((score): score is number => typeof score === 'number')
    if (journeyScores.length) return Math.round((journeyScores.reduce((sum, score) => sum + score, 0) / journeyScores.length) * 100)
    return Math.round((currentUnits.reduce((sum, unit) => sum + (competencies[unit.id] ?? 0), 0) / currentUnits.length) * 100)
  }, [competencies, currentUnits, journeyUnits])
  const currentLessonCount = getPlanLessonCount(plan)

  return (
    <main className="juba-mobile-courses min-h-screen px-4 py-8 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-6xl space-y-8">
        <section className="card relative overflow-hidden border-0 bg-primary text-white p-4 p-md-5">
          <div className="relative z-10 max-w-3xl">
            <div className="page-pretitle d-flex align-items-center gap-2"><i className="ti ti-sparkles icon icon-sm" aria-hidden="true" /> {t('heroEyebrow')}</div>
            <h1 className="mt-4 text-4xl font-black tracking-tight text-white sm:text-6xl">{t('heroTitle')}</h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-white/80 sm:text-lg">{t('heroDescription')}</p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Link href="/courses" className="inline-flex items-center gap-2 rounded-[18px] bg-white px-5 py-3 font-black text-[#373fb8] shadow-[0_8px_18px_rgba(43,45,90,.10)] transition hover:-translate-y-0.5">{t('openRoadmap')} <i className="ti ti-arrow-right icon" aria-hidden="true" /></Link>
              <Link href="/assessment" className="inline-flex items-center gap-2 rounded-[18px] border-2 border-white/25 bg-white/10 px-5 py-3 font-black text-white transition hover:bg-white/20">{t('findLevel')}</Link>
            </div>
          </div>
          <div className="juba-hero-glow" aria-hidden="true" />
        </section>

        <section className="grid gap-4 md:grid-cols-3">
          {skills.map((key, index) => {
            return (
              <div key={key} className="card p-4">
                <div className="avatar avatar-md rounded-2 bg-primary-lt text-primary"><i className={['ti ti-book','ti ti-headphones','ti ti-microphone'][index] + ' icon'} aria-hidden="true" /></div>
                <h2 className="mt-4 text-xl font-black text-[#202127]">{t(`skills.${key}.title`)}</h2>
                <p className="mt-2 text-sm leading-6 text-[rgba(32,33,39,.52)]">{t(`skills.${key}.text`)}</p>
              </div>
            )
          })}
        </section>

        <section>
          <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
            <div><p className="page-pretitle">{t('roadmapEyebrow')}</p><h2 className="mt-2 text-3xl font-black text-[#202127] sm:text-4xl">{t('roadmapTitle')}</h2></div>
            <span className="rounded-full border border-[rgba(7,7,9,.08)] bg-[#f4f4f2] px-4 py-2 text-sm font-bold text-[rgba(32,33,39,.52)]">CEFR · {t('levelCount', { count: CEFR_LEVELS.length })}</span>
          </div>
          {loading ? (
            <div className="grid gap-5 lg:grid-cols-2" aria-label={t('loading')}>{CEFR_LEVELS.map((level) => <div key={level} className="card h-64 animate-pulse rounded-[28px] border border-[rgba(7,7,9,.08)] bg-white p-6" />)}</div>
          ) : (
            <div className="grid gap-5 lg:grid-cols-2">
              {CEFR_LEVELS.map((level, index) => {
                const unlocked = currentLevel ? index <= currentIndex : index === 0
                const current = level === currentLevel
                const units = levelUnits[level] ?? []
                const journeyLevelUnits = units.map((unit) => journeyUnits[unit.id]).filter(Boolean)
                const totalLessons = journeyLevelUnits.reduce((sum, unit) => sum + (unit?.lessons?.length ?? 0), 0)
                const progress = current ? currentProgress : journeyLevelUnits.length ? Math.round((journeyLevelUnits.reduce((sum, unit) => sum + (unit?.progress ?? 0), 0) / journeyLevelUnits.length) * 100) : 0
                const lessonCount = current ? Math.max(currentLessonCount, totalLessons) : totalLessons || units.reduce((sum, unit) => sum + unit.lesson_types.length, 0)
                return (
                  <article key={level} className={`card relative rounded-[30px] border border-[rgba(7,7,9,.08)] bg-white p-6 shadow-[0_12px_30px_rgba(43,45,90,.055)] transition hover:-translate-y-1 ${current ? 'ring-2 ring-[#5862e2]' : ''}`}>
                    {current && <span className="absolute -top-3 right-5 rounded-full bg-[#fff3d1] px-3 py-1 text-[11px] font-black uppercase tracking-[.14em] text-[#202127]">{t('currentLevel')}</span>}
                    <div className="flex items-start justify-between gap-4">
                      <div><span className="text-xs font-bold uppercase tracking-[.16em] text-[rgba(32,33,39,.52)]">{t('levelLabel', { number: index + 1 })}</span><h3 className="mt-2 text-2xl font-black text-[#202127]">{t(`levels.${level}.title`)}</h3></div>
                      <div className={`flex h-10 w-10 items-center justify-center rounded-full ${unlocked ? 'bg-[#fff3d1] text-[#373fb8]' : 'bg-[#f4f4f2] text-[rgba(32,33,39,.52)]'}`}>{unlocked ? <CheckCircle2 className="h-5 w-5" /> : <LockKeyhole className="h-5 w-5" />}</div>
                    </div>
                    <p className="mt-3 max-w-xl text-sm leading-6 text-[rgba(32,33,39,.52)]">{t(`levels.${level}.desc`)}</p>
                    <div className="mt-6 flex items-center justify-between text-sm font-bold text-[#202127]"><span>{t('lessons', { count: lessonCount })}</span><span>{progress}%</span></div>
                    <div className="mt-2 h-2.5 overflow-hidden rounded-full bg-[#f4f4f2]"><div className="h-full rounded-full bg-[#fff3d1] transition-all" style={{ width: `${progress}%` }} /></div>
                    {unlocked ? (
                      <Link href={current ? '/plan' : `/courses/${level}`} className="mt-6 inline-flex items-center gap-2 rounded-xl bg-[#ededff] px-5 py-3 font-black text-[#373fb8] transition hover:bg-[#5862e2]">{current ? t('openLearningPlan') : t('exploreLevel')} <i className="ti ti-arrow-right icon" aria-hidden="true" /></Link>
                    ) : (
                      <span className="mt-6 inline-flex items-center gap-2 rounded-xl bg-[#f4f4f2] px-5 py-3 font-bold text-[rgba(32,33,39,.52)]"><i className="ti ti-lock icon" aria-hidden="true" /> {t('unlockLater')}</span>
                    )}
                  </article>
                )
              })}
            </div>
          )}
        </section>

        <section className="card">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="page-pretitle">{t('cefrEyebrow')}</p>
              <h2 className="mt-2 text-2xl font-black text-[#202127] sm:text-3xl">{t('cefrTitle')}</h2>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-[rgba(32,33,39,.52)]">{t('cefrDescription')}</p>
            </div>
            <span className="rounded-full bg-[#ededff] px-4 py-2 text-xs font-black text-[#373fb8]">CEFR · A1–C2</span>
          </div>
          <div className="mt-6 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            {CEFR_LEVELS.map((level) => (
              <article key={level} className="p-4">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <span className="text-xs font-black uppercase tracking-[.16em] text-[rgba(32,33,39,.52)]">{t('cefrLevelLabel')}</span>
                    <h3 className="mt-1 text-xl font-black text-[#202127]">{level} · {t(`levels.${level}.title`).replace(`${level} · `, '')}</h3>
                  </div>
                  <span className="rounded-full bg-white px-3 py-1 text-xs font-black text-[#373fb8] ring-1 ring-[rgba(7,7,9,.08)]">{level}</span>
                </div>
                <p className="mt-3 text-sm leading-6 text-[rgba(32,33,39,.52)]">{t(`levels.${level}.desc`)}</p>
                <div className="mt-5 space-y-3">
                  {CEFR_SKILLS.map((skill: CEFRSkill) => (
                    <div key={skill} className="border p-3 rounded-2">
                      <p className="text-xs font-black uppercase tracking-[.12em] text-[#373fb8]">{t(`cefrSkills.${skill}`)}</p>
                      <p className="mt-1 text-sm leading-5 text-[#202127]">{CEFR_DESCRIPTORS[locale === 'ar' ? 'ar' : 'en'][level][skill]}</p>
                    </div>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="card">
          <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="page-pretitle">{t('missionsEyebrow')}</p><h2 className="mt-2 text-2xl font-black text-[#202127]">{t('missionsTitle')}</h2></div><Link href="/learning-journey" className="font-bold text-[#373fb8] underline underline-offset-4">{t('openRoadmap')}</Link></div>
          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{places.map((place) => <div key={place.key} className="border p-4 rounded-2"><span className="text-2xl" aria-hidden="true">{place.icon}</span><p className="mt-3 font-black text-[#202127]">{t(`places.${place.key}.title`)}</p><p className="mt-1 text-sm text-[rgba(32,33,39,.52)]">{t(`places.${place.key}.text`)}</p></div>)}</div>
        </section>

        <section className="card">
          <div className="flex items-center gap-3"><i className="ti ti-sparkles icon text-primary" aria-hidden="true" /><h2 className="text-2xl font-black text-[#202127]">{t('rhythmTitle')}</h2></div>
          <div className="mt-6 grid gap-3 sm:grid-cols-4">{(['learn', 'practice', 'recall', 'review'] as const).map((step, i) => <div key={step} className="rounded-2xl border border-[rgba(7,7,9,.08)] bg-[#f4f4f2] p-4"><span className="text-xs font-bold text-[rgba(32,33,39,.52)]">0{i + 1}</span><p className="mt-2 font-black text-[#202127]">{t(`rhythm.${step}`)}</p></div>)}</div>
        </section>
      </div>
    </main>
  )
}
