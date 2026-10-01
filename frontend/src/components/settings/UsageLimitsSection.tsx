'use client'

import { useState, useEffect } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { type QuotaStatus } from '@/types/api'

export function UsageLimitsSection({ title }: { title?: string } = {}) {
  const t = useTranslations('settings')
  const [quota, setQuota] = useState<QuotaStatus | null>(null)

  useEffect(() => {
    apiFetch('/api/auth/quota')
      .then((r) => r.json())
      .then((data: QuotaStatus) => setQuota(data))
      .catch(() => {
        /* silently ignore — section stays in skeleton state */
      })
  }, [])

  return (
    <div className="rounded-[13px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-6 shadow-sm">
      <div className="mb-5 flex items-center gap-2 border-b border-[var(--duo-line)] pb-4">
        <span className="text-[var(--duo-muted)]">●</span>
        <span className="font-mono tracking-widest uppercase text-[var(--duo-muted)]">
          {title ?? t('sectionUsageLimits')}
        </span>
      </div>
      {quota === null ? (
        <div className="animate-pulse space-y-3">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="h-4 rounded-[6px] bg-[var(--duo-line)]" />
          ))}
        </div>
      ) : (
        <div className="space-y-3">
          {[
            {
              label: t('quotaSessions'),
              used: quota.sessions_this_week,
              limit: quota.sessions_limit,
              unlimited: quota.sessions_unlimited,
              format: (v: number) => String(v),
            },
            {
              label: t('quotaMinutesDay'),
              used: quota.minutes_today,
              limit: quota.minutes_limit,
              unlimited: quota.time_unlimited,
              format: (v: number) => String(v),
            },
            {
              label: t('quotaMinutesWeek'),
              used: quota.minutes_this_week,
              limit: quota.weekly_minutes_limit,
              unlimited: quota.weekly_minutes_unlimited,
              format: (v: number) => String(v),
            },
            {
              label: t('quotaTokens'),
              used: Math.round((quota.tokens_this_month ?? 0) / 1000),
              limit: Math.round((quota.tokens_monthly_limit ?? 0) / 1000),
              unlimited: quota.tokens_unlimited ?? false,
              format: (v: number) => `${v}k`,
            },
          ].map(({ label, used, limit, unlimited, format }) => {
            const pct =
              unlimited || limit === 0
                ? null
                : Math.min(100, Math.round((used / limit) * 100))
            const exceeded = !unlimited && limit > 0 && used >= limit
            return (
              <div key={label} className="flex items-center gap-3">
                <span className="w-36 shrink-0 font-mono tracking-widest uppercase text-[var(--duo-muted)]">
                  {label}
                </span>
                {unlimited ? (
                  <span className="text-[var(--duo-muted)] text-[var(--duo-muted)] font-mono">
                    {t('quotaUnlimited')}
                  </span>
                ) : (
                  <>
                    <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-[var(--duo-line)]">
                      <div
                        className={`h-full transition-all ${exceeded ? 'bg-[var(--duo-red)]' : 'bg-[var(--duo-green)]'}`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    <span
                      className={`text-[var(--duo-muted)] font-mono tabular-nums ${exceeded ? 'text-[var(--duo-red)]' : 'text-[var(--duo-muted)]'}`}
                    >
                      {format(used)}&thinsp;/&thinsp;{format(limit)}
                    </span>
                  </>
                )}
              </div>
            )
          })}
          <p className="pt-1 font-mono text-[var(--duo-muted)]">
            {t('quotaHint')}
          </p>
        </div>
      )}
    </div>
  )
}
