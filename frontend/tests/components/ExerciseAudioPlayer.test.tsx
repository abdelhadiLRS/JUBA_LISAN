import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import React from 'react'
import { ExerciseAudioPlayer } from '@/components/ui/exercise-audio-player'

const { mockApiFetch } = vi.hoisted(() => ({
  mockApiFetch: vi.fn(),
}))

vi.mock('@/lib/api', () => ({
  apiFetch: mockApiFetch,
}))

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))

type MockAudio = {
  play: ReturnType<typeof vi.fn>
  pause: ReturnType<typeof vi.fn>
  addEventListener: ReturnType<typeof vi.fn>
  emit: (event: string) => void
  duration: number
  currentTime: number
  src: string
}

let currentAudio: MockAudio | null = null
let urlCounter = 0

function makeAudio(playImpl?: () => Promise<void>): MockAudio {
  const listeners = new Map<string, () => void>()
  const audio: MockAudio = {
    play: vi.fn(playImpl ?? (() => Promise.resolve())),
    pause: vi.fn(),
    addEventListener: vi.fn((event: string, handler: () => void) => {
      listeners.set(event, handler)
    }),
    emit: (event: string) => listeners.get(event)?.(),
    duration: 100,
    currentTime: 0,
    src: '',
  }
  return audio
}

function okResponse() {
  return {
    ok: true,
    status: 200,
    blob: () => Promise.resolve(new Blob(['audio'], { type: 'audio/mpeg' })),
  } as Response
}

describe('ExerciseAudioPlayer', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    urlCounter = 0
    currentAudio = null

    vi.stubGlobal(
      'Audio',
      vi.fn(function MockAudio() {
        currentAudio = makeAudio()
        return currentAudio
      })
    )
    vi.spyOn(URL, 'createObjectURL').mockImplementation(() => {
      urlCounter += 1
      return `blob:exercise-${urlCounter}`
    })
    vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => undefined)
    mockApiFetch.mockResolvedValue(okResponse())
  })

  it('ignores a stale paused-play resolution after exerciseId changes', async () => {
    let resolveResume!: () => void
    const resumePromise = new Promise<void>((resolve) => {
      resolveResume = resolve
    })
    let playCount = 0

    vi.stubGlobal(
      'Audio',
      vi.fn(function MockAudio() {
        currentAudio = makeAudio(() => {
          playCount += 1
          return playCount === 1 ? Promise.resolve() : resumePromise
        })
        return currentAudio
      })
    )

    const { rerender } = render(<ExerciseAudioPlayer exerciseId={1} />)
    fireEvent.click(screen.getByRole('button', { name: 'audioPlay' }))

    await waitFor(() => {
      expect(currentAudio?.play).toHaveBeenCalledTimes(1)
      expect(screen.getByRole('button', { name: 'audioPause' })).toBeDefined()
    })

    fireEvent.click(screen.getByRole('button', { name: 'audioPause' }))
    fireEvent.click(screen.getByRole('button', { name: 'audioPlay' }))

    await waitFor(() => {
      expect(currentAudio?.play).toHaveBeenCalledTimes(2)
    })

    rerender(<ExerciseAudioPlayer exerciseId={2} />)

    await act(async () => {
      resolveResume()
    })

    expect(screen.getByRole('button', { name: 'audioPlay' })).toBeDefined()
  })

  it('ignores a stale paused-play rejection after exerciseId changes', async () => {
    let rejectResume!: (error: Error) => void
    const resumePromise = new Promise<void>((_, reject) => {
      rejectResume = reject
    })
    let playCount = 0

    vi.stubGlobal(
      'Audio',
      vi.fn(function MockAudio() {
        currentAudio = makeAudio(() => {
          playCount += 1
          return playCount === 1
            ? Promise.resolve()
            : resumePromise
        })
        return currentAudio
      })
    )

    const { rerender } = render(<ExerciseAudioPlayer exerciseId={1} />)
    fireEvent.click(screen.getByRole('button', { name: 'audioPlay' }))

    await waitFor(() => {
      expect(currentAudio?.play).toHaveBeenCalledTimes(1)
      expect(screen.getByRole('button', { name: 'audioPause' })).toBeDefined()
    })

    fireEvent.click(screen.getByRole('button', { name: 'audioPause' }))
    fireEvent.click(screen.getByRole('button', { name: 'audioPlay' }))

    await waitFor(() => {
      expect(currentAudio?.play).toHaveBeenCalledTimes(2)
    })

    rerender(<ExerciseAudioPlayer exerciseId={2} />)

    await act(async () => {
      rejectResume(new Error('stale playback failure'))
    })

    expect(screen.queryByRole('alert')).toBeNull()
    expect(screen.getByRole('button', { name: 'audioPlay' })).toBeDefined()
  })

  it('supports Home, End and arrow-key seeking on the progress slider', async () => {
    render(<ExerciseAudioPlayer exerciseId={1} />)
    fireEvent.click(screen.getByRole('button', { name: 'audioPlay' }))

    await waitFor(() => {
      expect(screen.getByRole('slider')).toBeDefined()
    })

    currentAudio!.emit('loadedmetadata')
    const slider = screen.getByRole('slider')

    fireEvent.keyDown(slider, { key: 'End' })
    expect(currentAudio!.currentTime).toBe(100)

    fireEvent.keyDown(slider, { key: 'Home' })
    expect(currentAudio!.currentTime).toBe(0)

    fireEvent.keyDown(slider, { key: 'ArrowRight' })
    expect(currentAudio!.currentTime).toBe(5)

    fireEvent.keyDown(slider, { key: 'ArrowLeft' })
    expect(currentAudio!.currentTime).toBe(0)
  })

  it('revokes the exercise audio blob URL when playback ends', async () => {
    render(<ExerciseAudioPlayer exerciseId={1} />)
    fireEvent.click(screen.getByRole('button', { name: 'audioPlay' }))

    await waitFor(() => {
      expect(URL.createObjectURL).toHaveBeenCalled()
    })

    currentAudio!.emit('ended')

    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:exercise-1')
    expect(screen.getByRole('button', { name: 'audioPlay' })).toBeDefined()
  })

  it('revokes the exercise audio blob URL when the exercise changes', async () => {
    const { rerender } = render(<ExerciseAudioPlayer exerciseId={1} />)
    fireEvent.click(screen.getByRole('button', { name: 'audioPlay' }))

    await waitFor(() => {
      expect(URL.createObjectURL).toHaveBeenCalled()
    })

    rerender(<ExerciseAudioPlayer exerciseId={2} />)

    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:exercise-1')
  })
})
