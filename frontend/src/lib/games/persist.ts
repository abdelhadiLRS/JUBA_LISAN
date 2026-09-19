import { apiFetch } from '@/lib/api'

export type GameEventPayload = {
  eventId?: string
  gameId: string
  questionsAnswered: number
  correctAnswers: number
  roundScore: number
  dailyChallenge?: boolean
  dailyChallengeDate?: string
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
  skills: Record<string, number>
}

const MAX_NETWORK_RETRIES = 2
const RETRY_DELAYS_MS = [150, 300]

function getEventId(eventId?: string): string {
  return eventId ?? crypto.randomUUID()
}

export async function persistGameEvent(payload: GameEventPayload): Promise<ServerGameStats> {
  const eventId = getEventId(payload.eventId)

  for (let attempt = 0; attempt <= MAX_NETWORK_RETRIES; attempt += 1) {
    try {
      const response = await apiFetch('/api/progress/game-event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_id: eventId,
          game_id: payload.gameId,
          questions_answered: payload.questionsAnswered,
          correct_answers: payload.correctAnswers,
          round_score: payload.roundScore,
          daily_challenge: payload.dailyChallenge ?? false,
          daily_challenge_date: payload.dailyChallengeDate ?? '',
        }),
      })

      if (!response.ok) throw new Error(`Game event failed: ${response.status}`)
      return response.json() as Promise<ServerGameStats>
    } catch (error) {
      if (attempt === MAX_NETWORK_RETRIES) throw error
      await new Promise((resolve) => setTimeout(resolve, RETRY_DELAYS_MS[attempt]))
    }
  }

  throw new Error('Game event failed')
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
  | { type: 'memory'; cards: Array<{ id: string; label: string }> }
  | { type: 'matching'; left: Array<{ id: string; label: string }>; right: Array<{ id: string; label: string }> }
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
