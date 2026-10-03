import {act,cleanup,renderHook,waitFor} from '@testing-library/react'
import {afterEach,beforeEach,describe,expect,it,vi} from 'vitest'
import {useReferenceFeatures} from './useReferenceFeatures'
const {apiFetch,events,markUpdated}=vi.hoisted(()=>({apiFetch:vi.fn(),events:{listener:null as null|(()=>void)},markUpdated:vi.fn()}))
vi.mock('@/lib/api',()=>({apiFetch}))
vi.mock('@/lib/learning-progress',()=>({markLearningProgressUpdated:markUpdated,subscribeToLearningProgressUpdated:(fn:()=>void)=>{events.listener=fn;return()=>{events.listener=null}}}))
const goal=(target=50)=>({daily_xp_target:target,weekly_xp_target:250,daily_xp:10,weekly_xp:10,daily_progress:.2,weekly_progress:.04,daily_completed:false,weekly_completed:false,daily_reward_xp:0,weekly_reward_xp:0,daily_reward_claimed:false,weekly_reward_claimed:false,day:'2026-10-03',week_start:'2026-09-28',week_end:'2026-10-04'})
const response=(value:unknown)=>({ok:true,status:200,json:async()=>value})
const game={total_xp:10,achievements:[],skills:{},games_played:0}
function deferred<T>(){let resolve!:(value:T)=>void;const promise=new Promise<T>(fn=>{resolve=fn});return {promise,resolve}}
beforeEach(()=>{apiFetch.mockReset();markUpdated.mockReset();events.listener=null})
afterEach(cleanup)
function read(url:string,target=50){return Promise.resolve(response(url.endsWith('/goals')?goal(target):url.includes('/history')?{entries:[]}:game))}
describe('Goal loading and write isolation',()=>{
 it('invalidates a pending old GET when PUT begins',async()=>{
  let reads=0
  const stale=deferred<ReturnType<typeof response>>()
  apiFetch.mockImplementation((url:string,options?:{method:string})=>{
   if(options?.method==='PUT')return Promise.resolve(response(goal(80)))
   if(url.endsWith('/goals')&&++reads===2)return stale.promise
   return read(url)
  })
  const {result}=renderHook(()=>useReferenceFeatures('en-US'))
  await waitFor(()=>expect(result.current.goal?.daily_xp_target).toBe(50))
  act(()=>{void result.current.load()})
  await act(async()=>{expect(await result.current.saveTargets(80,250)).toBe(true)})
  await act(async()=>{stale.resolve(response(goal(50)));await Promise.resolve()})
  expect(result.current.goal?.daily_xp_target).toBe(80)
  expect(markUpdated).toHaveBeenCalledTimes(1)
 })
 it('coalesces progress updates during a save and refreshes after release',async()=>{
  const write=deferred<ReturnType<typeof response>>();let target=50
  apiFetch.mockImplementation((url:string,options?:{method:string})=>options?.method==='PUT'?write.promise:read(url,target))
  const {result}=renderHook(()=>useReferenceFeatures('en-US'))
  await waitFor(()=>expect(result.current.loading).toBe(false))
  let saved!:Promise<boolean>
  act(()=>{saved=result.current.saveTargets(80,250)})
  act(()=>{events.listener?.();events.listener?.()})
  expect(apiFetch.mock.calls.filter(([,options])=>!options)).toHaveLength(3)
  target=80
  await act(async()=>{write.resolve(response(goal(80)));await saved})
  await waitFor(()=>expect(result.current.loading).toBe(false))
  expect(apiFetch.mock.calls.filter(([,options])=>!options)).toHaveLength(6)
  expect(result.current.goal?.daily_xp_target).toBe(80)
 })
 it('does not duplicate PUT calls',async()=>{
  const write=deferred<ReturnType<typeof response>>()
  apiFetch.mockImplementation((url:string,options?:{method:string})=>options?.method==='PUT'?write.promise:read(url))
  const {result}=renderHook(()=>useReferenceFeatures('en-US'))
  await waitFor(()=>expect(result.current.loading).toBe(false))
  let first!:Promise<boolean>,second!:Promise<boolean>
  act(()=>{first=result.current.saveTargets(80,250);second=result.current.saveTargets(90,250)})
  expect(await second).toBe(false)
  expect(apiFetch.mock.calls.filter(([,options])=>options?.method==='PUT')).toHaveLength(1)
  await act(async()=>{write.resolve(response(goal(80)));await first})
 })
 it('does not apply an old-language write to a new-language panel',async()=>{
  const write=deferred<ReturnType<typeof response>>();let target=50
  apiFetch.mockImplementation((url:string,options?:{method:string})=>options?.method==='PUT'?write.promise:read(url,target))
  const {result,rerender}=renderHook(({language})=>useReferenceFeatures(language),{initialProps:{language:'en-US'}})
  await waitFor(()=>expect(result.current.loading).toBe(false))
  let saved!:Promise<boolean>;act(()=>{saved=result.current.saveTargets(80,250)})
  target=30;rerender({language:'fr-FR'})
  await act(async()=>{write.resolve(response(goal(80)));expect(await saved).toBe(false)})
  await waitFor(()=>expect(result.current.goal?.daily_xp_target).toBe(30))
  expect(result.current.saved).toBe(false)
 })
 it('keeps the existing goal and reports a rejected save',async()=>{
  apiFetch.mockImplementation((url:string,options?:{method:string})=>options?.method==='PUT'?Promise.resolve({ok:false,status:500}):read(url))
  const {result}=renderHook(()=>useReferenceFeatures('en-US'))
  await waitFor(()=>expect(result.current.loading).toBe(false))
  await act(async()=>{expect(await result.current.saveTargets(80,250)).toBe(false)})
  expect(result.current.goal?.daily_xp_target).toBe(50)
  expect(result.current.saveError).toBe(true)
  expect(markUpdated).not.toHaveBeenCalled()
 })
 it('does not issue a save for invalid target values',async()=>{
  apiFetch.mockImplementation((url:string)=>read(url))
  const {result}=renderHook(()=>useReferenceFeatures('en-US'))
  await waitFor(()=>expect(result.current.loading).toBe(false))
  await act(async()=>{expect(await result.current.saveTargets(0,250)).toBe(false)})
  expect(apiFetch.mock.calls.filter(([,options])=>options?.method==='PUT')).toHaveLength(0)
 })
})
