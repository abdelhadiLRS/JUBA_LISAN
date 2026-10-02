'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import {
  AlertTriangle,
  Bug,
  MessageSquareText,
  ShieldAlert,
  Star,
  Ticket,
  UserPlus,
  Users,
} from 'lucide-react'
import { AdminNav } from '@/components/admin/AdminNav'
import {
  AdminBadge,
  AdminMetric,
  AdminPageHeader,
  AdminPanel,
} from '@/components/admin/AdminShell'
import { apiFetch } from '@/lib/api'
import { useConfigStore } from '@/store/config'

interface AdminOverviewStats {
  users_total: number
  users_active: number
  users_inactive: number
  subscriptions_active: number
  subscriptions_trialing: number
  subscriptions_past_due: number
  feedback_total: number
  feedback_pending: number
  feedback_bug_pending: number
  reviews_pending: number
}

const actions = [
  {
    href: '/admin/users',
    key: 'manageUsers',
    descriptionKey: 'manageUsersDesc',
    icon: Users,
  },
  {
    href: '/admin/users?create=1',
    key: 'createUser',
    descriptionKey: 'createUserDesc',
    icon: UserPlus,
  },
  {
    href: '/admin/feedback',
    key: 'reviewFeedback',
    descriptionKey: 'reviewFeedbackDesc',
    icon: MessageSquareText,
  },
  {
    href: '/admin/reviews',
    key: 'reviewReviews',
    descriptionKey: 'reviewReviewsDesc',
    icon: Star,
  },
] as const

