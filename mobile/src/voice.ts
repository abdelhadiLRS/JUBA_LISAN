import { Audio } from 'expo-av'

export type VoiceRecording = {
  uri: string
  durationMs: number
}

let recording: Audio.Recording | null = null

export async function requestMicrophonePermission() {
  const permission = await Audio.requestPermissionsAsync()
  return permission.granted
}

export async function startRecording() {
  if (recording) return

  const granted = await requestMicrophonePermission()
  if (!granted) throw new Error('Microphone permission is required for speaking practice.')

  await Audio.setAudioModeAsync({
    allowsRecordingIOS: true,
    playsInSilentModeIOS: true,
    shouldDuckAndroid: true,
    playThroughEarpieceAndroid: false,
  })

  const result = await Audio.Recording.createAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY)
  recording = result.recording
}

export async function stopRecording(): Promise<VoiceRecording | null> {
  if (!recording) return null

  const active = recording
  recording = null
  await active.stopAndUnloadAsync()
  const status = await active.getStatusAsync()

  return {
    uri: active.getURI() || '',
    durationMs: 'durationMillis' in status && typeof status.durationMillis === 'number' ? status.durationMillis : 0,
  }
}

export function isRecording() {
  return recording !== null
}

export async function playRecording(uri: string) {
  const sound = await Audio.Sound.createAsync({ uri }, { shouldPlay: true })
  sound.sound.setOnPlaybackStatusUpdate((status) => {
    if (!status.isLoaded || !status.didJustFinish) return
    void sound.sound.unloadAsync()
  })
  return sound.sound
}
