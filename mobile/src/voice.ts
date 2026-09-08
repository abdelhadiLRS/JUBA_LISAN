import {
  createAudioPlayer,
  RecordingPresets,
  requestRecordingPermissionsAsync,
  setAudioModeAsync,
} from 'expo-audio'
import type { AudioRecorder } from 'expo-audio'

export type VoiceRecording = {
  uri: string
  durationMs: number
}

let recording: AudioRecorder | null = null

type AudioRecorderConstructor = new (preset: unknown) => AudioRecorder

function getAudioRecorderConstructor(): AudioRecorderConstructor {
  const module = require('expo-audio') as { AudioRecorder?: AudioRecorderConstructor }
  if (!module.AudioRecorder) {
    throw new Error('This Expo Audio build does not expose the imperative AudioRecorder API yet.')
  }
  return module.AudioRecorder
}

export async function requestMicrophonePermission() {
  const permission = await requestRecordingPermissionsAsync()
  return permission.granted
}

export async function startRecording() {
  if (recording) return

  const granted = await requestMicrophonePermission()
  if (!granted) throw new Error('Microphone permission is required for speaking practice.')

  await setAudioModeAsync({
    allowsRecording: true,
    playsInSilentMode: true,
  })

  const Recorder = getAudioRecorderConstructor()
  const next = new Recorder(RecordingPresets.HIGH_QUALITY)
  await next.prepareToRecordAsync()
  next.record()
  recording = next
}

export async function stopRecording(): Promise<VoiceRecording | null> {
  if (!recording) return null

  const active = recording
  recording = null
  const durationMs = active.currentTime * 1000

  await active.stop()
  const uri = active.uri
  active.release()

  if (!uri) return null
  return { uri, durationMs }
}

export function isRecording() {
  return recording?.isRecording === true
}

export async function playRecording(uri: string) {
  const player = createAudioPlayer(uri)
  player.play()

  const cleanup = setInterval(() => {
    if (!player.playing && player.duration > 0 && player.currentTime >= player.duration - 0.1) {
      clearInterval(cleanup)
      player.release()
    }
  }, 250)

  return player
}
