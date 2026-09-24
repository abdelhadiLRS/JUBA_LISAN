import Link from 'next/link'
import { Globe2, Sparkles } from 'lucide-react'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

interface LanguageShowcaseProps { t: (key: string) => string }

export function LanguageShowcase({ t }: LanguageShowcaseProps) {
  return (
    <section id="languages" className="juba-funfluent-languages scroll-mt-24 py-20 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="juba-ff-section-head">
          <span className="juba-ff-section-tag"><Globe2 className="mr-1 inline h-3.5 w-3.5" />Configured language catalog</span>
          <h2>{t('languagesTitle')}</h2>
          <p>These are the target languages currently defined by JUBA LISAN, including their scripts and language-learning text capabilities.</p>
        </div>
        <div className="juba-ff-language-cloud">
          {SUPPORTED_TARGET_LANGUAGES.map((language, i) => (
            <article key={language.code} className="juba-ff-language-card">
              <img src={language.flagPath} alt="" className="juba-ff-language-flag object-cover" />
              <div>
                <strong>{language.nameEn}</strong>
                <span>{language.code} · {language.iso639.toUpperCase()}</span>
                <small>{language.script === 'latin' ? 'Latin script' : language.script.replaceAll('-', ' · ')}</small>
              </div>
            </article>
          ))}
        </div>
        <div className="mt-10 text-center">
          <Link href="/dashboard" className="juba-ff-primary">Manage your languages <span aria-hidden="true">→</span></Link>
        </div>
      </div>
    </section>
  )
}
