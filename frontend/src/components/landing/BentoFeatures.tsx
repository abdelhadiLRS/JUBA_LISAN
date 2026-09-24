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
    <section className="juba-funfluent-features scroll-mt-24 py-20 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="juba-ff-section-head">
          <span className="juba-ff-section-tag"><Sparkles className="mr-1 inline h-3.5 w-3.5" />Everything in one place</span>
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
              <Link href={href} className="juba-ff-feature-link">Open in JUBA LISAN <span aria-hidden="true">→</span></Link>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
