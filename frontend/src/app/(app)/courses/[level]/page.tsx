'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { BookOpen, LockKeyhole, CheckCircle2, ChevronLeft, ChevronRight } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { CEFR_LEVELS, getCurriculumUnits, type CEFRLevel, type CurriculumUnit } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
import '../courses-reference.css'

interface StudyPlan {cefr_level:CEFRLevel}
interface JourneyUnit {id:string;progress:number;state:string;lessons?:Array<{id:number;title:string;lesson_type:string;is_completed:boolean;available:boolean;state:string}>}
interface JourneyResponse {sections?:Array<{units?:JourneyUnit[]}>}
const clamp=(value:number)=>Math.max(0,Math.min(100,Number.isFinite(value)?value:0))

export default function CourseLevelPage(){
  const params=useParams()
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const t=useTranslations('courseLevel')
  const locale=useLocale()
  const rtl=locale==='ar'
  const requestedLevel=String(params.level??'').toUpperCase() as CEFRLevel
  const level=CEFR_LEVELS.includes(requestedLevel)?requestedLevel:null
  const [units,setUnits]=useState<CurriculumUnit[]>([])
  const [plan,setPlan]=useState<StudyPlan|null>(null)
  const [journeyUnits,setJourneyUnits]=useState<Record<string,JourneyUnit>>({})
  const [loading,setLoading]=useState(true)
  const [loadError,setLoadError]=useState(false)
  const [reload,setReload]=useState(0)
  useEffect(()=>{
    if(!level){setLoading(false);return}
    const curriculumLevel=level
    let cancelled=false
    async function load(){
      setLoading(true);setLoadError(false)
      try{
        const [curriculum,planRes,journeyRes]=await Promise.all([getCurriculumUnits(curriculumLevel,activeLanguage?.code??'en-GB'),apiFetch('/api/study-plan/current').catch(()=>null),apiFetch('/api/study-plan/learning-path').catch(()=>null)])
        const nextPlan=planRes?.ok?await planRes.json() as StudyPlan:null
        const map:Record<string,JourneyUnit>={}
        if(journeyRes?.ok){const journey=await journeyRes.json() as JourneyResponse;for(const section of journey.sections??[])for(const unit of section.units??[])map[unit.id]=unit}
        if(cancelled)return
        setUnits(curriculum);setPlan(nextPlan);setJourneyUnits(map)
        if(!planRes||!journeyRes||(!journeyRes.ok&&journeyRes.status>=500))setLoadError(true)
      }catch{if(!cancelled)setLoadError(true)}finally{if(!cancelled)setLoading(false)}
    }
    void load();return ()=>{cancelled=true}
  },[activeLanguage?.code,level,reload])
  const isCurrentLevel=Boolean(level&&plan?.cefr_level===level)
  const currentIndex=plan?CEFR_LEVELS.indexOf(plan.cefr_level):-1
  const levelIndex=level?CEFR_LEVELS.indexOf(level):-1
  const levelUnlocked=levelIndex>=0&&(currentIndex<0?levelIndex===0:levelIndex<=currentIndex)
  const totals=useMemo(()=>({completed:units.reduce((sum,unit)=>sum+(journeyUnits[unit.id]?.lessons?.filter(lesson=>lesson.is_completed).length??0),0),available:units.reduce((sum,unit)=>sum+(journeyUnits[unit.id]?.lessons?.filter(lesson=>lesson.available).length??0),0)}),[journeyUnits,units])
  const formatLessonType=(type:string)=>{
    const normalized=type.trim().toLowerCase()
    if(/listen|audio/.test(normalized))return t('lessonTypes.listening')
    if(/read/.test(normalized))return t('lessonTypes.reading')
    if(/write/.test(normalized))return t('lessonTypes.writing')
    if(/grammar/.test(normalized))return t('lessonTypes.grammar')
    if(/vocab/.test(normalized))return t('lessonTypes.vocabulary')
    if(/review/.test(normalized))return t('lessonTypes.review')
    return type
  }
  const Forward=rtl?ChevronLeft:ChevronRight
  const Back=rtl?ChevronRight:ChevronLeft
  if(!level)return <div className="juba-page-shell"><section className="reference-course-empty"><BookOpen size={32}/><h1>{t('notFound')}</h1><p>{t('choose')}</p><Link href="/courses" className="juba-secondary-button"><Back size={16}/>{t('back')}</Link></section></div>
  return <div className="juba-page-shell reference-course-detail" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-course-detail{display:flex;flex-direction:column;gap:24px;}
      .juba-app-shell .reference-course-back{display:inline-flex;align-items:center;gap:8px;color:var(--juba-muted);font-size:13px;min-height:36px;align-self:flex-start;}
      .juba-app-shell .reference-course-detail-summary{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding:16px;border:1px solid var(--juba-border);border-radius:6px;}
      .juba-app-shell .reference-course-detail-summary>span{display:flex;align-items:center;gap:6px;font-size:13px;color:var(--juba-muted);font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-course-detail-summary strong{color:var(--juba-ink);font-size:16px;}
      .juba-app-shell .reference-course-lock{display:flex;align-items:flex-start;gap:12px;padding:16px;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-soft);}
      .juba-app-shell .reference-course-lock>svg{flex:none;color:var(--juba-muted);}
      .juba-app-shell .reference-course-lock h2{font-size:15px;font-weight:650;margin:0;}
      .juba-app-shell .reference-course-lock p{font-size:13px;line-height:1.6;color:var(--juba-muted);margin:6px 0 0;}
      .juba-app-shell .reference-unit-list{display:flex;flex-direction:column;gap:24px;}
      .juba-app-shell .reference-unit{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
      .juba-app-shell .reference-unit-head{display:flex;align-items:center;gap:12px;padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-unit-head>div{flex:1;min-width:0;}
      .juba-app-shell .reference-unit-head small{font-size:11px;color:var(--juba-muted);}
      .juba-app-shell .reference-unit-head h2{font-size:17px;font-weight:650;line-height:1.4;margin:4px 0 0;}
      .juba-app-shell .reference-unit-head>svg{color:var(--juba-green-dark);}
      .juba-app-shell .reference-unit-body{display:grid;grid-template-columns:minmax(0,1fr) minmax(240px,.7fr);gap:24px;padding:16px;}
      .juba-app-shell .reference-unit-tags{display:flex;flex-wrap:wrap;gap:6px;}
      .juba-app-shell .reference-unit-tags>span{font-size:11px;color:var(--juba-muted);padding:4px 8px;border-radius:4px;background:var(--juba-soft);}
      .juba-app-shell .reference-unit-stats{display:flex;flex-wrap:wrap;gap:12px 20px;margin-block:16px;}
      .juba-app-shell .reference-unit-stats>div{display:flex;align-items:center;gap:8px;}
      .juba-app-shell .reference-unit-stats dt{font-size:11px;color:var(--juba-muted);}
      .juba-app-shell .reference-unit-stats dd{margin:0;font-size:14px;font-weight:650;}
      .juba-app-shell .reference-unit-competencies h3{font-size:13px;font-weight:650;margin:0 0 8px;}
      .juba-app-shell .reference-unit-competencies ul{padding:0;list-style:none;margin:0;display:flex;flex-direction:column;gap:8px;}
      .juba-app-shell .reference-unit-competencies li{display:flex;align-items:flex-start;gap:8px;font-size:13px;line-height:1.6;color:var(--juba-muted);}
      .juba-app-shell .reference-unit-competencies svg{flex:none;color:var(--juba-green-dark);margin-block-start:3px;}
      .juba-app-shell .reference-unit-progress-meta{display:flex;justify-content:space-between;gap:8px;font-size:12px;color:var(--juba-muted);margin-block-end:8px;}
      .juba-app-shell .reference-unit-lessons{display:flex;flex-direction:column;margin-block-start:12px;}
      .juba-app-shell .reference-unit-lessons>a,.juba-app-shell .reference-unit-lessons>div{display:flex;align-items:center;gap:8px;padding-block:12px;border-block-end:1px solid var(--juba-border);font-size:13px;color:var(--juba-ink);text-decoration:none;}
      .juba-app-shell .reference-unit-lessons>div{color:var(--juba-muted);}
      .juba-app-shell .reference-unit-lessons>a:hover{color:var(--juba-green-dark);}
      .juba-app-shell .reference-unit-lessons strong{flex:1;min-width:0;font-size:13px;font-weight:550;overflow-wrap:anywhere;}
      .juba-app-shell .reference-unit-lessons small{font-size:10px;color:var(--juba-muted);}
      .juba-app-shell .reference-unit-plan{display:inline-flex;align-items:center;gap:8px;min-height:40px;margin-block-start:16px;}
      .juba-app-shell .reference-course-continue{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:16px;border:1px solid var(--juba-border);border-radius:6px;}
      .juba-app-shell .reference-course-continue h2{font-size:18px;font-weight:650;margin:0;}
      .juba-app-shell .reference-course-continue p{font-size:13px;color:var(--juba-muted);margin:6px 0 0;}
      .juba-app-shell .reference-course-continue a{padding-inline:16px;}
      @media(max-width:850px){.juba-app-shell .reference-unit-body{grid-template-columns:1fr;gap:16px;}.juba-app-shell .reference-course-detail,.juba-app-shell .reference-unit-list{gap:16px;}.juba-app-shell .reference-course-back{min-height:44px;}}
    `}</style>
    <Link href="/courses" className="reference-course-back"><Back size={16} aria-hidden="true"/>{t('all')}</Link>
    <header className="reference-course-heading"><span className="reference-course-level">{level}</span><div><h1>{t(`levels.${level}.title`)}</h1><p>{t(`levels.${level}.description`)}</p></div></header>
    <div className="reference-course-detail-summary"><span><strong>{units.length}</strong>{t('units')}</span>{isCurrentLevel&&<><span><strong>{totals.completed}</strong>{t('completed')}</span><span><strong>{totals.available}</strong>{t('ready')}</span></>}</div>
    {loadError&&<div className="reference-course-error" role="alert"><span>{rtl?'تعذر تحميل بعض بيانات المستوى.':'Some level data could not be loaded.'}</span><button className="juba-secondary-button" onClick={()=>setReload(value=>value+1)} disabled={loading}>{rtl?'إعادة المحاولة':'Retry'}</button></div>}
    {!loading&&!levelUnlocked&&<section className="reference-course-lock"><LockKeyhole size={20}/><div><h2>{t('notUnlocked')}</h2><p>{t('unlockDesc')}</p></div></section>}
    <div className="reference-unit-list">{loading?<div className="reference-course-loading" role="status" aria-label={rtl?'جارٍ تحميل الوحدات':'Loading units'}>{[0,1,2,3].map(index=><div className="reference-course-skeleton" key={index} aria-hidden="true"/>)}</div>:units.map(unit=>{
      const journey=journeyUnits[unit.id]
      const progress=clamp(Math.round((journey?.progress??0)*100))
      const lessons=journey?.lessons??[]
      const state=journey?.state??(unit.prerequisite_unit?'locked':'available')
      const canOpen=levelUnlocked&&state!=='locked'
      const stats=[{label:t('grammar'),value:unit.grammar_points.length},{label:t('vocab'),value:unit.vocabulary_set_ids.length},{label:t('competencies'),value:unit.competency_checklist.length},{label:t('listening'),value:lessons.filter(lesson=>/listen|listening|audio/i.test(lesson.lesson_type)).length},{label:t('reading'),value:lessons.filter(lesson=>/read|reading/i.test(lesson.lesson_type)).length}]
      return <article className="reference-unit" key={unit.id}><header className="reference-unit-head"><span className="reference-course-level">{String(unit.unit_number).padStart(2,'0')}</span><div><small>{unit.level} · {t('unit')} {unit.unit_number}</small><h2>{unit.title}</h2></div>{state==='completed'?<CheckCircle2 size={20} aria-label={t('completed')}/>:!canOpen?<LockKeyhole size={18} aria-label={t('locked')}/>:null}</header><div className="reference-unit-body"><div><div className="reference-unit-tags">{unit.lesson_types.map(type=><span key={type}>{formatLessonType(type)}</span>)}{unit.grammar_points.slice(0,3).map(point=><span key={point}>{point}</span>)}</div><dl className="reference-unit-stats">{stats.map(({label,value})=><div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl>{unit.competency_checklist.length>0&&<section className="reference-unit-competencies"><h3>{t('byEnd')}</h3><ul>{unit.competency_checklist.slice(0,2).map(item=><li key={item}><CheckCircle2 size={14} aria-hidden="true"/><span>{item}</span></li>)}</ul></section>}</div><div><div className="reference-unit-progress-meta"><span>{progress}% {t('mastery')}</span><span>{lessons.length} {t('lessons')}</span></div><div className="reference-course-track" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress} aria-label={`${unit.title}: ${t('mastery')}`}><span style={{width:progress+'%'}}/></div>{canOpen&&lessons.length>0?<div className="reference-unit-lessons">{lessons.slice(0,3).map(lesson=>lesson.available||lesson.is_completed?<Link key={lesson.id} href={'/lesson/'+lesson.id} aria-label={lesson.title+' · '+formatLessonType(lesson.lesson_type)}><strong>{lesson.title}</strong><small>{formatLessonType(lesson.lesson_type)}</small>{lesson.is_completed?<CheckCircle2 size={16}/>:<Forward size={16}/>}</Link>:<div key={lesson.id} aria-disabled="true" aria-label={lesson.title+' · '+t('locked')}><strong>{lesson.title}</strong><LockKeyhole size={16}/></div>)}</div>:canOpen?<Link href="/plan" className="juba-secondary-button reference-unit-plan">{t('openPlan')}<Forward size={16}/></Link>:<span className="reference-course-locked reference-unit-plan"><LockKeyhole size={16}/>{t('locked')}</span>}</div></div></article>
    })}</div>
    {!loading&&!units.length&&<section className="reference-course-empty"><BookOpen size={24}/><p>{rtl?'لا توجد وحدات متاحة لهذا المستوى واللغة.':'No units are currently available for this level and language.'}</p><button className="juba-secondary-button" onClick={()=>setReload(value=>value+1)}>{rtl?'تحديث':'Refresh'}</button></section>}
    {isCurrentLevel&&<section className="reference-course-continue"><div><p>{t('keepMoving')}</p><h2>{t('continue')}</h2><p>{t('continueDesc')}</p></div><Link className="juba-primary-button" href="/plan">{t('openLearning')}<BookOpen size={16}/></Link></section>}
  </div>
}
