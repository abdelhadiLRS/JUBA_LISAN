import {LEAGUE_TIERS} from './league-movement'
export type HistoryEntry={user_id:number;display_name:string;rank:number;xp:number;is_current_user:boolean}
export type HistoricalSeason={season_id:number|null;target_language:string;week_start:string;week_end:string;tier:string;next_tier:string|null;finalized:boolean;joined:boolean;total:number;current_user:HistoryEntry|null;entries:HistoryEntry[]}
export type HistoryMetric='xp'|'rank'|'tier'
export function seasonValue(season:HistoricalSeason,metric:HistoryMetric):number|null{
  if(metric==='tier'){
    // Plot the participated tier, not a promotion forecast or next week's tier.
    const index=LEAGUE_TIERS.indexOf(season.tier as typeof LEAGUE_TIERS[number])
    return index>=0?index+1:null
  }
  const entry=season.current_user
  if(!entry)return null
  const value=metric==='xp'?entry.xp:entry.rank
  return Number.isFinite(value)&&value>=(metric==='rank'?1:0)?value:null
}
export function chronologicalHistory(seasons:HistoricalSeason[],settledOnly:boolean):HistoricalSeason[]{
  const unique=new Map<number,HistoricalSeason>()
  for(const season of seasons){
    if(season.season_id===null||!Number.isFinite(Date.parse(season.week_start+'T00:00:00Z')))continue
    if(settledOnly&&!season.finalized)continue
    unique.set(season.season_id,season)
  }
  return [...unique.values()].sort((a,b)=>a.week_start.localeCompare(b.week_start))
}
export function chartPoints(seasons:HistoricalSeason[],metric:HistoryMetric){
  const valid=seasons.map(season=>({season,value:seasonValue(season,metric)})).filter((point):point is {season:HistoricalSeason;value:number}=>point.value!==null)
  if(!valid.length)return []
  const times=valid.map(point=>Date.parse(point.season.week_start+'T00:00:00Z'))
  const values=valid.map(point=>point.value)
  const minTime=Math.min(...times),maxTime=Math.max(...times)
  const minValue=metric==='xp'?0:Math.min(...values)
  const maxValue=metric==='tier'?6:Math.max(...values,minValue+1)
  return valid.map((point,index)=>{
    const fraction=(point.value-minValue)/(maxValue-minValue||1)
    return {...point,x:maxTime===minTime?400:56+(times[index]-minTime)/(maxTime-minTime)*688,
      y:metric==='rank'?40+fraction*184:224-fraction*184}
  })
}
