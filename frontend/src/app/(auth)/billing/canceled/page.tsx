'use client'

import Link from 'next/link'
import { useTranslations } from 'next-intl'

export default function BillingCanceledPage() {
  const t = useTranslations('billing')

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#f4f4f2] px-4">
      <div className="border-[rgba(7,7,9,.08)] bg-[#fff] w-full max-w-sm space-y-5 border border-[rgba(7,7,9,.08)] p-8 text-center">
        <div className="text-[rgba(32,33,39,.52)] text-2xl">△</div>
        <p className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
          {t('canceledLabel')}
        </p>
        <h1 className="text-[#202127] font-sans text-base font-bold">
          {t('canceledTitle')}
        </h1>
        <p className="text-[rgba(32,33,39,.52)] font-sans text-xs leading-relaxed">
          {t('canceledDesc')}
        </p>
        <div className="flex flex-col gap-2">
          <Link
            href="/dashboard"
            className="bg-[#5862e2] text-white hover:bg-[#5862e2]/90 block py-3 font-sans text-xs font-bold tracking-wide transition-colors"
          >
            {t('canceledCtaDashboard')}
          </Link>
          <Link
            href="/settings"
            className="border-[rgba(7,7,9,.08)] text-[rgba(32,33,39,.52)] hover:text-[#202127] hover:border-[#5862e2] block border py-3 font-sans text-xs tracking-wide transition-colors"
          >
            {t('canceledCtaSettings')}
          </Link>
        </div>
        <p className="text-[rgba(32,33,39,.52)] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
          {t('canceledNoCharge')}
        </p>
      </div>
    </div>
  )
}
