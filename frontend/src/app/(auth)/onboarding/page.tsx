'use client'

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { Check, Loader2 } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { splitYearlyCta, type BillingInterval } from '@/lib/billing-copy'
import { mapUser } from '@/lib/mappers'
import { useAuthStore, isSubscribed, isFreemiumTrialActive } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useLanguageStore } from '@/store/language'
import TargetLanguageSelector from '@/components/TargetLanguageSelector'
import { DEFAULT_TARGET_LANGUAGE } from '@/lib/target-languages'

const LEARNING_GOALS = [
  'travel',
  'work',
  'academic',
  'daily',
  'media',
  'emigration',
  'exams',
  'social',
] as const

type LearningGoal = (typeof LEARNING_GOALS)[number]

function getSelectedPlan(plan: string | null): BillingInterval | null {
  return plan === 'monthly' || plan === 'yearly' ? plan : null
}

const btnPrimary =
  'inline-flex w-full items-center justify-center gap-2 rounded-xl py-3 text-sm font-semibold text-white transition-colors disabled:opacity-50'
const btnGhost =
  'inline-flex w-full items-center justify-center py-1 text-xs font-medium text-[var(--juba-muted)] transition-colors hover:text-[var(--juba-text)] disabled:opacity-40'

export default function OnboardingPage() {
  const t = useTranslations('onboarding')
  const tCommon = useTranslations('common')
  const router = useRouter()
  const searchParams = useSearchParams()
  const setUser = useAuthStore((s) => s.setUser)
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const stripeTrialDays = useConfigStore((s) => s.stripeTrialDays)
  const priceMonthly = useConfigStore((s) => s.priceMonthly)
  const priceYearly = useConfigStore((s) => s.priceYearly)
  const loadConfig = useConfigStore((s) => s.load)
  const fetchLanguages = useLanguageStore((s) => s.fetchLanguages)
  const availableLanguageCodes = useLanguageStore(
    (s) => s.availableLanguageCodes
  )

  const isNewLanguage = searchParams.get('new') === 'true'
  const queryLanguage = searchParams.get('language')
  const selectedPlan = getSelectedPlan(searchParams.get('plan'))

  const [step, setStep] = useState<1 | 2 | 3>(1)
  const [targetLanguage, setTargetLanguage] = useState(
    queryLanguage ?? DEFAULT_TARGET_LANGUAGE
  )
  const [selectedGoals, setSelectedGoals] = useState<LearningGoal[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [languagesLoaded, setLanguagesLoaded] = useState(false)
  const [checkoutLoading, setCheckoutLoading] =
    useState<BillingInterval | null>(null)
  const [checkoutError, setCheckoutError] = useState('')

  useEffect(() => {
    loadConfig()
    fetchLanguages().then(() => {
      setLanguagesLoaded(true)
      const codes = useLanguageStore.getState().availableLanguageCodes
      if (codes.length > 0 && !codes.includes(targetLanguage)) {
        setTargetLanguage(codes[0])
      }
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fetchLanguages])

  function toggleGoal(goal: LearningGoal) {
    setSelectedGoals((prev) =>
      prev.includes(goal) ? prev.filter((g) => g !== goal) : [...prev, goal]
    )
  }

  async function handleStep1(e: React.FormEvent) {
    e.preventDefault()
    setStep(2)
  }

  const subscribed = isSubscribed(user, stripeEnabled)
  const showTrial = stripeEnabled && !subscribed
  const freemiumTrialActive = isFreemiumTrialActive(user, stripeEnabled)
  const totalSteps = showTrial || freemiumTrialActive ? 3 : 2

  async function handleStep2() {
    setLoading(true)
    setError('')
    try {
      const body: Record<string, unknown> = {
        target_language: targetLanguage,
        learning_goals: selectedGoals,
      }
      const res = await apiFetch('/api/auth/me', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!res.ok) throw new Error(t('saveFailed'))
      const updated = await res.json()
      const mapped = mapUser(updated, user)
      setUser(mapped)
      const trialActive = isFreemiumTrialActive(mapped, stripeEnabled)
      if (trialActive || showTrial) {
        setStep(3)
      } else {
        router.push('/dashboard')
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : t('saveFailed'))
    } finally {
      setLoading(false)
    }
  }

  async function handleCheckout(interval: BillingInterval) {
    setCheckoutLoading(interval)
    setCheckoutError('')
    try {
      if (!useAuthStore.getState().accessToken) {
        const refreshRes = await fetch('/api/auth/refresh', {
          method: 'POST',
          credentials: 'include',
        })
        if (!refreshRes.ok) {
          router.push('/login')
          return
        }
        const { access_token } = await refreshRes.json()
        useAuthStore.getState().setTokens(access_token)
      }

      const res = await apiFetch('/api/billing/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan: interval }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail ?? t('trialError'))
      }
      const { url } = await res.json()
      window.location.assign(url)
    } catch (err: unknown) {
      setCheckoutError(err instanceof Error ? err.message : t('trialError'))
      setCheckoutLoading(null)
    }
  }

  const checkoutPlans: BillingInterval[] =
    selectedPlan === 'monthly' ? ['monthly', 'yearly'] : ['yearly', 'monthly']
  const trialEligible = !user?.trial_used
  const yearlyCta = splitYearlyCta(
    t(trialEligible ? 'trialCtaYearly' : 'trialCtaYearlyTrialUsed', {
      price: String(priceYearly),
    })
  )

  const stepTitle =
    step === 1
      ? isNewLanguage
        ? t('newLanguageHeadline')
        : t('title')
      : step === 2
        ? t('goals.title')
        : t(trialEligible ? 'trialHeadline' : 'trialHeadlineTrialUsed')

  return (
    <div className="bg-fl-bg bg-dot-grid flex min-h-screen items-center justify-center px-4 py-10">
      <div className="w-full max-w-md">
        {/* Brand header */}
        <div className="mb-8 flex flex-col items-center">
          <span
            className="mb-3 flex h-11 w-11 items-center justify-center rounded-2xl text-base font-black text-white"
            style={{ background: 'var(--juba-primary)' }}
            aria-hidden="true"
          >
            JL
          </span>
          <h1 className="text-fl-fg text-lg font-bold tracking-wide">
            JUBA LISAN
          </h1>
          <p className="text-fl-muted-2 mt-1 text-sm">{tCommon('tagline')}</p>
        </div>

        {/* Progress dots */}
        <div
          className="mb-4 flex items-center justify-center gap-2"
          aria-label={`Step ${step} of ${totalSteps}`}
        >
          {Array.from({ length: totalSteps }).map((_, i) => (
            <span
              key={i}
              className="h-1.5 rounded-full transition-all duration-300"
              style={{
                width: i + 1 === step ? '1.75rem' : '0.375rem',
                background:
                  i + 1 <= step ? 'var(--juba-primary)' : 'var(--juba-border)',
              }}
            />
          ))}
        </div>

        <div className="border-fl-border bg-fl-surface rounded-2xl border p-6 sm:p-8">
          {/* Step indicator */}
          <div className="mb-6 flex items-center justify-between gap-2">
            <h2 className="text-fl-fg text-base font-semibold">{stepTitle}</h2>
            <span className="text-fl-muted-3 text-xs font-medium tabular-nums">
              {step}/{totalSteps}
            </span>
          </div>

          {error && (
            <div
              className="mb-5 rounded-xl px-4 py-3 text-sm"
              role="alert"
              style={{
                color: 'var(--juba-danger)',
                background:
                  'color-mix(in srgb, var(--juba-danger) 8%, transparent)',
                border:
                  '1px solid color-mix(in srgb, var(--juba-danger) 30%, transparent)',
              }}
            >
              {error}
            </div>
          )}

          {/* Step 1: Language */}
          {step === 1 && (
            <form onSubmit={handleStep1} className="space-y-6">
              <p className="text-fl-muted-2 text-sm">
                {isNewLanguage ? t('newLanguageSubtitle') : t('subtitle')}
              </p>
              <div>
                <label className="text-fl-muted-1 mb-3 block text-xs font-semibold tracking-wide uppercase">
                  {t('chooseVariant')}
                </label>
                {!languagesLoaded ? (
                  <div className="border-fl-border text-fl-muted-2 animate-pulse rounded-xl border px-4 py-3 text-sm">
                    …
                  </div>
                ) : availableLanguageCodes.length > 0 ? (
                  <TargetLanguageSelector
                    value={targetLanguage}
                    onChange={setTargetLanguage}
                    availableCodes={availableLanguageCodes}
                  />
                ) : (
                  <div className="space-y-3 text-center">
                    <p className="text-fl-muted-2 text-sm">{t('saveFailed')}</p>
                    <button
                      type="button"
                      onClick={() => {
                        setLanguagesLoaded(false)
                        fetchLanguages()
                      }}
                      className="text-fl-accent text-sm font-medium underline transition-all hover:no-underline"
                    >
                      {tCommon('retry')}
                    </button>
                  </div>
                )}
              </div>
              <button
                type="submit"
                className={`${btnPrimary} bg-[var(--juba-primary)] hover:bg-[var(--juba-primary-dark)]`}
              >
                {tCommon('next')}
              </button>
            </form>
          )}

          {/* Step 2: Learning goals */}
          {step === 2 && (
            <div className="space-y-5">
              <p className="text-fl-muted-2 text-sm">{t('goals.subtitle')}</p>
              <div className="grid grid-cols-2 gap-2">
                {LEARNING_GOALS.map((goal) => {
                  const active = selectedGoals.includes(goal)
                  return (
                    <button
                      key={goal}
                      type="button"
                      onClick={() => toggleGoal(goal)}
                      aria-pressed={active}
                      className={`rounded-xl border px-3 py-3 text-sm font-medium transition-colors ${
                        active
                          ? 'border-transparent text-white'
                          : 'border-fl-border text-fl-muted-2 hover:text-fl-fg hover:bg-[var(--juba-surface-soft)]'
                      }`}
                      style={
                        active
                          ? {
                              background: 'var(--juba-primary)',
                            }
                          : undefined
                      }
                    >
                      {t(`goals.${goal}`)}
                    </button>
                  )
                })}
              </div>
              <button
                type="button"
                disabled={loading}
                onClick={() => handleStep2()}
                className={`${btnPrimary} bg-[var(--juba-primary)] hover:bg-[var(--juba-primary-dark)]`}
              >
                {loading ? (
                  <>
                    <Loader2
                      className="h-4 w-4 animate-spin"
                      aria-hidden="true"
                    />
                    {tCommon('saving')}
                  </>
                ) : (
                  t('continue')
                )}
              </button>
              <button
                type="button"
                disabled={loading}
                onClick={() => handleStep2()}
                className={btnGhost}
              >
                {t('goals.skip')}
              </button>
            </div>
          )}

          {/* Step 3: Trial confirmation */}
          {step === 3 && freemiumTrialActive && (
            <div className="space-y-5">
              <h2 className="text-fl-fg text-center text-base font-bold">
                {t('freemiumTrialTitle')}
              </h2>
              <p className="text-fl-muted-1 text-center text-sm leading-relaxed">
                {t('freemiumTrialDesc')}
              </p>
              <ul className="text-fl-muted-2 space-y-2 text-sm">
                {[
                  'freemiumChatLabel',
                  'freemiumVoiceLabel',
                  'freemiumListeningLabel',
                  'freemiumReadingLabel',
                ].map((key) => (
                  <li key={key} className="flex items-start gap-2.5">
                    <span
                      className="mt-0.5 flex h-4.5 w-4.5 shrink-0 items-center justify-center rounded-full"
                      style={{
                        color: 'var(--juba-primary)',
                        background: 'var(--juba-primary-soft)',
                      }}
                    >
                      <Check className="h-3 w-3" aria-hidden="true" />
                    </span>
                    {t(key)}
                  </li>
                ))}
              </ul>
              <button
                type="button"
                onClick={() => router.push('/dashboard')}
                className={`${btnPrimary} bg-[var(--juba-primary)] hover:bg-[var(--juba-primary-dark)]`}
              >
                {t('goToDashboard')}
              </button>
            </div>
          )}

          {/* Step 3: Stripe subscription */}
          {step === 3 && !freemiumTrialActive && (
            <div className="space-y-5 text-center">
              <h2 className="text-fl-fg text-base font-bold">
                {t(trialEligible ? 'trialTitle' : 'trialTitleTrialUsed', {
                  days: stripeTrialDays,
                })}
              </h2>
              <p className="text-fl-muted-1 text-sm leading-relaxed">
                {t(trialEligible ? 'trialDesc' : 'trialDescTrialUsed', {
                  days: stripeTrialDays,
                })}
              </p>
              <div className="flex flex-col gap-3">
                {checkoutPlans.map((plan, index) => {
                  const isPrimary = index === 0
                  return (
                    <button
                      key={plan}
                      type="button"
                      disabled={checkoutLoading !== null}
                      onClick={() => handleCheckout(plan)}
                      className={`w-full rounded-xl py-3 text-sm font-semibold transition-colors disabled:opacity-50 ${
                        isPrimary
                          ? 'bg-[var(--juba-primary)] text-white hover:bg-[var(--juba-primary-dark)]'
                          : 'border-fl-border text-fl-muted-1 hover:text-fl-fg border hover:bg-[var(--juba-surface-soft)]'
                      }`}
                    >
                      {checkoutLoading === plan ? (
                        <Loader2
                          className="mx-auto h-4 w-4 animate-spin"
                          aria-hidden="true"
                        />
                      ) : plan === 'monthly' ? (
                        t(
                          trialEligible
                            ? 'trialCtaMonthly'
                            : 'trialCtaMonthlyTrialUsed',
                          {
                            price: String(priceMonthly),
                          }
                        )
                      ) : (
                        <span className="flex flex-col items-center gap-0.5 leading-relaxed">
                          <span>{yearlyCta.main}</span>
                          {yearlyCta.savings && (
                            <span
                              className={`text-xs ${isPrimary ? 'text-white/80' : 'text-fl-muted-3'}`}
                            >
                              {yearlyCta.savings}
                            </span>
                          )}
                        </span>
                      )}
                    </button>
                  )
                })}
              </div>
              {checkoutError && (
                <p className="text-sm" style={{ color: 'var(--juba-danger)' }}>
                  {checkoutError}
                </p>
              )}
              <p className="text-fl-muted-3 text-xs">
                {t(trialEligible ? 'trialNoCharge' : 'trialNoChargeTrialUsed')}
              </p>
              <button
                type="button"
                disabled={checkoutLoading !== null}
                onClick={() => router.push('/dashboard')}
                className={btnGhost}
              >
                {t('trialSkip')}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
