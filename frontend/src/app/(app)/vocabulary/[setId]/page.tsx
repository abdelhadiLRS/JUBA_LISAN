'use client'

import { useState, useEffect, use, useCallback } from 'react'
import { notFound, useRouter } from 'next/navigation'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { Library, ChevronLeft, ChevronRight, ChevronDown, CheckCircle2, Plus, Languages } from 'lucide-react'
import { PageLoading } from '@/components/ui/page-loading'
import type { VocabularyNativeHelp, VocabularySet } from '@/data/types'
import { useLanguageStore } from '@/store/language'
import { useAuthStore } from '@/store/auth'
import { apiFetch } from '@/lib/api'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import '../vocabulary-reference.css'

const POS_LABELS:Record<string,string>={noun:'n.',verb:'v.',adjective:'adj.',adverb:'adv.',phrase:'phr.',conjunction:'conj.',preposition:'prep.',numeral:'num.',pronoun:'pron.'}
export default function VocabularySetPage({params}:{params:Promise<{setId:string}>}){
  const {setId}=use(params)
  const router=useRouter()
  const t=useTranslations('vocabulary')
  const tCommon=useTranslations('common')
  const tTargetLang=useTranslations('targetLanguages')
  const locale=useLocale()
  const rtl=locale==='ar'
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const user=useAuthStore(s=>s.user)
  const [vocabSet,setVocabSet]=useState<VocabularySet|null>(null)
  const [loading,setLoading]=useState(true)
  const [adding,setAdding]=useState(false)
  const [addedCount,setAddedCount]=useState<number|null>(null)
  const [error,setError]=useState('')
  const [nativeHelpOpen,setNativeHelpOpen]=useState(false)
  const [nativeHelp,setNativeHelp]=useState<VocabularyNativeHelp|null>(null)
  const [loadingNativeHelp,setLoadingNativeHelp]=useState(false)
  const [nativeHelpError,setNativeHelpError]=useState(false)
  const nativeLanguageName=user?.native_language?tTargetLang(user.native_language):''
  const targetLanguageCode=activeLanguage?.code??'en-GB'
  useEffect(()=>{
    let cancelled=false
    const lang=activeLanguage?.code??'en-GB'
    setLoading(true)
    apiFetch(`/api/vocabulary/${encodeURIComponent(setId)}?language=${lang}`).then(res=>{if(!res.ok)throw new Error('not found');return res.json()}).then((data:{set:VocabularySet})=>{if(!cancelled)setVocabSet(data.set)}).catch(()=>{if(!cancelled)setVocabSet(null)}).finally(()=>{if(!cancelled)setLoading(false)})
    return ()=>{cancelled=true}
  },[setId,activeLanguage?.code])
  useEffect(()=>{setNativeHelpOpen(false);setNativeHelp(null);setNativeHelpError(false)},[setId,activeLanguage?.code])
  const generateNativeHelp=useCallback(async()=>{
    if(loadingNativeHelp)return
    setLoadingNativeHelp(true);setNativeHelpError(false)
    try{const res=await apiFetch(`/api/vocabulary/${encodeURIComponent(setId)}/native-help?language=${targetLanguageCode}`,{method:'POST'});if(!res.ok)throw new Error('native help failed');const data=await res.json() as {native_help:VocabularyNativeHelp};setNativeHelp(data.native_help)}catch{setNativeHelpError(true)}finally{setLoadingNativeHelp(false)}
  },[loadingNativeHelp,setId,targetLanguageCode])
  async function handleAddAll(){
    if(!vocabSet)return
    setAdding(true);setError('')
    try{
      const cards=vocabSet.words.map(word=>({word:word.word,definition:word.definition,example_sentence:word.example,translation:''}))
      const res=await apiFetch('/api/flashcards/bulk',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({flashcards:cards})})
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error((data as {detail?:string}).detail??`Error ${res.status}`)}
      const data=await res.json() as {created:number};setAddedCount(data.created)
    }catch(err){const msg=err instanceof Error?err.message:'';setError(msg==='No active study plan found'?tCommon('noActivePlan'):msg||'Failed to add flashcards.')}finally{setAdding(false)}
  }
  if(loading)return <PageLoading/>
  if(!vocabSet)notFound()
  const Back=rtl?ChevronRight:ChevronLeft
  const helpId='vocabulary-native-help'
  return <div className="juba-page-shell reference-vocab-detail" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-vocab-detail{display:flex;flex-direction:column;gap:24px;}
      .juba-app-shell .reference-vocab-breadcrumb{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:12px;color:var(--juba-muted);min-height:32px;}
      .juba-app-shell .reference-vocab-breadcrumb a{display:flex;align-items:center;gap:8px;color:var(--juba-green-dark);}
      .juba-app-shell .reference-vocab-detail-meta{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:12px 16px;border:1px solid var(--juba-border);border-radius:6px;}
      .juba-app-shell .reference-vocab-detail-meta>span{font-size:12px;color:var(--juba-muted);}
      .juba-app-shell .reference-vocab-detail-meta>button{margin-inline-start:auto;padding-inline:12px;}
      .juba-app-shell .reference-vocab-added{display:flex;align-items:center;gap:8px;color:var(--juba-green-dark);font-size:13px;flex-wrap:wrap;}
      .juba-app-shell .reference-vocab-added button{text-decoration:underline;min-height:36px;}
      .juba-app-shell .reference-vocab-help-toggle{display:flex;align-items:center;gap:12px;padding:16px;width:100%;border:0;background:transparent;text-align:start;font-size:14px;font-weight:600;color:var(--juba-ink);}
      .juba-app-shell .reference-vocab-help-toggle>span{flex:1;}
      .juba-app-shell .reference-vocab-help-toggle>svg{color:var(--juba-green-dark);flex:none;}
      .juba-app-shell .reference-vocab-help-toggle[aria-expanded="true"]>svg:last-child{transform:rotate(180deg);}
      .juba-app-shell .reference-vocab-help-body{padding:16px;border-block-start:1px solid var(--juba-border);font-size:14px;line-height:1.7;color:var(--juba-muted);}
      .juba-app-shell .reference-vocab-help-body section{border-block-start:1px solid var(--juba-border);padding-block-start:16px;margin-block-start:16px;}
      .juba-app-shell .reference-vocab-help-body h3{font-size:14px;font-weight:650;margin:0 0 8px;}
      .juba-app-shell .reference-vocab-help-body ul{margin:0;padding-inline-start:20px;}
      .juba-app-shell .reference-vocab-help-body p{margin:4px 0;}
      .juba-app-shell .reference-vocab-help-item{padding-block:8px;}
      .juba-app-shell .reference-vocab-help-body[hidden]{display:none;}
      .juba-app-shell .reference-vocab-word{padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-vocab-word:last-child{border:0;}
      .juba-app-shell .reference-vocab-word-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-block-end:8px;}
      .juba-app-shell .reference-vocab-word-head>span:first-child{font-size:16px;font-weight:650;color:var(--juba-ink);}
      .juba-app-shell .reference-vocab-word-head small{font-size:11px;color:var(--juba-muted);}
      .juba-app-shell .reference-vocab-word-rank{margin-inline-start:auto;direction:ltr;unicode-bidi:isolate;font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-vocab-word p{font-size:14px;line-height:1.7;color:var(--juba-muted);margin:4px 0;}
      .juba-app-shell .reference-vocab-word p:last-child{font-style:italic;}
      .juba-app-shell .reference-vocab-back{display:inline-flex;align-items:center;gap:8px;min-height:44px;align-self:flex-start;font-size:13px;color:var(--juba-muted);}
      @media(max-width:640px){.juba-app-shell .reference-vocab-detail{gap:16px;}.juba-app-shell .reference-vocab-detail-meta>button{margin-inline-start:0;width:100%;}.juba-app-shell .reference-vocab-help-toggle{font-size:13px;}}
    `}</style>
    <nav className="reference-vocab-breadcrumb" aria-label={rtl?'مسار التنقل':'Breadcrumb'}><Link href="/vocabulary"><Back size={14}/>{t('title')}</Link><span aria-hidden="true">/</span><span>{vocabSet.level}</span><span aria-hidden="true">/</span><span>{vocabSet.topic}</span></nav>
    <header className="reference-vocab-header"><Library size={40} aria-hidden="true"/><div><h1>{vocabSet.topic}</h1><p>{t('vocabularySet')} · {vocabSet.words.length} {t('words')}</p></div></header>
    <section className="reference-vocab-detail-meta"><span className="juba-badge">{vocabSet.level}</span><span>{vocabSet.unit_ref}</span>{addedCount!==null?<div className="reference-vocab-added" role="status"><CheckCircle2 size={18}/><span>{t('cardsAdded',{count:addedCount})}</span><button onClick={()=>router.push('/flashcards')}>{t('goToFlashcards')}</button></div>:<button className="juba-primary-button" onClick={handleAddAll} disabled={adding}><Plus size={16}/>{adding?'…':t('addAll',{count:vocabSet.words.length})}</button>}</section>
    {error&&<div className="reference-vocab-alert" role="alert">{error}</div>}
    {nativeLanguageName&&<section className="reference-vocab-panel"><button className="reference-vocab-help-toggle" aria-expanded={nativeHelpOpen} aria-controls={helpId} onClick={()=>setNativeHelpOpen(value=>!value)}><Languages size={20}/><span>{tCommon('nativeHelpTitle',{language:nativeLanguageName})}</span><ChevronDown size={16}/></button><div className="reference-vocab-help-body" id={helpId} hidden={!nativeHelpOpen}>{loadingNativeHelp?<p role="status">{tCommon('nativeHelpLoading',{language:nativeLanguageName})}</p>:nativeHelp?<>
      <p dir="auto">{nativeHelp.summary}</p>
      {nativeHelp.study_tips.length>0&&<section><h3>{tCommon('nativeHelpStudyTips')}</h3><ul>{nativeHelp.study_tips.map((tip,index)=><li dir="auto" key={index}>{tip}</li>)}</ul></section>}
      {nativeHelp.word_notes.length>0&&<section><h3>{tCommon('nativeHelpWordNotes')}</h3>{nativeHelp.word_notes.map((item,index)=><div className="reference-vocab-help-item" key={index}><TargetLanguageText languageCode={targetLanguageCode} className="font-semibold">{item.word}</TargetLanguageText><p dir="auto">{item.meaning}</p><p dir="auto">{item.note}</p></div>)}</section>}
      {nativeHelp.common_traps.length>0&&<section><h3>{tCommon('nativeHelpCommonTraps')}</h3>{nativeHelp.common_traps.map((trap,index)=><div className="reference-vocab-help-item" key={index}><p dir="auto">{trap.mistake}</p><p dir="auto">{trap.fix}</p></div>)}</section>}
      {nativeHelp.mini_glossary.length>0&&<section><h3>{tCommon('nativeHelpMiniGlossary')}</h3>{nativeHelp.mini_glossary.map((item,index)=><div className="reference-vocab-help-item" key={index}><TargetLanguageText languageCode={targetLanguageCode} className="font-semibold">{item.term}</TargetLanguageText><p dir="auto">{item.meaning}</p>{item.note&&<p dir="auto">{item.note}</p>}</div>)}</section>}
      {nativeHelp.practice_prompts.length>0&&<section><h3>{tCommon('nativeHelpPractice')}</h3><ul>{nativeHelp.practice_prompts.map((prompt,index)=><li key={index} dir="auto">{prompt}</li>)}</ul></section>}
    </>:<div>{nativeHelpError&&<p role="alert">{tCommon('error')}</p>}<button className="juba-secondary-button" onClick={()=>void generateNativeHelp()}>{nativeHelpError?tCommon('retry'):tCommon('nativeHelpShow',{language:nativeLanguageName})}</button></div>}</div></section>}
    <section className="reference-vocab-panel" aria-label={t('words')}><header className="reference-vocab-panel-head"><h2>{t('words')}</h2><span>{vocabSet.words.length}</span></header>{vocabSet.words.map((word,index)=><article className="reference-vocab-word" key={index}><div className="reference-vocab-word-head"><TargetLanguageText languageCode={targetLanguageCode}>{word.word}</TargetLanguageText><small>{POS_LABELS[word.pos]??word.pos}</small>{word.ipa&&<small dir="ltr">{word.ipa}</small>}{word.frequency_rank&&<small className="reference-vocab-word-rank">#{word.frequency_rank}</small>}</div><TargetLanguageText as="p" languageCode={targetLanguageCode}>{word.definition}</TargetLanguageText><TargetLanguageText as="p" languageCode={targetLanguageCode}>&ldquo;{word.example}&rdquo;</TargetLanguageText></article>)}{!vocabSet.words.length&&<div className="reference-vocab-empty"><p>{t('noResults')}</p></div>}</section>
    <Link href="/vocabulary" className="reference-vocab-back"><Back size={16}/>{t('backToVocabulary')}</Link>
  </div>
}
