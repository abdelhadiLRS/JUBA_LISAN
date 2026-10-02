'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
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
    const curriculumLevel = level
    let cancelled = false
    async function load() {
      setLoading(true)
      const language = activeLanguage?.code ?? 'en-GB'
      const [curriculum, planRes, journeyRes] = await Promise.all([
        getCurriculumUnits(curriculumLevel, language).catch(() => []),
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

  if (!level) return <main className='juba-page-shell w-full px-4 py-5 sm:px-6 sm:py-6 lg:px-8 box-border'><div className='juba-reference-list-card p-8 text-center'><p className='juba-eyebrow justify-center'>{t('notFound')}</p><h1 className='mt-3 text-3xl font-black text-[var(--juba-ink,var(--juba-text))]'>{t('choose')}</h1><Link href='/courses' className='mt-6 inline-flex items-center gap-2 rounded-[12px] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] px-5 py-3 font-bold text-[var(--juba-green,var(--duo-green-dark))]'>{t('back')} <i className='ti ti-arrow-right icon icon-sm' aria-hidden='true' /></Link></div></main>

  return (
    <main className='juba-page-shell w-full px-4 py-5 sm:px-6 sm:py-6 lg:px-8 box-border'>
      <div className='w-full space-y-6'>
        <Link href='/courses' className='inline-flex items-center gap-2 text-sm font-bold text-[var(--juba-muted)] hover:text-[var(--juba-ink,var(--juba-text))]'><i className='ti ti-arrow-left icon icon-sm' aria-hidden='true' /> {t('all')}</Link>
        <section className='juba-reference-hero relative overflow-hidden rounded-[12px] border border-[var(--juba-green,var(--duo-green-dark))] bg-[var(--juba-green,var(--duo-green))] p-6 text-white shadow-sm sm:p-8'>
          <div className='relative z-10 max-w-3xl'><div className='juba-eyebrow'><i className='ti ti-sparkles icon icon-sm' aria-hidden='true' /> {t('cefrLevel')} {level}</div><h1 className='mt-4 text-3xl font-black tracking-[-0.03em] text-white sm:text-4xl'>{t(`levels.${level}.title`)}</h1><p className='mt-4 text-base leading-7 text-white/80 sm:text-base'>{t(`levels.${level}.description`)}</p><div className='mt-6 flex flex-wrap gap-3 text-sm font-bold text-[var(--juba-ink,var(--juba-text))]'><span className='rounded-full border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] px-4 py-2'>{units.length} {t('units')}</span>{isCurrentLevel && <><span className='rounded-full border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] px-4 py-2'>{totals.completed} {t('completed')}</span><span className='rounded-full border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] px-4 py-2'>{totals.available} {t('ready')}</span></>}</div></div>
          <div className='juba-hero-glow' aria-hidden='true' />
        </section>
        {!loading && !levelUnlocked && <div className='juba-reference-list-card flex items-start gap-4 border-dashed p-6'><LockKeyhole className='mt-1 h-5 w-5 shrink-0 text-[var(--juba-muted)]' /><div><h2 className='font-black text-[var(--juba-ink,var(--juba-text))]'>{t('notUnlocked')}</h2><p className='mt-1 text-sm leading-6 text-[var(--juba-muted)]'>{t('unlockDesc')}</p></div></div>}
        <section className='juba-reference-section space-y-4'>
          {loading ? Array.from({ length: 4 }, (_, index) => <div key={index} className='juba-card h-40 animate-pulse' />) : units.map((unit) => {
            const journey = journeyUnits[unit.id]
            const progress = Math.round((journey?.progress ?? 0) * 100)
            const lessons = journey?.lessons ?? []
            const listeningCount = lessons.filter((lesson) => /listen|listening|audio/i.test(lesson.lesson_type)).length
            const readingCount = lessons.filter((lesson) => /read|reading/i.test(lesson.lesson_type)).length
            const state = journey?.state ?? (unit.prerequisite_unit ? 'locked' : 'available')
            const canOpen = levelUnlocked && state !== 'locked'
            return (
              <article key={unit.id} className={state === 'completed' ? 'juba-reference-list-card p-6 ring-1 ring-[var(--duo-green)]' : 'juba-reference-list-card p-6'}>
              <div className='flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between'><div className='min-w-0'><div className='flex items-center gap-3'><span className='flex h-10 w-10 shrink-0 items-center justify-center rounded-[12px] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] text-sm font-black text-[var(--juba-green,var(--duo-green-dark))]'>{String(unit.unit_number).padStart(2, '0')}</span><div><p className='text-xs font-bold uppercase tracking-[.16em] text-[var(--juba-muted)]'>{unit.level} · {t('unit')} {unit.unit_number}</p><h2 className='mt-1 text-xl font-black text-[var(--juba-ink,var(--juba-text))]'>{unit.title}</h2></div></div>
              <div className='mt-5 flex flex-wrap gap-2'>{unit.lesson_types.map((type) => <span key={type} className='rounded-full border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] px-3 py-1 text-xs font-bold text-[var(--juba-muted)]'>{formatLessonType(type)}</span>)}{unit.grammar_points.slice(0, 3).map((point) => <span key={point} className='rounded-full border border-[var(--juba-border)] bg-[var(--juba-card,var(--juba-card,var(--duo-card)))] px-3 py-1 text-xs text-[var(--juba-muted)]'>{point}</span>)}</div>
              <div className='mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-5'>
                <div className='rounded-[12px] border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-[var(--juba-muted)]'>{t('grammar')}</p><p className='mt-1 text-lg font-black text-[var(--juba-ink,var(--juba-text))]'>{unit.grammar_points.length}</p></div>
                <div className='rounded-[12px] border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-[var(--juba-muted)]'>{t('vocab')}</p><p className='mt-1 text-lg font-black text-[var(--juba-ink,var(--juba-text))]'>{unit.vocabulary_set_ids.length}</p></div>
                <div className='rounded-[12px] border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-[var(--juba-muted)]'>{t('competencies')}</p><p className='mt-1 text-lg font-black text-[var(--juba-ink,var(--juba-text))]'>{unit.competency_checklist.length}</p></div>
                <div className='rounded-[12px] border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-[var(--juba-muted)]'>{t('listening')}</p><p className='mt-1 text-lg font-black text-[var(--juba-ink,var(--juba-text))]'>{listeningCount}</p></div>
                <div className='rounded-[12px] border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-[var(--juba-muted)]'>{t('reading')}</p><p className='mt-1 text-lg font-black text-[var(--juba-ink,var(--juba-text))]'>{readingCount}</p></div>
              </div>
              {unit.competency_checklist.length > 0 && <div className='mt-4 rounded-[12px] border border-[var(--juba-border)] bg-[var(--juba-card,var(--juba-card,var(--duo-card)))] p-4'><p className='text-xs font-extrabold uppercase tracking-[.14em] text-[var(--juba-muted)]'>{t('byEnd')}</p><ul className='mt-2 space-y-1.5 text-sm font-medium leading-6 text-[var(--juba-muted)]'>{unit.competency_checklist.slice(0, 2).map((item) => <li key={item} className='flex gap-2'><span className='text-[var(--juba-green,var(--duo-green-dark))]'>•</span><span>{item}</span></li>)}</ul></div>}
            </div>
              <div className='w-full lg:max-w-sm'><div className='flex items-center justify-between text-sm font-bold text-[var(--juba-ink,var(--juba-text))]'><span>{progress}% {t('mastery')}</span><span>{lessons.length} {t('lessons')}</span></div><div className='mt-2 h-2.5 overflow-hidden rounded-full bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))]' role='progressbar' aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress} aria-label={`${progress}% ${t('mastery')}`}><div className='h-full rounded-full bg-[var(--duo-green)]' style={{ width: progress + '%' }} /></div>
              {canOpen && lessons.length > 0 ? (
                <div className='mt-4 space-y-2'>
                  {lessons.slice(0, 3).map((lesson) => (
                    lesson.available || lesson.is_completed ? (
                      <Link
                        key={lesson.id}
                        href={'/lesson/' + lesson.id}
                        aria-label={lesson.title + ' — ' + formatLessonType(lesson.lesson_type)}
                        className='flex items-center justify-between rounded-[12px] border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] px-4 py-3 text-sm font-bold text-[var(--juba-ink,var(--juba-text))]'
                      >
                        <span className='min-w-0 truncate'>{lesson.title}</span>
                        <span className='shrink-0 rounded-full border border-[var(--juba-border)] bg-[var(--juba-card,var(--juba-card,var(--duo-card)))] px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wide text-[var(--juba-muted)]'>
                          {formatLessonType(lesson.lesson_type)}
                        </span>
                        {lesson.is_completed ? (
                          <i aria-hidden='true' className='ti ti-circle-check icon icon-sm shrink-0' />
                        ) : (
                          <ArrowRight aria-hidden='true' className='h-4 w-4 shrink-0' />
                        )}
                      </Link>
                    ) : (
                      <div
                        key={lesson.id}
                        aria-disabled='true'
                        aria-label={lesson.title + ' — ' + t('locked')}
                        className='flex items-center justify-between rounded-[12px] border border-[var(--juba-border)] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] px-4 py-3 text-sm font-bold text-[var(--juba-muted)]'
                      >
                        <span className='truncate'>{lesson.title}</span>
                        <i aria-hidden='true' className='ti ti-lock icon icon-sm shrink-0' />
                      </div>
                    )
                  ))}
                </div>
              ) : canOpen ? (
                <Link href='/plan' className='mt-4 inline-flex items-center gap-2 rounded-[12px] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] px-4 py-2.5 text-sm font-bold text-[var(--juba-green,var(--duo-green-dark))]'>
                  {t('openPlan')} <i className='ti ti-arrow-right icon icon-sm' aria-hidden='true' />
                </Link>
              ) : (
                <span className='mt-4 inline-flex items-center gap-2 rounded-[12px] bg-[color-mix(in_srgb,var(--duo-green)_10%,var(--juba-card,var(--juba-card,var(--duo-card))))] px-4 py-2.5 text-sm font-bold text-[var(--juba-muted)]'>
                  <i className='ti ti-lock icon icon-sm' aria-hidden='true' /> {t('locked')}
                </span>
              )}</div></div>
              </article>
            )
          })}
        </section>
        {isCurrentLevel && <section className='juba-reference-section juba-reference-list-card flex flex-col gap-5 p-6 sm:flex-row sm:items-center sm:justify-between'><div><p className='juba-eyebrow'>{t('keepMoving')}</p><h2 className='mt-2 text-2xl font-black text-[var(--juba-ink,var(--juba-text))]'>{t('continue')}</h2><p className='mt-1 text-sm text-[var(--juba-muted)]'>{t('continueDesc')}</p></div><Link href='/plan' className='inline-flex items-center justify-center gap-2 rounded-[12px] bg-[var(--duo-ink,#202127)] px-5 py-3 font-bold text-[#fff]'>{t('openLearning')} <i className='ti ti-book icon icon-sm' aria-hidden='true' /></Link></section>}
      </div>
    </main>
  )
}