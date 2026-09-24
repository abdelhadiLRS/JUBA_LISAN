'use client'

import { useState, useEffect } from 'react'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'

interface ContactFormModalProps {
  open: boolean
  onClose: () => void
}

type Status = 'idle' | 'loading' | 'success' | 'error'

export function ContactFormModal({ open, onClose }: ContactFormModalProps) {
  const t = useTranslations('contact')
  const tCommon = useTranslations('common')

  const [email, setEmail] = useState('')
  const [subject, setSubject] = useState('')
  const [description, setDescription] = useState('')
  const [status, setStatus] = useState<Status>('idle')
  const [errorMsg, setErrorMsg] = useState('')

  useEffect(() => {
    if (open) {
      setEmail('')
      setSubject('')
      setDescription('')
      setStatus('idle')
      setErrorMsg('')
    }
  }, [open])

  useEffect(() => {
    if (!open) return
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, onClose])

  useEffect(() => {
    if (status !== 'success') return
    const timer = setTimeout(() => onClose(), 2000)
    return () => clearTimeout(timer)
  }, [status, onClose])

  if (!open) return null

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setStatus('loading')
    setErrorMsg('')
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, subject, description }),
      })
      if (res.status === 204) {
        setStatus('success')
      } else {
        const data = await res.json().catch(() => ({}))
        setErrorMsg(data?.detail ?? t('errorGeneric'))
        setStatus('error')
      }
    } catch {
      setErrorMsg(t('errorGeneric'))
      setStatus('error')
    }
  }

  const isLoading = status === 'loading'

  return (
    <div
      className="fixed inset-0 z-[200] flex items-center justify-center p-4"
      style={{
        backgroundColor: 'color-mix(in srgb, var(--juba-app-ink) 55%, transparent)',
        backdropFilter: 'blur(8px)',
      }}
      onClick={onClose}
    >
      <div
        className="juba-card w-full max-w-md overflow-hidden border-2 border-[var(--juba-app-line)] shadow-[5px_5px_0_var(--juba-app-line)]"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-3 border-b-2 border-[var(--juba-app-line)] bg-[#fffdf8] px-6 py-4">
          <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[var(--juba-app-green-soft)] text-sm text-[var(--juba-app-green-dark)]" aria-hidden="true">
            ●
          </span>
          <span className="flex-1 text-sm font-semibold tracking-tight text-[var(--juba-app-ink)]">
            {t('title')}
          </span>
          <button
            onClick={onClose}
            className="rounded-xl border-2 border-transparent px-2 py-1 text-[var(--juba-app-muted)] transition hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-ink)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)]"
            aria-label={tCommon('close')}
          >
            ✕
          </button>
        </div>

        {status === 'success' ? (
          <div className="flex flex-col items-center gap-3 px-6 py-10">
            <span className="rounded-full bg-[color-mix(in srgb, var(--juba-app-yellow) 28%, var(--juba-app-surface))] px-4 py-2 text-sm font-semibold text-[var(--juba-app-green-dark)]">
              ✓ {t('sent')}
            </span>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="flex flex-col gap-5 px-6 py-6">
              <div className="flex flex-col gap-2">
                <label className="text-xs font-semibold text-[var(--juba-app-muted)]">{t('labelEmail')}</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={isLoading}
                  className="rounded-xl border-2 border-[var(--juba-app-line)] bg-[#fffdf8] shadow-[2px_2px_0_var(--juba-app-line)] px-3 py-2.5 text-sm text-[var(--juba-app-ink)] placeholder:text-[var(--juba-app-muted)] transition focus:border-[var(--juba-app-green)] focus:outline-none focus:ring-2 focus:ring-[var(--juba-app-green)]/30 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder={t('placeholderEmail')}
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-xs font-semibold text-[var(--juba-app-muted)]">{t('labelSubject')}</label>
                <input
                  type="text"
                  required
                  maxLength={200}
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  disabled={isLoading}
                  className="rounded-xl border border-[var(--juba-app-line)] bg-[#fffdf8] px-3 py-2.5 text-sm text-[var(--juba-app-ink)] placeholder:text-[var(--juba-app-muted)] transition focus:border-[var(--juba-app-green)] focus:outline-none focus:ring-2 focus:ring-[var(--juba-app-green)]/30 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder={t('placeholderSubject')}
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-xs font-semibold text-[var(--juba-app-muted)]">{t('labelDescription')}</label>
                <textarea
                  required
                  maxLength={5000}
                  rows={5}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  disabled={isLoading}
                  className="min-h-[120px] resize-y rounded-xl border-2 border-[var(--juba-app-line)] bg-[#fffdf8] shadow-[2px_2px_0_var(--juba-app-line)] px-3 py-2.5 text-sm leading-6 text-[var(--juba-app-ink)] placeholder:text-[var(--juba-app-muted)] transition focus:border-[var(--juba-app-green)] focus:outline-none focus:ring-2 focus:ring-[var(--juba-app-green)]/30 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder={t('placeholderDescription')}
                />
              </div>

              {status === 'error' && (
                <p className="rounded-xl bg-[color-mix(in_srgb,#b33a32_10%,var(--juba-app-surface))] px-3 py-2.5 text-sm leading-relaxed text-[#b33a32]">
                  {errorMsg}
                </p>
              )}
            </div>

            <div className="flex gap-3 border-t-2 border-[var(--juba-app-line)] bg-[#fffdf8] px-6 py-4">
              <button
                type="button"
                onClick={onClose}
                disabled={isLoading}
                className="flex-1 rounded-xl border-2 border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] shadow-[2px_2px_0_var(--juba-app-line)] px-4 py-2.5 text-sm font-semibold text-[var(--juba-app-muted)] transition hover:border-[var(--juba-app-green)] hover:text-[var(--juba-app-ink)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)] disabled:cursor-not-allowed disabled:opacity-50"
              >
                {tCommon('cancel')}
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 rounded-xl border-2 border-[var(--juba-app-line)] bg-[var(--juba-app-green-dark)] shadow-[3px_3px_0_var(--juba-app-line)] px-4 py-2.5 text-sm font-semibold text-white transition hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)] focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 inline h-4 w-4 animate-spin" />
                    {t('sending')}
                  </>
                ) : (
                  t('send')
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
