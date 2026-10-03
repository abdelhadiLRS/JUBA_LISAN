'use client'

import Link from 'next/link'
import {useEffect,useRef,useState} from 'react'
import {useTranslations} from 'next-intl'
import {Circle,CircleDot,Diamond,Check,Minus} from 'lucide-react'
import {getLandingSubscriptionState} from '@/lib/landing-subscription'
import {pricingAction,type PricingAction} from '@/lib/landing-pricing-policy'
import {apiFetch} from '@/lib/api'
import {useAuthStore} from '@/store/auth'

type BillingInterval='monthly'|'yearly'
interface PricingSectionProps{stripeEnabled:boolean;trialDays:number;hasSession:boolean;priceMonthly:number;priceYearly:number;totalPriceMonthly:number;totalPriceYearly:number}
type Config={ready:boolean;allowRegistration:boolean;stripeEnabled:boolean;trialDays:number;monthly:number;yearly:number;originalMonthly:number;originalYearly:number}
export default function PricingSection(props:PricingSectionProps){
  const t=useTranslations('billing'),landing=useTranslations('landing'),common=useTranslations('common')
  const [config,setConfig]=useState<Config>({ready:false,allowRegistration:false,stripeEnabled:props.stripeEnabled,trialDays:props.trialDays,monthly:props.priceMonthly,yearly:props.priceYearly,originalMonthly:props.totalPriceMonthly,originalYearly:props.totalPriceYearly})
  const [subscribed,setSubscribed]=useState<boolean|null>(props.hasSession?null:false)
  const [trialUsed,setTrialUsed]=useState(false)
  const [loading,setLoading]=useState<BillingInterval|null>(null)
  const [error,setError]=useState<string|null>(null)
  const [retry,setRetry]=useState(0)
  const lock=useRef(false),context=useRef(0)
  const token=useAuthStore(s=>s.accessToken)
  useEffect(()=>{
    const epoch=++context.current
    const controller=new AbortController()
    const timeout=setTimeout(()=>controller.abort(),10000)
    setConfig(value=>({...value,ready:false}));setError(null)
    setSubscribed(props.hasSession?null:false)
    const number=(value:unknown,fallback:number)=>typeof value==='number'&&Number.isFinite(value)&&value>=0?value:fallback
    void apiFetch('/api/config',{signal:controller.signal}).then(async response=>{
      if(!response.ok)throw new Error()
      const data=await response.json()
      if(epoch!==context.current)return
      setConfig({ready:true,allowRegistration:data.allow_registration===true,stripeEnabled:data.stripe_enabled===true,trialDays:number(data.stripe_trial_days,0),monthly:number(data.price_monthly,0),yearly:number(data.price_yearly,0),originalMonthly:number(data.total_price_monthly,0),originalYearly:number(data.total_price_yearly,0)})
    }).catch(()=>{if(epoch===context.current)setError(common('error'))}).finally(()=>clearTimeout(timeout))
    if(props.hasSession)void getLandingSubscriptionState().then(state=>{
      if(epoch!==context.current)return
      setSubscribed(state.subscribed);setTrialUsed(state.trialUsed)
    }).catch(()=>{if(epoch===context.current)setError(common('error'))})
    return()=>{context.current++;controller.abort();clearTimeout(timeout)}
  },[props.hasSession,token,retry,common])
  function action(paid:boolean,price:number):PricingAction{return pricingAction({paid,price,hasSession:props.hasSession,allowRegistration:config.allowRegistration,stripeEnabled:config.stripeEnabled,subscribed,configReady:config.ready})}
  async function checkout(interval:BillingInterval){
    const price=interval==='monthly'?config.monthly:config.yearly
    if(lock.current||action(true,price)!=='checkout')return
    lock.current=true;setLoading(interval);setError(null)
    const epoch=context.current
    try{
      // Recheck billing immediately before payment, even if cached landing data
      // or another browser tab changed the server configuration.
      const fresh=await apiFetch('/api/config')
      if(!fresh.ok)throw new Error(t('checkoutError'))
      const cfg=await fresh.json()
      const currentPrice=interval==='monthly'?cfg.price_monthly:cfg.price_yearly
      if(cfg.stripe_enabled!==true||typeof currentPrice!=='number'||currentPrice<=0)throw new Error(t('checkoutError'))
      if(epoch!==context.current)return
      const response=await apiFetch('/api/billing/checkout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({plan:interval})})
      if(!response.ok)throw new Error(t('checkoutError'))
      const data=await response.json()
      if(typeof data.url!=='string')throw new Error(t('checkoutError'))
      const url=new URL(data.url)
      if(url.protocol!=='https:')throw new Error(t('checkoutError'))
      if(epoch===context.current)window.location.assign(url.toString())
    }catch{if(epoch===context.current)setError(t('checkoutError'))}finally{lock.current=false;if(epoch===context.current)setLoading(null)}
  }
  const paidLabel=trialUsed||config.trialDays<=0?t('ctaRegisterTrialUsed'):t('ctaRegister')
  const plans=[{name:t('planFreeBadge'),icon:Circle,paid:false,interval:'monthly' as BillingInterval,price:0,original:0,period:'',badge:null,desc:t('planFreeDesc')},{name:t('planMonthlyName'),icon:CircleDot,paid:true,interval:'monthly' as BillingInterval,price:config.monthly,original:config.originalMonthly,period:t('month'),badge:config.trialDays>0&&!trialUsed?t('trialDays',{days:config.trialDays}):t('trialBadgeTrialUsed'),desc:null},{name:t('planYearlyName'),icon:Diamond,paid:true,interval:'yearly' as BillingInterval,price:config.yearly,original:config.originalYearly,period:t('year'),badge:t('bestValue'),desc:null}]
  // Paid plans are not advertised when server configuration disables billing.
  const visiblePlans=config.stripeEnabled?plans:plans.slice(0,1)
  function cta(paid:boolean,interval:BillingInterval,price:number){
    const state=action(paid,price)
    if(state==='wait')return <button type="button" disabled className="juba-ff-plan-cta" aria-busy="true">{common('loading')}</button>
    if(state==='checkout')return <button type="button" className="juba-ff-plan-cta inline-block px-6 py-2.5 text-center font-semibold" disabled={loading!==null} onClick={()=>void checkout(interval)}>{loading===interval?t('checkoutLoading'):paidLabel}</button>
    const href=state==='dashboard'?'/dashboard':state==='login'?'/login':paid?`/register?plan=${interval}`:'/register'
    const label=state==='dashboard'?landing('dashboard'):state==='login'?landing('signIn'):paid?paidLabel:t('planFreeCta')
    return <Link href={href} className={paid?'juba-ff-plan-cta inline-block px-6 py-2.5 text-center':'juba-ff-plan-free-link inline-block px-6 py-2.5 text-center'}>{label}</Link>
  }
  const rows=[...['f1','f2','f3','f4','f5'].map(key=>({label:t(`freeFeature.${key}`),free:true as boolean|'limited',monthly:true,yearly:true})),...['l1','l2','l3','l4','l5'].map(key=>({label:t(`freeFeature.${key}`),free:'limited' as const,monthly:true,yearly:true})),{label:t('planFeature.feature1'),free:false,monthly:true,yearly:true},{label:t('planFeature.feature2'),free:false,monthly:false,yearly:true}]
  return <section aria-labelledby="juba-landing-pricing-title" className="juba-ff-pricing w-full">
    <div className="juba-ff-pricing-intro mx-auto mb-10 max-w-3xl px-5 text-center"><h2 id="juba-landing-pricing-title" className="juba-ff-pricing-title">{t('pricingTitle')}</h2>{config.ready&&config.stripeEnabled&&<p>{trialUsed||config.trialDays<=0?t('pricingDescTrialUsed'):t('pricingDesc',{days:config.trialDays})}</p>}</div>
    {error&&<div role="alert" className="juba-ff-plan-error mb-4"><p>{error}</p><button type="button" disabled={loading!==null} onClick={()=>setRetry(value=>value+1)}>{common('retry')}</button></div>}
    <div className={`mb-12 grid grid-cols-1 gap-4 ${config.stripeEnabled?'md:grid-cols-3':''}`}>
      {visiblePlans.map(plan=>{const Icon=plan.icon;return <div key={plan.name} className={`juba-ff-plan-card flex flex-col gap-4 border border-[var(--busuu-line)] p-6 ${!plan.paid?'juba-ff-plan-free':plan.interval==='yearly'?'juba-ff-plan-yearly':'juba-ff-plan-paid'}`}><div className="juba-ff-plan-head flex items-center justify-between border-b pb-3"><div className="flex items-center gap-2"><Icon className="juba-ff-plan-icon h-5 w-5"/><span className="juba-ff-plan-name font-semibold">{plan.name}</span></div>{plan.badge&&<span className="juba-ff-plan-badge border px-2 py-1">{plan.badge}</span>}</div><div className="min-h-[4.25rem]">{plan.paid?<>{plan.original>plan.price&&<p className="juba-ff-plan-old line-through">{t('priceOriginal',{price:plan.original,period:plan.period})}</p>}<p className="juba-ff-plan-price flex items-baseline gap-2 text-2xl font-bold">{config.ready&&plan.price>0?t('priceAmount',{amount:plan.price}):common('loading')}<span className="juba-ff-period text-sm">/ {plan.period}</span></p></>:<p className="juba-ff-plan-desc text-sm">{config.ready&&!config.stripeEnabled?landing('heroSub'):plan.desc}</p>}</div>{cta(plan.paid,plan.interval,plan.price)}</div>})}
    </div>
    {config.ready&&config.stripeEnabled&&<><div className="juba-ff-comparison overflow-x-auto border border-[var(--busuu-line)]" role="region" aria-label={t('pricingTitle')} tabIndex={0}><table className="w-full min-w-[680px] table-fixed"><caption className="sr-only">{t('pricingTitle')}</caption><thead><tr className="juba-ff-comparison-head border-b"><th className="w-[42%] px-5 py-3 text-start"><span className="sr-only">{landing('navFeatures')}</span></th>{[t('planFreeName'),t('planMonthlyName'),t('planYearlyName')].map(name=><th key={name} className="px-4 py-3 text-center">{name}</th>)}</tr></thead><tbody>{rows.map((row,index)=><tr key={index} className="border-b border-[var(--busuu-line)]"><th scope="row" className="juba-ff-table-cell px-5 py-3 text-start text-xs font-normal">{row.label}</th>{[row.free,row.monthly,row.yearly].map((value,column)=><td key={column} className="px-4 py-3 text-center">{value==='limited'?<span className="juba-ff-limited text-xs">{t('limitedLabel')}</span>:value?<Check className="juba-ff-check mx-auto h-4 w-4" aria-label={common('done')}/>:<Minus className="juba-ff-minus mx-auto h-4 w-4" aria-label={common('back')}/>}</td>)}</tr>)}</tbody></table></div><div className="mt-8 text-center">{cta(true,'yearly',config.yearly)}</div></>}
  </section>
}
