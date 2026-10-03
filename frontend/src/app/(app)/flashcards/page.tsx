'use client'

import { useCallback, useEffect, useRef, useState, type FormEvent } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { BookMarked, Layers, Sparkles, CheckCircle2, Mic, RefreshCw } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { VoiceRecorder } from '@/components/ui/VoiceRecorder'
import { PageLoading } from '@/components/ui/page-loading'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { CEFR_LEVELS } from '@/data/curriculum'
import { markLearningProgressUpdated } from '@/lib/learning-progress'
import '../resource-reference.css'
import './learning-session.css'

interface CardData{id:number;word:string;definition:string;example_sentence:string;translation:string;ease_factor:number;interval:number;repetitions:number;source?:string|null}
export default function FlashcardsPage(){
  const t=useTranslations('flashcards')
  const tCommon=useTranslations('common')
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const [cards,setCards]=useState<CardData[]>([])
  const [current,setCurrent]=useState(0)
  const [flipped,setFlipped]=useState(false)
  const [loading,setLoading]=useState(true)
  const [total,setTotal]=useState(0)
  const [showGenerate,setShowGenerate]=useState(false)
  const [genTopic,setGenTopic]=useState('')
  const [genCount,setGenCount]=useState(10)
  const [genCefr,setGenCefr]=useState('B1')
  const [generating,setGenerating]=useState(false)
  const [genError,setGenError]=useState('')
  const [speakingMode,setSpeakingMode]=useState(false)
  const [reviewing,setReviewing]=useState(false)
  const [loadError,setLoadError]=useState(false)
  const [reviewError,setReviewError]=useState('')
  const [completed,setCompleted]=useState(0)
  const [voiceFeedback,setVoiceFeedback]=useState<{text:string;correct:boolean;expected:string}|null>(null)
  const reviewLock=useRef(false)
  const generationLock=useRef(false)
  const loadVersion=useRef(0)
  const contextVersion=useRef(0)
  const mounted=useRef(true)
  const languageCode=activeLanguage?.code??'en-GB'
  useEffect(()=>{mounted.current=true;return ()=>{mounted.current=false;contextVersion.current+=1;loadVersion.current+=1}},[])
  const loadDue=useCallback(async()=>{
    const version=++loadVersion.current
    setLoading(true);setLoadError(false)
    try{
      const res=await apiFetch('/api/flashcards/due')
      if(!res.ok)throw new Error()
      const data=await res.json() as {due:CardData[];total:number}
      if(!mounted.current||version!==loadVersion.current)return
      setCards(data.due);setTotal(data.total);setCurrent(0);setCompleted(0);setFlipped(false);setReviewError('');setVoiceFeedback(null)
    }catch{if(mounted.current&&version===loadVersion.current)setLoadError(true)}finally{if(mounted.current&&version===loadVersion.current)setLoading(false)}
  },[])
  useEffect(()=>{contextVersion.current+=1;void loadDue()},[loadDue,languageCode])
  async function reviewCard(quality:number,expectedId?:number){
    const card=cards[current]
    if(!card||reviewLock.current||loading||(expectedId!==undefined&&expectedId!==card.id))return
    reviewLock.current=true;setReviewing(true);setReviewError('')
    const context=contextVersion.current
    try{
      const res=await apiFetch(`/api/flashcards/${card.id}/review`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({quality})})
      if(!res.ok)throw new Error(tCommon('error'))
      markLearningProgressUpdated()
      if(!mounted.current||context!==contextVersion.current)return
      setCompleted(value=>value+1)
      if(current<cards.length-1){setCurrent(value=>value+1);setFlipped(false)}else await loadDue()
    }catch{if(mounted.current&&context===contextVersion.current)setReviewError(tCommon('error'))}finally{reviewLock.current=false;if(mounted.current)setReviewing(false)}
  }
  async function handleSpeakingTranscription(transcription:string,expectedId:number){
    const card=cards[current]
    if(!card||card.id!==expectedId||reviewLock.current)return
    const normalize=(value:string)=>value.trim().toLowerCase().replace(/[\p{P}\p{S}\s]+/gu,'')
    const correct=normalize(transcription)===normalize(card.word)
    setVoiceFeedback({text:transcription,correct,expected:card.word})
    await reviewCard(correct?5:2,expectedId)
  }
  async function generateCards(event:FormEvent){
    event.preventDefault()
    if(!genTopic.trim()||generationLock.current||reviewLock.current)return
    generationLock.current=true;setGenerating(true);setGenError('')
    const context=contextVersion.current
    try{
      const res=await apiFetch('/api/flashcards/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({topic:genTopic.trim(),count:genCount,cefr_level:genCefr,target_language:activeLanguage?.code})})
      if(!res.ok){const data=await res.json().catch(()=>({}));throw new Error(data.detail||`Error ${res.status}`)}
      if(!mounted.current||context!==contextVersion.current)return
      setShowGenerate(false);setGenTopic('');await loadDue()
    }catch(err){if(mounted.current&&context===contextVersion.current)setGenError(err instanceof Error&&err.message==='No active study plan found'?tCommon('noActivePlan'):tCommon('error'))}finally{generationLock.current=false;if(mounted.current)setGenerating(false)}
  }
  const card=cards[current]
  const sessionProgress=cards.length?Math.min(100,Math.round(completed/cards.length*100)):0
  return <div className="juba-page-shell reference-resource-page learning-session">
    <header className="learning-session-header"><Layers size={40} aria-hidden="true"/><div><h1>{t('title')}</h1><p>{total} {t('total')} · {cards.length} {t('due')}</p></div><div className="learning-session-actions"><Link className="juba-secondary-button" href="/flashcards/vocabulary"><BookMarked size={16}/>{t('myVocabularyBtn')}</Link><button className="juba-primary-button" aria-expanded={showGenerate} aria-controls="flashcard-generation" onClick={()=>setShowGenerate(value=>!value)} disabled={reviewing||generating}><Sparkles size={16}/>{t('generateBtn')}</button></div></header>
    {showGenerate&&<section className="reference-resource-panel" id="flashcard-generation"><header className="reference-resource-panel-head"><h2>{t('generate')}</h2></header><form className="learning-generation-form" onSubmit={generateCards}>{genError&&<p className="learning-session-error" role="alert">{genError}</p>}<label htmlFor="flashcard-topic">{t('topic')}</label><input className="juba-input" id="flashcard-topic" value={genTopic} onChange={event=>setGenTopic(event.target.value)} placeholder={t('topicPlaceholder')} required disabled={generating}/><div className="learning-generation-options"><div><label htmlFor="flashcard-count">{t('count')}</label><select className="juba-input" id="flashcard-count" value={genCount} onChange={event=>setGenCount(Number(event.target.value))} disabled={generating}>{[5,10,15,20].map(count=><option key={count} value={count}>{count} {t('cards')}</option>)}</select></div><div><label htmlFor="flashcard-level">{t('level')}</label><select className="juba-input" id="flashcard-level" value={genCefr} onChange={event=>setGenCefr(event.target.value)} disabled={generating}>{CEFR_LEVELS.map(level=><option key={level} value={level}>{level}</option>)}</select></div></div><button className="juba-primary-button" disabled={generating||reviewing||!genTopic.trim()}>{generating?t('generating'):t('submit')}</button></form></section>}
    {loading?<PageLoading/>:loadError?<section className="reference-resource-panel reference-resource-state" role="alert"><p>{tCommon('error')}</p><button className="juba-secondary-button" disabled={reviewing} onClick={()=>void loadDue()}>{tCommon('retry')}</button></section>:!card?<section className="reference-resource-panel reference-resource-state"><CheckCircle2 size={40}/><p>{t('noDue')}</p>{total===0&&<p>{t('noCardsHint')}</p>}<button className="juba-secondary-button" onClick={()=>void loadDue()}><RefreshCw size={16}/>{t('refresh')}</button></section>:<>
      <section className="learning-session-status"><div><span>{completed}/{cards.length} {t('due')}</span><div className="learning-session-progress" role="progressbar" aria-label={t('title')} aria-valuemin={0} aria-valuemax={100} aria-valuenow={sessionProgress}><span style={{width:sessionProgress+'%'}}/></div></div><div className="learning-session-modes" role="group" aria-label={t('title')}><button aria-pressed={!speakingMode} disabled={reviewing||generating} onClick={()=>{setSpeakingMode(false);setFlipped(false);setVoiceFeedback(null)}}>{t('standardMode')}</button><button aria-pressed={speakingMode} disabled={reviewing||generating} onClick={()=>{setSpeakingMode(true);setFlipped(false);setVoiceFeedback(null)}}><Mic size={14}/>{t('speakingMode')}</button></div></section>
      {reviewError&&<div className="learning-session-error" role="alert">{reviewError}</div>}
      {voiceFeedback&&<div className="learning-voice-feedback" data-correct={voiceFeedback.correct} role="status"><span dir="auto">{voiceFeedback.text}</span><strong dir="auto">{voiceFeedback.expected}</strong>{voiceFeedback.correct&&<CheckCircle2 size={18} aria-hidden="true"/>}</div>}
      <section className="reference-resource-panel learning-flashcard" aria-busy={reviewing}><header className="reference-resource-panel-head"><h2>{speakingMode?t('speakingMode'):flipped?t('back'):t('front')}</h2><span>{current+1}/{cards.length}</span></header>
        {!speakingMode?<><div className="learning-flashcard-prompt"><TargetLanguageText as="p" languageCode={languageCode} dir="auto" className="learning-flashcard-word">{card.word}</TargetLanguageText><AudioPlayer text={card.word} size="md"/></div>{flipped&&<div className="learning-flashcard-answer" id="flashcard-answer"><TargetLanguageText as="p" languageCode={languageCode} dir="auto">{card.definition}</TargetLanguageText>{card.example_sentence&&<TargetLanguageText as="p" languageCode={languageCode} dir="auto" className="learning-flashcard-example">{card.example_sentence}</TargetLanguageText>}{card.translation&&<p dir="auto">{card.translation}</p>}</div>}<div className="learning-flashcard-reveal"><button className="juba-secondary-button" onClick={()=>setFlipped(value=>!value)} disabled={reviewing||generating} aria-expanded={flipped}>{flipped?t('tapToHide'):t('tapToReveal')}</button></div>{flipped&&<div className="learning-flashcard-ratings">{[{key:'again',quality:0},{key:'hard',quality:3},{key:'good',quality:4},{key:'easy',quality:5}].map(({key,quality})=><button key={key} data-rating={key} disabled={reviewing||generating} onClick={()=>void reviewCard(quality)}>{t(key)}</button>)}</div>}</>:<div className="learning-speaking-card"><TargetLanguageText as="p" languageCode={languageCode} dir="auto">{card.definition}</TargetLanguageText>{card.example_sentence&&<TargetLanguageText as="p" languageCode={languageCode} dir="auto" className="learning-flashcard-example">{card.example_sentence}</TargetLanguageText>}{card.translation&&<p dir="auto">{card.translation}</p>}<p className="learning-speaking-instruction">{t('sayWord')}</p>{!reviewing&&!generating&&<VoiceRecorder key={card.id+'-'+languageCode} onTranscription={text=>handleSpeakingTranscription(text,card.id)} maxSeconds={5}/>}</div>}
        <footer className="learning-flashcard-schedule">EF {card.ease_factor.toFixed(2)} · {t('interval')} {card.interval}d · {t('repetitions')} {card.repetitions}</footer>
      </section>
    </>}
  </div>
}
