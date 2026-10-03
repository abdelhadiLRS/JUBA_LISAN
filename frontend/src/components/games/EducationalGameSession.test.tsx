import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { ArenaGame } from './EducationalGameSession'
import type { ArenaState } from '@/lib/games/persist'

// Keep persist.ts real: HTTP status parsing, request bodies and cancellation
// are exercised alongside the React component. Only the transport is replaced.
const mocks=vi.hoisted(()=>({api:vi.fn(),progress:vi.fn(),mark:vi.fn()}))
vi.mock('@/lib/api',()=>({apiFetch:mocks.api}))
vi.mock('@/store/auth',()=>({useAuthStore:(select:(state:{user:{id:number}})=>unknown)=>select({user:{id:1}})}))
vi.mock('@/store/progress',()=>({useProgressStore:{getState:()=>({streak:1,setProgress:mocks.progress})}}))
vi.mock('@/lib/learning-progress',()=>({markLearningProgressUpdated:mocks.mark}))
const props={gameId:'memory' as const,language:'en' as const,targetLanguage:'en-GB',difficulty:1,arabic:false,title:'Word memory',onExit:vi.fn(),onReplay:vi.fn()}
const board:ArenaState={session_id:'round-1',game:'memory',version:0,phase:'playing',index:0,total:3,lives:3,correct:0,attempts:0,max_moves:22,deadline:null,relaxed:false,feedback:null,cards:[{id:'a',label:null,side:'word',opened:false,matched:false},{id:'b',label:null,side:'meaning',opened:false,matched:false}]}
const reply=(value:unknown,status=200)=>new Response(JSON.stringify(value),{status,headers:{'Content-Type':'application/json'}})
const flipped={...board,version:1,cards:[{...board.cards![0],opened:true,label:'book'},board.cards![1]]}
beforeEach(()=>{sessionStorage.clear();vi.clearAllMocks();mocks.api.mockImplementation(()=>Promise.resolve(reply(board)));vi.stubGlobal('crypto',{randomUUID:vi.fn(()=> 'move-id')})})
afterEach(()=>{cleanup();vi.unstubAllGlobals()})
async function play(){fireEvent.click(screen.getByRole('button',{name:'Start playing'}));await screen.findByRole('button',{name:'Hidden card 1'})}

