'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { CircleHelp, Plus, Minus } from 'lucide-react'
import { useAuthStore } from '@/store/auth'

interface FAQItem { q:string;a:React.ReactNode }
export default function FAQPage() {
  const t=useTranslations('faq')
  const [open,setOpen]=useState<number|null>(null)
  const isAdmin=useAuthStore(s=>s.user?.role==='admin')
  const strong=(chunks:React.ReactNode)=><strong className="font-semibold text-[var(--juba-ink)]">{chunks}</strong>
  const code=(chunks:React.ReactNode)=><code className="rounded bg-[var(--juba-soft)] px-1 text-[var(--juba-ink)]">{chunks}</code>
  const adminLink=(chunks:React.ReactNode)=><Link href="/admin/users" className="underline underline-offset-2">{chunks}</Link>
  const settingsLink=(chunks:React.ReactNode)=><Link href="/settings" className="underline underline-offset-2">{chunks}</Link>
  const feedbackLink=(chunks:React.ReactNode)=><Link href="/feedback" className="underline underline-offset-2">{chunks}</Link>
  const workflowSteps=[t('workflowStep1'),t('workflowStep2'),t('workflowStep3'),t('workflowStep4'),t('workflowStep5'),t('workflowStep6')]
  const providers:[string,string][]=[['ollama',t('provider_ollama')],['openai',t('provider_openai')],['anthropic',t('provider_anthropic')],['deepseek',t('provider_deepseek')]]
  const faqs:FAQItem[]=[
    {q:t('q_start'),a:t.rich('a_start',{strong})},{q:t('q_language'),a:t('a_language')},
    {q:t('q_workflow'),a:<ol className="space-y-2">{workflowSteps.map((step,index)=><li key={index} className="flex items-start gap-2"><span className="shrink-0">{index+1}.</span><span>{step}</span></li>)}</ol>},
    {q:t('q_assessment'),a:t('a_assessment')},{q:t('q_studyPlan'),a:t.rich('a_studyPlan',{strong})},{q:t('q_resources'),a:t.rich('a_resources',{strong})},{q:t('q_flashcards'),a:t.rich('a_flashcards',{strong})},{q:t('q_vocabulary'),a:t.rich('a_vocabulary',{strong})},{q:t('q_tutor'),a:t('a_tutor')},{q:t('q_voice'),a:t.rich('a_voice',{strong})},{q:t('q_listening'),a:t.rich('a_listening',{strong})},{q:t('q_reading'),a:t.rich('a_reading',{strong})},{q:t('q_feedback'),a:t.rich('a_feedback',{feedbackLink})},{q:t('q_password'),a:t.rich('a_password',{settingsLink})},{q:t('q_uiLanguage'),a:t.rich('a_uiLanguage',{settingsLink,strong})},
  ]
  if(isAdmin)faqs.push({q:t('q_providers'),a:<><p>{t.rich('a_providers_intro',{code})}</p><ul className="mt-2 space-y-2">{providers.map(([name,description])=><li key={name} className="flex items-start gap-2"><code>{name}</code><span>{description}</span></li>)}</ul></>},{q:t('q_invite'),a:t.rich('a_invite',{adminLink,code})})
  return <div className="juba-page-shell reference-faq">
    <style>{`
      .juba-app-shell .reference-faq{display:flex;flex-direction:column;gap:24px;}
      .juba-app-shell .reference-faq-header{display:flex;align-items:center;gap:16px;min-height:100px;}
      .juba-app-shell .reference-faq-header>svg{color:var(--juba-green);flex:none;}
      .juba-app-shell .reference-faq-header h1{font-size:28px;font-weight:650;margin:0;}
      .juba-app-shell .reference-faq-header p{font-size:14px;color:var(--juba-muted);margin:6px 0 0;}
      .juba-app-shell .reference-faq-panel{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
      .juba-app-shell .reference-faq-row{border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-faq-row:last-child{border:0;}
      .juba-app-shell .reference-faq-question{display:flex;align-items:center;justify-content:space-between;gap:16px;width:100%;min-height:56px;padding:14px 16px;text-align:start;color:var(--juba-ink);font-size:14px;font-weight:600;border:0;background:transparent;}
      .juba-app-shell .reference-faq-question:hover,.juba-app-shell .reference-faq-question[aria-expanded="true"]{background:var(--juba-green-soft);}
      .juba-app-shell .reference-faq-question>svg{color:var(--juba-green-dark);flex:none;}
      .juba-app-shell .reference-faq-answer{padding:16px;border-block-start:1px solid var(--juba-border);font-size:14px;line-height:1.7;color:var(--juba-muted);}
      .juba-app-shell .reference-faq-answer[hidden]{display:none;}
      .juba-app-shell .reference-faq-answer p{max-width:75ch;}
      @media(max-width:640px){.juba-app-shell .reference-faq{gap:16px;}.juba-app-shell .reference-faq-header h1{font-size:24px;}.juba-app-shell .reference-faq-header>svg{width:32px;height:32px;}}
    `}</style>
    <header className="reference-faq-header"><CircleHelp size={40} aria-hidden="true"/><div><h1>{t('title')}</h1><p>{t('subtitle')}</p></div></header>
    <section className="reference-faq-panel" aria-label={t('title')}>{faqs.map((item,index)=>{const expanded=open===index;return <div key={index} className="reference-faq-row"><button id={'faq-question-'+index} className="reference-faq-question" aria-expanded={expanded} aria-controls={'faq-answer-'+index} onClick={()=>setOpen(expanded?null:index)}><span>{item.q}</span>{expanded?<Minus size={16} aria-hidden="true"/>:<Plus size={16} aria-hidden="true"/>}</button><div id={'faq-answer-'+index} className="reference-faq-answer" hidden={!expanded} aria-labelledby={'faq-question-'+index}>{item.a}</div></div>})}</section>
  </div>
}
