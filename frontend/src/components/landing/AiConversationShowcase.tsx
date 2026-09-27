import Link from 'next/link'
import { Mic, Volume2, Sparkles, User, Bot, Circle, ArrowRight, MessageSquare } from 'lucide-react'

interface AiConversationShowcaseProps { t: (key: string) => string }

export function AiConversationShowcase({ t }: AiConversationShowcaseProps) {
  return (
    <section id="demo" className="juba-funfluent-demo juba-jl-ai-conversation scroll-mt-24 py-20 sm:py-24 relative overflow-hidden">
      <style>{".juba-jl-ai-conversation{background:#f7fff3;color:#242424;font-family:'Nunito Sans','Noto Sans Arabic',system-ui,sans-serif}.juba-jl-ai-conversation .juba-ff-demo-cloud{display:none}.juba-jl-ai-conversation .juba-ff-demo-intro{text-align:center;max-width:760px;margin:0 auto 34px}.juba-jl-ai-conversation .juba-ff-section-tag{display:inline-flex;align-items:center;gap:5px;color:#46a302;font-weight:900;font-size:12px;letter-spacing:.08em;text-transform:uppercase}.juba-jl-ai-conversation .juba-ff-demo-intro h2{margin:12px 0 10px;color:#242424;font-size:clamp(2.2rem,5vw,4.2rem);line-height:.98;font-weight:950;letter-spacing:-.06em}.juba-jl-ai-conversation .juba-ff-demo-intro p{color:#777;line-height:1.7}.juba-jl-ai-conversation .juba-ff-chat-card{max-width:920px;margin:0 auto;border:2px solid #e5e5e5;border-radius:24px;background:#fff;box-shadow:0 5px 0 rgba(0,0,0,.07);overflow:hidden}.juba-jl-ai-conversation .juba-ff-chat-top{display:flex;align-items:center;gap:12px;padding:18px 20px;border-bottom:2px solid #e5e5e5;background:#fff}.juba-jl-ai-conversation .juba-ff-avatar{display:grid;place-items:center;width:46px;height:46px;border-radius:50%;background:#efffe6;color:#46a302;position:relative}.juba-jl-ai-conversation .juba-ff-avatar i{position:absolute;right:1px;bottom:2px;width:10px;height:10px;border:2px solid #fff;border-radius:50%;background:#58cc02}.juba-jl-ai-conversation .juba-ff-live-pill{margin-left:auto!important;padding:7px 11px;border-radius:999px;background:#46a302!important;color:#fff!important;font-size:11px!important;font-weight:900!important;letter-spacing:.08em}.juba-jl-ai-conversation .juba-ff-chat-body{display:grid;gap:14px;padding:24px;background:#fbfbfb}.juba-jl-ai-conversation .juba-ff-chat-message{display:flex;align-items:flex-end;gap:10px;max-width:78%;font-weight:700;line-height:1.55}.juba-jl-ai-conversation .juba-ff-chat-message.user{margin-left:auto;flex-direction:row-reverse}.juba-jl-ai-conversation .juba-ff-chat-message span{padding:13px 16px;border:2px solid #e5e5e5;border-radius:17px;background:#fff;color:#242424;box-shadow:0 3px 0 rgba(0,0,0,.04)}.juba-jl-ai-conversation .juba-ff-chat-message.user span{border-color:#b9e9a0;background:#efffe6}.juba-jl-ai-conversation .juba-ff-chat-message svg{width:18px;height:18px;color:#46a302;flex:none}.juba-jl-ai-conversation .juba-ff-chat-message em{display:flex;align-items:center;gap:5px;margin-top:8px;color:#46a302;font-style:normal;font-size:12px}.juba-jl-ai-conversation .juba-ff-chat-controls{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:16px 20px;border-top:2px solid #e5e5e5;background:#fff;color:#777;font-size:12px;font-weight:800}.juba-jl-ai-conversation .juba-ff-chat-controls>div{margin-left:auto}.juba-jl-ai-conversation .juba-ff-demo-action{display:inline-flex;align-items:center;gap:7px;min-height:42px;padding:9px 13px;border:2px solid #46a302;border-radius:12px;background:#58cc02;color:#fff;font-weight:900;text-decoration:none;box-shadow:0 3px 0 #46a302}.juba-jl-ai-conversation .juba-ff-demo-action:hover{transform:translateY(1px);box-shadow:0 2px 0 #46a302}.juba-jl-ai-conversation .juba-ff-demo-note{color:#777!important}@media(max-width:640px){.juba-jl-ai-conversation .juba-ff-chat-body{padding:16px}.juba-jl-ai-conversation .juba-ff-chat-message{max-width:92%}.juba-jl-ai-conversation .juba-ff-chat-controls>div{margin-left:0;width:100%;display:grid;grid-template-columns:1fr}.juba-jl-ai-conversation .juba-ff-demo-action{justify-content:center}}"}</style>
      <div className="juba-ff-demo-cloud cloud-a" aria-hidden="true" />
      <div className="juba-ff-demo-cloud cloud-b" aria-hidden="true" />
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="juba-ff-demo-intro">
          <span className="juba-ff-section-tag"><Sparkles className="mr-1 inline h-3.5 w-3.5" />{t('aiPracticeLabel')}</span>
          <h2>{t('showcaseTitle')}</h2>
          <p>{t('showcaseSubtitle')}</p>
        </div>
        <div className="juba-ff-chat-card" aria-label={t('aiTutorPreviewLabel')}>
          <div className="juba-ff-chat-top">
            <div className="juba-ff-avatar"><Bot className="h-6 w-6" /><i /></div>
            <div><strong>JUBA AI Tutor</strong><span><Circle className="mr-1 inline h-2 w-2 fill-current" />{t('availableInApp')}</span></div>
            <span className="juba-ff-live-pill">JUBA AI</span>
          </div>
          <div className="juba-ff-chat-body">
            <div className="juba-ff-chat-message user"><span>{t('showcaseUserMsg')}</span><User /></div>
            <div className="juba-ff-chat-message ai"><Bot /><span>{t('showcaseAiMsg')}<em><Volume2 /> {t('audioReply')}</em></span></div>
          </div>
          <div className="juba-ff-chat-controls">
            <span><Mic /> {t('voicePractice')}</span><span className="hidden sm:inline">• {t('realConversationWorkflow')}</span>
            <div className="flex gap-2">
              <Link href="/chat" className="juba-ff-demo-action"><MessageSquare /> {t('openAiTutor')} <ArrowRight /></Link>
              <Link href="/conversation" className="juba-ff-demo-action"><Mic /> {t('startConversation')} <ArrowRight /></Link>
            </div>
          </div>
        </div>
        <p className="juba-ff-demo-note mt-5 text-center text-xs leading-relaxed">{t('demoNote')}</p>
      </div>
    </section>
  )
}
