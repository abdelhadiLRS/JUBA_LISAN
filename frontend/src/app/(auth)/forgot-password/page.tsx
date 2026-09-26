'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'
import { apiFetch } from '@/lib/api'

export default function ForgotPasswordPage() {
  const t = useTranslations('auth.forgotPassword')
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await apiFetch('/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      })
      if (!res.ok) throw new Error(t('error'))
      setSent(true)
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
          <Image
            src="/logo.png"
            alt="JUBA LISAN"
            width={100}
            height={100}
            className="mb-4"
          />
          <h1 className="text-[#202127] font-sans text-xl font-bold tracking-wide">
            JUBA LISAN
          </h1>
        </div>

        <div className="space-y-6 rounded-[26px] border border-black/[0.08] bg-white p-8 shadow-[0_12px_30px_rgba(43,45,90,.055)]">
          <div className="flex items-center gap-2">
            <span className="text-[#202127] text-black/50">●</span>
            <span className="text-black/50 text-black/50 font-semibold tracking-wide">
              {t('title')}
            </span>
          </div>

          {sent ? (
            <div className="space-y-4">
              <p className="text-black/50 font-sans text-xs leading-relaxed">
                {t('sent')}
              </p>
              <Link
                href="/login"
                className="text-black/50 hover:text-[#202127] block font-sans text-xs underline transition-colors"
              >
                {t('backToLogin')}
              </Link>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <p className="text-black/50 font-sans text-xs leading-relaxed">
                {t('description')}
              </p>
              {error && (
                <div className="border-red-200 rounded-2xl text-red-600 border px-4 py-3 font-sans text-xs">
                  ✕ {error}
                </div>
              )}
              <input
                type="email"
                placeholder={t('emailPlaceholder')}
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoCorrect="off"
                autoCapitalize="none"
                spellCheck={false}
                className="bg-[#fafafa] border-black/[0.08] text-[#202127] placeholder:text-black/50 focus:border-[#5862e2] w-full border px-4 py-3 font-sans text-xs transition-colors focus:outline-none"
              />
              <button
                type="submit"
                disabled={loading}
                className="bg-[#373fb8] text-white hover:bg-[#373fb8]/90 w-full py-3 font-sans text-xs font-bold tracking-wide transition-colors disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 inline h-4 w-4 animate-spin" />
                    {t('sending')}
                  </>
                ) : (
                  t('submit')
                )}
              </button>
              <Link
                href="/login"
                className="text-black/50 hover:text-black/50 block text-center font-sans text-xs transition-colors"
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
