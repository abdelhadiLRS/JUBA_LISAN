'use client'

import { useState, useEffect, useMemo } from 'react'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { Library, Search, ChevronRight, ChevronLeft, Flame, Trophy, CheckCircle2 } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import type { VocabularySet } from '@/data/types'
import { CEFR_LEVELS, type CEFRLevel } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
import { useAuthStore } from '@/store/auth'
import './vocabulary-reference.css'

type GuestWord={word:string;translation:string;source?:string;target?:string}
type ProgressSummary={total_xp:number;current_streak:number;total_lessons:number;total_exercises:number;exercises_correct:number;accuracy:number;vocabulary_level?:string;vocabulary_mastered?:number;vocabulary_total?:number;vocabulary_progress?:number}
function readGuestWords():GuestWord[]{if(typeof window==='undefined')return [];try{const value:unknown=JSON.parse(window.localStorage.getItem('juba_lisan_saved_vocabulary')||'[]');return Array.isArray(value)?value.filter((item):item is GuestWord=>!!item&&typeof item==='object'&&typeof item.word==='string'&&typeof item.translation==='string'):[]}catch{return []}}
export default function VocabularyIndexPage(){
  const t=useTranslations('vocabulary')
  const tCommon=useTranslations('common')
  const locale=useLocale()
  const rtl=locale==='ar'
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const authenticated=!!useAuthStore(s=>s.accessToken)
  const [activeLevel,setActiveLevel]=useState<CEFRLevel|'All'>('All')
  const [search,setSearch]=useState('')
  const [vocabSets,setVocabSets]=useState<VocabularySet[]>([])
  const [guestWords,setGuestWords]=useState<GuestWord[]>([])
  const [progress,setProgress]=useState<ProgressSummary|null>(null)
  const [loading,setLoading]=useState(true)
  const [loadError,setLoadError]=useState(false)
  const [progressError,setProgressError]=useState(false)
  const [reload,setReload]=useState(0)
  useEffect(()=>{
    let cancelled=false
    setGuestWords(readGuestWords());setLoading(true);setLoadError(false);setProgressError(false)
    const lang=activeLanguage?.code??'en-GB'
    apiFetch(`/api/vocabulary?language=${lang}`).then(res=>res.ok?res.json():Promise.reject()).then((data:{sets:VocabularySet[]})=>{if(!cancelled)setVocabSets(data.sets)}).catch(()=>{if(!cancelled){setVocabSets([]);setLoadError(true)}}).finally(()=>{if(!cancelled)setLoading(false)})
    if(authenticated)apiFetch('/api/progress/summary').then(res=>res.ok?res.json():Promise.reject()).then((data:ProgressSummary)=>{if(!cancelled)setProgress(data)}).catch(()=>{if(!cancelled){setProgress(null);setProgressError(true)}})
    else setProgress(null)
    return ()=>{cancelled=true}
  },[activeLanguage?.code,authenticated,reload])
  const filtered=useMemo(()=>{const q=search.toLowerCase();return vocabSets.filter(set=>(activeLevel==='All'||set.level===activeLevel)&&(!q||set.topic.toLowerCase().includes(q)||set.id.includes(q)))},[vocabSets,activeLevel,search])
  const totalWords=vocabSets.reduce((total,set)=>total+set.words.length,0)
  const usedLevels=CEFR_LEVELS.filter(level=>vocabSets.some(set=>set.level===level))
  const hasFilters=Boolean(search)||activeLevel!=='All'
  const pct=Math.max(0,Math.min(100,(progress?.vocabulary_progress??0)*100))
  const Forward=rtl?ChevronLeft:ChevronRight
  return <div className="juba-page-shell reference-vocabulary" dir={rtl?'rtl':'ltr'}>
    <header className="reference-vocab-header"><Library size={40} aria-hidden="true"/><div><h1>{t('title')}</h1><p>{vocabSets.length} {t('sets')} · {totalWords} {t('words')}{usedLevels.length>0?` · ${usedLevels[0]} - ${usedLevels[usedLevels.length-1]}`:''}</p></div>{authenticated&&<Link href="/vocabulary/review" className="juba-primary-button">{rtl?'ابدأ المراجعة':'Start review'}<Forward size={16}/></Link>}</header>
    {authenticated&&progress&&<section className="reference-vocab-panel"><div className="reference-vocab-stats"><div><Trophy size={18}/><span>XP</span><strong>{progress.total_xp}</strong></div><div><Flame size={18}/><span>{rtl?'السلسلة':'Streak'}</span><strong>{progress.current_streak} {rtl?'أيام':'days'}</strong></div><div><CheckCircle2 size={18}/><span>{rtl?'الدقة':'Accuracy'}</span><strong>{Math.round(progress.accuracy*100)}%</strong></div><div><Library size={18}/><span>{rtl?'المتقن':'Mastered'}</span><strong>{progress.vocabulary_mastered??0} / {progress.vocabulary_total??0}</strong></div></div><div className="reference-vocab-progress"><div><span>{rtl?'تقدم المفردات':'Vocabulary progress'}</span><strong>{Math.round(pct)}%</strong></div><div className="reference-vocab-track" role="progressbar" aria-label={t('title')} aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(pct)}><span style={{width:pct+'%'}}/></div></div></section>}
    {progressError&&<div className="reference-vocab-alert" role="alert"><span>{tCommon('error')}</span><button className="juba-secondary-button" onClick={()=>setReload(value=>value+1)}>{tCommon('retry')}</button></div>}
    {!authenticated&&guestWords.length>0&&<section className="reference-vocab-panel"><header className="reference-vocab-panel-head"><h2>{rtl?'كلماتك المحفوظة على الجهاز':'Your saved words on this device'}</h2><Link href="/translator">{rtl?'ترجم المزيد':'Translate more'}<Forward size={14}/></Link></header><p className="reference-vocab-intro">{guestWords.length} {rtl?'كلمة محفوظة من المترجم.':'saved words from Instant Translator.'}</p><div className="reference-vocab-saved">{guestWords.slice(0,6).map((item,index)=><div key={item.word+'-'+index}><strong dir="auto">{item.word}</strong><span dir="auto">{item.translation}</span></div>)}</div></section>}
    <section className="reference-vocab-panel reference-vocab-filters" aria-label={t('searchPlaceholder')}><label className="reference-vocab-search"><Search size={18} aria-hidden="true"/><input className="juba-input" type="search" value={search} onChange={event=>setSearch(event.target.value)} placeholder={t('searchPlaceholder')} aria-label={t('searchPlaceholder')} autoComplete="off"/></label><div className="reference-vocab-tabs" role="group" aria-label={t('all')}><button onClick={()=>setActiveLevel('All')} aria-pressed={activeLevel==='All'}>{t('all')}</button>{usedLevels.map(level=><button key={level} onClick={()=>setActiveLevel(activeLevel===level?'All':level)} aria-pressed={activeLevel===level}>{level}</button>)}</div></section>
    {loading?<section className="reference-vocab-loading" role="status" aria-label={rtl?'جارٍ تحميل المفردات':'Loading vocabulary'}>{[0,1,2].map(index=><div key={index} aria-hidden="true"/>)}</section>:loadError?<section className="reference-vocab-empty" role="alert"><Library size={28}/><p>{tCommon('error')}</p><button className="juba-secondary-button" onClick={()=>setReload(value=>value+1)}>{tCommon('retry')}</button></section>:<>
      {CEFR_LEVELS.map(level=>{const sets=filtered.filter(set=>set.level===level);return sets.length?<section className="reference-vocab-panel" key={level} aria-labelledby={'vocab-'+level}><header className="reference-vocab-panel-head"><h2 id={'vocab-'+level}>{level}</h2><span>{sets.length} {t('sets')} · {sets.reduce((sum,set)=>sum+set.words.length,0)} {t('words')}</span></header>{sets.map(set=><Link className="reference-vocab-set-row" href={'/vocabulary/'+set.id} key={set.id}><span className="reference-vocab-set-icon"><Library size={20}/></span><div><strong>{set.topic}</strong><small>{set.words.length} {t('words')} · {set.unit_ref}</small></div><span className="juba-badge">{set.level}</span><Forward size={16} aria-hidden="true"/></Link>)}</section>:null})}
      {!filtered.length&&<section className="reference-vocab-empty"><Library size={28}/><p>{t('noResults')}</p>{hasFilters&&<button className="juba-secondary-button" onClick={()=>{setSearch('');setActiveLevel('All')}}>{tCommon('clearFilters')}</button>}</section>}
    </>}
  </div>
}
