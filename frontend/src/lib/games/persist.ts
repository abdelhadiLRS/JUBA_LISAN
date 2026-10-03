import { apiFetch } from '@/lib/api'
import { completeWithRecovery } from './complete-with-recovery'

export type GameId = 'math' | 'words' | 'quick_choice' | 'context_quest' | 'listen_choose' | 'listening_detective' | 'word_categories' | 'translation_sprint' | 'grammar_duel' | 'spelling' | 'word_scramble' | 'fill_blank' | 'sequence' | 'memory' | 'matching' | 'ordering' | 'sentence_builder' | 'review_mix'
export type GameLanguage = 'ar' | 'fr' | 'en' | 'es' | 'de' | 'it' | 'pt' | 'ja' | 'ko' | 'zh' | 'tr' | 'ru' | 'nl' | 'pl' | 'el' | 'sv' | 'da' | 'no' | 'fi' | 'cs'

/** Map the learner's target language, independently of interface locale. */
export function gameLanguageForTargetLanguage(targetLanguage?: string | null): GameLanguage {
  const code = String(targetLanguage ?? '').trim().toLowerCase().replace('_', '-')
  const base = code.split('-')[0]
  const supported:GameLanguage[] = ['ar','fr','en','es','de','it','pt','ja','ko','zh','tr','ru','nl','pl','el','sv','da','no','fi','cs']
  return supported.includes(base as GameLanguage) ? base as GameLanguage : 'en'
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
  adaptive_mode?: 'new' | 'review' | 'steady' | 'challenge' | 'skill_review' | 'skill_challenge'
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
  skill_results: Record<string, {
    correct: number
    questions: number
    accuracy: number
    mastery_before?: number
    mastery_after?: number
    mastery_delta?: number
  }>
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

export type GameSessionNextResponse = {
  session_id: string
  correct: boolean
  question: GameSessionQuestion | null
  finished: boolean
  answered: number
  total: number
  adaptive_mode: 'new' | 'review' | 'steady' | 'challenge' | 'skill_review' | 'skill_challenge'
}

export async function answerGameSessionQuestion(
  sessionId: string,
  questionId: string,
  choice: string,
): Promise<GameSessionNextResponse> {
  const response = await apiFetch('/api/progress/game-session/next', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      question_id: questionId,
      choice,
    }),
  })
  if (!response.ok) {
    let detail = ''
    try {
      const payload = await response.json() as { detail?: string }
      if (typeof payload.detail === 'string') detail = payload.detail
    } catch {
      // Preserve the HTTP status when the server returns no JSON detail.
    }
    throw new Error(detail || `Game answer validation failed: ${response.status}`)
  }
  return response.json() as Promise<GameSessionNextResponse>
}

export async function completeGameSession(
  sessionId: string,
  answers: Array<{ question_id: string; choice: string }>,
  dailyChallenge = false,
  dailyChallengeDate = '',
  interactionTrace: InteractiveGameTrace[] = [],
): Promise<GameSessionResult> {
  return completeWithRecovery(sessionId, {
    session_id: sessionId,
    answers,
    interaction_trace: interactionTrace,
    daily_challenge: dailyChallenge,
    daily_challenge_date: dailyChallengeDate,
  })
}

// Arcade contracts are deliberately separate from legacy quiz/trace scoring.
export type ArenaMove = {
  action_id: string
  version: number
  kind: 'flip' | 'hide' | 'pair' | 'answer' | 'timeout' | 'continue' | 'leave'
  value: string
  order: string[]
}
export type ArenaState = {
  session_id: string
  game: string
  version: number
  phase: 'playing' | 'feedback' | 'finished'
  index: number
  total: number
  lives: number
  correct: number
  attempts: number
  max_moves: number
  deadline: number | null
  relaxed: boolean
  question?: {prompt:string;choices?:string[];tiles?:Array<{id:string;label:string}>}
  cards?: Array<{id:string;label:string|null;side:'word'|'meaning';opened:boolean;matched:boolean}>
  feedback: {correct:boolean;answer?:string;meaning?:string}|null
  result?: GameSessionResult & {won:boolean}
}
async function arenaFetch(path:string, body?:unknown):Promise<ArenaState>{
  const response=await apiFetch(path,body===undefined?undefined:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
  if(!response.ok){
    let detail=''
    try{const error=await response.json();if(typeof error.detail==='string')detail=error.detail}catch{}
    throw new Error(detail||`Arcade request failed: ${response.status}`)
  }
  return response.json()
}
export function startArena(gameId:string,targetLanguage:string,difficulty:number,relaxed=false){
  return arenaFetch('/api/progress/game-session/arena',{game_id:gameId,target_language:targetLanguage,difficulty,relaxed})
}
export function readArena(id:string){return arenaFetch('/api/progress/game-session/arena/'+encodeURIComponent(id))}
export function moveArena(id:string,move:ArenaMove){return arenaFetch('/api/progress/game-session/arena/'+encodeURIComponent(id)+'/move',move)}
