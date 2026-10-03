'use client'
import Link from 'next/link'
import {useEffect,useState} from 'react'
import {useLocale} from 'next-intl'
import {apiFetch} from '@/lib/api'
import {useAuthStore} from '@/store/auth'

type Feature='chat'|'lessons'|'listening'|'reading'|'voice'|'flashcards'|'translation'|'tts'
type Status={tier:string;metered:boolean;features:Record<Feature,{remaining:number;limit:number;reserved:number;unit:string;period:string;resets_at:string}>}
export function FreemiumQuotaBanner({feature,className=''}:{feature:Feature;className?:string}){
  const ar=useLocale().startsWith('ar'),token=useAuthStore(s=>s.accessToken)
  const [status,setStatus]=useState<Status|null>(null),[failed,setFailed]=useState(false)
  useEffect(()=>{
    if(!token){setStatus(null);return}
    const controller=new AbortController();let busy=false
    async function refresh(){
      if(busy||document.hidden)return
      busy=true
      try{
        const response=await apiFetch('/api/subscriptions/me',{signal:controller.signal})
        if(!response.ok)throw new Error()
        const data=await response.json()
        if(!controller.signal.aborted){setStatus(data);setFailed(false)}
      }catch{if(!controller.signal.aborted)setFailed(true)}finally{busy=false}
    }
    setStatus(null);void refresh()
    const timer=setInterval(()=>void refresh(),60000)
    const onVisible=()=>void refresh()
    window.addEventListener('focus',onVisible);document.addEventListener('visibilitychange',onVisible)
    return()=>{controller.abort();clearInterval(timer);window.removeEventListener('focus',onVisible);document.removeEventListener('visibilitychange',onVisible)}
  },[token,feature])
  if(status&&!status.metered)return null
  if(failed)return <p className={className} role="status">{ar?'تعذّر تحديث الحصة.':'Could not update allowance.'} <Link href="/settings/subscription">{ar?'تفاصيل الاشتراك':'Subscription details'}</Link></p>
  const quota=status?.features[feature]
  if(!quota)return null
  const seconds=quota.unit==='seconds'
  const remaining=seconds?Math.floor(quota.remaining/60):quota.remaining,limit=seconds?quota.limit/60:quota.limit
  const label=ar?({chat:'رسائل المعلم',lessons:'دروس جديدة',listening:'تمارين استماع جديدة',reading:'تمارين قراءة جديدة',voice:'دقائق المحادثة',flashcards:'بطاقات جديدة',translation:'ترجمة وتصحيح',tts:'دقائق النطق'})[feature]:({chat:'Tutor messages',lessons:'New lessons',listening:'New listening exercises',reading:'New reading exercises',voice:'Voice minutes',flashcards:'New cards',translation:'Translation and correction',tts:'Pronunciation minutes'})[feature]
  return <div className={`juba-billing-quota flex flex-wrap items-center justify-between gap-2 border px-3 py-2 ${className}`}>
    <span>{status?.tier==='go'?'Go':status?.tier==='plus'?'Plus':'Free'} · {label}: <strong>{remaining}/{limit}</strong> {ar?'متبقي':'remaining'}</span>
    <Link href="/settings/subscription">{ar?'التجديد':'Resets'} {new Date(quota.resets_at).toLocaleDateString(ar?'ar':'en-US')}</Link>
  </div>
}
