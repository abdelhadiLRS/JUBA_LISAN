import { ACHIEVEMENTS, type AchievementId } from '@/lib/games/achievements'

export interface GoalData {
  daily_xp_target:number;weekly_xp_target:number;daily_xp:number;weekly_xp:number;
  daily_progress:number;weekly_progress:number;daily_completed:boolean;weekly_completed:boolean;
  daily_reward_xp:number;weekly_reward_xp:number;daily_reward_claimed:boolean;weekly_reward_claimed:boolean;
  day:string;week_start:string;week_end:string;
}
export interface GameSummary {
  total_xp:number;games_played:number;questions_answered:number;correct_answers:number;
  best_round_score:number;daily_challenges_completed:number;last_daily_challenge_date:string;
  current_correct_streak:number;best_correct_streak:number;achievements:string[];skills:Record<string,number>;
}
export interface HistoryEntry {date:string;xp_earned:number}
export interface AchievementProgress {id:AchievementId;current:number;target:number;percent:number}
export function goalPercent(fraction:number){return Math.round(Math.max(0,Math.min(1,Number.isFinite(fraction)?fraction:0))*100)}
export function getMeasurableAchievements(summary:GameSummary):AchievementProgress[]{
  const metrics:[AchievementId,number,number][]=[['first_game',summary.games_played,1],['streak_5',summary.best_correct_streak,5],['xp_100',summary.total_xp,100],['xp_500',summary.total_xp,500],['multi_skill',Object.values(summary.skills??{}).filter(value=>value>0).length,3],['daily_challenge',summary.daily_challenges_completed,1]]
  return metrics.map(([id,current,target])=>({id,current:Math.max(0,current),target,percent:Math.min(100,Math.round(Math.max(0,current)/target*100))}))
}
export function getNextAchievement(summary:GameSummary):AchievementProgress|null{
  const unlocked=new Set(summary.achievements)
  // Closest measurable unfinished achievement. Recorded IDs, not thresholds, determine unlocks.
  return getMeasurableAchievements(summary).filter(item=>!unlocked.has(item.id)&&item.current<item.target).sort((a,b)=>b.percent-a.percent)[0]??null
}
export function knownEarnedAchievements(summary:GameSummary):AchievementId[]{return summary.achievements.filter((id):id is AchievementId=>Object.prototype.hasOwnProperty.call(ACHIEVEMENTS,id))}
export function weekActivity(entries:HistoryEntry[],day:string){
  const end=new Date(day+'T00:00:00Z')
  if(!Number.isFinite(end.getTime()))return []
  const values=new Map(entries.map(entry=>[entry.date,Math.max(0,entry.xp_earned)]))
  return Array.from({length:7},(_,index)=>{const date=new Date(end);date.setUTCDate(end.getUTCDate()-(6-index));const key=date.toISOString().slice(0,10);return {date:key,value:values.get(key)??0}})
}
