import Link from 'next/link'
import { Mic, Volume2, Sparkles, User, Bot, Circle, ArrowRight, MessageSquare } from 'lucide-react'

interface AiConversationShowcaseProps { t: (key: string) => string }

export function AiConversationShowcase({ t }: AiConversationShowcaseProps) {
  return (
    <section id="demo" className="juba-funfluent-demo scroll-mt-24 py-20 sm:py-24 relative overflow-hidden">
      <div className="juba-ff-demo-cloud cloud-a" aria-hidden="true" />
      <div className="juba-ff-demo-cloud cloud-b" aria-hidden="true" />
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="juba-ff-demo-intro">
          <span className="juba-ff-section-tag"><Sparkles className="mr-1 inline h-3.5 w-3.5" />JUBA LISAN AI practice</span>
          <h2>{t('showcaseTitle')}</h2>
          <p>{t('showcaseSubtitle')}</p>
        </div>
        <div className="juba-ff-chat-card" aria-label="JUBA LISAN AI tutor preview">
          <div className="juba-ff-chat-top">
            <div className="juba-ff-avatar"><Bot className="h-6 w-6" /><i /></div>
            <div><strong>JUBA AI Tutor</strong><span><Circle className="mr-1 inline h-2 w-2 fill-current" />Available in the app</span></div>
            <span className="juba-ff-live-pill">JUBA AI</span>
          </div>
          <div className="juba-ff-chat-body">
            <div className="juba-ff-chat-message user"><span>{t('showcaseUserMsg')}</span><User /></div>
            <div className="juba-ff-chat-message ai"><Bot /><span>{t('showcaseAiMsg')}<em><Volume2 /> Audio reply</em></span></div>
          </div>
          <div className="juba-ff-chat-controls">
            <span><Mic /> Voice practice</span><span className="hidden sm:inline">• Real conversation workflow</span>
            <div className="flex gap-2">
              <Link href="/chat" className="juba-ff-demo-action"><MessageSquare /> Open AI Tutor <ArrowRight /></Link>
              <Link href="/conversation" className="juba-ff-demo-action"><Mic /> Start conversation <ArrowRight /></Link>
            </div>
          </div>
        </div>
        <p className="juba-ff-demo-note mt-5 text-center text-xs leading-relaxed">The conversation shown above is an illustrative preview; the buttons open the real JUBA LISAN AI workflows.</p>
      </div>
    </section>
  )
}
