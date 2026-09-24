'use client'

import { useEffect, useMemo, useState } from 'react'
import { useTranslations } from 'next-intl'
import Link from 'next/link'
import { ArrowRight, BookOpen, CheckCircle2, Headphones, LockKeyhole, Mic2, Sparkles } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { CEFR_LEVELS, getCurriculumUnits, type CEFRLevel, type CurriculumUnit } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'

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
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const [plan, setPlan] = useState<StudyPlan | null>(null)
  const [competencies, setCompetencies] = useState<Record<string, number>>({})
  const [levelUnits, setLevelUnits] = useState<Record<CEFRLevel, CurriculumUnit[]>>({} as Record<CEFRLevel, CurriculumUnit[]>)
  const [journeyUnits, setJourneyUnits] = useState<Record<string, { id: string; progress: number; state: string; lessons?: Array<{ id: number; is_completed: boolean; state: string }> }>>({})
  const [loading, setLoading] = useState(true)

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
  }, [activeLanguage?.code])

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
        <section className="juba-card relative overflow-hidden rounded-[32px] border-2 border-[var(--juba-app-line)] bg-[var(--juba-app-green)] p-7 text-white shadow-[0_22px_48px_rgba(24,37,27,.12)] sm:p-10">
          <div className="relative z-10 max-w-3xl">
            <div className="juba-eyebrow"><Sparkles className="h-4 w-4" /> {t('heroEyebrow')}</div>
            <h1 className="mt-4 text-4xl font-black tracking-tight text-white sm:text-6xl">{t('heroTitle')}</h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-white/80 sm:text-lg">{t('heroDescription')}</p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Link href="/courses" className="inline-flex items-center gap-2 rounded-[18px] bg-white px-5 py-3 font-black text-[var(--juba-app-green-dark)] shadow-[0_5px_0_#d7ceff] transition hover:-translate-y-0.5">{t('openRoadmap')} <ArrowRight className="h-4 w-4" /></Link>
              <Link href="/assessment" className="inline-flex items-center gap-2 rounded-[18px] border-2 border-white/25 bg-white/10 px-5 py-3 font-black text-white transition hover:bg-white/20">{t('findLevel')}</Link>
            </div>
          </div>
          <div className="juba-hero-glow" aria-hidden="true" />
        </section>

        <section className="grid gap-4 md:grid-cols-3">
          {skills.map((key, index) => {
            const Icon = [BookOpen, Headphones, Mic2][index]
            return (
              <div key={key} className="juba-card rounded-[27px] border-2 border-[var(--juba-app-line)] bg-white p-5 shadow-[0_12px_28px_rgba(52,37,90,.07)]">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[var(--juba-app-green-soft)] text-[var(--juba-app-green-dark)]"><Icon className="h-5 w-5" /></div>
                <h2 className="mt-4 text-xl font-black text-[var(--juba-app-ink)]">{t(\`skills.\${key}.title\`)}</h2>
                <p className="mt-2 text-sm leading-6 text-[var(--juba-app-muted)]">{t(\`skills.\${key}.text\`)}</p>
              </div>
            )
          })}
        </section>

        <section>
          <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
            <div><p className="juba-eyebrow">{t('roadmapEyebrow')}</p><h2 className="mt-2 text-3xl font-black text-[var(--juba-app-ink)] sm:text-4xl">{t('roadmapTitle')}</h2></div>
            <span className="rounded-full border border-[var(--juba-app-line)] bg-[#f3f7ef] px-4 py-2 text-sm font-bold text-[var(--juba-app-muted)]">CEFR · {t('levelCount', { count: CEFR_LEVELS.length })}</span>
          </div>
          {loading ? (
            <div className="grid gap-5 lg:grid-cols-2" aria-label={t('loading')}>{CEFR_LEVELS.map((level) => <div key={level} className="juba-card h-64 animate-pulse rounded-[28px] border-2 border-[var(--juba-app-line)] bg-white p-6" />)}</div>
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
                  <article key={level} className={\`juba-card relative rounded-[30px] border-2 border-[var(--juba-app-line)] bg-white p-6 shadow-[0_12px_28px_rgba(52,37,90,.07)] transition hover:-translate-y-1 \${current ? 'ring-2 ring-[var(--juba-app-green)]' : ''}\`}>
                    {current && <span className="absolute -top-3 right-5 rounded-full bg-[var(--juba-app-yellow)] px-3 py-1 text-[11px] font-black uppercase tracking-[.14em] text-[var(--juba-app-ink)]">{t('currentLevel')}</span>}
                    <div className="flex items-start justify-between gap-4">
                      <div><span className="text-xs font-bold uppercase tracking-[.16em] text-[var(--juba-app-muted)]">{t('levelLabel', { number: index + 1 })}</span><h3 className="mt-2 text-2xl font-black text-[var(--juba-app-ink)]">{t(\`levels.\${level}.title\`)}</h3></div>
                      <div className={\`flex h-10 w-10 items-center justify-center rounded-full \${unlocked ? 'bg-[var(--juba-app-yellow)] text-[var(--juba-app-green-dark)]' : 'bg-[#f3f7ef] text-[var(--juba-app-muted)]'}\`}>{unlocked ? <CheckCircle2 className="h-5 w-5" /> : <LockKeyhole className="h-5 w-5" />}</div>
                    </div>
                    <p className="mt-3 max-w-xl text-sm leading-6 text-[var(--juba-app-muted)]">{t(\`levels.\${level}.desc\`)}</p>
                    <div className="mt-6 flex items-center justify-between text-sm font-bold text-[var(--juba-app-ink)]"><span>{t('lessons', { count: lessonCount })}</span><span>{progress}%</span></div>
                    <div className="mt-2 h-2.5 overflow-hidden rounded-full bg-[#f3f7ef]"><div className="h-full rounded-full bg-[var(--juba-app-yellow)] transition-all" style={{ width: \`\${progress}%\` }} /></div>
                    {unlocked ? (
                      <Link href={current ? '/plan' : \`/courses/\${level}\`} className="mt-6 inline-flex items-center gap-2 rounded-xl bg-[var(--juba-app-green-soft)] px-5 py-3 font-black text-[var(--juba-app-green-dark)] transition hover:bg-[var(--juba-app-green)]">{current ? t('openLearningPlan') : t('exploreLevel')} <ArrowRight className="h-4 w-4" /></Link>
                    ) : (
                      <span className="mt-6 inline-flex items-center gap-2 rounded-xl bg-[#f3f7ef] px-5 py-3 font-bold text-[var(--juba-app-muted)]"><LockKeyhole className="h-4 w-4" /> {t('unlockLater')}</span>
                    )}
                  </article>
                )
              })}
            </div>
          )}
        </section>

        <section className="juba-card rounded-[30px] border-2 border-[var(--juba-app-line)] bg-white p-6 shadow-[0_12px_28px_rgba(52,37,90,.07)] sm:p-7">
          <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="juba-eyebrow">{t('missionsEyebrow')}</p><h2 className="mt-2 text-2xl font-black text-[var(--juba-app-ink)]">{t('missionsTitle')}</h2></div><Link href="/learning-journey" className="font-bold text-[var(--juba-app-green-dark)] underline underline-offset-4">{t('openRoadmap')}</Link></div>
          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{places.map((place) => <div key={place.key} className="rounded-2xl border border-[var(--juba-app-line)] bg-[#f3f7ef] p-4"><span className="text-2xl" aria-hidden="true">{place.icon}</span><p className="mt-3 font-black text-[var(--juba-app-ink)]">{t(\`places.\${place.key}.title\`)}</p><p className="mt-1 text-sm text-[var(--juba-app-muted)]">{t(\`places.\${place.key}.text\`)}</p></div>)}</div>
        </section>

        <section className="juba-card rounded-[30px] border-2 border-[var(--juba-app-line)] bg-white p-6 shadow-[0_12px_28px_rgba(52,37,90,.07)] sm:p-7">
          <div className="flex items-center gap-3"><Sparkles className="h-6 w-6 text-[var(--juba-app-green-dark)]" /><h2 className="text-2xl font-black text-[var(--juba-app-ink)]">{t('rhythmTitle')}</h2></div>
          <div className="mt-6 grid gap-3 sm:grid-cols-4">{(['learn', 'practice', 'recall', 'review'] as const).map((step, i) => <div key={step} className="rounded-2xl border border-[var(--juba-app-line)] bg-[#f3f7ef] p-4"><span className="text-xs font-bold text-[var(--juba-app-muted)]">0{i + 1}</span><p className="mt-2 font-black text-[var(--juba-app-ink)]">{t(\`rhythm.\${step}\`)}</p></div>)}</div>
        </section>
      </div>
    </main>
  )
}
