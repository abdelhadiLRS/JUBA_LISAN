'use client'
import {useCallback,useEffect,useRef,useState} from 'react'
import {apiFetch} from '@/lib/api'
import {useAuthStore} from '@/store/auth'
import {parseQuotaResponse,quotaAccountKey,type AccountQuota} from '@/lib/quota-client'
export type {QuotaSnapshot,AccountQuota} from '@/lib/quota-client'

export function useAccountQuota(feature:string){
 const token=useAuthStore(s=>s.accessToken),user=useAuthStore(s=>s.user)
 const key=quotaAccountKey(token,user)
 const [snapshot,setSnapshot]=useState<{key:string;data:AccountQuota}|null>(null),[failed,setFailed]=useState(false)
 const lifecycle=useRef(0),request=useRef<{key:string;controller:AbortController;promise:Promise<AccountQuota|null>}|null>(null)
 const refresh=useCallback(()=>{
  if(!key)return Promise.resolve(null)
  if(request.current?.key===key&&!request.current.controller.signal.aborted)return request.current.promise
  const version=lifecycle.current,controller=new AbortController()
  const sameAccount=()=>{const current=useAuthStore.getState();return !controller.signal.aborted&&version===lifecycle.current&&quotaAccountKey(current.accessToken,current.user)===key}
  const promise=(async()=>{
   const timeout=setTimeout(()=>controller.abort(),12000)
   try{
    const response=await apiFetch('/api/subscriptions/me',{signal:controller.signal})
    if(!response.ok)throw new Error('Could not read quota')
    const data=parseQuotaResponse(await response.json())
    if(!sameAccount())return null
    setSnapshot({key,data});setFailed(false);return data
   }catch{if(version===lifecycle.current&&quotaAccountKey(useAuthStore.getState().accessToken,useAuthStore.getState().user)===key)setFailed(true);return null}
   finally{clearTimeout(timeout);if(request.current?.controller===controller)request.current=null}
  })()
  request.current={key,controller,promise}
  return promise
 },[key])
 useEffect(()=>{
  lifecycle.current++;request.current?.controller.abort();request.current=null;setSnapshot(null);setFailed(false)
  void refresh()
  const onVisible=()=>{if(!document.hidden)void refresh()}
  const timer=setInterval(onVisible,60000)
  window.addEventListener('focus',onVisible);document.addEventListener('visibilitychange',onVisible)
  return()=>{lifecycle.current++;request.current?.controller.abort();request.current=null;clearInterval(timer);window.removeEventListener('focus',onVisible);document.removeEventListener('visibilitychange',onVisible)}
 },[refresh])
 const state=snapshot?.key===key?snapshot.data:null,quota=state?.features[feature]
 return {state,quota,failed,refresh,exhausted:state?.metered===true&&!!quota&&quota.remaining<=0}
}