export default function AdminOverviewPage() {
  const t = useTranslations('admin')
  const maintenanceMode = useConfigStore((s) => s.maintenanceMode)
  const [stats, setStats] = useState<AdminOverviewStats | null>(null)
  const [loadingStats, setLoadingStats] = useState(true)
  const [statsError, setStatsError] = useState('')

  useEffect(() => {
    let cancelled = false
    async function loadStats() {
      setLoadingStats(true)
      setStatsError('')
      try {
        const res = await apiFetch('/api/admin/stats')
        if (!res.ok) throw new Error()
        const data = await res.json()
        if (!cancelled) setStats(data)
      } catch {
        if (!cancelled) setStatsError(t('adminStatsError'))
      } finally {
        if (!cancelled) setLoadingStats(false)
      }
    }
    loadStats()
    return () => {
      cancelled = true
    }
  }, [t])

  return (
    <div className="juba-page-shell juba-admin-shell w-full space-y-5 px-4 py-5 sm:px-6 lg:px-8">
      <div className="juba-reference-hero">
        <AdminPageHeader
          eyebrow={`${t('title')} / ${t('overview')}`}
          title={t('title')}
        />
      </div>

      <AdminNav />

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
        <AdminMetric
          label={t('users')}
          value={loadingStats ? t('loading') : (stats?.users_total ?? '—')}
          icon={Users}
        />
        <AdminMetric
          label={t('activeUsers')}
          value={loadingStats ? t('loading') : (stats?.users_active ?? '—')}
          icon={ShieldAlert}
        />
        <AdminMetric
          label={t('paidAccess')}
          value={
            loadingStats
              ? t('loading')
              : `${stats?.subscriptions_active ?? 0} / ${stats?.subscriptions_trialing ?? 0}`
          }
          icon={Ticket}
        />
        <AdminMetric
          label={t('pendingFeedback')}
          value={loadingStats ? t('loading') : (stats?.feedback_pending ?? '—')}
          icon={MessageSquareText}
        />
        <AdminMetric
          label={t('pendingReviews')}
          value={loadingStats ? t('loading') : (stats?.reviews_pending ?? '—')}
          icon={Star}
        />
      </div>

      {statsError && (
        <div className="rounded-[10px] border border-[color-mix(in_srgb,var(--duo-red)_30%,transparent)] bg-[var(--duo-card)] px-4 py-3 font-sans text-xs text-[var(--duo-red)]">
          {statsError}
        </div>
      )}

      <div
        className={`juba-reference-list-card rounded-[10px] border px-5 py-4 shadow-sm ${
          maintenanceMode
            ? 'border-[color-mix(in_srgb,var(--duo-yellow)_40%,transparent)] bg-[color-mix(in_srgb,var(--duo-yellow)_8%,transparent)]'
            : 'border-[var(--duo-line)] bg-[var(--duo-card)]'
        }`}
      >
        <div className="flex flex-wrap items-center gap-3">
          <ShieldAlert
            className={`size-5 ${
              maintenanceMode ? 'text-[var(--duo-yellow)]' : 'text-[var(--duo-muted)]'
            }`}
            aria-hidden="true"
          />
          <div className="min-w-0">
            <p className="text-[var(--duo-muted)] font-sans text-xs tracking-wide">
              {t('maintenanceTitle')}
            </p>
            <p className="mt-1 font-sans text-sm text-[var(--duo-muted)]">
              {maintenanceMode
                ? t('maintenanceOnDesc')
                : t('maintenanceOffDesc')}
            </p>
          </div>
          <Link
            href="/admin/system"
            className="border-[var(--duo-line)] text-[var(--duo-muted)] hover:text-[var(--duo-ink)] hover:border-[var(--duo-green)] ms-auto border px-3 py-2 font-semibold tracking-wide transition-colors"
          >
            {t('openSystemControls')}
          </Link>
        </div>
      </div>

      <div className="juba-reference-section"><AdminPanel title={t('operationalAlerts')}>
        <div className="divide-[var(--duo-line)] divide-y border-[var(--duo-line)]">
          <Link
            href="/admin/feedback?status=pending&type=bug"
            className="hover:bg-[var(--duo-bg)] flex flex-wrap items-center gap-3 px-5 py-4 transition-colors"
          >
            <Bug
              className={`size-5 ${stats?.feedback_bug_pending ? 'text-[var(--duo-red)]' : 'text-[var(--duo-muted)]'}`}
              aria-hidden="true"
            />
            <div className="min-w-0 flex-1">
              <p className="text-[var(--duo-ink)] font-sans text-sm">{t('pendingBugs')}</p>
              <p className="text-[var(--duo-muted)] mt-1 font-sans text-xs">
                {t('pendingBugsDesc')}
              </p>
            </div>
            <AdminBadge
              tone={stats?.feedback_bug_pending ? 'danger' : 'neutral'}
            >
              {loadingStats ? t('loading') : (stats?.feedback_bug_pending ?? 0)}
            </AdminBadge>
          </Link>
          <Link
            href="/admin/users?subscription=past_due"
            className="hover:bg-[var(--duo-bg)] flex flex-wrap items-center gap-3 px-5 py-4 transition-colors"
          >
            <AlertTriangle
              className={`size-5 ${stats?.subscriptions_past_due ? 'text-[var(--duo-yellow)]' : 'text-[var(--duo-muted)]'}`}
              aria-hidden="true"
            />
            <div className="min-w-0 flex-1">
              <p className="text-[var(--duo-ink)] font-sans text-sm">
                {t('pastDueSubscriptions')}
              </p>
              <p className="text-[var(--duo-muted)] mt-1 font-sans text-xs">
                {t('pastDueSubscriptionsDesc')}
              </p>
            </div>
            <AdminBadge
              tone={stats?.subscriptions_past_due ? 'warning' : 'neutral'}
            >
              {loadingStats
                ? t('loading')
                : (stats?.subscriptions_past_due ?? 0)}
            </AdminBadge>
          </Link>
        </div>
      </AdminPanel></div>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        {actions.map((action) => {
          const Icon = action.icon
          return (
            <Link
              key={action.href}
              href={action.href}
              className="juba-reference-list-card border-[var(--duo-line)] bg-[var(--duo-card)] hover:border-[var(--duo-green)] group rounded-[10px] border p-5 shadow-sm transition-colors"
            >
              <div className="mb-5 flex items-center justify-between">
                <Icon
                  className="text-[var(--duo-muted)] group-hover:text-[var(--duo-ink)] size-5 transition-colors"
                  aria-hidden="true"
                />
                <Ticket
                  className="text-[var(--duo-muted)] group-hover:text-[var(--duo-muted)] size-4 transition-colors"
                  aria-hidden="true"
                />
              </div>
              <p className="text-[var(--duo-ink)] font-sans text-sm tracking-wide">
                {t(action.key)}
              </p>
              <p className="text-[var(--duo-muted)] mt-2 font-sans text-xs leading-relaxed">
                {t(action.descriptionKey)}
              </p>
            </Link>
          )
        })}
      </div>
    </div>
  )
}
