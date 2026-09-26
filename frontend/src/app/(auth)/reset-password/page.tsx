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
    <div className="bg-[#f4f4f2] flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="mb-10 flex flex-col items-center">
          <h1 className="text-[#202127] font-sans text-xl font-bold tracking-wide">
            JUBA LISAN
          </h1>
        </div>

        <div className="border-[rgba(7,7,9,.08)] bg-[#fff] space-y-6 border border-[rgba(7,7,9,.08)] p-8">
          <div className="flex items-center gap-2">
            <span className="text-[#202127] text-[rgba(32,33,39,.52)]">●</span>
            <span className="text-[rgba(32,33,39,.52)] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
              {t('title')}
            </span>
          </div>

          {done ? (
            <p className="text-[rgba(32,33,39,.52)] font-sans text-xs leading-relaxed">
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
                className="bg-[#f4f4f2] border-[rgba(7,7,9,.08)] text-[#202127] placeholder:text-[rgba(32,33,39,.52)] focus:border-[#5862e2] w-full border px-4 py-3 font-sans text-xs transition-colors focus:outline-none"
              />
              <input
                type="password"
                placeholder={t('confirmPassword')}
                required
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                autoComplete="new-password"
                className="bg-[#f4f4f2] border-[rgba(7,7,9,.08)] text-[#202127] placeholder:text-[rgba(32,33,39,.52)] focus:border-[#5862e2] w-full border px-4 py-3 font-sans text-xs transition-colors focus:outline-none"
              />
              <button
                type="submit"
                disabled={loading || !token}
                className="bg-[#5862e2] text-white hover:bg-[#5862e2]/90 w-full py-3 font-sans text-xs font-bold tracking-wide transition-colors disabled:opacity-50"
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
                className="text-[rgba(32,33,39,.52)] hover:text-[rgba(32,33,39,.52)] block text-center font-sans text-xs transition-colors"
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
