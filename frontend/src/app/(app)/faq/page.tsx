'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { useAuthStore } from '@/store/auth'

interface FAQItem {
  q: string
  a: React.ReactNode
}

export default function FAQPage() {
  const t = useTranslations('faq')
  const [open, setOpen] = useState<number | null>(null)
  const isAdmin = useAuthStore((s) => s.user?.role === 'admin')

  const strong = (chunks: React.ReactNode) => (
    <strong className="text-[var(--duo-ink)]">{chunks}</strong>
  )
  const code = (chunks: React.ReactNode) => (
    <code className="text-[var(--duo-ink)] bg-[var(--duo-bg)] px-1">{chunks}</code>
  )
  const adminLink = (chunks: React.ReactNode) => (
    <Link href="/admin/users" className="text-[var(--duo-ink)] underline underline-offset-2">
      {chunks}
    </Link>
  )
  const settingsLink = (chunks: React.ReactNode) => (
    <Link href="/settings" className="text-[var(--duo-ink)] underline underline-offset-2">
      {chunks}
    </Link>
  )
  const feedbackLink = (chunks: React.ReactNode) => (
    <Link href="/feedback" className="text-[var(--duo-ink)] underline underline-offset-2">
      {chunks}
    </Link>
  )

  const workflowSteps = [
    t('workflowStep1'), t('workflowStep2'), t('workflowStep3'),
    t('workflowStep4'), t('workflowStep5'), t('workflowStep6'),
  ]

  const providers: [string, string][] = [
    ['ollama', t('provider_ollama')],
    ['openai', t('provider_openai')],
    ['anthropic', t('provider_anthropic')],
    ['deepseek', t('provider_deepseek')],
  ]

  const faqs: FAQItem[] = (() => {
    const items: FAQItem[] = [
      { q: t('q_start'), a: t.rich('a_start', { strong }) },
      { q: t('q_language'), a: t('a_language') },
      {
        q: t('q_workflow'),
        a: (
          <ol className="list-none space-y-1">
            {workflowSteps.map((step, i) => (
              <li key={i} className="flex items-start gap-3">
                <span className="text-[var(--duo-muted)] mt-0.5 shrink-0 font-sans">{i + 1}.</span>
                <span>{step}</span>
              </li>
            ))}
          </ol>
        ),
      },
      { q: t('q_assessment'), a: t('a_assessment') },
      { q: t('q_studyPlan'), a: t.rich('a_studyPlan', { strong }) },
      { q: t('q_resources'), a: t.rich('a_resources', { strong }) },
      { q: t('q_flashcards'), a: t.rich('a_flashcards', { strong }) },
      { q: t('q_vocabulary'), a: t.rich('a_vocabulary', { strong }) },
      { q: t('q_tutor'), a: t('a_tutor') },
      { q: t('q_voice'), a: t.rich('a_voice', { strong }) },
      { q: t('q_listening'), a: t.rich('a_listening', { strong }) },
      { q: t('q_reading'), a: t.rich('a_reading', { strong }) },
      { q: t('q_feedback'), a: t.rich('a_feedback', { feedbackLink }) },
      { q: t('q_password'), a: t.rich('a_password', { settingsLink }) },
      { q: t('q_uiLanguage'), a: t.rich('a_uiLanguage', { settingsLink, strong }) },
    ]

    if (isAdmin) {
      items.push(
        {
          q: t('q_providers'),
          a: (
            <>
              {t.rich('a_providers_intro', { code })}
              <ul className="mt-2 list-none space-y-1">
                {providers.map(([name, desc]) => (
                  <li key={name} className="flex items-start gap-2">
                    <code className="text-[var(--duo-muted)] shrink-0">{name}</code>
                    <span className="text-[var(--duo-muted)]">— {desc}</span>
                  </li>
                ))}
              </ul>
            </>
          ),
        },
        { q: t('q_invite'), a: t.rich('a_invite', { adminLink, code }) }
      )
    }
    return items
  })()

  return (
    <div className="w-full space-y-6 px-4 py-5 sm:px-6 sm:py-6 lg:px-8">
      <section className="juba-reference-hero min-h-[112px] px-5 py-5 sm:px-6 sm:py-6">
        <div className="max-w-3xl space-y-2">
          <p className="juba-eyebrow">{t('title')}</p>
          <h1 className="text-[30px] font-extrabold tracking-tight text-[var(--duo-ink)] sm:text-3xl">
            {t('subtitle')}
          </h1>
        </div>
      </section>

      <section className="juba-reference-section juba-reference-list-card overflow-hidden">
        <div className="flex items-center gap-2 border-b border-[var(--duo-line)] bg-white px-5 py-3">
          <span className="text-sm font-bold text-[var(--duo-green-dark)]">●</span>
          <span className="font-sans text-[10px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">
            {t('title')}
          </span>
        </div>
        <div className="juba-faq-list">
        {faqs.map((item, i) => (
          <div key={i} className={i < faqs.length - 1 ? 'border-[var(--duo-line)] border-b' : ''}>
            <button
              onClick={() => setOpen(open === i ? null : i)}
              className="flex w-full items-center justify-between px-5 py-4 text-left transition-colors hover:bg-[var(--duo-bg)] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[var(--duo-green-dark)]/30"
            >
              <span className="text-[var(--duo-ink)] pe-4 font-sans text-sm font-semibold tracking-tight">{item.q}</span>
              <span className="text-[var(--duo-muted)] shrink-0 font-sans text-sm">{open === i ? '−' : '+'}</span>
            </button>
            {open === i && (
              <div className="border-t border-[var(--duo-line)] bg-[var(--duo-bg)] px-5 pt-4 pb-5 font-sans text-sm leading-relaxed text-[var(--duo-muted)]">
                {item.a}
              </div>
            )}
          </div>
        ))}
        </div>
      </section>
    </div>
  )
}
