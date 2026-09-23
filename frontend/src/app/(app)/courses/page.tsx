'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { ArrowRight, BookOpen, CheckCircle2, Headphones, LockKeyhole, Mic2, Sparkles } from 'lucide-react'
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
  { icon: '☕', title: 'Café', text: 'Order, ask and respond.' },
  { icon: '🍽️', title: 'Restaurant', text: 'Food, requests and payment.' },
  { icon: '✈️', title: 'Travel', text: 'Tickets, directions and arrival.' },
  { icon: '💼', title: 'Work', text: 'Meetings and everyday tasks.' },
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
    <main className="min-h-screen px-4 py-8 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-6xl space-y-8">
        <section className="juba-card relative overflow-hidden rounded-[32px] border-2 border-[#eee8ff] bg-[#6c45f5] p-7 text-white shadow-[0_22px_48px_rgba(108,69,245,.22)] sm:p-10">
          <div className="relative z-10 max-w-3xl">
            <div className="juba-eyebrow"><Sparkles className="h-4 w-4" /> Your learning world</div>
            <h1 className="mt-4 text-4xl font-black tracking-tight text-white sm:text-6xl">Learn language you can actually use.</h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-white/80 sm:text-lg">Move through practical situations, strengthen your memory, and unlock the next part of your journey one mission at a time.</p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Link href="/learning-journey" className="inline-flex items-center gap-2 rounded-[18px] bg-white px-5 py-3 font-black text-[#5a35dc] shadow-[0_5px_0_#d7ceff] transition hover:-translate-y-0.5">Continue journey <ArrowRight className="h-4 w-4" /></Link>
              <Link href="/assessment" className="inline-flex items-center gap-2 rounded-[18px] border-2 border-white/25 bg-white/10 px-5 py-3 font-black text-white transition hover:bg-white/20">Find my level</Link>
            </div>
          </div>
          <div className="juba-hero-glow" aria-hidden="true" />
        </section>

        <section className="grid gap-4 md:grid-cols-3">
          {skills.map(({ icon: Icon, title, text }) => (
            <div key={title} className="juba-card rounded-[27px] border-2 border-[#eee8ff] bg-white p-5 shadow-[0_12px_28px_rgba(52,37,90,.07)]">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#eee8ff] text-[#5a35dc]"><Icon className="h-5 w-5" /></div>
              <h2 className="mt-4 text-xl font-black text-fl-fg">{title}</h2>
              <p className="mt-2 text-sm leading-6 text-fl-muted-2">{text}</p>
            </div>
          ))}
        </section>

        <section>
          <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
            <div><p className="juba-eyebrow">Your roadmap</p><h2 className="mt-2 text-3xl font-black text-fl-fg sm:text-4xl">One path. Six levels.</h2></div>
            <span className="rounded-full border border-fl-border bg-fl-surface-2 px-4 py-2 text-sm font-bold text-fl-muted">CEFR · {CEFR_LEVELS.length} levels</span>
          </div>

          {loading ? (
            <div className="grid gap-5 lg:grid-cols-2" aria-label="Loading courses">
              {CEFR_LEVELS.map((level) => <div key={level} className="juba-card h-64 animate-pulse rounded-[28px] border-2 border-[#eee8ff] bg-white p-6" />)}
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
                  <article key={level} className={`juba-card relative rounded-[30px] border-2 border-[#eee8ff] bg-white p-6 shadow-[0_12px_28px_rgba(52,37,90,.07)] transition hover:-translate-y-1 ${current ? 'ring-2 ring-[var(--juba-primary)]' : ''}`}>
                    {current && <span className="absolute -top-3 right-5 rounded-full bg-[#ffd85a] px-3 py-1 text-[11px] font-black uppercase tracking-[.14em] text-[var(--juba-text)]">Current level</span>}
                    <div className="flex items-start justify-between gap-4">
                      <div><span className="text-xs font-bold uppercase tracking-[.16em] text-fl-muted-2">Level {index + 1}</span><h3 className="mt-2 text-2xl font-black text-fl-fg">{LEVEL_META[level].title}</h3></div>
                      <div className={`flex h-10 w-10 items-center justify-center rounded-full ${unlocked ? 'bg-[#fff0b5] text-[#5a35dc]' : 'bg-fl-surface-2 text-fl-muted-2'}`}>
                        {unlocked ? <CheckCircle2 className="h-5 w-5" /> : <LockKeyhole className="h-5 w-5" />}
                      </div>
                    </div>
                    <p className="mt-3 max-w-xl text-sm leading-6 text-fl-muted-2">{LEVEL_META[level].desc}</p>
                    <div className="mt-6 flex items-center justify-between text-sm font-bold text-fl-fg"><span>{lessonCount} lessons</span><span>{progress}%</span></div>
                    <div className="mt-2 h-2.5 overflow-hidden rounded-full bg-fl-surface-2"><div className="h-full rounded-full bg-[#ffd85a] transition-all" style={{ width: `${progress}%` }} /></div>
                    {unlocked ? (
                      <Link href={current ? '/plan' : `/courses/${level}`} className="mt-6 inline-flex items-center gap-2 rounded-xl bg-[#eee8ff] px-5 py-3 font-black text-[#5a35dc] transition hover:bg-[var(--juba-primary)]">
                        {current ? 'Open learning plan' : 'Explore level'} <ArrowRight className="h-4 w-4" />
                      </Link>
                    ) : (
                      <span className="mt-6 inline-flex items-center gap-2 rounded-xl bg-fl-surface-2 px-5 py-3 font-bold text-fl-muted-2"><LockKeyhole className="h-4 w-4" /> Unlock later</span>
                    )}
                  </article>
                )
              })}
            </div>
          )}
        </section>

        <section className="juba-card rounded-[30px] border-2 border-[#eee8ff] bg-white p-6 shadow-[0_12px_28px_rgba(52,37,90,.07)] sm:p-7">
          <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="juba-eyebrow">Real-world missions</p><h2 className="mt-2 text-2xl font-black text-fl-fg">Practice language where it matters.</h2></div><Link href="/learning-journey" className="font-bold text-[#5a35dc] underline underline-offset-4">See my journey</Link></div>
          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {places.map((place) => <div key={place.title} className="rounded-2xl border border-fl-border bg-fl-surface-2 p-4"><span className="text-2xl" aria-hidden="true">{place.icon}</span><p className="mt-3 font-black text-fl-fg">{place.title}</p><p className="mt-1 text-sm text-fl-muted-2">{place.text}</p></div>)}
          </div>
        </section>

        <section className="juba-card rounded-[30px] border-2 border-[#eee8ff] bg-white p-6 shadow-[0_12px_28px_rgba(52,37,90,.07)] sm:p-7">
          <div className="flex items-center gap-3"><Sparkles className="h-6 w-6 text-[var(--juba-primary-dark)]" /><h2 className="text-2xl font-black text-fl-fg">The JUBA rhythm</h2></div>
          <div className="mt-6 grid gap-3 sm:grid-cols-4">{['Learn', 'Practice', 'Recall', 'Review'].map((step, i) => <div key={step} className="rounded-2xl border border-fl-border bg-fl-surface-2 p-4"><span className="text-xs font-bold text-fl-muted-2">0{i + 1}</span><p className="mt-2 font-black text-fl-fg">{step}</p></div>)}</div>
        </section>
      </div>
    </main>
  )
}
