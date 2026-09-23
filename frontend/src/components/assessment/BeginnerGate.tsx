'use client'

import { useTranslations } from 'next-intl'

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
  const tLang = useTranslations('targetLanguages')

  return (
    <div className="flex min-h-[60vh] items-center justify-center p-4 sm:p-6">
      <div className="w-full max-w-xl overflow-hidden rounded-[30px] border-2 border-[var(--juba-lilac)] bg-white shadow-[0_22px_55px_rgba(61,42,130,0.12)]">
        <div className="flex items-center gap-3 border-b-2 border-[var(--juba-lilac)] bg-[var(--juba-lilac)]/40 px-6 py-4">
          <span className="text-xs text-[var(--juba-muted)]">●</span>
          <span className="text-xs text-[var(--juba-muted)] font-semibold tracking-[0.12em] uppercase">
            {t('step1')}
          </span>
        </div>
        <div className="space-y-7 p-6 sm:p-8">
          <div className="space-y-3 text-center">
            <p className="text-2xl font-extrabold tracking-tight text-[var(--juba-text)]">
              {t('studiedBefore', { language: tLang(languageCode) })}
            </p>
            <p className="text-xs text-[var(--juba-muted)] font-mono">
              {t('studiedBeforeHint')}
            </p>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <button
              onClick={onBeginner}
              className="border-[var(--juba-border)] text-[var(--juba-muted)] hover:border-[var(--juba-border)]-2 hover:text-fl-fg w-full border px-5 py-4 text-left font-mono text-xs tracking-widest uppercase transition-colors"
            >
              <span className="text-[var(--juba-muted)] mr-3">○</span>
              {t('beginnerOption')}
              <span className="text-xs text-[var(--juba-muted)] mt-1 ml-6 block normal-case">
                {t('beginnerOptionHint')}
              </span>
            </button>
            <button
              onClick={onHasExperience}
              className="bg-[var(--juba-violet)] text-white hover:bg-[var(--juba-violet-dark)] w-full px-5 py-4 text-left font-mono text-xs font-bold tracking-widest uppercase transition-colors"
            >
              <span className="mr-3">●</span>
              {t('hasExperienceOption')}
              <span className="text-fl-hint mt-1 ml-6 block font-normal normal-case opacity-70">
                {t('hasExperienceOptionHint')}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
