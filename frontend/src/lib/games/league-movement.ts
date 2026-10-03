export const LEAGUE_TIERS=['bronze','silver','gold','sapphire','ruby','diamond'] as const
export type Movement='promotion'|'demotion'|'stay'
/** Mirrors server next_tier: shared SQL ranks, positive XP, five-player minimum. */
export function projectedMovement(tier:string,rank:number,xp:number,total:number):Movement{
  const index=LEAGUE_TIERS.indexOf(tier as typeof LEAGUE_TIERS[number])
  if(index<0||total<5||rank<1)return 'stay'
  const quota=Math.max(1,Math.floor(total/5))
  if(xp>0&&rank<=quota&&index<LEAGUE_TIERS.length-1)return 'promotion'
  if(rank>total-quota&&index>0)return 'demotion'
  return 'stay'
}
export function settledMovement(tier:string,next:string|null):Movement|null{
  if(next===null)return null
  const before=LEAGUE_TIERS.indexOf(tier as typeof LEAGUE_TIERS[number])
  const after=LEAGUE_TIERS.indexOf(next as typeof LEAGUE_TIERS[number])
  if(before<0||after<0)return null
  return after>before?'promotion':after<before?'demotion':'stay'
}
