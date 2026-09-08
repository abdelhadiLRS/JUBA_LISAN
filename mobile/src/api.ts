import AsyncStorage from '@react-native-async-storage/async-storage'
import * as SecureStore from 'expo-secure-store'
import Constants from 'expo-constants'

const TOKEN_KEY = 'juba_lisan_access_token'
const LEGACY_TOKEN_KEY = TOKEN_KEY

const configuredApiUrl =
  process.env.EXPO_PUBLIC_API_URL ||
  (Constants.expoConfig?.extra?.apiBaseUrl as string | undefined)

export const API_BASE_URL = (configuredApiUrl || 'http://localhost:8000').replace(/\/$/, '')

export type User = {
  id: number
  username: string
  displayName: string
  email?: string
  native_language?: string
  target_language?: string
  role: 'admin' | 'user'
  avatar?: string | null
}

export type ProgressSummary = {
  current_streak?: number
  total_xp?: number
  accuracy?: number
  vocabulary_mastered?: number
  vocabulary_total?: number
  vocabulary_progress?: number
  total_lessons?: number
  total_exercises?: number
}

export async function setToken(token: string) {
  await SecureStore.setItemAsync(TOKEN_KEY, token)
  await AsyncStorage.removeItem(LEGACY_TOKEN_KEY)
}

export async function clearToken() {
  await SecureStore.deleteItemAsync(TOKEN_KEY).catch(() => undefined)
  await AsyncStorage.removeItem(LEGACY_TOKEN_KEY)
}

export async function getToken() {
  const secureToken = await SecureStore.getItemAsync(TOKEN_KEY)
  if (secureToken) return secureToken
  const legacyToken = await AsyncStorage.getItem(LEGACY_TOKEN_KEY)
  if (legacyToken) {
    await SecureStore.setItemAsync(TOKEN_KEY, legacyToken)
    await AsyncStorage.removeItem(LEGACY_TOKEN_KEY)
  }
  return legacyToken
}

export async function apiFetch(path: string, options: RequestInit = {}) {
  const token = await getToken()
  const headers = new Headers(options.headers)
  if (!headers.has('Content-Type') && options.body) headers.set('Content-Type', 'application/json')
  if (token) headers.set('Authorization', `Bearer ${token}`)
  return fetch(`${API_BASE_URL}${path}`, { ...options, headers })
}

export async function login(email: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Unable to sign in')
  await setToken(data.access_token)
  // Best-effort replay of offline actions created before this login.
  try {
    const { syncPendingActions } = await import('./sync')
    await syncPendingActions()
  } catch {
    // Keep login successful even when the device is still offline.
  }
  return data.access_token as string
}

export async function me(): Promise<User> {
  const response = await apiFetch('/api/auth/me')
  if (!response.ok) throw new Error('Session expired')
  return response.json()
}

export async function progress(): Promise<ProgressSummary> {
  const response = await apiFetch('/api/progress/summary')
  if (!response.ok) throw new Error('Unable to load progress')
  return response.json()
}

export async function todayPlan() {
  const response = await apiFetch('/api/study-plan/today')
  if (!response.ok) return null
  return response.json()
}
