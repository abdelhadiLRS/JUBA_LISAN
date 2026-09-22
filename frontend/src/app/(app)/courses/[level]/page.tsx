'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, ArrowRight, BookOpen, CheckCircle2, LockKeyhole, Sparkles } from 'lucide-react'
import { useParams } from 'next/navigation'
import { apiFetch } from '@/lib/api'
import { CEFR_LEVELS, getCurriculumUnits, type CEFRLevel, type CurriculumUnit } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
import { useTranslations } from 'next-intl'

interface StudyPlan { cefr_level: CEFRLevel }
interface JourneyUnit { id: string; progress: number; state: string; lessons?: Array<{ id: number; title: string; lesson_type: string; is_completed: boolean; available: boolean; state: string }> }
interface JourneyResponse { sections?: Array<{ units?: JourneyUnit[] }> }


export default function CourseLevelPage() {
  const params = useParams()
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const t = useTranslations('courseLevel')
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

  const formatLessonType = (type: string) => {
    const normalized = type.trim().toLowerCase()
    if (/listen|audio/.test(normalized)) return t('lessonTypes.listening')
    if (/read/.test(normalized)) return t('lessonTypes.reading')
    if (/write/.test(normalized)) return t('lessonTypes.writing')
    if (/grammar/.test(normalized)) return t('lessonTypes.grammar')
    if (/vocab/.test(normalized)) return t('lessonTypes.vocabulary')
    if (/review/.test(normalized)) return t('lessonTypes.review')
    return type
  }

  if (!level) return <main className='mx-auto max-w-4xl px-4 py-16'><div className='juba-card p-8 text-center'><p className='juba-eyebrow justify-center'>{t('notFound')}</p><h1 className='mt-3 text-3xl font-black text-fl-fg'>{t('choose')}</h1><Link href='/courses' className='mt-6 inline-flex items-center gap-2 rounded-xl bg-[var(--juba-primary-soft)] px-5 py-3 font-bold text-[var(--juba-primary-dark)]'>{t('back')} <ArrowRight className='h-4 w-4' /></Link></div></main>

  return (
    <main className='min-h-screen px-4 py-8 sm:px-6 lg:px-10'>
      <div className='mx-auto max-w-6xl space-y-7'>
        <Link href='/courses' className='inline-flex items-center gap-2 text-sm font-bold text-fl-muted hover:text-fl-fg'><ArrowLeft className='h-4 w-4' /> {t('all')}</Link>
        <section className='juba-card relative overflow-hidden p-7 sm:p-10'>
          <div className='relative z-10 max-w-3xl'><div className='juba-eyebrow'><Sparkles className='h-4 w-4' /> {t('cefrLevel')} {level}</div><h1 className='mt-4 text-4xl font-black tracking-tight text-fl-fg sm:text-6xl'>{t(`levels.${level}.title`)}</h1><p className='mt-4 text-base leading-7 text-fl-muted-2 sm:text-lg'>{t(`levels.${level}.description`)}</p><div className='mt-6 flex flex-wrap gap-3 text-sm font-bold text-fl-fg'><span className='rounded-full border border-fl-border bg-fl-surface-2 px-4 py-2'>{units.length} {t('units')}</span>{isCurrentLevel && <><span className='rounded-full border border-fl-border bg-fl-surface-2 px-4 py-2'>{totals.completed} {t('completed')}</span><span className='rounded-full border border-fl-border bg-fl-surface-2 px-4 py-2'>{totals.available} {t('ready')}</span></>}</div></div>
          <div className='juba-hero-glow' aria-hidden='true' />
        </section>
        {!loading && !levelUnlocked && <div className='juba-card flex items-start gap-4 border-dashed p-6'><LockKeyhole className='mt-1 h-5 w-5 shrink-0 text-fl-muted-2' /><div><h2 className='font-black text-fl-fg'>{t('notUnlocked')}</h2><p className='mt-1 text-sm leading-6 text-fl-muted-2'>{t('unlockDesc')}</p></div></div>}
        <section className='space-y-4'>
          {loading ? Array.from({ length: 4 }, (_, index) => <div key={index} className='juba-card h-40 animate-pulse' />) : units.map((unit) => {
            const journey = journeyUnits[unit.id]
            const progress = Math.round((journey?.progress ?? 0) * 100)
            const lessons = journey?.lessons ?? []
            const listeningCount = lessons.filter((lesson) => /listen|listening|audio/i.test(lesson.lesson_type)).length
            const readingCount = lessons.filter((lesson) => /read|reading/i.test(lesson.lesson_type)).length
            const state = journey?.state ?? (unit.prerequisite_unit ? 'locked' : 'available')
            const canOpen = levelUnlocked && state !== 'locked'
            return (
              <article key={unit.id} className={state === 'completed' ? 'juba-card p-6 ring-1 ring-[var(--juba-primary)]' : 'juba-card p-6'}>
              <div className='flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between'><div className='min-w-0'><div className='flex items-center gap-3'><span className='flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-[var(--juba-primary-soft)] text-sm font-black text-[var(--juba-primary-dark)]'>{String(unit.unit_number).padStart(2, '0')}</span><div><p className='text-xs font-bold uppercase tracking-[.16em] text-fl-muted-2'>{unit.level} · {t('unit')} {unit.unit_number}</p><h2 className='mt-1 text-xl font-black text-fl-fg'>{unit.title}</h2></div></div>
              <div className='mt-5 flex flex-wrap gap-2'>{unit.lesson_types.map((type) => <span key={type} className='rounded-full border border-fl-border bg-fl-surface-2 px-3 py-1 text-xs font-bold text-fl-muted'>{formatLessonType(type)}</span>)}{unit.grammar_points.slice(0, 3).map((point) => <span key={point} className='rounded-full border border-fl-border bg-fl-surface px-3 py-1 text-xs text-fl-muted-2'>{point}</span>)}</div>
              <div className='mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-5'>
                <div className='rounded-2xl border border-fl-border bg-fl-surface-2 p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-fl-muted-2'>{t('grammar')}</p><p className='mt-1 text-lg font-black text-fl-fg'>{unit.grammar_points.length}</p></div>
                <div className='rounded-2xl border border-fl-border bg-fl-surface-2 p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-fl-muted-2'>{t('vocab')}</p><p className='mt-1 text-lg font-black text-fl-fg'>{unit.vocabulary_set_ids.length}</p></div>
                <div className='rounded-2xl border border-fl-border bg-fl-surface-2 p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-fl-muted-2'>{t('competencies')}</p><p className='mt-1 text-lg font-black text-fl-fg'>{unit.competency_checklist.length}</p></div>
                <div className='rounded-2xl border border-fl-border bg-fl-surface-2 p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-fl-muted-2'>{t('listening')}</p><p className='mt-1 text-lg font-black text-fl-fg'>{listeningCount}</p></div>
                <div className='rounded-2xl border border-fl-border bg-fl-surface-2 p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-fl-muted-2'>{t('reading')}</p><p className='mt-1 text-lg font-black text-fl-fg'>{readingCount}</p></div>
              </div>
              {unit.competency_checklist.length > 0 && <div className='mt-4 rounded-2xl border border-fl-border bg-fl-surface p-4'><p className='text-xs font-extrabold uppercase tracking-[.14em] text-fl-muted-2'>{t('byEnd')}</p><ul className='mt-2 space-y-1.5 text-sm font-medium leading-6 text-fl-muted-2'>{unit.competency_checklist.slice(0, 2).map((item) => <li key={item} className='flex gap-2'><span className='text-[var(--juba-primary)]'>•</span><span>{item}</span></li>)}</ul></div>}
            </div></div>
              <div className='w-full lg:max-w-sm'><div className='flex items-center justify-between text-sm font-bold text-fl-fg'><span>{progress}% {t('mastery')}</span><span>{lessons.length} {t('lessons')}</span></div><div className='mt-2 h-2.5 overflow-hidden rounded-full bg-fl-surface-2' role='progressbar' aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress} aria-label={`${progress}% ${t('mastery')}`}><div className='h-full rounded-full bg-[var(--juba-warm)]' style={{ width: progress + '%' }} /></div>
              {canOpen && lessons.length > 0 ? (
                <div className='mt-4 space-y-2'>
                  {lessons.slice(0, 3).map((lesson) => (
                    lesson.available || lesson.is_completed ? (
                      <Link
                        key={lesson.id}
                        href={'/lesson/' + lesson.id}
                        aria-label={lesson.title + ' — ' + formatLessonType(lesson.lesson_type)}
                        className='flex items-center justify-between rounded-xl border border-fl-border bg-fl-surface-2 px-4 py-3 text-sm font-bold text-fl-fg'
                      >
                        <span className='min-w-0 truncate'>{lesson.title}</span>
                        <span className='shrink-0 rounded-full border border-fl-border bg-fl-surface px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wide text-fl-muted-2'>
                          {formatLessonType(lesson.lesson_type)}
                        </span>
                        {lesson.is_completed ? (
                          <CheckCircle2 aria-hidden='true' className='h-4 w-4 shrink-0' />
                        ) : (
                          <ArrowRight aria-hidden='true' className='h-4 w-4 shrink-0' />
                        )}
                      </Link>
                    ) : (
                      <div
                        key={lesson.id}
                        aria-disabled='true'
                        aria-label={lesson.title + ' — ' + t('locked')}
                        className='flex items-center justify-between rounded-xl border border-fl-border bg-fl-surface-2 px-4 py-3 text-sm font-bold text-fl-muted-2'
                      >
                        <span className='truncate'>{lesson.title}</span>
                        <LockKeyhole aria-hidden='true' className='h-4 w-4 shrink-0' />
                      </div>
                    )
                  ))}
                </div>
              ) : canOpen ? (
                <Link href='/plan' className='mt-4 inline-flex items-center gap-2 rounded-xl bg-[var(--juba-primary-soft)] px-4 py-2.5 text-sm font-bold text-[var(--juba-primary-dark)]'>
                  {t('openPlan')} <ArrowRight className='h-4 w-4' />
                </Link>
              ) : (
                <span className='mt-4 inline-flex items-center gap-2 rounded-xl bg-fl-surface-2 px-4 py-2.5 text-sm font-bold text-fl-muted-2'>
                  <LockKeyhole className='h-4 w-4' /> {t('locked')}
                </span>
              )}</div></div>
              </article>
            )
          })}
        </section>
        {isCurrentLevel && <section className='juba-card flex flex-col gap-5 p-6 sm:flex-row sm:items-center sm:justify-between'><div><p className='juba-eyebrow'>{t('keepMoving')}</p><h2 className='mt-2 text-2xl font-black text-fl-fg'>{t('continue')}</h2><p className='mt-1 text-sm text-fl-muted-2'>{t('continueDesc')}</p></div><Link href='/plan' className='inline-flex items-center justify-center gap-2 rounded-xl bg-[var(--juba-text)] px-5 py-3 font-bold text-[var(--juba-surface)]'>{t('openLearning')} <BookOpen className='h-4 w-4' /></Link></section>}
      </div>
    </main>
  )
}