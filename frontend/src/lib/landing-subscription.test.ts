import {beforeEach,describe,expect,it,vi} from 'vitest'
const {apiFetch,auth}=vi.hoisted(()=>({apiFetch:vi.fn(),auth:{accessToken:'token-a' as string|null}}))
vi.mock('@/lib/api',()=>({apiFetch}))
vi.mock('@/store/auth',()=>({useAuthStore:{getState:()=>auth}}))
import {getLandingSubscriptionState} from './landing-subscription'
beforeEach(()=>{apiFetch.mockReset();auth.accessToken='token-a'})
describe('Verified subscription state',()=>{
 it('rejects failed reads instead of allowing duplicate checkout',async()=>{
  apiFetch.mockResolvedValue({ok:false});await expect(getLandingSubscriptionState()).rejects.toThrow('verified')
 })
 it('retries a failure rather than caching it forever',async()=>{
  apiFetch.mockRejectedValueOnce(new TypeError('network')).mockResolvedValueOnce({ok:true,json:async()=>({subscription_status:'active',trial_used:true})})
  await expect(getLandingSubscriptionState()).rejects.toThrow('network')
  expect(await getLandingSubscriptionState()).toEqual({subscribed:true,trialUsed:true})
  expect(apiFetch).toHaveBeenCalledTimes(2)
 })
 it('does not reuse a resolved subscription snapshot',async()=>{
  apiFetch.mockResolvedValueOnce({ok:true,json:async()=>({subscription_status:'none'})}).mockResolvedValueOnce({ok:true,json:async()=>({subscription_status:'active'})})
  expect((await getLandingSubscriptionState()).subscribed).toBe(false)
  expect((await getLandingSubscriptionState()).subscribed).toBe(true)
 })
 it('coalesces concurrent reads for the same account token',async()=>{
  let resolve!:(value:unknown)=>void
  apiFetch.mockReturnValue(new Promise(value=>{resolve=value}))
  const a=getLandingSubscriptionState(),b=getLandingSubscriptionState()
  expect(apiFetch).toHaveBeenCalledTimes(1)
  resolve({ok:true,json:async()=>({subscription_status:'trialing'})})
  expect(await a).toEqual(await b)
 })
})
