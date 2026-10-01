'use client'

import { useLocale, useTranslations } from 'next-intl'

interface Props {
  onBeginner: () => void
  onHasExperience: () => void
  languageCode: string
}

export default function BeginnerGate({
  onBeginner,
  onHasExperience,
  languageCode,
}: Props) {
  const t = useTranslations('assessment')
  const locale = useLocale()

  // Resolve the language name through the browser's CLDR data instead of
  // relying on a message namespace that may be absent in an older dev build.
  const language = (() => {
    try {
      return new Intl.DisplayNames([locale], { type: 'language' }).of(languageCode) ?? languageCode
    } catch {
      return languageCode
    }
  })()

  return (
    <div className="flex min-h-[60vh] items-center justify-center bg-[var(--duo-bg)] p-4 sm:p-6">
      <div className="w-full max-w-xl overflow-hidden rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] shadow-sm">
        <div className="flex items-center gap-3 border-b border-[var(--duo-line)] bg-[var(--duo-bg)] px-6 py-4">
          <span className="text-xs text-[var(--duo-muted)]">●</span>
          <span className="text-xs text-[var(--duo-muted)] font-semibold tracking-[0.12em] uppercase">
            {t('step1')}
          </span>
        </div>
        <div className="space-y-7 p-6 sm:p-8">
          <div className="space-y-3 text-center">
            <p className="text-2xl font-extrabold tracking-tight text-[var(--duo-ink)]">
              {t('studiedBefore', { language })}
            </p>
            <p className="text-xs text-[var(--duo-muted)] font-sans">
              {t('studiedBeforeHint')}
            </p>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <button
              type="button"
              onClick={onBeginner}
              className="w-full rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-bg)] px-5 py-4 text-left font-sans text-xs uppercase tracking-widest text-[var(--duo-ink)] transition-colors hover:border-[var(--duo-green)] hover:bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] hover:text-[var(--duo-green-dark)] "
            >
              <span className="text-[var(--duo-muted)] me-3">○</span>
              {t('beginnerOption')}
              <span className="text-xs text-[var(--duo-muted)] mt-1 ms-6 block normal-case">
                {t('beginnerOptionHint')}
              </span>
            </button>
            <button
              type="button"
              onClick={onHasExperience}
              className="w-full rounded-[10px] bg-[var(--duo-green)] px-5 py-4 text-left font-sans text-xs font-bold uppercase tracking-widest text-white shadow-sm transition-colors hover:bg-[var(--duo-green-dark)] "
            >
              <span className="me-3">●</span>
              {t('hasExperienceOption')}
              <span className="text-[var(--duo-muted)] mt-1 ms-6 block font-normal normal-case opacity-70">
                {t('hasExperienceOptionHint')}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
