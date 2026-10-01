'use client'

import { useState, useEffect } from 'react'
import { useTranslations } from 'next-intl'
import { Flame, BookOpen, Clock, CheckCircle, ArrowRight, Zap } from 'lucide-react'
import Link from 'next/link'

interface DailyMomentumProps {
  nextAction: {
    id: number | null
    title: string
    lesson_type: string
    estimated_minutes: number
    is_completed: boolean
  } | null
  reviewDueCount: number
  goalProgress: {
    current: number
    target: number
  }
  hasPlan: boolean
  completedLessonCount: number
}

const btnPrimary =
  'inline-flex items-center justify-center gap-2 rounded-[10px] px-4 py-2.5 text-sm font-semibold text-white transition-all disabled:opacity-50 shadow-sm hover:shadow-sm active:scale-[0.98]'
const btnSecondary =
  'inline-flex items-center justify-center gap-2 rounded-[10px] border border-[var(--duo-line)] px-4 py-2.5 text-sm font-medium transition-all hover:bg-[var(--duo-card)] hover:border-[var(--duo-green)] active:scale-[0.98]'

export function DailyMomentum({
  nextAction,
  reviewDueCount,
  goalProgress,
  hasPlan,
  completedLessonCount,
}: DailyMomentumProps) {
  const t = useTranslations('dashboard')
  const tPlan = useTranslations('plan')
  const [animatedProgress, setAnimatedProgress] = useState(0)
  const [isCelebrating, setIsCelebrating] = useState(false)

  // Animate progress bar on mount/update
  useEffect(() => {
    const targetProgress = Math.min(100, (goalProgress.current / goalProgress.target) * 100)
    const duration = 800
    const startTime = Date.now()
    
    const animate = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3) // cubic ease-out
      setAnimatedProgress(eased * targetProgress)
      
      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }
    
    requestAnimationFrame(animate)
  }, [goalProgress.current, goalProgress.target])

  // Celebration animation when completing all lessons
  useEffect(() => {
    if (goalProgress.current >= goalProgress.target && goalProgress.target > 0) {
      setIsCelebrating(true)
      const timer = setTimeout(() => setIsCelebrating(false), 2000)
      return () => clearTimeout(timer)
    }
  }, [goalProgress.current, goalProgress.target])

  function getLessonTypeLabelKey(value: string): string {
    return `lessonTypes.${value}`
  }

  const goalPercentage = goalProgress.target > 0 
    ? Math.round((goalProgress.current / goalProgress.target) * 100) 
    : 0

  return (
    <section 
      className={`mb-6 overflow-hidden rounded-[13px] border border-[var(--duo-line)] bg-[var(--duo-card)] shadow-sm transition-all duration-500 ${
        isCelebrating ? 'ring-2 ring-[var(--duo-yellow)] ring-offset-2 ring-offset-[var(--duo-bg)]' : ''
      }`}
      aria-label={t('dailyMomentum')}
    >
      {/* Header with gradient */}
      <div className="relative border-b border-[var(--duo-line)] bg-[color-mix(in_srgb,var(--duo-green)_6%,var(--duo-card))] p-5 sm:p-6">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -right-16 -top-16 h-32 w-32 rounded-full bg-[var(--duo-green)]/5 blur-2xl" />
          <div className="absolute -bottom-8 -left-8 h-24 w-24 rounded-full bg-[var(--duo-yellow)]/5 blur-xl" />
        </div>
        
        <div className="relative flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-[10px] bg-[var(--duo-green)] text-white shadow-sm">
            <Flame className="h-5 w-5" />
          </div>
          <div>
            <h2 className="text-[var(--duo-ink)] text-lg font-bold tracking-tight">{t('dailyMomentum')}</h2>
            <p className="text-[var(--duo-muted)] mt-0.5 text-sm">{t('dailyMomentumSubtitle')}</p>
          </div>
          
          {isCelebrating && (
            <div className="absolute right-4 top-4 animate-bubble-in">
              <Zap className="h-6 w-6 text-[var(--duo-yellow)]" />
            </div>
          )}
        </div>
      </div>
      
      {/* Three core questions grid */}
      <div className="grid grid-cols-1 gap-4 p-5 sm:p-6 md:grid-cols-3">
        {/* What should I do now? */}
        <div className="group relative overflow-hidden rounded-[13px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-4 transition-colors duration-200 hover:border-[var(--duo-green)]">
          <div className="absolute inset-0 bg-gradient-to-br from-[var(--duo-green)]/0 via-[var(--duo-green)]/0 to-[var(--duo-green)]/4 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
          
          <div className="relative">
            <div className="mb-3 flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-[var(--duo-green)]" />
              <p className="text-[var(--duo-muted)] text-xs font-semibold uppercase tracking-wide">{t('whatNow')}</p>
            </div>
            
            {nextAction ? (
              <>
                <h3 className="text-[var(--duo-ink)] text-base font-bold leading-tight">{nextAction.title}</h3>
                <div className="mt-2 flex items-center gap-2">
                  <span className="rounded-md bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] px-2 py-0.5 text-xs font-medium text-[var(--duo-green-dark)]">
                    {tPlan(getLessonTypeLabelKey(nextAction.lesson_type))}
                  </span>
                  <span className="flex items-center gap-1 text-[var(--duo-muted)] text-xs">
                    <Clock className="h-3 w-3" />
                    {nextAction.estimated_minutes}min
                  </span>
                </div>
                <Link href={`/lesson/${nextAction.id}`} className="mt-4 inline-flex">
                  <button className={`${btnPrimary} bg-[var(--duo-green)] hover:bg-[var(--duo-green-dark)]`}>
                    {t('startLesson')}
                    <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </button>
                </Link>
              </>
            ) : hasPlan ? (
              <div className="flex flex-col items-center justify-center py-4">
                <CheckCircle className="mb-2 h-8 w-8 text-[var(--duo-yellow)]" />
                <p className="text-[var(--duo-muted)] text-sm font-medium">{t('allCaughtUp')}</p>
              </div>
            ) : (
              <Link href="/assessment">
                <p className="text-[var(--duo-green-dark)] text-sm font-semibold hover:underline">
                  {t('takeAssessment')} →
                </p>
              </Link>
            )}
          </div>
        </div>
        
        {/* What is due for review? */}
        <div className="group relative overflow-hidden rounded-xl border border-[var(--duo-line)] bg-[var(--duo-card)] p-4 transition-all duration-300 hover:border-[var(--duo-green)]">
          <div className="absolute inset-0 bg-gradient-to-br from-[var(--duo-green)]/0 via-[var(--duo-green)]/0 to-[var(--duo-green)]/4 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
          
          <div className="relative">
            <div className="mb-3 flex items-center gap-2">
              <Clock className="h-4 w-4 text-[var(--duo-green)]" />
              <p className="text-[var(--duo-muted)] text-xs font-semibold uppercase tracking-wide">{t('dueForReview')}</p>
            </div>
            
            {reviewDueCount > 0 ? (
              <>
                <div className="mb-2 flex items-baseline gap-2">
                  <h3 className="text-[var(--duo-ink)] text-3xl font-bold text-[var(--duo-green)]">
                    {reviewDueCount}
                  </h3>
                  <span className="text-[var(--duo-muted)] text-sm">{t('itemsToReview')}</span>
                </div>
                <div className="mt-3 flex items-center gap-2 text-[var(--duo-muted)] text-xs">
                  <div className="h-2 w-2 rounded-full bg-[var(--duo-green)] animate-pulse" />
                  <span>{t('reviewReminder')}</span>
                </div>
                <Link href="/review" className="mt-4 inline-flex">
                  <button className={btnSecondary}>
                    {t('reviewNow')}
                    <ArrowRight className="h-4 w-4" />
                  </button>
                </Link>
              </>
            ) : (
              <div className="flex flex-col items-center justify-center py-4">
                <CheckCircle className="mb-2 h-8 w-8 text-[var(--duo-yellow)]" />
                <h3 className="text-[var(--duo-ink)] text-xl font-bold">✓</h3>
                <p className="text-[var(--duo-muted)] mt-1 text-sm">{t('noReviewsDue')}</p>
              </div>
            )}
          </div>
        </div>
        
        {/* How close to today's goal? */}
        <div className="group relative overflow-hidden rounded-[13px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-4 transition-colors duration-200 hover:border-[var(--duo-green)]">
          <div className="absolute inset-0 bg-gradient-to-br from-[var(--duo-green)]/0 via-[var(--duo-green)]/0 to-[var(--duo-green)]/4 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
          
          <div className="relative">
            <div className="mb-3 flex items-center gap-2">
              <Zap className={`h-4 w-4 ${goalProgress.current >= goalProgress.target ? 'text-[var(--duo-yellow)]' : 'text-[var(--duo-green)]'}`} />
              <p className="text-[var(--duo-muted)] text-xs font-semibold uppercase tracking-wide">{t('todayGoal')}</p>
            </div>
            
            <div className="mb-3 flex items-end justify-between">
              <div className="flex items-baseline gap-1">
                <span className={`text-3xl font-bold ${goalProgress.current >= goalProgress.target ? 'text-[var(--duo-yellow)]' : 'text-[var(--duo-ink)]'}`}>
                  {goalProgress.current}
                </span>
                <span className="text-[var(--duo-muted)] text-sm">/ {goalProgress.target}</span>
              </div>
              <span className={`rounded-full px-2 py-1 text-xs font-bold ${
                goalProgress.current >= goalProgress.target 
                  ? 'bg-[color-mix(in_srgb,var(--duo-yellow)_14%,transparent)] text-[var(--duo-yellow)]' 
                  : 'bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] text-[var(--duo-green)]'
              }`}>
                {goalPercentage}%
              </span>
            </div>
            
            {/* Animated progress bar */}
            <div className="bg-[var(--duo-line)] relative h-3 w-full overflow-hidden rounded-full">
              <div 
                className="absolute inset-y-0 start-0 rounded-full transition-all duration-300"
                style={{ 
                  width: `${animatedProgress}%`,
                  background: goalProgress.current >= goalProgress.target 
                    ? 'var(--duo-yellow)' 
                    : 'linear-gradient(90deg, var(--duo-green), var(--duo-yellow))'
                }}
              />
              {/* Shimmer effect on completion */}
              {goalProgress.current >= goalProgress.target && (
                <div className="absolute inset-0 overflow-hidden">
                  <div className="absolute inset-y-0 start-0 w-full animate-shimmer bg-gradient-to-r from-transparent via-white/30 to-transparent" />
                </div>
              )}
            </div>
            
            <p className="text-[var(--duo-muted)] mt-2 text-xs">
              {goalProgress.current >= goalProgress.target 
                ? t('goalCompleted') 
                : t('lessonsCompletedToday')}
            </p>
          </div>
        </div>
      </div>
      
      {/* Motivational footer */}
      {goalProgress.current > 0 && goalProgress.current < goalProgress.target && (
        <div className="border-t border-[var(--duo-line)] bg-[var(--duo-card)]/50 px-5 py-3">
          <p className="text-[var(--duo-muted)] text-center text-xs">
            {t('keepGoing', { remaining: goalProgress.target - goalProgress.current })}
          </p>
        </div>
      )}
    </section>
  )
}
