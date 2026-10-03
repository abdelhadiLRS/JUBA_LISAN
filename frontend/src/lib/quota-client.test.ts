import {describe,it,expect} from 'vitest'
import {quotaAccountKey,parseQuotaResponse} from './quota-client'
const jwt=(sub:string,version:number)=>`header.${btoa(JSON.stringify({sub,version})).replace(/=/g,'')}.signature`
const valid=()=>({tier:'go',metered:true,features:{chat:{remaining:0,limit:40,resets_at:'2026-10-04T00:00:00Z',period:'day',unit:'requests'}}})
describe('Quota client identity and response contracts',()=>{
 it('keeps the account identity through token rotation',()=>{expect(quotaAccountKey(jwt('1',1),null)).toBe(quotaAccountKey(jwt('1',2),null))})
 it('uses token subject rather than a stale user object on account transition',()=>{expect(quotaAccountKey(jwt('2',1),{id:1})).toBe('account:2')})
 it('does not retain an account quota after logout',()=>{expect(quotaAccountKey(null,{id:1})).toBeNull()})
 it('rejects malformed quota counts and periods',()=>{
  expect(parseQuotaResponse(valid()).features.chat.remaining).toBe(0)
  for(const remaining of [NaN,-1,0.5,'40']){const data=valid();Object.assign(data.features.chat,{remaining});expect(()=>parseQuotaResponse(data)).toThrow()}
  const data=valid();data.features.chat.resets_at='invalid';expect(()=>parseQuotaResponse(data)).toThrow()
 })
})
