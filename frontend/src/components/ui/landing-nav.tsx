'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { ChevronDown, Menu, X } from 'lucide-react'
import { normalizeLocale, type Locale } from '@/lib/locales'

interface LandingNavProps {
  hasSession: boolean
  allowRegistration: boolean
  dir: 'ltr' | 'rtl'
  navFeatures: string
  primaryNavigation: string
  navLanguages: string
  interfaceLanguages: string
  navReviews: string
  navPricing: string
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
  allowRegistration,
  dir,
  navFeatures,
  primaryNavigation,
  navLanguages,
  interfaceLanguages,
  navReviews,
  navPricing,
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
  const headerRef = useRef<HTMLElement>(null)
  const menuRef = useRef<HTMLDivElement>(null)
  const localeMenuRef = useRef<HTMLDetailsElement>(null)

  useEffect(() => {
    if (!open) return

    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'

    requestAnimationFrame(() => {
      menuRef.current?.querySelector<HTMLElement>('a, button, [tabindex]:not([tabindex="-1"])')?.focus()
    })

    const handlePointerDown = (event: PointerEvent) => {
      if (!(event.target instanceof Node) || headerRef.current?.contains(event.target)) return
      setOpen(false)
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault()
        setOpen(false)
        requestAnimationFrame(() => menuButtonRef.current?.focus())
        return
      }

      if (event.key !== 'Tab' || !menuRef.current) return
      const focusable = [
        ...(menuButtonRef.current ? [menuButtonRef.current] : []),
        ...Array.from(
          menuRef.current.querySelectorAll<HTMLElement>('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'),
        ),
      ]
      if (!focusable.length) return

      const first = focusable[0]
      const last = focusable[focusable.length - 1]
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault()
        last.focus()
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault()
        first.focus()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    document.addEventListener('pointerdown', handlePointerDown)
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      document.removeEventListener('pointerdown', handlePointerDown)
      document.body.style.overflow = previousOverflow
    }
  }, [open])

  useEffect(() => {
    const handleViewportChange = () => {
      if (!window.matchMedia('(min-width: 1001px)').matches) return

      if (open) {
        setOpen(false)
        requestAnimationFrame(() => {
          document.querySelector<HTMLElement>('.juba-busuu-nav-links a')?.focus()
        })
      }

      if (localeMenuRef.current) localeMenuRef.current.open = false
    }

    handleViewportChange()
    window.addEventListener('resize', handleViewportChange)
    return () => window.removeEventListener('resize', handleViewportChange)
  }, [open])

  useEffect(() => {
    const handlePointerDown = (event: PointerEvent) => {
      const menu = localeMenuRef.current
      if (!menu?.open || !(event.target instanceof Node) || menu.contains(event.target)) return
      menu.open = false
    }

    document.addEventListener('pointerdown', handlePointerDown)
    return () => document.removeEventListener('pointerdown', handlePointerDown)
  }, [])

  const localeCodes: Locale[] = ['en', 'ar', 'es', 'fr', 'pt', 'de', 'it', 'pl', 'nl', 'ro', 'ru']
  const safeLocale = typeof locale === 'string' ? normalizeLocale(locale) : 'en'
  const localeDisplayNames = new Intl.DisplayNames([safeLocale], { type: 'language' })
  const localeOptions: Array<[Locale, string]> = localeCodes.map((code) => [
    code,
    localeDisplayNames.of(code) ?? code.toUpperCase(),
  ])

  const links = [
    { href: '#features', label: navFeatures },
    { href: '#languages', label: navLanguages },
    ...(showReviews ? [{ href: '#reviews', label: navReviews }] : []),
    { href: '#pricing', label: navPricing },
  ]
  const desktopLinks = links.slice(1)

  const handleLocaleKeyDown = (event: React.KeyboardEvent<HTMLDetailsElement>) => {
    if (event.key !== 'Escape' || !localeMenuRef.current?.open) return
    event.preventDefault()
    localeMenuRef.current.open = false
    requestAnimationFrame(() => localeMenuRef.current?.querySelector<HTMLElement>('summary')?.focus())
  }

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
    <header ref={headerRef} className="juba-busuu-nav" dir={dir}>
      <div className="juba-busuu-nav-inner">
        <Link href={safeLocale === 'en' ? '/' : `/${safeLocale}`} aria-label={homeLabel} aria-current="page" className="juba-busuu-brand" data-brand="JUBA LISAN">
          <Image src="/logo.png" alt="JUBA LISAN" width={150} height={52} priority style={{ height: 'auto' }} />
        </Link>

        <nav className="juba-busuu-nav-links" aria-label={primaryNavigation}>
          <a href="#features" className="juba-busuu-nav-pill">{navFeatures}</a>
          {desktopLinks.map((link) => (
            <a key={link.href} href={link.href}>{link.label}</a>
          ))}
        </nav>

        <div className="juba-busuu-nav-actions">
          {!hasSession && (
            <Link href="/login" className="juba-busuu-login">
              {signIn}
            </Link>
          )}
          <Link href={hasSession ? '/dashboard' : allowRegistration ? '/register' : '/login'} className="juba-busuu-nav-cta">
            {hasSession ? dashboard : allowRegistration ? getStarted : signIn}
          </Link>
          <span className="juba-busuu-nav-rule" aria-hidden="true" />
          <details ref={localeMenuRef} onKeyDown={handleLocaleKeyDown} className="juba-busuu-locale-menu">
            <summary
              className="juba-busuu-locale"
              aria-label={`${interfaceLanguages}: ${localeDisplayNames.of(safeLocale) ?? safeLocale.toUpperCase()}`}
            >
              <span>{safeLocale.toUpperCase()}</span>
              <ChevronDown aria-hidden="true" />
            </summary>
            <div className="juba-busuu-locale-options">
              {localeOptions.map(([code, label]) => (
                <Link
                  key={code}
                  href={code === 'en' ? '/' : `/${code}`}
                  aria-current={code === safeLocale ? 'page' : undefined}
                  lang={code}
                  dir="auto"
                  hrefLang={code}
                  onClick={() => {
                    if (localeMenuRef.current) localeMenuRef.current.open = false
                  }}
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

      <div
        ref={menuRef}
        id="juba-busuu-mobile-menu"
        className="juba-busuu-mobile-menu"
        hidden={!open}
        aria-hidden={!open}
      >
        <nav aria-label={primaryNavigation}>
          {links.map((link) => (
            <a key={link.href + link.label} href={link.href} onClick={() => close(link.href)}>
              {link.label}
            </a>
          ))}
        </nav>
        <div className="juba-busuu-mobile-actions">
          {!hasSession && (
            <Link href="/login" onClick={() => close()}>
              {signIn}
            </Link>
          )}
          <Link
            className="juba-busuu-mobile-cta"
            href={hasSession ? '/dashboard' : allowRegistration ? '/register' : '/login'}
            onClick={() => close()}
          >
            {hasSession ? dashboard : allowRegistration ? getStarted : signIn}
          </Link>
          <nav className="juba-busuu-mobile-locales" aria-label={interfaceLanguages}>
            {localeOptions.map(([code, label]) => (
              <Link
                key={code}
                href={code === 'en' ? '/' : `/${code}`}
                onClick={() => close()}
                aria-current={code === safeLocale ? 'page' : undefined}
                lang={code}
                dir="auto"
                hrefLang={code}
              >
                {label}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  )
}
