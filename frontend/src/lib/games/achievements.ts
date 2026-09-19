export type AchievementId =
  | 'first_game'
  | 'perfect_round'
  | 'streak_5'
  | 'xp_100'
  | 'xp_500'
  | 'multi_skill'
  | 'daily_challenge'

export interface GameStats {
  gamesPlayed: number
  questionsAnswered: number
  correctAnswers: number
  bestRoundScore: number
  dailyChallengesCompleted: number
  lastDailyChallengeDate?: string
  currentCorrectStreak?: number
  bestCorrectStreak: number
}

export interface AchievementState {
  unlocked: AchievementId[]
}

export interface AchievementContext {
  xp: number
  skills: Record<string, number>
  stats: GameStats
  roundScore: number
  perfectRound: boolean
  dailyChallengeCompleted: boolean
}

export const ACHIEVEMENTS: Record<AchievementId, { xp: number; title: string; description: string }> = {
  first_game: { xp: 25, title: 'First Game', description: 'Complete your first game.' },
  perfect_round: { xp: 50, title: 'Perfect Round', description: 'Complete a round without mistakes.' },
  streak_5: { xp: 40, title: 'On Fire', description: 'Reach a five-answer correct streak.' },
  xp_100: { xp: 25, title: 'Getting Started', description: 'Reach 100 XP.' },
  xp_500: { xp: 100, title: 'Rising Star', description: 'Reach 500 XP.' },
  multi_skill: { xp: 75, title: 'Multi-Skilled', description: 'Build progress in three skills.' },
  daily_challenge: { xp: 60, title: 'Daily Hero', description: 'Complete a daily challenge.' },
}

export function getAchievementRewardXP(ids: AchievementId[]): number {
  return ids.reduce((total, id) => total + (ACHIEVEMENTS[id]?.xp ?? 0), 0)
}

export function evaluateAchievements(
  context: AchievementContext,
  existing: AchievementId[] = [],
): AchievementId[] {
  const unlocked = new Set(existing)
  if (context.stats.gamesPlayed >= 1) unlocked.add('first_game')
  if (context.perfectRound) unlocked.add('perfect_round')
  if (context.stats.bestCorrectStreak >= 5) unlocked.add('streak_5')
  if (context.xp >= 100) unlocked.add('xp_100')
  if (context.xp >= 500) unlocked.add('xp_500')
  if (Object.values(context.skills).filter((value) => value > 0).length >= 3) unlocked.add('multi_skill')
  if (context.dailyChallengeCompleted) unlocked.add('daily_challenge')
  return Array.from(unlocked)
}

export function emptyGameStats(): GameStats {
  return {
    gamesPlayed: 0,
    questionsAnswered: 0,
    correctAnswers: 0,
    bestRoundScore: 0,
    dailyChallengesCompleted: 0,
    lastDailyChallengeDate: '',
    currentCorrectStreak: 0,
    bestCorrectStreak: 0,
  }
}
