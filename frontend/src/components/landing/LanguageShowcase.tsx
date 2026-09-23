import { Globe2, Sparkles } from 'lucide-react'

interface LanguageShowcaseProps { t: (key: string) => string }

const LANGUAGES = [
  ['en-US','English (US)','🇺🇸','Hello!'],['en-GB','English (UK)','🇬🇧','Hello!'],
  ['es-ES','Spanish','🇪🇸','¡Hola!'],['fr-FR','French','🇫🇷','Bonjour !'],
  ['de-DE','German','🇩🇪','Hallo!'],['it-IT','Italian','🇮🇹','Ciao!'],
  ['pt-PT','Portuguese','🇵🇹','Olá!'],['ja-JP','Japanese','🇯🇵','こんにちは！'],
  ['ko-KR','Korean','🇰🇷','안녕하세요!'],['zh-CN','Chinese','🇨🇳','你好！'],
]

export function LanguageShowcase({ t }: LanguageShowcaseProps) {
  return (
    <section id="languages" className="juba-funfluent-languages scroll-mt-24 py-20 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="juba-ff-section-head">
          <span className="juba-ff-section-tag"><Globe2 className="mr-1 inline h-3.5 w-3.5" />Global learning</span>
          <h2>{t('languagesTitle')}</h2>
          <p>{t('languagesSubtitle')}</p>
        </div>
        <div className="juba-ff-language-cloud">
          {LANGUAGES.map(([code,name,flag,greeting], i) => (
            <article key={code} className={`juba-ff-language-card lang-${i % 5}`}>
              <span className="juba-ff-language-flag">{flag}</span>
              <div><strong>{name}</strong><span>{greeting}</span></div>
              <small>{code}</small>
            </article>
          ))}
        </div>
        <div className="juba-ff-language-banner">
          <Sparkles className="h-6 w-6" />
          <span>Learn with real accents, natural phrases, and context—not isolated word lists.</span>
        </div>
      </div>
    </section>
  )
}
