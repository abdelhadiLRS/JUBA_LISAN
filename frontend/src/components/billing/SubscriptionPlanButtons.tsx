'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { ArrowRight, Loader2 } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { splitYearlyCta, type BillingInterval } from '@/lib/billing-copy'
import { useConfigStore } from '@/store/config'

interface SubscriptionPlanButtonsProps {
  className?: string
}

export function SubscriptionPlanButtons({
  className = '',
}: SubscriptionPlanButtonsProps) {
  const tBilling = useTranslations('billing')
  const priceMonthly = useConfigStore((s) => s.priceMonthly)
  const priceYearly = useConfigStore((s) => s.priceYearly)
  const [loading, setLoading] = useState<BillingInterval | null>(null)
  const [error, setError] = useState<string | null>(null)
  const yearlyCta = splitYearlyCta(
    tBilling('planYearly', { price: String(priceYearly) })
  )

  async function startCheckout(plan: BillingInterval) {
    if (loading) return
    setLoading(plan)
    setError(null)
    try {
      const res = await apiFetch('/api/billing/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail ?? tBilling('checkoutError'))
      }
      const { url } = await res.json()
      window.location.assign(url)
    } catch (err) {
      setError(err instanceof Error ? err.message : tBilling('checkoutError'))
      setLoading(null)
    }
  }

  return (
    <div className={`space-y-3 juba-billing-actions ${className}`}>
      <div className="flex flex-col gap-3 sm:flex-row">
        <button
          type="button"
          onClick={() => startCheckout('yearly')}
          disabled={loading !== null}
          className="bg-[var(--duo-green)] hover:bg-[var(--duo-green-dark)] text-white flex-1 rounded-xl px-4 py-2.5 text-xs font-bold shadow-[0_3px_0_var(--duo-green-dark)] transition-colors disabled:opacity-50"
        >
          {loading === 'yearly' ? (
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
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
          type="button"
          onClick={() => startCheckout('monthly')}
          disabled={loading !== null}
          className="border-2 border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-green)] hover:text-[var(--duo-green-dark)] flex-1 rounded-xl px-4 py-2.5 text-xs font-bold transition-colors disabled:opacity-50"
        >
          {loading === 'monthly' ? (
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
          ) : (
            <><span>{tBilling('planMonthly', { price: String(priceMonthly) })}</span><ArrowRight className="h-4 w-4" /></>
          )}
        </button>
      </div>
      {error && <p className="rounded-xl border border-[var(--duo-red)]/30 bg-[color-mix(in_srgb,var(--duo-red)_8%,transparent)] px-3 py-2 text-[var(--duo-red)] font-sans text-xs leading-5">{error}</p>}
    </div>
  )
}
