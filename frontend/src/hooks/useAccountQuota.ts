'use client'
import {useCallback,useEffect,useState} from 'react'
import {apiFetch} from '@/lib/api'
import {useAuthStore} from '@/store/auth'
export type QuotaSnapshot={remaining:number;limit:number;resets_at:string;period:string;unit:string}
export type AccountQuota={tier:string;metered:boolean;features:Record<string,QuotaSnapshot>}
export function useAccountQuota(feature:string){
 const token=useAuthStore(s=>s.accessToken),[state,setState]=useState<AccountQuota|null>(null),[failed,setFailed]=useState(false)
 const refresh=useCallback(async()=>{
  if(!token)return null
  try{const response=await apiFetch('/api/subscriptions/me');if(!response.ok)throw new Error();const data=await response.json() as AccountQuota
   // Ignore responses from an account/session that has changed during the request.
   if(useAuthStore.getState().accessToken!==token)return null
   setState(data);setFailed(false);return data
  }catch{if(useAuthStore.getState().accessToken===token)setFailed(true);return null}
 },[token])
 useEffect(()=>{setState(null);setFailed(false);void refresh();const timer=setInterval(()=>{if(!document.hidden)void refresh()},60000);return()=>clearInterval(timer)},[refresh])
 const quota=state?.features[feature]
 return {state,quota,failed,refresh,exhausted:state?.metered===true&&!!quota&&quota.remaining<=0}
}
