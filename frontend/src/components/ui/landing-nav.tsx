'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Menu, X } from 'lucide-react'
import { hasActiveLandingSubscription } from '@/lib/landing-subscription'

interface LandingNavProps {
  hasSession: boolean
  stripeEnabled: boolean
  navFeatures: string
  navReviews: string
  navPricing: string
  navFAQ: string
  showReviews: boolean
  signIn: string
  dashboard: string
}

export function LandingNav({
  hasSession,
  stripeEnabled,
  navFeatures,
  navReviews,
  navPricing,
  navFAQ,
  showReviews,
  signIn,
  dashboard,
}: LandingNavProps) {
  const [open, setOpen] = useState(false)
  const [showPricing, setShowPricing] = useState(stripeEnabled && !hasSession)

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

  const links = (
    <>
      <a href="#features" onClick={() => setOpen(false)} className="juba-nav-link text-[var(--juba-muted)] hover:text-[var(--juba-text)] text-sm font-medium transition-colors">{navFeatures}</a>
      <a href="#demo" onClick={() => setOpen(false)} className="juba-nav-link text-[var(--juba-muted)] hover:text-[var(--juba-text)] text-sm font-medium transition-colors">AI Demo</a>
      <a href="#languages" onClick={() => setOpen(false)} className="juba-nav-link text-[var(--juba-muted)] hover:text-[var(--juba-text)] text-sm font-medium transition-colors">Languages</a>
      {showReviews && <a href="#reviews" onClick={() => setOpen(false)} className="juba-nav-link text-[var(--juba-muted)] hover:text-[var(--juba-text)] text-sm font-medium transition-colors">{navReviews}</a>}
      {showPricing && <a href="#pricing" onClick={() => setOpen(false)} className="juba-nav-link text-[var(--juba-muted)] hover:text-[var(--juba-text)] text-sm font-medium transition-colors">{navPricing}</a>}
      <a href="#faq" onClick={() => setOpen(false)} className="juba-nav-link text-[var(--juba-muted)] hover:text-[var(--juba-text)] text-sm font-medium transition-colors">{navFAQ}</a>
    </>
  )

  return (
    <nav className="juba-site-nav sticky top-0 z-50 w-full border-b border-[var(--juba-border-soft)] bg-[color-mix(in_srgb,var(--juba-surface)_88%,transparent)] backdrop-blur-md transition-all">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link href="/" className="juba-brand flex items-center gap-3 group">
          <div className="juba-brand-mark relative flex h-9 w-9 items-center justify-center rounded-xl bg-[var(--juba-primary-dark)] text-white font-bold text-lg shadow-sm group-hover:scale-105 transition-transform">J</div>
          <span className="font-sans text-lg font-extrabold tracking-tight text-[var(--juba-text)]">JUBA <span className="juba-brand-accent text-[var(--juba-primary-dark)]">LISAN</span></span>
        </Link>

        <div className="hidden items-center gap-8 md:flex">{links}</div>

        <div className="hidden items-center gap-4 md:flex">
          <Link href={hasSession ? '/dashboard' : '/login'} className="juba-nav-signin text-sm font-semibold text-[var(--juba-muted)] hover:text-[var(--juba-text)] transition-colors">{hasSession ? dashboard : signIn}</Link>
          <Link href={hasSession ? '/dashboard' : '/register'} className="juba-nav-cta rounded-xl bg-[var(--juba-primary-dark)] px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:brightness-95 hover:shadow-md transition-all active:scale-95">{hasSession ? dashboard : 'Get Started'}</Link>
        </div>

        <button onClick={() => setOpen(!open)} className="juba-menu rounded-xl p-2 text-[var(--juba-muted)] hover:bg-[var(--juba-surface-soft)] hover:text-[var(--juba-text)] md:hidden" aria-label="Toggle menu">
          {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {open && (
        <div className="juba-mobile-menu border-b border-[var(--juba-border)] bg-[var(--juba-surface)] px-6 pt-4 pb-6 md:hidden animate-in slide-in-from-top-2 duration-200">
          <div className="flex flex-col gap-4">
            {links}
            <div className="pt-2 border-t border-[var(--juba-border-soft)] flex flex-col gap-3">
              <Link href={hasSession ? '/dashboard' : '/login'} onClick={() => setOpen(false)} className="juba-nav-signin w-full text-center py-2 text-sm font-semibold text-[var(--juba-muted)] hover:text-[var(--juba-text)]">{hasSession ? dashboard : signIn}</Link>
              <Link href={hasSession ? '/dashboard' : '/register'} onClick={() => setOpen(false)} className="juba-nav-cta w-full text-center rounded-xl bg-[var(--juba-primary-dark)] py-2.5 text-sm font-semibold text-white shadow-sm hover:brightness-95">{hasSession ? dashboard : 'Get Started'}</Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
