'use client'
import {useEffect,useState,useRef} from 'react'
import type {FormEvent} from 'react'
import {useTranslations,useLocale} from 'next-intl'
import {ArrowRightLeft,BookOpenCheck,Check,Copy,Languages,Loader2,Volume2,X} from 'lucide-react'
import Link from 'next/link'
import {apiFetch,saveTranslatedWordLocally} from '@/lib/api'
import {useAuthStore} from '@/store/auth'
import {TARGET_LANGUAGE_CATALOG} from '@/lib/target-languages'
const MAX_CHARS=1000
const LANGUAGES=TARGET_LANGUAGE_CATALOG.map(language=>({code:language.iso639,label:language.name})).filter((item,index,all)=>all.findIndex(value=>value.code===item.code)===index)
function languageLabel(code:string){return LANGUAGES.find(item=>item.code===code)?.label??code.toUpperCase()}
export function VisitorTranslator(){
 const t=useTranslations('visitorTranslator'),ar=useLocale().startsWith('ar'),token=useAuthStore(s=>s.accessToken)
 const [open,setOpen]=useState(false),[text,setText]=useState(''),[source,setSource]=useState('auto'),[target,setTarget]=useState('ar')
 const [translation,setTranslation]=useState(''),[detected,setDetected]=useState(''),[loading,setLoading]=useState(false),[error,setError]=useState('')
 const [saved,setSaved]=useState(false),[copied,setCopied]=useState(false),[exhausted,setExhausted]=useState(false)
 const version=useRef(0),lock=useRef(false)
 useEffect(()=>{version.current++;setTranslation('');setDetected('');setError('');setExhausted(false);setLoading(false)},[token])
 useEffect(()=>{if(!open)return;const handler=(e:KeyboardEvent)=>{if(e.key==='Escape')setOpen(false)};document.addEventListener('keydown',handler);return()=>document.removeEventListener('keydown',handler)},[open])
 function reset(){version.current++;setTranslation('');setDetected('');setSaved(false);setError('');setExhausted(false)}
 async function translate(event?:FormEvent){
  event?.preventDefault();if(!token||!text.trim()||lock.current||text.length>MAX_CHARS)return
  lock.current=true;setLoading(true);setError('');setSaved(false);setExhausted(false)
  const epoch=version.current
  try{const response=await apiFetch('/api/translate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text,source,target})})
   const data=await response.json().catch(()=>({}))
   if(epoch!==version.current)return
   if(response.status===402){setExhausted(true);throw new Error(ar?'نفدت حصة الترجمة والتصحيح. راجع موعد التجديد أو باقتك.':'Translation and correction allowance reached. Check your reset time or plan.')}
   if(!response.ok)throw new Error(typeof data.detail==='string'?data.detail:t('translationFailed'))
   if(typeof data.translation!=='string')throw new Error(t('translationFailed'))
   setTranslation(data.translation);setDetected(typeof data.source==='string'?data.source:source)
  }catch(err){if(epoch===version.current){setTranslation('');setDetected('');setError(err instanceof Error?err.message:t('translationFailed'))}}
  finally{lock.current=false;if(epoch===version.current)setLoading(false)}
 }
 function save(){if(!text.trim()||!translation.trim())return;saveTranslatedWordLocally({source:detected||source,target,word:text.trim(),translation:translation.trim()});setSaved(true)}
 async function copy(){try{await navigator.clipboard.writeText(translation);setCopied(true);setTimeout(()=>setCopied(false),1600)}catch{setCopied(false)}}
 function speak(){if(!translation||!('speechSynthesis'in window))return;window.speechSynthesis.cancel();const voice=new SpeechSynthesisUtterance(translation);voice.lang=target;window.speechSynthesis.speak(voice)}
 return <><button type="button" onClick={()=>setOpen(true)} aria-label={t('open')} className="fixed bottom-5 end-5 z-40 inline-flex min-h-11 items-center gap-2 rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] px-5 py-3 text-sm font-semibold"><Languages size={16}/>{t('translate')}</button>
 {open&&<div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-[var(--duo-muted)] p-3 sm:p-6" onMouseDown={e=>{if(e.target===e.currentTarget)setOpen(false)}}><div role="dialog" aria-modal="true" aria-labelledby="visitor-translator-title" className="w-full max-w-6xl rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)]">
  <header className="flex items-center justify-between border-b border-[var(--duo-line)] px-5 py-4"><h2 id="visitor-translator-title" className="text-xl font-semibold">{t('title')}</h2><button type="button" onClick={()=>setOpen(false)} aria-label={t('close')} className="min-h-11 min-w-11 p-2"><X size={20}/></button></header>
  {!token?<div className="p-7"><p>{ar?'سجّل الدخول لاستخدام حصتك المجانية في الترجمة وحفظ الكلمات.':'Sign in to use your free translation allowance and save words.'}</p><Link className="juba-primary-button inline-flex min-h-11 px-5 py-3 mt-4" href="/login">{ar?'تسجيل الدخول':'Sign in'}</Link></div>:<form onSubmit={translate} className="p-4 sm:p-7"><div className="grid overflow-hidden rounded-[10px] border border-[var(--duo-line)] lg:grid-cols-[1fr_auto_1fr]">
   <section className="flex min-h-[360px] flex-col"><label className="sr-only" htmlFor="visitor-translator-source">{t('sourceLanguage')}</label><select id="visitor-translator-source" value={source} disabled={loading} onChange={e=>{setSource(e.target.value);reset()}} className="min-h-11 border-b border-[var(--duo-line)] bg-transparent px-5 py-3"><option value="auto">{t('autoDetect')}</option>{LANGUAGES.map(item=><option key={item.code} value={item.code}>{item.label}</option>)}</select>
   <textarea value={text} onChange={e=>{setText(e.target.value);reset()}} maxLength={MAX_CHARS} rows={8} autoFocus disabled={loading} placeholder={t('inputPlaceholder')} aria-label={t('textToTranslate')} className="min-h-[255px] flex-1 resize-none bg-transparent px-5 py-5 text-lg leading-8"/><div className="flex justify-between px-5 pb-4 text-xs"><span>{text.length}/{MAX_CHARS}</span><span>{detected?languageLabel(detected):source==='auto'?t('automaticDetection'):languageLabel(source)}</span></div></section>
   <div className="flex items-center justify-center border-y border-[var(--duo-line)] bg-[var(--duo-bg)] p-3 lg:border-x lg:border-y-0"><button type="button" disabled={source==='auto'||loading} aria-label={t('swap')} onClick={()=>{if(source!=='auto'){setSource(target);setTarget(source);reset()}}} className="min-h-11 min-w-11 rounded-full border border-[var(--duo-line)] bg-[var(--duo-card)] p-2.5"><ArrowRightLeft size={16}/></button></div>
   <section className="flex min-h-[360px] flex-col bg-[var(--duo-bg)]"><label className="sr-only" htmlFor="visitor-translator-target">{t('targetLanguage')}</label><select id="visitor-translator-target" value={target} disabled={loading} onChange={e=>{setTarget(e.target.value);reset()}} className="min-h-11 border-b border-[var(--duo-line)] bg-transparent px-5 py-3">{LANGUAGES.map(item=><option key={item.code} value={item.code}>{item.label}</option>)}</select>
    <div className="flex-1 px-5 py-5">{error?<div role="alert"><p className="text-[var(--duo-red)]">{error}</p>{exhausted&&<Link className="underline" href="/settings/subscription">{ar?'الباقة والتجديد':'Plan and reset time'}</Link>}</div>:translation?<><p className="text-lg leading-8">{translation}</p><div className="mt-6 flex flex-wrap gap-2"><button type="button" onClick={speak} aria-label={ar?'استمع':'Listen'} className="min-h-11 p-2"><Volume2 size={20}/></button><button type="button" onClick={()=>void copy()} aria-label={ar?'نسخ':'Copy'} className="min-h-11 p-2">{copied?<Check size={20}/>:<Copy size={20}/>}</button><button type="button" onClick={save} className="inline-flex min-h-11 items-center gap-2 px-3 py-2"><BookOpenCheck size={16}/>{saved?t('savedLocally'):t('learnThis')}</button></div>{saved&&<p role="status" className="mt-3 text-xs">{t('savedNote')}</p>}</>:<p>{t('translationPlaceholder')}</p>}</div></section>
  </div><div className="mt-4 flex flex-wrap items-center justify-between gap-3"><p className="text-xs">{t('workflow')}</p><button type="submit" disabled={!text.trim()||loading} className="inline-flex min-h-11 items-center gap-2 rounded-[10px] bg-[var(--duo-green)] px-7 py-3 font-semibold text-[var(--duo-card)]">{loading?<Loader2 size={16} className="animate-spin"/>:<Languages size={16}/>} {loading?t('translating'):t('translate')}</button></div></form>}
 </div></div>}</>
}
