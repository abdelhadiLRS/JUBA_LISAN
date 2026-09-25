'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Check, ChevronDown, Globe2, Menu, X, Sparkles } from 'lucide-react'
import { hasActiveLandingSubscription } from '@/lib/landing-subscription'
import type { Locale } from '@/lib/locales'

interface LandingNavProps {
  hasSession: boolean
  stripeEnabled: boolean
  dir: 'ltr' | 'rtl'
  navFeatures: string
  navDemo: string
  navLanguages: string
  navReviews: string
  navPricing: string
  navFAQ: string
  showReviews: boolean
  signIn: string
  dashboard: string
  getStarted: string
  homeLabel: string
  brandTagline: string
  openMenuLabel: string
  closeMenuLabel: string
  locale: Locale
}

const LOCALES_DATA: Record<Locale, { name: string; native: string }> = {
  en: { name: 'English', native: 'English' },
  ar: { name: 'Arabic', native: 'العربية' },
  es: { name: 'Spanish', native: 'Español' },
  fr: { name: 'French', native: 'Français' },
  pt: { name: 'Portuguese', native: 'Português' },
  de: { name: 'German', native: 'Deutsch' },
  it: { name: 'Italian', native: 'Italiano' },
  pl: { name: 'Polish', native: 'Polski' },
  nl: { name: 'Dutch', native: 'Nederlands' },
  ro: { name: 'Romanian', native: 'Română' },
  ru: { name: 'Russian', native: 'Русский' },
}

