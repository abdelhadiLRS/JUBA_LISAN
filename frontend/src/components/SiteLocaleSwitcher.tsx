'use client'

import { useMemo, useState } from 'react'
import { usePathname } from 'next/navigation'
import { Check, ChevronDown, Languages } from 'lucide-react'
import type { Locale } from '@/lib/locales'

const LOCALES: Array<{ code: Locale; label: string; native: string }> = [
  { code: 'en', label: 'English', native: 'English' },
  { code: 'ar', label: 'Arabic', native: 'العربية' },
  { code: 'es', label: 'Spanish', native: 'Español' },
  { code: 'fr', label: 'French', native: 'Français' },
  { code: 'pt', label: 'Portuguese', native: 'Português' },
  { code: 'de', label: 'German', native: 'Deutsch' },
  { code: 'it', label: 'Italian', native: 'Italiano' },
  { code: 'pl', label: 'Polish', native: 'Polski' },
  { code: 'nl', label: 'Dutch', native: 'Nederlands' },
  { code: 'ro', label: 'Romanian', native: 'Română' },
  { code: 'ru', label: 'Russian', native: 'Русский' },
]

export function SiteLocaleSwitcher({ locale }: { locale: Locale }) {
  const [open, setOpen] = useState(false)
  const pathname = usePathname()

  // Landing has its own full region/language control in the header.
  // This global control covers auth, legal, onboarding and the app shell.
  const isLandingRoute = useMemo(() => {
    const segments = pathname.split('/').filter(Boolean)
    return (
      segments.length === 0 ||
      (segments.length === 1 && LOCALES.some((item) => item.code === segments[0]))
    )
  }, [pathname])

  function selectLocale(next: Locale) {
    if (next === locale) {
      setOpen(false)
      return
    }

    const segments = pathname.split('/').filter(Boolean)
    const hasLocalePrefix =
      segments.length > 0 && LOCALES.some((item) => item.code === segments[0])
    const cleanPath = hasLocalePrefix
      ? `/${segments.slice(1).join('/')}`
      : pathname

    const nextPath = `/${next}${cleanPath === '/' ? '' : cleanPath}`
    window.location.assign(nextPath)
  }

  if (isLandingRoute) return null

  const current = LOCALES.find((item) => item.code === locale) ?? LOCALES[0]

  return (
    <div className="fixed bottom-4 left-4 z-[90]" dir="ltr">
      <div className="relative">
        <button
          type="button"
          onClick={() => setOpen((value) => !value)}
          aria-expanded={open}
          aria-haspopup="listbox"
          className="flex items-center gap-2 rounded-full border border-[var(--juba-app-line)] bg-white/95 px-3 py-2 text-xs font-bold text-[var(--juba-app-ink)] shadow-sm backdrop-blur transition hover:-translate-y-0.5 hover:shadow-md"
        >
          <Languages className="h-4 w-4 text-[var(--juba-app-green)]" aria-hidden="true" />
          <span>{current.native}</span>
          <ChevronDown className="h-3.5 w-3.5" aria-hidden="true" />
        </button>

        {open && (
          <div
            role="listbox"
            aria-label={locale === 'ar' ? 'لغة الموقع' : 'Site language'}
            className="absolute bottom-[calc(100%+8px)] left-0 w-52 overflow-hidden rounded-2xl border border-[var(--juba-app-line)] bg-white p-1.5 shadow-lg"
          >
            {LOCALES.map((item) => (
              <button
                key={item.code}
                type="button"
                role="option"
                aria-selected={item.code === locale}
                onClick={() => selectLocale(item.code)}
                className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm transition hover:bg-[var(--juba-app-green-soft)]"
              >
                <span className="min-w-0 flex-1">
                  <span className="block font-bold text-[var(--juba-app-ink)]">{item.native}</span>
                  <span className="block text-[10px] text-[var(--juba-app-muted)]">{item.label}</span>
                </span>
                {item.code === locale && <Check className="h-4 w-4 text-[var(--juba-app-green)]" aria-hidden="true" />}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
