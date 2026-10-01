'use client'

import { useEffect, useEffectEvent, useId, useRef } from 'react'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'


interface ConfirmDialogProps {
  open: boolean
  title: string
  message: string
  confirmLabel?: string
  cancelLabel?: string
  danger?: boolean
  confirming?: boolean
  error?: string
  onConfirm: () => void
  onCancel: () => void
}

export function ConfirmDialog({
  open,
  title,
  message,
  confirmLabel = 'Confirm',
  cancelLabel,
  danger = false,
  confirming = false,
  error,
  onConfirm,
  onCancel,
}: ConfirmDialogProps) {
  const tCommon = useTranslations('common')
  const titleId = useId()
  const descriptionId = useId()
  const cancelRef = useRef<HTMLButtonElement>(null)
  const dialogRef = useRef<HTMLDivElement>(null)
  const cancelIfIdle = useEffectEvent(() => {
    if (!confirming) onCancel()
  })
  useEffect(() => {
    if (!open) return
    const opener = document.activeElement as HTMLElement | null
    cancelRef.current?.focus()
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') cancelIfIdle()
      if (e.key !== 'Tab') return
      const controls = dialogRef.current?.querySelectorAll<HTMLElement>(
        'button:not(:disabled), [href], input:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"])'
      )
      if (!controls?.length) {
        e.preventDefault()
        return
      }
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
    return () => {
      window.removeEventListener('keydown', onKey)
      opener?.focus()
    }
  }, [open])

  if (!open) return null

  return (
    <div
      className="fixed inset-0 z-[200] flex items-center justify-center p-4"
      style={{
        backgroundColor: 'color-mix(in srgb, var(--duo-ink) 55%, transparent)',
        backdropFilter: 'blur(8px)',
      }}
      onClick={() => !confirming && onCancel()}
    >
      <div
        ref={dialogRef}
        className="w-full max-w-sm overflow-hidden rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] shadow-sm"
        onClick={(e) => e.stopPropagation()}
        role="alertdialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={descriptionId}
      >
        <div className="flex items-center gap-3 border-b border-[var(--duo-line)] bg-[var(--duo-card)] px-6 py-4">
          <span
            className={`flex h-8 w-8 items-center justify-center rounded-full text-sm ${danger ? 'bg-[color-mix(in_srgb,var(--duo-red)_12%,var(--duo-card))] text-[var(--duo-red)]' : 'bg-[var(--duo-yellow)] text-[var(--duo-green-dark)]'}`}
            aria-hidden="true"
          >
            {danger ? <i className="ti ti-alert-triangle icon" aria-hidden="true" /> : <i className="ti ti-circle-check icon" aria-hidden="true" />}
          </span>
          <span id={titleId} className="text-sm font-semibold tracking-tight text-[var(--duo-ink)]">
            {title}
          </span>
        </div>

        <div className="px-6 py-6">
          <p id={descriptionId} className="text-sm leading-6 text-[var(--duo-muted)]">
            {message}
          </p>
          {error && (
            <p role="alert" className="mt-3 text-sm leading-5 text-[var(--duo-red)]">
              {error}
            </p>
          )}
        </div>

        <div className="flex gap-3 border-t border-[var(--duo-line)] bg-[var(--duo-card)] px-6 py-4">
          <button
            type="button"
            ref={cancelRef}
            onClick={onCancel}
            disabled={confirming}
            className="flex-1 rounded-[10px] border border-[var(--duo-line)] px-4 py-2.5 text-sm font-semibold text-[var(--duo-muted)] transition-colors hover:border-[var(--duo-green)] hover:text-[var(--duo-green-dark)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-green)] focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {cancelLabel ?? tCommon('cancel')}
          </button>
          <button
            type="button"
            onClick={onConfirm}
            disabled={confirming}
            aria-busy={confirming}
            className={`flex-1 rounded-[10px] border border-transparent px-4 py-2.5 text-sm font-semibold shadow-sm transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${
              danger
                ? 'bg-[var(--duo-red)] text-white hover:opacity-90 focus-visible:ring-[var(--duo-red)]'
                : 'bg-[var(--duo-green-dark)] text-white hover:opacity-90 focus-visible:ring-[var(--duo-green)]'
            }`}
          >
            {confirming ? <span className="inline-flex items-center gap-2"><Loader2 className="size-4 animate-spin" />{confirmLabel}</span> : confirmLabel}
          </button>
        </div>
      </div>
    </div>
  )
}
