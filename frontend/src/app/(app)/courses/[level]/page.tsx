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

  if (!level) return <main className='mx-auto max-w-4xl px-4 py-16'><div className='juba-card p-8 text-center'><p className='juba-eyebrow justify-center'>{t('notFound')}</p><h1 className='mt-3 text-3xl font-black text-[#202127]'>{t('choose')}</h1><Link href='/courses' className='mt-6 inline-flex items-center gap-2 rounded-[20px] bg-[#ededff] px-5 py-3 font-bold text-[#373fb8]'>{t('back')} <ArrowRight className='h-4 w-4' /></Link></div></main>

  return (
    <main className='min-h-screen px-4 py-8 sm:px-6 lg:px-10'>
      <div className='mx-auto max-w-6xl space-y-7'>
        <Link href='/courses' className='inline-flex items-center gap-2 text-sm font-bold text-[rgba(32,33,39,.52)] hover:text-[#202127]'><ArrowLeft className='h-4 w-4' /> {t('all')}</Link>
        <section className='relative overflow-hidden rounded-[26px] border border-[#5862e2] bg-[#5862e2] p-7 text-white shadow-[0 12px 30px rgba(43,45,90,.055)] sm:p-10'>
          <div className='relative z-10 max-w-3xl'><div className='juba-eyebrow'><Sparkles className='h-4 w-4' /> {t('cefrLevel')} {level}</div><h1 className='mt-4 text-4xl font-black tracking-tight text-[#202127] sm:text-6xl'>{t(`levels.${level}.title`)}</h1><p className='mt-4 text-base leading-7 text-[rgba(32,33,39,.52)] sm:text-lg'>{t(`levels.${level}.description`)}</p><div className='mt-6 flex flex-wrap gap-3 text-sm font-bold text-[#202127]'><span className='rounded-full border border-[rgba(7,7,9,.08)] bg-[#ededff] px-4 py-2'>{units.length} {t('units')}</span>{isCurrentLevel && <><span className='rounded-full border border-[rgba(7,7,9,.08)] bg-[#ededff] px-4 py-2'>{totals.completed} {t('completed')}</span><span className='rounded-full border border-[rgba(7,7,9,.08)] bg-[#ededff] px-4 py-2'>{totals.available} {t('ready')}</span></>}</div></div>
          <div className='juba-hero-glow' aria-hidden='true' />
        </section>
        {!loading && !levelUnlocked && <div className='juba-card flex items-start gap-4 border-dashed p-6'><LockKeyhole className='mt-1 h-5 w-5 shrink-0 text-[rgba(32,33,39,.52)]' /><div><h2 className='font-black text-[#202127]'>{t('notUnlocked')}</h2><p className='mt-1 text-sm leading-6 text-[rgba(32,33,39,.52)]'>{t('unlockDesc')}</p></div></div>}
        <section className='space-y-4'>
          {loading ? Array.from({ length: 4 }, (_, index) => <div key={index} className='rounded-[28px] border border-[#ededff] bg-white h-40 animate-pulse' />) : units.map((unit) => {
            const journey = journeyUnits[unit.id]
            const progress = Math.round((journey?.progress ?? 0) * 100)
            const lessons = journey?.lessons ?? []
            const listeningCount = lessons.filter((lesson) => /listen|listening|audio/i.test(lesson.lesson_type)).length
            const readingCount = lessons.filter((lesson) => /read|reading/i.test(lesson.lesson_type)).length
            const state = journey?.state ?? (unit.prerequisite_unit ? 'locked' : 'available')
            const canOpen = levelUnlocked && state !== 'locked'
            return (
              <article key={unit.id} className={state === 'completed' ? 'juba-card p-6 ring-2 ring-[#5862e2]' : 'juba-card p-6'}>
              <div className='flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between'><div className='min-w-0'><div className='flex items-center gap-3'><span className='flex h-10 w-10 shrink-0 items-center justify-center rounded-[24px] bg-[#ededff] text-sm font-black text-[#373fb8]'>{String(unit.unit_number).padStart(2, '0')}</span><div><p className='text-xs font-bold uppercase tracking-[.16em] text-[rgba(32,33,39,.52)]'>{unit.level} · {t('unit')} {unit.unit_number}</p><h2 className='mt-1 text-xl font-black text-[#202127]'>{unit.title}</h2></div></div>
              <div className='mt-5 flex flex-wrap gap-2'>{unit.lesson_types.map((type) => <span key={type} className='rounded-full border border-[rgba(7,7,9,.08)] bg-[#ededff] px-3 py-1 text-xs font-bold text-[rgba(32,33,39,.52)]'>{formatLessonType(type)}</span>)}{unit.grammar_points.slice(0, 3).map((point) => <span key={point} className='rounded-full border border-[rgba(7,7,9,.08)] bg-[#fff] px-3 py-1 text-xs text-[rgba(32,33,39,.52)]'>{point}</span>)}</div>
              <div className='mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-5'>
                <div className='rounded-[24px] border border-[rgba(7,7,9,.08)] bg-[#ededff] p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-[rgba(32,33,39,.52)]'>{t('grammar')}</p><p className='mt-1 text-lg font-black text-[#202127]'>{unit.grammar_points.length}</p></div>
                <div className='rounded-[24px] border border-[rgba(7,7,9,.08)] bg-[#ededff] p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-[rgba(32,33,39,.52)]'>{t('vocab')}</p><p className='mt-1 text-lg font-black text-[#202127]'>{unit.vocabulary_set_ids.length}</p></div>
                <div className='rounded-[24px] border border-[rgba(7,7,9,.08)] bg-[#ededff] p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-[rgba(32,33,39,.52)]'>{t('competencies')}</p><p className='mt-1 text-lg font-black text-[#202127]'>{unit.competency_checklist.length}</p></div>
                <div className='rounded-[24px] border border-[rgba(7,7,9,.08)] bg-[#ededff] p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-[rgba(32,33,39,.52)]'>{t('listening')}</p><p className='mt-1 text-lg font-black text-[#202127]'>{listeningCount}</p></div>
                <div className='rounded-[24px] border border-[rgba(7,7,9,.08)] bg-[#ededff] p-3'><p className='text-[11px] font-extrabold uppercase tracking-[.14em] text-[rgba(32,33,39,.52)]'>{t('reading')}</p><p className='mt-1 text-lg font-black text-[#202127]'>{readingCount}</p></div>
              </div>
              {unit.competency_checklist.length > 0 && <div className='mt-4 rounded-[24px] border border-[rgba(7,7,9,.08)] bg-[#fff] p-4'><p className='text-xs font-extrabold uppercase tracking-[.14em] text-[rgba(32,33,39,.52)]'>{t('byEnd')}</p><ul className='mt-2 space-y-1.5 text-sm font-medium leading-6 text-[rgba(32,33,39,.52)]'>{unit.competency_checklist.slice(0, 2).map((item) => <li key={item} className='flex gap-2'><span className='text-[#5862e2]'>•</span><span>{item}</span></li>)}</ul></div>}
            </div>
              <div className='w-full lg:max-w-sm'><div className='flex items-center justify-between text-sm font-bold text-[#202127]'><span>{progress}% {t('mastery')}</span><span>{lessons.length} {t('lessons')}</span></div><div className='mt-2 h-2.5 overflow-hidden rounded-full bg-[#ededff]' role='progressbar' aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress} aria-label={`${progress}% ${t('mastery')}`}><div className='h-full rounded-full bg-[#fff3d1]' style={{ width: progress + '%' }} /></div>
              {canOpen && lessons.length > 0 ? (
                <div className='mt-4 space-y-2'>
                  {lessons.slice(0, 3).map((lesson) => (
                    lesson.available || lesson.is_completed ? (
                      <Link
                        key={lesson.id}
                        href={'/lesson/' + lesson.id}
                        aria-label={lesson.title + ' — ' + formatLessonType(lesson.lesson_type)}
                        className='flex items-center justify-between rounded-[20px] border border-[rgba(7,7,9,.08)] bg-[#ededff] px-4 py-3 text-sm font-bold text-[#202127]'
                      >
                        <span className='min-w-0 truncate'>{lesson.title}</span>
                        <span className='shrink-0 rounded-full border border-[rgba(7,7,9,.08)] bg-[#fff] px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wide text-[rgba(32,33,39,.52)]'>
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
                        className='flex items-center justify-between rounded-[20px] border border-[rgba(7,7,9,.08)] bg-[#ededff] px-4 py-3 text-sm font-bold text-[rgba(32,33,39,.52)]'
                      >
                        <span className='truncate'>{lesson.title}</span>
                        <LockKeyhole aria-hidden='true' className='h-4 w-4 shrink-0' />
                      </div>
                    )
                  ))}
                </div>
              ) : canOpen ? (
                <Link href='/plan' className='mt-4 inline-flex items-center gap-2 rounded-[20px] bg-[#ededff] px-4 py-2.5 text-sm font-bold text-[#373fb8]'>
                  {t('openPlan')} <ArrowRight className='h-4 w-4' />
                </Link>
              ) : (
                <span className='mt-4 inline-flex items-center gap-2 rounded-[20px] bg-[#ededff] px-4 py-2.5 text-sm font-bold text-[rgba(32,33,39,.52)]'>
                  <LockKeyhole className='h-4 w-4' /> {t('locked')}
                </span>
              )}</div></div>
              </article>
            )
          })}
        </section>
        {isCurrentLevel && <section className='rounded-[28px] border border-[#ededff] bg-white flex flex-col gap-5 p-6 sm:flex-row sm:items-center sm:justify-between'><div><p className='juba-eyebrow'>{t('keepMoving')}</p><h2 className='mt-2 text-2xl font-black text-[#202127]'>{t('continue')}</h2><p className='mt-1 text-sm text-[rgba(32,33,39,.52)]'>{t('continueDesc')}</p></div><Link href='/plan' className='inline-flex items-center justify-center gap-2 rounded-[20px] bg-[#202127] px-5 py-3 font-bold text-[#fff]'>{t('openLearning')} <BookOpen className='h-4 w-4' /></Link></section>}
      </div>
    </main>
  )
}