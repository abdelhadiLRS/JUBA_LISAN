import {describe,it,expect} from 'vitest'
import {freeTrialActive,subscriptionTimestamp} from './subscription-time'
describe('Subscription UTC timestamp contract',()=>{
 it('interprets naive backend timestamps as UTC',()=>{expect(subscriptionTimestamp('2026-10-03T12:00:00')).toBe(Date.parse('2026-10-03T12:00:00Z'))})
 it('retains explicit positive and negative offsets',()=>{
  expect(subscriptionTimestamp('2026-10-03T14:00:00+02:00')).toBe(Date.parse('2026-10-03T12:00:00Z'))
  expect(subscriptionTimestamp('2026-10-03T08:00:00-04:00')).toBe(Date.parse('2026-10-03T12:00:00Z'))
 })
 it('is inactive exactly at expiry and active immediately before',()=>{
  const user={subscription_status:'none',freemium_trial_ends_at:'2026-10-03T12:00:00'},now=Date.parse('2026-10-03T12:00:00Z')
  expect(freeTrialActive(user,true,true,now)).toBe(false)
  expect(freeTrialActive(user,true,true,now-1)).toBe(true)
 })
 it('does not interpret a paid subscription as a free trial',()=>{for(const subscription_status of ['active','trialing'])expect(freeTrialActive({subscription_status,freemium_trial_ends_at:'2026-10-04T12:00:00'},true,true,Date.parse('2026-10-03T12:00:00Z'))).toBe(false)})
 it('rejects invalid timestamps and honors deployment feature flags',()=>{
  for(const timestamp of [null,'','not a date','10/03/2026'])expect(subscriptionTimestamp(timestamp)).toBeNull()
  const user={freemium_trial_ends_at:'2026-10-04T12:00:00'}
  expect(freeTrialActive(user,false,true,0)).toBe(false)
  expect(freeTrialActive(user,true,false,0)).toBe(false)
 })
})
