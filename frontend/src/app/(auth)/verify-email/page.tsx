'use client'

import { Suspense, useCallback, useEffect, useRef, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { PageLoading } from '@/components/ui/page-loading'

const VERIFY_TIMEOUT_MS = 15_000

function VerifyEmailContent() {
  const t = useTranslations('auth.verifyEmail')
  const tCommon = useTranslations('common')
  const searchParams = useSearchParams()
  const token = searchParams.get('token')
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>(
    'loading'
  )
  const controllerRef = useRef<AbortController | null>(null)

  const verify = useCallback(() => {
    if (!token) {
      setStatus('error')
      return
    }

    setStatus('loading')

    controllerRef.current?.abort()
    const controller = new AbortController()
    controllerRef.current = controller
    const timeoutId = setTimeout(() => controller.abort(), VERIFY_TIMEOUT_MS)

    apiFetch(`/api/auth/verify-email?token=${encodeURIComponent(token)}`, {
      signal: controller.signal,
    })
      .then((res) => setStatus(res.ok ? 'success' : 'error'))
      .catch((err) => {
        if (err instanceof DOMException && err.name === 'AbortError') {
          setStatus('error')
        } else {
          setStatus('error')
        }
      })
      .finally(() => {
        clearTimeout(timeoutId)
        controllerRef.current = null
      })
  }, [token])

  useEffect(() => {
    verify()
    return () => {
      controllerRef.current?.abort()
    }
  }, [verify])

  return (
    <div className="bg-[var(--juba-bg)] bg-dot-grid flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="mb-10 flex flex-col items-center">
          <h1 className="text-[var(--juba-text)] font-sans text-xl font-bold tracking-wide">
            FreeLingo
          </h1>
        </div>
        <div className="border-[var(--juba-border)] bg-[var(--juba-surface)] space-y-6 border-2 border-[var(--juba-border)] p-8 text-center">
          <div className="flex items-center justify-center gap-2">
            <span className="text-[var(--juba-text)] text-[var(--juba-muted)]">●</span>
            <span className="text-[var(--juba-muted)] text-[var(--juba-muted)] font-semibold tracking-wide">
              {t('title')}
            </span>
          </div>

          {status === 'loading' && <PageLoading fullScreen={false} />}

          {status === 'success' && (
            <>
              <p className="text-[var(--juba-text)] font-sans text-sm">{t('success')}</p>
              <Link
                href="/login"
                className="bg-[var(--juba-violet)] text-white hover:bg-[var(--juba-violet)]/90 block w-full py-3 text-center font-sans text-xs font-bold tracking-wide transition-colors"
              >
                {t('goToLogin')}
              </Link>
            </>
          )}

          {status === 'error' && (
            <>
              <p className="text-red-600 font-sans text-xs">{t('error')}</p>
              <button
                onClick={verify}
                className="bg-[var(--juba-violet)] text-white hover:bg-[var(--juba-violet)]/90 block w-full py-3 text-center font-sans text-xs font-bold tracking-wide transition-colors"
              >
                {tCommon('retry')}
              </button>
              <Link
                href="/login"
                className="text-[var(--juba-muted)] hover:text-[var(--juba-text)] block font-sans text-xs underline transition-colors"
              >
                {t('goToLogin')}
              </Link>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default function VerifyEmailPage() {
  return (
    <Suspense>
      <VerifyEmailContent />
    </Suspense>
  )
}
