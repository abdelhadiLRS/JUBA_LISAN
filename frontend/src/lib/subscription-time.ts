/** Backend naive database timestamps represent UTC, never browser local time. */
export function subscriptionTimestamp(value:string|null|undefined):number|null{
 if(!value)return null
 const text=value.trim()
 // Require ISO datetime, rather than Date.parse's locale-dependent formats.
 if(!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$/i.test(text))return null
 const withZone=/(Z|[+-]\d{2}:?\d{2})$/i.test(text)?text:`${text}Z`
 const result=Date.parse(withZone)
 return Number.isFinite(result)?result:null
}
export function freeTrialActive(user:{subscription_status?:string;freemium_trial_ends_at?:string|null}|null,stripeEnabled:boolean,trialEnabled:boolean,now=Date.now()):boolean{
 if(!stripeEnabled||!trialEnabled||!user||user.subscription_status==='active'||user.subscription_status==='trialing')return false
 const end=subscriptionTimestamp(user.freemium_trial_ends_at)
 return end!==null&&end>now
}
