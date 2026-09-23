'use client'

import { useState, useEffect, useRef } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useConfigStore } from '@/store/config'

const OPENAI_VOICES = [
  'alloy',
  'ash',
  'coral',
  'echo',
  'fable',
  'nova',
  'onyx',
  'sage',
  'shimmer',
] as const
const TTS_VOICE_STORAGE_KEY = 'tts_voice'

export function VoiceSection({ title }: { title?: string } = {}) {
  const t = useTranslations('settings')
  const ttsProvider = useConfigStore((s) => s.ttsProvider)
  const openaiTtsVoice = useConfigStore((s) => s.openaiTtsVoice)

  const [selectedVoice, setSelectedVoice] = useState<string>('')
  const [playingVoice, setPlayingVoice] = useState<string | null>(null)
  const [loadingVoice, setLoadingVoice] = useState<string | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)

  useEffect(() => {
    if (ttsProvider !== 'openai') return
    const stored =
      typeof window !== 'undefined'
        ? localStorage.getItem(TTS_VOICE_STORAGE_KEY)
        : null
    const voices: readonly string[] = OPENAI_VOICES
    setSelectedVoice(
      stored && voices.includes(stored) ? stored : openaiTtsVoice || 'nova'
    )
  }, [ttsProvider, openaiTtsVoice])

  // Cleanup audio on unmount
  useEffect(() => {
    return () => {
      audioRef.current?.pause()
      audioRef.current = null
    }
  }, [])

  function selectVoice(voice: string) {
    setSelectedVoice(voice)
    localStorage.setItem(TTS_VOICE_STORAGE_KEY, voice)
  }

  async function togglePreview(voice: string) {
    if (playingVoice === voice) {
      audioRef.current?.pause()
      audioRef.current = null
      setPlayingVoice(null)
      return
    }
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current = null
      setPlayingVoice(null)
    }
    setLoadingVoice(voice)
    try {
      const res = await apiFetch(`/api/tts/preview/${voice}`)
      if (!res.ok) return
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const audio = new Audio(url)
      audioRef.current = audio
      setPlayingVoice(voice)
      audio.onended = () => {
        URL.revokeObjectURL(url)
        setPlayingVoice(null)
        audioRef.current = null
      }
      audio.onerror = () => {
        URL.revokeObjectURL(url)
        setPlayingVoice(null)
        audioRef.current = null
      }
      await audio.play()
    } finally {
      setLoadingVoice(null)
    }
  }

  if (ttsProvider !== 'openai') return null

  return (
    <div className="border-[var(--juba-border)] bg-[var(--juba-surface)] border p-6">
      <div className="border-[var(--juba-border)] mb-5 flex items-center gap-2 border-b pb-4">
        <span className="text-[var(--juba-text)] text-[var(--juba-muted)]">●</span>
        <span className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
          {title ?? t('sectionVoice')}
        </span>
      </div>
      <p className="text-[var(--juba-muted)] text-[var(--juba-muted)] mb-4 font-mono">
        {t('voiceHint')}
      </p>
      <div className="flex items-center gap-3">
        <select
          value={selectedVoice}
          onChange={(e) => selectVoice(e.target.value)}
          className="bg-[var(--juba-bg)] border-[var(--juba-border)] text-[var(--juba-text)] focus:border-[var(--juba-border)]-2 flex-1 appearance-none border px-4 py-3 font-mono text-sm tracking-widest uppercase transition-colors focus:outline-none"
        >
          {OPENAI_VOICES.map((voice) => (
            <option key={voice} value={voice}>
              {voice}
            </option>
          ))}
        </select>
        <button
          type="button"
          onClick={() => void togglePreview(selectedVoice)}
          disabled={loadingVoice === selectedVoice}
          className="text-[var(--juba-muted)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] border-[var(--juba-border)] hover:border-[var(--juba-border)]-2 border px-4 py-3 font-mono tracking-widest whitespace-nowrap uppercase transition-colors disabled:opacity-40"
        >
          {loadingVoice === selectedVoice
            ? '...'
            : playingVoice === selectedVoice
              ? t('voiceStop')
              : t('voicePlay')}
        </button>
      </div>
    </div>
  )
}
