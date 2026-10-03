import {describe,expect,it} from 'vitest'
import {pricingAction} from './landing-pricing-policy'
const base={paid:true,hasSession:true,allowRegistration:true,stripeEnabled:true,subscribed:false as boolean|null,price:10,configReady:true}
describe('Landing pricing policy',()=>{
 it('requires verified config before exposing actions',()=>expect(pricingAction({...base,configReady:false})).toBe('wait'))
 it('does not start payments when Stripe is disabled',()=>expect(pricingAction({...base,stripeEnabled:false})).toBe('dashboard'))
 it('does not start payments for unavailable prices',()=>{for(const price of [0,-1,NaN,Infinity])expect(pricingAction({...base,price})).toBe('dashboard')})
 it('waits for subscription status',()=>expect(pricingAction({...base,subscribed:null})).toBe('wait'))
 it('sends subscribed learners to dashboard rather than duplicate checkout',()=>expect(pricingAction({...base,subscribed:true})).toBe('dashboard'))
 it('allows checkout only for eligible signed-in learners',()=>expect(pricingAction(base)).toBe('checkout'))
 it('sends visitors to login when public registration is closed',()=>expect(pricingAction({...base,hasSession:false,allowRegistration:false})).toBe('login'))
 it('preserves registration when the server allows it',()=>expect(pricingAction({...base,hasSession:false})).toBe('register'))
 it('never checks out a free plan',()=>expect(pricingAction({...base,paid:false})).toBe('dashboard'))
})
