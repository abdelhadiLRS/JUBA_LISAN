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
        className="inline-flex w-full items-center gap-2 rounded-xl border-2 border-transparent px-2.5 py-1.5 text-left text-sm font-medium text-[var(--juba-app-muted)] transition hover:border-[var(--juba-app-line)] hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-ink)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)]"
      >
        <MessageCircle className="h-4 w-4 shrink-0" aria-hidden="true" />
        {t('contact')}
      </button>
      <ContactFormModal open={open} onClose={() => setOpen(false)} />
    </>
  )
}
