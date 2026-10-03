'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { useLocale } from 'next-intl'
import { BookOpen, CheckCircle2, Headphones, LockKeyhole, Mic2, Coffee, Utensils, Plane, Briefcase, ChevronRight, ChevronLeft } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { CEFR_LEVELS, getCurriculumUnits, type CEFRLevel, type CurriculumUnit } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
import './courses-reference.css'

interface StudyPlan {cefr_level:CEFRLevel;generated_plan?:{weekly_plan?:Array<{days?:Array<{unit_id:string}>}>}}
interface CompetencyRecord {unit_id:string;score:number}
interface JourneyUnit {id:string;progress:number;state:string;lessons?:Array<{id:number;is_completed:boolean;state:string}>}
const LEVEL_META:Record<CEFRLevel,{title:string;desc:string}>={
  A1:{title:'A1 · Starter',desc:'Build your first practical vocabulary and everyday phrases.'},
  A2:{title:'A2 · Elementary',desc:'Understand common situations and speak with more confidence.'},
  B1:{title:'B1 · Intermediate',desc:'Express ideas, follow conversations, and read with independence.'},
  B2:{title:'B2 · Upper Intermediate',desc:'Handle richer conversations and more precise language.'},
  C1:{title:'C1 · Advanced',desc:'Develop fluent, nuanced communication for demanding contexts.'},
  C2:{title:'C2 · Mastery',desc:'Refine precise, natural communication across demanding contexts.'},
}
const AR_LEVEL_META:Record<CEFRLevel,{title:string;desc:string}>={
  A1:{title:'A1 · البداية',desc:'ابنِ مفرداتك الأولى والعبارات اليومية العملية.'},
  A2:{title:'A2 · أساسي',desc:'افهم المواقف الشائعة وتحدث بثقة أكبر.'},
  B1:{title:'B1 · متوسط',desc:'عبّر عن أفكارك وتابع المحادثات واقرأ باستقلالية.'},
  B2:{title:'B2 · فوق المتوسط',desc:'تعامل مع محادثات أعمق ولغة أكثر دقة.'},
  C1:{title:'C1 · متقدم',desc:'طوّر تواصلًا طليقًا ودقيقًا في المواقف المتقدمة.'},
  C2:{title:'C2 · إتقان',desc:'حسّن التواصل الطبيعي والدقيق في مختلف المواقف.'},
}
const skills=[{icon:BookOpen,title:'Learn',text:'Build useful language in small, focused steps.',arTitle:'تعلّم',arText:'ابنِ لغة مفيدة بخطوات صغيرة ومركزة.'},{icon:Headphones,title:'Listen',text:'Train your ear with short real-world practice.',arTitle:'استمع',arText:'درّب أذنك بممارسة قصيرة من الواقع.'},{icon:Mic2,title:'Speak',text:'Turn recognition into confident active recall.',arTitle:'تحدث',arText:'حوّل معرفتك إلى استخدام فعلي بثقة.'}]
const places=[{icon:Coffee,title:'Café',text:'Order, ask and respond.',arTitle:'المقهى',arText:'اطلب واسأل وأجب.'},{icon:Utensils,title:'Restaurant',text:'Food, requests and payment.',arTitle:'المطعم',arText:'الطعام والطلبات والدفع.'},{icon:Plane,title:'Travel',text:'Tickets, directions and arrival.',arTitle:'السفر',arText:'التذاكر والاتجاهات والوصول.'},{icon:Briefcase,title:'Work',text:'Meetings and everyday tasks.',arTitle:'العمل',arText:'الاجتماعات والمهام اليومية.'}]
function lessonCount(plan:StudyPlan|null){return plan?.generated_plan?.weekly_plan?.reduce((total,week)=>total+(week.days?.length??0),0)??0}
const clamp=(value:number)=>Math.max(0,Math.min(100,Number.isFinite(value)?value:0))

