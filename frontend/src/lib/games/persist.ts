import { apiFetch } from '@/lib/api'

export type GameId = 'math' | 'words' | 'sequence' | 'memory' | 'matching' | 'ordering'
export type GameLanguage = 'ar' | 'fr' | 'en'

export type ServerGameStats = {
  total_xp: number
  games_played: number
  questions_answered: number
  correct_answers: number
  best_round_score: number
  daily_challenges_completed: number
  last_daily_challenge_date: string
  current_correct_streak: number
  best_correct_streak: number
  achievements: string[]
  skills: Record<string, number>
}

export type GameSessionQuestion = {
  id: string
  prompt: string
  choices: string[]
  hint: string
  skill: string
  difficulty: number
}

export type GameSessionStartResponse = {
  session_id: string
  game_id: string
  questions: GameSessionQuestion[]
  expires_at: string
  interaction?: InteractiveGameChallenge
}

export type InteractiveGameChallenge =
  | { type: 'memory'; cards: Array<{ id: string; label: string; pair_key?: string }> }
  | { type: 'matching'; left: Array<{ id: string; label: string; pair_key?: string }>; right: Array<{ id: string; label: string; pair_key?: string }> }
  | { type: 'ordering'; items: Array<{ id: string; label: string }> }

export type InteractiveGameTrace =
  | { first: string; second: string }
  | { left: string; right: string }
  | { order: string[] }

export type GameSessionResult = ServerGameStats & {
  round_score: number
  round_correct: number
  round_questions: number
  xp_earned: number
  new_achievements: string[]
}

export async function startGameSession(
  gameId: string,
  language: 'ar' | 'fr' | 'en',
  difficulty: number,
): Promise<GameSessionStartResponse> {
  const response = await apiFetch('/api/progress/game-session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      game_id: gameId,
      language,
      difficulty: Math.min(3, Math.max(1, Math.floor(difficulty))),
    }),
  })
  if (!response.ok) throw new Error(`Game session start failed: ${response.status}`)
  return response.json() as Promise<GameSessionStartResponse>
}

export async function completeGameSession(
  sessionId: string,
  answers: Array<{ question_id: string; choice: string }>,
  dailyChallenge = false,
  dailyChallengeDate = '',
  interactionTrace: InteractiveGameTrace[] = [],
): Promise<GameSessionResult> {
  const response = await apiFetch('/api/progress/game-session/complete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      answers,
      interaction_trace: interactionTrace,
      daily_challenge: dailyChallenge,
      daily_challenge_date: dailyChallengeDate,
    }),
  })
  if (!response.ok) throw new Error(`Game session completion failed: ${response.status}`)
  return response.json() as Promise<GameSessionResult>
}