describe('Arcade component plus real HTTP contracts',()=>{
  it('starts a real board without exposing hidden answers',async()=>{
    render(<ArenaGame {...props}/>);await play()
    const [,options]=mocks.api.mock.calls[0]
    expect(JSON.parse(options.body)).toEqual({game_id:'memory',target_language:'en-GB',difficulty:1,relaxed:false})
    expect(options.signal).toBeInstanceOf(AbortSignal)
    expect(screen.queryByText('book')).toBeNull()
    expect((screen.getByRole('button',{name:'End and save learning'}) as HTMLButtonElement).disabled).toBe(true)
  })
  it('flips only after server validation',async()=>{
    mocks.api.mockImplementation((url:string)=>Promise.resolve(reply(url.endsWith('/move')?flipped:board)))
    render(<ArenaGame {...props}/>);await play()
    fireEvent.click(screen.getByRole('button',{name:'Hidden card 1'}))
    await screen.findByRole('button',{name:'book'})
    expect(JSON.parse(mocks.api.mock.calls[1][1].body)).toEqual({action_id:'move-id',version:0,kind:'flip',value:'a',order:[]})
  })
  it('clears a permanent 409 and allows another valid move',async()=>{
    let moves=0
    mocks.api.mockImplementation((url:string)=>Promise.resolve(url.endsWith('/move')?(++moves===1?reply({detail:'Invalid card'},409):reply(flipped)):reply(board)))
    render(<ArenaGame {...props}/>);await play()
    fireEvent.click(screen.getByRole('button',{name:'Hidden card 1'}))
    await screen.findByText('Move rejected. You can continue playing.')
    expect(screen.queryByRole('button',{name:'Retry move'})).toBeNull()
    expect((screen.getByRole('button',{name:'Hidden card 1'}) as HTMLButtonElement).disabled).toBe(false)
    fireEvent.click(screen.getByRole('button',{name:'Hidden card 1'}))
    await screen.findByRole('button',{name:'book'})
  })
  it('removes expired saved rounds and can start afresh',async()=>{
    sessionStorage.setItem('juba:arcade:1:en-GB:memory:1','expired')
    mocks.api.mockImplementation((url:string)=>Promise.resolve(url.endsWith('/expired')?reply({detail:'Round expired'},410):reply(board)))
    render(<ArenaGame {...props}/>)
    await screen.findByText('Round expired or learning plan changed. Start a new round.')
    expect(sessionStorage.getItem('juba:arcade:1:en-GB:memory:1')).toBeNull()
    await waitFor(()=>expect((screen.getByRole('button',{name:'Start playing'}) as HTMLButtonElement).disabled).toBe(false))
    await play()
  })
  it('clears a terminal plan-change rejection rather than replaying it',async()=>{
    mocks.api.mockImplementation((url:string)=>Promise.resolve(url.endsWith('/move')?reply({detail:'Learning plan changed; start a new round'},409):reply(board)))
    render(<ArenaGame {...props}/>);await play()
    fireEvent.click(screen.getByRole('button',{name:'Hidden card 1'}))
    await screen.findByRole('button',{name:'Start playing'})
    expect(screen.queryByRole('button',{name:'Retry move'})).toBeNull()
  })
  it('recovers a committed move after its response is lost',async()=>{
    mocks.api.mockImplementation((url:string,options?:RequestInit)=>url.endsWith('/move')?Promise.reject(new Error('network')):Promise.resolve(reply(options?.method==='POST'?board:flipped)))
    render(<ArenaGame {...props}/>);await play()
    fireEvent.click(screen.getByRole('button',{name:'Hidden card 1'}))
    await screen.findByRole('button',{name:'book'})
    expect(mocks.api.mock.calls.filter(([url])=>url.endsWith('/move'))).toHaveLength(1)
  })
  it('preserves the action ID only for an uncertain transient failure',async()=>{
    let moves=0
    mocks.api.mockImplementation((url:string)=>Promise.resolve(url.endsWith('/move')?(++moves===1?reply({detail:'Temporary failure'},503):reply(flipped)):reply(board)))
    render(<ArenaGame {...props}/>);await play()
    fireEvent.click(screen.getByRole('button',{name:'Hidden card 1'}))
    fireEvent.click(await screen.findByRole('button',{name:'Retry move'}))
    await screen.findByRole('button',{name:'book'})
    const calls=mocks.api.mock.calls.filter(([url])=>url.endsWith('/move'))
    expect(calls[0][1].body).toEqual(calls[1][1].body)
  })
  it('aborts a pending start when the screen unmounts',async()=>{
    mocks.api.mockImplementation((_url:string,options:RequestInit)=>new Promise((_resolve,reject)=>options.signal?.addEventListener('abort',()=>reject(new DOMException('aborted','AbortError')))))
    const {unmount}=render(<ArenaGame {...props}/>)
    fireEvent.click(screen.getByRole('button',{name:'Start playing'}))
    const signal=mocks.api.mock.calls[0][1].signal as AbortSignal
    unmount();expect(signal.aborted).toBe(true)
    await Promise.resolve()
    expect(mocks.progress).not.toHaveBeenCalled()
  })
  it('sends distinct repeated-letter IDs in the selected order',async()=>{
    const letters={...board,game:'word_scramble',cards:undefined,question:{prompt:'a greeting',tiles:[{id:'x',label:'l'},{id:'y',label:'l'}]}}
    mocks.api.mockImplementation((url:string)=>Promise.resolve(reply(url.endsWith('/move')?{...letters,phase:'feedback',version:1,feedback:{correct:true,answer:'ll',meaning:'a greeting'}}:letters)))
    render(<ArenaGame {...props} gameId="word_scramble"/>)
    fireEvent.click(screen.getByRole('button',{name:'Start playing'}))
    const buttons=await screen.findAllByRole('button',{name:'l',exact:true});fireEvent.click(buttons[0]);fireEvent.click(buttons[1]);fireEvent.click(screen.getByRole('button',{name:'Check word'}))
    await waitFor(()=>expect(mocks.api.mock.calls.some(([,options])=>options?.body&&JSON.parse(options.body).order?.join(',')==='x,y')).toBe(true))
  })
  it('offers untimed practice and stationary targets',async()=>{
    mocks.api.mockResolvedValue(reply({...board,game:'quick_choice',cards:undefined,relaxed:true,question:{prompt:'book',choices:['a written work','a drink','a person','a place']}}))
    const {container}=render(<ArenaGame {...props} gameId="quick_choice"/>)
    fireEvent.click(screen.getByLabelText('Untimed practice, same XP'));fireEvent.click(screen.getByRole('button',{name:'Start playing'}));await screen.findByText('book')
    expect(JSON.parse(mocks.api.mock.calls[0][1].body).relaxed).toBe(true)
    fireEvent.click(screen.getByLabelText('Keep targets still'))
    expect(container.querySelector('.arcade-hunt')?.getAttribute('data-still')).toBe('true')
  })
})
