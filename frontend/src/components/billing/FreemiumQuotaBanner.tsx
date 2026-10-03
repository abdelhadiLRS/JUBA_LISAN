'use client'
import Link from 'next/link'
import {useLocale} from 'next-intl'
import {useAccountQuota} from '@/hooks/useAccountQuota'

type Feature='chat'|'lessons'|'listening'|'reading'|'voice'|'flashcards'|'translation'|'tts'
export function FreemiumQuotaBanner({feature,className=''}:{feature:Feature;className?:string}){
 const locale=useLocale(),ar=locale.startsWith('ar')
 const {state,quota,failed,refresh}=useAccountQuota(feature)
 if(state&&!state.metered)return null
 if(failed)return <p className={className} role="status">{ar?'تعذّر تحديث الحصة.':'Could not update allowance.'} <button type="button" onClick={()=>void refresh()} className="min-h-11 underline">{ar?'أعد المحاولة':'Retry'}</button> <Link href="/settings/subscription">{ar?'تفاصيل الاشتراك':'Subscription details'}</Link></p>
 if(!state||!quota)return null
 // Do not floor sub-minute balances to zero: 30 usable seconds are not exhaustion.
 const label=ar?({chat:'رسائل المعلم',lessons:'دروس جديدة',listening:'تمارين استماع جديدة',reading:'تمارين قراءة جديدة',voice:'المحادثة الصوتية',flashcards:'بطاقات جديدة',translation:'ترجمة وتصحيح',tts:'صوت النطق'})[feature]:({chat:'Tutor messages',lessons:'New lessons',listening:'New listening exercises',reading:'New reading exercises',voice:'Voice conversation',flashcards:'New cards',translation:'Translation and correction',tts:'Pronunciation audio'})[feature]
 const number=new Intl.NumberFormat(locale),unit=quota.unit==='seconds'?(ar?' ثانية':' sec'):''
 return <div className={`juba-billing-quota flex flex-wrap items-center justify-between gap-2 border px-3 py-2 ${className}`}>
  <span>{state.tier==='go'?'Go':state.tier==='plus'?'Plus':'Free'} · {label}: <strong>{number.format(quota.remaining)}/{number.format(quota.limit)}{unit}</strong> {ar?'متبقي':'remaining'}</span>
  <Link href="/settings/subscription">{ar?'التجديد':'Resets'} {new Date(quota.resets_at).toLocaleString(locale)}</Link>
 </div>
}
