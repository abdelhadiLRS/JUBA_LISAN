const LEARNING_PROGRESS_EVENT = 'juba:learning-progress-updated'
const LEARNING_PROGRESS_KEY = 'juba:learning-progress-updated'
const LEARNING_PROGRESS_CHANNEL = 'juba:learning-progress'

let progressChannel: BroadcastChannel | null = null

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

  window.dispatchEvent(new Event(LEARNING_PROGRESS_EVENT))

  try {
    getProgressChannel()?.postMessage({ type: LEARNING_PROGRESS_EVENT, timestamp })
  } catch {
    // BroadcastChannel can be unavailable or closed in restricted browser contexts.
  }
}

export function subscribeToLearningProgressUpdated(listener: () => void): () => void {
  const channel = getProgressChannel()
  const onChannelMessage = (event: MessageEvent<{ type?: string }>) => {
    if (event.data?.type === LEARNING_PROGRESS_EVENT) {
      listener()
    }
  }
  const onStorage = (event: StorageEvent) => {
    if (event.storageArea === localStorage && event.key === LEARNING_PROGRESS_KEY && event.newValue) {
      listener()
    }
  }

  window.addEventListener(LEARNING_PROGRESS_EVENT, listener)
  window.addEventListener('storage', onStorage)
  channel?.addEventListener('message', onChannelMessage)

  return () => {
    window.removeEventListener(LEARNING_PROGRESS_EVENT, listener)
    window.removeEventListener('storage', onStorage)
    channel?.removeEventListener('message', onChannelMessage)
  }
}
