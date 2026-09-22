import { apiFetch } from '@/lib/api'

export interface AdaptiveExerciseRecommendation {
  exercise_id: number
  recommended_action?: string | null
  recommended_variant?: string | null
  mastery_score?: number
  mastery_state?: string
  mastery_variants?: number
}

export interface AdaptiveExerciseLike {
  id: number
  recommended_action?: string | null
  recommended_variant?: string | null
}

export function mergeAdaptiveRecommendations<T extends AdaptiveExerciseLike>(
  exercises: T[],
  summaries: AdaptiveExerciseRecommendation[],
): T[] {
  const byExerciseId = new Map(summaries.map((summary) => [summary.exercise_id, summary]))

  return exercises.map((exercise) => {
    const summary = byExerciseId.get(exercise.id)
    if (!summary) return exercise

    return {
      ...exercise,
      recommended_action: summary.recommended_action ?? undefined,
      recommended_variant: summary.recommended_variant ?? null,
      ...(summary.mastery_score !== undefined ? { mastery_score: summary.mastery_score } : {}),
      ...(summary.mastery_state !== undefined ? { mastery_state: summary.mastery_state } : {}),
      ...(summary.mastery_variants !== undefined ? { mastery_variants: summary.mastery_variants } : {}),
    }
  })
}

export function hasAdaptiveTarget(recommendation: Pick<AdaptiveExerciseLike, 'recommended_variant'>): boolean {
  return typeof recommendation.recommended_variant === 'string' && recommendation.recommended_variant.trim().length > 0
}


const ADAPTIVE_RETRY_ACTIONS = new Set(['retry_easier', 'advance_harder'])

export function normaliseAdaptiveAction(action?: string | null): string {
  return typeof action === 'string' ? action.trim().toLowerCase() : ''
}

export function isAdaptiveRetryAction(action?: string | null): boolean {
  return ADAPTIVE_RETRY_ACTIONS.has(normaliseAdaptiveAction(action))
}

export function isAdaptiveAdvanceAction(action?: string | null): boolean {
  return normaliseAdaptiveAction(action) === 'advance'
}

export function isAdaptiveReinforcementAction(action?: string | null): boolean {
  return normaliseAdaptiveAction(action) === 'reinforce'
}


export interface LessonMasteryNextExercise {
  id: number
  lesson_id: number
  exercise_type: string
  question: string
  options: string[] | null
  correct_answer: string
  explanation: string | null
  native_explanation: string | null
  user_answer: string | null
  score: number | null
  feedback: string | null
  native_hint: string | null
  content_id?: string | null
  variant?: string | null
  accepted_answers?: string[] | null
  metadata?: Record<string, string> | null
  skills?: string[] | null
  recommended_action?: string
  recommended_variant?: string | null
  mastery_score?: number
  mastery_state?: string
  mastery_variants?: number
}

export type LessonMasteryNextReason = 'struggling' | 'unseen' | 'lowest_mastery'

export interface LessonMasteryNextResponse {
  exercise: LessonMasteryNextExercise
  reason: LessonMasteryNextReason
}

export async function fetchNextMasteryExercise(lessonId: number): Promise<LessonMasteryNextResponse | null> {
  const response = await apiFetch(`/api/lessons/${lessonId}/mastery/next`)
  if (response.status === 404) return null
  if (!response.ok) throw new Error('mastery_next_failed')
  return response.json() as Promise<LessonMasteryNextResponse>
}


export async function fetchNextSkillMasteryExercise(
  lessonId: number,
  skill: string,
): Promise<LessonMasteryNextResponse | null> {
  const response = await apiFetch(
    `/api/lessons/${lessonId}/mastery/skills/${encodeURIComponent(skill)}/next`,
  )
  if (response.status === 404) return null
  if (!response.ok) throw new Error('skill_mastery_next_failed')
  return response.json() as Promise<LessonMasteryNextResponse>
}
