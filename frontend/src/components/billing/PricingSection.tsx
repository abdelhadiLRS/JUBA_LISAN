'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { useTranslations } from 'next-intl'
import { Circle, CircleDot, Diamond, Check, Minus, ArrowRight, Loader2 } from 'lucide-react'
import { getLandingSubscriptionState } from '@/lib/landing-subscription'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

type BillingInterval = 'monthly' | 'yearly'

interface PricingSectionProps {
  stripeEnabled: boolean
  trialDays: number
  hasSession: boolean
  priceMonthly: number
  priceYearly: number
  totalPriceMonthly: number
  totalPriceYearly: number
}

export default function PricingSection({
  stripeEnabled,
  trialDays,
  hasSession,
  priceMonthly,
  priceYearly,
  totalPriceMonthly,
  totalPriceYearly,
}: PricingSectionProps) {
  const tBilling = useTranslations('billing')
  const [subscribed, setSubscribed] = useState<boolean | null>(
    hasSession ? null : false
  )
  const [trialUsed, setTrialUsed] = useState(false)
  const [checkoutLoading, setCheckoutLoading] =
    useState<BillingInterval | null>(null)
  const [checkoutError, setCheckoutError] = useState<string | null>(null)

  useEffect(() => {
    if (!hasSession) return
    async function checkSubscription() {
      const state = await getLandingSubscriptionState()
      setSubscribed(state.subscribed)
      setTrialUsed(state.trialUsed)
    }
    checkSubscription()
  }, [hasSession])

  // Pricing is a public landing-page section. Keep it visible to visitors even
  // when Stripe is temporarily disabled; authenticated checkout still follows
  // the backend billing configuration.

  async function startCheckout(plan: BillingInterval) {
    if (checkoutLoading) return
    setCheckoutLoading(plan)
    setCheckoutError(null)

    try {
      if (!useAuthStore.getState().accessToken) {
        const refreshRes = await fetch('/api/auth/refresh', {
          method: 'POST',
          credentials: 'include',
        })
        if (!refreshRes.ok) throw new Error(tBilling('checkoutError'))
        const { access_token } = await refreshRes.json()
        useAuthStore.getState().setTokens(access_token)
      }

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
      setCheckoutError(
        err instanceof Error ? err.message : tBilling('checkoutError')
      )
      setCheckoutLoading(null)
    }
  }

  const planIcons = [Circle, CircleDot, Diamond]

  const freeRows = ['f1', 'f2', 'f3', 'f4', 'f5']
  const limitedRows = ['l1', 'l2', 'l3', 'l4', 'l5']
  const tableRows = [
    ...freeRows.map((k) => ({
      label: tBilling(`freeFeature.${k}`),
      free: true as boolean | 'limited',
      monthly: true,
      yearly: true,
    })),
    ...limitedRows.map((k) => ({
      label: tBilling(`freeFeature.${k}`),
      free: 'limited' as const,
      monthly: true,
      yearly: true,
    })),
    {
      label: tBilling('planFeature.feature1'),
      free: false as boolean | 'limited',
      monthly: true,
      yearly: true,
    },
    {
      label: tBilling('planFeature.feature2'),
      free: false,
      monthly: false,
      yearly: true,
    },
  ]

  const plans = [
    {
      name: tBilling('planFreeBadge'),
      icon: planIcons[0],
      price: null,
      priceLabel: null,
      badge: null,
      desc: tBilling('planFreeDesc'),
      badgeStyle: '',
      href: hasSession ? '/dashboard' : '/register',
      cta: tBilling('planFreeCta'),
      isFree: true as const,
    },
    {
      name: tBilling('planMonthlyName'),
      icon: planIcons[1],
      price: priceMonthly,
      priceLabel: tBilling('month'),
      originalPrice: totalPriceMonthly,
      badge: tBilling(trialUsed ? 'trialBadgeTrialUsed' : 'trialBadge'),
      desc: null,
      badgeStyle: 'text-[#275d19] border-[#3d7b27]/30',
      href: hasSession ? '/dashboard' : '/register?plan=monthly',
      cta: tBilling(trialUsed ? 'ctaRegisterTrialUsed' : 'ctaRegister'),
      isFree: false as const,
      interval: 'monthly' as const,
    },
    {
      name: tBilling('planYearlyName'),
      icon: planIcons[2],
      price: priceYearly,
      priceLabel: tBilling('year'),
      originalPrice: totalPriceYearly,
      badge: tBilling('bestValue'),
      desc: null,
      badgeStyle: 'text-[#275d19] border-[#3d7b27]/30',
      href: hasSession ? '/dashboard' : '/register?plan=yearly',
      cta: tBilling(trialUsed ? 'ctaRegisterTrialUsed' : 'ctaRegister'),
      isFree: false as const,
      interval: 'yearly' as const,
    },
  ]

  return (
    <section id="public-pricing" aria-label={tBilling('pricingTitle')} className="juba-ff-pricing mx-auto block w-full max-w-6xl px-4 pb-24 sm:px-6">
      <div className="mb-10 text-center">
        <h2 className="juba-ff-pricing-title mb-2 font-sans text-3xl font-black tracking-tight">
          {tBilling('pricingTitle')}
        </h2>
        <p className="juba-ff-pricing-subtitle font-sans text-sm">
          {tBilling(trialUsed ? 'pricingDescTrialUsed' : 'pricingDesc', {
            days: trialDays,
          })}
        </p>
      </div>

      {/* Plan cards */}
      <div className="mb-12 grid grid-cols-1 gap-4 md:grid-cols-3">
        {plans.map((plan) => {
          const Icon = plan.icon
          return (
            <div
              key={plan.name}
              className={`juba-ff-plan-card flex flex-col gap-4 rounded-[26px] border border-[#d9e5d7] bg-white p-6 shadow-[0_12px_30px_rgba(24,48,34,.07)] ${
                plan.isFree
                  ? 'juba-ff-plan-free'
                  : plan.name === tBilling('planYearlyName')
                    ? 'juba-ff-plan-yearly'
                    : 'juba-ff-plan-paid'
              }`}
            >
              <div className="juba-ff-plan-head flex items-center justify-between border-b pb-3">
                <div className="flex items-center gap-2">
                  <Icon className="juba-ff-plan-icon h-5 w-5" />
                  <span className="juba-ff-plan-name font-sans text-sm font-black tracking-tight">
                    {plan.name}
                  </span>
                </div>
                {plan.badge && (
                  <span
                    className={`text-[#68766d] border px-2 py-0.5 font-sans text-[0.65rem] font-extrabold tracking-wide uppercase ${plan.badgeStyle}`}
                  >
                    {plan.badge}
                  </span>
                )}
              </div>

              <div className="min-h-[4.25rem]">
                {plan.price !== null ? (
                  <>
                    <p className="juba-ff-plan-old font-sans text-sm line-through">
                      {plan.originalPrice > 0 ? tBilling('priceOriginal', {
                        price: plan.originalPrice,
                        period: plan.priceLabel,
                      }) : '—'}
                    </p>
                    <p className="juba-ff-plan-price flex items-baseline gap-2 font-sans text-2xl font-black">
                      {plan.price > 0 ? tBilling('priceAmount', { amount: plan.price }) : '—'}
                      <span className="text-[#68766d] text-sm">
                        {tBilling('pricePerPeriod', {
                          period: plan.priceLabel,
                        })}
                      </span>
                    </p>
                  </>
                ) : (
                  <>
                    <p
                      className="text-[#68766d] invisible font-sans text-sm"
                      aria-hidden
                    >
                      &nbsp;
                    </p>
                    <p className="juba-ff-plan-desc font-sans text-sm leading-relaxed">
                      {plan.desc}
                    </p>
                  </>
                )}
              </div>

              {hasSession && !plan.isFree ? (
                <button
                  type="button"
                  disabled={checkoutLoading !== null}
                  onClick={() => startCheckout(plan.interval)}
                  className="juba-ff-plan-cta inline-block px-6 py-2.5 text-center font-sans text-sm font-extrabold transition-colors disabled:opacity-50"
                >
                  {checkoutLoading === plan.interval ? 'Loading…' : plan.cta}
                </button>
              ) : (
                <Link
                  href={plan.href}
                  className={`inline-block px-6 py-2.5 text-center font-sans text-xs font-bold tracking-widest uppercase transition-colors ${
                    plan.isFree
                      ? 'border-[#d9e5d7] text-[#68766d] hover:text-[#183022] border'
                      : 'juba-ff-plan-cta'
                  }`}
                >
                  {plan.cta}
                </Link>
              )}
            </div>
          )
        })}
      </div>

      {/* Comparison table */}
      <div className="juba-ff-comparison overflow-hidden rounded-[26px] border border-[#d9e5d7] bg-white shadow-[0_12px_30px_rgba(24,48,34,.06)]">
        <table className="w-full table-fixed">
          <thead>
            <tr className="juba-ff-comparison-head border-b">
              <th className="text-[#68766d] w-[42%] px-3 py-3 text-left font-sans tracking-widest uppercase sm:w-auto sm:px-5">
                &nbsp;
              </th>
              <th className="text-[#68766d] sm:text-[#183022] w-[19.333%] px-1 py-3 text-center font-sans tracking-[0.18em] uppercase sm:w-auto sm:px-4 sm:tracking-widest">
                {tBilling('planFreeName')}
              </th>
              <th className="text-[#68766d] sm:text-[#183022] w-[19.333%] px-1 py-3 text-center font-sans tracking-[0.18em] uppercase sm:w-auto sm:px-4 sm:tracking-widest">
                {tBilling('planMonthlyName')}
              </th>
              <th className="text-[#68766d] text-[#68766d] sm:text-[#183022] w-[19.333%] px-1 py-3 text-center font-sans tracking-[0.18em] uppercase sm:w-auto sm:px-4 sm:tracking-widest">
                {tBilling('planYearlyName')}
              </th>
            </tr>
          </thead>
          <tbody>
            {tableRows.map((row, i) => (
              <tr
                key={i}
                className={
                  i < tableRows.length - 1 ? 'border-[#d9e5d7] border-b' : ''
                }
              >
                <td className="juba-ff-table-cell px-3 py-3 font-sans text-xs sm:px-5">
                  {row.label}
                </td>
                <td className="px-1 py-3 text-center sm:px-4">
                  {row.free === 'limited' ? (
                    <span className="juba-ff-limited font-sans text-[0.6rem] tracking-widest uppercase">
                      {tBilling('limitedLabel')}
                    </span>
                  ) : row.free ? (
                    <Check className="juba-ff-check mx-auto h-4 w-4" />
                  ) : (
                    <Minus className="juba-ff-minus mx-auto h-4 w-4" />
                  )}
                </td>
                <td className="px-1 py-3 text-center sm:px-4">
                  {row.monthly ? (
                    <Check className="text-[#275d19] mx-auto h-3.5 w-3.5" />
                  ) : (
                    <Minus className="text-[#68766d] mx-auto h-3.5 w-3.5" />
                  )}
                </td>
                <td className="px-1 py-3 text-center sm:px-4">
                  {row.yearly ? (
                    <Check className="text-[#275d19] mx-auto h-3.5 w-3.5" />
                  ) : (
                    <Minus className="text-[#68766d] mx-auto h-3.5 w-3.5" />
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-8 text-center">
        {hasSession ? (
          <button
            type="button"
            disabled={checkoutLoading !== null}
            onClick={() => startCheckout('yearly')}
            className="juba-ff-plan-cta inline-block px-10 py-3 font-sans text-xs font-bold tracking-widest uppercase transition-colors disabled:opacity-50"
          >
            {checkoutLoading === 'yearly' ? 'Loading…' : tBilling(trialUsed ? 'ctaRegisterTrialUsed' : 'ctaRegister')}
          </button>
        ) : (
          <Link
            href="/register?plan=yearly"
            className="juba-ff-plan-cta inline-block px-10 py-3 font-sans text-xs font-bold tracking-widest uppercase transition-colors"
          >
            {tBilling(trialUsed ? 'ctaRegisterTrialUsed' : 'ctaRegister')}
          </Link>
        )}
        {checkoutError && (
          <p className="juba-ff-plan-error mx-auto mt-3 max-w-xl rounded-xl border border-[var(--landing-green-dark)]/20 bg-white px-3 py-2 font-sans text-xs leading-5">
            {checkoutError}
          </p>
        )}
      </div>
    </section>
  )
}
