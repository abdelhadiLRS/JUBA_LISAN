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
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-white px-6 py-12 text-neutral-900 dark:bg-neutral-950 dark:text-white">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(245,158,11,0.14),transparent_42%)]" />
      <div className="relative w-full max-w-lg">
        <div className="mb-8 flex items-center justify-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-amber-500 text-lg font-black text-white shadow-lg shadow-amber-500/20">
            J
          </div>
          <span className="text-xl font-extrabold tracking-tight">
            JUBA <span className="text-amber-600 dark:text-amber-400">LISAN</span>
          </span>
        </div>

        <section className="juba-card overflow-hidden bg-white/95 dark:bg-neutral-900/95">
          <div className="border-b border-neutral-200 px-7 py-6 dark:border-neutral-800 sm:px-9">
            <div className="mb-4 inline-flex items-center rounded-full border border-red-200 bg-red-50 px-3 py-1 text-[11px] font-bold uppercase tracking-wider text-red-600 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-400">
              {t('label')}
            </div>
            <h1 className="text-2xl font-black tracking-tight text-neutral-900 dark:text-white">
              {t('title')}
            </h1>
          </div>

          <div className="space-y-6 px-7 py-7 sm:px-9 sm:py-8">
            <p className="text-sm leading-7 text-neutral-600 dark:text-neutral-300">
              {t('body')}
            </p>

            {error.digest && (
              <div className="rounded-xl border border-neutral-200 bg-neutral-50 px-4 py-3 text-xs text-neutral-500 dark:border-neutral-800 dark:bg-neutral-950 dark:text-neutral-400">
                {t('digest')}: <span className="font-mono">{error.digest}</span>
              </div>
            )}

            <div className="flex flex-col gap-3 sm:flex-row">
              <button
                onClick={reset}
                className="flex-1 rounded-xl bg-amber-500 px-6 py-3.5 text-sm font-bold text-white shadow-md shadow-amber-500/20 transition hover:bg-amber-600 active:scale-[0.98]"
              >
                {t('retry')}
              </button>
              <Link
                href="/dashboard"
                className="flex-1 rounded-xl border border-neutral-200 px-6 py-3.5 text-center text-sm font-bold text-neutral-700 transition hover:bg-neutral-50 dark:border-neutral-800 dark:text-neutral-200 dark:hover:bg-neutral-800"
              >
                {t('dashboard')}
              </Link>
            </div>
          </div>
        </section>

        <p className="mt-6 text-center text-xs text-neutral-400 dark:text-neutral-600">
          © {new Date().getFullYear()} JUBA LISAN
        </p>
      </div>
    </main>
  )
}
