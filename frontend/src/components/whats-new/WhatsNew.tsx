'use client'

import { useState, useEffect, useCallback, useMemo, useRef } from 'react'
import { useTranslations, useMessages } from 'next-intl'
import { CircleDot, Sparkles } from 'lucide-react'

const WHATS_NEW_VERSION = 'v1.8.44'
const STORAGE_KEY = `fl_whats_new_seen_${WHATS_NEW_VERSION}`
const TOUR_KEY = 'fl_tour_done'

type WhatsNewEntry = {
  label: string
  desc: string
}

function isWhatsNewEntry(value: unknown): value is WhatsNewEntry {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false
  const entry = value as Record<string, unknown>
  return typeof entry.label === 'string' && typeof entry.desc === 'string'
}

export default function WhatsNew() {
  const t = useTranslations('whatsNew')
  const messages = useMessages()
  const [visible, setVisible] = useState(false)
  const closeButtonRef = useRef<HTMLButtonElement>(null)
  const previousFocusRef = useRef<HTMLElement | null>(null)

  // Derive entries from raw messages and ignore malformed translation payloads.
  const entries = useMemo(() => {
    const nsValue = (messages as Record<string, unknown>)['whatsNew']
    if (!nsValue || typeof nsValue !== 'object' || Array.isArray(nsValue)) {
      return []
    }

    const ns = nsValue as Record<string, unknown>
    return Object.keys(ns)
      .filter((k) => /^entry\d+$/.test(k))
      .sort((a, b) => parseInt(a.slice(5)) - parseInt(b.slice(5)))
      .flatMap((key) => {
        const entry = ns[key]
        return isWhatsNewEntry(entry)
          ? [{ key, label: entry.label, desc: entry.desc }]
          : []
      })
  }, [messages])

  useEffect(() => {
    const tourDone = localStorage.getItem(TOUR_KEY)
    const seen = localStorage.getItem(STORAGE_KEY)
    if (tourDone && !seen) {
      setVisible(true)
    }
  }, [])

  const dismiss = useCallback(() => {
    localStorage.setItem(STORAGE_KEY, '1')
    setVisible(false)
  }, [])

  useEffect(() => {
    if (!visible) return
    previousFocusRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null
    closeButtonRef.current?.focus()
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') dismiss()
    }
    window.addEventListener('keydown', onKeyDown)
    return () => {
      window.removeEventListener('keydown', onKeyDown)
      previousFocusRef.current?.focus()
      previousFocusRef.current = null
    }
  }, [visible, dismiss])

  if (!visible) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" role="presentation">
      {/* Backdrop */}
      <div
        className="bg-[color-mix(in_srgb,var(--duo-ink)_55%,transparent)] absolute inset-0 backdrop-blur-sm"
        onClick={dismiss}
        aria-hidden="true"
      />

      {/* Modal */}
      <div className="relative z-10 w-full max-w-md rounded-[20px] border-2 border-[var(--duo-line)] bg-[var(--duo-card)] text-[var(--duo-ink)] shadow-[0_6px_0_var(--duo-line)]" role="dialog" aria-modal="true" aria-labelledby="whats-new-title">
        {/* Header */}
        <div className="flex items-center gap-3 border-b-2 border-[var(--duo-line)] px-5 pt-5 pb-4">
          <Sparkles
            className="text-[var(--duo-purple)] h-[1.125rem] w-[1.125rem]"
            aria-hidden="true"
          />
          <div>
            <p id="whats-new-title" className="text-xs text-[var(--duo-muted)] font-bold tracking-widest uppercase">
              {t('title')}
            </p>
            <p className="text-[10px] text-[var(--duo-muted)] font-bold tracking-widest">
              {t('version')}
            </p>
          </div>
        </div>

        {/* Entries */}
        <div className="max-h-[50vh] space-y-5 overflow-y-auto px-5 py-5">
          {entries.map((entry) => (
            <div key={entry.key} className="flex gap-3">
              <CircleDot
                className="text-[var(--duo-purple)] mt-0.5 h-3.5 w-3.5 shrink-0"
                aria-hidden="true"
              />
              <div>
                <p className="text-fl-label text-xs text-[var(--duo-muted)] mb-1 font-bold tracking-widest uppercase">
                  {entry.label}
                </p>
                <p className="text-[var(--duo-muted)] text-xs leading-relaxed">
                  {t.rich(`${entry.key}.desc`, {
                    bold: (chunks) => (
                      <strong className="text-[var(--duo-ink)] font-semibold">
                        {chunks}
                      </strong>
                    ),
                  })}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="flex justify-end border-t-2 border-[var(--duo-line)] px-5 pt-3 pb-5">
          <button
            ref={closeButtonRef}
            type="button"
            onClick={dismiss}
            className="text-xs rounded-xl bg-[var(--duo-green)] text-white hover:bg-[var(--duo-green-dark)] px-5 py-2.5 font-bold tracking-widest uppercase shadow-[0_3px_0_var(--duo-green-dark)] transition-colors"
          >
            {t('cta')} →
          </button>
        </div>
      </div>
    </div>
  )
}
