'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import {
  BookOpen,
  GraduationCap,
  Headphones,
  MessageSquare,
  Mic,
  ArrowRight,
  Loader2,
} from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { splitYearlyCta, type BillingInterval } from '@/lib/billing-copy'
import { useConfigStore } from '@/store/config'
import { useAuthStore, isSubscribed, needsPaymentRecovery } from '@/store/auth'

const PAYWALL_CONTEXT = {
  chat: {
    icon: MessageSquare,
    title: 'paywallChatTitle',
    desc: 'paywallChatDesc',
  },
  voice: {
    icon: Mic,
    title: 'paywallConversationTitle',
    desc: 'paywallConversationDesc',
  },
  listening: {
    icon: Headphones,
    title: 'paywallListeningTitle',
    desc: 'paywallListeningDesc',
  },
  reading: {
    icon: BookOpen,
    title: 'paywallReadingTitle',
    desc: 'paywallReadingDesc',
  },
  lessons: {
    icon: GraduationCap,
    title: 'paywallLessonsTitle',
    desc: 'paywallLessonsDesc',
  },
} as const

type FeatureContext = keyof typeof PAYWALL_CONTEXT

interface PaywallBannerProps {
  feature?: FeatureContext
  compact?: boolean
}

export function PaywallBanner({
  feature = 'chat',
  compact = false,
}: PaywallBannerProps) {
  const t = useTranslations('billing')
  const router = useRouter()
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const trialDays = useConfigStore((s) => s.stripeTrialDays)
  const priceMonthly = useConfigStore((s) => s.priceMonthly)
  const priceYearly = useConfigStore((s) => s.priceYearly)
  const [loading, setLoading] = useState<BillingInterval | null>(null)
  const [portalLoading, setPortalLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const paymentRecovery = needsPaymentRecovery(user)
  const yearlyCta = splitYearlyCta(
    t('planYearly', { price: String(priceYearly) })
  )

  if (!stripeEnabled || isSubscribed(user, stripeEnabled)) return null

  const context = PAYWALL_CONTEXT[feature] ?? PAYWALL_CONTEXT.chat
  const Icon = context.icon
  const trialEligible = !user?.trial_used

  async function handleCheckout(interval: BillingInterval) {
    setLoading(interval)
    setError(null)
    try {
      const res = await apiFetch('/api/billing/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan: interval }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail ?? t('checkoutError'))
      }
      const { url } = await res.json()
      window.location.assign(url)
    } catch (err) {
      setError(err instanceof Error ? err.message : t('checkoutError'))
      setLoading(null)
    }
  }

  async function handleManageBilling() {
    setPortalLoading(true)
    setError(null)
    try {
      const res = await apiFetch('/api/billing/portal', { method: 'POST' })
      if (!res.ok) throw new Error(t('portalError'))
      const { url } = await res.json()
      window.location.assign(url)
    } catch (err) {
      setError(err instanceof Error ? err.message : t('portalError'))
      setPortalLoading(false)
    }
  }

  const containerClass = compact
    ? 'border-[var(--juba-border)] bg-[var(--juba-surface)] w-full border p-5 text-center'
    : 'flex min-h-[60vh] flex-col items-center justify-center px-6 py-16 text-center'

  return (
    <div className={containerClass}>
      {compact ? (
        <div className="juba-card mx-auto w-full max-w-md p-7 sm:p-8">
          <PaywallContent />
        </div>
      ) : (
        <div className="juba-card w-full max-w-md p-7 sm:p-8">
          <PaywallContent />
        </div>
      )}
    </div>
  )

  function PaywallContent() {
    return (
      <>
        <Icon
          className="text-[var(--juba-app-green-dark)] mx-auto mb-5 h-6 w-6"
          aria-hidden="true"
        />

        <p className="juba-badge mb-3">
          {t('paywallLabel')}
        </p>
        <h2 className="text-[var(--juba-app-ink)] mb-3 font-sans text-xl font-black tracking-tight">
          {t(paymentRecovery ? 'premiumBannerPastDueTitle' : context.title)}
        </h2>
        <p className="text-[var(--juba-app-muted)] mb-6 font-sans text-sm leading-6">
          {paymentRecovery
            ? t('premiumBannerPastDueDesc')
            : t(
                context.desc ??
                  (trialEligible ? 'paywallDesc' : 'paywallDescTrialUsed'),
                { days: trialDays }
              )}
        </p>

        {paymentRecovery ? (
          <button
            onClick={handleManageBilling}
            disabled={portalLoading}
            className="bg-[var(--juba-app-green)] text-white hover:bg-[var(--juba-app-green-dark)] w-full rounded-xl border-2 border-[var(--juba-app-ink)] px-4 py-3 shadow-[3px_3px_0_var(--juba-app-ink)] font-sans text-sm font-extrabold transition-colors disabled:opacity-50"
          >
            {portalLoading ? '...' : t('updatePayment')}
          </button>
        ) : (
          <div className="flex flex-col gap-3">
            <button
              onClick={() => handleCheckout('yearly')}
              disabled={loading !== null}
              className="bg-[var(--juba-violet)] text-white hover:bg-[var(--juba-violet)]/90 w-full px-4 py-3 font-mono text-xs tracking-widest uppercase transition-colors disabled:opacity-50"
            >
              {loading === 'yearly' ? (
                '...'
              ) : (
                <span className="flex flex-col items-center gap-0.5 leading-relaxed">
                  <span>{yearlyCta.main}</span>
                  {yearlyCta.savings && (
                    <span className="text-white/80 text-[0.68rem]">
                      {yearlyCta.savings}
                    </span>
                  )}
                </span>
              )}
            </button>
            <button
              onClick={() => handleCheckout('monthly')}
              disabled={loading !== null}
              className="border-[var(--juba-app-line)] text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] hover:border-[var(--juba-app-ink)] w-full rounded-xl border-2 px-4 py-3 font-mono text-xs tracking-widest uppercase transition-colors disabled:opacity-50"
            >
              {loading === 'monthly'
                ? '...'
                : t('planMonthly', { price: String(priceMonthly) })}
            </button>
          </div>
        )}

        {error && (
          <p className="mt-4 rounded-xl border border-[var(--juba-app-error)]/25 bg-red-50 px-3 py-2 font-sans text-xs leading-5 text-[var(--juba-app-error)]">{error}</p>
        )}

        {!paymentRecovery && (
          <p className="mt-6 text-xs font-semibold leading-5 text-[var(--juba-app-muted)]">
            {t(trialEligible ? 'paywallNoCharge' : 'paywallNoChargeTrialUsed')}
          </p>
        )}

        <button
          onClick={() => router.push('/dashboard')}
          className="mt-5 inline-flex w-full items-center justify-center gap-2 text-sm font-bold text-[var(--juba-app-muted)] transition-colors hover:text-[var(--juba-app-ink)]"
        >
          {t('paywallSkip')}
        </button>
      </>
    )
  }
}
