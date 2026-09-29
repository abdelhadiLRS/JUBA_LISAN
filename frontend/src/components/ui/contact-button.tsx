'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { MessageCircle } from 'lucide-react'
import { ContactFormModal } from '@/components/ui/contact-form-modal'

export function ContactButton() {
  const t = useTranslations('landing')
  const [open, setOpen] = useState(false)

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="inline-flex w-full items-center gap-2 rounded-xl border border-transparent px-2.5 py-1.5 text-start text-sm font-semibold text-[var(--busuu-muted)] transition hover:border-[var(--busuu-line)] hover:bg-[var(--busuu-mint)] hover:text-[var(--busuu-ink)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--busuu-green)] focus-visible:ring-offset-2"
      >
        <MessageCircle className="h-4 w-4 shrink-0" aria-hidden="true" />
        {t('contact')}
      </button>
      <ContactFormModal open={open} onClose={() => setOpen(false)} />
    </>
  )
}