export function LandingNav({
  hasSession,
  stripeEnabled,
  dir,
  navFeatures,
  navDemo,
  navLanguages,
  navReviews,
  navPricing,
  navFAQ,
  showReviews,
  signIn,
  dashboard,
  getStarted,
  homeLabel,
  brandTagline,
  openMenuLabel,
  closeMenuLabel,
  locale,
}: LandingNavProps) {
  const [open, setOpen] = useState(false)
  const [regionOpen, setRegionOpen] = useState(false)
  const [showPricing, setShowPricing] = useState(true)
  const [visitorCountry, setVisitorCountry] = useState<string>('DZ')

  const countryLabels: Record<string, { name: string }> = {
    DZ: { name: 'Algeria' },
    EG: { name: 'Egypt' },
    SA: { name: 'Saudi Arabia' },
    AE: { name: 'United Arab Emirates' },
    US: { name: 'United States' },
    FR: { name: 'France' },
    DE: { name: 'Germany' },
    ES: { name: 'Spain' },
    IT: { name: 'Italy' },
    GB: { name: 'United Kingdom' },
  }

  useEffect(() => {
    try {
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone
      const timezoneCountries: Record<string, string> = {
        'Africa/Algiers': 'DZ', 'Africa/Cairo': 'EG', 'Africa/Casablanca': 'MA', 'Africa/Tunis': 'TN',
        'Europe/London': 'GB', 'Europe/Paris': 'FR', 'Europe/Madrid': 'ES', 'Europe/Rome': 'IT',
        'Europe/Berlin': 'DE', 'Asia/Dubai': 'AE', 'Asia/Riyadh': 'SA', 'America/New_York': 'US',
      }
      setVisitorCountry(timezoneCountries[timezone] ?? 'DZ')
    } catch {
      setVisitorCountry('DZ')
    }
  }, [])

  const currentCountry = countryLabels[visitorCountry] ?? countryLabels.DZ
  const countryFlag = (code: string) =>
    code.toUpperCase().replace(/[A-Z]/g, (char) => String.fromCodePoint(char.charCodeAt(0) + 127397))
  const localeLinks = (Object.entries(LOCALES_DATA) as Array<[Locale, { name: string; native: string }]>).map(
    ([code, language]) => ({ code, ...language })
  )

  useEffect(() => {
    let canceled = false
    if (!stripeEnabled) {
      setShowPricing(false)
      return
    }
    if (!hasSession) {
      setShowPricing(true)
      return
    }
    setShowPricing(false)
    async function checkSubscription() {
      const subscribed = await hasActiveLandingSubscription()
      if (!canceled) setShowPricing(!subscribed)
    }
    checkSubscription()
    return () => {
      canceled = true
    }
  }, [hasSession, stripeEnabled])

  const closeMenu = () => setOpen(false)

  const links = (
    <>
      <a href="#features" onClick={closeMenu} className="text-sm font-black text-[var(--juba-app-ink)] hover:text-[var(--juba-app-green)] transition-colors">
        {navFeatures}
      </a>
      <a href="#demo" onClick={closeMenu} className="text-sm font-black text-[var(--juba-app-ink)] hover:text-[var(--juba-app-green)] transition-colors">
        {navDemo}
      </a>
      <a href="#languages" onClick={closeMenu} className="text-sm font-black text-[var(--juba-app-ink)] hover:text-[var(--juba-app-green)] transition-colors">
        {navLanguages}
      </a>
      {showReviews && (
        <a href="#reviews" onClick={closeMenu} className="text-sm font-black text-[var(--juba-app-ink)] hover:text-[var(--juba-app-green)] transition-colors">
          {navReviews}
        </a>
      )}
      {showPricing && (
        <a href="#pricing" onClick={closeMenu} className="text-sm font-black text-[var(--juba-app-ink)] hover:text-[var(--juba-app-green)] transition-colors">
          {navPricing}
        </a>
      )}
      <a href="#faq" onClick={closeMenu} className="text-sm font-black text-[var(--juba-app-ink)] hover:text-[var(--juba-app-green)] transition-colors">
        {navFAQ}
      </a>
    </>
  )

  return (
    <nav dir={dir} className="sticky top-0 z-50 w-full bg-[#fcfaf7]/90 backdrop-blur-md border-b border-[var(--juba-app-line)] transition-all">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-3 group" aria-label={homeLabel}>
          <span className="relative flex h-11 w-11 items-center justify-center rounded-2xl bg-[var(--juba-app-green)] text-white font-black text-xl shadow-[3px_3px_0_var(--juba-app-ink)] group-hover:translate-x-0.5 group-hover:translate-y-0.5 transition-transform">
            J
            <span className="absolute -top-1 -right-1 text-xs text-[var(--juba-app-yellow)]">✦</span>
          </span>
          <span className="flex flex-col">
            <span className="font-sans text-xl font-black tracking-tight text-[var(--juba-app-ink)]">
              JUBA <span className="text-[var(--juba-app-green)]">LISAN</span>
            </span>
            <small className="text-[10px] font-bold text-[var(--juba-app-muted)] -mt-1">{brandTagline}</small>
          </span>
        </Link>

        {/* Desktop Nav Links */}
        <div className="hidden items-center gap-8 md:flex">{links}</div>

        {/* Desktop Right Controls */}
        <div className="hidden items-center gap-4 md:flex">
          {/* Region / Language Selector Dropdown */}
          <div className="relative">
            <button
              type="button"
              onClick={() => setRegionOpen((value) => !value)}
              aria-expanded={regionOpen}
              aria-haspopup="menu"
              aria-label={dir === 'rtl' ? 'تغيير المنطقة أو اللغة' : 'Change region or language'}
              className="flex items-center gap-2 rounded-2xl border-2 border-[var(--juba-app-ink)] bg-white px-3.5 py-2 text-xs font-black text-[var(--juba-app-ink)] shadow-[2px_2px_0_var(--juba-app-ink)] hover:bg-[#f5f8f1] transition-all"
            >
              <span className="text-base">{countryFlag(visitorCountry)}</span>
              <span className="rounded-md bg-[var(--juba-app-green-soft)] px-1.5 py-0.5 text-[10px] font-black">{visitorCountry}</span>
              <span className="text-xs font-black uppercase">{locale}</span>
              <ChevronDown className="h-4 w-4" />
            </button>

            {regionOpen && (
              <div role="menu" className="absolute end-0 top-[calc(100%+8px)] z-50 w-72 rounded-2xl border-2 border-[var(--juba-app-ink)] bg-white p-4 shadow-[6px_6px_0_var(--juba-app-ink)] animate-in fade-in zoom-in-95 duration-150">
                <div className="mb-2 flex items-center gap-2 text-[10px] font-black uppercase tracking-wider text-[var(--juba-app-green)]">
                  <Globe2 className="h-4 w-4" /> Region & Language
                </div>
                <div className="rounded-xl border border-[var(--juba-app-line)] bg-[#f5f8f1] p-3">
                  <div className="text-[10px] font-bold text-[var(--juba-app-muted)]">Visitor Region</div>
                  <div className="mt-1 flex items-center gap-2 font-black text-[var(--juba-app-ink)] text-xs">
                    <span className="text-base">{countryFlag(visitorCountry)}</span>
                    <span className="rounded bg-white px-1.5 py-0.5 text-[10px] border border-[var(--juba-app-line)]">{visitorCountry}</span>
                    <span>{currentCountry.name}</span>
                  </div>
                </div>

                <div className="mt-3 border-t border-[var(--juba-app-line)] pt-3">
                  <div className="text-[10px] font-bold text-[var(--juba-app-muted)] mb-2">Interface Language</div>
                  <div className="grid max-h-56 grid-cols-2 gap-1.5 overflow-auto">
                    {localeLinks.map((language) => (
                      <Link
                        key={language.code}
                        href={`/${language.code}`}
                        onClick={() => setRegionOpen(false)}
                        className={`flex items-center justify-between rounded-xl px-3 py-2 text-xs font-black transition ${
                          locale === language.code
                            ? 'border border-[var(--juba-app-ink)] bg-[var(--juba-app-green-soft)] text-[var(--juba-app-ink)]'
                            : 'text-[var(--juba-app-muted)] hover:bg-[#f5f8f1] hover:text-[var(--juba-app-ink)]'
                        }`}
                      >
                        <span>{language.native}</span>
                        {locale === language.code && <Check className="h-3.5 w-3.5 text-[var(--juba-app-green)]" />}
                      </Link>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          <Link href={hasSession ? '/dashboard' : '/login'} className="text-sm font-black text-[var(--juba-app-ink)] hover:text-[var(--juba-app-green)] transition-colors">
            {hasSession ? dashboard : signIn}
          </Link>

          <Link
            href={hasSession ? '/dashboard' : '/register'}
            className="flex items-center gap-2 rounded-2xl border-2 border-[var(--juba-app-ink)] bg-[var(--juba-app-green)] px-5 py-2.5 text-sm font-black text-white shadow-[3px_3px_0_var(--juba-app-ink)] hover:bg-[#236328] hover:translate-x-0.5 hover:translate-y-0.5 active:translate-x-1 active:translate-y-1 transition-all"
          >
            <span>{hasSession ? dashboard : getStarted}</span>
            <Sparkles className="h-4 w-4 text-[var(--juba-app-yellow)]" />
          </Link>
        </div>

        {/* Mobile Hamburger Button */}
        <button
          type="button"
          onClick={() => setOpen((value) => !value)}
          className="flex h-11 w-11 items-center justify-center rounded-2xl border-2 border-[var(--juba-app-ink)] bg-white shadow-[2px_2px_0_var(--juba-app-ink)] md:hidden"
          aria-label={open ? closeMenuLabel : openMenuLabel}
          aria-expanded={open}
          aria-controls="juba-mobile-navigation"
        >
          {open ? <X className="h-6 w-6 text-[var(--juba-app-ink)]" /> : <Menu className="h-6 w-6 text-[var(--juba-app-ink)]" />}
        </button>
      </div>

      {/* Mobile Full-width Sheet Navigation */}
      {open && (
        <div
          id="juba-mobile-navigation"
          className="fixed inset-x-0 top-20 bottom-0 z-50 overflow-y-auto bg-[#fcfaf7] p-6 shadow-2xl border-t-2 border-[var(--juba-app-ink)] md:hidden animate-in slide-in-from-top-4 duration-200"
        >
          <div className="flex flex-col gap-6">
            {/* Nav links */}
            <div className="flex flex-col gap-4 text-lg font-black text-[var(--juba-app-ink)] border-b border-[var(--juba-app-line)] pb-6">
              {links}
            </div>

            {/* Region / Language selection */}
            <div className="rounded-2xl border-2 border-[var(--juba-app-ink)] bg-white p-4 shadow-[4px_4px_0_var(--juba-app-ink)]">
              <div className="flex items-center justify-between text-xs font-black uppercase text-[var(--juba-app-green)] mb-3">
                <span className="flex items-center gap-1.5"><Globe2 className="h-4 w-4" /> Region & Language</span>
                <span className="rounded bg-[var(--juba-app-green-soft)] px-2 py-0.5 text-[10px] font-black border border-[var(--juba-app-line)]">{visitorCountry}</span>
              </div>
              <div className="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto">
                {localeLinks.map((language) => (
                  <Link
                    key={language.code}
                    href={`/${language.code}`}
                    onClick={closeMenu}
                    className={`rounded-xl px-3 py-2 text-xs font-black text-center border transition ${
                      locale === language.code
                        ? 'border-[var(--juba-app-ink)] bg-[var(--juba-app-green-soft)] text-[var(--juba-app-ink)]'
                        : 'border-[var(--juba-app-line)] text-[var(--juba-app-muted)] hover:border-[var(--juba-app-ink)]'
                    }`}
                  >
                    {language.native}
                  </Link>
                ))}
              </div>
            </div>

            {/* Mobile Actions */}
            <div className="flex flex-col gap-3 pt-2">
              <Link
                href={hasSession ? '/dashboard' : '/login'}
                onClick={closeMenu}
                className="flex h-12 w-full items-center justify-center rounded-2xl border-2 border-[var(--juba-app-ink)] bg-white text-base font-black text-[var(--juba-app-ink)] shadow-[3px_3px_0_var(--juba-app-ink)]"
              >
                {hasSession ? dashboard : signIn}
              </Link>
              <Link
                href={hasSession ? '/dashboard' : '/register'}
                onClick={closeMenu}
                className="flex h-12 w-full items-center justify-center gap-2 rounded-2xl border-2 border-[var(--juba-app-ink)] bg-[var(--juba-app-green)] text-base font-black text-white shadow-[3px_3px_0_var(--juba-app-ink)]"
              >
                <span>{hasSession ? dashboard : getStarted}</span>
                <Sparkles className="h-5 w-5 text-[var(--juba-app-yellow)]" />
              </Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
