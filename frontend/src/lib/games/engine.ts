export type GameId = 'math' | 'words' | 'sequence'
export type GameLanguage = 'ar' | 'fr' | 'en'
export type Difficulty = 1 | 2 | 3

import { getQuestionBank } from '@/lib/games/questions'

export interface GameQuestion {
  prompt: string
  choices: string[]
  answer: string
  hint: string
  skill: string
  difficulty: Difficulty
  topic?: string
  id?: string
  explanation?: string
}

export interface GameResult {
  correct: boolean
  xp: number
  skill: string
  difficulty: Difficulty
}

export function shuffle<T>(items: T[], random: () => number = Math.random): T[] {
  const copy = [...items]
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(random() * (i + 1))
    ;[copy[i], copy[j]] = [copy[j], copy[i]]
  }
  return copy
}

function clampDifficulty(level: number): Difficulty {
  if (level >= 5) return 3
  if (level >= 3) return 2
  return 1
}

export function getDifficulty(level: number): Difficulty {
  return clampDifficulty(level)
}

export function seededRandom(seed: number): () => number {
  let value = seed >>> 0
  return () => {
    value += 0x6d2b79f5
    let t = value
    t = Math.imul(t ^ (t >>> 15), t | 1)
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

function dailySeed(date: string, round: number, game: GameId, lang: GameLanguage): number {
  const input = `${date}|${round}|${game}|${lang}`
  let hash = 2166136261
  for (let index = 0; index < input.length; index += 1) {
    hash ^= input.charCodeAt(index)
    hash = Math.imul(hash, 16777619)
  }
  return hash >>> 0
}

function fromBank(game: GameId, lang: GameLanguage, difficulty: Difficulty, random: () => number): GameQuestion | null {
  const bank = getQuestionBank(game, lang, difficulty)
  if (!bank.length) return null
  const item = bank[Math.floor(random() * bank.length)]
  return {
    id: item.id,
    topic: item.topic,
    prompt: item.prompt,
    choices: shuffle(item.choices, random),
    answer: item.answer,
    hint: item.hint,
    explanation: item.explanation,
    skill: item.skill,
    difficulty: item.difficulty,
  }
}

export function buildQuestion(game: GameId, lang: GameLanguage, level = 1, random: () => number = Math.random): GameQuestion {
  const difficulty = getDifficulty(level)
  const bankQuestion = fromBank(game, lang, difficulty, random)
  if (bankQuestion) return bankQuestion

  if (game === 'math') {
    const max = difficulty === 1 ? 18 : difficulty === 2 ? 60 : 150
    const a = 2 + Math.floor(random() * max)
    const b = 2 + Math.floor(random() * max)
    const subtraction = random() > 0.5
    const left = subtraction ? Math.max(a, b) : a
    const right = subtraction ? Math.min(a, b) : b
    const answer = subtraction ? left - right : left + right
    const spread = difficulty === 1 ? 2 : difficulty === 2 ? 5 : 10
    const choices = shuffle([answer, answer + 1, answer - 1, answer + spread].map(String), random)
    return {
      prompt: `${left} ${subtraction ? '-' : '+'} ${right} = ?`,
      choices,
      answer: String(answer),
      hint: lang === 'ar' ? 'قسّم العملية إلى خطوات صغيرة.' : lang === 'fr' ? 'Découpe le calcul en petites étapes.' : 'Break the calculation into small steps.',
      skill: 'math',
      difficulty,
      topic: 'arithmetic',
    }
  }

  const start = 2 + Math.floor(random() * (difficulty * 4))
  const step = 2 + Math.floor(random() * (difficulty * 4))
  const answer = start + step * 4
  const values = [start, start + step, start + step * 2, start + step * 3]
  return {
    prompt: `${values.join('  →  ')}  →  ?`,
    choices: shuffle([answer, answer + step, answer - step, answer + 2 * step].map(String), random),
    answer: String(answer),
    hint: lang === 'ar' ? 'ابحث عن مقدار الزيادة الثابتة.' : lang === 'fr' ? 'Trouve l’écart constant.' : 'Find the constant step.',
    skill: 'logic',
    difficulty,
    topic: 'sequences',
  }
}

export function buildDailyQuestion(game: GameId, lang: GameLanguage, level = 1, date = new Date().toISOString().slice(0, 10), round = 0): GameQuestion {
  return buildQuestion(game, lang, level, seededRandom(dailySeed(date, round, game, lang)))
}

export function scoreAnswer(question: GameQuestion, choice: string): GameResult {
  const correct = choice === question.answer
  const xp = correct ? 10 + (question.difficulty - 1) * 5 : 0
  return { correct, xp, skill: question.skill, difficulty: question.difficulty }
}
