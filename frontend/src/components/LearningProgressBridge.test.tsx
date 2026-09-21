import { describe, expect, it, vi } from 'vitest'
import { refreshLearningPlan } from '@/components/LearningProgressBridge'

describe('refreshLearningPlan', () => {
  it('reloads the plan route', () => {
    const reload = vi.fn()

    refreshLearningPlan('/plan', reload)

    expect(reload).toHaveBeenCalledTimes(1)
  })

  it('reloads nested plan routes', () => {
    const reload = vi.fn()

    refreshLearningPlan('/plan/unit-1', reload)

    expect(reload).toHaveBeenCalledTimes(1)
  })

  it('reloads localized plan routes', () => {
    const reload = vi.fn()

    refreshLearningPlan('/fr/plan', reload)
    refreshLearningPlan('/de/plan/unit-1', reload)

    expect(reload).toHaveBeenCalledTimes(2)
  })

  it('ignores query strings when matching the plan route', () => {
    const reload = vi.fn()

    refreshLearningPlan('/plan?section=1', reload)

    expect(reload).toHaveBeenCalledTimes(1)
  })

  it('handles trailing slashes and nested localized routes with queries', () => {
    const reload = vi.fn()

    refreshLearningPlan('/fr/plan/unit-1/?section=practice', reload)
    refreshLearningPlan('/de/plan/', reload)

    expect(reload).toHaveBeenCalledTimes(2)
  })

  it('does not match near-miss plan routes', () => {
    const reload = vi.fn()

    refreshLearningPlan('/planning', reload)
    refreshLearningPlan('/fr/plans', reload)
    refreshLearningPlan('/fr/planish', reload)

    expect(reload).not.toHaveBeenCalled()
  })

  it('ignores unrelated routes', () => {
    const reload = vi.fn()

    refreshLearningPlan('/dashboard', reload)

    expect(reload).not.toHaveBeenCalled()
  })
})
