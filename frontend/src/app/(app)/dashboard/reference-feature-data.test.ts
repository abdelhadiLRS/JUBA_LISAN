import { describe, expect, it } from 'vitest'
import { getNextAchievement, knownEarnedAchievements, goalPercent, weekActivity, type GameSummary } from './reference-feature-data'
const summary:GameSummary={total_xp:60,games_played:1,questions_answered:4,correct_answers:4,best_round_score:100,daily_challenges_completed:0,last_daily_challenge_date:'',current_correct_streak:4,best_correct_streak:4,achievements:['first_game'],skills:{grammar:.2}}
describe('reference dashboard real data',()=>{
  it('converts backend goal fractions to percentages and clamps invalid ranges',()=>{expect(goalPercent(.5)).toBe(50);expect(goalPercent(2)).toBe(100);expect(goalPercent(-1)).toBe(0);expect(goalPercent(NaN)).toBe(0)})
  it('selects the closest incomplete measurable achievement without inventing perfect-round progress',()=>{expect(getNextAchievement(summary)?.id).toBe('streak_5');expect(getNextAchievement(summary)?.percent).toBe(80)})
  it('does not infer earned IDs merely from thresholds',()=>{const data={...summary,total_xp:500,achievements:['first_game','perfect_round','unknown']};expect(knownEarnedAchievements(data)).toEqual(['first_game','perfect_round']);expect(getNextAchievement(data)?.id).not.toBe('xp_100')})
  it('uses server day boundaries and zero-fills dates with no recorded XP',()=>{const days=weekActivity([{date:'2026-10-02',xp_earned:15}],'2026-10-03');expect(days).toHaveLength(7);expect(days[0].date).toBe('2026-09-27');expect(days[5]).toEqual({date:'2026-10-02',value:15});expect(days[6]).toEqual({date:'2026-10-03',value:0})})
})
