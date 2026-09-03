'use client'

import { useEffect, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { CheckCircle2, Megaphone, RefreshCw, X } from 'lucide-react'

import {
  apiFetch,
  clearGuestSyncNotice,
  getGuestSyncNotice,
  syncGuestMemoryAfterLogin,
} from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'

export function DashboardAnnouncement() {
  const locale = useLocale()
  const t = useTranslations('dashboard')
  const banner = useConfigStore((state) => state.dashboardBanner)
  const dismissedRevision = useAuthStore(
    (state) => state.user?.dismissed_dashboard_banner_revision
  )
  const setDismissedRevision = useAuthStore(
    (state) => state.setDismissedDashboardBannerRevision
  )
  const [pending, setPending] = useState(false)
  const [syncing, setSyncing] = useState(false)
  const [error, setError] = useState(false)
  const [syncNotice, setSyncNotice] = useState<ReturnType<typeof getGuestSyncNotice>>(null)

  useEffect(() => {
    setSyncNotice(getGuestSyncNotice())
  }, [])

  async function dismiss() {
    if (!banner) return
    setPending(true)
    setError(false)
    try {
      const response = await apiFetch('/api/dashboard-banner/dismiss', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ revision: banner.revision }),
      })
      if (!response.ok) throw new Error('dismiss failed')
      setDismissedRevision(banner.revision)
    } catch {
      setError(true)
    } finally {
      setPending(false)
    }
  }

  async function retryGuestSync() {
    setSyncing(true)
    try {
      await syncGuestMemoryAfterLogin()
      setSyncNotice(getGuestSyncNotice())
    } finally {
      setSyncing(false)
    }
  }

  function dismissSyncNotice() {
    clearGuestSyncNotice()
    setSyncNotice(null)
  }

  const translation = banner
    ? banner.translations[locale] ??
      banner.translations.en ??
      Object.values(banner.translations)[0]
    : null
  const showAnnouncement =
    Boolean(banner && translation) && dismissedRevision !== banner?.revision
  const isArabic = locale.toLowerCase().startsWith('ar')

  return (
    <>
      {syncNotice && (
        <section
          role="status"
          dir={isArabic ? 'rtl' : 'ltr'}
          className={`relative mb-6 rounded-2xl border p-4 pr-12 ${
            syncNotice.status === 'synced'
              ? 'border-[color-mix(in_srgb,var(--juba-primary)_45%,var(--juba-border))] bg-[var(--juba-primary-soft)]'
              : 'border-fl-border bg-fl-surface'
          }`}
        >
          <div className="flex items-start gap-3">
            <CheckCircle2
              className={`mt-0.5 size-5 shrink-0 ${
                syncNotice.status === 'synced'
                  ? 'text-[var(--juba-primary)]'
                  : 'text-fl-muted-1'
              }`}
              aria-hidden="true"
            />
            <div className="min-w-0">
              <p className="text-fl-fg text-sm font-semibold">
                {syncNotice.status === 'synced'
                  ? isArabic
                    ? `تمت مزامنة ${syncNotice.count} ${syncNotice.count === 1 ? 'كلمة' : 'كلمات'} محفوظة من وضع الزائر.`
                    : `${syncNotice.count} saved ${syncNotice.count === 1 ? 'word was' : 'words were'} synced from guest mode.`
                  : isArabic
                    ? 'احتفظنا بالكلمات المحفوظة على هذا الجهاز. يمكنك مزامنتها لاحقًا.'
                    : 'Your saved words are still on this device and can be synced later.'}
              </p>
              <p className="text-fl-muted-2 mt-1 text-xs leading-relaxed">
                {syncNotice.status === 'synced'
                  ? isArabic
                    ? 'أصبحت الآن جزءًا من مفردات حسابك.'
                    : 'They are now part of your account vocabulary.'
                  : isArabic
                    ? 'إذا لم تكن لديك خطة دراسة، أنشئ خطة أولًا ثم أعد المحاولة.'
                    : 'If you do not have a study plan yet, create one and try again.'}
              </p>
              {syncNotice.status === 'failed' && (
                <button
                  type="button"
                  onClick={retryGuestSync}
                  disabled={syncing}
                  className="mt-3 inline-flex items-center gap-2 rounded-full border border-fl-border bg-fl-surface px-3 py-1.5 text-xs font-semibold text-fl-fg transition-colors hover:bg-[var(--juba-surface-soft)] disabled:cursor-wait disabled:opacity-50"
                >
                  <RefreshCw className={`size-3.5 ${syncing ? 'animate-spin' : ''}`} aria-hidden="true" />
                  {isArabic ? 'إعادة المزامنة' : 'Retry sync'}
                </button>
              )}
            </div>
          </div>
          <button
            type="button"
            onClick={dismissSyncNotice}
            aria-label={isArabic ? 'إغلاق' : 'Dismiss'}
            className="text-fl-muted-2 hover:text-fl-fg absolute top-3 right-3 inline-flex size-8 items-center justify-center transition-colors"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        </section>
      )}

      {showAnnouncement && translation && (
        <section
          aria-labelledby="dashboard-announcement-title"
          className="border-fl-accent/50 bg-fl-accent/5 relative mb-6 border p-5 pr-14"
        >
          <div className="flex gap-3">
            <Megaphone
              className="text-fl-accent mt-0.5 size-5 shrink-0"
              aria-hidden="true"
            />
            <div className="min-w-0">
              <h2
                id="dashboard-announcement-title"
                className="text-fl-fg font-mono text-lg font-bold whitespace-pre-wrap"
              >
                {translation.title}
              </h2>
              <p className="text-fl-accent mt-1 font-mono text-xs font-bold tracking-wide whitespace-pre-wrap">
                {translation.subtitle}
              </p>
              <p className="text-fl-muted-1 mt-3 font-mono text-sm leading-relaxed whitespace-pre-wrap">
                {translation.description}
              </p>
              {error && (
                <p role="alert" className="text-fl-error mt-3 font-mono text-xs">
                  {t('announcementDismissError')}
                </p>
              )}
            </div>
          </div>
          <button
            type="button"
            onClick={dismiss}
            disabled={pending}
            aria-label={t('announcementDismiss')}
            className="text-fl-muted-2 hover:text-fl-fg absolute top-3 right-3 inline-flex size-9 items-center justify-center transition-colors disabled:cursor-wait disabled:opacity-40"
          >
            <X className="size-5" aria-hidden="true" />
          </button>
        </section>
      )}
    </>
  )
}
