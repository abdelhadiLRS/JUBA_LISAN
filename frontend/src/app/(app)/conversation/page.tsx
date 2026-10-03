'use client'

import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import { useTranslations } from 'next-intl'
import { Mic, Clock } from 'lucide-react'
import type { ChatContextItem } from '@/lib/conversation-ws'
import { PageLoading } from '@/components/ui/page-loading'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { MaintenanceGate } from '@/components/billing/MaintenanceBanner'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'
import { useAuthStore, isSubscribed, isFreemiumTrialActive } from '@/store/auth'
import { useFreemiumStore } from '@/store/freemium'

function ConversationLoading(){return <div className="reference-voice-loading" role="status"><PageLoading minHeight="min-h-0"/></div>}
const ConversationMode=dynamic(()=>import('@/components/conversation/ConversationMode'),{ssr:false,loading:ConversationLoading})

export default function ConversationPage(){
  const t=useTranslations('conversation')
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const stripeEnabled=useConfigStore(s=>s.stripeEnabled)
  const user=useAuthStore(s=>s.user)
  const fetchFreemium=useFreemiumStore(s=>s.fetchStatus)
  const freemiumStatus=useFreemiumStore(s=>s.status)
  const freemiumExhausted=stripeEnabled&&!isSubscribed(user,stripeEnabled)&&!isFreemiumTrialActive(user,stripeEnabled)&&freemiumStatus&&freemiumStatus.voice_remaining_seconds<=0
  const freemiumVoiceRemaining=freemiumStatus?Math.ceil(freemiumStatus.voice_remaining_seconds/60):undefined
  const freemiumVoiceLimit=freemiumStatus?Math.ceil(freemiumStatus.voice_limit_seconds/60):undefined
  const showFreemiumVoicePill=stripeEnabled&&!isSubscribed(user,stripeEnabled)&&!isFreemiumTrialActive(user,stripeEnabled)&&freemiumStatus&&freemiumStatus.voice_limit_seconds>0
  const [initialContext,setInitialContext]=useState<ChatContextItem[]|undefined>(undefined)
  const [autoStart,setAutoStart]=useState(false)
  const [cefrLevel,setCefrLevel]=useState<string|null>(null)
  const [planReady,setPlanReady]=useState(false)
  const [voiceTrial,setVoiceTrial]=useState<{token:string;durationSeconds:number;cefrLevel?:string;targetLanguage?:string}|null>(null)
  useEffect(()=>{if(stripeEnabled&&!isSubscribed(user,stripeEnabled))fetchFreemium()},[stripeEnabled,user,fetchFreemium])
  useEffect(()=>{
    const raw=sessionStorage.getItem('voice_context')
    if(raw){
      sessionStorage.removeItem('voice_context')
      try{
        const parsed=JSON.parse(raw) as unknown
        if(typeof parsed==='object'&&parsed!==null&&'messages' in (parsed as Record<string,unknown>)){
          const pkg=parsed as {messages:unknown}
          if(Array.isArray(pkg.messages))setInitialContext(pkg.messages as ChatContextItem[])
          setAutoStart(true)
        }else if(Array.isArray(parsed)){setInitialContext(parsed as ChatContextItem[]);setAutoStart(true)}
      }catch{/* Ignore malformed stored context. */}
    }
    const trialRaw=sessionStorage.getItem('assessment_voice_trial')
    if(trialRaw){
      sessionStorage.removeItem('assessment_voice_trial')
      try{
        const parsed=JSON.parse(trialRaw) as {token?:unknown;durationSeconds?:unknown;cefrLevel?:unknown;targetLanguage?:unknown}
        if(typeof parsed.token==='string'&&parsed.token.length>0){
          setVoiceTrial({token:parsed.token,durationSeconds:typeof parsed.durationSeconds==='number'?parsed.durationSeconds:300,cefrLevel:typeof parsed.cefrLevel==='string'?parsed.cefrLevel:undefined,targetLanguage:typeof parsed.targetLanguage==='string'?parsed.targetLanguage:undefined})
          setInitialContext([{role:'user',content:t('assessmentVoiceContext')}]);setAutoStart(true)
        }
      }catch{/* Ignore malformed trial context. */}
    }
    setPlanReady(false)
    apiFetch('/api/study-plan/today').then(res=>res.ok?res.json():null).then(data=>{if(data?.cefr_level)setCefrLevel(data.cefr_level)}).catch(()=>{/* Preserve default conversation timing without a plan. */}).finally(()=>setPlanReady(true))
  },[activeLanguage?.code,t])
  const remaining=freemiumVoiceRemaining??0
  const limit=freemiumVoiceLimit??0
  const quotaPercent=limit?Math.max(0,Math.min(100,Math.round(remaining/limit*100))):0
  const trialMinutes=Math.max(1,Math.round((voiceTrial?.durationSeconds??300)/60))
  const statusLabel=voiceTrial?t('trialBanner',{minutes:trialMinutes}):freemiumExhausted?t('quotaExceededTime'):t('statusReady')
  return <div className="juba-page-shell reference-voice-page">
    <style>{`
      .juba-app-shell .reference-voice-page{display:flex;flex-direction:column;gap:24px;min-width:0;}
      .juba-app-shell .reference-voice-header{display:flex;align-items:center;gap:16px;min-height:100px;flex-wrap:wrap;}
      .juba-app-shell .reference-voice-header>svg{color:var(--juba-green);flex:none;}
      .juba-app-shell .reference-voice-header>div{flex:1;min-width:0;}
      .juba-app-shell .reference-voice-header h1{font-size:28px;font-weight:650;margin:0;}
      .juba-app-shell .reference-voice-header p{font-size:14px;color:var(--juba-muted);margin:6px 0 0;}
      .juba-app-shell .reference-voice-status{padding:6px 10px;border-radius:4px;background:var(--juba-green-soft);color:var(--juba-green-dark);font-size:12px;}
      .juba-app-shell .reference-voice-status[data-exhausted="true"]{background:oklch(96% .04 87);color:oklch(45% .09 75);}
      .juba-app-shell .reference-voice-quota{padding:16px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);}
      .juba-app-shell .reference-voice-quota>div:first-child{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--juba-muted);}
      .juba-app-shell .reference-voice-quota>div:last-child{flex:1;min-width:180px;max-width:440px;margin-inline-start:auto;}
      .juba-app-shell .reference-voice-quota p{font-size:12px;margin:0 0 8px;color:var(--juba-muted);}
      .juba-app-shell .reference-voice-track{height:8px;border-radius:3px;overflow:hidden;background:var(--juba-soft);}
      .juba-app-shell .reference-voice-track>span{display:block;height:100%;background:var(--juba-green);}
      .juba-app-shell .reference-voice-track[data-low="true"]>span{background:var(--juba-yellow);}
      .juba-app-shell .reference-voice-loading{padding:32px;border:1px solid var(--juba-border);border-radius:6px;}
      @media(max-width:640px){.juba-app-shell .reference-voice-page{gap:16px;}.juba-app-shell .reference-voice-header h1{font-size:24px;}.juba-app-shell .reference-voice-header>svg{width:32px;height:32px;}.juba-app-shell .reference-voice-quota>div:last-child{max-width:none;}}
    `}</style>
    <header className="reference-voice-header"><Mic size={40} aria-hidden="true"/><div><h1>{t('title')}</h1><p>{t('subtitle')}</p></div>{planReady&&<span className="reference-voice-status" data-exhausted={Boolean(freemiumExhausted)} role="status">{statusLabel}</span>}</header>
    {!planReady?<PageLoading minHeight="min-h-[60vh]"/>:<>
      <section className="reference-voice-quota" aria-label={t('quotaMinutes')}><div><Clock size={18} aria-hidden="true"/><strong>{voiceTrial?t('trialCtaLabel'):cefrLevel?`CEFR ${cefrLevel}`:t('statusReady')}</strong></div>{showFreemiumVoicePill&&<div><p>{t('freemiumVoiceRemaining',{remaining,limit})}</p><div className="reference-voice-track" data-low={quotaPercent<25} role="progressbar" aria-label={t('quotaMinutes')} aria-valuemin={0} aria-valuemax={100} aria-valuenow={quotaPercent}><span style={{width:quotaPercent+'%'}}/></div></div>}</section>
      <MaintenanceGate>{voiceTrial?<ConversationMode initialContext={initialContext} autoStart={autoStart} cefrLevel={voiceTrial.cefrLevel??cefrLevel} targetLanguage={voiceTrial.targetLanguage??activeLanguage?.code} voiceTrialToken={voiceTrial.token} voiceTrialDurationSeconds={voiceTrial.durationSeconds} trialMode/>:freemiumExhausted?<><FreemiumQuotaBanner feature="voice" className="mb-4"/><PaywallBanner feature="voice" compact/></>:<ConversationMode initialContext={initialContext} autoStart={autoStart} cefrLevel={cefrLevel} targetLanguage={activeLanguage?.code} freemiumVoiceRemaining={showFreemiumVoicePill?freemiumVoiceRemaining:undefined} freemiumVoiceLimit={showFreemiumVoicePill?freemiumVoiceLimit:undefined}/>}</MaintenanceGate>
    </>}
  </div>
}
