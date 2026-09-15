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
    <main className="flex min-h-[70vh] items-center justify-center px-6 py-12">
      <section className="border-fl-border bg-fl-surface w-full max-w-lg border p-8 text-center shadow-sm">
        <p className="text-fl-accent mb-3 font-mono text-xs font-semibold tracking-[0.2em] uppercase">
          JUBA LISAN
        </p>
        <h1 className="text-fl-fg mb-3 text-xl font-semibold">
          Dashboard temporarily unavailable
        </h1>
        <p className="text-fl-muted-2 mb-6 text-sm leading-6">
          The dashboard could not render correctly. Your account data is not
          affected. Try again, or return to the dashboard entry point.
        </p>
        {error.digest && (
          <p className="text-fl-muted-3 mb-6 font-mono text-xs">
            Error reference: {error.digest}
          </p>
        )}
        <div className="flex flex-wrap items-center justify-center gap-3">
          <button
            type="button"
            onClick={reset}
            className="bg-fl-accent text-fl-accent-fg rounded-xl px-5 py-2.5 text-sm font-semibold transition-opacity hover:opacity-90"
          >
            Try again
          </button>
          <Link
            href="/dashboard"
            className="border-fl-border text-fl-fg rounded-xl border px-5 py-2.5 text-sm font-medium transition-colors hover:bg-[var(--juba-surface-soft)]"
          >
            Go to dashboard
          </Link>
        </div>
      </section>
    </main>
  )
}
