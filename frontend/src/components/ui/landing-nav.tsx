'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Check, ChevronDown, Globe2, Menu, X } from 'lucide-react'
import type { Locale } from '@/lib/locales'
import { hasActiveLandingSubscription } from '@/lib/landing-subscription'

interface LandingNavProps {
  hasSession: boolean
  stripeEnabled: boolean
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

export function LandingNav({
  hasSession,
  stripeEnabled,
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
  const [showPricing, setShowPricing] = useState(stripeEnabled && !hasSession)
  const [regionOpen, setRegionOpen] = useState(false)
  const [visitorCountry, setVisitorCountry] = useState('DZ')

  const languageLabels: Record<Locale, { native: string; flag: string }> = {
    en: { native: 'English', flag: '🇬🇧' }, ar: { native: 'العربية', flag: '🇩🇿' }, es: { native: 'Español', flag: '🇪🇸' },
    fr: { native: 'Français', flag: '🇫🇷' }, pt: { native: 'Português', flag: '🇵🇹' }, de: { native: 'Deutsch', flag: '🇩🇪' },
    it: { native: 'Italiano', flag: '🇮🇹' }, pl: { native: 'Polski', flag: '🇵🇱' }, nl: { native: 'Nederlands', flag: '🇳🇱' },
    ro: { native: 'Română', flag: '🇷🇴' }, ru: { native: 'Русский', flag: '🇷🇺' },
  }

  const countryLabels: Record<string, { name: string; flag: string }> = {
    DZ: { name: 'Algeria', flag: '🇩🇿' }, FR: { name: 'France', flag: '🇫🇷' }, GB: { name: 'United Kingdom', flag: '🇬🇧' },
    ES: { name: 'Spain', flag: '🇪🇸' }, DE: { name: 'Germany', flag: '🇩🇪' }, IT: { name: 'Italy', flag: '🇮🇹' },
    PT: { name: 'Portugal', flag: '🇵🇹' }, PL: { name: 'Poland', flag: '🇵🇱' }, NL: { name: 'Netherlands', flag: '🇳🇱' },
    RO: { name: 'Romania', flag: '🇷🇴' }, RU: { name: 'Russia', flag: '🇷🇺' }, US: { name: 'United States', flag: '🇺🇸' },
  }

  useEffect(() => {
    try {
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone
      const timezoneCountries: Record<string, string> = {
        'Africa/Algiers': 'DZ',
        'Africa/Casablanca': 'MA',
        'Africa/Cairo': 'EG',
        'Africa/Tunis': 'TN',
        'Africa/Tripoli': 'LY',
        'Africa/Lagos': 'NG',
        'Africa/Johannesburg': 'ZA',
        'Africa/Nairobi': 'KE',
        'Europe/Paris': 'FR',
        'Europe/London': 'GB',
        'Europe/Dublin': 'IE',
        'Europe/Madrid': 'ES',
        'Europe/Lisbon': 'PT',
        'Europe/Berlin': 'DE',
        'Europe/Rome': 'IT',
        'Europe/Amsterdam': 'NL',
        'Europe/Brussels': 'BE',
        'Europe/Zurich': 'CH',
        'Europe/Warsaw': 'PL',
        'Europe/Prague': 'CZ',
        'Europe/Vienna': 'AT',
        'Europe/Bucharest': 'RO',
        'Europe/Sofia': 'BG',
        'Europe/Athens': 'GR',
        'Europe/Moscow': 'RU',
        'Europe/Kyiv': 'UA',
        'Asia/Dubai': 'AE',
        'Asia/Riyadh': 'SA',
        'Asia/Qatar': 'QA',
        'Asia/Kuwait': 'KW',
        'Asia/Amman': 'JO',
        'Asia/Beirut': 'LB',
        'Asia/Jerusalem': 'IL',
        'Asia/Kolkata': 'IN',
        'Asia/Dhaka': 'BD',
        'Asia/Bangkok': 'TH',
        'Asia/Singapore': 'SG',
        'Asia/Tokyo': 'JP',
        'Asia/Seoul': 'KR',
        'Asia/Shanghai': 'CN',
        'Asia/Taipei': 'TW',
        'Australia/Sydney': 'AU',
        'Pacific/Auckland': 'NZ',
        'America/New_York': 'US',
        'America/Chicago': 'US',
        'America/Denver': 'US',
        'America/Los_Angeles': 'US',
        'America/Toronto': 'CA',
        'America/Vancouver': 'CA',
        'America/Mexico_City': 'MX',
        'America/Sao_Paulo': 'BR',
        'America/Argentina/Buenos_Aires': 'AR',
      }

      let detected = timezoneCountries[timezone]

      // Time zone is the primary signal. If it is ambiguous/unknown,
      // use the browser locale's region as a secondary hint.
      if (!detected) {
        const language = navigator.language || ''
        const region = language.match(/[-_](\\w{2}|\\d{3})$/)?.[1]?.toUpperCase()
        if (region && countryLabels[region]) detected = region
      }

      setVisitorCountry(detected ?? 'DZ')
    } catch {
      setVisitorCountry('DZ')
    }
  }, [])


  function CountryFlag({ code, className = 'h-5 w-7' }: { code: string; className?: string }) {
    return (
      <img
        src={`https://flagcdn.com/w80/${code.toLowerCase()}.png`}
        alt=""
        aria-hidden="true"
        className={`inline-block rounded-[2px] object-cover shadow-sm ${className}`}
        loading="eager"
      />
    )
  }

  const currentLanguage = languageLabels[locale]
  const currentCountry = countryLabels[visitorCountry] ?? countryLabels.DZ
  const localeLinks = (Object.entries(languageLabels) as Array<[Locale, { native: string; flag: string }]>).map(([code, language]) => ({ code, ...language }))

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
      <a href="#features" onClick={closeMenu} className="juba-nav-link juba-ff-nav-link text-sm font-medium transition-colors">{navFeatures}</a>
      <a href="#demo" onClick={closeMenu} className="juba-nav-link juba-ff-nav-link text-sm font-medium transition-colors">{navDemo}</a>
      <a href="#languages" onClick={closeMenu} className="juba-nav-link juba-ff-nav-link text-sm font-medium transition-colors">{navLanguages}</a>
      {showReviews && <a href="#reviews" onClick={closeMenu} className="juba-nav-link juba-ff-nav-link text-sm font-medium transition-colors">{navReviews}</a>}
      {showPricing && <a href="#pricing" onClick={closeMenu} className="juba-nav-link juba-ff-nav-link text-sm font-medium transition-colors">{navPricing}</a>}
      <a href="#faq" onClick={closeMenu} className="juba-nav-link juba-ff-nav-link text-sm font-medium transition-colors">{navFAQ}</a>
    </>
  )

  return (
    <nav className="juba-site-nav juba-ff-site-nav sticky top-0 z-50 w-full transition-all">
      <div className="juba-ff-nav-inner mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link href="/" className="juba-brand juba-ff-brand flex items-center gap-3 group" aria-label={homeLabel}>
          <span className="juba-brand-mark juba-ff-brand-mark relative flex h-10 w-10 items-center justify-center rounded-xl font-black text-lg transition-transform">
            J
            <i className="juba-brand-spark" aria-hidden="true">✦</i>
          </span>
          <span className="juba-ff-brand-copy">
            <span className="juba-ff-brand-name font-sans text-lg font-black tracking-tight">JUBA <span className="juba-brand-accent">LISAN</span></span>
            <small>{brandTagline}</small>
          </span>
        </Link>

        <div className="hidden items-center gap-8 md:flex">{links}</div>

        <div className="hidden items-center gap-3 md:flex">
          <div className="relative">
            <button type="button" onClick={() => setRegionOpen((value) => !value)} aria-expanded={regionOpen} aria-haspopup="menu" className="juba-nav-region flex items-center gap-2 rounded-full border border-[var(--juba-app-line)] bg-white/80 px-3 py-2 text-xs font-bold text-[var(--juba-app-ink)] backdrop-blur transition hover:-translate-y-0.5 hover:shadow-sm">
              <CountryFlag code={visitorCountry} className="h-4 w-6" /><span className="sr-only">{currentCountry.name}</span><ChevronDown className="h-3 w-3" aria-hidden="true" />
            </button>
            {regionOpen && <div role="menu" className="absolute right-0 top-[calc(100%+8px)] z-50 w-72 rounded-2xl border border-[var(--juba-app-line)] bg-white p-3 shadow-xl">
              <div className="mb-2 flex items-center gap-2 px-2 text-[10px] font-black uppercase tracking-[.14em] text-[var(--juba-app-muted)]"><Globe2 className="h-3.5 w-3.5" /> Region & language</div>
              <div className="rounded-xl bg-[var(--juba-app-green-soft)] px-3 py-2.5"><div className="text-[10px] font-bold text-[var(--juba-app-muted)]">Visitor region</div><div className="mt-0.5 flex items-center gap-2 font-black text-[var(--juba-app-ink)]"><CountryFlag code={visitorCountry} className="h-5 w-7" /><span>{currentCountry.name}</span></div></div>
              <div className="mt-3 border-t border-[var(--juba-app-line)] pt-3">
                <div className="px-2 text-[10px] font-bold text-[var(--juba-app-muted)]">Interface language</div>
                <div className="mt-1 grid max-h-56 grid-cols-2 gap-1 overflow-auto">
                  {localeLinks.map((language) => (
                    <Link
                      key={language.code}
                      href={`/${language.code}`}
                      onClick={() => setRegionOpen(false)}
                      className={`flex items-center justify-between rounded-xl px-3 py-2 text-xs font-bold transition ${locale === language.code ? 'bg-[var(--juba-app-green-soft)] text-[var(--juba-app-ink)]' : 'text-[var(--juba-app-muted)] hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-ink)]'}`}
                    >
                      <span>{language.flag} {language.native}</span>
                      {locale === language.code && <Check className="h-3.5 w-3.5 text-[var(--juba-app-green)]" />}
                    </Link>
                  ))}
                </div>
              </div>
              <p className="mt-2 px-2 text-[10px] leading-4 text-[var(--juba-app-muted)]">Your region is detected from your browser time zone. It is only an estimate and is not precise location data.</p>
            </div>}
          </div>
          <Link href={hasSession ? '/dashboard' : '/login'} className="juba-nav-signin juba-ff-nav-signin text-sm font-semibold transition-colors">{hasSession ? dashboard : signIn}</Link>
          <Link href={hasSession ? '/dashboard' : '/register'} className="juba-nav-cta juba-ff-nav-cta rounded-xl px-5 py-2.5 text-sm font-black transition-all active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--landing-green)] focus-visible:ring-offset-2"><span>{hasSession ? dashboard : getStarted}</span><span aria-hidden="true">✦</span></Link>
        </div>

        <button
          type="button"
          onClick={() => setOpen((value) => !value)}
          className="juba-menu juba-ff-menu rounded-xl p-2 md:hidden"
          aria-label={open ? closeMenuLabel : openMenuLabel}
          aria-expanded={open}
          aria-controls="juba-mobile-navigation"
        >
          {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {open && (
        <div id="juba-mobile-navigation" className="juba-mobile-menu juba-ff-mobile-menu border-b px-6 pt-4 pb-6 md:hidden animate-in slide-in-from-top-2 duration-200">
          <div className="flex flex-col gap-4">
            <div className="rounded-2xl border border-[var(--juba-app-line)] bg-white/80 p-3"><div className="text-[10px] font-black uppercase tracking-[.14em] text-[var(--juba-app-muted)]"><CountryFlag code={visitorCountry} className="h-4 w-6" /><span className="sr-only">{currentCountry.name}</span></div></div>
            {links}
            <div className="juba-mobile-actions pt-2 flex flex-col gap-3">
              <Link href={hasSession ? '/dashboard' : '/login'} onClick={closeMenu} className="juba-nav-signin juba-ff-nav-signin w-full text-center py-2 text-sm font-semibold">{hasSession ? dashboard : signIn}</Link>
              <Link href={hasSession ? '/dashboard' : '/register'} onClick={closeMenu} className="juba-nav-cta juba-ff-nav-cta flex w-full items-center justify-center gap-2 rounded-xl py-2.5 text-sm font-black">
                <span>{hasSession ? dashboard : getStarted}</span><span aria-hidden="true">✦</span>
              </Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
