'use client'

import { useRef, useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { float32ToWav } from '@/lib/audio'

interface VoiceRecorderProps {
  onTranscription: (text: string) => void
  maxSeconds?: number
  disabled?: boolean
  className?: string
}

type RecorderState = 'idle' | 'recording' | 'transcribing' | 'error'

export function VoiceRecorder({
  onTranscription,
  maxSeconds = 5,
  disabled = false,
  className = '',
}: VoiceRecorderProps) {
  const [state, setState] = useState<RecorderState>('idle')
  const streamRef = useRef<MediaStream | null>(null)
  const audioCtxRef = useRef<AudioContext | null>(null)
  const chunksRef = useRef<Float32Array[]>([])
  const processorRef = useRef<ScriptProcessorNode | null>(null)
  const autoStopRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const t = useTranslations('voiceRecorder')

  function cleanupAudio() {
    if (autoStopRef.current) {
      clearTimeout(autoStopRef.current)
      autoStopRef.current = null
    }
    processorRef.current?.disconnect()
    processorRef.current = null
    audioCtxRef.current?.close()
    audioCtxRef.current = null
    streamRef.current?.getTracks().forEach((t) => t.stop())
    streamRef.current = null
  }

  async function processAndSend(inputRate: number) {
    const chunks = chunksRef.current
    chunksRef.current = []

    if (chunks.length === 0) {
      setState('error')
      setTimeout(() => setState('idle'), 2000)
      return
    }

    setState('transcribing')

    const totalLength = chunks.reduce((sum, c) => sum + c.length, 0)
    const combined = new Float32Array(totalLength)
    let offset = 0
    for (const chunk of chunks) {
      combined.set(chunk, offset)
      offset += chunk.length
    }

    let samples = combined
    if (inputRate !== 16000) {
      const offlineCtx = new OfflineAudioContext(
        1,
        Math.ceil((combined.length * 16000) / inputRate),
        16000
      )
      const buffer = offlineCtx.createBuffer(1, combined.length, inputRate)
      buffer.getChannelData(0).set(combined)
      const source = offlineCtx.createBufferSource()
      source.buffer = buffer
      source.connect(offlineCtx.destination)
      source.start(0)
      const rendered = await offlineCtx.startRendering()
      samples = rendered.getChannelData(0)
    }

    const wav = float32ToWav(samples, 16000)
    const formData = new FormData()
    formData.append(
      'audio',
      new Blob([wav], { type: 'audio/wav' }),
      'recording.wav'
    )

    try {
      const res = await apiFetch('/api/stt', {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) throw new Error(`STT error ${res.status}`)
      const { text } = (await res.json()) as { text: string }
      onTranscription(text)
      setState('idle')
    } catch {
      setState('error')
      setTimeout(() => setState('idle'), 2000)
    }
  }

  function stopRecording() {
    if (!streamRef.current) return
    const sampleRate = audioCtxRef.current?.sampleRate || 48000
    cleanupAudio()
    processAndSend(sampleRate)
  }

  async function startRecording() {
    chunksRef.current = []
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      })
      streamRef.current = stream

      const audioCtx = new AudioContext()
      audioCtxRef.current = audioCtx

      const source = audioCtx.createMediaStreamSource(stream)
      const processor = audioCtx.createScriptProcessor(4096, 1, 1)
      processorRef.current = processor

      processor.onaudioprocess = (e) => {
        const input = e.inputBuffer.getChannelData(0)
        chunksRef.current.push(new Float32Array(input))
      }

      source.connect(processor)
      processor.connect(audioCtx.destination)

      autoStopRef.current = setTimeout(() => {
        stopRecording()
      }, maxSeconds * 1000)
    } catch {
      setState('error')
      setTimeout(() => setState('idle'), 2000)
    }
  }

  async function handleClick() {
    if (disabled) return

    if (state === 'recording') {
      stopRecording()
      return
    }

    if (state !== 'idle') return

    setState('recording')
    await startRecording()
  }

  const label =
    state === 'recording'
      ? `■ ${t('stop')}`
      : state === 'transcribing'
        ? `... ${t('processing')}`
        : state === 'error'
          ? `✕ ${t('error')}`
          : `● ${t('record')}`

  const colorClass =
    state === 'recording'
      ? 'border-[color-mix(in_srgb,#b33a32_55%,var(--juba-app-line))] bg-[color-mix(in_srgb,#b33a32_8%,var(--juba-app-surface))] text-[#b33a32] animate-pulse'
      : state === 'transcribing'
        ? 'border-[var(--juba-app-line)] bg-[var(--juba-app-green-soft)] text-[var(--juba-app-muted)] animate-pulse'
        : state === 'error'
          ? 'border-[color-mix(in_srgb,#b33a32_40%,var(--juba-app-line))] bg-[color-mix(in_srgb,#b33a32_8%,var(--juba-app-surface))] text-[#b33a32]'
          : disabled
            ? 'border-[var(--juba-app-line)] bg-[var(--juba-app-green-soft)] text-[var(--juba-app-muted)] cursor-not-allowed opacity-40'
            : 'border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] text-[var(--juba-app-muted)] hover:border-[var(--juba-app-green)] hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-green-dark)]'

  return (
    <button
      onClick={handleClick}
      disabled={disabled && state === 'idle'}
      aria-label={state === 'recording' ? t('ariaStop') : t('ariaRecord')}
      className={`inline-flex items-center gap-2 rounded-xl border-2 px-3 py-2 text-xs font-semibold tracking-wide shadow-[2px_2px_0_var(--juba-app-line)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[3px_3px_0_var(--juba-app-line)] active:translate-y-0.5 active:shadow-[1px_1px_0_var(--juba-app-line)] ${colorClass} ${className}`}
    >
      {label}
    </button>
  )
}
