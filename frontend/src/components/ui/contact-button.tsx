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
        className="inline-flex w-full items-center gap-2 rounded-[10px] border border-transparent px-2.5 py-1.5 text-start text-sm font-semibold text-[var(--duo-muted)] transition hover:border-[var(--duo-line)] hover:bg-[var(--duo-mint)] hover:text-[var(--duo-ink)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-green)] focus-visible:ring-offset-2"
      >
        <MessageCircle className="h-4 w-4 shrink-0" aria-hidden="true" />
        {t('contact')}
      </button>
      <ContactFormModal open={open} onClose={() => setOpen(false)} />
    </>
  )
}
