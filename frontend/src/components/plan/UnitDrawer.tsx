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
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-[rgba(36,36,36,.48)] p-0 backdrop-blur-sm sm:items-center sm:p-4" role="dialog" aria-modal="true" aria-label={unit.title}>
      <div
        ref={ref}
        className="flex max-h-[88vh] w-full flex-col overflow-hidden rounded-t-[24px] border-2 border-[var(--juba-learning-border)] bg-white shadow-[0_24px_70px_rgba(36,36,36,.18)] sm:max-w-xl sm:rounded-[24px]"
      >
        {/* Header */}
        <div className="sticky top-0 z-10 flex items-center justify-between gap-4 border-b-2 border-[var(--juba-learning-border)] bg-white px-5 py-4 sm:px-6">
          <div className="min-w-0">
            <span
              className="inline-flex rounded-full bg-[var(--juba-learning-green-soft)] px-2.5 py-1 text-xs font-black text-[var(--juba-learning-green-dark)]"
            >
              {unit.level} · {t('unitLabel')}
            </span>
            <p className="mt-1 truncate text-base font-black text-[var(--juba-learning-ink)]">
              {unit.title}
            </p>
          </div>
          <button
            onClick={onClose}
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border-2 border-[var(--juba-learning-border)] bg-white text-[var(--juba-learning-muted)] shadow-[0_2px_0_rgba(0,0,0,.05)] transition-colors hover:border-[var(--juba-learning-green)] hover:bg-[var(--juba-learning-green-soft)] hover:text-[var(--juba-learning-green-dark)]"
            aria-label={tCommon('close')}
          >
            <X className="h-4.5 w-4.5" aria-hidden="true" />
          </button>
        </div>

        {/* Grammar points */}
        {unit.grammar_points.length > 0 && (
          <div className="border-b-2 border-[var(--juba-learning-border)] px-5 py-5 sm:px-6">
            <p className="mb-2.5 text-xs font-black uppercase tracking-wide text-[var(--juba-learning-muted)]">
              {t('grammarCovered')}
            </p>
            <div className="flex flex-wrap gap-1.5">
              {unit.grammar_points.map((gp) => (
                <span
                  key={gp}
                  className="rounded-full border-2 border-[var(--juba-learning-border)] bg-[var(--juba-learning-green-soft)] px-2.5 py-1 text-xs font-bold text-[var(--juba-learning-green-dark)]"
                >
                  {gp}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Lessons */}
        <div>
          <div className="border-b-2 border-[var(--juba-learning-border)] bg-[#fafafa] px-5 py-3 sm:px-6">
            <p className="text-xs font-black uppercase tracking-wide text-[var(--juba-learning-muted)]">
              {t('lessonsHeader', { count: lessons.length })}
            </p>
          </div>
          <div className="divide-y-2 divide-[var(--juba-learning-border)]">
            {lessons.length === 0 ? (
              <div className="px-5 py-6 sm:px-6">
                <p className="text-sm font-semibold text-[var(--juba-learning-muted)]">{t('noLessons')}</p>
              </div>
            ) : (
              lessons.map((lesson, i) => (
                <div
                  key={lesson.id ?? i}
                  className="flex items-center gap-3 px-5 py-4 sm:px-6"
                >
                  {lesson.completed ? (
                    <span
                      className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 border-[var(--juba-learning-green-dark)] bg-[var(--juba-learning-green)] text-white shadow-[0_2px_0_var(--juba-learning-green-dark)]"
                    >
                      <Check className="h-3.5 w-3.5" aria-hidden="true" />
                    </span>
                  ) : (
                    <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 border-[var(--juba-learning-border)] bg-white text-[var(--juba-learning-muted)]">
                      <Circle className="h-2.5 w-2.5" aria-hidden="true" />
                    </span>
                  )}
                  <div className="min-w-0 flex-1">
                    <p
                      className={`truncate text-sm font-medium ${lesson.completed ? 'text-[var(--juba-learning-muted)] line-through' : 'text-[var(--juba-learning-ink)]'}`}
                    >
                      {lesson.title}
                    </p>
                    <p className="mt-0.5 text-xs font-semibold text-[var(--juba-learning-muted)]">
                      {t('weekDay', { week: lesson.week, day: lesson.day })} ·{' '}
                      {lessonTypeLabel[lesson.lesson_type] ??
                        lesson.lesson_type}
                    </p>
                  </div>
                  {lesson.id != null && lesson.action && (
                    <button
                      onClick={() => onStartLesson(lesson.id!)}
                      className="min-h-10 shrink-0 rounded-[12px] border-2 border-[var(--juba-learning-green-dark)] bg-[var(--juba-learning-green)] px-3 py-2 text-xs font-black text-white shadow-[0_3px_0_var(--juba-learning-green-dark)] transition-transform hover:translate-y-0.5"
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
        <div className="border-t-2 border-[var(--juba-learning-border)] bg-white px-5 py-4 sm:px-6">
          <div className="grid gap-2 sm:grid-cols-2">
            <button
              onClick={onStartUnit}
              className="min-h-11 w-full rounded-[13px] border-2 border-[var(--juba-learning-green-dark)] bg-[var(--juba-learning-green)] px-5 py-2.5 text-sm font-black text-white shadow-[0_4px_0_var(--juba-learning-green-dark)] transition-transform hover:translate-y-0.5"
            >
              {tCommon('start')} →
            </button>
            <button
              onClick={onClose}
              className="min-h-11 w-full rounded-[13px] border-2 border-[var(--juba-learning-border)] bg-white px-5 py-2.5 text-sm font-black text-[var(--juba-learning-ink)] shadow-[0_3px_0_rgba(0,0,0,.05)] transition-transform hover:translate-y-0.5"
            >
              {tCommon('close')}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
