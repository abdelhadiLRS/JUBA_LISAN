import {create} from 'zustand'
import {useConfigStore} from '@/store/config'
import {freeTrialActive} from '@/lib/subscription-time'

export type SubscriptionStatus='none'|'incomplete'|'incomplete_expired'|'trialing'|'active'|'past_due'|'canceled'|'unpaid'|'paused'
export interface User{
 id:number
 username:string
 displayName:string
 email?:string
 native_language?:string
 target_language?:string
 ui_locale?:string|null
 role:'admin'|'user'
 conversation_max_duration:number
 conversation_inactivity_timeout:number
 avatar?:string|null
 is_verified?:boolean
 bio?:string|null
 learning_goals?:string[]|null
 subscription_status?:SubscriptionStatus
 subscription_ends_at?:string|null
 cancel_at_period_end?:boolean
 trial_used?:boolean
 assessment_voice_trial_used?:boolean
 freemium_trial_ends_at?:string|null
 freemium_trial_used?:boolean
 dismissed_dashboard_banner_revision?:number|null
}
/** Paid state only; active does not mean feature quotas are unlimited. */
export function isSubscribed(user:User|null,stripeEnabled:boolean):boolean{
 return !stripeEnabled||user?.subscription_status==='active'||user?.subscription_status==='trialing'
}
export function needsPaymentRecovery(user:User|null):boolean{
 return user?.subscription_status==='past_due'||user?.subscription_status==='unpaid'||user?.subscription_status==='paused'
}
export function isFreemiumTrialActive(user:User|null,stripeEnabled:boolean):boolean{
 return freeTrialActive(user,stripeEnabled,useConfigStore.getState().freemiumTrialEnabled)
}
interface AuthStore{
 accessToken:string|null
 user:User|null
 setTokens:(access:string)=>void
 setUser:(user:User)=>void
 setDismissedDashboardBannerRevision:(revision:number)=>void
 logout:()=>void
}
export const useAuthStore=create<AuthStore>(set=>({
 accessToken:null,user:null,
 setTokens:(access:string)=>set({accessToken:access}),
 setUser:(user:User)=>set({user}),
 setDismissedDashboardBannerRevision:(revision:number)=>set(state=>({user:state.user?{...state.user,dismissed_dashboard_banner_revision:revision}:null})),
 logout:()=>{
  if(typeof window!=='undefined'){try{localStorage.removeItem('fl_tour_done')}catch{}}
  set({accessToken:null,user:null})
 }
}))
