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
    <div className="flex min-h-[60vh] items-center justify-center bg-[#f4f4f2] p-4 sm:p-6">
      <div className="w-full max-w-xl overflow-hidden rounded-[26px] border border-[rgba(7,7,9,.08)] bg-white shadow-[0_12px_30px_rgba(43,45,90,.055)]">
        <div className="flex items-center gap-3 border-b border-[rgba(7,7,9,.07)] bg-[#f4f4f2] px-6 py-4">
          <span className="text-xs text-[rgba(32,33,39,.52)]">●</span>
          <span className="text-xs text-[rgba(32,33,39,.52)] font-semibold tracking-[0.12em] uppercase">
            {t('step1')}
          </span>
        </div>
        <div className="space-y-7 p-6 sm:p-8">
          <div className="space-y-3 text-center">
            <p className="text-2xl font-extrabold tracking-tight text-[#202127]">
              {t('studiedBefore', { language })}
            </p>
            <p className="text-xs text-[rgba(32,33,39,.52)] font-sans">
              {t('studiedBeforeHint')}
            </p>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <button
              type="button"
              onClick={onBeginner}
              className="w-full rounded-[16px] border border-[rgba(7,7,9,.08)] bg-[#f4f4f2] px-5 py-4 text-left font-sans text-xs uppercase tracking-widest text-[#202127] transition-all hover:border-[#5862e2] hover:bg-[#ededff] hover:text-[#373fb8] hover:shadow-[0_8px_18px_rgba(43,45,90,.05)]"
            >
              <span className="text-[rgba(32,33,39,.52)] mr-3">○</span>
              {t('beginnerOption')}
              <span className="text-xs text-[rgba(32,33,39,.52)] mt-1 ml-6 block normal-case">
                {t('beginnerOptionHint')}
              </span>
            </button>
            <button
              type="button"
              onClick={onHasExperience}
              className="w-full rounded-[16px] bg-[#5862e2] px-5 py-4 text-left font-sans text-xs font-bold uppercase tracking-widest text-white shadow-[0_8px_18px_rgba(88,98,226,.18)] transition-all hover:bg-[#373fb8] hover:shadow-[0_10px_22px_rgba(55,63,184,.2)]"
            >
              <span className="mr-3">●</span>
              {t('hasExperienceOption')}
              <span className="text-[rgba(32,33,39,.52)] mt-1 ml-6 block font-normal normal-case opacity-70">
                {t('hasExperienceOptionHint')}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
