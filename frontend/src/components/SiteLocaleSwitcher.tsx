'use client'

import { useMemo, useState } from 'react'
import { usePathname } from 'next/navigation'
import { Check, ChevronDown, Globe2 } from 'lucide-react'
import type { Locale } from '@/lib/locales'

const LOCALES: Array<{ code: Locale; label: string; native: string; country: string }> = [
  { code: 'en', label: 'English', native: 'English', country: 'gb' },
  { code: 'ar', label: 'Arabic', native: 'العربية', country: 'dz' },
  { code: 'es', label: 'Spanish', native: 'Español', country: 'es' },
  { code: 'fr', label: 'French', native: 'Français', country: 'fr' },
  { code: 'pt', label: 'Portuguese', native: 'Português', country: 'pt' },
  { code: 'de', label: 'German', native: 'Deutsch', country: 'de' },
  { code: 'it', label: 'Italian', native: 'Italiano', country: 'it' },
  { code: 'pl', label: 'Polish', native: 'Polski', country: 'pl' },
  { code: 'nl', label: 'Dutch', native: 'Nederlands', country: 'nl' },
  { code: 'ro', label: 'Romanian', native: 'Română', country: 'ro' },
  { code: 'ru', label: 'Russian', native: 'Русский', country: 'ru' },
]

function getVisitorCountry(): string {
  try {
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone
    const timezoneCountries: Record<string, string> = {
      'Africa/Algiers': 'DZ', 'Africa/Casablanca': 'MA', 'Africa/Tunis': 'TN',
      'Africa/Cairo': 'EG', 'Africa/Tripoli': 'LY', 'Africa/Lagos': 'NG',
      'Africa/Johannesburg': 'ZA', 'Africa/Nairobi': 'KE', 'Europe/Paris': 'FR',
      'Europe/London': 'GB', 'Europe/Dublin': 'IE', 'Europe/Madrid': 'ES',
      'Europe/Lisbon': 'PT', 'Europe/Berlin': 'DE', 'Europe/Rome': 'IT',
      'Europe/Amsterdam': 'NL', 'Europe/Brussels': 'BE', 'Europe/Zurich': 'CH',
      'Europe/Warsaw': 'PL', 'Europe/Bucharest': 'RO', 'Europe/Moscow': 'RU',
      'Europe/Kyiv': 'UA', 'Asia/Dubai': 'AE', 'Asia/Riyadh': 'SA',
      'Asia/Tokyo': 'JP', 'Asia/Seoul': 'KR', 'Asia/Shanghai': 'CN',
      'Australia/Sydney': 'AU', 'Pacific/Auckland': 'NZ',
      'America/New_York': 'US', 'America/Chicago': 'US',
      'America/Denver': 'US', 'America/Los_Angeles': 'US',
      'America/Toronto': 'CA', 'America/Vancouver': 'CA',
    }
    return timezoneCountries[timezone] ?? 'DZ'
  } catch {
    return 'DZ'
  }
}

function countryFlag(countryCode: string): string {
  return countryCode.toUpperCase().replace(/[A-Z]/g, (char) =>
    String.fromCodePoint(char.charCodeAt(0) + 127397),
  )
}

