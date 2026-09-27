'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { ChevronDown, Menu, X } from 'lucide-react'
import type { Locale } from '@/lib/locales'

interface LandingNavProps {
  hasSession: boolean
  dir: 'ltr' | 'rtl'
  navFeatures: string
  navLanguages: string
  navReviews: string
  navPricing: string
  navFAQ: string
  showReviews: boolean
  signIn: string
  dashboard: string
  getStarted: string
  homeLabel: string
  openMenuLabel: string
  closeMenuLabel: string
  locale: Locale
}

export function LandingNav({
  hasSession,
  dir,
  navFeatures,
  navLanguages,
  navReviews,
  navPricing,
  navFAQ,
  showReviews,
  signIn,
  dashboard,
  getStarted,
  homeLabel,
  openMenuLabel,
  closeMenuLabel,
  locale,
}: LandingNavProps) {
  const [open, setOpen] = useState(false)

  const localeOptions: Array<[Locale, string]> = [
    ['en', 'English'], ['ar', 'العربية'], ['es', 'Español'], ['fr', 'Français'],
    ['pt', 'Português'], ['de', 'Deutsch'], ['it', 'Italiano'], ['pl', 'Polski'],
    ['nl', 'Nederlands'], ['ro', 'Română'], ['ru', 'Русский'],
  ]

  const links = [
    { href: '#features', label: navFeatures },
    { href: '#languages', label: navLanguages },
    { href: '#pricing', label: navPricing },
    { href: '#faq', label: navFAQ },
    ...(showReviews ? [{ href: '#reviews', label: navReviews }] : []),
  ]

  const close = () => setOpen(false)

  return (
    <header className="juba-busuu-nav" dir={dir}>
      <div className="juba-busuu-nav-inner">
        <Link href="/" aria-label={homeLabel} className="juba-busuu-brand">
          <Image src="/logo.png" alt="JUBA LISAN" width={150} height={52} priority />
        </Link>

        <nav className="juba-busuu-nav-links" aria-label={navFeatures}>
          {links.map((link) => (
            <a key={link.href + link.label} href={link.href}>{link.label}</a>
          ))}
        </nav>

        <div className="juba-busuu-nav-actions">
          <Link href={hasSession ? '/dashboard' : '/login'} className="juba-busuu-login">
            {hasSession ? dashboard : signIn}
          </Link>
          <Link href={hasSession ? '/dashboard' : '/register'} className="juba-busuu-nav-cta">
            {hasSession ? dashboard : getStarted}
          </Link>
          <details className="juba-busuu-locale-menu">
            <summary className="juba-busuu-locale" aria-label={navLanguages}>
              <span>{locale.toUpperCase()}</span><ChevronDown aria-hidden="true" />
            </summary>
            <div className="juba-busuu-locale-options">
              {localeOptions.map(([code, label]) => (
                <Link key={code} href={code === 'en' ? '/' : `/${code}`} aria-current={code === locale ? 'page' : undefined}>
                  {label}
                </Link>
              ))}
            </div>
          </details>
        </div>

        <button type="button" className="juba-busuu-menu" onClick={() => setOpen((v) => !v)}
          aria-expanded={open} aria-label={open ? closeMenuLabel : openMenuLabel}>
          {open ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
        </button>
      </div>

      {open && (
        <div className="juba-busuu-mobile-menu">
          <nav aria-label={navFeatures}>
            {links.map((link) => (
              <a key={link.href + link.label} href={link.href} onClick={close}>{link.label}</a>
            ))}
          </nav>
          <div className="juba-busuu-mobile-actions">
            <Link href={hasSession ? '/dashboard' : '/login'} onClick={close}>{hasSession ? dashboard : signIn}</Link>
            <Link className="juba-busuu-mobile-cta" href={hasSession ? '/dashboard' : '/register'} onClick={close}>
              {hasSession ? dashboard : getStarted}
            </Link>
            <div className="juba-busuu-mobile-locales">
              {localeOptions.map(([code, label]) => (
                <Link key={code} href={code === 'en' ? '/' : `/${code}`} onClick={close}
                  aria-current={code === locale ? 'page' : undefined}>
                  {label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}
    </header>
  )
}
