import { Mic, Volume2, Sparkles, User, Bot, Circle } from 'lucide-react'

interface AiConversationShowcaseProps { t: (key: string) => string }

export function AiConversationShowcase({ t }: AiConversationShowcaseProps) {
  return (
    <section id="demo" className="juba-funfluent-demo scroll-mt-24 py-20 sm:py-24 relative overflow-hidden">
      <div className="juba-ff-demo-cloud cloud-a" aria-hidden="true" />
      <div className="juba-ff-demo-cloud cloud-b" aria-hidden="true" />
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="juba-ff-demo-intro">
          <span className="juba-ff-section-tag"><Sparkles className="mr-1 inline h-3.5 w-3.5" />Meet your AI tutor</span>
          <h2>{t('showcaseTitle')}</h2>
          <p>{t('showcaseSubtitle')}</p>
        </div>
        <div className="juba-ff-chat-card">
          <div className="juba-ff-chat-top">
            <div className="juba-ff-avatar"><Bot className="h-6 w-6" /><i /></div>
            <div><strong>JUBA AI Tutor</strong><span><Circle className="mr-1 inline h-2 w-2 fill-current" />B2 · Ready to speak</span></div>
            <span className="juba-ff-live-pill">● LIVE</span>
          </div>
          <div className="juba-ff-chat-body">
            <div className="juba-ff-chat-message user"><span>{t('showcaseUserMsg')}</span><User /></div>
            <div className="juba-ff-chat-message ai"><Bot /><span>{t('showcaseAiMsg')}<em><Volume2 /> 00:04</em></span></div>
          </div>
          <div className="juba-ff-chat-controls">
            <span><Mic /> {t('showcaseMicActive')}</span>
            <button><Mic /> Hold to speak</button>
          </div>
        </div>
      </div>
    </section>
  )
}
