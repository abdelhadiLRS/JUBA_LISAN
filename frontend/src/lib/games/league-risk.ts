import {LEAGUE_TIERS,projectedMovement} from './league-movement'
export type LeagueRiskInput={season_id:number|null;joined:boolean;finalized:boolean;tier:string;total:number;ends_at:string;current_user:{rank:number;xp:number}|null}
export type LeagueRisk={level:'near'|'danger';rank:number;cutoff:number;expiresSoon:boolean;seasonId:number;signature:string}
export function leagueRisk(season:LeagueRiskInput,now=Date.now()):LeagueRisk|null{
  const index=LEAGUE_TIERS.indexOf(season.tier as typeof LEAGUE_TIERS[number])
  const end=Date.parse(season.ends_at)
  const entry=season.current_user
  if(!season.joined||season.finalized||season.season_id===null||index<=0||season.total<5||!entry||!Number.isFinite(end)||end<=now)return null
  if(!Number.isInteger(entry.rank)||entry.rank<1||entry.rank>season.total||!Number.isFinite(entry.xp))return null
  const quota=Math.max(1,Math.floor(season.total/5))
  const cutoff=season.total-quota
  const movement=projectedMovement(season.tier,entry.rank,entry.xp,season.total)
  // Never call an actual promotion position at risk, including shared ranks.
  if(movement==='promotion')return null
  const level=movement==='demotion'?'danger':entry.rank>=Math.max(1,cutoff-1)?'near':null
  if(!level)return null
  const expiresSoon=end-now<=48*60*60*1000
  return {level,rank:entry.rank,cutoff,expiresSoon,seasonId:season.season_id,
    signature:`${season.season_id}:${level}:${expiresSoon?'closing':'open'}`}
}
