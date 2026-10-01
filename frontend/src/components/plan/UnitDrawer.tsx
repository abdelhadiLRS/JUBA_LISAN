'use client'

import { useEffect, useRef } from 'react'
import { useTranslations } from 'next-intl'
import { Check, Circle, X } from 'lucide-react'
import type { CurriculumUnit } from '@/data/curriculum'

interface Lesson {
  id: number | null
  title: string
  lesson_type: string
  week: number
  day: number
  completed: boolean
  action?: 'start' | 'continue' | 'review'
}

interface Props {
  unit: CurriculumUnit
  lessons: Lesson[]
  onClose: () => void
  onStartLesson: (lessonId: number) => void
  onStartUnit: () => void
}

export default function UnitDrawer({
  unit,
  lessons,
  onClose,
  onStartLesson,
  onStartUnit,
}: Props) {
  const t = useTranslations('plan')
  const tCommon = useTranslations('common')
  const ref = useRef<HTMLDivElement>(null)

  // Close on outside click
  useEffect(() => {
    function handler(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose()
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [onClose])

  // Close on Escape
  useEffect(() => {
    function handler(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [onClose])

  const lessonTypeLabel: Record<string, string> = {
    grammar: t('lessonTypes.grammar'),
    vocabulary: t('lessonTypes.vocabulary'),
    reading: t('lessonTypes.reading'),
    writing: t('lessonTypes.writing'),
    listening: t('lessonTypes.listening'),
    conversation: t('lessonTypes.conversation'),
    review: t('lessonTypes.review'),
    level_test: t('lessonTypes.level_test'),
  }

  return (
    <div className="bg-[color-mix(in_srgb,var(--duo-ink)_48%,transparent)] fixed inset-0 z-50 flex items-end justify-center p-0 backdrop-blur-sm sm:items-center sm:p-4">
      <div
        ref={ref}
        className="border-[var(--duo-line)] bg-[var(--duo-card)] max-h-[80vh] w-full overflow-y-auto rounded-t-[10px] border shadow-lg sm:max-w-xl sm:rounded-[10px]"
      >
        {/* Header */}
        <div className="border-[var(--duo-line)] bg-[var(--duo-card)] sticky top-0 z-10 flex items-center justify-between gap-4 border-b px-6 py-5 sm:px-7">
          <div className="min-w-0">
            <span
              className="text-xs font-semibold"
              style={{ color: 'var(--duo-green-dark)' }}
            >
              {unit.level} · {t('unitLabel')}
            </span>
            <p className="text-[var(--duo-ink)] mt-0.5 truncate text-base font-bold">
              {unit.title}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] shrink-0 rounded-[10px] p-2 transition-colors hover:bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-green)] focus-visible:ring-offset-2"
            aria-label={tCommon('close')}
          >
            <X className="h-4.5 w-4.5" aria-hidden="true" />
          </button>
        </div>

        {/* Grammar points */}
        {unit.grammar_points.length > 0 && (
          <div className="border-[var(--duo-line)] border-b px-6 py-5 sm:px-7">
            <p className="text-[var(--duo-muted)] mb-2.5 text-xs font-semibold tracking-wide uppercase">
              {t('grammarCovered')}
            </p>
            <div className="flex flex-wrap gap-1.5">
              {unit.grammar_points.map((gp) => (
                <span
                  key={gp}
                  className="bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] text-[var(--duo-muted)] rounded-full px-2.5 py-1 text-xs font-medium"
                >
                  {gp}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Lessons */}
        <div>
          <div className="border-[var(--duo-line)] border-b px-5 py-3 sm:px-6">
            <p className="text-[var(--duo-muted)] text-xs font-semibold tracking-wide uppercase">
              {t('lessonsHeader', { count: lessons.length })}
            </p>
          </div>
          <div className="divide-y divide-[var(--duo-line)]">
            {lessons.length === 0 ? (
              <div className="px-5 py-6 sm:px-6">
                <p className="text-[var(--duo-muted)] text-sm">{t('noLessons')}</p>
              </div>
            ) : (
              lessons.map((lesson, i) => (
                <div
                  key={lesson.id ?? i}
                  className={`flex items-center gap-3 px-5 py-3.5 transition-colors sm:px-6 ${lesson.action ? 'hover:bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)]' : ''}`}
                >
                  {lesson.completed ? (
                    <span
                      className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full"
                      style={{
                        background: 'var(--duo-green)',
                        color: 'var(--duo-ink)',
                      }}
                    >
                      <Check className="h-3.5 w-3.5" aria-hidden="true" />
                    </span>
                  ) : (
                    <span className="border-[var(--duo-line)] text-[var(--duo-muted)] flex h-6 w-6 shrink-0 items-center justify-center rounded-full border">
                      <Circle className="h-2.5 w-2.5" aria-hidden="true" />
                    </span>
                  )}
                  <div className="min-w-0 flex-1">
                    <p
                      className={`truncate text-sm font-medium ${lesson.completed ? 'text-[var(--duo-muted)] line-through' : 'text-[var(--duo-ink)]'}`}
                    >
                      {lesson.title}
                    </p>
                    <p className="text-[var(--duo-muted)] mt-0.5 text-xs">
                      {t('weekDay', { week: lesson.week, day: lesson.day })} ·{' '}
                      {lessonTypeLabel[lesson.lesson_type] ??
                        lesson.lesson_type}
                    </p>
                  </div>
                  {lesson.id != null && lesson.action && (
                    <button
                      onClick={() => onStartLesson(lesson.id!)}
                      className="shrink-0 bg-[var(--duo-green)] hover:bg-[var(--duo-green-dark)] text-white rounded-[10px] px-3 py-2 text-xs font-bold shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-green)] focus-visible:ring-offset-2"
                    >
                      {lesson.action === 'review'
                        ? t('reviewLesson')
                        : lesson.action === 'continue'
                          ? t('resume')
                          : `${t('startLearning')} →`}
                    </button>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Primary action */}
        <div className="border-[var(--duo-line)] bg-[var(--duo-card)] sticky bottom-0 border-t px-6 py-5 sm:px-7">
          <div className="grid gap-2 sm:grid-cols-2">
            <button
              onClick={onStartUnit}
              className="bg-[var(--duo-green)] hover:bg-[var(--duo-green-dark)] text-white w-full rounded-[10px] px-5 py-3 text-xs font-bold shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-green)] focus-visible:ring-offset-2"
            >
              {tCommon('start')} →
            </button>
            <button
              onClick={onClose}
              className="border border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-green)] hover:text-[var(--duo-green-dark)] w-full rounded-[10px] px-5 py-3 text-xs font-bold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-green)] focus-visible:ring-offset-2"
            >
              {tCommon('close')}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
