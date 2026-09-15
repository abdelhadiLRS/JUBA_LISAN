import { create } from 'zustand'

export interface DashboardBannerTranslation {
  title: string
  subtitle: string
  description: string
}

export interface DashboardBanner {
  revision: number
  translations: Record<string, DashboardBannerTranslation>
}

interface ConfigStore {
  stripeEnabled: boolean
  stripeTrialDays: number
  freemiumTrialEnabled: boolean
  ttsProvider: string
  openaiTtsVoice: string
  maintenanceMode: boolean
  priceMonthly: number
  priceYearly: number
  totalPriceMonthly: number
  totalPriceYearly: number
  dashboardBanner: DashboardBanner | null
  loaded: boolean
  load: () => Promise<void>
}

const CONFIG_REQUEST_TIMEOUT_MS = 8_000

function isBannerTranslation(value: unknown): value is DashboardBannerTranslation {
  if (!value || typeof value !== 'object') return false
  const candidate = value as Record<string, unknown>
  return (
    typeof candidate.title === 'string' &&
    typeof candidate.subtitle === 'string' &&
    typeof candidate.description === 'string'
  )
}

function parseDashboardBanner(value: unknown): DashboardBanner | null {
  if (!value || typeof value !== 'object') return null
  const candidate = value as Record<string, unknown>
  if (
    typeof candidate.revision !== 'number' ||
    !Number.isFinite(candidate.revision) ||
    !candidate.translations ||
    typeof candidate.translations !== 'object'
  ) {
    return null
  }

  const translations: Record<string, DashboardBannerTranslation> = {}
  for (const [locale, translation] of Object.entries(
    candidate.translations as Record<string, unknown>
  )) {
    if (isBannerTranslation(translation)) {
      translations[locale] = translation
    }
  }

  return Object.keys(translations).length > 0
    ? { revision: candidate.revision, translations }
    : null
}

export const useConfigStore = create<ConfigStore>((set, get) => ({
  stripeEnabled: false,
  stripeTrialDays: 7,
  freemiumTrialEnabled: true,
  ttsProvider: 'local',
  openaiTtsVoice: 'nova',
  maintenanceMode: false,
  priceMonthly: 0.0,
  priceYearly: 0.0,
  totalPriceMonthly: 0.0,
  totalPriceYearly: 0.0,
  dashboardBanner: null,
  loaded: false,
  load: async () => {
    if (get().loaded) return
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), CONFIG_REQUEST_TIMEOUT_MS)

    try {
      const res = await fetch('/api/config', {
        signal: controller.signal,
        cache: 'no-store',
      })
      if (!res.ok) {
        set({ loaded: true })
        return
      }
      const data = await res.json()
      set({
        stripeEnabled: data.stripe_enabled ?? false,
        stripeTrialDays: data.stripe_trial_days ?? 7,
        freemiumTrialEnabled: data.freemium_trial_enabled ?? true,
        ttsProvider: data.tts_provider ?? 'local',
        openaiTtsVoice: data.openai_tts_voice ?? 'nova',
        maintenanceMode: data.maintenance_mode ?? false,
        priceMonthly: data.price_monthly ?? 0.0,
        priceYearly: data.price_yearly ?? 0.0,
        totalPriceMonthly: data.total_price_monthly ?? 0.0,
        totalPriceYearly: data.total_price_yearly ?? 0.0,
        dashboardBanner: parseDashboardBanner(data.dashboard_banner),
        loaded: true,
      })
    } catch {
      // Non-fatal: keep defaults (stripe disabled)
      set({ loaded: true })
    } finally {
      clearTimeout(timeout)
    }
  },
}))
