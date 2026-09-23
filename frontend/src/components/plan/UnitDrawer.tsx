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
    <div className="bg-[#242033]/35 fixed inset-0 z-50 flex items-end justify-center p-0 backdrop-blur-sm sm:items-center sm:p-4">
      <div
        ref={ref}
        className="border-[#ebe7f5] bg-white max-h-[80vh] w-full overflow-y-auto rounded-t-[30px] border shadow-[0_24px_70px_rgba(39,28,72,0.2)] sm:max-w-xl sm:rounded-[30px]"
      >
        {/* Header */}
        <div className="border-[#ebe7f5] bg-white sticky top-0 z-10 flex items-center justify-between gap-4 border-b px-6 py-5 sm:px-7">
          <div className="min-w-0">
            <span
              className="text-xs font-semibold"
              style={{ color: 'var(--juba-violet-dark)' }}
            >
              {unit.level} · {t('unitLabel')}
            </span>
            <p className="text-[#242033] mt-0.5 truncate text-base font-bold">
              {unit.title}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-[#938da2] hover:text-[#242033] shrink-0 rounded-2xl p-2 transition-colors hover:bg-[var(--juba-lilac)]"
            aria-label={tCommon('close')}
          >
            <X className="h-4.5 w-4.5" aria-hidden="true" />
          </button>
        </div>

        {/* Grammar points */}
        {unit.grammar_points.length > 0 && (
          <div className="border-[#ebe7f5] border-b px-6 py-5 sm:px-7">
            <p className="text-[#938da2] mb-2.5 text-xs font-semibold tracking-wide uppercase">
              {t('grammarCovered')}
            </p>
            <div className="flex flex-wrap gap-1.5">
              {unit.grammar_points.map((gp) => (
                <span
                  key={gp}
                  className="bg-white-2 text-[#5f596e] rounded-full px-2.5 py-1 text-xs font-medium"
                >
                  {gp}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Lessons */}
        <div>
          <div className="border-[#ebe7f5] border-b px-5 py-3 sm:px-6">
            <p className="text-[#938da2] text-xs font-semibold tracking-wide uppercase">
              {t('lessonsHeader', { count: lessons.length })}
            </p>
          </div>
          <div className="divide-fl-border divide-y">
            {lessons.length === 0 ? (
              <div className="px-5 py-6 sm:px-6">
                <p className="text-[#938da2] text-sm">{t('noLessons')}</p>
              </div>
            ) : (
              lessons.map((lesson, i) => (
                <div
                  key={lesson.id ?? i}
                  className={`flex items-center gap-3 px-5 py-3.5 transition-colors sm:px-6 ${lesson.action ? 'hover:bg-[var(--juba-lilac)]' : ''}`}
                >
                  {lesson.completed ? (
                    <span
                      className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full"
                      style={{
                        background: 'var(--juba-violet)',
                        color: 'var(--juba-text)',
                      }}
                    >
                      <Check className="h-3.5 w-3.5" aria-hidden="true" />
                    </span>
                  ) : (
                    <span className="border-[#ebe7f5] text-[#938da2] flex h-6 w-6 shrink-0 items-center justify-center rounded-full border">
                      <Circle className="h-2.5 w-2.5" aria-hidden="true" />
                    </span>
                  )}
                  <div className="min-w-0 flex-1">
                    <p
                      className={`truncate text-sm font-medium ${lesson.completed ? 'text-[#777087] line-through' : 'text-[#242033]'}`}
                    >
                      {lesson.title}
                    </p>
                    <p className="text-[#938da2] mt-0.5 text-xs">
                      {t('weekDay', { week: lesson.week, day: lesson.day })} ·{' '}
                      {lessonTypeLabel[lesson.lesson_type] ??
                        lesson.lesson_type}
                    </p>
                  </div>
                  {lesson.id != null && lesson.action && (
                    <button
                      onClick={() => onStartLesson(lesson.id!)}
                      className="shrink-0 rounded-2xl bg-[var(--juba-violet)] px-3 py-2 text-xs font-bold text-white transition-colors hover:bg-[var(--juba-violet-dark)]"
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
        <div className="border-[#ebe7f5] bg-white sticky bottom-0 border-t px-6 py-5 sm:px-7">
          <button
            onClick={onClose}
            className="border-[#ebe7f5] text-[#777087] hover:text-[#242033] w-full rounded-2xl border-2 py-2.5 text-sm font-medium transition-colors hover:bg-[var(--juba-lilac)]"
          >
            {tCommon('close')}
          </button>
        </div>
      </div>
    </div>
  )
}
