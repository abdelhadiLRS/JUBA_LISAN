'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, ArrowRight, BookOpen, CheckCircle2, LockKeyhole, Sparkles } from 'lucide-react'
import { useParams } from 'next/navigation'
import { apiFetch } from '@/lib/api'
import { CEFR_LEVELS, getCurriculumUnits, type CEFRLevel, type CurriculumUnit } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'

interface StudyPlan { cefr_level: CEFRLevel }
interface JourneyUnit { id: string; progress: number; state: string; lessons?: Array<{ id: number; title: string; lesson_type: string; is_completed: boolean; available: boolean; state: string }> }
interface JourneyResponse { sections?: Array<{ units?: JourneyUnit[] }> }

const META: Record<CEFRLevel, { title: string; description: string }> = {
  A1: { title: 'A1 · Starter', description: 'Build a practical foundation for everyday communication.' },
  A2: { title: 'A2 · Elementary', description: 'Handle familiar situations with growing confidence.' },
  B1: { title: 'B1 · Intermediate', description: 'Communicate independently across everyday topics.' },
  B2: { title: 'B2 · Upper Intermediate', description: 'Express ideas with greater range, accuracy and nuance.' },
  C1: { title: 'C1 · Advanced', description: 'Communicate fluently in demanding academic and professional contexts.' },
  C2: { title: 'C2 · Mastery', description: 'Refine precision, flexibility and natural expression.' },
}

