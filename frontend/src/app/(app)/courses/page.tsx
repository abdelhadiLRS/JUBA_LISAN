'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { ArrowRight, BookOpen, CheckCircle2, Headphones, LockKeyhole, Mic2, Sparkles, Coffee, Utensils, Plane, Briefcase } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { CEFR_LEVELS, getCurriculumUnits, type CEFRLevel, type CurriculumUnit } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'

interface StudyPlan {
  cefr_level: CEFRLevel
  generated_plan?: {
    weekly_plan?: Array<{
      days?: Array<{ unit_id: string }>
    }>
  }
}

interface CompetencyRecord {
  unit_id: string
  score: number
}

const LEVEL_META: Record<CEFRLevel, { title: string; desc: string }> = {
  A1: { title: 'A1 · Starter', desc: 'Build your first practical vocabulary and everyday phrases.' },
  A2: { title: 'A2 · Elementary', desc: 'Understand common situations and speak with more confidence.' },
  B1: { title: 'B1 · Intermediate', desc: 'Express ideas, follow conversations, and read with independence.' },
  B2: { title: 'B2 · Upper Intermediate', desc: 'Handle richer conversations and more precise language.' },
  C1: { title: 'C1 · Advanced', desc: 'Develop fluent, nuanced communication for demanding contexts.' },
  C2: { title: 'C2 · Mastery', desc: 'Refine precise, natural communication across demanding contexts.' },
}

const skills = [
  { icon: BookOpen, title: 'Learn', text: 'Build useful language in small, focused steps.' },
  { icon: Headphones, title: 'Listen', text: 'Train your ear with short real-world practice.' },
  { icon: Mic2, title: 'Speak', text: 'Turn recognition into confident active recall.' },
]

const places = [
  { icon: Coffee, title: 'Café', text: 'Order, ask and respond.' },
  { icon: Utensils, title: 'Restaurant', text: 'Food, requests and payment.' },
  { icon: Plane, title: 'Travel', text: 'Tickets, directions and arrival.' },
  { icon: Briefcase, title: 'Work', text: 'Meetings and everyday tasks.' },
]

function getPlanLessonCount(plan: StudyPlan | null): number {
  return plan?.generated_plan?.weekly_plan?.reduce(
    (total, week) => total + (week.days?.length ?? 0),
    0,
  ) ?? 0
}

