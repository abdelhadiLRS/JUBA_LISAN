'use client'

import { useLocale, useTranslations } from 'next-intl'
import { Check, ChevronLeft, ChevronRight } from 'lucide-react'
export interface DurationOption{weeks:number;daysPerWeek:number;intensity:'intensive'|'standard'|'relaxed'|'very_relaxed'}
export const DURATION_OPTIONS:DurationOption[]=[{weeks:4,daysPerWeek:5,intensity:'intensive'},{weeks:8,daysPerWeek:5,intensity:'standard'},{weeks:12,daysPerWeek:4,intensity:'relaxed'},{weeks:16,daysPerWeek:3,intensity:'very_relaxed'}]
export const GOAL_OPTIONS=[{id:'grammar'},{id:'vocabulary'},{id:'reading'},{id:'writing'},{id:'conversation'},{id:'listening'}]
interface Props{selectedWeeks:number;selectedGoals:string[];onSelectDuration:(option:DurationOption)=>void;onToggleGoal:(goal:string)=>void;onConfirm:()=>void;onBack:()=>void;cefr_level:string;loading:boolean;error?:string}
export default function DurationSelector({selectedWeeks,selectedGoals,onSelectDuration,onToggleGoal,onConfirm,onBack,cefr_level,loading,error=''}:Props){
  const t=useTranslations('assessment')
  const tCommon=useTranslations('common')
  const rtl=useLocale()==='ar'
  const selected=DURATION_OPTIONS.find(option=>option.weeks===selectedWeeks)??DURATION_OPTIONS[2]
  const intensityMap:Record<string,string>={intensive:t('intensity.intensive'),standard:t('intensity.standard'),relaxed:t('intensity.relaxed'),very_relaxed:t('intensity.veryRelaxed')}
  const goalLabel=(goal:string)=>t(`goals.${goal as 'grammar'|'vocabulary'|'reading'|'writing'|'conversation'|'listening'}`)
  const Forward=rtl?ChevronLeft:ChevronRight
  const Back=rtl?ChevronRight:ChevronLeft
  return <div className="reference-duration-workspace">
    <style>{`
      .juba-app-shell .reference-duration-workspace{display:grid;grid-template-columns:minmax(0,1fr) 264px;gap:24px;align-items:start;}
      .juba-app-shell .reference-duration-primary{display:flex;flex-direction:column;gap:24px;min-width:0;}
      .juba-app-shell .reference-duration-panel{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
      .juba-app-shell .reference-duration-panel>header{padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-duration-panel h2{font-size:14px;font-weight:650;margin:0;}
      .juba-app-shell .reference-duration-panel>header p{font-size:11px;color:var(--juba-muted);margin:0 0 6px;}
      .juba-app-shell .reference-duration-options{display:flex;flex-direction:column;}
      .juba-app-shell .reference-duration-options button{display:flex;align-items:center;gap:12px;padding:16px;border:0;border-block-end:1px solid var(--juba-border);background:transparent;color:var(--juba-ink);text-align:start;width:100%;}
      .juba-app-shell .reference-duration-options button:last-child{border:0;}
      .juba-app-shell .reference-duration-options button[aria-pressed="true"]{background:var(--juba-green-soft);}
      .juba-app-shell .reference-duration-choice{width:24px;height:24px;display:grid;place-items:center;border:1px solid var(--juba-border);border-radius:50%;flex:none;color:var(--juba-green-dark);}
      .juba-app-shell .reference-duration-options strong{font-size:14px;font-weight:650;}
      .juba-app-shell .reference-duration-options small{display:block;font-size:12px;line-height:1.6;color:var(--juba-muted);margin-block-start:4px;}
      .juba-app-shell .reference-duration-goals{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:16px;}
      .juba-app-shell .reference-duration-goals button{display:flex;align-items:center;gap:6px;min-height:40px;padding:8px 12px;border:1px solid var(--juba-border);border-radius:5px;color:var(--juba-muted);background:var(--juba-card);font-size:13px;}
      .juba-app-shell .reference-duration-goals button[aria-pressed="true"]{color:var(--juba-green-dark);background:var(--juba-green-soft);border-color:var(--juba-green);}
      .juba-app-shell .reference-duration-summary{padding:16px;margin:0;display:flex;flex-direction:column;gap:16px;}
      .juba-app-shell .reference-duration-summary dt{font-size:11px;color:var(--juba-muted);}
      .juba-app-shell .reference-duration-summary dd{font-size:13px;line-height:1.6;margin:4px 0 0;color:var(--juba-ink);}
      .juba-app-shell .reference-duration-actions{display:flex;flex-direction:column;gap:8px;padding:16px;border-block-start:1px solid var(--juba-border);}
      .juba-app-shell .reference-duration-actions button{padding-inline:12px;}
      .juba-app-shell .reference-duration-error{padding:12px 16px;font-size:13px;color:var(--duo-red);border-block-start:1px solid var(--juba-border);}
      @media(max-width:1000px){.juba-app-shell .reference-duration-workspace{grid-template-columns:1fr;}}
      @media(max-width:640px){.juba-app-shell .reference-duration-primary,.juba-app-shell .reference-duration-workspace{gap:16px;}.juba-app-shell .reference-duration-goals button{min-height:44px;}}
    `}</style>
    <div className="reference-duration-primary"><section className="reference-duration-panel"><header><p>{t('step3')}</p><h2>{t('howManyWeeks',{cefr_level})}</h2></header><div className="reference-duration-options" role="group" aria-label={t('howManyWeeks',{cefr_level})}>{DURATION_OPTIONS.map(option=><button key={option.weeks} onClick={()=>onSelectDuration(option)} aria-pressed={selectedWeeks===option.weeks}><span className="reference-duration-choice" aria-hidden="true">{selectedWeeks===option.weeks&&<Check size={14}/>}</span><span><strong>{t('nWeeks',{count:option.weeks})}</strong><small>{intensityMap[option.intensity]} · {t('approxLessons',{count:option.weeks*option.daysPerWeek})}</small><small>{t('daysPerWeek',{count:option.daysPerWeek})}</small></span></button>)}</div></section><section className="reference-duration-panel"><header><h2>{t('mainGoals')}</h2></header><div className="reference-duration-goals" role="group" aria-label={t('mainGoals')}>{GOAL_OPTIONS.map(goal=><button key={goal.id} onClick={()=>onToggleGoal(goal.id)} aria-pressed={selectedGoals.includes(goal.id)}>{selectedGoals.includes(goal.id)&&<Check size={14} aria-hidden="true"/>}{goalLabel(goal.id)}</button>)}</div></section></div>
    <aside className="reference-duration-panel"><header><h2>{t('step3')}</h2></header><dl className="reference-duration-summary"><div><dt>{t('summaryLevel')}</dt><dd>{cefr_level}</dd></div><div><dt>{t('summaryDuration')}</dt><dd>{t('nWeeks',{count:selected.weeks})} · {t('daysPerWeek',{count:selected.daysPerWeek})}</dd></div><div><dt>{t('summaryGoals')}</dt><dd>{selectedGoals.length?selectedGoals.map(goalLabel).join(', '):t('noneSelected')}</dd></div></dl>{error&&<div className="reference-duration-error" role="alert">{error}</div>}<div className="reference-duration-actions"><button className="juba-primary-button" onClick={onConfirm} disabled={loading||!selectedGoals.length}>{loading?t('buildingPlan'):t('startMyPlan')}<Forward size={16}/></button><button className="juba-secondary-button" onClick={onBack}><Back size={16}/>{tCommon('back')}</button></div></aside>
  </div>
}
