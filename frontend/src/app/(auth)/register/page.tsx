'use client'

import { Suspense, useCallback, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { ArrowRight, Eye, EyeOff, Globe2, Loader2, LockKeyhole, Mail, UserRound } from 'lucide-react'
import { apiFetch, readApiError } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

const LANGUAGES = ['en', 'es', 'fr', 'pt', 'de', 'it', 'pl', 'nl', 'ro', 'ru'] as const
const TARGET_LANGUAGES = ['en-US', 'en-GB', 'de-DE', 'es-ES', 'fr-FR', 'it-IT', 'ja-JP', 'ko-KR', 'pt-PT', 'zh-CN'] as const

type SelectedPlan = 'monthly' | 'yearly'

function getSelectedPlan(plan: string | null): SelectedPlan | null {
  return plan === 'monthly' || plan === 'yearly' ? plan : null
}

function RegisterForm() {
  const t = useTranslations('auth.register')
  const tLang = useTranslations('languages')
  const tCommon = useTranslations('common')
  const router = useRouter()
  const searchParams = useSearchParams()
  const invite = searchParams.get('invite')
  const selectedPlan = getSelectedPlan(searchParams.get('plan'))
  const setTokens = useAuthStore((s) => s.setTokens)

  const [username, setUsername] = useState('')
  const [displayName, setDisplayName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [nativeLanguage, setNativeLanguage] = useState('fr')
  const [targetLanguage, setTargetLanguage] = useState('en-GB')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [termsAccepted, setTermsAccepted] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    const cleanUsername = username.trim().replace(/\s+/g, '_').toLowerCase()
    const cleanEmail = email.trim().toLowerCase()
    if (!/^[a-zA-Z0-9._-]{3,50}$/.test(cleanUsername)) return setError(t('invalidUsernameChars'))
    if (!cleanEmail) return setError(t('invalidEmail'))
    if (password !== confirmPassword) return setError(t('passwordMismatch'))
    if (!/^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{10,25}$/.test(password)) return setError(t('invalidPassword'))
    if (!termsAccepted) return setError(t('termsRequired'))

    setLoading(true)
    try {
      const body: Record<string, string> = {
        username: cleanUsername,
        email: cleanEmail,
        password,
        display_name: displayName.trim() || cleanUsername,
        native_language: nativeLanguage,
        target_language: targetLanguage,
      }
      if (invite) body.invite_token = invite

      const res = await apiFetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!res.ok) {
        const detail = await readApiError(res)
        const normalized = detail.toLowerCase()
        if (normalized.includes('username already')) throw new Error(t('usernameTaken'))
        if (normalized.includes('email already')) throw new Error(t('emailTaken'))
        if (normalized.includes('registration is closed')) throw new Error(t('registrationClosed'))
        if (normalized.includes('invite')) throw new Error(t('invalidInvite'))
        throw new Error(detail)
      }

      const data = await res.json() as { access_token?: string }
      if (!data.access_token) throw new Error('Registration succeeded but the server returned no access token.')
      setTokens(data.access_token)
      router.replace(selectedPlan ? `/onboarding?plan=${selectedPlan}` : '/onboarding')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : t('error'))
    } finally {
      setLoading(false)
    }
  }, [username, displayName, email, password, confirmPassword, nativeLanguage, targetLanguage, termsAccepted, invite, selectedPlan, router, setTokens, t])

  return (
    <main className="min-h-screen bg-[#07111f] text-white selection:bg-cyan-300 selection:text-slate-950">
      <div className="mx-auto grid min-h-screen max-w-7xl lg:grid-cols-[.9fr_1.1fr]">
        <section className="relative hidden overflow-hidden px-10 py-10 lg:flex lg:flex-col lg:justify-between xl:px-16">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(34,211,238,.18),transparent_34%),radial-gradient(circle_at_80%_80%,rgba(99,102,241,.22),transparent_38%)]" />
          <div className="relative flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-2xl bg-white/10 ring-1 ring-white/15 backdrop-blur">
              <Image src="/logo.png" alt="FreeLingo" width={30} height={30} priority />
            </div>
            <span className="text-lg font-semibold">FreeLingo</span>
          </div>
          <div className="relative max-w-xl">
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-indigo-300/20 bg-indigo-300/10 px-3 py-1.5 text-xs text-indigo-100">
              <Globe2 className="h-3.5 w-3.5" />
              {tCommon('tagline')}
            </div>
            <h2 className="text-5xl font-semibold leading-[1.05] tracking-tight xl:text-6xl">Your language journey starts with one account.</h2>
            <p className="mt-6 max-w-lg text-base leading-7 text-slate-300">Choose your languages, set your goals and let the platform adapt your practice over time.</p>
          </div>
          <div className="relative text-xs text-slate-400">One account · Multiple languages · Personal progress</div>
        </section>

        <section className="flex items-center justify-center px-5 py-8 sm:px-8">
          <div className="w-full max-w-xl">
            <div className="mb-6 flex items-center gap-3 lg:hidden">
              <div className="grid h-11 w-11 place-items-center rounded-2xl bg-white/10 ring-1 ring-white/10"><Image src="/logo.png" alt="FreeLingo" width={30} height={30} priority /></div>
              <span className="text-lg font-semibold">FreeLingo</span>
            </div>

            <div className="rounded-3xl border border-white/10 bg-white/[.055] p-6 shadow-2xl shadow-black/30 backdrop-blur-xl sm:p-8">
              <div className="mb-7">
                <p className="text-sm font-medium text-cyan-300">Create your profile</p>
                <h1 className="mt-1 text-3xl font-semibold tracking-tight">{t('title')}</h1>
                <p className="mt-2 text-sm leading-6 text-slate-400">A few details are enough to build your first learning plan.</p>
              </div>

              {invite && <div className="mb-5 rounded-2xl border border-cyan-300/15 bg-cyan-300/10 px-4 py-3 text-sm text-cyan-100">{t('inviteActive')}</div>}
              {error && <div className="mb-5 rounded-2xl border border-rose-400/20 bg-rose-400/10 px-4 py-3 text-sm leading-5 text-rose-200">{error}</div>}

              <form onSubmit={handleSubmit} noValidate className="space-y-5">
                <div className="grid gap-5 sm:grid-cols-2">
                  <label className="block">
                    <span className="mb-2 block text-sm font-medium text-slate-200">{t('username')}</span>
                    <div className="relative"><UserRound className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" /><input value={username} onChange={(e) => setUsername(e.target.value)} required autoComplete="username" className="w-full rounded-2xl border border-white/10 bg-slate-950/50 px-11 py-3.5 text-sm outline-none transition focus:border-cyan-300/50 focus:ring-4 focus:ring-cyan-300/10" /></div>
                  </label>
                  <label className="block">
                    <span className="mb-2 block text-sm font-medium text-slate-200">{t('displayName')}</span>
                    <input value={displayName} onChange={(e) => setDisplayName(e.target.value)} placeholder={t('displayNamePlaceholder')} className="w-full rounded-2xl border border-white/10 bg-slate-950/50 px-4 py-3.5 text-sm outline-none transition placeholder:text-slate-600 focus:border-cyan-300/50 focus:ring-4 focus:ring-cyan-300/10" />
                  </label>
                </div>

                <label className="block">
                  <span className="mb-2 block text-sm font-medium text-slate-200">{t('email')}</span>
                  <div className="relative"><Mail className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" /><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" autoCapitalize="none" autoCorrect="off" spellCheck={false} className="w-full rounded-2xl border border-white/10 bg-slate-950/50 px-11 py-3.5 text-sm outline-none transition focus:border-cyan-300/50 focus:ring-4 focus:ring-cyan-300/10" /></div>
                </label>

                <div className="grid gap-5 sm:grid-cols-2">
                  {[
                    { label: t('password'), value: password, set: setPassword, show: showPassword, toggle: () => setShowPassword((v) => !v), auto: 'new-password' },
                    { label: t('confirmPassword'), value: confirmPassword, set: setConfirmPassword, show: showConfirmPassword, toggle: () => setShowConfirmPassword((v) => !v), auto: 'new-password' },
                  ].map((field) => (
                    <label key={field.label} className="block">
                      <span className="mb-2 block text-sm font-medium text-slate-200">{field.label}</span>
                      <div className="relative"><LockKeyhole className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" /><input type={field.show ? 'text' : 'password'} value={field.value} onChange={(e) => field.set(e.target.value)} required autoComplete={field.auto} className="w-full rounded-2xl border border-white/10 bg-slate-950/50 px-11 py-3.5 pr-12 text-sm outline-none transition focus:border-cyan-300/50 focus:ring-4 focus:ring-cyan-300/10" /><button type="button" onClick={field.toggle} className="absolute right-2 top-1/2 -translate-y-1/2 rounded-xl p-2 text-slate-500 hover:bg-white/5 hover:text-white">{field.show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}</button></div>
                    </label>
                  ))}
                </div>

                <div className="grid gap-5 sm:grid-cols-2">
                  <label className="block"><span className="mb-2 block text-sm font-medium text-slate-200">{t('nativeLanguage')}</span><select value={nativeLanguage} onChange={(e) => setNativeLanguage(e.target.value)} className="w-full rounded-2xl border border-white/10 bg-slate-950/50 px-4 py-3.5 text-sm outline-none focus:border-cyan-300/50">{LANGUAGES.map((code) => <option key={code} value={code}>{tLang(code)}</option>)}</select></label>
                  <label className="block"><span className="mb-2 block text-sm font-medium text-slate-200">Learning language</span><select value={targetLanguage} onChange={(e) => setTargetLanguage(e.target.value)} className="w-full rounded-2xl border border-white/10 bg-slate-950/50 px-4 py-3.5 text-sm outline-none focus:border-cyan-300/50">{TARGET_LANGUAGES.map((code) => <option key={code} value={code}>{code}</option>)}</select></label>
                </div>

                <label className="flex cursor-pointer items-start gap-3 rounded-2xl border border-white/5 bg-white/[.025] p-3.5">
                  <input id="terms-accept" type="checkbox" checked={termsAccepted} onChange={(e) => setTermsAccepted(e.target.checked)} className="mt-1 h-4 w-4 accent-cyan-300" />
                  <span className="text-xs leading-5 text-slate-400">{t('termsAccept')} <Link href="/terms?from=register" className="text-slate-200 underline underline-offset-2">{t('termsLink')}</Link> {t('andWord')} <Link href="/privacy?from=register" className="text-slate-200 underline underline-offset-2">{t('privacyLink')}</Link></span>
                </label>

                <button disabled={loading} type="submit" className="group flex w-full items-center justify-center gap-2 rounded-2xl bg-cyan-300 px-4 py-3.5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-200 hover:shadow-lg hover:shadow-cyan-300/15 disabled:cursor-not-allowed disabled:opacity-60">
                  {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4 transition group-hover:translate-x-0.5" />}
                  {loading ? t('creatingAccount') : t('submit')}
                </button>
              </form>

              <p className="mt-7 text-center text-sm text-slate-400">Already have an account? <Link href="/login" className="font-medium text-cyan-300 hover:text-cyan-200">Sign in</Link></p>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}

export default function RegisterPage() {
  return <Suspense><RegisterForm /></Suspense>
}
