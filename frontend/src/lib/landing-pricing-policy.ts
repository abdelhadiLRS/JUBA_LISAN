export type PricingAction='checkout'|'dashboard'|'register'|'login'|'wait'
export function pricingAction(input:{paid:boolean;hasSession:boolean;allowRegistration:boolean;stripeEnabled:boolean;subscribed:boolean|null;price:number;configReady:boolean}):PricingAction{
  if(!input.configReady)return 'wait'
  if(input.paid&&(!input.stripeEnabled||!Number.isFinite(input.price)||input.price<=0))return input.hasSession?'dashboard':input.allowRegistration?'register':'login'
  if(!input.hasSession)return input.allowRegistration?'register':'login'
  if(!input.paid)return 'dashboard'
  if(input.subscribed===null)return 'wait'
  return input.subscribed?'dashboard':'checkout'
}
