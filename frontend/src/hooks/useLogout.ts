'use client'

import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/auth'
import { apiFetch } from '@/lib/api'

/**
 * Returns a stable handleLogout function that:
 * 1. Attempts to invalidate the server-side refresh token.
 * 2. Always clears the in-memory auth state, even if the backend is unavailable.
 * 3. Redirects to /login.
 */
export function useLogout() {
  const router = useRouter()
  const logout = useAuthStore((s) => s.logout)

  async function handleLogout() {
    try {
      await apiFetch('/api/auth/logout', { method: 'POST' })
    } finally {
      logout()
      router.push('/login')
    }
  }

  return handleLogout
}
