import { render } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { usePathname } from 'next/navigation'
import { useLearningProgressSync } from '@/hooks/use-learning-progress'
import { LearningProgressBridge } from '@/components/LearningProgressBridge'

vi.mock('next/navigation', () => ({
  usePathname: vi.fn(),
}))

vi.mock('@/hooks/use-learning-progress', () => ({
  useLearningProgressSync: vi.fn(),
}))

const mockedUsePathname = vi.mocked(usePathname)
const mockedUseLearningProgressSync = vi.mocked(useLearningProgressSync)

describe('LearningProgressBridge', () => {
  beforeEach(() => {
    mockedUsePathname.mockReset()
    mockedUseLearningProgressSync.mockReset()
  })

  it('reloads the plan when learning progress changes', () => {
    mockedUsePathname.mockReturnValue('/plan')
    const reload = vi.spyOn(window.location, 'reload').mockImplementation(() => undefined)

    render(<LearningProgressBridge />)

    expect(mockedUseLearningProgressSync).toHaveBeenCalledTimes(1)
    const refresh = mockedUseLearningProgressSync.mock.calls[0]?.[0]
    expect(refresh).toBeTypeOf('function')

    refresh?.()

    expect(reload).toHaveBeenCalledTimes(1)
    reload.mockRestore()
  })

  it('does not reload unrelated routes', () => {
    mockedUsePathname.mockReturnValue('/dashboard')
    const reload = vi.spyOn(window.location, 'reload').mockImplementation(() => undefined)

    render(<LearningProgressBridge />)

    const refresh = mockedUseLearningProgressSync.mock.calls[0]?.[0]
    refresh?.()

    expect(reload).not.toHaveBeenCalled()
    reload.mockRestore()
  })

  it('also handles nested plan routes', () => {
    mockedUsePathname.mockReturnValue('/plan/unit-1')
    const reload = vi.spyOn(window.location, 'reload').mockImplementation(() => undefined)

    render(<LearningProgressBridge />)

    const refresh = mockedUseLearningProgressSync.mock.calls[0]?.[0]
    refresh?.()

    expect(reload).toHaveBeenCalledTimes(1)
    reload.mockRestore()
  })
})