export default function CoursesPage(){
  const locale=useLocale()
  const rtl=locale==='ar'
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const [plan,setPlan]=useState<StudyPlan|null>(null)
  const [competencies,setCompetencies]=useState<Record<string,number>>({})
  const [levelUnits,setLevelUnits]=useState<Record<CEFRLevel,CurriculumUnit[]>>({} as Record<CEFRLevel,CurriculumUnit[]>)
  const [journeyUnits,setJourneyUnits]=useState<Record<string,JourneyUnit>>({})
  const [loading,setLoading]=useState(true)
  const [loadError,setLoadError]=useState(false)
  const [reload,setReload]=useState(0)
  useEffect(()=>{
    let cancelled=false
    async function load(){
      setLoading(true);setLoadError(false)
      try{
        const language=activeLanguage?.code??'en-GB'
        const [planRes,compRes,journeyRes,...curriculumResponses]=await Promise.all([
          apiFetch('/api/study-plan/current').catch(()=>null),apiFetch('/api/progress/competencies').catch(()=>null),apiFetch('/api/study-plan/learning-path').catch(()=>null),...CEFR_LEVELS.map(level=>getCurriculumUnits(level,language).catch(()=>[])),
        ])
        const nextPlan=planRes?.ok?await planRes.json() as StudyPlan:null
        const nextCompetencies:Record<string,number>={}
        if(compRes?.ok){const raw=await compRes.json();if(Array.isArray(raw)){for(const item of raw as CompetencyRecord[])nextCompetencies[item.unit_id]=item.score}else if(raw&&typeof raw==='object')Object.assign(nextCompetencies,raw as Record<string,number>)}
        const nextJourney:Record<string,JourneyUnit>={}
        if(journeyRes?.ok){const journey=await journeyRes.json();for(const section of journey.sections??[])for(const unit of section.units??[])nextJourney[unit.id]=unit}
        if(cancelled)return
        setPlan(nextPlan);setCompetencies(nextCompetencies);setJourneyUnits(nextJourney)
        setLevelUnits(Object.fromEntries(CEFR_LEVELS.map((level,index)=>[level,curriculumResponses[index]??[]])) as Record<CEFRLevel,CurriculumUnit[]>)
        if(!planRes||!compRes||!journeyRes||(!compRes.ok&&compRes.status>=500)||(!journeyRes.ok&&journeyRes.status>=500))setLoadError(true)
      }catch{if(!cancelled)setLoadError(true)}finally{if(!cancelled)setLoading(false)}
    }
    void load();return ()=>{cancelled=true}
  },[activeLanguage?.code,reload])
  const currentLevel=plan?.cefr_level??null
  const currentIndex=currentLevel?CEFR_LEVELS.indexOf(currentLevel):0
  const currentUnits=currentLevel?(levelUnits[currentLevel]??[]):[]
  const currentProgress=useMemo(()=>{
    if(!currentUnits.length)return 0
    const scores=currentUnits.map(unit=>journeyUnits[unit.id]?.progress).filter((score):score is number=>typeof score==='number')
    if(scores.length)return Math.round(scores.reduce((sum,score)=>sum+score,0)/scores.length*100)
    return Math.round(currentUnits.reduce((sum,unit)=>sum+(competencies[unit.id]??0),0)/currentUnits.length*100)
  },[competencies,currentUnits,journeyUnits])
  const totalUnits=CEFR_LEVELS.reduce((sum,level)=>sum+(levelUnits[level]?.length??0),0)
  const Arrow=rtl?ChevronLeft:ChevronRight
  return <div className="juba-page-shell reference-courses" dir={rtl?'rtl':'ltr'}>
    <header className="reference-course-heading"><BookOpen size={40} aria-hidden="true"/><div><h1>{rtl?'الكورسات':'Courses'}</h1><p>{rtl?'تعلّم لغة يمكنك استخدامها فعليًا.':'Learn language you can actually use.'}</p></div><div className="reference-course-heading-actions"><Link href="/plan" className="juba-primary-button">{rtl?'تابع مسارك':'Continue journey'}<Arrow size={16}/></Link><Link href="/assessment" className="juba-secondary-button">{rtl?'حدد مستواي':'Find my level'}</Link></div></header>
    {loadError&&<div className="reference-course-error" role="alert"><span>{rtl?'تعذر تحميل بعض بيانات التقدم.':'Some progress data could not be loaded.'}</span><button className="juba-secondary-button" onClick={()=>setReload(value=>value+1)} disabled={loading}>{rtl?'إعادة المحاولة':'Retry'}</button></div>}
    <div className="reference-course-layout"><div className="reference-course-primary">
      <section className="reference-course-summary" aria-label={rtl?'ملخص التقدم':'Progress summary'}><div><h2>{rtl?'تقدم الكورس':'Course progress'}</h2><strong>{currentLevel??(rtl?'لم يُحدد بعد':'Not set')}</strong><div className="reference-course-track" role="progressbar" aria-label={rtl?'تقدم الكورس الحالي':'Current course progress'} aria-valuemin={0} aria-valuemax={100} aria-valuenow={clamp(currentProgress)}><span style={{width:clamp(currentProgress)+'%'}}/></div><p>{clamp(currentProgress)}%</p></div><div><h2>{rtl?'دروس خطتك':'Plan lessons'}</h2><strong>{loading?'…':lessonCount(plan)}</strong><p>{rtl?'تابع التعلم من خطتك الحالية.':'Continue learning from your current plan.'}</p><Link href="/plan">{rtl?'فتح الخطة':'Open learning plan'}<Arrow size={14}/></Link></div></section>
      <section className="reference-course-panel" aria-labelledby="course-levels"><div className="reference-course-panel-head"><h2 id="course-levels">{rtl?'المستويات':'Course levels'}</h2><span>CEFR · {CEFR_LEVELS.length}</span></div>{loading?<div className="reference-course-loading" role="status" aria-label={rtl?'جارٍ تحميل الكورسات':'Loading courses'}>{CEFR_LEVELS.map(level=><div key={level} className="reference-course-skeleton" aria-hidden="true"/>)}</div>:CEFR_LEVELS.map((level,index)=>{
        const unlocked=currentLevel?index<=currentIndex:index===0
        const current=level===currentLevel
        const units=levelUnits[level]??[]
        const journey=units.map(unit=>journeyUnits[unit.id]).filter(Boolean)
        const totalLessons=journey.reduce((sum,unit)=>sum+(unit?.lessons?.length??0),0)
        const progress=clamp(current?currentProgress:journey.length?Math.round(journey.reduce((sum,unit)=>sum+(unit?.progress??0),0)/journey.length*100):0)
        const count=current?Math.max(lessonCount(plan),totalLessons):totalLessons||units.reduce((sum,unit)=>sum+unit.lesson_types.length,0)
        const meta=(rtl?AR_LEVEL_META:LEVEL_META)[level]
        return <article className="reference-course-row" key={level} data-current={current}><span className="reference-course-level">{level}</span><div className="reference-course-row-copy"><h3>{meta.title}{current&&<span className="juba-badge">{rtl?'المستوى الحالي':'Current level'}</span>}</h3><p>{meta.desc}</p><div className="reference-course-row-meta"><span>{count} {rtl?'درسًا':'lessons'}</span><span>{progress}%</span></div><div className="reference-course-track" role="progressbar" aria-label={level+' '+(rtl?'تقدم الكورس':'course progress')} aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress}><span style={{width:progress+'%'}}/></div></div><div className="reference-course-row-action">{unlocked?<><CheckCircle2 size={18} aria-hidden="true"/><Link className="juba-secondary-button" href={current?'/plan':'/courses/'+level}>{current?(rtl?'فتح الخطة':'Open learning plan'):(rtl?'استكشف المستوى':'Explore level')}<Arrow size={14}/></Link></>:<span className="reference-course-locked"><LockKeyhole size={16}/>{rtl?'يُفتح لاحقًا':'Unlock later'}</span>}</div></article>
      })}{!loading&&!totalUnits&&<div className="reference-course-empty"><BookOpen size={24}/><p>{rtl?'لا توجد وحدات متاحة لهذه اللغة حاليًا.':'No curriculum units are currently available for this language.'}</p><button className="juba-secondary-button" onClick={()=>setReload(value=>value+1)}>{rtl?'تحديث':'Refresh'}</button></div>}</section>
    </div><aside className="reference-course-secondary">
      <section className="reference-course-panel"><div className="reference-course-panel-head"><h2>{rtl?'الممارسة':'Practice'}</h2></div><p className="reference-course-intro">{rtl?'تقدم في مواقف عملية وقوِّ ذاكرتك وافتح الخطوة التالية.':'Move through practical situations, strengthen your memory, and unlock the next part of your journey one mission at a time.'}</p>{skills.map(({icon:Icon,title,text,arTitle,arText})=><div className="reference-course-resource" key={title}><Icon size={20} aria-hidden="true"/><div><strong>{rtl?arTitle:title}</strong><p>{rtl?arText:text}</p></div></div>)}</section>
      <section className="reference-course-panel"><div className="reference-course-panel-head"><h2>{rtl?'مهام من الواقع':'Real-world missions'}</h2><Link href="/plan" aria-label={rtl?'عرض مساري':'See my journey'}><Arrow size={16}/></Link></div>{places.map(({icon:Icon,title,text,arTitle,arText})=><div className="reference-course-resource" key={title}><Icon size={20} aria-hidden="true"/><div><strong>{rtl?arTitle:title}</strong><p>{rtl?arText:text}</p></div></div>)}</section>
      <section className="reference-course-panel"><div className="reference-course-panel-head"><h2>{rtl?'إيقاع JUBA':'The JUBA rhythm'}</h2></div><ol className="reference-course-rhythm">{(rtl?['تعلّم','مارس','استرجع','راجع']:['Learn','Practice','Recall','Review']).map((step,index)=><li key={step}><span>{String(index+1).padStart(2,'0')}</span>{step}</li>)}</ol></section>
    </aside></div>
  </div>
}
