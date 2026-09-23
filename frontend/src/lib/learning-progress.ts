const LEARNING_PROGRESS_EVENT = 'juba:learning-progress-updated'
const LEARNING_PROGRESS_KEY = 'juba:learning-progress-updated'
const LEARNING_PROGRESS_CHANNEL = 'juba:learning-progress'

let progressChannel: BroadcastChannel | null = null
let progressSubscriberCount = 0

function getProgressChannel(): BroadcastChannel | null {
  if (typeof window === 'undefined' || typeof BroadcastChannel === 'undefined') {
    return null
  }
  if (!progressChannel) {
    progressChannel = new BroadcastChannel(LEARNING_PROGRESS_CHANNEL)
  }
  return progressChannel
}

export function markLearningProgressUpdated(): void {
  if (typeof window === 'undefined') return

  const timestamp = String(Date.now())

  try {
    sessionStorage.setItem(LEARNING_PROGRESS_KEY, timestamp)
  } catch {
    // Storage can be unavailable in private/restricted browser contexts.
  }

  try {
    localStorage.setItem(LEARNING_PROGRESS_KEY, timestamp)
  } catch {
    // Local storage can be unavailable in private/restricted browser contexts.
  }

  window.dispatchEvent(new CustomEvent(LEARNING_PROGRESS_EVENT, { detail: { timestamp } }))

  try {
    progressChannel?.postMessage({ type: LEARNING_PROGRESS_EVENT, timestamp })
  } catch {
    // BroadcastChannel can be unavailable or closed in restricted browser contexts.
  }
}

export function subscribeToLearningProgressUpdated(listener: () => void): () => void {
  if (typeof window === 'undefined') return () => undefined

  const channel = getProgressChannel()
  if (channel) progressSubscriberCount += 1
  let lastSignalTimestamp = ''
  const notify = (timestamp?: string) => {
    if (timestamp && timestamp === lastSignalTimestamp) return
    if (timestamp) lastSignalTimestamp = timestamp
    listener()
  }
  const onChannelMessage = (event: MessageEvent<{ type?: string; timestamp?: string }>) => {
    if (event.data?.type === LEARNING_PROGRESS_EVENT) {
      notify(event.data.timestamp)
    }
  }
  const onStorage = (event: StorageEvent) => {
    if (event.storageArea === localStorage && event.key === LEARNING_PROGRESS_KEY && event.newValue) {
      notify(event.newValue)
    }
  }

  window.addEventListener(LEARNING_PROGRESS_EVENT, listener)
  window.addEventListener('storage', onStorage)
  channel?.addEventListener('message', onChannelMessage)

  let active = true
  return () => {
    if (!active) return
    active = false

    window.removeEventListener(LEARNING_PROGRESS_EVENT, onLocalEvent)
    window.removeEventListener('storage', onStorage)
    channel?.removeEventListener('message', onChannelMessage)
    if (channel) {
      progressSubscriberCount = Math.max(0, progressSubscriberCount - 1)
      if (progressSubscriberCount === 0) {
        channel.close()
        progressChannel = null
      }
    }
  }
}
