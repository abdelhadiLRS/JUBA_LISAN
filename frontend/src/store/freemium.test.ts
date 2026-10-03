import {beforeEach,describe,expect,it,vi} from 'vitest'
import {useAuthStore} from './auth'
import {useFreemiumStore} from './freemium'
const {apiFetch}=vi.hoisted(()=>({apiFetch:vi.fn()}))
vi.mock('@/lib/api',()=>({apiFetch}))
const token=(sub:string,version=1)=>`header.${btoa(JSON.stringify({sub,version})).replace(/=/g,'')}.signature`
const status=(remaining:number)=>({trial_active:false,trial_ends_at:null,chat_remaining:remaining,chat_limit:5,lessons_remaining:1,lessons_limit:1,listening_remaining:2,listening_limit:2,reading_remaining:2,reading_limit:2,voice_remaining_seconds:300,voice_limit_seconds:300})
const response=(remaining:number)=>({ok:true,json:async()=>status(remaining)})
function deferred(){let resolve!:(value:unknown)=>void;const promise=new Promise(value=>{resolve=value});return {promise,resolve}}
beforeEach(()=>{apiFetch.mockReset();useAuthStore.setState({accessToken:null,user:null});useFreemiumStore.setState({status:null,loaded:false,lastFetch:0});useAuthStore.setState({accessToken:token('1')})})
describe('Legacy quota store account isolation',()=>{
 it('clears cached values on logout',async()=>{
  apiFetch.mockResolvedValue(response(4));await useFreemiumStore.getState().fetchStatus()
  expect(useFreemiumStore.getState().status?.chat_remaining).toBe(4)
  useAuthStore.setState({accessToken:null,user:null})
  expect(useFreemiumStore.getState().status).toBeNull();expect(useFreemiumStore.getState().loaded).toBe(false)
 })
 it('does not accept old-account responses after switching accounts',async()=>{
  const old=deferred();apiFetch.mockReturnValueOnce(old.promise)
  const first=useFreemiumStore.getState().fetchStatus()
  useAuthStore.setState({accessToken:token('2')})
  apiFetch.mockResolvedValueOnce(response(5));await useFreemiumStore.getState().fetchStatus()
  old.resolve(response(0));await first
  expect(useFreemiumStore.getState().status?.chat_remaining).toBe(5)
 })
 it('keeps cache for a same-account token renewal',async()=>{
  apiFetch.mockResolvedValue(response(4));await useFreemiumStore.getState().fetchStatus()
  useAuthStore.setState({accessToken:token('1',2)})
  await useFreemiumStore.getState().fetchStatus()
  expect(apiFetch).toHaveBeenCalledTimes(1);expect(useFreemiumStore.getState().status?.chat_remaining).toBe(4)
 })
 it('coalesces refreshes and never guesses a review charge',async()=>{
  apiFetch.mockResolvedValueOnce(response(2));await useFreemiumStore.getState().fetchStatus()
  const next=deferred();apiFetch.mockReturnValueOnce(next.promise)
  useFreemiumStore.getState().decrement('reading_remaining')
  const waiting=useFreemiumStore.getState().fetchStatus(true)
  expect(useFreemiumStore.getState().status?.reading_remaining).toBe(2)
  expect(apiFetch).toHaveBeenCalledTimes(2)
  next.resolve(response(2));await waiting
  expect(useFreemiumStore.getState().status?.reading_remaining).toBe(2)
 })
 it('invalidates unavailable readings rather than displaying stale quota',async()=>{
  apiFetch.mockResolvedValueOnce(response(3));await useFreemiumStore.getState().fetchStatus()
  apiFetch.mockResolvedValueOnce({ok:false});await useFreemiumStore.getState().fetchStatus(true)
  expect(useFreemiumStore.getState().status).toBeNull();expect(useFreemiumStore.getState().loaded).toBe(false)
 })
})
