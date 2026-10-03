import {apiFetch} from '@/lib/api'
import {useAuthStore} from '@/store/auth'

interface LandingSubscriptionState{subscribed:boolean;trialUsed:boolean}
let pending:{token:string|null;promise:Promise<LandingSubscriptionState>}|null=null

/** Share only an in-flight request for the same token, never stale account state. */
export async function getLandingSubscriptionState():Promise<LandingSubscriptionState>{
  const token=useAuthStore.getState().accessToken
  if(pending?.token===token)return pending.promise
  const promise=(async()=>{
    const controller=new AbortController()
    const timeout=setTimeout(()=>controller.abort(),12000)
    try{
      // apiFetch handles refresh through the centralized auth flow.
      const response=await apiFetch('/api/auth/me',{signal:controller.signal})
      if(!response.ok)throw new Error('Subscription status could not be verified')
      const me=await response.json()
      if(typeof me.subscription_status!=='string')throw new Error('Invalid subscription status')
      return {subscribed:me.subscription_status==='active'||me.subscription_status==='trialing',trialUsed:me.trial_used===true}
    }finally{clearTimeout(timeout)}
  })()
  const request={token,promise};pending=request
  try{return await promise}finally{if(pending===request)pending=null}
}

/** Legacy boolean read; cannot authorize payment. Strict callers use the state API. */
export async function hasActiveLandingSubscription():Promise<boolean>{
  try{return (await getLandingSubscriptionState()).subscribed}catch{return false}
}
