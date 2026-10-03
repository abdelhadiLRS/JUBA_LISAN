'use client'

import Link from 'next/link'
import {useEffect, useRef, useState} from 'react'
import {useLocale} from 'next-intl'
import {apiFetch} from '@/lib/api'
import {useAuthStore} from '@/store/auth'
import './subscription-pricing.css'

type Tier = 'free' | 'go' | 'plus'
type Interval = 'monthly' | 'yearly'
type Allowance = {limit:number;period:'day'|'week'|'month';unit:'requests'|'cards'|'seconds'}
type Plan = {tier:Tier;prices:Record<Interval,number>;checkout_available:Record<Interval,boolean>;voice_session_max_seconds:number;allowances:Record<string,Allowance>}
type Catalog = {currency:string;metered:boolean;plans:Plan[];trial:{tier:string;days:number;card_required:boolean}}
type Account = {tier:Tier;subscription_status:string;trial_available:boolean;trial_ends_at:string|null}
interface PricingSectionProps {stripeEnabled:boolean;trialDays:number;hasSession:boolean;priceMonthly:number;priceYearly:number;totalPriceMonthly:number;totalPriceYearly:number}

export default function PricingSection(props:PricingSectionProps) {
  const locale = useLocale(), ar = locale.startsWith('ar')
  const token = useAuthStore(s=>s.accessToken)
  const signedIn = props.hasSession || !!token
  const [catalog,setCatalog] = useState<Catalog|null>(null)
  const [account,setAccount] = useState<Account|null>(null)
  const [allowRegistration,setAllowRegistration] = useState(false)
  const [interval,setInterval] = useState<Interval>('monthly')
  const [error,setError] = useState<string|null>(null)
  const [loading,setLoading] = useState<string|null>(null)
  const [retry,setRetry] = useState(0)
  const lock = useRef(false), epoch = useRef(0)
  const word = (arabic:string, english:string)=>ar?arabic:english
  useEffect(()=>{
    const version = ++epoch.current, controller = new AbortController()
    const timeout = setTimeout(()=>controller.abort(),12000)
    setCatalog(null);setAccount(null);setError(null);setLoading(null)
    void (async()=>{
      try {
        const response = await apiFetch('/api/config',{signal:controller.signal})
        if(!response.ok)throw new Error()
        const config = await response.json()
        const products = config.subscription_catalog as Catalog|undefined
        if(!products || !Array.isArray(products.plans) || products.plans.length!==3)throw new Error()
        let current:Account|null = null
        if(signedIn){
          const res = await apiFetch('/api/subscriptions/me',{signal:controller.signal})
          if(!res.ok)throw new Error()
          current = await res.json()
        }
        if(version!==epoch.current)return
        setCatalog(products);setAllowRegistration(config.allow_registration===true);setAccount(current)
      }catch{if(version===epoch.current)setError(ar?'تعذّر تحميل الباقات.':'Could not load plans.')}
      finally{clearTimeout(timeout)}
    })()
    return()=>{epoch.current++;controller.abort();clearTimeout(timeout)}
  },[signedIn,token,retry,ar])

  async function act(kind:'checkout'|'portal'|'trial', tier?:Tier) {
    if(lock.current || !catalog || !signedIn)return
    lock.current=true;setLoading(kind==='checkout'?tier!:kind);setError(null)
    const version=epoch.current
    try {
      const response=await apiFetch(kind==='trial'?'/api/subscriptions/trial':`/api/billing/${kind}`,{
        method:'POST',headers:{'Content-Type':'application/json'},
        ...(kind==='checkout'?{body:JSON.stringify({tier,interval})}:{})})
      if(!response.ok)throw new Error()
      const data=await response.json()
      if(version!==epoch.current)return
      if(kind==='trial'){setRetry(x=>x+1);return}
      if(typeof data.url!=='string')throw new Error()
      const url=new URL(data.url)
      const expected=kind==='portal'?'billing.stripe.com':'checkout.stripe.com'
      if(url.protocol!=='https:' || url.hostname!==expected)throw new Error()
      window.location.assign(url.toString())
    }catch{if(version===epoch.current)setError(ar?'تعذّر تنفيذ الطلب. لم يتم تأكيد أي دفع.':'Request failed. No payment was confirmed.')}
    finally{lock.current=false;if(version===epoch.current)setLoading(null)}
  }
  const names:Record<string,string>={chat:word('رسائل المعلم','Tutor messages'),lessons:word('دروس جديدة','New lessons'),
    reading:word('تمارين قراءة جديدة','New reading exercises'),listening:word('تمارين استماع جديدة','New listening exercises'),
    flashcards:word('بطاقات مولّدة بالذكاء الاصطناعي','AI-generated cards'),translation:word('ترجمة وتصحيح مستقل','Translation and standalone correction'),
    voice:word('محادثة صوتية','Voice conversation'),tts:word('صوت نطق جديد خارج المحادثة','Standalone pronunciation audio')}
  function allowance(value:Allowance) {
    const number=value.unit==='seconds'?value.limit/60:value.limit
    const unit=value.unit==='seconds'?word('دقيقة','min'):value.unit==='cards'?word('بطاقة','cards'):''
    const period=value.period==='day'?word('يوم','day'):value.period==='week'?word('أسبوع','week'):word('شهر','month')
    return `${new Intl.NumberFormat(locale).format(number)} ${unit} / ${period}`
  }
  function action(plan:Plan) {
    if(!signedIn)return <Link className="juba-tier-action" href={allowRegistration?`/register?tier=${plan.tier}&interval=${interval}`:'/login'}>{allowRegistration?word('ابدأ','Get started'):word('تسجيل الدخول','Sign in')}</Link>
    if(plan.tier==='free' || !catalog?.metered)return <Link className="juba-tier-action" href="/dashboard">{word('واصل التعلم','Keep learning')}</Link>
    if(account?.subscription_status==='active' || account?.subscription_status==='trialing')return <button className="juba-tier-action" disabled={!!loading} onClick={()=>void act('portal')}>{account.tier===plan.tier?word('إدارة اشتراكك','Manage subscription'):word('تغيير الباقة','Change plan')}</button>
    return <button className="juba-tier-action" disabled={!!loading || !plan.checkout_available[interval]} onClick={()=>void act('checkout',plan.tier)}>{loading===plan.tier?word('جارٍ التحويل','Opening checkout'):plan.checkout_available[interval]?word('اشترك','Subscribe'):word('الدفع غير مفعّل بعد','Checkout not configured')}</button>
  }
  return <section className="juba-tier-pricing" aria-labelledby="juba-landing-pricing-title" dir={ar?'rtl':'ltr'}>
    <header><div><h2 id="juba-landing-pricing-title">{word('اختر مساحة تعلّمك','Choose your learning plan')}</h2><p>{word('نفس قواعد التعلّم والمنافسة. حصص ذكاء اصطناعي مختلفة.','Same learning and competition rules. Different AI allowances.')}</p></div>
      <div className="juba-tier-interval" role="group" aria-label={word('مدة الفوترة','Billing interval')}>
        {(['monthly','yearly'] as const).map(value=><button key={value} type="button" aria-pressed={interval===value} disabled={!!loading} onClick={()=>setInterval(value)}>{value==='monthly'?word('شهري','Monthly'):word('سنوي','Yearly')}</button>)}
      </div></header>
    {error&&<p role="alert">{error} <button disabled={!!loading} onClick={()=>setRetry(x=>x+1)}>{word('إعادة المحاولة','Retry')}</button></p>}
    {!catalog&&!error&&<p role="status">{word('جارٍ تحميل الأسعار والحدود','Loading prices and limits')}</p>}
    {catalog&&<><div className="juba-tier-table" role="region" aria-label={word('مقارنة الباقات','Plan comparison')} tabIndex={0}><table>
      <caption className="sr-only">{word('أسعار وحدود Free وGo وPlus','Free, Go and Plus prices and limits')}</caption>
      <thead><tr><th scope="col">{word('المزايا','Features')}</th>{catalog.plans.map(plan=><th key={plan.tier} scope="col"><span className="juba-tier-name">{plan.tier==='free'?'Free':plan.tier==='go'?'Go':'Plus'}</span>
        <span className="juba-tier-price">{new Intl.NumberFormat(locale,{style:'currency',currency:catalog.currency}).format(plan.prices[interval]/100)}</span><span className="juba-tier-period">{interval==='monthly'?word('في الشهر','per month'):word('في السنة، تُدفع سنويًا','per year, billed annually')}</span>{action(plan)}</th>)}</tr></thead>
      <tbody>{Object.entries(names).map(([key,label])=><tr key={key}><th scope="row">{label}</th>{catalog.plans.map(plan=><td key={plan.tier}>{allowance(plan.allowances[key])}</td>)}</tr>)}
        <tr><th scope="row">{word('الحد الأقصى للجلسة الصوتية','Maximum voice session')}</th>{catalog.plans.map(plan=><td key={plan.tier}>{plan.voice_session_max_seconds/60} {word('دقيقة','min')}</td>)}</tr>
        <tr><th scope="row">{word('التقييم، الخطة، المراجع والمراجعة','Assessment, plan, references and review')}</th>{catalog.plans.map(plan=><td key={plan.tier}>{word('متاحة','Included')}</td>)}</tr>
        <tr><th scope="row">{word('الألعاب والدوريات','Games and leagues')}</th>{catalog.plans.map(plan=><td key={plan.tier}>{word('نفس قواعد XP','Same XP rules')}</td>)}</tr>
      </tbody></table></div>
      {!catalog.metered?<p>{word('الوضع المحلي بلا بوابة دفع. هذه حصص الخدمة المستضافة وليست قيودًا على نسختك المحلية.','Self-hosted mode has no paywall. These are hosted-service allowances, not limits on your local installation.')}</p>:<p>{word('الحصص مشتركة بين لغات الحساب وتتجدد بتوقيت UTC، بلا ترحيل. المراجعة والطلبات الفاشلة لا تخصم حصة التوليد.','Allowances are shared across account languages and reset in UTC, without rollover. Reviews and failed requests do not consume generation quota.')}</p>}
      {catalog.metered&&<p>{word('حتى 2000 حرف للرسالة، 1000 حرف للترجمة، و20 بطاقة في طلب التوليد الواحد. لا أفضلية مدفوعة في XP.','Up to 2,000 characters per tutor message, 1,000 per translation and 20 cards per generation request. No paid XP advantage.')}</p>}
      {account?.trial_available&&<button className="juba-tier-trial" disabled={!!loading} onClick={()=>void act('trial')}>{word('جرّب Go لمدة 7 أيام دون بطاقة','Try Go for 7 days, no card')}</button>}
      {account?.trial_ends_at&&<p>{word('تنتهي التجربة في','Trial ends on')} {new Date(account.trial_ends_at.endsWith('Z')?account.trial_ends_at:`${account.trial_ends_at}Z`).toLocaleDateString(locale)}</p>}
    </>}
  </section>
}
