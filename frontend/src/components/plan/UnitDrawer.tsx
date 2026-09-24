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
}

export default function UnitDrawer({
  unit,
  lessons,
  onClose,
  onStartLesson,
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
    <div className="bg-[rgba(24,37,27,.48)] fixed inset-0 z-50 flex items-end justify-center p-0 backdrop-blur-sm sm:items-center sm:p-4">
      <div
        ref={ref}
        className="border-[var(--juba-app-line)] bg-white max-h-[80vh] w-full overflow-y-auto rounded-t-[30px] border shadow-[0_24px_70px_rgba(24,37,27,.18)] sm:max-w-xl sm:rounded-[30px]"
      >
        {/* Header */}
        <div className="border-[var(--juba-app-line)] bg-white sticky top-0 z-10 flex items-center justify-between gap-4 border-b px-6 py-5 sm:px-7">
          <div className="min-w-0">
            <span
              className="text-xs font-semibold"
              style={{ color: 'var(--juba-app-green-dark)' }}
            >
              {unit.level} · {t('unitLabel')}
            </span>
            <p className="text-[var(--juba-app-ink)] mt-0.5 truncate text-base font-bold">
              {unit.title}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] shrink-0 rounded-2xl p-2 transition-colors hover:bg-[var(--juba-app-green-soft)]"
            aria-label={tCommon('close')}
          >
            <X className="h-4.5 w-4.5" aria-hidden="true" />
          </button>
        </div>

        {/* Grammar points */}
        {unit.grammar_points.length > 0 && (
          <div className="border-[var(--juba-app-line)] border-b px-6 py-5 sm:px-7">
            <p className="text-[var(--juba-app-muted)] mb-2.5 text-xs font-semibold tracking-wide uppercase">
              {t('grammarCovered')}
            </p>
            <div className="flex flex-wrap gap-1.5">
              {unit.grammar_points.map((gp) => (
                <span
                  key={gp}
                  className="bg-[var(--juba-app-green-soft)] text-[var(--juba-app-muted)] rounded-full px-2.5 py-1 text-xs font-medium"
                >
                  {gp}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Lessons */}
        <div>
          <div className="border-[var(--juba-app-line)] border-b px-5 py-3 sm:px-6">
            <p className="text-[var(--juba-app-muted)] text-xs font-semibold tracking-wide uppercase">
              {t('lessonsHeader', { count: lessons.length })}
            </p>
          </div>
          <div className="divide-fl-border divide-y">
            {lessons.length === 0 ? (
              <div className="px-5 py-6 sm:px-6">
                <p className="text-[var(--juba-app-muted)] text-sm">{t('noLessons')}</p>
              </div>
            ) : (
              lessons.map((lesson, i) => (
                <div
                  key={lesson.id ?? i}
                  className={`flex items-center gap-3 px-5 py-3.5 transition-colors sm:px-6 ${lesson.action ? 'hover:bg-[var(--juba-app-green-soft)]' : ''}`}
                >
                  {lesson.completed ? (
                    <span
                      className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full"
                      style={{
                        background: 'var(--juba-app-green)',
                        color: 'var(--juba-app-ink)',
                      }}
                    >
                      <Check className="h-3.5 w-3.5" aria-hidden="true" />
                    </span>
                  ) : (
                    <span className="border-[var(--juba-app-line)] text-[var(--juba-app-muted)] flex h-6 w-6 shrink-0 items-center justify-center rounded-full border">
                      <Circle className="h-2.5 w-2.5" aria-hidden="true" />
                    </span>
                  )}
                  <div className="min-w-0 flex-1">
                    <p
                      className={`truncate text-sm font-medium ${lesson.completed ? 'text-[var(--juba-app-muted)] line-through' : 'text-[var(--juba-app-ink)]'}`}
                    >
                      {lesson.title}
                    </p>
                    <p className="text-[var(--juba-app-muted)] mt-0.5 text-xs">
                      {t('weekDay', { week: lesson.week, day: lesson.day })} ·{' '}
                      {lessonTypeLabel[lesson.lesson_type] ??
                        lesson.lesson_type}
                    </p>
                  </div>
                  {lesson.id != null && lesson.action && (
                    <button
                      onClick={() => onStartLesson(lesson.id!)}
                      className="shrink-0 juba-primary-button rounded-xl px-3 py-2 text-xs"
                    >
                      {lesson.action === 'review'
                        ? t('reviewLesson')
                        : lesson.action === 'continue'
                          ? t('resume')
                          : `${tCommon('start')} →`}
                    </button>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Close */}
        <div className="border-[var(--juba-app-line)] bg-white sticky bottom-0 border-t px-6 py-5 sm:px-7">
          <button
            onClick={onClose}
            className="juba-secondary-button w-full"
          >
            {tCommon('close')}
          </button>
        </div>
      </div>
    </div>
  )
}
