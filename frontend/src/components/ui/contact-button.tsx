'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { ContactFormModal } from '@/components/ui/contact-form-modal'

export function ContactButton() {
  const t = useTranslations('landing')
  const [open, setOpen] = useState(false)

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="w-full rounded-lg px-2 py-1.5 text-left text-sm font-medium text-[var(--juba-muted)] transition-colors hover:bg-[var(--juba-primary-soft)] hover:text-[var(--juba-text)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-primary)]"
      >
        {t('contact')}
      </button>
      <ContactFormModal open={open} onClose={() => setOpen(false)} />
    </>
  )
}
