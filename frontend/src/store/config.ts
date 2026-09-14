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
        dashboardBanner: data.dashboard_banner ?? null,
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