export default function CourseLevelPage() {
  const params = useParams()
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const requestedLevel = String(params.level ?? '').toUpperCase() as CEFRLevel
  const level = CEFR_LEVELS.includes(requestedLevel) ? requestedLevel : null
  const [units, setUnits] = useState<CurriculumUnit[]>([])
  const [plan, setPlan] = useState<StudyPlan | null>(null)
  const [journeyUnits, setJourneyUnits] = useState<Record<string, JourneyUnit>>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!level) { setLoading(false); return }
    let cancelled = false
    async function load() {
      setLoading(true)
      const language = activeLanguage?.code ?? 'en-GB'
      const [curriculum, planRes, journeyRes] = await Promise.all([
        getCurriculumUnits(level, language).catch(() => []),
        apiFetch('/api/study-plan/current').catch(() => null),
        apiFetch('/api/study-plan/learning-path').catch(() => null),
      ])
      if (cancelled) return
      setUnits(curriculum)
      if (planRes?.ok) setPlan(await planRes.json())
      if (journeyRes?.ok) {
        const journey = await journeyRes.json() as JourneyResponse
        const map: Record<string, JourneyUnit> = {}
        for (const section of journey.sections ?? []) for (const unit of section.units ?? []) map[unit.id] = unit
        setJourneyUnits(map)
      }
      setLoading(false)
    }
    void load()
    return () => { cancelled = true }
  }, [activeLanguage?.code, level])

  const isCurrentLevel = !!level && plan?.cefr_level === level
  const currentIndex = plan ? CEFR_LEVELS.indexOf(plan.cefr_level) : -1
  const levelIndex = level ? CEFR_LEVELS.indexOf(level) : -1
  const levelUnlocked = levelIndex >= 0 && (currentIndex < 0 ? levelIndex === 0 : levelIndex <= currentIndex)
  const totals = useMemo(() => {
    const completed = units.reduce((sum, unit) => sum + (journeyUnits[unit.id]?.lessons?.filter((lesson) => lesson.is_completed).length ?? 0), 0)
    const available = units.reduce((sum, unit) => sum + (journeyUnits[unit.id]?.lessons?.filter((lesson) => lesson.available).length ?? 0), 0)
    return { completed, available }
  }, [journeyUnits, units])

  if (!level) return <main className='mx-auto max-w-4xl px-4 py-16'><div className='juba-card p-8 text-center'><p className='juba-eyebrow justify-center'>Course not found</p><h1 className='mt-3 text-3xl font-black text-fl-fg'>Choose a CEFR level.</h1><Link href='/courses' className='mt-6 inline-flex items-center gap-2 rounded-xl bg-[var(--juba-primary-soft)] px-5 py-3 font-bold text-[var(--juba-primary-dark)]'>Back to courses <ArrowRight className='h-4 w-4' /></Link></div></main>

  return (
    <main className='min-h-screen px-4 py-8 sm:px-6 lg:px-10'>
      <div className='mx-auto max-w-6xl space-y-7'>
        <Link href='/courses' className='inline-flex items-center gap-2 text-sm font-bold text-fl-muted hover:text-fl-fg'><ArrowLeft className='h-4 w-4' /> All courses</Link>
        <section className='juba-card relative overflow-hidden p-7 sm:p-10'>
          <div className='relative z-10 max-w-3xl'><div className='juba-eyebrow'><Sparkles className='h-4 w-4' /> CEFR level {level}</div><h1 className='mt-4 text-4xl font-black tracking-tight text-fl-fg sm:text-6xl'>{META[level].title}</h1><p className='mt-4 text-base leading-7 text-fl-muted-2 sm:text-lg'>{META[level].description}</p><div className='mt-6 flex flex-wrap gap-3 text-sm font-bold text-fl-fg'><span className='rounded-full border border-fl-border bg-fl-surface-2 px-4 py-2'>{units.length} units</span>{isCurrentLevel && <><span className='rounded-full border border-fl-border bg-fl-surface-2 px-4 py-2'>{totals.completed} lessons completed</span><span className='rounded-full border border-fl-border bg-fl-surface-2 px-4 py-2'>{totals.available} ready now</span></>}</div></div>
          <div className='juba-hero-glow' aria-hidden='true' />
        </section>
        {!loading && !levelUnlocked && <div className='juba-card flex items-start gap-4 border-dashed p-6'><LockKeyhole className='mt-1 h-5 w-5 shrink-0 text-fl-muted-2' /><div><h2 className='font-black text-fl-fg'>This level is not unlocked yet.</h2><p className='mt-1 text-sm leading-6 text-fl-muted-2'>Continue your current learning plan to unlock later CEFR levels.</p></div></div>}
        <section className='space-y-4'>
          {loading ? Array.from({ length: 4 }, (_, index) => <div key={index} className='juba-card h-40 animate-pulse' />) : units.map((unit) => {
            const journey = journeyUnits[unit.id]
            const progress = Math.round((journey?.progress ?? 0) * 100)
            const lessons = journey?.lessons ?? []
            const state = journey?.state ?? (unit.prerequisite_unit ? 'locked' : 'available')
            const canOpen = levelUnlocked && state !== 'locked'
            return <article key={unit.id} className={state === 'completed' ? 'juba-card p-6 ring-1 ring-[var(--juba-primary)]' : 'juba-card p-6'}>
              <div className='flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between'><div className='min-w-0'><div className='flex items-center gap-3'><span className='flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-[var(--juba-primary-soft)] text-sm font-black text-[var(--juba-primary-dark)]'>{String(unit.unit_number).padStart(2, '0')}</span><div><p className='text-xs font-bold uppercase tracking-[.16em] text-fl-muted-2'>{unit.level} · Unit {unit.unit_number}</p><h2 className='mt-1 text-xl font-black text-fl-fg'>{unit.title}</h2></div></div>
              <div className='mt-5 flex flex-wrap gap-2'>{unit.lesson_types.map((type) => <span key={type} className='rounded-full border border-fl-border bg-fl-surface-2 px-3 py-1 text-xs font-bold text-fl-muted'>{type}</span>)}{unit.grammar_points.slice(0, 3).map((point) => <span key={point} className='rounded-full border border-fl-border bg-fl-surface px-3 py-1 text-xs text-fl-muted-2'>{point}</span>)}</div>
              <div className='mt-4 grid gap-3 sm:grid-cols-3'>
                <div className='rounded-2xl border border-fl-border bg-fl-surface-2 p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-fl-muted-2'>Grammar</p><p className='mt-1 text-lg font-black text-fl-fg'>{unit.grammar_points.length}</p></div>
                <div className='rounded-2xl border border-fl-border bg-fl-surface-2 p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-fl-muted-2'>Vocabulary sets</p><p className='mt-1 text-lg font-black text-fl-fg'>{unit.vocabulary_set_ids.length}</p></div>
                <div className='rounded-2xl border border-fl-border bg-fl-surface-2 p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-fl-muted-2'>Competencies</p><p className='mt-1 text-lg font-black text-fl-fg'>{unit.competency_checklist.length}</p></div>
              </div>
              {unit.competency_checklist.length > 0 && <div className='mt-4 rounded-2xl border border-fl-border bg-fl-surface p-4'><p className='text-xs font-extrabold uppercase tracking-[.14em] text-fl-muted-2'>By the end of this unit</p><ul className='mt-2 space-y-1.5 text-sm font-medium leading-6 text-fl-muted-2'>{unit.competency_checklist.slice(0, 2).map((item) => <li key={item} className='flex gap-2'><span className='text-[var(--juba-primary)]'>•</span><span>{item}</span></li>)}</ul></div>}
            </div></div>
              <div className='w-full lg:max-w-sm'><div className='flex items-center justify-between text-sm font-bold text-fl-fg'><span>{progress}% mastery</span><span>{lessons.length} lessons</span></div><div className='mt-2 h-2.5 overflow-hidden rounded-full bg-fl-surface-2'><div className='h-full rounded-full bg-[var(--juba-warm)]' style={{ width: progress + '%' }} /></div>
              {canOpen && lessons.length > 0 ? <div className='mt-4 space-y-2'>{lessons.slice(0, 3).map((lesson) => <Link key={lesson.id} href={lesson.available || lesson.is_completed ? '/lesson/' + lesson.id : '#'} className='flex items-center justify-between rounded-xl border border-fl-border bg-fl-surface-2 px-4 py-3 text-sm font-bold text-fl-fg'><span className='truncate'>{lesson.title}</span>{lesson.is_completed ? <CheckCircle2 className='h-4 w-4 shrink-0' /> : <ArrowRight className='h-4 w-4 shrink-0' />}</Link>)}</div> : canOpen ? <Link href='/plan' className='mt-4 inline-flex items-center gap-2 rounded-xl bg-[var(--juba-primary-soft)] px-4 py-2.5 text-sm font-bold text-[var(--juba-primary-dark)]'>Open plan <ArrowRight className='h-4 w-4' /></Link> : <span className='mt-4 inline-flex items-center gap-2 rounded-xl bg-fl-surface-2 px-4 py-2.5 text-sm font-bold text-fl-muted-2'><LockKeyhole className='h-4 w-4' /> Locked</span>}</div></div>
            </article>
          })}
        </section>
        {isCurrentLevel && <section className='juba-card flex flex-col gap-5 p-6 sm:flex-row sm:items-center sm:justify-between'><div><p className='juba-eyebrow'>Keep moving</p><h2 className='mt-2 text-2xl font-black text-fl-fg'>Continue your active plan.</h2><p className='mt-1 text-sm text-fl-muted-2'>Open the generated daily lessons and keep the journey moving.</p></div><Link href='/plan' className='inline-flex items-center justify-center gap-2 rounded-xl bg-[var(--juba-text)] px-5 py-3 font-bold text-[var(--juba-surface)]'>Open learning plan <BookOpen className='h-4 w-4' /></Link></section>}
      </div>
    </main>
  )
}