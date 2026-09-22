'use client'

import { useEffect, useRef, useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'

interface ExerciseAudioPlayerProps {
  exerciseId: number
  onFirstPlay?: () => void
}

export function ExerciseAudioPlayer({
  exerciseId,
  onFirstPlay,
}: ExerciseAudioPlayerProps) {
  const t = useTranslations('listening')
  const [state, setState] = useState<
    'idle' | 'loading' | 'playing' | 'paused' | 'error'
  >('idle')
  const [progress, setProgress] = useState(0)
  const [duration, setDuration] = useState(0)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const blobUrlRef = useRef<string | null>(null)
  const playedRef = useRef(false)
  const requestControllerRef = useRef<AbortController | null>(null)
  const requestIdRef = useRef(0)

  async function handlePlayPause() {
    if (state === 'loading') return

    if (state === 'playing') {
      audioRef.current?.pause()
      setState('paused')
      return
    }

    if (state === 'paused' && audioRef.current) {
      try {
        await audioRef.current.play()
        setState('playing')
      } catch {
        setState('error')
      }
      return
    }

    setState('loading')
    const requestId = ++requestIdRef.current
    const controller = new AbortController()
    requestControllerRef.current?.abort()
    requestControllerRef.current = controller

    try {
      const res = await apiFetch(`/api/listening/audio/${exerciseId}`, {
        signal: controller.signal,
      })
      if (!res.ok) throw new Error(`${res.status}`)
      const blob = await res.blob()
      if (controller.signal.aborted || requestId !== requestIdRef.current) return

      audioRef.current?.pause()
      if (blobUrlRef.current) {
        URL.revokeObjectURL(blobUrlRef.current)
      }
      const url = URL.createObjectURL(blob)
      blobUrlRef.current = url

      const audio = new Audio(url)
      audioRef.current = audio
      const isCurrentRequest = () =>
        !controller.signal.aborted && requestId === requestIdRef.current

      audio.addEventListener('loadedmetadata', () => {
        if (!isCurrentRequest()) return
        setDuration(audio.duration)
      })
      audio.addEventListener('timeupdate', () => {
        if (!isCurrentRequest()) return
        if (audio.duration > 0) {
          setProgress((audio.currentTime / audio.duration) * 100)
        }
      })
      audio.addEventListener('ended', () => {
        if (!isCurrentRequest()) return
        setProgress(100)
        setState('idle')
      })
      audio.addEventListener('error', () => {
        if (isCurrentRequest()) setState('error')
      })

      await audio.play()
      if (!isCurrentRequest()) return
      setState('playing')

      if (!playedRef.current) {
        playedRef.current = true
        onFirstPlay?.()
      }
    } catch (error) {
      if (controller.signal.aborted || requestId !== requestIdRef.current) return
      setState('error')
    } finally {
      if (requestId === requestIdRef.current) {
        requestControllerRef.current = null
      }
    }
  }

  function handleSeek(e: React.MouseEvent<HTMLDivElement>) {
    const audio = audioRef.current
    if (!audio || audio.duration === 0) return
    const rect = e.currentTarget.getBoundingClientRect()
    const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
    audio.currentTime = ratio * audio.duration
    setProgress(ratio * 100)
  }

  useEffect(() => {
    return () => {
      requestIdRef.current += 1
      requestControllerRef.current?.abort()
      requestControllerRef.current = null

      const audio = audioRef.current
      audio?.pause()
      if (audio) {
        audio.src = ''
      }
      audioRef.current = null

      if (blobUrlRef.current) {
        URL.revokeObjectURL(blobUrlRef.current)
        blobUrlRef.current = null
      }
    }
  }, [exerciseId])

  const icon = state === 'loading' ? '◌' : state === 'playing' ? '▐▐' : '▶'
  const label = state === 'playing' ? t('audioPause') : t('audioPlay')

  return (
    <div className="juba-card space-y-3 p-4">
      <div className="flex items-center gap-4">
        <button
          type="button"
          onClick={handlePlayPause}
          disabled={state === 'loading'}
          aria-label={label}
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[var(--juba-primary-soft)] text-[var(--juba-primary-dark)] font-mono text-sm font-bold transition-colors hover:bg-[var(--juba-primary)] hover:text-[var(--juba-text)] disabled:cursor-not-allowed disabled:opacity-40"
        >
          {icon}
        </button>

        <div
          className="h-2 flex-1 cursor-pointer overflow-hidden rounded-full bg-[var(--juba-surface-soft)]"
          onClick={handleSeek}
          onKeyDown={(e) => {
            const audio = audioRef.current
            if (!audio || audio.duration === 0) return
            if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) return
            e.preventDefault()
            if (e.key === 'Home') {
              audio.currentTime = 0
            } else if (e.key === 'End') {
              audio.currentTime = audio.duration
            } else {
              const delta = audio.duration * 0.05
              audio.currentTime = Math.max(
                0,
                Math.min(
                  audio.duration,
                  audio.currentTime + (e.key === 'ArrowRight' ? delta : -delta)
                )
              )
            }
            setProgress((audio.currentTime / audio.duration) * 100)
          }}
          role="slider"
          tabIndex={0}
          aria-label={t('audioProgress')}
          aria-orientation="horizontal"
          aria-valuenow={Math.round(progress)}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <div
            className="h-full rounded-full bg-[var(--juba-primary)] transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>

        {duration > 0 && (
          <span className="shrink-0 rounded-lg bg-[var(--juba-surface-soft)] px-2 py-1 text-xs font-medium tabular-nums text-[var(--juba-muted)]">
            {Math.ceil(duration)}s
          </span>
        )}
      </div>
      {state === 'error' && (
        <p
          className="text-xs font-medium text-[var(--juba-danger)]"
          role="alert"
        >
          {t('audioError')}
        </p>
      )}
    </div>
  )
}
