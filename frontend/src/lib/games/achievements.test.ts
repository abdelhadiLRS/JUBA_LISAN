import { describe, expect, it } from 'vitest'
import { evaluateAchievements, emptyGameStats } from './achievements'

describe('game achievements', () => {
  it('unlocks first game and xp milestones', () => {
    const stats = { ...emptyGameStats(), gamesPlayed: 1 }
    const unlocked = evaluateAchievements({ xp: 500, skills: {}, stats, roundScore: 0, perfectRound: false, dailyChallengeCompleted: false })
    expect(unlocked).toEqual(expect.arrayContaining(['first_game', 'xp_100', 'xp_500']))
  })

  it('unlocks a perfect round', () => {
    const unlocked = evaluateAchievements({ xp: 80, skills: {}, stats: emptyGameStats(), roundScore: 80, perfectRound: true, dailyChallengeCompleted: false })
    expect(unlocked).toContain('perfect_round')
  })

  it('preserves existing achievements', () => {
    const unlocked = evaluateAchievements({ xp: 0, skills: {}, stats: emptyGameStats(), roundScore: 0, perfectRound: false, dailyChallengeCompleted: false }, ['daily_challenge'])
    expect(unlocked).toContain('daily_challenge')
  })

  it('requires progress in three skills', () => {
    const stats = emptyGameStats()
    expect(evaluateAchievements({ xp: 0, skills: { math: 0.1, words: 0.2 }, stats, roundScore: 0, perfectRound: false, dailyChallengeCompleted: false })).not.toContain('multi_skill')
    expect(evaluateAchievements({ xp: 0, skills: { math: 0.1, words: 0.2, sequence: 0.3 }, stats, roundScore: 0, perfectRound: false, dailyChallengeCompleted: false })).toContain('multi_skill')
  })
})
