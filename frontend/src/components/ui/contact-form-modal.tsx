'use client'

import { useState, useEffect, useRef, useId } from 'react'
import { AlertCircle, CheckCircle2, CircleHelp, LoaderCircle, Send, X } from 'lucide-react'
import { useTranslations } from 'next-intl'


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
  const dialogRef = useRef<HTMLDivElement>(null)
  const titleId = useId()
  const descriptionId = useId()
  const firstFieldRef = useRef<HTMLInputElement>(null)
  const openerRef = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (open) {
      openerRef.current = document.activeElement as HTMLElement | null
      requestAnimationFrame(() => firstFieldRef.current?.focus())
      setEmail('')
      setSubject('')
      setDescription('')
      setStatus('idle')
      setErrorMsg('')
    } else {
      openerRef.current?.focus()
      openerRef.current = null
    }
  }, [open])

  const isLoading = status === 'loading'

  useEffect(() => {
    if (!open) return
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape' && !isLoading) onClose()
      if (e.key !== 'Tab') return
      const controls = dialogRef.current?.querySelectorAll<HTMLElement>(
        'button:not(:disabled), input:not(:disabled), textarea:not(:disabled)'
      )
      if (!controls?.length) return
      const first = controls[0]
      const last = controls[controls.length - 1]
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault()
        last.focus()
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault()
        first.focus()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, onClose, isLoading])

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

  return (
    <div
      className="fixed inset-0 z-[200] flex items-center justify-center p-4"
      style={{
        backgroundColor: 'color-mix(in srgb, var(--busuu-ink) 55%, transparent)',
        backdropFilter: 'blur(8px)',
      }}
      onClick={() => !isLoading && onClose()}
      aria-busy={isLoading}
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={descriptionId}
        className="w-full max-w-md overflow-hidden rounded-3xl border border-[var(--busuu-line)] bg-[var(--busuu-card)] text-[var(--busuu-ink)] shadow-[0_24px_70px_color-mix(in_srgb,var(--busuu-ink)_18%,transparent)]"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-3 border-b border-[var(--busuu-line)] bg-[var(--busuu-mint)] px-6 py-4">
          <span className="flex h-8 w-8 items-center justify-center rounded-full bg-white text-[var(--busuu-green-dark)]" aria-hidden="true">
            <CircleHelp className="h-4 w-4" aria-hidden="true" />
          </span>
          <span id={titleId} className="flex-1 text-sm font-bold tracking-tight text-[var(--busuu-ink)]">
            {t('title')}
          </span>
          <button
            type="button"
            onClick={onClose}
            disabled={isLoading}
            aria-label={tCommon('close')}
            className="inline-flex h-9 w-9 items-center justify-center rounded-full text-[var(--busuu-muted)] transition hover:bg-white hover:text-[var(--busuu-ink)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--busuu-green)] disabled:opacity-50"
          >
            <X className="h-4 w-4" aria-hidden="true" />
          </button>
        </div>

        {status === 'success' ? (
          <div className="flex flex-col items-center gap-3 px-6 py-10" role="status" aria-live="polite">
            <span className="inline-flex items-center gap-2 rounded-full bg-[var(--busuu-mint)] px-4 py-2 text-sm font-bold text-[var(--busuu-green-dark)]">
              <CheckCircle2 className="h-4 w-4" aria-hidden="true" /> {t('sent')}
            </span>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <p id={descriptionId} className="sr-only">{t('description')}</p>
            <div className="flex flex-col gap-5 px-6 py-6">
              <div className="flex flex-col gap-2">
                <label htmlFor="contact-email" className="text-xs font-semibold text-[var(--busuu-muted)]">{t('labelEmail')}</label>
                <input
                  ref={firstFieldRef}
                  id="contact-email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={isLoading}
                  className="w-full rounded-xl border border-[var(--busuu-line)] bg-white px-3 py-2.5 text-sm text-[var(--busuu-ink)] placeholder:text-[var(--busuu-muted)] transition focus:border-[var(--busuu-green)] focus:outline-none focus:ring-2 focus:ring-[var(--busuu-green)]/20 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder={t('placeholderEmail')}
                />
              </div>

              <div className="flex flex-col gap-2">
                <label htmlFor="contact-subject" className="text-xs font-semibold text-[var(--duo-muted)]">{t('labelSubject')}</label>
                <input
                  id="contact-subject"
                  type="text"
                  required
                  maxLength={200}
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  disabled={isLoading}
                  className="w-full rounded-xl border border-[var(--busuu-line)] bg-white px-3 py-2.5 text-sm text-[var(--busuu-ink)] placeholder:text-[var(--busuu-muted)] transition focus:border-[var(--busuu-green)] focus:outline-none focus:ring-2 focus:ring-[var(--busuu-green)]/20 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder={t('placeholderSubject')}
                />
              </div>

              <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between gap-3">
                  <label htmlFor="contact-description" className="text-xs font-semibold text-[var(--duo-muted)]">{t('labelDescription')}</label>
                  <span className="text-[10px] font-medium tabular-nums text-[var(--duo-muted)]">{description.length}/5000</span>
                </div>
                <textarea
                  id="contact-description"
                  required
                  maxLength={5000}
                  rows={5}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  disabled={isLoading}
                  className="w-full min-h-[120px] resize-y rounded-xl border border-[var(--busuu-line)] bg-white px-3 py-2.5 text-sm leading-6 text-[var(--busuu-ink)] placeholder:text-[var(--busuu-muted)] transition focus:border-[var(--busuu-green)] focus:outline-none focus:ring-2 focus:ring-[var(--busuu-green)]/20 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder={t('placeholderDescription')}
                />
              </div>

              {status === 'error' && (
                <p role="alert" className="inline-flex w-full items-start gap-2 rounded-xl bg-[color-mix(in_srgb,var(--busuu-green)_8%,white)] px-3 py-2.5 text-sm leading-relaxed text-[var(--busuu-green-dark)]">
                  <AlertCircle className="h-4 w-4 shrink-0" aria-hidden="true" />
                  <span>{errorMsg}</span>
                </p>
              )}
            </div>

            <div className="flex gap-3 border-t border-[var(--busuu-line)] bg-[var(--busuu-cream)] px-6 py-4">
              <button
                type="button"
                onClick={onClose}
                disabled={isLoading}
                className="flex-1 rounded-full border border-[var(--busuu-line)] bg-white px-4 py-2.5 text-sm font-bold text-[var(--busuu-ink)] transition hover:bg-[var(--busuu-mint)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--busuu-green)] disabled:opacity-50"
              >
                {tCommon('cancel')}
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="inline-flex flex-1 items-center justify-center rounded-full border border-[var(--busuu-green-dark)] bg-[var(--busuu-green)] px-4 py-2.5 text-sm font-bold text-white shadow-[0_3px_0_var(--busuu-green-dark)] transition hover:bg-[var(--busuu-green-dark)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--busuu-green)] focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" aria-busy={isLoading}
              >
                {isLoading ? (
                  <span className="inline-flex items-center">
                    <LoaderCircle className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
                    {t('sending')}
                  </span>
                ) : (
                  <><Send className="me-2 h-4 w-4" aria-hidden="true" />{t('send')}</>
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
