'use client'

import { Suspense, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'
import { apiFetch } from '@/lib/api'

function ResetPasswordContent() {
  const t = useTranslations('auth.resetPassword')
  const router = useRouter()
  const searchParams = useSearchParams()
  const token = searchParams.get('token') ?? ''
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [done, setDone] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    if (password !== confirm) {
      setError(t('mismatch'))
      return
    }
    if (password.length < 8) {
      setError(t('tooShort'))
      return
    }
    setLoading(true)
    try {
      const res = await apiFetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, new_password: password }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || t('error'))
      }
      setDone(true)
      setTimeout(() => router.push('/login'), 2000)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : t('error'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-[var(--juba-bg)] bg-dot-grid flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="mb-10 flex flex-col items-center">
          <h1 className="text-[var(--juba-text)] font-sans text-xl font-bold tracking-wide">
            FreeLingo
          </h1>
        </div>

        <div className="border-[var(--juba-border)] bg-[var(--juba-surface)] space-y-6 border-2 border-[var(--juba-border)] p-8">
          <div className="flex items-center gap-2">
            <span className="text-[var(--juba-text)] text-[var(--juba-muted)]">●</span>
            <span className="text-[var(--juba-muted)] text-[var(--juba-muted)] font-semibold tracking-wide">
              {t('title')}
            </span>
          </div>

          {done ? (
            <p className="text-[var(--juba-muted)] font-sans text-xs leading-relaxed">
              {t('success')}
            </p>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              {!token && (
                <div className="border-red-200 text-red-600 border px-4 py-3 font-sans text-xs">
                  {t('missingToken')}
                </div>
              )}
              {error && (
                <div className="border-red-200 text-red-600 border px-4 py-3 font-sans text-xs">
                  ✕ {error}
                </div>
              )}
              <input
                type="password"
                placeholder={t('newPassword')}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="new-password"
                className="bg-[var(--juba-bg)] border-[var(--juba-border)] text-[var(--juba-text)] placeholder:text-[var(--juba-muted)] focus:border-[var(--juba-violet)] w-full border px-4 py-3 font-sans text-xs transition-colors focus:outline-none"
              />
              <input
                type="password"
                placeholder={t('confirmPassword')}
                required
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                autoComplete="new-password"
                className="bg-[var(--juba-bg)] border-[var(--juba-border)] text-[var(--juba-text)] placeholder:text-[var(--juba-muted)] focus:border-[var(--juba-violet)] w-full border px-4 py-3 font-sans text-xs transition-colors focus:outline-none"
              />
              <button
                type="submit"
                disabled={loading || !token}
                className="bg-[var(--juba-violet)] text-white hover:bg-[var(--juba-violet)]/90 w-full py-3 font-sans text-xs font-bold tracking-wide transition-colors disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 inline h-4 w-4 animate-spin" />
                    {t('saving')}
                  </>
                ) : (
                  t('submit')
                )}
              </button>
              <Link
                href="/login"
                className="text-[var(--juba-muted)] hover:text-[var(--juba-muted)] block text-center font-sans text-xs transition-colors"
              >
                {t('backToLogin')}
              </Link>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}

export default function ResetPasswordPage() {
  return (
    <Suspense>
      <ResetPasswordContent />
    </Suspense>
  )
}
