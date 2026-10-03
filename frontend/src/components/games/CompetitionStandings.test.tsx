import {afterEach, beforeEach, describe, expect, it, vi} from 'vitest'
import {cleanup, fireEvent, render, screen, waitFor} from '@testing-library/react'
import CompetitionStandings from './CompetitionStandings'

const {fetchApi, state, events}=vi.hoisted(()=>({fetchApi:vi.fn(),state:{activeLanguage:{code:'en-US'},isSwitching:false},events:{listener:null as null|(()=>void)}}))
vi.mock('@/lib/api',()=>({apiFetch:fetchApi}))
vi.mock('next-intl',()=>({useLocale:()=> 'en'}))
vi.mock('@/store/language',()=>({useLanguageStore:(selector:(value:typeof state)=>unknown)=>selector(state)}))
vi.mock('@/lib/learning-progress',()=>({subscribeToLearningProgressUpdated:(listener:()=>void)=>{events.listener=listener;return()=>{events.listener=null}}}))
const entry={user_id:1,username:'learner',display_name:'Learner',rank:1,xp:0,is_current_user:true}
function board(xp=0){return {target_language:'en-US',period:'week',total:1,offset:0,limit:10,entries:[{...entry,xp}],current_user:{...entry,xp}}}
function league(joined=true,xp=0){return {season_id:joined?1:null,target_language:'en-US',week_start:'2026-09-28',week_end:'2026-10-04',ends_at:'2026-10-05T00:00:00Z',joined,tier:'bronze',finalized:false,next_tier:null,total:joined?1:0,entries:joined?[{...entry,xp}]:[],current_user:joined?{...entry,xp}:null}}
const response=(data:unknown)=>({ok:true,json:async()=>data})
beforeEach(()=>{fetchApi.mockReset();events.listener=null;state.activeLanguage={code:'en-US'};state.isSwitching=false})
afterEach(cleanup)

describe('Game results competition connection',()=>{
  it('refreshes both rankings after a saved learning-progress event without writing XP',async()=>{
    let xp=0
    fetchApi.mockImplementation((url:string)=>Promise.resolve(response(url.startsWith('/api/leaderboard')?board(xp):league(true,xp))))
    render(<CompetitionStandings/> )
    await screen.findByText('Standings synced with saved XP.')
    expect(fetchApi.mock.calls).toHaveLength(2)
    xp=90;events.listener?.()
    await waitFor(()=>expect(screen.getAllByText('90 XP')).toHaveLength(2))
    expect(fetchApi.mock.calls).toHaveLength(4)
    expect(fetchApi.mock.calls.every(([,options])=>options===undefined)).toBe(true)
  })
  it('does not enroll on reads and offers explicit enrollment with saved pre-join XP',async()=>{
    let joined=false
    fetchApi.mockImplementation((url:string,options?:{method:string})=>{
      if(options?.method==='POST'){joined=true;return Promise.resolve(response(league(true,90)))}
      return Promise.resolve(response(url.startsWith('/api/leaderboard')?joined?board(90):{...board(),entries:[],current_user:null,total:0}:league(joined,90)))
    })
    render(<CompetitionStandings/> )
    const button=await screen.findByRole('button',{name:'Join league'})
    expect(fetchApi.mock.calls.every(([,options])=>options===undefined)).toBe(true)
    fireEvent.click(button)
    await screen.findByText('bronze')
    const writes=fetchApi.mock.calls.filter(([,options])=>options?.method==='POST')
    expect(writes).toHaveLength(1)
    expect(writes[0][0]).toBe('/api/leagues/join')
    expect(JSON.parse(writes[0][1].body)).toEqual({target_language:'en-US'})
    expect(screen.getAllByText('90 XP')).toHaveLength(2)
  })
  it('shows ranking errors without replacing the saved game result',async()=>{
    fetchApi.mockResolvedValue({ok:false})
    render(<CompetitionStandings/> )
    await screen.findByText('Could not load rankings. Your saved game result is unchanged.')
    expect(screen.queryByText('Standings synced with saved XP.')).toBeNull()
    expect(screen.getAllByRole('button',{name:'Retry'})).toHaveLength(2)
  })
  it('ignores an older refresh after a newer saved result arrives',async()=>{
    let resolves:Array<(value:unknown)=>void>=[]
    fetchApi.mockImplementation(()=>new Promise(resolve=>{resolves.push(resolve)}))
    render(<CompetitionStandings/> )
    await waitFor(()=>expect(resolves).toHaveLength(2))
    events.listener?.()
    await waitFor(()=>expect(resolves).toHaveLength(4))
    resolves[2](response(board(90)));resolves[3](response(league(true,90)))
    await waitFor(()=>expect(screen.getAllByText('90 XP')).toHaveLength(2))
    resolves[0](response(board(0)));resolves[1](response(league(true,0)))
    await Promise.resolve();await Promise.resolve()
    expect(screen.getAllByText('90 XP')).toHaveLength(2)
  })
  it('requests the chosen leaderboard period',async()=>{
    fetchApi.mockImplementation((url:string)=>Promise.resolve(response(url.startsWith('/api/leaderboard')?board():league())))
    render(<CompetitionStandings/> )
    await screen.findByText('Standings synced with saved XP.')
    fireEvent.change(screen.getByRole('combobox'),{target:{value:'all'}})
    await waitFor(()=>expect(fetchApi.mock.calls.some(([url])=>url.includes('period=all'))).toBe(true))
  })
})
