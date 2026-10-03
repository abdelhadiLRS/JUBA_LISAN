'use client'
import Link from 'next/link'
import {useLocale} from 'next-intl'
import {useEffect,useState} from 'react'
import {pendingProductSelection,productQuery} from '@/lib/subscription-selection'

/** All payment entry points go through one tier-aware, server-backed catalog. */
export function SubscriptionPlanButtons({className=''}:{className?:string}){
 const ar=useLocale().startsWith('ar'),[query,setQuery]=useState('')
 useEffect(()=>{setQuery(productQuery(pendingProductSelection()))},[])
 return <div className={`juba-billing-actions ${className}`}><Link className="juba-primary-button inline-flex min-h-11 items-center justify-center px-4 py-3" href={`/settings/subscription${query?'?'+query:''}`}>
 {ar?'قارن Free وGo وPlus واختر باقتك':'Compare Free, Go and Plus'}</Link></div>
}
