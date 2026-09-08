import {
  AudioRecorder,
  createAudioPlayer,
  RecordingPresets,
  requestRecordingPermissionsAsync,
  setAudioModeAsync,
} from 'expo-audio'

export type VoiceRecording = {
  uri: string
  durationMs: number
}

let recording: AudioRecorder | null = null

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

  const next = new AudioRecorder(RecordingPresets.HIGH_QUALITY)
  await next.prepareToRecordAsync()
  next.record()
  recording = next
}

export async function stopRecording(): Promise<VoiceRecording | null> {
  if (!recording) return null

  const active = recording
  recording = null
  const uri = active.uri || ''
  const durationMs = active.currentTime * 1000

  await active.stop()
  active.release()

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
