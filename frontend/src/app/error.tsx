'use client'

import { useEffect } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { getLogger } from '@/lib/logger'

const errorLogger = getLogger('global-error')

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  const t = useTranslations('error')

  useEffect(() => {
    errorLogger.error('Unhandled error', error)
  }, [error])

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-[var(--juba-bg)] px-6 py-12 text-[var(--juba-text)]">
      <div className="juba-hero-glow pointer-events-none absolute inset-0" />
      <div className="relative w-full max-w-lg">
        <div className="mb-8 flex items-center justify-center gap-3">
          <div
            className="flex h-11 w-11 items-center justify-center rounded-2xl text-lg font-black text-white shadow-lg"
            style={{ background: 'var(--juba-primary-dark)' }}
            aria-hidden="true"
          >
            JL
          </div>
          <span className="text-xl font-extrabold tracking-tight">
            JUBA <span style={{ color: 'var(--juba-primary-dark)' }}>LISAN</span>
          </span>
        </div>

        <section className="juba-card overflow-hidden">
          <div className="border-b border-[var(--juba-border-soft)] px-7 py-6 sm:px-9">
            <div className="mb-4 inline-flex items-center rounded-full border border-[color-mix(in_srgb,var(--juba-danger)_35%,var(--juba-border))] bg-[color-mix(in_srgb,var(--juba-danger)_10%,var(--juba-surface))] px-3 py-1 text-[11px] font-bold uppercase tracking-wider text-[var(--juba-danger)]">
              {t('label')}
            </div>
            <h1 className="text-2xl font-black tracking-tight text-[var(--juba-text)]">
              {t('title')}
            </h1>
          </div>

          <div className="space-y-6 px-7 py-7 sm:px-9 sm:py-8">
            <p className="text-sm leading-7 text-[var(--juba-muted)]">
              {t('body')}
            </p>

            {error.digest && (
              <div className="rounded-xl border border-[var(--juba-border-soft)] bg-[var(--juba-surface-soft)] px-4 py-3 text-xs text-[var(--juba-muted)]">
                {t('digest')}: <span className="font-mono">{error.digest}</span>
              </div>
            )}

            <div className="flex flex-col gap-3 sm:flex-row">
              <button
                onClick={reset}
                className="flex-1 rounded-xl px-6 py-3.5 text-sm font-bold text-white shadow-md transition hover:brightness-95 active:scale-[0.98]"
                style={{ background: 'var(--juba-primary-dark)' }}
              >
                {t('retry')}
              </button>
              <Link
                href="/dashboard"
                className="flex-1 rounded-xl border border-[var(--juba-border)] bg-[var(--juba-surface)] px-6 py-3.5 text-center text-sm font-bold text-[var(--juba-text)] transition hover:bg-[var(--juba-surface-soft)]"
              >
                {t('dashboard')}
              </Link>
            </div>
          </div>
        </section>

        <p className="mt-6 text-center text-xs text-[var(--juba-muted)]">
          © {new Date().getFullYear()} JUBA LISAN
        </p>
      </div>
    </main>
  )
}
