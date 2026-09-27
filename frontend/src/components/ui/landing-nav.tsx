'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Menu, X } from 'lucide-react'
import type { Locale } from '@/lib/locales'

interface LandingNavProps {
  hasSession: boolean
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

export function LandingNav({
  hasSession,
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

  const links = [
    { href: '#features', label: navFeatures },
    { href: '#languages', label: navLanguages },
    { href: '#pricing', label: navPricing },
    { href: '#faq', label: navFAQ },
    ...(showReviews ? [{ href: '#reviews', label: navReviews }] : []),
    ...(navDemo ? [{ href: '#features', label: navDemo }] : []),
  ]

  return (
    <header className="juba-busuu-nav" dir={dir}>
      <div className="juba-busuu-nav-inner">
        <Link href="/" aria-label={homeLabel} className="juba-busuu-brand">
          <Image src="/logo.png" alt="JUBA LISAN" width={150} height={52} priority />
          <span>{brandTagline}</span>
        </Link>

        <nav className="juba-busuu-nav-links" aria-label="Primary navigation">
          {links.slice(0, 5).map((link) => (
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
          <Link href={locale === 'ar' ? '/en' : '/ar'} className="juba-busuu-locale" aria-label="Change language">
            {locale === 'ar' ? 'EN' : 'AR'}
          </Link>
        </div>

        <button
          type="button"
          className="juba-busuu-menu"
          onClick={() => setOpen((value) => !value)}
          aria-expanded={open}
          aria-label={open ? closeMenuLabel : openMenuLabel}
        >
          {open ? <X /> : <Menu />}
        </button>
      </div>

      {open && (
        <div className="juba-busuu-mobile-menu">
          <nav>
            {links.map((link) => (
              <a key={link.href + link.label} href={link.href} onClick={() => setOpen(false)}>{link.label}</a>
            ))}
          </nav>
          <div className="juba-busuu-mobile-actions">
            <Link href={hasSession ? '/dashboard' : '/login'} onClick={() => setOpen(false)}>{hasSession ? dashboard : signIn}</Link>
            <Link href={hasSession ? '/dashboard' : '/register'} onClick={() => setOpen(false)}>{hasSession ? dashboard : getStarted}</Link>
            <Link href={locale === 'ar' ? '/en' : '/ar'} onClick={() => setOpen(false)}>{locale === 'ar' ? 'English' : 'العربية'}</Link>
          </div>
        </div>
      )}
    </header>
  )
}
