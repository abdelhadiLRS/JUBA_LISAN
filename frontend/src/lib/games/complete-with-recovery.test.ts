import {beforeEach, describe, expect, it, vi} from 'vitest'
import {completeWithRecovery} from './complete-with-recovery'

const {fetchApi}=vi.hoisted(()=>({fetchApi:vi.fn()}))
vi.mock('@/lib/api',()=>({apiFetch:fetchApi}))
const saved={xp_earned:90,total_xp:190,round_correct:3,round_questions:3,round_score:100,new_achievements:[],achievements:['first_game'],skills:{memory:.5},skill_results:{},games_played:1,questions_answered:3,correct_answers:3,best_round_score:100,daily_challenges_completed:0,last_daily_challenge_date:'',current_correct_streak:3,best_correct_streak:3}
const ok=()=>({ok:true,status:200,json:async()=>saved})
beforeEach(()=>{fetchApi.mockReset()})

describe('Committed game result recovery',()=>{
  it('returns an accepted completion without a second request',async()=>{
    fetchApi.mockResolvedValueOnce(ok())
    expect(await completeWithRecovery('s1',{session_id:'s1'})).toEqual(saved)
    expect(fetchApi).toHaveBeenCalledTimes(1)
  })
  it('recovers a lost network response through a read, never another award POST',async()=>{
    fetchApi.mockRejectedValueOnce(new TypeError('Failed to fetch')).mockResolvedValueOnce(ok())
    expect(await completeWithRecovery('s1',{session_id:'s1'})).toEqual(saved)
    expect(fetchApi.mock.calls.map(([url])=>url)).toEqual(['/api/progress/game-session/complete','/api/progress/game-session/s1/result'])
    expect(fetchApi.mock.calls.filter(([,options])=>options?.method==='POST')).toHaveLength(1)
  })
  it('confirms a previously completed session after a 409 conflict',async()=>{
    fetchApi.mockResolvedValueOnce({ok:false,status:409}).mockResolvedValueOnce(ok())
    expect(await completeWithRecovery('s1',{})).toEqual(saved)
    expect(fetchApi).toHaveBeenCalledTimes(2)
  })
  it('recovers an unreadable successful response',async()=>{
    fetchApi.mockResolvedValueOnce({ok:true,status:200,json:async()=>{throw new SyntaxError('truncated')}}).mockResolvedValueOnce(ok())
    expect(await completeWithRecovery('s1',{})).toEqual(saved)
  })
  it('does not mask a validation, authentication or expiration rejection',async()=>{
    for(const status of [401,403,404,410,422,429]){
      fetchApi.mockReset();fetchApi.mockResolvedValueOnce({ok:false,status})
      await expect(completeWithRecovery('s1',{})).rejects.toThrow(String(status))
      expect(fetchApi).toHaveBeenCalledTimes(1)
    }
  })
  it('does not claim success when the session is still unfinished',async()=>{
    fetchApi.mockResolvedValueOnce({ok:false,status:500}).mockResolvedValueOnce({ok:false,status:409})
    await expect(completeWithRecovery('s1',{})).rejects.toThrow('500')
    expect(fetchApi).toHaveBeenCalledTimes(2)
  })
  it('preserves the original failure if recovery also fails',async()=>{
    const original=new TypeError('Connection lost')
    fetchApi.mockRejectedValueOnce(original).mockRejectedValueOnce(new TypeError('still unavailable'))
    await expect(completeWithRecovery('s1',{})).rejects.toBe(original)
  })
  it('encodes the requested session ID',async()=>{
    fetchApi.mockResolvedValueOnce({ok:false,status:409}).mockResolvedValueOnce(ok())
    await completeWithRecovery('a/b',{})
    expect(fetchApi.mock.calls[1][0]).toBe('/api/progress/game-session/a%2Fb/result')
  })
})
