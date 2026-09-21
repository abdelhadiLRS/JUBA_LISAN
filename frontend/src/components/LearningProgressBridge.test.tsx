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

  it('ignores unrelated routes', () => {
    const reload = vi.fn()

    refreshLearningPlan('/dashboard', reload)

    expect(reload).not.toHaveBeenCalled()
  })
})
