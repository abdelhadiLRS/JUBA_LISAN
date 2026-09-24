'use client'

import { useEffect, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { Loader2, Megaphone, ShieldAlert } from 'lucide-react'

import { AdminNav } from '@/components/admin/AdminNav'
import { AdminPageHeader } from '@/components/admin/AdminShell'
import { apiFetch } from '@/lib/api'
import type { DashboardBannerTranslation } from '@/store/config'
import { useConfigStore } from '@/store/config'

const BANNER_LOCALES = [
  'en',
  'es',
  'fr',
  'pt',
  'de',
  'it',
  'ru',
  'nl',
  'pl',
  'ro',
] as const

type BannerLocale = (typeof BANNER_LOCALES)[number]
type BannerTranslations = Record<BannerLocale, DashboardBannerTranslation>

interface AdminDashboardBanner {
  source_locale: BannerLocale
  is_active: boolean
  revision: number
  translations: BannerTranslations
  created_at: string
  updated_at: string
}

const EMPTY_TRANSLATION: DashboardBannerTranslation = {
  title: '',
  subtitle: '',
  description: '',
}

function emptyTranslations(): BannerTranslations {
  return Object.fromEntries(
    BANNER_LOCALES.map((locale) => [locale, { ...EMPTY_TRANSLATION }])
  ) as BannerTranslations
}

export default function AdminSystemPage() {
  const t = useTranslations('admin')
  const currentLocale = useLocale()
  const defaultLocale = BANNER_LOCALES.includes(currentLocale as BannerLocale)
    ? (currentLocale as BannerLocale)
    : 'en'
  const maintenanceMode = useConfigStore((s) => s.maintenanceMode)
  const [maintenanceLoading, setMaintenanceLoading] = useState(false)
  const [maintenanceError, setMaintenanceError] = useState('')
  const [bannerLoading, setBannerLoading] = useState(true)
  const [bannerError, setBannerError] = useState('')
  const [bannerSuccess, setBannerSuccess] = useState('')
  const [translating, setTranslating] = useState(false)
  const [saving, setSaving] = useState(false)
  const [sourceLocale, setSourceLocale] = useState<BannerLocale>(defaultLocale)
  const [source, setSource] = useState({ ...EMPTY_TRANSLATION })
  const [translations, setTranslations] =
    useState<BannerTranslations>(emptyTranslations)
  const [hasTranslations, setHasTranslations] = useState(false)
  const [editorLocale, setEditorLocale] = useState<BannerLocale>(defaultLocale)
  const [isActive, setIsActive] = useState(true)
  const [revision, setRevision] = useState<number | null>(null)
  const [updatedAt, setUpdatedAt] = useState<string | null>(null)

  useEffect(() => {
    async function loadBanner() {
      try {
        const response = await apiFetch('/api/admin/dashboard-banner')
        if (!response.ok) throw new Error('load failed')
        const banner: AdminDashboardBanner | null = await response.json()
        if (banner) {
          setSourceLocale(banner.source_locale)
          setEditorLocale(banner.source_locale)
          setSource({ ...banner.translations[banner.source_locale] })
          setTranslations(banner.translations)
          setHasTranslations(true)
          setIsActive(banner.is_active)
          setRevision(banner.revision)
          setUpdatedAt(banner.updated_at)
        }
      } catch {
        setBannerError(t('dashboardBanner.loadError'))
      } finally {
        setBannerLoading(false)
      }
    }

    loadBanner()
    // The admin state is loaded once; subsequent edits remain local until Save.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function toggleMaintenance() {
    setMaintenanceLoading(true)
    setMaintenanceError('')
    try {
      const nextMode = !maintenanceMode
      const res = await apiFetch('/api/admin/maintenance', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ maintenance_mode: nextMode }),
      })
      if (res.ok) {
        const data = await res.json()
        useConfigStore.setState({ maintenanceMode: data.maintenance_mode })
      } else {
        setMaintenanceError(t('maintenanceError'))
      }
    } catch {
      setMaintenanceError(t('maintenanceError'))
    } finally {
      setMaintenanceLoading(false)
    }
  }

  async function translateBanner() {
    setTranslating(true)
    setBannerError('')
    setBannerSuccess('')
    try {
      const response = await apiFetch('/api/admin/dashboard-banner/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source_locale: sourceLocale, ...source }),
      })
      if (!response.ok) throw new Error('translate failed')
      const data: { translations: BannerTranslations } = await response.json()
      setTranslations(data.translations)
      setHasTranslations(true)
      setEditorLocale(sourceLocale)
      setBannerSuccess(t('dashboardBanner.translateSuccess'))
    } catch {
      setBannerError(t('dashboardBanner.translateError'))
    } finally {
      setTranslating(false)
    }
  }

  async function saveBanner() {
    setSaving(true)
    setBannerError('')
    setBannerSuccess('')
    try {
      const response = await apiFetch('/api/admin/dashboard-banner', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          source_locale: sourceLocale,
          is_active: isActive,
          translations,
        }),
      })
      if (!response.ok) throw new Error('save failed')
      const saved: AdminDashboardBanner = await response.json()
      setRevision(saved.revision)
      setUpdatedAt(saved.updated_at)
      setTranslations(saved.translations)
      setIsActive(saved.is_active)
      useConfigStore.setState({
        dashboardBanner: saved.is_active
          ? { revision: saved.revision, translations: saved.translations }
          : null,
      })
      setBannerSuccess(t('dashboardBanner.saveSuccess'))
    } catch {
      setBannerError(t('dashboardBanner.saveError'))
    } finally {
      setSaving(false)
    }
  }

  function updateTranslation(
    field: keyof DashboardBannerTranslation,
    value: string
  ) {
    setTranslations((current) => ({
      ...current,
      [editorLocale]: { ...current[editorLocale], [field]: value },
    }))
  }

  const editorTranslation = translations[editorLocale]
  const completedLocales = BANNER_LOCALES.filter((locale) =>
    Object.values(translations[locale]).every((value) => value.trim())
  ).length
  const sourceComplete = Object.values(source).every((value) => value.trim())

  return (
    <div className="juba-admin-system-shell mx-auto max-w-6xl space-y-4 p-4 sm:p-6">
      <AdminPageHeader
        eyebrow={`${t('title')} / ${t('system')}`}
        title={t('system')}
      />

      <AdminNav />

      {maintenanceError && (
        <div className="border-red-200/60 text-[var(--juba-app-error)] border px-4 py-3 font-sans text-xs border-[var(--juba-app-line)]">
          {maintenanceError}
        </div>
      )}

      <div
        className={`juba-card border px-5 py-4 ${maintenanceMode ? 'border-yellow-500/40 bg-yellow-500/5' : 'border-[var(--juba-app-line)] bg-[var(--juba-app-surface)]'}`}
      >
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex gap-3">
            <ShieldAlert
              className={`mt-0.5 size-5 shrink-0 ${maintenanceMode ? 'text-yellow-500' : 'text-[var(--juba-app-muted)]'}`}
              aria-hidden="true"
            />
            <div>
              <div className="mb-1 flex flex-wrap items-center gap-2">
                <span className="text-[var(--juba-app-muted)] font-sans text-xs tracking-wide">
                  {t('maintenanceTitle')}
                </span>
                <span
                  className={`text-[var(--juba-app-muted)] border px-2 py-0.5 font-semibold tracking-wide ${
                    maintenanceMode
                      ? 'border-yellow-500/40 text-yellow-500'
                      : 'border-[var(--juba-app-line)] text-[var(--juba-app-muted)]'
                  }`}
                >
                  {maintenanceMode ? t('maintenanceOn') : t('maintenanceOff')}
                </span>
              </div>
              <p className="text-[var(--juba-app-muted)] font-sans">
                {t('maintenanceDesc')}
              </p>
            </div>
          </div>
          <button
            onClick={toggleMaintenance}
            disabled={maintenanceLoading}
            className={`inline-flex shrink-0 items-center justify-center gap-2 px-4 py-3 font-sans text-xs font-bold tracking-wide transition-colors ${
              maintenanceMode
                ? 'bg-[var(--juba-app-ink)] text-white hover:opacity-90'
                : 'bg-[var(--juba-app-green)] text-white hover:bg-[var(--juba-app-green)]/90'
            } disabled:opacity-50`}
          >
            {maintenanceLoading && (
              <Loader2 className="size-3.5 animate-spin" aria-hidden="true" />
            )}
            {maintenanceMode ? t('maintenanceDisable') : t('maintenanceEnable')}
          </button>
        </div>
      </div>

      <section className="juba-card border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] border p-5">
        <div className="border-[var(--juba-app-line)] mb-5 flex gap-3 border-b pb-4">
          <Megaphone
            className="text-[var(--juba-app-green)] mt-0.5 size-5 shrink-0"
            aria-hidden="true"
          />
          <div>
            <h2 className="text-[var(--juba-app-ink)] font-sans text-sm font-bold tracking-wide">
              {t('dashboardBanner.title')}
            </h2>
            <p className="text-[var(--juba-app-muted)] mt-1 font-sans text-xs">
              {t('dashboardBanner.description')}
            </p>
          </div>
        </div>

        {bannerLoading ? (
          <div className="text-[var(--juba-app-muted)] flex items-center gap-2 font-sans text-xs">
            <Loader2 className="size-4 animate-spin" aria-hidden="true" />
            {t('dashboardBanner.loading')}
          </div>
        ) : (
          <div className="space-y-6">
            {bannerError && (
              <p
                role="alert"
                className="border-red-200/60 text-[var(--juba-app-error)] border px-4 py-3 font-sans text-xs border-[var(--juba-app-line)]"
              >
                {bannerError}
              </p>
            )}
            {bannerSuccess && (
              <p className="border-[var(--juba-app-green)]/30 text-[var(--juba-app-green)] border px-4 py-3 font-sans text-xs border-[var(--juba-app-line)]">
                {bannerSuccess}
              </p>
            )}

            <div className="grid gap-4 md:grid-cols-[12rem_1fr]">
              <label className="space-y-2 font-sans text-xs">
                <span className="text-[var(--juba-app-muted)] block tracking-wide">
                  {t('dashboardBanner.sourceLocale')}
                </span>
                <select
                  value={sourceLocale}
                  onChange={(event) =>
                    setSourceLocale(event.target.value as BannerLocale)
                  }
                  className="border-[var(--juba-app-line)] bg-[var(--juba-app-bg)] text-[var(--juba-app-ink)] w-full border px-3 py-2"
                >
                  {BANNER_LOCALES.map((locale) => (
                    <option key={locale} value={locale}>
                      {t(`dashboardBanner.locales.${locale}`)}
                    </option>
                  ))}
                </select>
              </label>
              <label className="flex items-end gap-3 pb-2 font-sans text-xs">
                <input
                  type="checkbox"
                  checked={isActive}
                  onChange={(event) => setIsActive(event.target.checked)}
                  className="accent-[var(--juba-app-green)] size-4"
                />
                <span>
                  <span className="text-[var(--juba-app-ink)] block font-bold">
                    {t('dashboardBanner.activeLabel')}
                  </span>
                  <span className="text-[var(--juba-app-muted)] mt-1 block">
                    {t('dashboardBanner.activeHint')}
                  </span>
                </span>
              </label>
            </div>

            <div className="grid gap-4">
              <label className="space-y-2 font-sans text-xs">
                <span className="text-[var(--juba-app-muted)] block tracking-wide">
                  {t('dashboardBanner.fieldTitle')}
                </span>
                <input
                  value={source.title}
                  onChange={(event) =>
                    setSource((current) => ({
                      ...current,
                      title: event.target.value,
                    }))
                  }
                  maxLength={160}
                  className="border-[var(--juba-app-line)] bg-[var(--juba-app-bg)] text-[var(--juba-app-ink)] w-full border px-3 py-2 font-sans text-sm"
                />
              </label>
              <label className="space-y-2 font-sans text-xs">
                <span className="text-[var(--juba-app-muted)] block tracking-wide">
                  {t('dashboardBanner.fieldSubtitle')}
                </span>
                <input
                  value={source.subtitle}
                  onChange={(event) =>
                    setSource((current) => ({
                      ...current,
                      subtitle: event.target.value,
                    }))
                  }
                  maxLength={240}
                  className="border-[var(--juba-app-line)] bg-[var(--juba-app-bg)] text-[var(--juba-app-ink)] w-full border px-3 py-2 font-sans text-sm"
                />
              </label>
              <label className="space-y-2 font-sans text-xs">
                <span className="text-[var(--juba-app-muted)] block tracking-wide">
                  {t('dashboardBanner.fieldDescription')}
                </span>
                <textarea
                  value={source.description}
                  onChange={(event) =>
                    setSource((current) => ({
                      ...current,
                      description: event.target.value,
                    }))
                  }
                  maxLength={2000}
                  rows={5}
                  className="border-[var(--juba-app-line)] bg-[var(--juba-app-bg)] text-[var(--juba-app-ink)] w-full resize-y border px-3 py-2 font-sans text-sm"
                />
              </label>
              <div>
                <button
                  type="button"
                  onClick={translateBanner}
                  disabled={translating || !sourceComplete}
                  className="bg-fl-fg text-fl-bg hover:bg-[var(--juba-app-green)] inline-flex items-center gap-2 px-4 py-3 font-sans text-xs font-bold tracking-wide transition-colors disabled:opacity-40"
                >
                  {translating && (
                    <Loader2
                      className="size-3.5 animate-spin"
                      aria-hidden="true"
                    />
                  )}
                  {t('dashboardBanner.translate')}
                </button>
              </div>
            </div>

            {hasTranslations && (
              <div className="border-[var(--juba-app-line)] space-y-4 border-t pt-5">
                <div className="flex flex-wrap items-end justify-between gap-3">
                  <label className="space-y-2 font-sans text-xs">
                    <span className="text-[var(--juba-app-muted)] block tracking-wide">
                      {t('dashboardBanner.editTranslation')}
                    </span>
                    <select
                      value={editorLocale}
                      onChange={(event) =>
                        setEditorLocale(event.target.value as BannerLocale)
                      }
                      className="border-[var(--juba-app-line)] bg-[var(--juba-app-bg)] text-[var(--juba-app-ink)] min-w-52 border px-3 py-2"
                    >
                      {BANNER_LOCALES.map((locale) => {
                        const complete = Object.values(
                          translations[locale]
                        ).every((value) => value.trim())
                        return (
                          <option key={locale} value={locale}>
                            {complete ? '✓ ' : ''}
                            {t(`dashboardBanner.locales.${locale}`)}
                          </option>
                        )
                      })}
                    </select>
                  </label>
                  <p className="text-[var(--juba-app-muted)] font-sans text-xs">
                    {t('dashboardBanner.completion', {
                      complete: completedLocales,
                      total: BANNER_LOCALES.length,
                    })}
                  </p>
                </div>

                <div className="grid gap-4">
                  <label className="space-y-2 font-sans text-xs">
                    <span className="text-[var(--juba-app-muted)] block tracking-wide">
                      {t('dashboardBanner.fieldTitle')}
                    </span>
                    <input
                      value={editorTranslation.title}
                      onChange={(event) =>
                        updateTranslation('title', event.target.value)
                      }
                      maxLength={160}
                      className="border-[var(--juba-app-line)] bg-[var(--juba-app-bg)] text-[var(--juba-app-ink)] w-full border px-3 py-2 font-sans text-sm"
                    />
                  </label>
                  <label className="space-y-2 font-sans text-xs">
                    <span className="text-[var(--juba-app-muted)] block tracking-wide">
                      {t('dashboardBanner.fieldSubtitle')}
                    </span>
                    <input
                      value={editorTranslation.subtitle}
                      onChange={(event) =>
                        updateTranslation('subtitle', event.target.value)
                      }
                      maxLength={240}
                      className="border-[var(--juba-app-line)] bg-[var(--juba-app-bg)] text-[var(--juba-app-ink)] w-full border px-3 py-2 font-sans text-sm"
                    />
                  </label>
                  <label className="space-y-2 font-sans text-xs">
                    <span className="text-[var(--juba-app-muted)] block tracking-wide">
                      {t('dashboardBanner.fieldDescription')}
                    </span>
                    <textarea
                      value={editorTranslation.description}
                      onChange={(event) =>
                        updateTranslation('description', event.target.value)
                      }
                      maxLength={2000}
                      rows={5}
                      className="border-[var(--juba-app-line)] bg-[var(--juba-app-bg)] text-[var(--juba-app-ink)] w-full resize-y border px-3 py-2 font-sans text-sm"
                    />
                  </label>
                </div>

                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div className="text-[var(--juba-app-muted)] font-sans text-xs">
                    {revision !== null && (
                      <span className="mr-4">
                        {t('dashboardBanner.revision', { revision })}
                      </span>
                    )}
                    {updatedAt && (
                      <span>
                        {t('dashboardBanner.updated', {
                          date: new Intl.DateTimeFormat(currentLocale, {
                            dateStyle: 'medium',
                            timeStyle: 'short',
                          }).format(new Date(updatedAt)),
                        })}
                      </span>
                    )}
                  </div>
                  <button
                    type="button"
                    onClick={saveBanner}
                    disabled={
                      saving || completedLocales !== BANNER_LOCALES.length
                    }
                    className="bg-[var(--juba-app-green)] text-white hover:bg-[var(--juba-app-green)]/90 inline-flex items-center justify-center gap-2 px-5 py-3 font-sans text-xs font-bold tracking-wide transition-colors disabled:opacity-40"
                  >
                    {saving && (
                      <Loader2
                        className="size-3.5 animate-spin"
                        aria-hidden="true"
                      />
                    )}
                    {t('dashboardBanner.save')}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  )
}
