'use client'
import Link from 'next/link'
import {useLocale} from 'next-intl'
import {useEffect,useState} from 'react'
import {apiFetch} from '@/lib/api'
import {useAuthStore} from '@/store/auth'

type Feature='chat'|'voice'|'listening'|'reading'|'lessons'
type Account={tier:string;metered:boolean;features:Record<string,{remaining:number;resets_at:string}>}
export function PaywallBanner({feature='chat',compact=false}:{feature?:Feature;compact?:boolean}){
 const locale=useLocale(),ar=locale.startsWith('ar'),token=useAuthStore(s=>s.accessToken)
 const [account,setAccount]=useState<Account|null>(null)
 useEffect(()=>{const controller=new AbortController()
  void apiFetch('/api/subscriptions/me',{signal:controller.signal}).then(async res=>{if(res.ok){const data=await res.json();if(!controller.signal.aborted)setAccount(data)}}).catch(()=>{})
  return()=>controller.abort()
 },[token,feature])
 if(account&&!account.metered)return null
 const quota=account?.features[feature]
 return <section className={`juba-billing-quota border border-[var(--duo-line)] bg-[var(--duo-card)] ${compact?'p-4':'mx-auto max-w-lg p-6'}`} aria-live="polite">
  <h2 className="text-lg font-semibold">{ar?'وصلت إلى حد الحصة الحالية':'Current allowance reached'}</h2>
  <p className="my-3">{ar?'قراءة المحتوى المحفوظ ومراجعته متاحة. راجع موعد التجديد أو خيارات باقتك.':'Saved content and review remain available. Check the reset time or your plan options.'}</p>
  {quota&&<p>{ar?'التجديد':'Resets'}: {new Date(quota.resets_at).toLocaleString(locale)}</p>}
  <Link className="juba-primary-button inline-flex min-h-11 items-center px-4 py-2 mt-3" href="/settings/subscription">{ar?'الاشتراك والحصص':'Plan and allowances'}</Link>
 </section>
}
