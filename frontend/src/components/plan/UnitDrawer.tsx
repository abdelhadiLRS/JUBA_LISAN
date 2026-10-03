'use client'

import { useEffect, useId, useRef } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { Check, Circle, X, ChevronLeft, ChevronRight } from 'lucide-react'
import type { CurriculumUnit } from '@/data/curriculum'
interface Lesson{id:number|null;title:string;lesson_type:string;week:number;day:number;completed:boolean;action?:'start'|'continue'|'review'}
interface Props{unit:CurriculumUnit;lessons:Lesson[];onClose:()=>void;onStartLesson:(lessonId:number)=>void;onStartUnit?:()=>void}
export default function UnitDrawer({unit,lessons,onClose,onStartLesson,onStartUnit}:Props){
  const t=useTranslations('plan')
  const tCommon=useTranslations('common')
  const rtl=useLocale()==='ar'
  const ref=useRef<HTMLDivElement>(null)
  const closeRef=useRef(onClose)
  closeRef.current=onClose
  const titleId=useId()
  const completed=lessons.filter(lesson=>lesson.completed).length
  const progress=lessons.length?Math.round(completed/lessons.length*100):0
  const nextLesson=lessons.find(lesson=>lesson.id!==null&&!lesson.completed&&(lesson.action==='start'||lesson.action==='continue'))
  const canStart=Boolean(onStartUnit||nextLesson)
  const Forward=rtl?ChevronLeft:ChevronRight
  useEffect(()=>{
    const previous=document.activeElement as HTMLElement|null
    const panel=ref.current
    const previousOverflow=document.body.style.overflow
    document.body.style.overflow='hidden'
    panel?.focus()
    function keydown(event:KeyboardEvent){
      if(event.key==='Escape'){event.preventDefault();closeRef.current();return}
      if(event.key!=='Tab')return
      const focusable=Array.from(panel?.querySelectorAll<HTMLElement>('button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex="0"]')??[]).filter(element=>!element.closest('[hidden]'))
      if(!focusable.length){event.preventDefault();panel?.focus();return}
      const first=focusable[0];const last=focusable[focusable.length-1]
      if(event.shiftKey&&(document.activeElement===first||!panel?.contains(document.activeElement)||document.activeElement===panel)){event.preventDefault();last.focus()}
      else if(!event.shiftKey&&(document.activeElement===last||!panel?.contains(document.activeElement)||document.activeElement===panel)){event.preventDefault();first.focus()}
    }
    document.addEventListener('keydown',keydown)
    return ()=>{document.body.style.overflow=previousOverflow;document.removeEventListener('keydown',keydown);previous?.focus()}
  },[])
  const lessonTypeLabel:Record<string,string>={grammar:t('lessonTypes.grammar'),vocabulary:t('lessonTypes.vocabulary'),reading:t('lessonTypes.reading'),writing:t('lessonTypes.writing'),listening:t('lessonTypes.listening'),conversation:t('lessonTypes.conversation'),review:t('lessonTypes.review'),level_test:t('lessonTypes.level_test')}
  function startUnit(){if(onStartUnit)onStartUnit();else if(nextLesson?.id!=null)onStartLesson(nextLesson.id)}
  return <div className="learning-unit-overlay" onMouseDown={event=>{if(event.target===event.currentTarget)onClose()}}>
    <style>{`
      .juba-app-shell .learning-unit-overlay{position:fixed;inset:0;z-index:60;display:flex;align-items:center;justify-content:center;padding:24px;background:oklch(25% .01 130 / .4);}
      .juba-app-shell .learning-unit-drawer{display:flex;flex-direction:column;width:100%;max-width:640px;max-height:calc(100dvh - 48px);min-height:0;overflow:hidden;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);color:var(--juba-ink);box-shadow:0 8px 32px oklch(25% .01 130 / .08);}
      .juba-app-shell .learning-unit-header{display:flex;align-items:center;gap:16px;padding:16px;border-block-end:1px solid var(--juba-border);flex:none;}
      .juba-app-shell .learning-unit-header>div{flex:1;min-width:0;}
      .juba-app-shell .learning-unit-header small{font-size:11px;color:var(--juba-green-dark);}
      .juba-app-shell .learning-unit-header h2{font-size:18px;line-height:1.5;font-weight:650;margin:4px 0 0;overflow-wrap:anywhere;}
      .juba-app-shell .learning-unit-close{display:grid;place-items:center;width:40px;height:40px;border:0;border-radius:5px;background:transparent;color:var(--juba-muted);flex:none;}
      .juba-app-shell .learning-unit-scroll{min-height:0;overflow-y:auto;overscroll-behavior:contain;}
      .juba-app-shell .learning-unit-progress{padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .learning-unit-progress>div:first-child{display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:12px;color:var(--juba-muted);margin-block-end:8px;}
      .juba-app-shell .learning-unit-track{height:8px;border-radius:3px;background:var(--juba-soft);overflow:hidden;}
      .juba-app-shell .learning-unit-track>span{display:block;height:100%;background:var(--juba-yellow);}
      .juba-app-shell .learning-unit-grammar{padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .learning-unit-grammar h3{font-size:13px;font-weight:650;margin:0 0 12px;}
      .juba-app-shell .learning-unit-grammar>div{display:flex;gap:6px;flex-wrap:wrap;}
      .juba-app-shell .learning-unit-grammar span{font-size:11px;color:var(--juba-muted);padding:4px 8px;border-radius:4px;background:var(--juba-soft);}
      .juba-app-shell .learning-unit-lessons-title{padding:12px 16px;margin:0;font-size:13px;font-weight:650;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .learning-unit-lessons{list-style:none;padding:0;margin:0;}
      .juba-app-shell .learning-unit-lessons li{display:flex;align-items:center;gap:12px;padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .learning-unit-lessons li:last-child{border:0;}
      .juba-app-shell .learning-unit-node{display:grid;place-items:center;width:28px;height:28px;border:1px solid var(--juba-border);border-radius:50%;color:var(--juba-muted);flex:none;}
      .juba-app-shell .learning-unit-node[data-done="true"]{color:var(--juba-green-dark);background:var(--juba-green-soft);}
      .juba-app-shell .learning-unit-lessons li>div{flex:1;min-width:0;}
      .juba-app-shell .learning-unit-lessons strong{display:block;font-size:14px;font-weight:600;overflow-wrap:anywhere;}
      .juba-app-shell .learning-unit-lessons p{font-size:11px;color:var(--juba-muted);margin:4px 0 0;}
      .juba-app-shell .learning-unit-lessons button{padding-inline:12px;font-size:12px;}
      .juba-app-shell .learning-unit-empty{padding:24px 16px;font-size:14px;color:var(--juba-muted);margin:0;text-align:center;}
      .juba-app-shell .learning-unit-footer{padding:16px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;border-block-start:1px solid var(--juba-border);flex:none;}
      .juba-app-shell .learning-unit-footer button{padding-inline:16px;}
      @media(max-width:640px){.juba-app-shell .learning-unit-overlay{padding:12px;align-items:flex-end;}.juba-app-shell .learning-unit-drawer{max-height:calc(100dvh - 24px);}.juba-app-shell .learning-unit-close{width:44px;height:44px;}.juba-app-shell .learning-unit-lessons li{flex-wrap:wrap;}.juba-app-shell .learning-unit-lessons button{margin-inline-start:40px;}}
    `}</style>
    <div className="learning-unit-drawer" ref={ref} tabIndex={-1} role="dialog" aria-modal="true" aria-labelledby={titleId} dir={rtl?'rtl':'ltr'}><header className="learning-unit-header"><div><small>{unit.level} · {t('unitLabel')}</small><h2 id={titleId} dir="auto">{unit.title}</h2></div><button className="learning-unit-close" onClick={onClose} aria-label={tCommon('close')}><X size={18}/></button></header><div className="learning-unit-scroll"><section className="learning-unit-progress"><div><span>{t('lessonsHeader',{count:lessons.length})}</span><strong>{completed}/{lessons.length}</strong></div><div className="learning-unit-track" role="progressbar" aria-label={t('lessonsHeader',{count:lessons.length})} aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress}><span style={{width:progress+'%'}}/></div></section>{unit.grammar_points.length>0&&<section className="learning-unit-grammar"><h3>{t('grammarCovered')}</h3><div>{unit.grammar_points.map(point=><span key={point} dir="auto">{point}</span>)}</div></section>}<h3 className="learning-unit-lessons-title">{t('lessonsHeader',{count:lessons.length})}</h3>{!lessons.length?<p className="learning-unit-empty">{t('noLessons')}</p>:<ul className="learning-unit-lessons">{lessons.map((lesson,index)=><li key={lesson.id??index}><span className="learning-unit-node" data-done={lesson.completed} aria-hidden="true">{lesson.completed?<Check size={16}/>:<Circle size={10}/>}</span><div><strong dir="auto">{lesson.title}</strong><p>{t('weekDay',{week:lesson.week,day:lesson.day})} · {lessonTypeLabel[lesson.lesson_type]??lesson.lesson_type}</p></div>{lesson.id!=null&&lesson.action&&<button className="juba-secondary-button" onClick={()=>onStartLesson(lesson.id!)}>{lesson.action==='review'?t('reviewLesson'):lesson.action==='continue'?t('resume'):t('startLearning')}<Forward size={14}/></button>}</li>)}</ul>}</div><footer className="learning-unit-footer">{canStart&&<button className="juba-primary-button" onClick={startUnit}>{tCommon('start')}<Forward size={16}/></button>}<button className="juba-secondary-button" onClick={onClose}>{tCommon('close')}</button></footer></div>
  </div>
}
