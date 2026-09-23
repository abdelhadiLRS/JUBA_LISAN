'use client'

import { Suspense, useCallback, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { ArrowRight, Eye, EyeOff, Globe2, Loader2, LockKeyhole, Mail } from 'lucide-react'
import { apiFetch, readApiError, syncGuestMemoryAfterLogin } from '@/lib/api'
import { mapUser } from '@/lib/mappers'
import { useAuthStore } from '@/store/auth'

function LoginForm() {
  const t = useTranslations('auth.login')
  const tCommon = useTranslations('common')
  const router = useRouter()
  const searchParams = useSearchParams()
  const registered = searchParams.get('registered') === 'true'
  const setTokens = useAuthStore((s) => s.setTokens)
  const setUser = useAuthStore((s) => s.setUser)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    const normalizedEmail = email.trim().toLowerCase()
    if (!normalizedEmail) return setError(t('emailRequired'))
    if (!password) return setError(t('passwordRequired'))
    setLoading(true)
    try {
      const res = await apiFetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: normalizedEmail, password }),
      })
      if (!res.ok) throw new Error(await readApiError(res))
      const data = await res.json() as { access_token?: string }
      if (!data.access_token) throw new Error('No access token returned by server')
      setTokens(data.access_token)
      const meRes = await apiFetch('/api/auth/me')
      if (!meRes.ok) throw new Error(await readApiError(meRes))
      setUser(mapUser(await meRes.json()))
      await syncGuestMemoryAfterLogin()
      router.replace('/dashboard')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : t('loginFailed'))
    } finally {
      setLoading(false)
    }
  }, [email, password, router, setTokens, setUser, t])

  return (
    <main className="juba-auth-mobile min-h-screen bg-[var(--juba-bg)] text-[var(--juba-text)]">
      <div className="mx-auto grid min-h-screen max-w-7xl lg:grid-cols-[1.05fr_.95fr]">
        <section className="relative hidden overflow-hidden px-10 py-10 lg:flex lg:flex-col lg:justify-between xl:px-16">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,color-mix(in_srgb,var(--juba-primary)_26%,transparent),transparent_34%),radial-gradient(circle_at_80%_70%,color-mix(in_srgb,var(--juba-warm)_18%,transparent),transparent_38%)]" />
          <div className="relative">
            <div className="flex items-center gap-3">
              <div className="grid h-11 w-11 place-items-center rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)] shadow-[var(--juba-shadow)]">
                <Image src="/logo.png" alt="JUBA LISAN" width={30} height={30} priority />
              </div>
              <span className="text-lg font-semibold tracking-tight">JUBA LISAN</span>
            </div>
            <div className="mt-28 max-w-xl">
              <p className="mb-5 inline-flex items-center gap-2 rounded-full border border-[var(--juba-border)] bg-[var(--juba-primary-soft)] px-3 py-1.5 text-xs font-medium text-[var(--juba-primary-dark)]">
                <Globe2 className="h-3.5 w-3.5" />
                {tCommon('tagline')}
              </p>
              <h2 className="text-5xl font-semibold leading-[1.05] tracking-tight xl:text-6xl">
                Learn languages with a platform built around <span className="text-[var(--juba-primary-dark)]">you.</span>
              </h2>
              <p className="mt-6 max-w-lg text-base leading-7 text-[var(--juba-muted)]">
                Practice, listen, speak and track your progress from one clean workspace.
              </p>
            </div>
          </div>
          <div className="relative flex items-center gap-3 text-xs text-[var(--juba-muted)]">
            <span className="h-2 w-2 rounded-full bg-[var(--juba-warm)]" />
            Secure session · Personal progress · Multi-language learning
          </div>
        </section>

        <section className="flex items-center justify-center px-5 py-10 sm:px-8">
          <div className="w-full max-w-md">
            <div className="mb-8 flex items-center gap-3 lg:hidden">
              <div className="grid h-11 w-11 place-items-center rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface)]">
                <Image src="/logo.png" alt="JUBA LISAN" width={30} height={30} priority />
              </div>
              <span className="text-lg font-semibold">JUBA LISAN</span>
            </div>

            <div className="juba-card p-6 sm:p-8">
              <div className="mb-8">
                <p className="text-sm font-medium text-[var(--juba-primary-dark)]">Welcome back</p>
                <h1 className="mt-1 text-3xl font-semibold tracking-tight">{t('title')}</h1>
                <p className="mt-2 text-sm leading-6 text-[var(--juba-muted)]">Sign in to continue your learning journey.</p>
              </div>

              {registered && (
                <div className="mb-5 rounded-2xl border border-[var(--juba-warm)] bg-[var(--juba-warm-soft)] px-4 py-3 text-sm text-[var(--juba-primary-dark)]">
                  ✓ {t('accountCreated')}
                </div>
              )}
              {error && (
                <div className="mb-5 rounded-2xl border border-[var(--juba-danger)] bg-[color-mix(in_srgb,var(--juba-danger)_10%,var(--juba-surface))] px-4 py-3 text-sm leading-5 text-[var(--juba-danger)]">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} noValidate className="space-y-5">
                <label className="block">
                  <span className="mb-2 block text-sm font-medium">{t('email')}</span>
                  <div className="relative">
                    <Mail className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--juba-muted)]" />
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} autoComplete="username" autoCorrect="off" autoCapitalize="none" spellCheck={false} required className="w-full rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] px-11 py-3.5 text-sm outline-none transition placeholder:text-[var(--juba-muted)] focus:border-[var(--juba-primary)] focus:ring-4 focus:ring-[color-mix(in_srgb,var(--juba-primary)_18%,transparent)]" />
                  </div>
                </label>
                <label className="block">
                  <span className="mb-2 block text-sm font-medium">{t('password')}</span>
                  <div className="relative">
                    <LockKeyhole className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--juba-muted)]" />
                    <input type={showPassword ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)} autoComplete="current-password" autoCorrect="off" autoCapitalize="none" spellCheck={false} required className="w-full rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] px-11 py-3.5 pr-12 text-sm outline-none transition focus:border-[var(--juba-primary)] focus:ring-4 focus:ring-[color-mix(in_srgb,var(--juba-primary)_18%,transparent)]" />
                    <button type="button" onClick={() => setShowPassword((v) => !v)} className="absolute right-2 top-1/2 -translate-y-1/2 rounded-xl p-2 text-[var(--juba-muted)] hover:bg-[var(--juba-primary-soft)] hover:text-[var(--juba-text)]" aria-label={showPassword ? t('hidePassword') : t('showPassword')}>
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                </label>
                <button disabled={loading} type="submit" className="group flex w-full items-center justify-center gap-2 rounded-2xl bg-[var(--juba-primary-dark)] px-4 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60">
                  {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
                  {loading ? t('signingIn') : t('submit')}
                </button>
              </form>

              <div className="mt-7 flex flex-col gap-3 text-center text-sm text-[var(--juba-muted)]">
                <span>{t('noAccount')} <Link href="/register" className="font-medium text-[var(--juba-primary-dark)] hover:underline">{t('register')}</Link></span>
                <Link href="/forgot-password" className="hover:text-[var(--juba-text)]">{t('forgotPassword')}</Link>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}

export default function LoginPage() {
  return <Suspense><LoginForm /></Suspense>
}
