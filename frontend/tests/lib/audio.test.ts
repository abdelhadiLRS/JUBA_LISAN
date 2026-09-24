import { describe, it, expect, vi } from 'vitest'
import { float32ToWav } from '@/lib/audio'

describe('float32ToWav', () => {
  it('produces a valid WAV header', () => {
    const samples = new Float32Array(100)
    const buffer = float32ToWav(samples, 16000)
    const view = new DataView(buffer)

    expect(
      String.fromCharCode(
        view.getUint8(0),
        view.getUint8(1),
        view.getUint8(2),
        view.getUint8(3)
      )
    ).toBe('RIFF')
    expect(
      String.fromCharCode(
        view.getUint8(8),
        view.getUint8(9),
        view.getUint8(10),
        view.getUint8(11)
      )
    ).toBe('WAVE')
    expect(
      String.fromCharCode(
        view.getUint8(12),
        view.getUint8(13),
        view.getUint8(14),
        view.getUint8(15)
      )
    ).toBe('fmt ')
    expect(
      String.fromCharCode(
        view.getUint8(36),
        view.getUint8(37),
        view.getUint8(38),
        view.getUint8(39)
      )
    ).toBe('data')
  })

  it('writes correct PCM format chunk', () => {
    const samples = new Float32Array(100)
    const buffer = float32ToWav(samples, 16000)
    const view = new DataView(buffer)

    expect(view.getUint32(16, true)).toBe(16)
    expect(view.getUint16(20, true)).toBe(1)
    expect(view.getUint16(22, true)).toBe(1)
    expect(view.getUint32(24, true)).toBe(16000)
    expect(view.getUint32(28, true)).toBe(32000)
    expect(view.getUint16(32, true)).toBe(2)
    expect(view.getUint16(34, true)).toBe(16)
  })

  it('calculates correct buffer size (44 byte header + data)', () => {
    const samples = new Float32Array(1000)
    const buffer = float32ToWav(samples, 16000)

    expect(buffer.byteLength).toBe(44 + 1000 * 2)
  })

  it('writes correct RIFF chunk size', () => {
    const samples = new Float32Array(100)
    const buffer = float32ToWav(samples, 16000)
    const view = new DataView(buffer)
    const dataSize = 100 * 2

    expect(view.getUint32(4, true)).toBe(36 + dataSize)
    expect(view.getUint32(40, true)).toBe(dataSize)
  })

  it('clamps samples to [-1, 1] range', () => {
    const samples = new Float32Array([2.0, -2.0, 0.5, -0.5])
    const buffer = float32ToWav(samples, 16000)
    const view = new DataView(buffer)

    const sample0 = view.getInt16(44, true)
    const sample1 = view.getInt16(46, true)
    const sample2 = view.getInt16(48, true)
    const sample3 = view.getInt16(50, true)

    expect(sample0).toBe(0x7fff)
    expect(sample1).toBe(-0x8000)
    expect(sample2).toBeGreaterThan(0)
    expect(sample3).toBeLessThan(0)
  })

  it('encodes silence as zeros', () => {
    const samples = new Float32Array(10)
    const buffer = float32ToWav(samples, 16000)
    const view = new DataView(buffer)

    for (let i = 0; i < 10; i++) {
      expect(view.getInt16(44 + i * 2, true)).toBe(0)
    }
  })

  it('handles empty sample array', () => {
    const samples = new Float32Array(0)
    const buffer = float32ToWav(samples, 16000)

    expect(buffer.byteLength).toBe(44)
  })

  it('works with different sample rates', () => {
    const samples = new Float32Array(100)
    const buffer = float32ToWav(samples, 44100)
    const view = new DataView(buffer)

    expect(view.getUint32(24, true)).toBe(44100)
    expect(view.getUint32(28, true)).toBe(88200)
  })
})


