'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import {
  MicVAD,
  type RealTimeVADOptions,
} from '@ricky0123/vad-web'
import type { SpeechProbabilities } from '@ricky0123/vad-web/dist/models'

type SafeVADOptions = Partial<RealTimeVADOptions> & {
  userSpeakingThreshold?: number
}

type SafeMicVAD = {
  loading: boolean
  errored: false | string
  listening: boolean
  userSpeaking: boolean
  start: (audioContext?: AudioContext) => Promise<void>
  pause: () => Promise<void>
  toggle: () => Promise<void>
}

export function useSafeMicVAD(
  options: SafeVADOptions
): SafeMicVAD {
  const [loading, setLoading] = useState(false)
  const [errored, setErrored] = useState<false | string>(false)
  const [listening, setListening] = useState(false)
  const [userSpeaking, setUserSpeaking] = useState(false)
  const vadRef = useRef<MicVAD | null>(null)
  const mountedRef = useRef(true)
  const startedRef = useRef(false)
  const optionsRef = useRef(options)
  const userSpeakingThreshold = options.userSpeakingThreshold ?? 0.6

  optionsRef.current = options

  const start = useCallback(async (audioContext?: AudioContext) => {
    if (loading || listening) return

    if (vadRef.current) {
      try {
        await vadRef.current.destroy()
      } catch {
        // A partially initialized VAD may not have audio instances yet.
      }
      vadRef.current = null
      startedRef.current = false
    }

    setLoading(true)
    setErrored(false)

    try {
      const current = optionsRef.current
      const vadOptions: Partial<RealTimeVADOptions> = {
        ...current,
        startOnLoad: false,
        ...(audioContext ? { audioContext } : {}),
        onFrameProcessed: (
          probabilities: SpeechProbabilities,
          frame: Float32Array
        ) => {
          setUserSpeaking(
            probabilities.isSpeech > userSpeakingThreshold
          )
          void current.onFrameProcessed?.(probabilities, frame)
        },
        onSpeechStart: () => {
          void current.onSpeechStart?.()
        },
        onSpeechEnd: (audio: Float32Array) => {
          void current.onSpeechEnd?.(audio)
        },
        onSpeechRealStart: () => {
          void current.onSpeechRealStart?.()
        },
        onVADMisfire: () => {
          void current.onVADMisfire?.()
        },
      }

      const vad = await MicVAD.new(vadOptions)
      vadRef.current = vad

      if (!mountedRef.current) {
        // Never call destroy() on an unstarted MicVAD: vad-web currently
        // throws because its audio instances are intentionally still null.
        return
      }

      await vad.start()
      startedRef.current = true
      if (!mountedRef.current) return
      setListening(true)
    } catch (error) {
      vadRef.current = null
      const message =
        error instanceof Error ? error.message : String(error)
      if (mountedRef.current) {
        setErrored(message)
        setListening(false)
      }
      throw error
    } finally {
      if (mountedRef.current) setLoading(false)
    }
  }, [listening, loading, userSpeakingThreshold])

  const pause = useCallback(async () => {
    const vad = vadRef.current
    if (!vad) return
    try {
      await vad.pause()
    } finally {
      if (mountedRef.current) {
        setListening(false)
        setUserSpeaking(false)
      }
    }
  }, [])

  const toggle = useCallback(async () => {
    if (listening) {
      await pause()
    } else {
      await start()
    }
  }, [listening, pause, start])

  useEffect(() => {
    return () => {
      mountedRef.current = false
      const vad = vadRef.current
      vadRef.current = null
      if (vad && startedRef.current) {
        // Only destroy an instance after it has successfully started.
        // The upstream react wrapper destroys unstarted instances and
        // triggers "MicVAD has null stream..." during React/Next dev remounts.
        void vad.destroy().catch(() => {})
      }
    }
  }, [])

  return {
    loading,
    errored,
    listening,
    userSpeaking,
    start,
    pause,
    toggle,
  }
}
