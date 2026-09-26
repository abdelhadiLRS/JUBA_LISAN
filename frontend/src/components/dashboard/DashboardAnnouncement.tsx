'use client'

import { useEffect, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { CheckCircle2, Megaphone, RefreshCw, X } from 'lucide-react'

import * as api from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'

type GuestSyncNotice = {
  status: 'synced' | 'failed'
  count: number
}

type BannerTranslation = {
  title: string
  subtitle: string
  description: string
}

function readGuestSyncNotice(): GuestSyncNotice | null {
  try {
    return api.getGuestSyncNotice()
  } catch {
    return null
  }
}

function isBannerTranslation(value: unknown): value is BannerTranslation {
  if (!value || typeof value !== 'object') return false
  const candidate = value as Record<string, unknown>
  return (
    typeof candidate.title === 'string' &&
    typeof candidate.subtitle === 'string' &&
    typeof candidate.description === 'string'
  )
}

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
  const [syncNotice, setSyncNotice] = useState<GuestSyncNotice | null>(null)

  useEffect(() => {
    setSyncNotice(readGuestSyncNotice())
  }, [])

  async function dismiss() {
    if (!banner) return
    setPending(true)
    setError(false)
    try {
      const response = await api.apiFetch('/api/dashboard-banner/dismiss', {
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
      await api.syncGuestMemoryAfterLogin()
      setSyncNotice(readGuestSyncNotice())
    } finally {
      setSyncing(false)
    }
  }

  function dismissSyncNotice() {
    try {
      api.clearGuestSyncNotice()
    } finally {
      setSyncNotice(null)
    }
  }

  const rawTranslations = banner?.translations
  const translationCandidates =
    rawTranslations && typeof rawTranslations === 'object'
      ? (rawTranslations as Record<string, unknown>)
      : {}
  const translation =
    [translationCandidates[locale], translationCandidates.en, ...Object.values(translationCandidates)].find(
      isBannerTranslation
    ) ?? null
  const showAnnouncement =
    Boolean(banner && translation) && dismissedRevision !== banner?.revision
  const isArabic = locale.toLowerCase().startsWith('ar')

  return (
    <>
      {syncNotice && (
        <section
          role="status"
          dir={isArabic ? 'rtl' : 'ltr'}
          className={`relative mb-6 rounded-[26px] border p-4 pr-12 shadow-[0_12px_30px_rgba(43,45,90,.055)] ${
            syncNotice.status === 'synced'
              ? 'border-[rgba(7,7,9,.08)] bg-[#ededff]'
              : 'border-[rgba(7,7,9,.08)] bg-white'
          }`}
        >
          <div className="flex items-start gap-3">
            <CheckCircle2
              className={`mt-0.5 size-5 shrink-0 ${
                syncNotice.status === 'synced'
                  ? 'text-[#5862e2]'
                  : 'text-[rgba(32,33,39,.52)]'
              }`}
              aria-hidden="true"
            />
            <div className="min-w-0">
              <p className="text-[#202127] text-sm font-semibold">
                {syncNotice.status === 'synced'
                  ? isArabic
                    ? `تمت مزامنة ${syncNotice.count} ${syncNotice.count === 1 ? 'كلمة' : 'كلمات'} محفوظة من وضع الزائر.`
                    : `${syncNotice.count} saved ${syncNotice.count === 1 ? 'word was' : 'words were'} synced from guest mode.`
                  : isArabic
                    ? 'احتفظنا بالكلمات المحفوظة على هذا الجهاز. يمكنك مزامنتها لاحقًا.'
                    : 'Your saved words are still on this device and can be synced later.'}
              </p>
              <p className="text-[rgba(32,33,39,.52)] mt-1 text-xs leading-relaxed">
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
                  className="mt-3 inline-flex items-center gap-2 rounded-full border border-[rgba(7,7,9,.08)] bg-white px-3 py-1.5 text-xs font-semibold text-[#202127] transition-colors hover:bg-[#f4f4f2] disabled:cursor-wait disabled:opacity-50"
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
            className="text-[rgba(32,33,39,.52)] hover:text-[#202127] absolute top-3 right-3 inline-flex size-8 items-center justify-center transition-colors"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        </section>
      )}

      {showAnnouncement && translation && (
        <section
          aria-labelledby="dashboard-announcement-title"
          className="relative mb-6 rounded-[26px] border border-[rgba(7,7,9,.08)] bg-[#ededff] p-5 pr-14 shadow-[0_12px_30px_rgba(43,45,90,.055)]"
        >
          <div className="flex gap-3">
            <Megaphone
              className="text-[#373fb8] mt-0.5 size-5 shrink-0"
              aria-hidden="true"
            />
            <div className="min-w-0">
              <h2
                id="dashboard-announcement-title"
                className="text-[#202127] text-lg font-extrabold leading-tight whitespace-pre-wrap"
              >
                {translation.title}
              </h2>
              <p className="text-[#373fb8] mt-1 text-xs font-extrabold tracking-[.12em] uppercase whitespace-pre-wrap">
                {translation.subtitle}
              </p>
              <p className="text-[rgba(32,33,39,.52)] mt-3 text-sm leading-relaxed whitespace-pre-wrap">
                {translation.description}
              </p>
              {error && (
                <p role="alert" className="text-[#b33a32] mt-3 font-sans text-xs">
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
            className="text-[rgba(32,33,39,.52)] hover:text-[#202127] absolute top-3 right-3 inline-flex size-9 items-center justify-center transition-colors disabled:cursor-wait disabled:opacity-40"
          >
            <X className="size-5" aria-hidden="true" />
          </button>
        </section>
      )}
    </>
  )
}
