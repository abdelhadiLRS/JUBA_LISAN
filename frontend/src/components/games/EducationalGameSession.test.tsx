import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { ArenaGame } from './EducationalGameSession'
import type { ArenaState } from '@/lib/games/persist'

const mocks=vi.hoisted(()=>({start:vi.fn(),move:vi.fn(),read:vi.fn(),progress:vi.fn(),mark:vi.fn()}))
vi.mock('@/lib/games/persist',()=>({startArena:mocks.start,moveArena:mocks.move,readArena:mocks.read,startGameSession:vi.fn(),answerGameSessionQuestion:vi.fn(),completeGameSession:vi.fn()}))
vi.mock('@/store/auth',()=>({useAuthStore:(select:(state:{user:{id:number}})=>unknown)=>select({user:{id:1}})}))
vi.mock('@/store/progress',()=>({useProgressStore:{getState:()=>({streak:1,setProgress:mocks.progress})}}))
vi.mock('@/lib/learning-progress',()=>({markLearningProgressUpdated:mocks.mark}))
const props={gameId:'memory' as const,language:'en' as const,targetLanguage:'en-GB',difficulty:1,arabic:false,title:'Word memory',onExit:vi.fn(),onReplay:vi.fn()}
const board:ArenaState={session_id:'round-1',game:'memory',version:0,phase:'playing',index:0,total:3,lives:3,correct:0,attempts:0,max_moves:22,deadline:null,relaxed:false,feedback:null,cards:[{id:'a',label:null,side:'word',opened:false,matched:false},{id:'b',label:null,side:'meaning',opened:false,matched:false}]}
beforeEach(()=>{sessionStorage.clear();vi.clearAllMocks();mocks.start.mockResolvedValue(board);vi.stubGlobal('crypto',{randomUUID:vi.fn(()=> 'move-id')})})
afterEach(()=>{cleanup();vi.unstubAllGlobals()})

describe('Language arcade',()=>{
  it('starts a real board without putting hidden answers into the DOM',async()=>{
    render(<ArenaGame {...props}/>)
    fireEvent.click(screen.getByRole('button',{name:'Start playing'}))
    await screen.findByRole('button',{name:'Hidden card 1'})
    expect(mocks.start).toHaveBeenCalledWith('memory','en-GB',1,false)
    expect(screen.queryByText('book')).toBeNull()
    expect(screen.queryByText('pair_key')).toBeNull()
  })
  it('asks the server to flip and only displays the returned label',async()=>{
    mocks.move.mockResolvedValue({...board,version:1,cards:[{...board.cards![0],opened:true,label:'book'},board.cards![1]]})
    render(<ArenaGame {...props}/>)
    fireEvent.click(screen.getByRole('button',{name:'Start playing'}))
    fireEvent.click(await screen.findByRole('button',{name:'Hidden card 1'}))
    await screen.findByRole('button',{name:'book'})
    expect(mocks.move).toHaveBeenCalledWith('round-1',{action_id:'move-id',version:0,kind:'flip',value:'a',order:[]})
  })
  it('uses distinct letter IDs, including repeated letters',async()=>{
    mocks.start.mockResolvedValue({...board,game:'word_scramble',cards:undefined,question:{prompt:'a greeting',tiles:[{id:'x',label:'l'},{id:'y',label:'l'}]}})
    mocks.move.mockResolvedValue({...board,game:'word_scramble',phase:'feedback',version:1,feedback:{correct:true,answer:'ll',meaning:'a greeting'}})
    render(<ArenaGame {...props} gameId="word_scramble"/>)
    fireEvent.click(screen.getByRole('button',{name:'Start playing'}))
    const buttons=await screen.findAllByRole('button',{name:'l',exact:true})
    fireEvent.click(buttons[0]);fireEvent.click(buttons[1])
    fireEvent.click(screen.getByRole('button',{name:'Check word'}))
    await waitFor(()=>expect(mocks.move).toHaveBeenCalledWith('round-1',expect.objectContaining({kind:'answer',order:['x','y']})))
  })
  it('offers untimed practice and still targets without changing earned XP',async()=>{
    mocks.start.mockResolvedValue({...board,game:'quick_choice',cards:undefined,relaxed:true,question:{prompt:'book',choices:['a written work','a drink','a person','a place']}})
    const {container}=render(<ArenaGame {...props} gameId="quick_choice"/>)
    fireEvent.click(screen.getByLabelText('Untimed practice, same XP'))
    fireEvent.click(screen.getByRole('button',{name:'Start playing'}))
    await screen.findByText('book')
    expect(mocks.start).toHaveBeenCalledWith('quick_choice','en-GB',1,true)
    fireEvent.click(screen.getByLabelText('Keep targets still'))
    expect(container.querySelector('.arcade-hunt')?.getAttribute('data-still')).toBe('true')
  })
  it('recovers a committed move after its response is lost without resubmitting',async()=>{
    mocks.move.mockRejectedValue(new Error('network'))
    mocks.read.mockResolvedValue({...board,version:1,cards:[{...board.cards![0],opened:true,label:'book'},board.cards![1]]})
    render(<ArenaGame {...props}/>)
    fireEvent.click(screen.getByRole('button',{name:'Start playing'}))
    fireEvent.click(await screen.findByRole('button',{name:'Hidden card 1'}))
    await screen.findByRole('button',{name:'book'})
    expect(mocks.move).toHaveBeenCalledTimes(1)
    expect(mocks.read).toHaveBeenCalledWith('round-1')
  })
  it('keeps the same action ID when retrying an uncommitted move',async()=>{
    mocks.move.mockRejectedValueOnce(new Error('network')).mockResolvedValue({...board,version:1,cards:[{...board.cards![0],opened:true,label:'book'},board.cards![1]]})
    mocks.read.mockResolvedValue(board)
    render(<ArenaGame {...props}/>)
    fireEvent.click(screen.getByRole('button',{name:'Start playing'}))
    fireEvent.click(await screen.findByRole('button',{name:'Hidden card 1'}))
    fireEvent.click(await screen.findByRole('button',{name:'Retry move'}))
    await screen.findByRole('button',{name:'book'})
    expect(mocks.move.mock.calls[1][1]).toEqual(mocks.move.mock.calls[0][1])
  })
})
