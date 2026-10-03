'use client'

import {useEffect,useState,type FormEvent} from 'react'
import Link from 'next/link'
import {useLocale,useTranslations} from 'next-intl'
import {Flame,Trophy,CheckCircle2,Pencil,RefreshCw} from 'lucide-react'
import {useLanguageStore} from '@/store/language'
import {ACHIEVEMENTS,type AchievementId} from '@/lib/games/achievements'
import {getNextAchievement,knownEarnedAchievements,goalPercent,weekActivity} from './reference-feature-data'
import {useReferenceFeatures} from './useReferenceFeatures'

const arabicAchievements:Record<AchievementId,{title:string;description:string}>={first_game:{title:'اللعبة الأولى',description:'أكمل لعبتك الأولى.'},perfect_round:{title:'جولة بلا أخطاء',description:'أكمل جولة دون أخطاء.'},streak_5:{title:'سلسلة متوهجة',description:'حقق خمس إجابات صحيحة متتالية.'},xp_100:{title:'البداية',description:'اجمع 100 XP.'},xp_500:{title:'نجم صاعد',description:'اجمع 500 XP.'},multi_skill:{title:'متعدد المهارات',description:'حقق تقدمًا في ثلاث مهارات.'},daily_challenge:{title:'بطل اليوم',description:'أكمل تحديًا يوميًا.'}}
function Progress({percent,label}:{percent:number;label:string}){return <div className="ref-feature-track" role="progressbar" aria-label={label} aria-valuemin={0} aria-valuemax={100} aria-valuenow={percent}><span style={{width:percent+'%'}}/></div>}
export default function ReferenceFeatures(){
 const locale=useLocale(),rtl=locale.startsWith('ar'),common=useTranslations('common')
 const language=useLanguageStore(state=>state.activeLanguage?.code)
 const {goal,game,history,loading,saving,goalError,gameError,historyError,noPlan,saveError,saved,load,saveTargets}=useReferenceFeatures(language)
 const [editing,setEditing]=useState(false),[daily,setDaily]=useState(''),[weekly,setWeekly]=useState('')
 useEffect(()=>{setEditing(false);setDaily('');setWeekly('')},[language])
 function edit(){if(!goal)return;setDaily(String(goal.daily_xp_target));setWeekly(String(goal.weekly_xp_target));setEditing(true)}
 async function save(event:FormEvent<HTMLFormElement>){event.preventDefault();if(!goal)return;if(await saveTargets(Number(daily),Number(weekly)))setEditing(false)}
 const next=game?getNextAchievement(game):null,earned=game?knownEarnedAchievements(game):[]
 const achievement=(id:AchievementId)=>rtl?arabicAchievements[id]:ACHIEVEMENTS[id]
 const bars=goal?weekActivity(history,goal.day):[],max=Math.max(1,...bars.map(bar=>bar.value))
 return <section className="juba-page-shell ref-features" dir={rtl?'rtl':'ltr'} aria-label={rtl?'أهداف التعلم والإنجازات':'Learning goals and achievements'}>
 <style>{`
 .juba-app-shell .reference-dashboard-route .reference-dashboard-card:has(>.reference-dashboard-achievement){display:none;}
 .juba-app-shell .ref-features{padding-block-start:0!important;}
 .juba-app-shell .ref-features-title{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-block-end:16px;}
 .juba-app-shell .ref-features-title h2{font-size:18px;font-weight:650;margin:0;}
 .juba-app-shell .ref-features-refresh{display:grid;place-items:center;width:44px;height:44px;border:0;border-radius:5px;background:transparent;color:var(--juba-muted);}
 .juba-app-shell .ref-features-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) 244px;gap:24px;align-items:start;}
 .juba-app-shell .ref-feature-card{min-width:0;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);padding:16px;}
 .juba-app-shell .ref-feature-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-block-end:16px;}
 .juba-app-shell .ref-feature-head h3{font-size:14px;font-weight:650;margin:0;}
 .juba-app-shell .ref-feature-head a,.juba-app-shell .ref-feature-head button{display:inline-flex;align-items:center;gap:4px;font-size:11px;color:var(--juba-muted);background:transparent;border:0;min-height:44px;}
 .juba-app-shell .ref-feature-goal{display:flex;align-items:center;gap:12px;margin-block-end:16px;}
 .juba-app-shell .ref-feature-goal>svg{color:var(--juba-yellow);flex:none;}
 .juba-app-shell .ref-feature-goal>div{flex:1;min-width:0;}
 .juba-app-shell .ref-feature-goal p{font-size:13px;margin:0 0 8px;font-variant-numeric:tabular-nums;}
 .juba-app-shell .ref-feature-track{height:9px;border-radius:3px;overflow:hidden;background:var(--juba-soft);}
 .juba-app-shell .ref-feature-track>span{display:block;height:100%;border-radius:inherit;background:var(--juba-yellow);}
 .juba-app-shell .ref-feature-chart{display:flex;align-items:stretch;gap:8px;height:120px;margin-block:16px;background:repeating-linear-gradient(to top,transparent 0,transparent calc(25% - 1px),var(--juba-border) 25%);}
 .juba-app-shell .ref-feature-chart>div{display:flex;flex-direction:column;align-items:center;flex:1;gap:8px;min-width:0;}
 .juba-app-shell .ref-feature-chart>div>div{height:calc(100% - 20px);display:flex;align-items:flex-end;justify-content:center;width:100%;}
 .juba-app-shell .ref-feature-chart span{display:block;width:14px;max-width:100%;background:var(--juba-yellow);border-radius:2px 2px 0 0;}
 .juba-app-shell .ref-feature-chart small{font-size:10px;color:var(--juba-muted);}
 .juba-app-shell .ref-feature-caption{font-size:12px;line-height:1.6;color:var(--juba-muted);margin:8px 0;}
 .juba-app-shell .ref-feature-goal-form{display:flex;flex-direction:column;gap:12px;border-block-start:1px solid var(--juba-border);padding-block-start:16px;margin-block-start:16px;}
 .juba-app-shell .ref-feature-goal-form label{font-size:12px;display:flex;flex-direction:column;gap:6px;}
 .juba-app-shell .ref-feature-goal-form input{width:100%;padding:8px 12px;}
 .juba-app-shell .ref-feature-form-actions{display:flex;gap:8px;flex-wrap:wrap;}
 .juba-app-shell .ref-feature-form-actions button{padding-inline:12px;}
 .juba-app-shell .ref-feature-state{padding:16px 0;display:flex;flex-direction:column;gap:12px;font-size:13px;line-height:1.6;color:var(--juba-muted);}
 .juba-app-shell .ref-feature-state button{padding-inline:12px;align-self:flex-start;}
 .juba-app-shell .ref-feature-error{font-size:12px;color:var(--duo-red);}
 .juba-app-shell .ref-feature-success{font-size:12px;color:var(--juba-green-dark);}
 .juba-app-shell .ref-feature-badge-progress{display:flex;align-items:center;gap:12px;}
 .juba-app-shell .ref-feature-badge-icon{display:grid;place-items:center;flex:none;width:48px;height:68px;border-radius:5px;background:var(--juba-green);color:var(--juba-card);}
 .juba-app-shell .ref-feature-badge-progress>div:last-child{min-width:0;flex:1;}
 .juba-app-shell .ref-feature-badge-progress strong{font-size:13px;font-weight:650;}
 .juba-app-shell .ref-feature-badge-progress p{font-size:11px;line-height:1.6;color:var(--juba-muted);margin:6px 0;}
 .juba-app-shell .ref-feature-earned{display:flex;flex-direction:column;gap:12px;}
 .juba-app-shell .ref-feature-earned>div{display:flex;align-items:center;gap:8px;font-size:12px;}
 .juba-app-shell .ref-feature-earned svg{color:var(--juba-green-dark);flex:none;}
 .juba-app-shell .ref-feature-earned strong{font-weight:600;}
 .juba-app-shell .ref-feature-skeleton{height:120px;border-radius:5px;background:var(--juba-soft);}
 @media(max-width:1100px){.juba-app-shell .ref-features-grid{grid-template-columns:1fr 1fr;}.juba-app-shell .ref-features-grid>section:last-child{grid-column:1/-1;}}
 @media(max-width:640px){.juba-app-shell .ref-features-grid{grid-template-columns:1fr;gap:16px;}}
 `}</style>
 <header className="ref-features-title"><h2>{rtl?'أهدافك وإنجازاتك':'Your goals and achievements'}</h2><button className="ref-features-refresh" aria-label={rtl?'تحديث':'Refresh'} disabled={loading||saving} onClick={()=>void load()}><RefreshCw size={18}/></button></header>
 <div className="ref-features-grid"><section className="ref-feature-card"><header className="ref-feature-head"><h3>{rtl?'الهدف اليومي':'Daily XP goal'}</h3>{goal&&<button onClick={edit} disabled={saving||loading} aria-expanded={editing} aria-controls="xp-goal-editor"><Pencil size={12}/>{rtl?'تعديل الهدف':'Edit goal'}</button>}</header>
 {loading?<div className="ref-feature-skeleton" role="status" aria-label={common('loading')}/>:noPlan?<div className="ref-feature-state"><p>{common('noActivePlan')}</p><Link href="/assessment">{rtl?'حدد مستواك لإنشاء خطة':'Create a plan with an assessment'}</Link></div>:goalError?<div className="ref-feature-state" role="alert"><p>{common('error')}</p><button className="juba-secondary-button" onClick={()=>void load()}>{common('retry')}</button></div>:goal?<><div className="ref-feature-goal"><Flame size={32}/><div><p>{goal.daily_xp}/{goal.daily_xp_target} XP</p><Progress percent={goalPercent(goal.daily_progress)} label={rtl?'تقدم الهدف اليومي':'Daily XP goal progress'}/></div></div><p className="ref-feature-caption">{rtl?'الهدف الأسبوعي':'Weekly goal'}: {goal.weekly_xp}/{goal.weekly_xp_target} XP</p><Progress percent={goalPercent(goal.weekly_progress)} label={rtl?'تقدم الهدف الأسبوعي':'Weekly XP goal progress'}/><p className="ref-feature-caption">{rtl?'نشاط XP لآخر 7 أيام':'XP activity over the last 7 days'}</p>{historyError?<p className="ref-feature-error" role="alert">{common('error')}</p>:<><div className="ref-feature-chart" aria-hidden="true">{bars.map(bar=><div key={bar.date} title={bar.date+': '+bar.value+' XP'}><div><span style={{height:bar.value/max*100+'%'}}/></div><small>{new Date(bar.date+'T00:00:00Z').toLocaleDateString(locale,{weekday:'short',timeZone:'UTC'})}</small></div>)}</div><details><summary className="ref-feature-caption">{rtl?'عرض القيم':'View activity values'}</summary>{bars.map(bar=><p className="ref-feature-caption" key={bar.date}>{bar.date}: {bar.value} XP</p>)}</details></>}<p className="ref-feature-caption">{rtl?'هدف اليوم يستبعد مكافآت الأهداف، والرسم يعرض XP الإجمالي.':'Daily goal excludes goal rewards; the chart shows total XP.'}</p>{goal.daily_reward_claimed&&<p className="ref-feature-success">{rtl?'مكافأة يومية مسجلة':'Daily reward recorded'}: {goal.daily_reward_xp} XP</p>}{goal.weekly_reward_claimed&&<p className="ref-feature-success">{rtl?'مكافأة أسبوعية مسجلة':'Weekly reward recorded'}: {goal.weekly_reward_xp} XP</p>}</>:null}
 {editing&&goal&&<form id="xp-goal-editor" className="ref-feature-goal-form" onSubmit={save}><label>{rtl?'هدف XP اليومي':'Daily XP target'}<input className="juba-input" type="number" min={1} max={10000} step={1} required value={daily} disabled={saving} onChange={event=>setDaily(event.target.value)}/></label><label>{rtl?'هدف XP الأسبوعي':'Weekly XP target'}<input className="juba-input" type="number" min={1} max={70000} step={1} required value={weekly} disabled={saving} onChange={event=>setWeekly(event.target.value)}/></label><div className="ref-feature-form-actions"><button className="juba-primary-button" disabled={saving||loading} type="submit">{saving?'…':rtl?'حفظ':'Save'}</button><button className="juba-secondary-button" type="button" disabled={saving} onClick={()=>setEditing(false)}>{common('cancel')}</button></div></form>}{saveError&&<p className="ref-feature-error" role="alert">{common('error')}</p>}{saved&&<p className="ref-feature-success" role="status">{rtl?'تم حفظ الأهداف في حسابك.':'Goals saved to your account.'}</p>}</section>
 <section className="ref-feature-card"><header className="ref-feature-head"><h3>{rtl?'الإنجاز التالي':'Next achievement'}</h3><Link href="/games">{rtl?'الألعاب':'Games'}</Link></header>{loading?<div className="ref-feature-skeleton" role="status" aria-label={common('loading')}/>:gameError?<div className="ref-feature-state" role="alert"><p>{common('error')}</p><button className="juba-secondary-button" onClick={()=>void load()}>{common('retry')}</button></div>:next?<div className="ref-feature-badge-progress"><span className="ref-feature-badge-icon"><Trophy size={28}/></span><div><strong>{achievement(next.id).title}</strong><p>{achievement(next.id).description}</p><Progress percent={next.percent} label={achievement(next.id).title}/><p>{next.current}/{next.target}</p></div></div>:<p className="ref-feature-caption">{rtl?'لا يوجد هدف إنجاز قابل للقياس غير مكتمل حاليًا.':'No incomplete measurable achievement target remains.'}</p>}<p className="ref-feature-caption">{rtl?'التقدم محسوب من نشاط حسابك وشروط الإنجازات الحالية.':'Progress uses your account activity and existing achievement thresholds.'}</p></section>
 <section className="ref-feature-card"><header className="ref-feature-head"><h3>{rtl?'إنجازات مكتسبة':'Earned achievements'}</h3><span>{earned.length}</span></header>{loading?<div className="ref-feature-skeleton" role="status" aria-label={common('loading')}/>:gameError?<p className="ref-feature-error" role="alert">{common('error')}</p>:earned.length?<div className="ref-feature-earned">{earned.map(id=><div key={id}><CheckCircle2 size={18}/><strong>{achievement(id).title}</strong></div>)}</div>:<p className="ref-feature-caption">{rtl?'لا توجد إنجازات مسجلة بعد. ابدأ بالممارسة.':'No achievements recorded yet. Start practising.'}</p>}</section></div>
 </section>
}
