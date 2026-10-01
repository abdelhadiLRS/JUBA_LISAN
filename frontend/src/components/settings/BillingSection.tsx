'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore, isSubscribed, needsPaymentRecovery } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { SubscriptionPlanButtons } from '@/components/billing/SubscriptionPlanButtons'

export function BillingSection() {
  const tBilling = useTranslations('billing')
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const [portalLoading, setPortalLoading] = useState(false)
  const [portalError, setPortalError] = useState<string | null>(null)
  const paymentRecovery = needsPaymentRecovery(user)
  const canManageBilling = isSubscribed(user, stripeEnabled) || paymentRecovery

  if (!stripeEnabled) return null

  async function handleManageSubscription() {
    setPortalLoading(true)
    setPortalError(null)
    try {
      const res = await apiFetch('/api/billing/portal', { method: 'POST' })
      if (!res.ok) throw new Error(tBilling('portalError'))
      const { url } = await res.json()
      window.location.assign(url)
    } catch (err) {
      setPortalError(
        err instanceof Error ? err.message : tBilling('portalError')
      )
      setPortalLoading(false)
    }
  }

  return (
    <div className="rounded-[13px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-6 shadow-sm">
      <div className="mb-4 flex items-center gap-2 border-b border-[var(--duo-line)] pb-4">
        <span className="text-[var(--duo-muted)]">●</span>
        <span className="text-[var(--duo-muted)] font-mono tracking-widest uppercase">
          {tBilling('section')}
        </span>
      </div>
      <div className="space-y-4">
        {/* Status badge */}
        <div className="flex items-center justify-between">
          <span className="text-[var(--duo-muted)] font-mono text-xs tracking-widest uppercase">
            {tBilling('status')}
          </span>
          <span
            className={`border px-2.5 py-1 font-mono text-xs font-bold tracking-widest uppercase ${
              user?.subscription_status === 'active' &&
              !user?.cancel_at_period_end
                ? 'border-[color-mix(in_srgb,var(--duo-green-dark)_40%,transparent)] text-[var(--duo-green-dark)]'
                : user?.subscription_status === 'active' &&
                    user?.cancel_at_period_end
                  ? 'border-[var(--duo-green)]/40 text-[var(--duo-green-dark)]'
                  : user?.subscription_status === 'trialing'
                    ? 'border-[var(--duo-green)]/40 text-[var(--duo-green-dark)]'
                    : paymentRecovery
                      ? 'border-[color-mix(in_srgb,var(--duo-yellow)_40%,transparent)] text-[var(--duo-yellow)]'
                      : 'border-[var(--duo-line)] text-[var(--duo-muted)]'
            }`}
          >
            {user?.subscription_status === 'active' &&
              !user?.cancel_at_period_end &&
              tBilling('statusActive')}
            {user?.subscription_status === 'active' &&
              user?.cancel_at_period_end &&
              tBilling('statusCanceling')}
            {user?.subscription_status === 'trialing' &&
              tBilling('statusTrialing')}
            {user?.subscription_status === 'past_due' &&
              tBilling('statusPastDue')}
            {user?.subscription_status === 'unpaid' && tBilling('statusUnpaid')}
            {user?.subscription_status === 'paused' && tBilling('statusPaused')}
            {user?.subscription_status === 'incomplete' &&
              tBilling('statusIncomplete')}
            {user?.subscription_status === 'incomplete_expired' &&
              tBilling('statusIncompleteExpired')}
            {user?.subscription_status === 'canceled' &&
              tBilling('statusCanceled')}
            {(!user?.subscription_status ||
              user?.subscription_status === 'none') &&
              tBilling('statusNone')}
          </span>
        </div>

        {/* Next billing / end date */}
        {user?.subscription_ends_at &&
          (user.subscription_status === 'active' ||
            user.subscription_status === 'trialing' ||
            user.subscription_status === 'past_due' ||
            user.subscription_status === 'unpaid' ||
            user.subscription_status === 'paused' ||
            user.subscription_status === 'canceled' ||
            user.cancel_at_period_end) &&
          new Date(user.subscription_ends_at) > new Date() && (
            <div className="flex items-center justify-between">
              <span className="text-[var(--duo-muted)] font-mono text-xs tracking-widest uppercase">
                {user.subscription_status === 'canceled' ||
                user.cancel_at_period_end
                  ? tBilling('accessUntil')
                  : tBilling('nextBilling')}
              </span>
              <span className="text-[var(--duo-muted)] font-mono text-xs">
                {new Date(user.subscription_ends_at).toLocaleDateString()}
              </span>
            </div>
          )}

        {paymentRecovery && (
          <div className="rounded-[10px] border border-[color-mix(in_srgb,var(--duo-yellow)_30%,transparent)] bg-[color-mix(in_srgb,var(--duo-yellow)_5%,transparent)] p-3">
            <p className="font-mono text-xs font-bold tracking-widest text-[var(--duo-yellow)] uppercase">
              {tBilling('pastDueTitle')}
            </p>
            <p className="text-[var(--duo-muted)] mt-2 font-mono text-xs leading-relaxed">
              {tBilling('pastDueDesc')}
            </p>
          </div>
        )}

        {/* Manage or subscribe button */}
        {canManageBilling ? (
          <button
            onClick={handleManageSubscription}
            disabled={portalLoading}
            className="w-full rounded-[10px] border border-[var(--duo-line)] py-2.5 font-mono text-xs font-bold tracking-widest uppercase text-[var(--duo-muted)] transition-colors hover:border-[var(--duo-green)] hover:text-[var(--duo-green-dark)] disabled:opacity-50"
          >
            {portalLoading
              ? '...'
              : tBilling(paymentRecovery ? 'updatePayment' : 'manage')}
          </button>
        ) : (
          <SubscriptionPlanButtons />
        )}

        {portalError && (
          <p className="text-[var(--duo-muted)] font-mono text-[var(--duo-red)]">{portalError}</p>
        )}
      </div>
    </div>
  )
}
