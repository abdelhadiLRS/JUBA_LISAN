import { apiFetch } from '@/lib/api'

export type GameEventPayload = {
  eventId?: string
  gameId: string
  questionsAnswered: number
  correctAnswers: number
  roundScore: number
  dailyChallenge?: boolean
  dailyChallengeDate?: string
  achievements?: string[]
}

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
}

export async function persistGameEvent(payload: GameEventPayload): Promise<ServerGameStats> {
  const response = await apiFetch('/api/progress/game-event', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      event_id: payload.eventId ?? crypto.randomUUID(),
      game_id: payload.gameId,
      questions_answered: payload.questionsAnswered,
      correct_answers: payload.correctAnswers,
      round_score: payload.roundScore,
      daily_challenge: payload.dailyChallenge ?? false,
      daily_challenge_date: payload.dailyChallengeDate ?? '',
      achievements: payload.achievements ?? [],
    }),
  })
  if (!response.ok) throw new Error(`Game event failed: ${response.status}`)
  return response.json() as Promise<ServerGameStats>
}