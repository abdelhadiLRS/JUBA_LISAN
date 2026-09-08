import AsyncStorage from '@react-native-async-storage/async-storage'

const PREFIX = 'juba_lisan_offline:'

export async function cacheSet<T>(key: string, value: T) {
  await AsyncStorage.setItem(`${PREFIX}${key}`, JSON.stringify(value))
}

export async function cacheGet<T>(key: string, fallback?: T): Promise<T> {
  const raw = await AsyncStorage.getItem(`${PREFIX}${key}`)
  if (!raw) return fallback as T
  try {
    return JSON.parse(raw) as T
  } catch {
    return fallback as T
  }
}

export async function cacheRemove(key: string) {
  await AsyncStorage.removeItem(`${PREFIX}${key}`)
}

export async function cacheClear() {
  const keys = await AsyncStorage.getAllKeys()
  const offlineKeys = keys.filter((key) => key.startsWith(PREFIX))
  if (offlineKeys.length) await AsyncStorage.multiRemove(offlineKeys)
}

export async function isOnline(timeoutMs = 4000) {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), timeoutMs)
  try {
    await fetch('https://clients3.google.com/generate_204', {
      method: 'HEAD',
      cache: 'no-store',
      signal: controller.signal,
    })
    return true
  } catch {
    return false
  } finally {
    clearTimeout(timeout)
  }
}

export const OFFLINE_KEYS = {
  todayPlan: 'today-plan',
  progress: 'progress',
  lessons: 'lessons',
  dueCards: 'due-cards',
  guestVocabulary: 'guest-vocabulary',
  pendingActions: 'pending-actions',
} as const

export type PendingAction = {
  id: string
  method: 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  path: string
  body?: unknown
  createdAt: string
}

export async function queueAction(action: PendingAction) {
  const current = await cacheGet<PendingAction[]>(OFFLINE_KEYS.pendingActions, [])
  current.push(action)
  await cacheSet(OFFLINE_KEYS.pendingActions, current)
}

export async function getPendingActions() {
  return cacheGet<PendingAction[]>(OFFLINE_KEYS.pendingActions, [])
}

export async function removePendingAction(id: string) {
  const current = await getPendingActions()
  await cacheSet(OFFLINE_KEYS.pendingActions, current.filter((item) => item.id !== id))
}
