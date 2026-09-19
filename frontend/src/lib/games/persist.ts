import { apiFetch } from '@/lib/api'

export type GameEventPayload = {
  gameId: string
  questionsAnswered: number
  correctAnswers: number
  roundScore: number
  dailyChallenge?: boolean
  dailyChallengeDate?: string
  achievements?: string[]
}

export async function persistGameEvent(payload: GameEventPayload) {
  return apiFetch('/api/progress/game-event', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      event_id: crypto.randomUUID(),
      game_id: payload.gameId,
      questions_answered: payload.questionsAnswered,
      correct_answers: payload.correctAnswers,
      round_score: payload.roundScore,
      daily_challenge: payload.dailyChallenge ?? false,
      daily_challenge_date: payload.dailyChallengeDate ?? '',
      achievements: payload.achievements ?? [],
    }),
  })
}
