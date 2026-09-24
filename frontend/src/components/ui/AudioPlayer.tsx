'use client'

import { useEffect, useRef, useState } from 'react'
import { Volume2, Square, Loader2, AlertCircle } from 'lucide-react'
import { useTranslations } from 'next-intl'
import { useAuthStore } from '@/store/auth'
import { getLogger } from '@/lib/logger'

const TTS_TIMEOUT_MS = 15_000
const ttsLogger = getLogger('tts')

interface AudioPlayerProps {
  text: string
  voice?: string
  size?: 'sm' | 'md'
  className?: string
  /** If set, fetches pre-cached audio via GET from this URL instead of POST /api/tts */
  audioUrl?: string
}

type PlayerState = 'idle' | 'loading' | 'playing' | 'error'

export function AudioPlayer({
  text,
  voice,
  size = 'sm',
  className = '',
  audioUrl,
}: AudioPlayerProps) {
  const [state, setState] = useState<PlayerState>('idle')
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const controllerRef = useRef<AbortController | null>(null)
  const accessToken = useAuthStore((s) => s.accessToken)
  const t = useTranslations('audioPlayer')

  const resolvedVoice =
    voice ??
    (typeof window !== 'undefined'
      ? (localStorage.getItem('tts_voice') ?? undefined)
      : undefined)

  useEffect(() => () => controllerRef.current?.abort(), [])

  async function handleClick() {
    if (state === 'loading') return

    if (state === 'playing') {
      audioRef.current?.pause()
      audioRef.current = null
      setState('idle')
      return
    }

    setState('loading')
    controllerRef.current?.abort()
    const controller = new AbortController()
    controllerRef.current = controller
    const timeoutId = setTimeout(() => controller.abort(), TTS_TIMEOUT_MS)

    try {
      const traceId = `tts-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`
      const t0 = performance.now()

      const fetchStart = performance.now()
      const res = await fetch(
        audioUrl ?? '/api/tts',
        audioUrl
          ? {
              headers: {
                ...(accessToken
                  ? { Authorization: `Bearer ${accessToken}` }
                  : {}),
              },
              credentials: 'include' as RequestCredentials,
              signal: controller.signal,
            }
          : {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-TTS-Trace-ID': traceId,
                ...(accessToken
                  ? { Authorization: `Bearer ${accessToken}` }
                  : {}),
              },
              body: JSON.stringify({ text, voice: resolvedVoice }),
              signal: controller.signal,
            }
      )
      clearTimeout(timeoutId)
      const fetchMs = performance.now() - fetchStart
      if (!res.ok) throw new Error(`TTS error ${res.status}`)

      const blobStart = performance.now()
      const blob = await res.blob()
      const blobMs = performance.now() - blobStart

      const url = URL.createObjectURL(blob)
      const audio = new Audio(url)
      audioRef.current = audio
      setState('playing')

      const playStart = performance.now()
      await audio.play()
      const playMs = performance.now() - playStart
      const totalMs = performance.now() - t0

      const backendSynthMs = res.headers.get('X-TTS-Backend-Synth-Ms')
      const backendTotalMs = res.headers.get('X-TTS-Backend-Total-Ms')
      const proxyFetchMs = res.headers.get('X-TTS-Proxy-Fetch-Ms')
      const proxyBufferMs = res.headers.get('X-TTS-Proxy-Buffer-Ms')
      const proxyTotalMs = res.headers.get('X-TTS-Proxy-Total-Ms')
      const responseTraceId = res.headers.get('X-TTS-Trace-ID') || traceId

      if (process.env.NODE_ENV === 'development') {
        ttsLogger.info('tts-metrics', {
          traceId: responseTraceId,
          textLength: text.length,
          blobBytes: blob.size,
          client: {
            fetchMs: Number(fetchMs.toFixed(1)),
            blobMs: Number(blobMs.toFixed(1)),
            playMs: Number(playMs.toFixed(1)),
            totalMs: Number(totalMs.toFixed(1)),
          },
          proxy: {
            fetchMs: proxyFetchMs ? Number(proxyFetchMs) : null,
            bufferMs: proxyBufferMs ? Number(proxyBufferMs) : null,
            totalMs: proxyTotalMs ? Number(proxyTotalMs) : null,
          },
          backend: {
            synthMs: backendSynthMs ? Number(backendSynthMs) : null,
            totalMs: backendTotalMs ? Number(backendTotalMs) : null,
          },
        })
      }

      audio.onended = () => {
        URL.revokeObjectURL(url)
        audioRef.current = null
        setState('idle')
      }
      audio.onerror = () => {
        URL.revokeObjectURL(url)
        audioRef.current = null
        setState('error')
        setTimeout(() => setState('idle'), 2000)
      }
    } catch {
      clearTimeout(timeoutId)
      setState('error')
      setTimeout(() => setState('idle'), 2000)
    }
  }

  const sizeClass =
    size === 'sm'
      ? 'min-h-9 min-w-9 px-2.5 py-1.5 text-[11px]'
      : 'min-h-10 min-w-10 px-3 py-2 text-xs'

  const label =
    state === 'loading' ? (
      <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
    ) : state === 'playing' ? (
      <Square className="h-3.5 w-3.5 fill-current" aria-hidden="true" />
    ) : state === 'error' ? (
      <AlertCircle className="h-4 w-4" aria-hidden="true" />
    ) : (
      <Volume2 className="h-4 w-4" aria-hidden="true" />
    )

  const colorClass =
    state === 'playing'
      ? 'border-[var(--juba-app-green)] bg-[var(--juba-app-green-soft)] text-[var(--juba-app-green-dark)]'
      : state === 'loading'
        ? 'border-[var(--juba-app-line)] bg-[var(--juba-app-green-soft)] text-[var(--juba-app-muted)]'
        : state === 'error'
          ? 'border-[color-mix(in_srgb,#b33a32_40%,var(--juba-app-line))] bg-[color-mix(in_srgb,#b33a32_8%,var(--juba-app-surface))] text-[var(--juba-app-error)]'
          : 'border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] text-[var(--juba-app-muted)] hover:border-[var(--juba-app-green)] hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-green-dark)]'

  return (
    <button
      type="button"
      onClick={handleClick}
      title={state === 'playing' ? t('stop') : t('listen')}
      aria-label={state === 'playing' ? t('ariaStop') : t('ariaListen')}
      aria-busy={state === 'loading'}
      disabled={state === 'loading'}
      className={`inline-flex items-center justify-center rounded-full border-2 font-semibold shadow-[2px_2px_0_var(--juba-app-line)] transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)] focus-visible:ring-offset-2 disabled:cursor-wait disabled:opacity-80 ${colorClass} ${sizeClass} ${className}`}
    >
      {label}
    </button>
  )
}
