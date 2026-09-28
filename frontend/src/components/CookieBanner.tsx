'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'

const COOKIE_KEY = 'fl_cookie_consent'

export function CookieBanner() {
  const t = useTranslations('cookieBanner')
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    try {
      if (!localStorage.getItem(COOKIE_KEY)) {
        setVisible(true)
      }
    } catch {
      // localStorage unavailable (SSR, private mode) — don't show
    }
  }, [])

  function accept() {
    try {
      localStorage.setItem(COOKIE_KEY, 'accepted')
    } catch {
      /* ignore */
    }
    setVisible(false)
  }

  if (!visible) return null

  return (
    <div className="fixed inset-x-0 bottom-0 z-50 border-t border-[var(--duo-line)] bg-[var(--duo-card)] shadow-[0_-3px_0_var(--duo-line)]">
      <div className="mx-auto flex max-w-5xl flex-col items-start gap-4 px-4 py-4 sm:flex-row sm:items-center sm:px-6">
        <p className="flex-1 text-xs font-medium leading-relaxed text-[var(--duo-muted)]">
          {t('message')}{' '}
          <Link
            href="/privacy"
            className="font-bold text-[var(--duo-ink)] underline decoration-[#5862e2] decoration-2 underline-offset-2 transition-opacity hover:opacity-70 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-purple)] focus-visible:ring-offset-2"
          >
            {t('learnMore')}
          </Link>
        </p>
        <button
          type="button"
          onClick={accept}
          className="inline-flex min-h-10 flex-shrink-0 items-center justify-center rounded-[14px] bg-[var(--duo-purple)] px-5 py-2 text-xs font-black uppercase tracking-wider text-white shadow-[0_3px_0_var(--duo-purple)] transition hover:bg-[var(--duo-purple)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-purple)] focus-visible:ring-offset-2"
        >
          {t('accept')}
        </button>
      </div>
    </div>
  )
}
