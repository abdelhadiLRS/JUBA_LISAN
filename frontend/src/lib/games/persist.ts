import { apiFetch } from '@/lib/api'

export type GameId = 'math' | 'words' | 'quick_choice' | 'context_quest' | 'listen_choose' | 'listening_detective' | 'word_categories' | 'translation_sprint' | 'grammar_duel' | 'spelling' | 'word_scramble' | 'fill_blank' | 'sequence' | 'memory' | 'matching' | 'ordering' | 'sentence_builder' | 'review_mix'
export type GameLanguage = 'ar' | 'fr' | 'en' | 'es' | 'de' | 'it' | 'pt' | 'ja' | 'ko' | 'zh'

/**
 * The game API currently has native question banks for Arabic, French and English.
 * Keep this mapping separate from the UI locale so the interface language never
 * silently becomes the learner's target language.
 */
export function gameLanguageForTargetLanguage(targetLanguage?: string | null): GameLanguage {
  const code = String(targetLanguage ?? '').trim().toLowerCase().replace('_', '-')
  if (code === 'ar' || code.startsWith('ar-')) return 'ar'
  if (code === 'fr' || code.startsWith('fr-')) return 'fr'
  if (code === 'en' || code === 'en-gb' || code === 'en-us' || code.startsWith('en-')) return 'en'
  if (code === 'es' || code.startsWith('es-')) return 'es'
  if (code === 'de' || code.startsWith('de-')) return 'de'
  if (code === 'it' || code.startsWith('it-')) return 'it'
  if (code === 'pt' || code.startsWith('pt-')) return 'pt'
  if (code === 'ja' || code.startsWith('ja-')) return 'ja'
  if (code === 'ko' || code.startsWith('ko-')) return 'ko'
  if (code === 'zh' || code.startsWith('zh-')) return 'zh'
  return 'en'
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

export type GameSessionQuestion = {
  id: string
  prompt: string
  choices: string[]
  hint: string
  skill: string
  difficulty: number
  input_mode?: 'choice' | 'text'
  audio_text?: string | null
  audio_language?: string | null
}

export type GameSessionStartResponse = {
  session_id: string
  game_id: string
  questions: GameSessionQuestion[]
  expires_at: string
  daily_challenge: boolean
  daily_challenge_date: string
  interaction?: InteractiveGameChallenge
  adaptive_mode?: 'new' | 'review' | 'steady' | 'challenge'
  effective_difficulty?: number
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
  language: GameLanguage,
  difficulty: number,
  review = false,
): Promise<GameSessionStartResponse> {
  const response = await apiFetch('/api/progress/game-session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      game_id: gameId,
      language,
      difficulty: Math.min(3, Math.max(1, Math.floor(difficulty))),
      review,
    }),
  })
  if (!response.ok) {
    let detail = ''
    try {
      const payload = await response.json() as { detail?: string | { msg?: string }[] }
      if (typeof payload.detail === 'string') detail = payload.detail
      else if (Array.isArray(payload.detail)) detail = payload.detail.map((item) => item?.msg).filter(Boolean).join('; ')
    } catch {
      // Keep the HTTP status when the server did not return JSON.
    }
    throw new Error(detail || `Game session start failed: ${response.status}`)
  }
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
