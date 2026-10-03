'use client'

import { useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { BookOpen, CheckCircle2, Volume2, ChevronLeft, ChevronRight, RotateCcw } from 'lucide-react'
import { apiFetch, getGuestMemory, getGuestReviewState } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import '../vocabulary-reference.css'

const REVIEW_KEY='juba_lisan_review_state'
type Word={word:string;translation:string;source?:string;target?:string;id?:number;definition?:string;example_sentence?:string}
type Rating='again'|'hard'|'good'|'easy'
type ReviewState={repetitions:number;interval:number;ease:number;due:number}
type ServerCard=Word&{id:number;next_review:string;repetitions:number;interval:number;ease_factor:number}
function guestSchedule(prev:ReviewState,rating:Rating):ReviewState{
  if(rating==='again')return {repetitions:0,interval:1,ease:Math.max(1.3,prev.ease-.2),due:Date.now()+3600000}
  const ease=Math.max(1.3,prev.ease+(rating==='easy'?.15:rating==='hard'?-.15:0))
  const repetitions=prev.repetitions+1
  const interval=prev.interval<=1?(rating==='easy'?4:rating==='hard'?1:2):Math.max(1,Math.round(prev.interval*ease))
  return {repetitions,interval,ease,due:Date.now()+interval*86400000}
}
function quality(rating:Rating){return rating==='again'?0:rating==='hard'?3:rating==='good'?4:5}
export default function VocabularyReviewPage(){
  const t=useTranslations('vocabularyReview')
  const locale=useLocale()
  const rtl=locale==='ar'
  const authenticated=!!useAuthStore(s=>s.accessToken)
  const [words,setWords]=useState<Word[]>([])
  const [states,setStates]=useState<Record<string,ReviewState>>({})
  const [index,setIndex]=useState(0)
  const [revealed,setRevealed]=useState(false)
  const [done,setDone]=useState(0)
  const [loading,setLoading]=useState(true)
  const [reviewing,setReviewing]=useState(false)
  const [error,setError]=useState('')
  const loadReviewCards=useCallback(async()=>{
    setLoading(true);setError('')
    if(!authenticated){
      const savedWords=getGuestMemory()
      const savedStates=getGuestReviewState()
      const dueWords=savedWords.filter(word=>{const state=savedStates[`${word.word.trim().toLowerCase()}::${word.target||''}`];return !state||state.due<=Date.now()})
      setStates(savedStates);setWords(dueWords);setIndex(0);setDone(0);setRevealed(false);setLoading(false);return
    }
    try{
      const res=await apiFetch('/api/flashcards/due')
      if(!res.ok)throw new Error(t('loadError'))
      const data=await res.json() as {due?:ServerCard[]}
      setWords((data.due||[]).map(card=>({...card,translation:card.translation||card.definition||'',source:card.source,target:card.target})))
      setIndex(0);setDone(0);setRevealed(false);setLoading(false)
    }catch(err){setError(err instanceof Error?err.message:t('loadError'));setLoading(false)}
  },[authenticated,t])
  useEffect(()=>{void loadReviewCards()},[loadReviewCards])
  const current=words[index]
  const remainingDue=Math.max(0,words.length-done)
  const progress=words.length?Math.min(100,Math.round(done/words.length*100)):0
  useEffect(()=>{
    const onKeyDown=(event:KeyboardEvent)=>{
      const target=event.target as HTMLElement|null
      if(target?.tagName==='INPUT'||target?.tagName==='TEXTAREA'||target?.isContentEditable)return
      if(!current||loading||reviewing||done>=words.length)return
      if(event.key===' '&&!revealed){event.preventDefault();setRevealed(true);return}
      if(!revealed)return
      const ratings:Record<string,Rating>={'1':'again','2':'hard','3':'good','4':'easy'}
      const rating=ratings[event.key]
      if(rating){event.preventDefault();void review(rating)}
    }
    window.addEventListener('keydown',onKeyDown)
    return ()=>window.removeEventListener('keydown',onKeyDown)
  },[current,loading,reviewing,revealed,done,words.length])
  async function review(rating:Rating){
    if(!current||reviewing||done>=words.length)return
    setReviewing(true)
    if(authenticated&&current.id){
      try{const res=await apiFetch(`/api/flashcards/${current.id}/review`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({quality:quality(rating)})});if(!res.ok)throw new Error(t('saveError'))}catch(err){setError(err instanceof Error?err.message:t('saveError'));setReviewing(false);return}
    }else{
      const id=`${current.word.trim().toLowerCase()}::${current.target||''}`
      const next={...states,[id]:guestSchedule(states[id]||{repetitions:0,interval:0,ease:2.5,due:0},rating)}
      setStates(next)
      if(typeof window!=='undefined')window.localStorage.setItem(REVIEW_KEY,JSON.stringify(next))
    }
    setError('');setDone(value=>value+1)
    if(index+1<words.length)setTimeout(()=>{setIndex(value=>value+1);setRevealed(false);setReviewing(false)},120)
    else setReviewing(false)
  }
  function speak(){
    if(!current||typeof window==='undefined'||!('speechSynthesis' in window))return
    window.speechSynthesis.cancel()
    const utterance=new SpeechSynthesisUtterance(current.word)
    const raw=current.source&&current.source!=='account'?current.source.replace(/_/g,'-'):'en-US'
    const defaults:Record<string,string>={en:'en-US',es:'es-ES',de:'de-DE',fr:'fr-FR',it:'it-IT',nl:'nl-NL',pl:'pl-PL',pt:'pt-PT',ro:'ro-RO',ru:'ru-RU'}
    const normalized=raw.toLowerCase()
    utterance.lang=normalized.includes('-')?normalized:(defaults[normalized]||normalized)
    window.speechSynthesis.speak(utterance)
  }
  const finished=done>=words.length&&words.length>0
  const Forward=rtl?ChevronLeft:ChevronRight
  return <div className="juba-page-shell reference-review" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-review{display:flex;flex-direction:column;gap:24px;}
      .juba-app-shell .reference-review-summary{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);}
      .juba-app-shell .reference-review-summary>div{flex:1;min-width:0;}
      .juba-app-shell .reference-review-summary span{font-size:12px;color:var(--juba-muted);display:block;margin-block-end:8px;}
      .juba-app-shell .reference-review-summary>strong{font-size:16px;font-weight:650;font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-review-state{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;min-height:260px;padding:32px 16px;border:1px solid var(--juba-border);border-radius:6px;text-align:center;background:var(--juba-card);}
      .juba-app-shell .reference-review-state>svg{color:var(--juba-green);}
      .juba-app-shell .reference-review-state h2{font-size:24px;font-weight:650;margin:0;}
      .juba-app-shell .reference-review-state p{font-size:14px;line-height:1.6;color:var(--juba-muted);margin:0;}
      .juba-app-shell .reference-review-state :is(a,button){padding-inline:16px;}
      .juba-app-shell .reference-review-loading{height:100px;width:min(100%,360px);background:var(--juba-soft);border-radius:6px;}
      .juba-app-shell .reference-review-card{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
      .juba-app-shell .reference-review-card-head{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px;border-block-end:1px solid var(--juba-border);font-size:12px;color:var(--juba-muted);font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-review-question{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;min-height:220px;padding:32px 16px;text-align:center;}
      .juba-app-shell .reference-review-word{display:flex;align-items:center;justify-content:center;gap:16px;max-width:100%;border:0;background:transparent;color:var(--juba-ink);}
      .juba-app-shell .reference-review-word>span{font-size:clamp(28px,4vw,48px);font-weight:650;overflow-wrap:anywhere;}
      .juba-app-shell .reference-review-word>svg{color:var(--juba-green-dark);flex:none;}
      .juba-app-shell .reference-review-question p{font-size:12px;color:var(--juba-muted);margin:0;}
      .juba-app-shell .reference-review-answer{border-block-start:1px solid var(--juba-border);padding:24px 16px;background:var(--juba-green-soft);text-align:center;}
      .juba-app-shell .reference-review-answer h2{font-size:24px;font-weight:650;margin:0;overflow-wrap:anywhere;}
      .juba-app-shell .reference-review-answer p{font-size:14px;line-height:1.6;color:var(--juba-muted);margin:12px 0 0;}
      .juba-app-shell .reference-review-controls{padding:16px;border-block-start:1px solid var(--juba-border);}
      .juba-app-shell .reference-review-reveal{display:flex;justify-content:center;}
      .juba-app-shell .reference-review-reveal button{padding-inline:24px;}
      .juba-app-shell .reference-review-ratings{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;}
      .juba-app-shell .reference-review-ratings button{display:flex;align-items:center;justify-content:center;gap:8px;min-height:44px;padding:8px;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);color:var(--juba-ink);font-size:13px;font-weight:600;}
      .juba-app-shell .reference-review-ratings kbd{font-family:inherit;font-size:10px;color:var(--juba-muted);}
      .juba-app-shell .reference-review-ratings button[data-rating="again"]{color:var(--duo-red);}
      .juba-app-shell .reference-review-ratings button[data-rating="hard"]{background:oklch(97% .03 90);color:oklch(45% .09 75);}
      .juba-app-shell .reference-review-ratings button[data-rating="good"]{background:var(--juba-green);color:var(--juba-card);border-color:var(--juba-green);}
      .juba-app-shell .reference-review-ratings button[data-rating="good"] kbd{color:inherit;}
      .juba-app-shell .reference-review-ratings button[data-rating="easy"]{background:var(--juba-green-soft);color:var(--juba-green-dark);}
      .juba-app-shell .reference-review-ratings button:not(:disabled):hover{border-color:var(--juba-green-dark);}
      @media(max-width:640px){.juba-app-shell .reference-review{gap:16px;}.juba-app-shell .reference-review-ratings{grid-template-columns:1fr 1fr;}.juba-app-shell .reference-review-question{min-height:180px;}.juba-app-shell .reference-review-card-head{flex-wrap:wrap;}}
    `}</style>
    <header className="reference-vocab-header"><BookOpen size={40} aria-hidden="true"/><div><h1>{t('title')}</h1>{!loading&&words.length>0&&<p>{authenticated?`${words.length} ${t('cardsDue')}`:`${remainingDue} ${t('dueNow')} · ${words.length} ${t('saved')}`}</p>}</div><Link href="/vocabulary" className="juba-secondary-button">{t('vocabulary')}<Forward size={16}/></Link></header>
    {loading?<section className="reference-review-state" role="status"><p>{t('loading')}</p><div className="reference-review-loading" aria-hidden="true"/></section>:error&&!words.length?<section className="reference-review-state" role="alert"><h2>{t('unavailable')}</h2><p>{error}</p><button className="juba-primary-button" onClick={()=>void loadReviewCards()}>{t('tryAgain')}</button></section>:!words.length?<section className="reference-review-state"><CheckCircle2 size={40}/><h2>{t('noDue')}</h2><p>{authenticated?t('caughtUp'):t('guestHint')}</p><Link className="juba-primary-button" href={authenticated?'/vocabulary':'/translator'}>{authenticated?t('openVocabulary'):t('openTranslator')}<Forward size={16}/></Link></section>:<>
      <section className="reference-review-summary"><div><span>{t('progressLabel')}</span><div className="reference-vocab-track" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress} aria-label={t('progressLabel')}><span style={{width:progress+'%'}}/></div></div><strong>{done}/{words.length}</strong></section>
      {error&&<div className="reference-vocab-alert" role="alert">{error}</div>}
      {finished?<section className="reference-review-state"><CheckCircle2 size={40}/><h2>{t('complete')}</h2><p>{t('reviewed',{count:words.length})}</p><button className="juba-primary-button" onClick={()=>void loadReviewCards()}><RotateCcw size={16}/>{t('reviewAgain')}</button></section>:<section className="reference-review-card"><header className="reference-review-card-head"><span aria-live="polite" aria-atomic="true">{index+1}/{words.length}</span><span>{authenticated?t('account'):<><bdi>{current.source||t('source')}</bdi> / <bdi>{current.target||t('target')}</bdi></>}</span></header><div className="reference-review-question"><button className="reference-review-word" onClick={speak} aria-label={`${t('tapToHear')}: ${current.word}`}><span dir="auto">{current.word}</span><Volume2 size={22} aria-hidden="true"/></button><p>{t('tapToHear')}</p><p aria-label={t('shortcutHint')}>{revealed?t('rateKeys'):t('spaceShortcut')}</p></div>{revealed&&<div className="reference-review-answer" id="review-answer" role="status" aria-live="polite" aria-atomic="true"><h2 dir="auto">{current.translation||current.definition}</h2>{current.example_sentence&&<p dir="auto">{current.example_sentence}</p>}</div>}<div className="reference-review-controls">{!revealed?<div className="reference-review-reveal"><button className="juba-primary-button" aria-expanded={false} onClick={()=>setRevealed(true)}>{t('reveal')}</button></div>:<div className="reference-review-ratings">{(['again','hard','good','easy'] as const).map((rating,key)=><button key={rating} data-rating={rating} disabled={reviewing} aria-label={t(rating)} onClick={()=>void review(rating)}><kbd aria-hidden="true">{key+1}</kbd>{t(rating)}</button>)}</div>}</div></section>}
    </>}
  </div>
}
