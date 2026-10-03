import {describe,expect,it} from 'vitest'
import {leagueRisk,type LeagueRiskInput} from './league-risk'
const now=Date.parse('2026-10-01T00:00:00Z')
const season=(extra:Partial<LeagueRiskInput>={}):LeagueRiskInput=>({season_id:7,joined:true,finalized:false,tier:'silver',total:10,ends_at:'2026-10-05T00:00:00Z',current_user:{rank:7,xp:20},...extra})
describe('Automatic demotion risk alerts',()=>{
  it('warns near the boundary without claiming actual demotion',()=>{
    expect(leagueRisk(season(),now)?.level).toBe('near')
    expect(leagueRisk(season({current_user:{rank:8,xp:20}}),now)?.level).toBe('near')
  })
  it('marks ranks strictly below the safe cutoff as danger',()=>{
    expect(leagueRisk(season({current_user:{rank:9,xp:20}}),now)?.level).toBe('danger')
    expect(leagueRisk(season(),now)?.cutoff).toBe(8)
  })
  it('never warns for Bronze, small divisions or nonparticipants',()=>{
    expect(leagueRisk(season({tier:'bronze'}),now)).toBeNull()
    expect(leagueRisk(season({total:4,current_user:{rank:4,xp:0}}),now)).toBeNull()
    expect(leagueRisk(season({joined:false}),now)).toBeNull()
    expect(leagueRisk(season({current_user:null}),now)).toBeNull()
  })
  it('does not label a tied safe rank as demotion',()=>{
    expect(leagueRisk(season({current_user:{rank:8,xp:10}}),now)?.level).toBe('near')
  })
  it('clears alerts after expiry or finalization',()=>{
    expect(leagueRisk(season({finalized:true}),now)).toBeNull()
    expect(leagueRisk(season(),Date.parse('2026-10-05T00:00:00Z'))).toBeNull()
  })
  it('reopens dismissed warnings only for escalation, deadline urgency or a new season',()=>{
    const warning=leagueRisk(season(),now)!
    expect(leagueRisk(season({current_user:{rank:8,xp:5}}),now)?.signature).toBe(warning.signature)
    expect(leagueRisk(season({current_user:{rank:9,xp:5}}),now)?.signature).not.toBe(warning.signature)
    expect(leagueRisk(season(),Date.parse('2026-10-03T00:00:00Z'))?.signature).not.toBe(warning.signature)
    expect(leagueRisk(season({season_id:8}),now)?.signature).not.toBe(warning.signature)
  })
  it('does not warn for safe ranks or promotion positions',()=>{
    expect(leagueRisk(season({current_user:{rank:6,xp:20}}),now)).toBeNull()
    expect(leagueRisk(season({current_user:{rank:1,xp:100}}),now)).toBeNull()
  })
  it('rejects invalid dates, tiers and ranks',()=>{
    expect(leagueRisk(season({ends_at:'invalid'}),now)).toBeNull()
    expect(leagueRisk(season({tier:'unknown'}),now)).toBeNull()
    expect(leagueRisk(season({current_user:{rank:0,xp:20}}),now)).toBeNull()
    expect(leagueRisk(season({current_user:{rank:11,xp:20}}),now)).toBeNull()
  })
})
