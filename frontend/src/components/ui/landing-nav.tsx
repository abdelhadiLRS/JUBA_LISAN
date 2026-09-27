'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { ChevronDown, Menu, X } from 'lucide-react'
import type { Locale } from '@/lib/locales'

interface LandingNavProps {
  hasSession: boolean
  dir: 'ltr' | 'rtl'
  navFeatures: string
  primaryNavigation: string
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
  primaryNavigation,
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
  const menuButtonRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    if (!open) return

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setOpen(false)
        requestAnimationFrame(() => menuButtonRef.current?.focus())
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [open])

  const localeOptions: Array<[Locale, string]> = [
    ['en', 'English'],
    ['ar', 'العربية'],
    ['es', 'Español'],
    ['fr', 'Français'],
    ['pt', 'Português'],
    ['de', 'Deutsch'],
    ['it', 'Italiano'],
    ['pl', 'Polski'],
    ['nl', 'Nederlands'],
    ['ro', 'Română'],
    ['ru', 'Русский'],
  ]

  const links = [
    { href: '#features', label: navFeatures },
    { href: '#languages', label: navLanguages },
    { href: '#pricing', label: navPricing },
    { href: '#faq', label: navFAQ },
    ...(showReviews ? [{ href: '#reviews', label: navReviews }] : []),
  ]

  const close = (href?: string) => {
    setOpen(false)
    requestAnimationFrame(() => {
      if (href?.startsWith('#')) {
        const target = document.querySelector<HTMLElement>(href)
        if (target) {
          const hadTabIndex = target.hasAttribute('tabindex')
          if (!hadTabIndex) target.setAttribute('tabindex', '-1')
          target.focus({ preventScroll: true })
          if (!hadTabIndex) {
            target.addEventListener('blur', () => target.removeAttribute('tabindex'), { once: true })
          }
          return
        }
      }
      menuButtonRef.current?.focus()
    })
  }

  return (
    <header className="juba-busuu-nav" dir={dir}>
      <div className="juba-busuu-nav-inner">
        <Link href="/" aria-label={homeLabel} className="juba-busuu-brand">
          <Image src="/logo.png" alt="JUBA LISAN" width={150} height={52} priority />
        </Link>

        <nav className="juba-busuu-nav-links" aria-label={primaryNavigation}>
          {links.map((link) => (
            <a key={link.href} href={link.href}>
              {link.label}
            </a>
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
              <span>{locale.toUpperCase()}</span>
              <ChevronDown aria-hidden="true" />
            </summary>
            <div className="juba-busuu-locale-options">
              {localeOptions.map(([code, label]) => (
                <Link
                  key={code}
                  href={code === 'en' ? '/' : `/${code}`}
                  aria-current={code === locale ? 'page' : undefined}
                  lang={code}
                  hrefLang={code}
                >
                  {label}
                </Link>
              ))}
            </div>
          </details>
        </div>

        <button
          ref={menuButtonRef}
          type="button"
          className="juba-busuu-menu"
          onClick={() => setOpen((value) => !value)}
          aria-expanded={open}
          aria-controls="juba-busuu-mobile-menu"
          aria-label={open ? closeMenuLabel : openMenuLabel}
        >
          {open ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
        </button>
      </div>

      {open && (
        <div id="juba-busuu-mobile-menu" className="juba-busuu-mobile-menu">
          <nav aria-label={primaryNavigation}>
            {links.map((link) => (
              <a key={link.href + link.label} href={link.href} onClick={() => close(link.href)}>
                {link.label}
              </a>
            ))}
          </nav>
          <div className="juba-busuu-mobile-actions">
            <Link href={hasSession ? '/dashboard' : '/login'} onClick={close}>
              {hasSession ? dashboard : signIn}
            </Link>
            <Link
              className="juba-busuu-mobile-cta"
              href={hasSession ? '/dashboard' : '/register'}
              onClick={close}
            >
              {hasSession ? dashboard : getStarted}
            </Link>
            <div className="juba-busuu-mobile-locales">
              {localeOptions.map(([code, label]) => (
                <Link
                  key={code}
                  href={code === 'en' ? '/' : `/${code}`}
                  onClick={close}
                  aria-current={code === locale ? 'page' : undefined}
                  lang={code}
                  hrefLang={code}
                >
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
