export interface AdaptiveExerciseRecommendation {
  exercise_id: number
  recommended_action?: string | null
  recommended_variant?: string | null
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
    }
  })
}

export function hasAdaptiveTarget(recommendation: Pick<AdaptiveExerciseLike, 'recommended_variant'>): boolean {
  return typeof recommendation.recommended_variant === 'string' && recommendation.recommended_variant.trim().length > 0
}


const ADAPTIVE_RETRY_ACTIONS = new Set(['retry_easier', 'advance_harder'])

export function isAdaptiveRetryAction(action?: string | null): boolean {
  return typeof action === 'string' && ADAPTIVE_RETRY_ACTIONS.has(action)
}

export function isAdaptiveReinforcementAction(action?: string | null): boolean {
  return action === 'reinforce'
}
