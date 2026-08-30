import { useAuthStore } from '@/store/auth'
import { useLoadingStore } from '@/store/loading'

const BASE_URL = ''
let isRefreshing = false
let refreshPromise: Promise<string | null> | null = null

export async function readApiError(res: Response): Promise<string> {
  try {
    const data = (await res.json()) as { detail?: unknown; message?: unknown }
    if (typeof data.detail === 'string') return data.detail
    if (typeof data.message === 'string') return data.message
    if (Array.isArray(data.detail)) return data.detail.map((item) => item && typeof item === 'object' && 'msg' in item ? String((item as { msg?: unknown }).msg ?? '') : String(item)).filter(Boolean).join(', ')
  } catch {}
  return res.statusText || `Request failed (${res.status})`
}

async function refreshToken(): Promise<string | null> {
  if (isRefreshing && refreshPromise) return refreshPromise
  isRefreshing = true
  refreshPromise = (async () => {
    try {
      const res = await fetch(`${BASE_URL}/api/auth/refresh`, { method: 'POST', credentials: 'include' })
      if (!res.ok) throw new Error('refresh failed')
      const data = (await res.json()) as { access_token?: string }
      if (!data.access_token) throw new Error('missing access token')
      useAuthStore.getState().setTokens(data.access_token)
      return data.access_token
    } catch {
      useAuthStore.getState().logout(); return null
    } finally { isRefreshing = false; refreshPromise = null }
  })()
  return refreshPromise
}

export async function apiFetch(url: string, options: RequestInit = {}): Promise<Response> {
  const { inc, dec } = useLoadingStore.getState(); inc()
  try { return await _apiFetch(url, options) } finally { dec() }
}

async function _apiFetch(url: string, options: RequestInit = {}): Promise<Response> {
  const token = useAuthStore.getState().accessToken
  const headers = new Headers(options.headers)
  headers.set('Accept', 'application/json')
  if (token) headers.set('Authorization', `Bearer ${token}`)
  let res = await fetch(`${BASE_URL}${url}`, { ...options, headers, credentials: 'include', cache: 'no-store' })
  const isAuthEntryPoint = url === '/api/auth/login' || url === '/api/auth/register'
  if (res.status === 401 && token && !isAuthEntryPoint) {
    const newToken = await refreshToken()
    if (newToken) { headers.set('Authorization', `Bearer ${newToken}`); res = await fetch(`${BASE_URL}${url}`, { ...options, headers, credentials: 'include', cache: 'no-store' }) }
  }
  return res
}

export function apiUrl(path: string): string { return `${BASE_URL}${path}` }

export type TranslatorSavedWord = { source: string; target: string; word: string; translation: string }
const TRANSLATOR_STORAGE_KEY = 'juba_lisan_saved_vocabulary'

/** Guest-safe Translator → Vocabulary persistence. Authentication is never required. */
export function saveTranslatedWordLocally(input: TranslatorSavedWord): TranslatorSavedWord[] {
  if (typeof window === 'undefined') return [input]
  try {
    const raw = window.localStorage.getItem(TRANSLATOR_STORAGE_KEY)
    const existing: unknown = raw ? JSON.parse(raw) : []
    const words = Array.isArray(existing) ? existing.filter(Boolean) as TranslatorSavedWord[] : []
    const normalized = input.word.trim().toLowerCase()
    const next = [input, ...words.filter((item) => item.word?.trim().toLowerCase() !== normalized)]
    window.localStorage.setItem(TRANSLATOR_STORAGE_KEY, JSON.stringify(next))
    return next
  } catch { return [input] }
}
