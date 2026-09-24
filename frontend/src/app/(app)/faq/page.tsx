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
    <strong className="text-[var(--juba-app-ink)]">{chunks}</strong>
  )
  const code = (chunks: React.ReactNode) => (
    <code className="text-[var(--juba-app-ink)] bg-[var(--juba-app-surface)]-2 px-1">{chunks}</code>
  )
  const adminLink = (chunks: React.ReactNode) => (
    <Link
      href="/admin/users"
      className="text-[var(--juba-app-ink)] underline underline-offset-2"
    >
      {chunks}
    </Link>
  )
  const settingsLink = (chunks: React.ReactNode) => (
    <Link href="/settings" className="text-[var(--juba-app-ink)] underline underline-offset-2">
      {chunks}
    </Link>
  )
  const feedbackLink = (chunks: React.ReactNode) => (
    <Link href="/feedback" className="text-[var(--juba-app-ink)] underline underline-offset-2">
      {chunks}
    </Link>
  )

  const workflowSteps = [
    t('workflowStep1'),
    t('workflowStep2'),
    t('workflowStep3'),
    t('workflowStep4'),
    t('workflowStep5'),
    t('workflowStep6'),
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
                <span className="text-fl-label text-[var(--juba-app-muted)] mt-0.5 shrink-0 font-sans">
                  {i + 1}.
                </span>
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
      {
        q: t('q_uiLanguage'),
        a: t.rich('a_uiLanguage', { settingsLink, strong }),
      },
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
                    <code className="text-[var(--juba-app-muted)] shrink-0">{name}</code>
                    <span className="text-[var(--juba-app-muted)]">— {desc}</span>
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
    <div className="juba-faq-shell mx-auto max-w-4xl space-y-6 p-4 sm:p-6">
      {/* Header */}
      <div className="border-[var(--juba-app-line)] mb-8 border-b pb-4">
        <p className="text-fl-label text-[var(--juba-app-muted)] mb-1 font-sans tracking-widest uppercase">
          {t('title')}
        </p>
        <h1 className="text-[var(--juba-app-ink)] font-sans text-2xl font-bold tracking-tight">
          {t('subtitle')}
        </h1>
      </div>

      {/* Accordion */}
      <div className="juba-card border-[var(--juba-app-line)] border">
        {faqs.map((item, i) => (
          <div
            key={i}
            className={i < faqs.length - 1 ? 'border-[var(--juba-app-line)] border-b' : ''}
          >
            <button
              onClick={() => setOpen(open === i ? null : i)}
              className="juba-faq-question hover:bg-[var(--juba-app-surface)] flex w-full items-center justify-between px-5 py-4 text-left transition-colors"
            >
              <span className="text-[var(--juba-app-ink)] pr-4 font-sans text-sm font-semibold tracking-tight">
                {item.q}
              </span>
              <span className="text-[var(--juba-app-muted)] shrink-0 font-sans text-sm">
                {open === i ? '−' : '+'}
              </span>
            </button>
            {open === i && (
              <div className="juba-faq-answer text-[var(--juba-app-muted)] border-[var(--juba-app-line)] bg-[#fffdf8] border-t px-5 pt-4 pb-5 font-sans text-sm leading-relaxed">
                {item.a}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
