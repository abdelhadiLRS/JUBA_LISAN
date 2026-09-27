import Link from 'next/link'
import { BookOpen, MessageSquare, Mic, Headphones, Layers, TrendingUp, Sparkles } from 'lucide-react'

interface BentoFeaturesProps { t: (key: string) => string }

const cards = [
  { key: 'feature1', icon: BookOpen, art: 'ASSESS', tone: 'green', href: '/assessment' },
  { key: 'feature2', icon: MessageSquare, art: 'AI', tone: 'yellow', href: '/chat' },
  { key: 'feature3', icon: Mic, art: 'VOICE', tone: 'blue', href: '/conversation' },
  { key: 'feature4', icon: Headphones, art: 'LISTEN', tone: 'purple', href: '/dashboard' },
  { key: 'feature6', icon: Layers, art: 'REVIEW', tone: 'coral', href: '/dashboard' },
  { key: 'feature8', icon: TrendingUp, art: 'PROGRESS', tone: 'mint', href: '/dashboard' },
]

export function BentoFeatures({ t }: BentoFeaturesProps) {
  return (
    <section className="juba-funfluent-features juba-jl-bento scroll-mt-24 py-20 sm:py-24">
      <style>{".juba-jl-bento{background:#fff;color:#242424;font-family:'Nunito Sans','Noto Sans Arabic',system-ui,sans-serif}.juba-jl-bento .juba-ff-section-head{text-align:center;max-width:760px;margin:0 auto 34px}.juba-jl-bento .juba-ff-section-tag{color:#46a302;font-weight:900}.juba-jl-bento .juba-ff-section-head h2{color:#242424;font-weight:950;letter-spacing:-.06em}.juba-jl-bento .juba-ff-section-head p{color:#777}.juba-jl-bento .juba-ff-feature-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.juba-jl-bento .juba-ff-feature-card{position:relative;border:2px solid #e5e5e5!important;border-radius:20px!important;background:#fff!important;color:#242424!important;box-shadow:0 4px 0 rgba(0,0,0,.06)!important;padding:22px!important;min-height:260px}.juba-jl-bento .juba-ff-feature-card:before{display:none!important}.juba-jl-bento .juba-ff-feature-art{height:70px;border-radius:16px;background:#efffe6!important;color:#46a302!important;display:grid;place-items:center;font-weight:950;letter-spacing:.12em}.juba-jl-bento .tone-yellow .juba-ff-feature-art{background:#fff8d9!important;color:#a97800!important}.juba-jl-bento .tone-blue .juba-ff-feature-art{background:#eaf8ff!important;color:#087fae!important}.juba-jl-bento .tone-purple .juba-ff-feature-art,.juba-jl-bento .tone-coral .juba-ff-feature-art,.juba-jl-bento .tone-mint .juba-ff-feature-art{background:#efffe6!important;color:#46a302!important}.juba-jl-bento .juba-ff-feature-icon{color:#46a302!important;background:#fff;border:2px solid #e5e5e5;border-radius:12px;width:42px;height:42px;display:grid;place-items:center;margin:16px 0 10px}.juba-jl-bento .juba-ff-feature-card h3{color:#242424!important;font-weight:900}.juba-jl-bento .juba-ff-feature-card p{color:#777!important;line-height:1.65}.juba-jl-bento .juba-ff-feature-link{color:#46a302!important;font-weight:900}@media(max-width:900px){.juba-jl-bento .juba-ff-feature-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:620px){.juba-jl-bento .juba-ff-feature-grid{grid-template-columns:1fr}}"}</style>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="juba-ff-section-head">
          <span className="juba-ff-section-tag"><Sparkles className="mr-1 inline h-3.5 w-3.5" />{t('featureSectionLabel')}</span>
          <h2>{t('bentoTitle')}</h2>
          <p>{t('bentoSubtitle')}</p>
        </div>
        <div className="juba-ff-feature-grid">
          {cards.map(({ key, icon: Icon, art, tone, href }) => (
            <article key={key} className={`juba-ff-feature-card tone-${tone}`}>
              <div className="juba-ff-feature-art" aria-hidden="true"><span>{art}</span></div>
              <div className="juba-ff-feature-icon"><Icon className="h-5 w-5" /></div>
              <h3>{t(`${key}Title`)}</h3>
              <p>{t(`${key}Desc`)}</p>
              <Link href={href} className="juba-ff-feature-link">{t('openInJuba')} <span aria-hidden="true">→</span></Link>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
