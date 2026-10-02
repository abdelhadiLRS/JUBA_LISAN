'use client'

import { useEffect } from 'react'
import Link from 'next/link'

interface DashboardErrorProps {
  error: Error & { digest?: string }
  reset: () => void
}

export default function DashboardError({ error, reset }: DashboardErrorProps) {
  useEffect(() => {
    console.error('JUBA LISAN dashboard error', error)
  }, [error])

  return (
    <main className="juba-reference-page flex min-h-[70vh] items-center justify-center px-6 py-12">
      <section className="juba-reference-list-card w-full max-w-lg p-8 text-center">
        <p className="text-[var(--duo-green-dark)] mb-3 font-mono text-xs font-semibold tracking-[0.2em] uppercase">
          JUBA LISAN
        </p>
        <h1 className="text-[var(--duo-ink)] mb-3 text-xl font-semibold">
          Dashboard temporarily unavailable
        </h1>
        <p className="text-[var(--duo-muted)] mb-6 text-sm leading-6">
          The dashboard could not render correctly. Your account data is not
          affected. Try again, or return to the dashboard entry point.
        </p>
        {error.digest && (
          <p className="text-[var(--duo-muted)] mb-6 font-mono text-xs">
            Error reference: {error.digest}
          </p>
        )}
        <div className="flex flex-wrap items-center justify-center gap-3">
          <button
            type="button"
            onClick={reset}
            className="juba-primary-button px-5 py-2.5 text-sm"
          >
            Try again
          </button>
          <Link
            href="/dashboard"
            className="juba-secondary-button px-5 py-2.5 text-sm"
          >
            Go to dashboard
          </Link>
        </div>
      </section>
    </main>
  )
}
