import Link from 'next/link'
import { Globe2, Sparkles } from 'lucide-react'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

interface LanguageShowcaseProps { t: (key: string) => string }

export function LanguageShowcase({ t }: LanguageShowcaseProps) {
  return (
    <section id="languages" className="juba-funfluent-languages juba-jl-languages scroll-mt-24 py-20 sm:py-24">
      <style>{".juba-jl-languages{background:#fff;color:#242424;font-family:'Nunito Sans','Noto Sans Arabic',system-ui,sans-serif}.juba-jl-languages .juba-ff-section-head{text-align:center;max-width:760px;margin:0 auto 34px}.juba-jl-languages .juba-ff-section-tag{color:#46a302;font-weight:900}.juba-jl-languages .juba-ff-section-head h2{color:#242424;font-weight:950;letter-spacing:-.06em}.juba-jl-languages .juba-ff-section-head p{color:#777}.juba-jl-languages .juba-ff-language-cloud{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.juba-jl-languages .juba-ff-language-card{border:2px solid #e5e5e5!important;border-radius:18px!important;background:#fff!important;box-shadow:0 3px 0 rgba(0,0,0,.05)!important;padding:18px!important}.juba-jl-languages .juba-ff-language-card:hover{border-color:#58cc02!important;background:#efffe6!important}.juba-jl-languages .juba-ff-language-card strong{display:block;color:#242424;font-weight:900}.juba-jl-languages .juba-ff-language-card span,.juba-jl-languages .juba-ff-language-card small{display:block;color:#777;margin-top:4px}.juba-jl-languages .juba-ff-primary{display:inline-flex;align-items:center;gap:8px;min-height:46px;padding:10px 16px;border:2px solid #46a302;border-radius:14px;background:#58cc02;color:#fff;font-weight:900;box-shadow:0 4px 0 #46a302}@media(max-width:900px){.juba-jl-languages .juba-ff-language-cloud{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.juba-jl-languages .juba-ff-language-cloud{grid-template-columns:1fr}}"}</style>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="juba-ff-section-head">
          <span className="juba-ff-section-tag"><Globe2 className="mr-1 inline h-3.5 w-3.5" />{t('languageCatalogLabel')}</span>
          <h2>{t('languagesTitle')}</h2>
          <p>{t('languageCatalogDescription')}</p>
        </div>
        <div className="juba-ff-language-cloud">
          {SUPPORTED_TARGET_LANGUAGES.map((language) => (
            <article key={language.code} className="juba-ff-language-card">
              <div>
                <strong>{language.nameEn}</strong>
                <span>{language.code} · {language.iso639.toUpperCase()}</span>
                <small>{language.script === 'latin' ? t('latinScript') : language.script.replaceAll('-', ' · ')}</small>
              </div>
            </article>
          ))}
        </div>
        <div className="mt-10 text-center">
          <Link href="/dashboard" className="juba-ff-primary">{t('manageLanguages')} <span aria-hidden="true">→</span></Link>
        </div>
      </div>
    </section>
  )
}
