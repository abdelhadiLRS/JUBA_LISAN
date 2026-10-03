import {describe,expect,it} from 'vitest'
import {chartPoints,chronologicalHistory,seasonValue,type HistoricalSeason} from './league-history'
const season=(id:number,week:string,extras:Partial<HistoricalSeason>={}):HistoricalSeason=>({season_id:id,target_language:'en-US',week_start:week,week_end:week,tier:'silver',next_tier:'gold',finalized:true,joined:true,total:10,current_user:{user_id:1,display_name:'Learner',rank:2,xp:100,is_current_user:true},entries:[],...extras})
describe('Historical league chart data integrity',()=>{
  it('sorts participation by actual week and deduplicates season IDs',()=>{
    const a=season(1,'2026-09-07'),b=season(2,'2026-09-21')
    expect(chronologicalHistory([b,a,b],true).map(s=>s.season_id)).toEqual([1,2])
  })
  it('separates pending seasons instead of calling them settled',()=>{
    const pending=season(2,'2026-09-21',{finalized:false,next_tier:null})
    expect(chronologicalHistory([season(1,'2026-09-07'),pending],true)).toHaveLength(1)
    expect(chronologicalHistory([pending],false)).toHaveLength(1)
  })
  it('preserves zero earned XP but never replaces a missing personal rank with zero',()=>{
    expect(seasonValue(season(1,'2026-09-07',{current_user:null}),'xp')).toBeNull()
    expect(seasonValue(season(1,'2026-09-07',{current_user:null}),'rank')).toBeNull()
    const zero=season(1,'2026-09-07');zero.current_user!.xp=0
    expect(seasonValue(zero,'xp')).toBe(0)
  })
  it('plots the participated tier rather than the promoted next tier',()=>{
    expect(seasonValue(season(1,'2026-09-07'),'tier')).toBe(2)
    expect(seasonValue(season(1,'2026-09-07',{tier:'unknown'}),'tier')).toBeNull()
  })
  it('positions missing participation weeks as time gaps, not zero-value points',()=>{
    const points=chartPoints([season(1,'2026-09-07'),season(2,'2026-09-14'),season(3,'2026-09-28')],'xp')
    expect(points).toHaveLength(3)
    expect(points[2].x-points[1].x).toBeCloseTo(2*(points[1].x-points[0].x))
  })
  it('places better ranks higher in the chart',()=>{
    const first=season(1,'2026-09-07'),second=season(2,'2026-09-14');second.current_user!.rank=1
    const points=chartPoints([first,second],'rank')
    expect(points[1].y).toBeLessThan(points[0].y)
  })
  it('keeps a single season and an all-zero XP series finite',()=>{
    const zero=season(1,'2026-09-07');zero.current_user!.xp=0
    const [point]=chartPoints([zero],'xp')
    expect(point.x).toBe(400);expect(point.y).toBe(224)
    expect(Number.isFinite(point.x)&&Number.isFinite(point.y)).toBe(true)
  })
  it('omits unavailable values and invalid dates',()=>{
    expect(chartPoints([season(1,'2026-09-07',{current_user:null})],'rank')).toEqual([])
    expect(chronologicalHistory([season(1,'invalid')],false)).toEqual([])
  })
})
