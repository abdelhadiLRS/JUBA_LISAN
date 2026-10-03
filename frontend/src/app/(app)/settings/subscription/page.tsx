'use client'
import {useEffect,useState} from 'react'
import Link from 'next/link'
import {useLocale} from 'next-intl'
import {apiFetch} from '@/lib/api'
import {useAuthStore} from '@/store/auth'
import PricingSection from '@/components/billing/PricingSection'

type Quota={limit:number;used:number;reserved:number;remaining:number;unit:string;period:string;resets_at:string}
type State={tier:string;metered:boolean;features:Record<string,Quota>;voice_session_max_seconds:number}
export default function SubscriptionSettings(){
  const locale=useLocale(),ar=locale.startsWith('ar'),token=useAuthStore(s=>s.accessToken)
  const [state,setState]=useState<State|null>(null),[error,setError]=useState(false),[retry,setRetry]=useState(0)
  useEffect(()=>{const controller=new AbortController();setError(false);setState(null)
    void apiFetch('/api/subscriptions/me',{signal:controller.signal}).then(async response=>{if(!response.ok)throw new Error();const data=await response.json();if(!controller.signal.aborted)setState(data)}).catch(()=>{if(!controller.signal.aborted)setError(true)})
    return()=>controller.abort()
  },[token,retry])
  const labels:Record<string,string>=ar?{chat:'رسائل المعلم',lessons:'دروس جديدة',reading:'تمارين القراءة',listening:'تمارين الاستماع',flashcards:'بطاقات مولّدة',translation:'الترجمة والتصحيح',voice:'المحادثة الصوتية',tts:'صوت النطق'}:{chat:'Tutor messages',lessons:'New lessons',reading:'Reading exercises',listening:'Listening exercises',flashcards:'Generated cards',translation:'Translation and correction',voice:'Voice conversation',tts:'Pronunciation audio'}
  return <main dir={ar?'rtl':'ltr'}><Link href="/settings">{ar?'العودة إلى الإعدادات':'Back to settings'}</Link><h1 className="text-2xl font-semibold my-6">{ar?'اشتراكك واستخدامك':'Your subscription and usage'}</h1>
    {error?<p role="alert">{ar?'تعذّر تحميل الاستخدام.':'Could not load usage.'} <button onClick={()=>setRetry(x=>x+1)}>{ar?'أعد المحاولة':'Retry'}</button></p>:!state?<p role="status">{ar?'جارٍ تحميل الاستخدام':'Loading usage'}</p>:<>
      <p className="mb-4">{ar?'الباقة الحالية':'Current plan'}: <strong>{state.tier==='go'?'Go':state.tier==='plus'?'Plus':'Free'}</strong>{!state.metered&&` (${ar?'وضع محلي بلا حصص مدفوعة':'self-hosted, no paid quota enforcement'})`}</p>
      <div className="overflow-x-auto border rounded-md"><table className="w-full min-w-[640px] text-start"><caption className="sr-only">{ar?'الاستهلاك الفعلي حسب الميزة':'Actual usage by feature'}</caption><thead><tr>{(ar?['الميزة','المستخدم','المتبقي','طلبات جارية','التجديد']:['Feature','Used','Remaining','In progress','Reset']).map(name=><th key={name} className="p-3 text-start">{name}</th>)}</tr></thead><tbody>{Object.entries(state.features).map(([key,q])=><tr key={key} className="border-t"><th scope="row" className="p-3 text-start font-normal">{labels[key]||key}{q.unit==='seconds'&&` (${ar?'ثانية':'seconds'})`}</th><td className="p-3">{q.used}/{q.limit}</td><td className="p-3">{q.remaining}</td><td className="p-3">{q.reserved}</td><td className="p-3">{new Date(q.resets_at).toLocaleString(locale)}</td></tr>)}</tbody></table></div>
      <p className="my-4">{ar?'الحصص مشتركة بين لغات الحساب، بلا ترحيل. الطلب الجاري يُحجز مؤقتًا ثم يُخصم عند نجاحه فقط.':'Allowances are shared across account languages, without rollover. In-flight requests reserve quota temporarily and consume it only on success.'}</p>
    </>}
    <PricingSection stripeEnabled={true} trialDays={7} hasSession={!!token} priceMonthly={0} priceYearly={0} totalPriceMonthly={0} totalPriceYearly={0}/>
  </main>
}