export function SiteLocaleSwitcher({ locale }: { locale: Locale }) {
  const [open, setOpen] = useState(false)
  const pathname = usePathname()
  const country = useMemo(() => getVisitorCountry(), [])

  const isLandingRoute = useMemo(() => {
    const segments = pathname.split('/').filter(Boolean)
    return segments.length === 0 ||
      (segments.length === 1 && LOCALES.some((item) => item.code === segments[0]))
  }, [pathname])

  function selectLocale(next: Locale) {
    setOpen(false)
    if (next === locale) return

    const segments = pathname.split('/').filter(Boolean)
    const hasLocalePrefix = segments.length > 0 && LOCALES.some((item) => item.code === segments[0])
    const cleanPath = hasLocalePrefix ? `/${segments.slice(1).join('/')}` : pathname
    const nextPath = `/${next}${cleanPath === '/' ? '' : cleanPath}`
    window.location.assign(nextPath)
  }

  if (isLandingRoute) return null

  const current = LOCALES.find((item) => item.code === locale) ?? LOCALES[0]

  return (
    <div className="fixed right-4 top-4 z-[90]" dir="ltr">
      <div className="relative">
        <button
          type="button"
          onClick={() => setOpen((value) => !value)}
          aria-expanded={open}
          aria-haspopup="listbox"
          aria-label={locale === 'ar' ? 'تغيير المنطقة ولغة الموقع' : 'Change region and site language'}
          className="flex items-center gap-2 rounded-full border border-[var(--juba-app-line)] bg-white/90 px-3 py-2 text-xs font-bold text-[var(--juba-app-ink)] shadow-sm backdrop-blur transition hover:-translate-y-0.5 hover:shadow-md"
        >
          <span className="text-base" aria-hidden="true">{countryFlag(country)}</span>
          <span className="rounded-md border border-[var(--juba-app-line)] px-2 py-1 text-[10px] font-black">{country}</span>
          <span className="text-xs font-black uppercase">{locale}</span>
          <ChevronDown className="h-3 w-3" aria-hidden="true" />
        </button>

        {open && (
          <div role="listbox" aria-label={locale === 'ar' ? 'لغة الموقع' : 'Site language'} className="absolute right-0 top-[calc(100%+8px)] w-64 overflow-hidden rounded-2xl border border-[var(--juba-app-line)] bg-white p-3 shadow-xl">
            <div className="mb-3 flex items-center gap-2 text-[10px] font-black uppercase tracking-[.14em] text-[var(--juba-app-muted)]">
              <Globe2 className="h-3.5 w-3.5" aria-hidden="true" />
              {locale === 'ar' ? 'المنطقة واللغة' : 'Region & language'}
            </div>
            <div className="mb-3 rounded-xl bg-[var(--juba-app-green-soft)] px-3 py-2.5">
              <div className="text-[10px] font-bold text-[var(--juba-app-muted)]">{locale === 'ar' ? 'منطقتك' : 'Visitor region'}</div>
              <div className="mt-1 flex items-center gap-2 font-black text-[var(--juba-app-ink)]">
                <span className="text-lg" aria-hidden="true">{countryFlag(country)}</span>
                <span>{country}</span>
              </div>
            </div>
            <div className="border-t border-[var(--juba-app-line)] pt-3">
              <div className="px-2 text-[10px] font-bold text-[var(--juba-app-muted)]">{locale === 'ar' ? 'لغة الواجهة' : 'Interface language'}</div>
              <div className="mt-1 grid max-h-64 grid-cols-2 gap-1 overflow-auto">
                {LOCALES.map((item) => (
                  <button key={item.code} type="button" role="option" aria-selected={item.code === locale} onClick={() => selectLocale(item.code)}
                    className={`flex items-center justify-between gap-2 rounded-xl px-3 py-2 text-xs font-bold transition ${locale === item.code ? 'bg-[var(--juba-app-green-soft)] text-[var(--juba-app-ink)]' : 'text-[var(--juba-app-muted)] hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-ink)]'}`}>
                    <span className="flex min-w-0 items-center gap-2"><span className="text-base leading-none" aria-hidden="true">{countryFlag(item.country.toUpperCase())}</span><span className="truncate">{item.native}</span></span>
                    {item.code === locale && <Check className="h-3.5 w-3.5 text-[var(--juba-app-green)]" aria-hidden="true" />}
                  </button>
                ))}
              </div>
            </div>
            <p className="mt-3 px-2 text-[10px] leading-4 text-[var(--juba-app-muted)]">{locale === 'ar' ? 'يتم تقدير المنطقة من المنطقة الزمنية للمتصفح، وتُستخدم DZ كقيمة افتراضية.' : 'Region is estimated from your browser time zone; DZ is the default.'}</p>
          </div>
        )}
      </div>
    </div>
  )
}