export default function CoursesPage() {
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
        const nextPlan = planRes?.ok ? (await planRes.json() as StudyPlan) : null

        if (cancelled) return
        setPlan(nextPlan)

        if (compRes?.ok) {
          const raw = await compRes.json()
          const next: Record<string, number> = {}
          if (Array.isArray(raw)) {
            for (const item of raw as CompetencyRecord[]) next[item.unit_id] = item.score
          } else if (raw && typeof raw === 'object') {
            Object.assign(next, raw as Record<string, number>)
          }
          if (!cancelled) setCompetencies(next)
        }

        if (journeyRes?.ok) {
          const journey = await journeyRes.json()
          const nextJourney: Record<string, { id: string; progress: number; state: string; lessons?: Array<{ id: number; is_completed: boolean; state: string }> }> = {}
          for (const section of journey.sections ?? []) {
            for (const unit of section.units ?? []) nextJourney[unit.id] = unit
          }
          setJourneyUnits(nextJourney)
        }

        const units = Object.fromEntries(
          CEFR_LEVELS.map((level, index) => [level, curriculumResponses[index] ?? []]),
        ) as Record<CEFRLevel, CurriculumUnit[]>
        setLevelUnits(units)
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
    if (currentUnits.length === 0) return 0
    const journeyScores = currentUnits.map((unit) => journeyUnits[unit.id]?.progress).filter((score): score is number => typeof score === 'number')
    if (journeyScores.length) return Math.round((journeyScores.reduce((sum, score) => sum + score, 0) / journeyScores.length) * 100)
    return Math.round((currentUnits.reduce((sum, unit) => sum + (competencies[unit.id] ?? 0), 0) / currentUnits.length) * 100)
  }, [competencies, currentUnits, journeyUnits])
  const currentLessonCount = getPlanLessonCount(plan)

  return (
    <main className="juba-mobile-courses w-full px-4 py-5 sm:px-6 sm:py-6 lg:px-8">
      <div className="w-full space-y-5">
        <section className="juba-page-hero juba-reference-hero relative overflow-hidden p-5 sm:p-6">
          <div className="relative z-10 max-w-4xl">
            <div className="juba-eyebrow"><Sparkles className="h-4 w-4" /> Your learning world</div>
            <h1 className="mt-2 text-[28px] font-extrabold tracking-tight text-[var(--duo-ink)] sm:text-4xl">Learn language you can actually use.</h1>
            <p className="mt-2 max-w-3xl text-sm leading-relaxed text-[var(--duo-muted)]">Move through practical situations, strengthen your memory, and unlock the next part of your journey one mission at a time.</p>
            <div className="juba-reference-actions mt-5 flex flex-wrap gap-2.5">
              <Link href="/learning-journey" className="juba-primary-button inline-flex items-center gap-2 text-sm font-bold transition-colors">Continue journey <ArrowRight className="h-4 w-4" /></Link>
              <Link href="/assessment" className="juba-secondary-button inline-flex items-center gap-2 text-sm font-bold text-[var(--duo-ink)] transition-colors">Find my level</Link>
            </div>
          </div>
          <div className="juba-hero-glow" aria-hidden="true" />
        </section>

        <section className="grid gap-3 md:grid-cols-3">
          {skills.map(({ icon: Icon, title, text }) => (
            <div key={title} className="juba-card p-5">
              <div className="flex h-11 w-11 items-center justify-center rounded-[10px] bg-[color-mix(in_srgb,var(--duo-green)_12%,transparent)] text-[var(--duo-green-dark)]"><Icon className="h-5 w-5" /></div>
              <h2 className="mt-4 text-xl font-black text-[var(--duo-ink)]">{title}</h2>
              <p className="mt-2 text-sm leading-6 text-[var(--duo-muted)]">{text}</p>
            </div>
          ))}
        </section>

        <section>
          <div className="juba-reference-section-head mb-4 flex flex-wrap items-end justify-between gap-3">
            <div><p className="juba-eyebrow">Your roadmap</p><h2 className="mt-1 text-2xl font-extrabold tracking-tight text-[var(--duo-ink)] sm:text-3xl">One path. Six levels.</h2></div>
            <span className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-bg)] px-3 py-2 text-xs font-bold text-[var(--duo-muted)]">CEFR · {CEFR_LEVELS.length} levels</span>
          </div>

          {loading ? (
            <div className="grid gap-4 lg:grid-cols-2" aria-label="Loading courses">
              {CEFR_LEVELS.map((level) => <div key={level} className="juba-card h-64 animate-pulse p-6" />)}
            </div>
          ) : (
            <div className="grid gap-5 lg:grid-cols-2">
              {CEFR_LEVELS.map((level, index) => {
                const unlocked = currentLevel ? index <= currentIndex : index === 0
                const current = level === currentLevel
                const units = levelUnits[level] ?? []
                const journeyLevelUnits = units.map((unit) => journeyUnits[unit.id]).filter(Boolean)
                const totalLessons = journeyLevelUnits.reduce((sum, unit) => sum + (unit?.lessons?.length ?? 0), 0)
                const progress = current
                  ? currentProgress
                  : journeyLevelUnits.length
                    ? Math.round((journeyLevelUnits.reduce((sum, unit) => sum + (unit?.progress ?? 0), 0) / journeyLevelUnits.length) * 100)
                    : 0
                const lessonCount = current ? Math.max(currentLessonCount, totalLessons) : totalLessons || units.reduce((sum, unit) => sum + unit.lesson_types.length, 0)

                return (
                  <article key={level} className={`juba-card relative p-6${current ? 'ring-1 ring-[var(--duo-green)]' : ''}`}>
                    {current && <span className="absolute -top-3 end-5 rounded-full bg-[var(--duo-green)] px-3 py-1 text-[11px] font-black uppercase tracking-[.14em] text-white shadow-sm">Current level</span>}
                    <div className="flex items-start justify-between gap-4">
                      <div><span className="text-xs font-bold uppercase tracking-[.16em] text-[var(--duo-muted)]">Level {index + 1}</span><h3 className="mt-2 text-2xl font-black text-[var(--duo-ink)]">{LEVEL_META[level].title}</h3></div>
                      <div className={`flex h-10 w-10 items-center justify-center rounded-full ${unlocked ? 'bg-[color-mix(in_srgb,var(--duo-green)_12%,transparent)] text-[var(--duo-green-dark)]' : 'bg-[var(--duo-bg)] text-[var(--duo-muted)]'}`}>
                        {unlocked ? <CheckCircle2 className="h-5 w-5" /> : <LockKeyhole className="h-5 w-5" />}
                      </div>
                    </div>
                    <p className="mt-3 max-w-xl text-sm leading-6 text-[var(--duo-muted)]">{LEVEL_META[level].desc}</p>
                    <div className="mt-6 flex items-center justify-between text-sm font-bold text-[var(--duo-ink)]"><span>{lessonCount} lessons</span><span>{progress}%</span></div>
                    <div role="progressbar" aria-label={`${level} course progress`} aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.min(100, Math.max(0, progress))} className="mt-2 h-2.5 overflow-hidden rounded-full bg-[var(--duo-bg)]"><div className="h-full rounded-full bg-[var(--duo-green)] transition-all" style={{ width: `${Math.min(100, Math.max(0, progress))}%` }} /></div>
                    {unlocked ? (
                      <Link href={current ? '/plan' : `/courses/${level}`} className="mt-6 inline-flex items-center gap-2 rounded-[10px] bg-[color-mix(in_srgb,var(--duo-green)_12%,transparent)] px-5 py-3 font-black text-[var(--duo-green-dark)] transition hover:bg-[var(--duo-green-dark)] hover:text-white">
                        {current ? 'Open learning plan' : 'Explore level'} <ArrowRight className="h-4 w-4" />
                      </Link>
                    ) : (
                      <span className="mt-6 inline-flex items-center gap-2 rounded-[10px] bg-[var(--duo-bg)] px-5 py-3 font-bold text-[var(--duo-muted)]"><LockKeyhole className="h-4 w-4" /> Unlock later</span>
                    )}
                  </article>
                )
              })}
            </div>
          )}
        </section>

        <section className="juba-card juba-reference-section p-5 sm:p-6">
          <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="juba-eyebrow">Real-world missions</p><h2 className="mt-2 text-2xl font-black text-[var(--duo-ink)]">Practice language where it matters.</h2></div><Link href="/learning-journey" className="font-bold text-[var(--duo-green-dark)] underline underline-offset-4">See my journey</Link></div>
          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {places.map(({ icon: Icon, title, text }) => <div key={title} className="juba-panel p-4 transition-colors hover:border-[var(--duo-green)] hover:bg-[color-mix(in_srgb,var(--duo-green)_8%,transparent)]"><span className="flex h-10 w-10 items-center justify-center rounded-[10px] bg-[color-mix(in_srgb,var(--duo-green)_12%,transparent)] text-[var(--duo-green-dark)]" aria-hidden="true"><Icon className="h-5 w-5" /></span><p className="mt-3 font-black text-[var(--duo-ink)]">{title}</p><p className="mt-1 text-sm text-[var(--duo-muted)]">{text}</p></div>)}
          </div>
        </section>

        <section className="juba-card p-5 sm:p-6">
          <div className="flex items-center gap-3"><Sparkles className="h-6 w-6 text-[var(--duo-green-dark)]" /><h2 className="text-2xl font-black text-[var(--duo-ink)]">The JUBA rhythm</h2></div>
          <div className="mt-6 grid gap-3 sm:grid-cols-4">{['Learn', 'Practice', 'Recall', 'Review'].map((step, i) => <div key={step} className="juba-panel p-4"><span className="text-xs font-bold text-[var(--duo-muted)]">0{i + 1}</span><p className="mt-2 font-black text-[var(--duo-ink)]">{step}</p></div>)}</div>
        </section>
      </div>
    </main>
  )
}