describe('createAudioQueue', () => {
  function createContext() {
    const sources: Array<{
      start: ReturnType<typeof vi.fn>
      stop: ReturnType<typeof vi.fn>
      connect: ReturnType<typeof vi.fn>
      onended?: () => void
      buffer?: AudioBuffer
    }> = []

    const ctx = {
      state: 'running',
      currentTime: 0,
      destination: {},
      resume: vi.fn(async () => {}),
      decodeAudioData: vi.fn(async () => ({
        duration: 0.5,
        sampleRate: 16000,
        numberOfChannels: 1,
      })),
      createBufferSource: vi.fn(() => {
        const source = {
          start: vi.fn(),
          stop: vi.fn(),
          connect: vi.fn(),
          onended: undefined as (() => void) | undefined,
          buffer: undefined as AudioBuffer | undefined,
        }
        sources.push(source)
        return source
      }),
    } as unknown as AudioContext

    return { ctx, sources }
  }

  it('decodes and schedules queued chunks in enqueue order', async () => {
    const { ctx, sources } = createContext()
    const idle = vi.fn()
    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx, idle)

    const first = queue.enqueue(new ArrayBuffer(4))
    const second = queue.enqueue(new ArrayBuffer(8))

    await Promise.all([first, second])

    expect(ctx.decodeAudioData).toHaveBeenCalledTimes(2)
    expect(ctx.createBufferSource).toHaveBeenCalledTimes(2)
    expect(sources[0].start).toHaveBeenCalledWith(0.005)
    expect(sources[1].start).toHaveBeenCalledWith(0.505)
    expect(idle).not.toHaveBeenCalled()

    sources[0].onended?.()
    expect(idle).not.toHaveBeenCalled()
    sources[1].onended?.()
    expect(idle).toHaveBeenCalledTimes(1)
  })

  it('ignores a late source ended event after cancellation', async () => {
    const { ctx, sources } = createContext()
    const idle = vi.fn()
    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx, idle)

    await queue.enqueue(new ArrayBuffer(4))
    expect(sources).toHaveLength(1)

    queue.cancel()
    expect(idle).toHaveBeenCalledTimes(1)

    sources[0].onended?.()
    expect(idle).toHaveBeenCalledTimes(1)
  })
  it('cancels pending chunks and prevents stale decode completion from scheduling audio', async () => {
    const { ctx, sources } = createContext()
    let resolveDecode!: (value: AudioBuffer) => void
    ctx.decodeAudioData = vi.fn(
      () =>
        new Promise<AudioBuffer>((resolve) => {
          resolveDecode = resolve
        })
    ) as typeof ctx.decodeAudioData

    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx)
    const pending = queue.enqueue(new ArrayBuffer(4))

    queue.cancel()

    resolveDecode({
      duration: 1,
      sampleRate: 16000,
      numberOfChannels: 1,
    } as AudioBuffer)

    await pending

    expect(sources).toHaveLength(0)
    expect(ctx.createBufferSource).not.toHaveBeenCalled()
  })

  it('uses HTMLAudio fallback when the AudioContext is closed', async () => {
    const { ctx } = createContext()
    Object.defineProperty(ctx, 'state', { value: 'closed', configurable: true })

    const play = vi.fn().mockResolvedValue(undefined)
    vi.stubGlobal('Audio', vi.fn(() => ({
      play,
      pause: vi.fn(),
      addEventListener: vi.fn((event, handler) => {
        if (event === 'ended') queueMicrotask(handler)
      }),
      removeEventListener: vi.fn(),
      src: 'blob:test',
    })))
    vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:test')
    vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => undefined)

    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx as AudioContext)

    await queue.enqueue(new ArrayBuffer(8))

    expect(play).toHaveBeenCalledTimes(1)
    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:test')
  })

  it('falls back when a suspended audio context cannot resume', async () => {
    const { ctx } = createContext()
    Object.defineProperty(ctx, 'state', { value: 'suspended', configurable: true })
    ctx.resume = vi.fn(async () => {
      throw new Error('resume blocked')
    }) as typeof ctx.resume

    const play = vi.fn(async () => {})
    const listeners = new Map<string, () => void>()
    const audio = {
      src: 'blob:suspended',
      play,
      pause: vi.fn(),
      addEventListener: vi.fn((type: string, listener: () => void) => {
        listeners.set(type, listener)
      }),
      removeEventListener: vi.fn((type: string) => {
        listeners.delete(type)
      }),
    }

    vi.stubGlobal('Audio', vi.fn(() => audio))
    vi.stubGlobal('URL', {
      createObjectURL: vi.fn(() => 'blob:suspended'),
      revokeObjectURL: vi.fn(),
    })

    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx)

    const playback = queue.enqueue(new ArrayBuffer(4))
    await Promise.resolve()
    await Promise.resolve()

    expect(ctx.resume).toHaveBeenCalledTimes(1)
    expect(play).toHaveBeenCalledTimes(1)

    listeners.get('ended')?.()
    await expect(playback).resolves.toBeUndefined()
  })

  it('falls back when resume succeeds but the context remains suspended', async () => {
    const { ctx } = createContext()
    Object.defineProperty(ctx, 'state', { value: 'suspended', configurable: true })
    ctx.resume = vi.fn(async () => {}) as typeof ctx.resume

    const play = vi.fn(async () => {})
    const listeners = new Map<string, () => void>()
    const audio = {
      src: 'blob:still-suspended',
      play,
      pause: vi.fn(),
      addEventListener: vi.fn((type: string, handler: () => void) => {
        listeners.set(type, handler)
      }),
      removeEventListener: vi.fn(),
    }

    vi.stubGlobal('Audio', vi.fn(() => audio))
    vi.stubGlobal('URL', {
      createObjectURL: vi.fn(() => 'blob:still-suspended'),
      revokeObjectURL: vi.fn(),
    })

    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx)

    const playback = queue.enqueue(new ArrayBuffer(4))

    await Promise.resolve()
    await Promise.resolve()

    expect(ctx.resume).toHaveBeenCalledTimes(1)
    expect(play).toHaveBeenCalledTimes(1)

    listeners.get('ended')?.()
    await expect(playback).resolves.toBeUndefined()
  })

  it('falls back when a Web Audio source cannot be created', async () => {
    const { ctx } = createContext()
    vi.spyOn(ctx, 'createBufferSource').mockImplementation(() => {
      throw new Error('source creation failed')
    })
    const play = vi.fn().mockResolvedValue(undefined)
    vi.stubGlobal('Audio', vi.fn(() => ({
      play,
      pause: vi.fn(),
      addEventListener: vi.fn((event, handler) => {
        if (event === 'ended') queueMicrotask(handler)
      }),
      removeEventListener: vi.fn(),
      src: 'blob:test',
    })))
    vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:test')
    vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => undefined)

    const queue = createAudioQueue(ctx as AudioContext)
    await queue.enqueue(new ArrayBuffer(8))

    expect(play).toHaveBeenCalledTimes(1)
    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:test')
  })

  it('waits for scheduled Web Audio chunks before starting HTMLAudio fallback', async () => {
    const { ctx, sources } = createContext()
    let createCount = 0
    const originalCreate = ctx.createBufferSource
    ctx.createBufferSource = vi.fn(() => {
      createCount += 1
      if (createCount === 2) {
        throw new Error('source creation failed')
      }
      return originalCreate()
    }) as typeof ctx.createBufferSource

    const listeners = new Map<string, () => void>()
    const play = vi.fn(async () => {})
    const audio = {
      src: 'blob:test',
      play,
      pause: vi.fn(),
      addEventListener: vi.fn((type: string, handler: () => void) => {
        listeners.set(type, handler)
      }),
      removeEventListener: vi.fn(),
    }

    vi.stubGlobal('Audio', vi.fn(() => audio))
    vi.stubGlobal('URL', {
      createObjectURL: vi.fn(() => 'blob:test'),
      revokeObjectURL: vi.fn(),
    })

    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx)

    await queue.enqueue(new ArrayBuffer(4))
    const fallback = queue.enqueue(new ArrayBuffer(8))

    await Promise.resolve()
    await Promise.resolve()

    expect(play).not.toHaveBeenCalled()
    expect(sources).toHaveLength(1)

    sources[0].onended?.()
    await Promise.resolve()

    expect(play).toHaveBeenCalledTimes(1)

    listeners.get('ended')?.()
    await fallback

    await queue.enqueue(new ArrayBuffer(16))
    expect(createCount).toBe(3)
    expect(sources).toHaveLength(1)
    expect(sources[0].start).toHaveBeenCalledWith(0.005)
  })

  it('cancels fallback playback while waiting for a scheduled Web Audio source', async () => {
    const { ctx, sources } = createContext()
    let createCount = 0
    const originalCreate = ctx.createBufferSource
    ctx.createBufferSource = vi.fn(() => {
      createCount += 1
      if (createCount === 2) {
        throw new Error('source creation failed')
      }
      return originalCreate()
    }) as typeof ctx.createBufferSource

    const play = vi.fn(async () => {})
    const audio = {
      src: 'blob:test',
      play,
      pause: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }

    vi.stubGlobal('Audio', vi.fn(() => audio))
    vi.stubGlobal('URL', {
      createObjectURL: vi.fn(() => 'blob:test'),
      revokeObjectURL: vi.fn(),
    })

    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx)
    const first = queue.enqueue(new ArrayBuffer(4))
    await first

    const fallback = queue.enqueue(new ArrayBuffer(8))
    await Promise.resolve()
    await Promise.resolve()

    expect(play).not.toHaveBeenCalled()
    expect(sources).toHaveLength(1)

    queue.cancel()

    await expect(fallback).resolves.toBeUndefined()
    expect(play).not.toHaveBeenCalled()
    expect(audio.pause).not.toHaveBeenCalled()
    expect(URL.revokeObjectURL).not.toHaveBeenCalled()
    expect(createCount).toBe(2)
  })

  it('cleans up fallback resources when HTMLAudio playback fails', async () => {
    const { ctx } = createContext()
    const listeners = new Map<string, () => void>()
    const audio = {
      src: 'blob:test',
      play: vi.fn(async () => {
        listeners.get('error')?.()
      }),
      pause: vi.fn(),
      addEventListener: vi.fn((type: string, handler: () => void) => {
        listeners.set(type, handler)
      }),
      removeEventListener: vi.fn(),
    }

    const idle = vi.fn()
    vi.stubGlobal('Audio', vi.fn(() => audio))
    vi.stubGlobal('URL', {
      createObjectURL: vi.fn(() => 'blob:test'),
      revokeObjectURL: vi.fn(),
    })

    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx, idle)

    await queue.enqueue(new ArrayBuffer(4))

    expect(audio.play).toHaveBeenCalledTimes(1)
    expect(audio.removeEventListener).toHaveBeenCalledWith(
      'ended',
      expect.any(Function)
    )
    expect(audio.removeEventListener).toHaveBeenCalledWith(
      'error',
      expect.any(Function)
    )
    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:test')
    expect(idle).toHaveBeenCalledTimes(1)
  })

  it('resolves an enqueue promise when fallback playback is cancelled', async () => {
    const { ctx } = createContext()
    ctx.decodeAudioData = vi.fn(async () => {
      throw new Error('decode failed')
    }) as typeof ctx.decodeAudioData

    const listeners = new Map<string, () => void>()
    const audio = {
      src: 'blob:test',
      play: vi.fn(async () => {}),
      pause: vi.fn(),
      addEventListener: vi.fn((type: string, handler: () => void) => {
        listeners.set(type, handler)
      }),
      removeEventListener: vi.fn(),
    }

    vi.stubGlobal('Audio', vi.fn(() => audio))
    vi.stubGlobal('URL', {
      createObjectURL: vi.fn(() => 'blob:test'),
      revokeObjectURL: vi.fn(),
    })

    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx)
    const pending = queue.enqueue(new ArrayBuffer(4))

    await Promise.resolve()
    await Promise.resolve()

    queue.cancel()

    await expect(pending).resolves.toBeUndefined()
    expect(audio.pause).toHaveBeenCalledTimes(1)
  it('notifies idle only once when cancelling active fallback playback', async () => {
    const { ctx } = createContext()
    ctx.decodeAudioData = vi.fn(async () => {
      throw new Error('decode failed')
    }) as typeof ctx.decodeAudioData

    const audio = {
      src: 'blob:cancel-idle',
      play: vi.fn(async () => {}),
      pause: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }

    const idle = vi.fn()
    vi.stubGlobal('Audio', vi.fn(() => audio))
    vi.stubGlobal('URL', {
      createObjectURL: vi.fn(() => 'blob:cancel-idle'),
      revokeObjectURL: vi.fn(),
    })

    const { createAudioQueue } = await import('@/lib/audio')
    const queue = createAudioQueue(ctx, idle)
    const pending = queue.enqueue(new ArrayBuffer(4))

    await Promise.resolve()
    await Promise.resolve()

    queue.cancel()

    await expect(pending).resolves.toBeUndefined()
    expect(idle).toHaveBeenCalledTimes(1)
  })

    expect(audio.src).toBe('')
    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:test')
    expect(listeners.get('ended')).toBeDefined()
  })
})
