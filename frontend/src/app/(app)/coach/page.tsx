'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { useLocale } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { BrainCircuit, CheckCircle2, Flame, Mic, RefreshCw, Target, Volume2, Zap, ChevronRight, ChevronLeft, Plane, Briefcase, Utensils, Hotel } from 'lucide-react'

interface ProgressSummary{current_streak?:number;total_xp?:number;accuracy?:number;vocabulary_mastered?:number;vocabulary_total?:number;vocabulary_progress?:number;skills?:Record<string,number>}
interface TodayPlan{cefr_level?:string|null;lessons?:Array<{id:number|null;title:string;lesson_type:string;estimated_minutes:number;is_completed:boolean}>;pending_count?:number}
const scenarios=[{icon:Plane,title:'Airport',arTitle:'المطار',desc:'Check in, ask for directions, handle delays.',arDesc:'إجراءات السفر والاتجاهات والتأخير.'},{icon:Briefcase,title:'Job interview',arTitle:'مقابلة العمل',desc:'Practice answers, confidence and professional vocabulary.',arDesc:'تدرّب على الإجابات والثقة والمفردات المهنية.'},{icon:Utensils,title:'Restaurant',arTitle:'المطعم',desc:'Order naturally and handle a real conversation.',arDesc:'اطلب بشكل طبيعي وتدرّب على محادثة واقعية.'},{icon:Hotel,title:'Hotel',arTitle:'الفندق',desc:'Book a room, solve problems and make requests.',arDesc:'احجز غرفة وحل المشكلات وقدّم الطلبات.'}]
export default function CoachPage(){
  const rtl=useLocale()==='ar'
  const user=useAuthStore(s=>s.user)
  const language=useLanguageStore(s=>s.activeLanguage)
  const [progress,setProgress]=useState<ProgressSummary>({})
  const [plan,setPlan]=useState<TodayPlan>({})
  const [loading,setLoading]=useState(true)
  const [refreshing,setRefreshing]=useState(false)
  const [error,setError]=useState(false)
  const [progressReady,setProgressReady]=useState(false)
  const [reload,setReload]=useState(0)
  useEffect(()=>{
    let cancelled=false
    async function load(){
      setLoading(true);setError(false);setProgressReady(false)
      try{
        const [progressRes,planRes]=await Promise.all([apiFetch('/api/progress/summary'),apiFetch('/api/study-plan/today')])
        const nextProgress=progressRes.ok?await progressRes.json() as ProgressSummary:{}
        const nextPlan=planRes.ok?await planRes.json() as TodayPlan:{}
        if(cancelled)return
        setProgress(nextProgress);setPlan(nextPlan);setProgressReady(progressRes.ok)
        if(!progressRes.ok||(!planRes.ok&&planRes.status>=500))setError(true)
      }catch{if(!cancelled){setError(true);setProgressReady(false)}}finally{if(!cancelled){setLoading(false);setRefreshing(false)}}
    }
    void load();return ()=>{cancelled=true}
  },[language?.code,reload])
  const weakestSkill=useMemo(()=>{const entries=Object.entries(progress.skills??{});return entries.length?entries.sort((a,b)=>Number(a[1])-Number(b[1]))[0][0]:null},[progress.skills])
  const completed=(plan.lessons??[]).filter(lesson=>lesson.is_completed).length
  const total=plan.lessons?.length??0
  const vocabProgress=Math.max(0,Math.min(100,Math.round((progress.vocabulary_progress??0)*100)))
  const dailyProgress=total?Math.min(100,Math.round(completed/total*100)):0
  const Forward=rtl?ChevronLeft:ChevronRight
  const name=user?.displayName||user?.username||''
  const actions=[{href:'/conversation',icon:Mic,title:rtl?'تحدث':'Speak',detail:rtl?'ممارسة مقترحة: 10 دقائق لتقوية الطلاقة.':'Suggested practice: 10 minutes to build fluency.'},{href:'/listening',icon:Volume2,title:rtl?'استمع':'Listen',detail:rtl?'ممارسة مقترحة: 8 دقائق من الاستماع المركز.':'Suggested practice: 8 minutes of focused listening.'},{href:'/flashcards',icon:RefreshCw,title:rtl?'راجع':'Review',detail:rtl?'راجع الكلمات المستحقة من بطاقاتك.':'Refresh the words due in your flashcards.'},{href:'/progress',icon:Target,title:rtl?'التقدم':'Progress',detail:rtl?'راجع تقدم المفردات والمهارات.':'View vocabulary and skill progress.'}]
  return <div className="juba-page-shell reference-coach" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-coach{display:flex;flex-direction:column;gap:24px;}
      .juba-app-shell .reference-coach-header{display:flex;align-items:center;gap:16px;min-height:100px;flex-wrap:wrap;}
      .juba-app-shell .reference-coach-header>svg{color:var(--juba-green);flex:none;}
      .juba-app-shell .reference-coach-header>div{flex:1;min-width:0;}
      .juba-app-shell .reference-coach-header h1{font-size:28px;font-weight:650;margin:0;}
      .juba-app-shell .reference-coach-header p{font-size:13px;line-height:1.6;color:var(--juba-muted);margin:6px 0 0;}
      .juba-app-shell .reference-coach-header button{padding-inline:12px;}
      .juba-app-shell .reference-coach-layout{display:grid;grid-template-columns:minmax(0,1fr) 264px;gap:24px;align-items:start;}
      .juba-app-shell .reference-coach-primary,.juba-app-shell .reference-coach-secondary{display:flex;flex-direction:column;gap:24px;min-width:0;}
      .juba-app-shell .reference-coach-card{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
      .juba-app-shell .reference-coach-card-head{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-coach-card-head h2{font-size:14px;font-weight:650;margin:0;}
      .juba-app-shell .reference-coach-card-head span{font-size:11px;color:var(--juba-muted);}
      .juba-app-shell .reference-coach-overview{display:grid;grid-template-columns:1fr 1fr;gap:24px;}
      .juba-app-shell .reference-coach-goal{padding:16px;}
      .juba-app-shell .reference-coach-goal>div:first-child{display:flex;align-items:center;justify-content:space-between;font-size:13px;margin-block-end:12px;}
      .juba-app-shell .reference-coach-track{height:8px;background:var(--juba-soft);border-radius:3px;overflow:hidden;}
      .juba-app-shell .reference-coach-track>span{display:block;height:100%;background:var(--juba-yellow);}
      .juba-app-shell .reference-coach-metrics{display:flex;flex-direction:column;padding-inline:16px;margin:0;}
      .juba-app-shell .reference-coach-metrics>div{display:flex;align-items:center;justify-content:space-between;gap:8px;padding-block:12px;border-block-end:1px solid var(--juba-border);font-size:12px;}
      .juba-app-shell .reference-coach-metrics>div:last-child{border:0;}
      .juba-app-shell .reference-coach-metrics dt{display:flex;align-items:center;gap:8px;color:var(--juba-muted);}
      .juba-app-shell .reference-coach-metrics svg{color:var(--juba-green);}
      .juba-app-shell .reference-coach-metrics dd{margin:0;font-weight:650;font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-coach-insight{padding:16px;}
      .juba-app-shell .reference-coach-insight h3{font-size:18px;font-weight:650;margin:0;}
      .juba-app-shell .reference-coach-insight p{font-size:13px;line-height:1.7;color:var(--juba-muted);margin:8px 0 16px;}
      .juba-app-shell .reference-coach-insight-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
      .juba-app-shell .reference-coach-insight-actions a{padding-inline:12px;}
      .juba-app-shell .reference-coach-lesson{display:flex;align-items:center;gap:12px;padding:16px;border-block-end:1px solid var(--juba-border);color:var(--juba-ink);text-decoration:none;}
      .juba-app-shell .reference-coach-lesson:last-child{border:0;}
      .juba-app-shell .reference-coach-lesson:hover{background:var(--juba-green-soft);}
      .juba-app-shell .reference-coach-lesson>span{display:grid;place-items:center;width:32px;height:32px;flex:none;background:var(--juba-green-soft);border-radius:50%;color:var(--juba-green-dark);font-size:12px;}
      .juba-app-shell .reference-coach-lesson>div{min-width:0;flex:1;}
      .juba-app-shell .reference-coach-lesson strong{font-size:14px;font-weight:600;}
      .juba-app-shell .reference-coach-lesson p{font-size:11px;color:var(--juba-muted);margin:4px 0 0;}
      .juba-app-shell .reference-coach-action,.juba-app-shell .reference-coach-scenario{display:flex;align-items:flex-start;gap:12px;padding:16px;border-block-end:1px solid var(--juba-border);color:var(--juba-ink);text-decoration:none;}
      .juba-app-shell .reference-coach-action:last-child,.juba-app-shell .reference-coach-scenario:last-child{border:0;}
      .juba-app-shell .reference-coach-action>svg,.juba-app-shell .reference-coach-scenario>svg{color:var(--juba-green);flex:none;}
      .juba-app-shell .reference-coach-action strong,.juba-app-shell .reference-coach-scenario strong{font-size:13px;font-weight:600;}
      .juba-app-shell .reference-coach-action p,.juba-app-shell .reference-coach-scenario p{font-size:12px;line-height:1.6;color:var(--juba-muted);margin:4px 0 0;}
      .juba-app-shell .reference-coach-empty{padding:24px 16px;display:flex;flex-direction:column;align-items:center;gap:12px;font-size:13px;text-align:center;color:var(--juba-muted);}
      .juba-app-shell .reference-coach-empty p{margin:0;line-height:1.7;}
      .juba-app-shell .reference-coach-error{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:12px 16px;border:1px solid var(--duo-red);border-radius:6px;font-size:13px;}
      .juba-app-shell .reference-coach-error button{padding-inline:12px;}
      .juba-app-shell .reference-coach-loading{height:80px;margin:16px;border-radius:5px;background:var(--juba-soft);}
      .juba-app-shell .reference-coach-footer{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;padding-block-start:16px;border-block-start:1px solid var(--juba-border);font-size:12px;color:var(--juba-muted);}
      @media(max-width:1000px){.juba-app-shell .reference-coach-layout{grid-template-columns:1fr;}.juba-app-shell .reference-coach-secondary{display:grid;grid-template-columns:1fr 1fr;}}
      @media(max-width:640px){.juba-app-shell .reference-coach,.juba-app-shell .reference-coach-primary{gap:16px;}.juba-app-shell .reference-coach-overview,.juba-app-shell .reference-coach-secondary{grid-template-columns:1fr;gap:16px;}.juba-app-shell .reference-coach-header h1{font-size:24px;}.juba-app-shell .reference-coach-header>svg{width:32px;height:32px;}}
    `}</style>
    <header className="reference-coach-header"><BrainCircuit size={40} aria-hidden="true"/><div><h1>{rtl?'مدرّب التعلم':'Learning coach'}</h1><p>{name}{name?' · ':''}{rtl?'خطوتك التالية وفق نشاطك وخطتك.':'Your next step based on your activity and plan.'}</p></div><button className="juba-secondary-button" onClick={()=>{setRefreshing(true);setReload(value=>value+1)}} disabled={refreshing||loading}><RefreshCw size={16}/>{rtl?'تحديث':'Refresh coaching'}</button></header>
    {error&&<div className="reference-coach-error" role="alert"><span>{rtl?'تعذر تحميل بعض بيانات التدريب. لا تتوفر توصيات موثوقة بعد.':'Some coaching data could not be loaded. Recommendations are not yet reliable.'}</span><button className="juba-secondary-button" onClick={()=>setReload(value=>value+1)} disabled={loading}>{rtl?'إعادة المحاولة':'Retry'}</button></div>}
    <div className="reference-coach-layout"><div className="reference-coach-primary">
      <div className="reference-coach-overview"><section className="reference-coach-card"><header className="reference-coach-card-head"><h2>{rtl?'هدف اليوم':'Daily goal'}</h2><Flame size={16}/></header>{loading?<div className="reference-coach-loading" role="status" aria-label={rtl?'جارٍ التحميل':'Loading'}/>:<div className="reference-coach-goal"><div><span>{rtl?'الدروس المكتملة':'Completed lessons'}</span><strong>{completed}/{total}</strong></div><div className="reference-coach-track" role="progressbar" aria-label={rtl?'تقدم اليوم':'Daily progress'} aria-valuemin={0} aria-valuemax={100} aria-valuenow={dailyProgress}><span style={{width:dailyProgress+'%'}}/></div></div>}</section><section className="reference-coach-card"><header className="reference-coach-card-head"><h2>{rtl?'نشاطك':'Your momentum'}</h2></header>{loading?<div className="reference-coach-loading" role="status" aria-label={rtl?'جارٍ التحميل':'Loading'}/>:progressReady?<dl className="reference-coach-metrics"><div><dt><Flame size={16}/>{rtl?'السلسلة':'Day streak'}</dt><dd>{progress.current_streak??0}</dd></div><div><dt><Zap size={16}/>XP</dt><dd>{progress.total_xp??0}</dd></div><div><dt><Target size={16}/>{rtl?'الدقة':'Accuracy'}</dt><dd>{Math.round((progress.accuracy??0)*100)}%</dd></div></dl>:<div className="reference-coach-empty"><p>{rtl?'لا تتوفر بيانات التقدم.':'Progress data is unavailable.'}</p></div>}</section></div>
      <section className="reference-coach-card"><header className="reference-coach-card-head"><h2>{rtl?'توجيه المدرب':'Coach insight'}</h2></header>{loading?<div className="reference-coach-loading" role="status" aria-label={rtl?'جارٍ التحميل':'Loading'}/>:weakestSkill&&progressReady?<div className="reference-coach-insight"><h3>{rtl?'ركّز اليوم على':'Focus today on'} <bdi>{weakestSkill.replaceAll('_',' ')}</bdi></h3><p>{rtl?'هذه المهارة صاحبة أقل تقدم مسجل في بياناتك الحالية. اختر جلسة ممارسة قصيرة أو تابع خطتك.':'This skill has the lowest recorded progress in your current data. Choose a short practice session or continue your plan.'}</p><div className="reference-coach-insight-actions"><Link href="/conversation" className="juba-primary-button">{rtl?'ابدأ الممارسة':'Start focused practice'}<Forward size={16}/></Link><Link href="/plan" className="juba-secondary-button">{rtl?'عرض خطتي':'View my plan'}</Link></div></div>:<div className="reference-coach-empty"><p>{rtl?'ابدأ التعلّم لتسجيل نشاط يدعم توصيات المدرب.':'Start learning to record activity for coaching recommendations.'}</p><Link href="/plan" className="juba-secondary-button">{rtl?'عرض خطتي':'View my plan'}</Link></div>}</section>
      <section className="reference-coach-card"><header className="reference-coach-card-head"><h2>{rtl?'قائمة اليوم':'Your best work for today'}</h2><span>{completed}/{total}</span></header>{loading?<div className="reference-coach-loading" role="status" aria-label={rtl?'جارٍ التحميل':'Loading'}/>:plan.lessons?.length?plan.lessons.slice(0,4).map((lesson,index)=><Link className="reference-coach-lesson" href={lesson.id?'/lesson/'+lesson.id:'/plan'} key={`${lesson.id}-${index}`}><span>{lesson.is_completed?<CheckCircle2 size={18}/>:index+1}</span><div><strong dir="auto">{lesson.title}</strong><p>{lesson.lesson_type.replaceAll('_',' ')} · {lesson.estimated_minutes||25} {rtl?'دقيقة':'min'}</p></div><Forward size={16}/></Link>):<div className="reference-coach-empty"><p>{rtl?'أكمل التقييم لفتح خطة تعلم متكيفة.':'Complete your assessment to unlock an adaptive learning plan.'}</p><Link className="juba-secondary-button" href="/assessment">{rtl?'التقييم':'Assessment'}</Link></div>}</section>
      {progressReady&&!loading&&<section className="reference-coach-card"><header className="reference-coach-card-head"><h2>{rtl?'تقدم المفردات':'Vocabulary progress'}</h2><span>{vocabProgress}%</span></header><div className="reference-coach-goal"><div><span>{rtl?'كلمات متقنة':'Words mastered'}</span><strong>{progress.vocabulary_mastered??0}/{progress.vocabulary_total??0}</strong></div><div className="reference-coach-track" role="progressbar" aria-label={rtl?'تقدم المفردات':'Vocabulary progress'} aria-valuemin={0} aria-valuemax={100} aria-valuenow={vocabProgress}><span style={{width:vocabProgress+'%'}}/></div></div></section>}
    </div><aside className="reference-coach-secondary"><section className="reference-coach-card"><header className="reference-coach-card-head"><h2>{rtl?'أدوات الممارسة':'Practice tools'}</h2></header>{actions.map(({href,icon:Icon,title,detail})=><Link className="reference-coach-action" href={href} key={href}><Icon size={20}/><div><strong>{title}</strong><p>{detail}</p></div></Link>)}</section><section className="reference-coach-card"><header className="reference-coach-card-head"><h2>{rtl?'مواقف واقعية':'Real-world rooms'}</h2></header>{scenarios.map(({icon:Icon,title,arTitle,desc,arDesc})=><Link className="reference-coach-scenario" href="/conversation" key={title}><Icon size={20}/><div><strong>{rtl?arTitle:title}</strong><p>{rtl?arDesc:desc}</p></div></Link>)}</section></aside></div>
    <footer className="reference-coach-footer"><span>{rtl?'التعلم':'Learning'} · {language?.name||(rtl?'مخصص لك':'personalized for you')}</span><span>CEFR {plan.cefr_level||(rtl?'متكيف':'adaptive')} · JUBA LISAN Coach</span></footer>
  </div>
}
