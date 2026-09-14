export type GameId = 'math' | 'words' | 'sequence' | 'memory' | 'matching' | 'ordering'
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

function localizedHint(lang: GameLanguage, ar: string, fr: string, en: string): string {
  return lang === 'ar' ? ar : lang === 'fr' ? fr : en
}

function buildMathQuestion(lang: GameLanguage, difficulty: Difficulty, random: () => number): GameQuestion {
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
    hint: localizedHint(lang, 'قسّم العملية إلى خطوات صغيرة.', 'Découpe le calcul en petites étapes.', 'Break the calculation into small steps.'),
    skill: 'math',
    difficulty,
    topic: 'arithmetic',
  }
}

function buildSequenceQuestion(lang: GameLanguage, difficulty: Difficulty, random: () => number): GameQuestion {
  const start = 2 + Math.floor(random() * (difficulty * 4))
  const step = 2 + Math.floor(random() * (difficulty * 4))
  const answer = start + step * 4
  const values = [start, start + step, start + step * 2, start + step * 3]
  return {
    prompt: `${values.join('  →  ')}  →  ?`,
    choices: shuffle([answer, answer + step, answer - step, answer + 2 * step].map(String), random),
    answer: String(answer),
    hint: localizedHint(lang, 'ابحث عن مقدار الزيادة الثابتة.', 'Trouve l’écart constant.', 'Find the constant step.'),
    skill: 'logic',
    difficulty,
    topic: 'sequences',
  }
}

function buildMemoryQuestion(lang: GameLanguage, difficulty: Difficulty, random: () => number): GameQuestion {
  const symbols = lang === 'ar'
    ? ['قمر', 'كتاب', 'بحر', 'شمس', 'قلم', 'باب']
    : lang === 'fr'
      ? ['lune', 'livre', 'mer', 'soleil', 'stylo', 'porte']
      : ['moon', 'book', 'sea', 'sun', 'pen', 'door']
  const size = difficulty === 1 ? 3 : difficulty === 2 ? 4 : 5
  const shown = shuffle(symbols, random).slice(0, size)
  const answer = shown.join(' • ')
  const alternatives = Array.from({ length: 3 }, () => shuffle(shown, random).join(' • '))
  const choices = shuffle(Array.from(new Set([answer, ...alternatives])).slice(0, 4), random)
  return {
    prompt: `${localizedHint(lang, 'تذكّر هذا الترتيب ثم اختره:', 'Mémorise cet ordre puis choisis-le :', 'Remember this order, then choose it:')}\n\n${answer}`,
    choices,
    answer,
    hint: localizedHint(lang, 'ركّز على ترتيب العناصر من اليسار إلى اليمين.', 'Concentre-toi sur l’ordre de gauche à droite.', 'Focus on the order from left to right.'),
    skill: 'memory',
    difficulty,
    topic: 'memory-sequence',
  }
}

function buildMatchingQuestion(lang: GameLanguage, difficulty: Difficulty, random: () => number): GameQuestion {
  const pairs = lang === 'ar'
    ? [['كتاب', 'book'], ['ماء', 'water'], ['مدرسة', 'school'], ['قلم', 'pen']]
    : lang === 'fr'
      ? [['livre', 'book'], ['eau', 'water'], ['école', 'school'], ['stylo', 'pen']]
      : [['book', 'livre'], ['water', 'eau'], ['school', 'école'], ['pen', 'stylo']]
  const pair = pairs[Math.floor(random() * pairs.length)]
  const wrong = shuffle(pairs.filter((candidate) => candidate[0] !== pair[0]).map((candidate) => candidate[1]), random).slice(0, 3)
  return {
    prompt: localizedHint(lang, `طابق: ${pair[0]}`, `Associe : ${pair[0]}`, `Match: ${pair[0]}`),
    choices: shuffle([pair[1], ...wrong], random),
    answer: pair[1],
    hint: localizedHint(lang, 'فكّر في معنى الكلمة وسياقها.', 'Pense au sens et au contexte du mot.', 'Think about the word meaning and context.'),
    skill: 'vocabulary',
    difficulty,
    topic: 'matching',
  }
}

function buildOrderingQuestion(lang: GameLanguage, difficulty: Difficulty, random: () => number): GameQuestion {
  const base = difficulty === 1 ? [1, 2, 3, 4] : difficulty === 2 ? [2, 4, 6, 8] : [3, 6, 9, 12]
  const scrambled = shuffle(base, random)
  const answer = base.join(' → ')
  const alternatives = [
    scrambled.join(' → '),
    [...base].reverse().join(' → '),
    [...base.slice(1), base[0]].join(' → '),
  ]
  return {
    prompt: localizedHint(lang, `رتّب الأرقام من الأصغر إلى الأكبر: ${scrambled.join(' · ')}`, `Ordonne du plus petit au plus grand : ${scrambled.join(' · ')}`, `Order from smallest to largest: ${scrambled.join(' · ')}`),
    choices: shuffle(Array.from(new Set([answer, ...alternatives])).slice(0, 4), random),
    answer,
    hint: localizedHint(lang, 'ابدأ بالعدد الأصغر ثم تابع تصاعديًا.', 'Commence par le plus petit puis monte.', 'Start with the smallest number and move upward.'),
    skill: 'ordering',
    difficulty,
    topic: 'ordering',
  }
}

export function buildQuestion(game: GameId, lang: GameLanguage, level = 1, random: () => number = Math.random): GameQuestion {
  const difficulty = getDifficulty(level)
  const bankQuestion = fromBank(game, lang, difficulty, random)
  if (bankQuestion) return bankQuestion

  if (game === 'math') return buildMathQuestion(lang, difficulty, random)
  if (game === 'sequence') return buildSequenceQuestion(lang, difficulty, random)
  if (game === 'memory') return buildMemoryQuestion(lang, difficulty, random)
  if (game === 'matching') return buildMatchingQuestion(lang, difficulty, random)
  if (game === 'ordering') return buildOrderingQuestion(lang, difficulty, random)
  return buildMatchingQuestion(lang, difficulty, random)
}

export function buildDailyQuestion(game: GameId, lang: GameLanguage, level = 1, date = new Date().toISOString().slice(0, 10), round = 0): GameQuestion {
  return buildQuestion(game, lang, level, seededRandom(dailySeed(date, round, game, lang)))
}

export function scoreAnswer(question: GameQuestion, choice: string): GameResult {
  const correct = choice === question.answer
  const xp = correct ? 10 + (question.difficulty - 1) * 5 : 0
  return { correct, xp, skill: question.skill, difficulty: question.difficulty }
}
