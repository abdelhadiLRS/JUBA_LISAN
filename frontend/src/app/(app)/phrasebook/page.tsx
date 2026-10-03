'use client'

import { useCallback, useEffect, useId, useMemo, useState } from 'react'
import { useTranslations } from 'next-intl'
import { BookOpen, Search, Copy, Check, ChevronDown, Languages } from 'lucide-react'
import { getPhrasebookCategories, getPhrasebookNativeHelp, type PhrasebookNativeHelp, type PhrasebookCategory, type Register } from '@/data/phrasebook'
import type { CEFRLevel } from '@/data/types'
import { useLanguageStore } from '@/store/language'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { PageLoading } from '@/components/ui/page-loading'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { useAuthStore } from '@/store/auth'
import '../resource-reference.css'

const CEFR_LEVELS:CEFRLevel[]=['A1','A2','B1','B2','C1','C2']
const REGISTERS:Register[]=['formal','neutral','informal']
function CopyButton({text}:{text:string}){
  const tCommon=useTranslations('common')
  const [copied,setCopied]=useState(false)
  const [failed,setFailed]=useState(false)
  useEffect(()=>{if(!copied)return;const timer=window.setTimeout(()=>setCopied(false),1500);return ()=>window.clearTimeout(timer)},[copied])
  async function handleCopy(){try{await navigator.clipboard.writeText(text);setCopied(true);setFailed(false)}catch{setFailed(true)}}
  return <><button className="reference-phrase-copy" onClick={()=>void handleCopy()} aria-label={copied?'Copied phrase':'Copy phrase'} title={copied?'Copied':'Copy'}>{copied?<Check size={16}/>:<Copy size={16}/>}</button>{failed&&<span className="reference-phrase-copy-error" role="alert">{tCommon('error')}</span>}</>
}
function CategoryCard({cat,registerFilter,search,language}:{cat:PhrasebookCategory;registerFilter:Register|'All';search:string;language:string}){
  const t=useTranslations('phrasebook')
  const tCommon=useTranslations('common')
  const tTargetLang=useTranslations('targetLanguages')
  const user=useAuthStore(s=>s.user)
  const nativeLanguageName=user?.native_language?tTargetLang(user.native_language):''
  const helpId=useId()
  const [nativeHelpOpen,setNativeHelpOpen]=useState(cat.level==='A1'||cat.level==='A2')
  const [nativeHelp,setNativeHelp]=useState<PhrasebookNativeHelp|null>(null)
  const [loadingNativeHelp,setLoadingNativeHelp]=useState(false)
  const [nativeHelpError,setNativeHelpError]=useState(false)
  const phrases=cat.phrases.filter(phrase=>(registerFilter==='All'||phrase.register===registerFilter)&&(!search||phrase.text.toLowerCase().includes(search.toLowerCase())))
  async function generateNativeHelp(){
    if(loadingNativeHelp)return
    setLoadingNativeHelp(true);setNativeHelpError(false)
    try{const help=await getPhrasebookNativeHelp(cat.id,language);if(help)setNativeHelp(help);else setNativeHelpError(true)}catch{setNativeHelpError(true)}finally{setLoadingNativeHelp(false)}
  }
  if(!phrases.length)return null
  return <section className="reference-resource-panel reference-phrase-category"><header className="reference-resource-panel-head"><span className="reference-phrase-category-icon" aria-hidden="true">{cat.icon}</span><h2 dir="auto">{cat.situation}</h2><span className="reference-phrase-level">{cat.level}</span></header>
    <ul className="reference-phrase-list">{phrases.map((phrase,index)=><li key={index}><div className="reference-phrase-text"><TargetLanguageText as="p" languageCode={language} dir="auto">{phrase.text}</TargetLanguageText>{phrase.context&&<TargetLanguageText as="p" languageCode={language} dir="auto" className="reference-resource-caption">{phrase.context}</TargetLanguageText>}</div><div className="reference-phrase-actions"><span className="reference-phrase-register" data-register={phrase.register}>{t(phrase.register)}</span><AudioPlayer text={phrase.text} size="sm" audioUrl={`/api/phrasebook/audio/${encodeURIComponent(cat.id)}/${cat.phrases.indexOf(phrase)}?language=${encodeURIComponent(language)}`}/><CopyButton text={phrase.text}/></div></li>)}</ul>
    {nativeLanguageName&&<div className="reference-phrase-help"><button className="reference-resource-help-toggle" onClick={()=>setNativeHelpOpen(value=>!value)} aria-expanded={nativeHelpOpen} aria-controls={helpId}><Languages size={18}/><span>{tCommon('nativeHelpTitle',{language:nativeLanguageName})}</span><ChevronDown size={16}/></button><div className="reference-resource-body reference-resource-native" id={helpId} hidden={!nativeHelpOpen}>{loadingNativeHelp?<p role="status">{tCommon('nativeHelpLoading',{language:nativeLanguageName})}</p>:nativeHelp?<>
      <p dir="auto">{nativeHelp.summary}</p>
      {nativeHelp.usage_tips.length>0&&<section><h3>{tCommon('nativeHelpUsageTips')}</h3><ul>{nativeHelp.usage_tips.map((tip,index)=><li key={index} dir="auto">{tip}</li>)}</ul></section>}
      {nativeHelp.register_notes.length>0&&<section><h3>{tCommon('nativeHelpRegisterNotes')}</h3>{nativeHelp.register_notes.map((note,index)=><p key={index} dir="auto">{note}</p>)}</section>}
      {nativeHelp.phrase_notes.length>0&&<section><h3>{tCommon('nativeHelpPhraseNotes')}</h3>{nativeHelp.phrase_notes.map((item,index)=><article key={index}><TargetLanguageText as="p" languageCode={language} dir="auto">{item.phrase}</TargetLanguageText><p dir="auto">{item.note}</p></article>)}</section>}
      {nativeHelp.common_traps.length>0&&<section><h3>{tCommon('nativeHelpCommonTraps')}</h3>{nativeHelp.common_traps.map((trap,index)=><article key={index}><p dir="auto">{trap.mistake}</p><p dir="auto">{trap.fix}</p></article>)}</section>}
      {nativeHelp.mini_glossary.length>0&&<section><h3>{tCommon('nativeHelpMiniGlossary')}</h3>{nativeHelp.mini_glossary.map((item,index)=><article key={index}><TargetLanguageText languageCode={language} dir="auto" className="font-semibold">{item.term}</TargetLanguageText><p dir="auto">{item.meaning}</p>{item.note&&<p dir="auto">{item.note}</p>}</article>)}</section>}
    </>:<div>{nativeHelpError&&<p role="alert">{tCommon('error')}</p>}<button className="juba-secondary-button" onClick={()=>void generateNativeHelp()}>{nativeHelpError?tCommon('retry'):tCommon('nativeHelpShow',{language:nativeLanguageName})}</button></div>}</div></div>}
  </section>
}
export default function PhrasebookPage(){
  const t=useTranslations('phrasebook')
  const tCommon=useTranslations('common')
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const [categories,setCategories]=useState<PhrasebookCategory[]>([])
  const [loading,setLoading]=useState(true)
  const [loadError,setLoadError]=useState(false)
  const [activeLevel,setActiveLevel]=useState<CEFRLevel|'All'>('All')
  const [activeRegister,setActiveRegister]=useState<Register|'All'>('All')
  const [search,setSearch]=useState('')
  const fetchCategories=useCallback(async(lang:string)=>{
    setLoading(true);setLoadError(false)
    try{setCategories(await getPhrasebookCategories(lang))}catch{setLoadError(true);setCategories([])}finally{setLoading(false)}
  },[])
  useEffect(()=>{void fetchCategories(activeLanguage?.code??'en-GB')},[activeLanguage?.code,fetchCategories])
  const filteredCategories=useMemo(()=>categories.filter(cat=>(activeLevel==='All'||cat.level===activeLevel)&&cat.phrases.some(phrase=>(activeRegister==='All'||phrase.register===activeRegister)&&(!search||phrase.text.toLowerCase().includes(search.toLowerCase())))),[activeLevel,activeRegister,search,categories])
  const totalPhrases=categories.reduce((total,cat)=>total+cat.phrases.length,0)
  const hasActiveFilters=activeLevel!=='All'||activeRegister!=='All'||Boolean(search)
  return <div className="juba-page-shell reference-resource-page reference-phrasebook">
    <style>{`
      .juba-app-shell .reference-phrase-filters{padding:16px;display:flex;flex-direction:column;gap:16px;}
      .juba-app-shell .reference-phrase-search{display:flex;align-items:center;gap:8px;max-width:480px;color:var(--juba-muted);}
      .juba-app-shell .reference-phrase-search input{flex:1;min-width:0;width:100%;padding:8px 12px;}
      .juba-app-shell .reference-phrase-filter-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
      .juba-app-shell .reference-phrase-filter-row>span{font-size:12px;font-weight:600;color:var(--juba-muted);min-width:70px;}
      .juba-app-shell .reference-phrase-filter-row>div{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
      .juba-app-shell .reference-phrase-filter-row button{min-height:36px;padding:6px 12px;border:1px solid var(--juba-border);border-radius:5px;background:var(--juba-card);color:var(--juba-muted);font-size:12px;}
      .juba-app-shell .reference-phrase-filter-row button[aria-pressed="true"]{background:var(--juba-green-soft);color:var(--juba-green-dark);border-color:var(--juba-green);}
      .juba-app-shell .reference-phrase-results{font-size:12px;color:var(--juba-muted);margin:0;}
      .juba-app-shell .reference-phrase-level-section{display:flex;flex-direction:column;gap:16px;}
      .juba-app-shell .reference-phrase-level-heading{display:flex;align-items:center;gap:12px;}
      .juba-app-shell .reference-phrase-level-heading h2{font-size:15px;font-weight:650;margin:0;color:var(--juba-green-dark);}
      .juba-app-shell .reference-phrase-level-heading>span{height:1px;background:var(--juba-border);flex:1;}
      .juba-app-shell .reference-phrase-category-icon{display:grid;place-items:center;width:32px;height:32px;border-radius:4px;background:var(--juba-soft);font-size:18px;}
      .juba-app-shell .reference-phrase-category .reference-resource-panel-head h2{flex:1;min-width:0;}
      .juba-app-shell .reference-phrase-level{font-size:11px;padding:4px 8px;border-radius:4px;background:var(--juba-green-soft);color:var(--juba-green-dark);}
      .juba-app-shell .reference-phrase-list{list-style:none;margin:0;padding:0;}
      .juba-app-shell .reference-phrase-list>li{display:flex;align-items:flex-start;gap:16px;padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-phrase-list>li:last-child{border:0;}
      .juba-app-shell .reference-phrase-text{flex:1;min-width:0;font-size:14px;line-height:1.7;}
      .juba-app-shell .reference-phrase-text p{margin:0;overflow-wrap:anywhere;}
      .juba-app-shell .reference-phrase-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;flex:none;}
      .juba-app-shell .reference-phrase-register{font-size:10px;color:var(--juba-muted);padding:4px 6px;border-radius:4px;background:var(--juba-soft);}
      .juba-app-shell .reference-phrase-register[data-register="formal"]{color:var(--juba-green-dark);background:var(--juba-green-soft);}
      .juba-app-shell .reference-phrase-copy{display:grid;place-items:center;width:36px;height:36px;border:0;border-radius:4px;background:transparent;color:var(--juba-muted);}
      .juba-app-shell .reference-phrase-copy:hover{background:var(--juba-green-soft);color:var(--juba-green-dark);}
      .juba-app-shell .reference-phrase-copy-error{font-size:11px;color:var(--duo-red);}
      .juba-app-shell .reference-phrase-help{border-block-start:1px solid var(--juba-border);}
      @media(max-width:640px){.juba-app-shell .reference-phrase-filter-row button,.juba-app-shell .reference-phrase-copy{min-height:44px;}.juba-app-shell .reference-phrase-list>li{flex-direction:column;gap:8px;}.juba-app-shell .reference-phrase-actions{align-self:flex-end;}}
    `}</style>
    <header className="reference-resource-heading"><BookOpen size={40} aria-hidden="true"/><div><h1>{t('title')}</h1><p>{t('statsLine',{situationCount:categories.length,phraseCount:totalPhrases,range:'A1 - C2'})}</p></div></header>
    <section className="reference-resource-panel reference-phrase-filters" aria-label={t('title')}><label className="reference-phrase-search"><Search size={18} aria-hidden="true"/><input className="juba-input" type="search" value={search} onChange={event=>setSearch(event.target.value)} placeholder={t('searchPlaceholder')} aria-label={t('searchPlaceholder')}/></label><div className="reference-phrase-filter-row"><span>{t('level')}</span><div role="group" aria-label={t('level')}>{(['All',...CEFR_LEVELS] as const).map(level=><button key={level} aria-pressed={activeLevel===level} onClick={()=>setActiveLevel(level)}>{level==='All'?tCommon('all'):level}</button>)}</div></div><div className="reference-phrase-filter-row"><span>{t('register')}</span><div role="group" aria-label={t('register')}>{(['All',...REGISTERS] as const).map(register=><button key={register} aria-pressed={activeRegister===register} onClick={()=>setActiveRegister(register)}>{register==='All'?tCommon('all'):t(register)}</button>)}</div></div></section>
    {loading?<PageLoading/>:loadError?<section className="reference-resource-panel reference-resource-state" role="alert"><p>{tCommon('error')}</p><button className="juba-secondary-button" onClick={()=>void fetchCategories(activeLanguage?.code??'en-GB')}>{tCommon('retry')}</button></section>:<>
      {hasActiveFilters&&<p className="reference-phrase-results" role="status">{t('situationsShown',{count:filteredCategories.length})}</p>}
      {CEFR_LEVELS.map(level=>{const cats=filteredCategories.filter(cat=>cat.level===level);return cats.length?<section className="reference-phrase-level-section" key={level} aria-labelledby={'phrase-level-'+level}><header className="reference-phrase-level-heading"><h2 id={'phrase-level-'+level}>{level}</h2><span aria-hidden="true"/></header>{cats.map(cat=><CategoryCard key={cat.id+'-'+(activeLanguage?.code??'en-GB')} cat={cat} registerFilter={activeRegister} search={search} language={activeLanguage?.code??'en-GB'}/>)}</section>:null})}
      {!filteredCategories.length&&<section className="reference-resource-panel reference-resource-state"><BookOpen size={28}/><p>{t('noResults')}</p>{hasActiveFilters&&<button className="juba-secondary-button" onClick={()=>{setActiveLevel('All');setActiveRegister('All');setSearch('')}}>{tCommon('clearFilters')}</button>}</section>}
    </>}
  </div>
}
