'use client'

import { useLocale, useTranslations } from 'next-intl'
import { BookOpen, GraduationCap, ChevronRight } from 'lucide-react'
interface Props{onBeginner:()=>void;onHasExperience:()=>void;languageCode:string}
export default function BeginnerGate({onBeginner,onHasExperience,languageCode}:Props){
  const t=useTranslations('assessment')
  const locale=useLocale()
  const language=(()=>{try{return new Intl.DisplayNames([locale],{type:'language'}).of(languageCode)??languageCode}catch{return languageCode}})()
  return <section className="reference-beginner-panel">
    <style>{`
      .juba-app-shell .reference-beginner-panel{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
      .juba-app-shell .reference-beginner-panel>header{padding:16px;border-block-end:1px solid var(--juba-border);font-size:12px;color:var(--juba-muted);}
      .juba-app-shell .reference-beginner-copy{padding:24px 16px;}
      .juba-app-shell .reference-beginner-copy h2{font-size:22px;font-weight:650;line-height:1.4;margin:0;}
      .juba-app-shell .reference-beginner-copy p{font-size:14px;line-height:1.7;color:var(--juba-muted);margin:8px 0 0;}
      .juba-app-shell .reference-beginner-options{display:flex;flex-direction:column;border-block-start:1px solid var(--juba-border);}
      .juba-app-shell .reference-beginner-options button{display:flex;align-items:center;gap:16px;width:100%;padding:20px 16px;border:0;border-block-end:1px solid var(--juba-border);background:transparent;color:var(--juba-ink);text-align:start;}
      .juba-app-shell .reference-beginner-options button:last-child{border:0;}
      .juba-app-shell .reference-beginner-options button:hover{background:var(--juba-green-soft);}
      .juba-app-shell .reference-beginner-options button>svg:first-child{color:var(--juba-green);flex:none;}
      .juba-app-shell .reference-beginner-options button>span{flex:1;min-width:0;}
      .juba-app-shell .reference-beginner-options strong{display:block;font-size:15px;font-weight:650;}
      .juba-app-shell .reference-beginner-options small{display:block;font-size:13px;line-height:1.6;color:var(--juba-muted);margin-block-start:4px;}
      .juba-app-shell[dir="rtl"] .reference-beginner-options button>svg:last-child{transform:scaleX(-1);}
    `}</style>
    <header>{t('step1')}</header><div className="reference-beginner-copy"><h2>{t('studiedBefore',{language})}</h2><p>{t('studiedBeforeHint')}</p></div><div className="reference-beginner-options"><button onClick={onBeginner}><BookOpen size={28} aria-hidden="true"/><span><strong>{t('beginnerOption')}</strong><small>{t('beginnerOptionHint')}</small></span><ChevronRight size={18} aria-hidden="true"/></button><button onClick={onHasExperience}><GraduationCap size={28} aria-hidden="true"/><span><strong>{t('hasExperienceOption')}</strong><small>{t('hasExperienceOptionHint')}</small></span><ChevronRight size={18} aria-hidden="true"/></button></div>
  </section>
}
