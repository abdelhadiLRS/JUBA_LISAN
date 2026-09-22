import { describe, expect, it } from 'vitest'
import {
  hasAdaptiveTarget,
  isAdaptiveReinforcementAction,
  isAdaptiveRetryAction,
  mergeAdaptiveRecommendations,
  normaliseAdaptiveAction,
} from '@/lib/adaptive-exercise'

describe('mergeAdaptiveRecommendations', () => {
  it('hydrates persisted adaptive recommendations onto matching exercises', () => {
    const exercises = [
      { id: 1, recommended_action: undefined, recommended_variant: null },
      { id: 2, recommended_action: undefined, recommended_variant: null },
    ]

    expect(
      mergeAdaptiveRecommendations(exercises, [
        { exercise_id: 1, recommended_action: 'retry_easier', recommended_variant: 'fill_blank' },
      ]),
    ).toEqual([
      { id: 1, recommended_action: 'retry_easier', recommended_variant: 'fill_blank' },
      { id: 2, recommended_action: undefined, recommended_variant: null },
    ])
  })

  it('hydrates mastery state from persisted summaries', () => {
    const exercises = [
      { id: 12, recommended_action: undefined, recommended_variant: null },
    ]

    expect(
      mergeAdaptiveRecommendations(exercises, [
        {
          exercise_id: 12,
          recommended_action: 'reinforce',
          recommended_variant: null,
          mastery_score: 0.875,
          mastery_state: 'mastered',
          mastery_variants: 3,
        },
      ]),
    ).toEqual([
      {
        id: 12,
        recommended_action: 'reinforce',
        recommended_variant: null,
        mastery_score: 0.875,
        mastery_state: 'mastered',
        mastery_variants: 3,
      },
    ])
  })

  it('clears a stale recommendation when the latest summary has no target variant', () => {
    const exercises = [
      { id: 7, recommended_action: 'retry_easier', recommended_variant: 'fill_blank' },
    ]

    expect(
      mergeAdaptiveRecommendations(exercises, [
        { exercise_id: 7, recommended_action: 'reinforce', recommended_variant: null },
      ]),
    ).toEqual([
      { id: 7, recommended_action: 'reinforce', recommended_variant: null },
    ])
  })

  it('leaves exercises without a matching summary unchanged', () => {
    const exercise = { id: 9, recommended_action: undefined, recommended_variant: null }

    expect(mergeAdaptiveRecommendations([exercise], [])).toEqual([exercise])
  })

  it('uses the latest summary when duplicate exercise ids are present', () => {
    const exercises = [
      { id: 4, recommended_action: 'retry_easier', recommended_variant: 'fill_blank' },
    ]

    const result = mergeAdaptiveRecommendations(exercises, [
      { exercise_id: 4, recommended_action: 'retry_easier', recommended_variant: 'fill_blank' },
      { exercise_id: 4, recommended_action: 'advance_harder', recommended_variant: 'translate' },
    ])

    expect(result).toEqual([
      { id: 4, recommended_action: 'advance_harder', recommended_variant: 'translate' },
    ])
    expect(exercises[0]).toEqual({
      id: 4,
      recommended_action: 'retry_easier',
      recommended_variant: 'fill_blank',
    })
  })

  it('recognizes only non-empty recommended variants as adaptive targets', () => {
    expect(hasAdaptiveTarget({ exercise_id: 1, recommended_variant: 'fill_blank' })).toBe(true)
    expect(hasAdaptiveTarget({ exercise_id: 2, recommended_variant: '' })).toBe(false)
    expect(hasAdaptiveTarget({ exercise_id: 3, recommended_variant: '   ' })).toBe(false)
    expect(hasAdaptiveTarget({ exercise_id: 4, recommended_variant: null })).toBe(false)
  })
})

describe('adaptive action helpers', () => {
  it('classifies actionable adaptive targets', async () => {
    expect(isAdaptiveRetryAction('retry_easier')).toBe(true)
    expect(isAdaptiveRetryAction('advance_harder')).toBe(true)
    expect(isAdaptiveRetryAction('reinforce')).toBe(false)
    expect(isAdaptiveReinforcementAction('reinforce')).toBe(true)
    expect(isAdaptiveReinforcementAction(null)).toBe(false)
  })

  it('rejects blank or unrelated actions as retry targets', async () => {
    expect(isAdaptiveRetryAction()).toBe(false)
    expect(isAdaptiveRetryAction(null)).toBe(false)
    expect(isAdaptiveRetryAction('advance')).toBe(false)
    expect(isAdaptiveRetryAction('retry')).toBe(false)
  })

  it('returns the canonical action used by adaptive UI labels', () => {
    expect(normaliseAdaptiveAction(' Advance_Harder ')).toBe('advance_harder')
    expect(normaliseAdaptiveAction(' Reinforce ')).toBe('reinforce')
    expect(normaliseAdaptiveAction(null)).toBe('')
  })

  it('normalizes adaptive action casing and surrounding whitespace', () => {
    expect(isAdaptiveRetryAction(' RETRY_EASIER ')).toBe(true)
    expect(isAdaptiveRetryAction(' Advance_Harder ')).toBe(true)
    expect(isAdaptiveReinforcementAction(' Reinforce ')).toBe(true)
  })
