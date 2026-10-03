import {act,cleanup,renderHook,waitFor} from '@testing-library/react'
import {afterEach,beforeEach,describe,expect,it,vi} from 'vitest'
import {useAuthStore} from '@/store/auth'
import {useAccountQuota} from './useAccountQuota'
const {apiFetch}=vi.hoisted(()=>({apiFetch:vi.fn()}))
vi.mock('@/lib/api',()=>({apiFetch}))
const jwt=(sub:string,version:number)=>`header.${btoa(JSON.stringify({sub,version})).replace(/=/g,'')}.signature`
const quota=(remaining:number)=>({tier:'go',metered:true,features:{chat:{remaining,limit:40,resets_at:'2026-10-04T00:00:00Z',period:'day',unit:'requests'}}})
function deferred(){let resolve!:(value:unknown)=>void;const promise=new Promise(resolveValue=>{resolve=resolveValue});return {promise,resolve}}
beforeEach(()=>{apiFetch.mockReset();useAuthStore.setState({accessToken:jwt('1',1),user:null})})
afterEach(()=>{cleanup();useAuthStore.setState({accessToken:null,user:null})})
describe('Account quota request lifecycle',()=>{
 it('accepts an account response after the access token was renewed',async()=>{
  const pending=deferred();apiFetch.mockReturnValue(pending.promise)
  const {result}=renderHook(()=>useAccountQuota('chat'))
  act(()=>useAuthStore.setState({accessToken:jwt('1',2)}))
  await act(async()=>pending.resolve({ok:true,json:async()=>quota(39)}))
  await waitFor(()=>expect(result.current.quota?.remaining).toBe(39))
  expect(apiFetch).toHaveBeenCalledTimes(1)
 })
 it('coalesces overlapping refresh calls',async()=>{
  apiFetch.mockResolvedValueOnce({ok:true,json:async()=>quota(40)})
  const {result}=renderHook(()=>useAccountQuota('chat'))
  await waitFor(()=>expect(result.current.quota?.remaining).toBe(40))
  const pending=deferred();apiFetch.mockReturnValueOnce(pending.promise)
  let first!:Promise<unknown>,second!:Promise<unknown>
  act(()=>{first=result.current.refresh();second=result.current.refresh()})
  expect(first).toBe(second);expect(apiFetch).toHaveBeenCalledTimes(2)
  await act(async()=>{pending.resolve({ok:true,json:async()=>quota(35)});await first})
  expect(result.current.quota?.remaining).toBe(35)
 })
 it('ignores a response from an account that logged out',async()=>{
  const pending=deferred();apiFetch.mockReturnValue(pending.promise)
  const {result}=renderHook(()=>useAccountQuota('chat'))
  act(()=>useAuthStore.setState({accessToken:null,user:null}))
  await act(async()=>pending.resolve({ok:true,json:async()=>quota(0)}))
  expect(result.current.state).toBeNull();expect(result.current.exhausted).toBe(false)
 })
})
