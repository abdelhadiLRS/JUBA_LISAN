const LEARNING_PROGRESS_EVENT = 'juba:learning-progress-updated'
const LEARNING_PROGRESS_KEY = 'juba:learning-progress-updated'

export function markLearningProgressUpdated(): void {
  try {
    sessionStorage.setItem(LEARNING_PROGRESS_KEY, String(Date.now()))
  } catch {
    // Storage can be unavailable in private/restricted browser contexts.
  }
  window.dispatchEvent(new Event(LEARNING_PROGRESS_EVENT))
}

export function subscribeToLearningProgressUpdated(listener: () => void): () => void {
  window.addEventListener(LEARNING_PROGRESS_EVENT, listener)
  return () => window.removeEventListener(LEARNING_PROGRESS_EVENT, listener)
}
