import type { GameId, GameLanguage, Difficulty } from '@/lib/games/engine'

export interface QuestionBankItem {
  id: string
  game: GameId
  lang: GameLanguage
  topic: string
  skill: string
  difficulty: Difficulty
  prompt: string
  answer: string
  choices: string[]
  hint: string
  explanation: string
}

const vocabulary: QuestionBankItem[] = [
  { id: 'ar-book', game: 'words', lang: 'ar', topic: 'daily-life', skill: 'vocabulary', difficulty: 1, prompt: 'كتاب', answer: 'Book', choices: ['Book', 'Water', 'School', 'Moon'], hint: 'شيء نقرأه.', explanation: 'كتاب تعني Book.' },
  { id: 'ar-water', game: 'words', lang: 'ar', topic: 'daily-life', skill: 'vocabulary', difficulty: 1, prompt: 'ماء', answer: 'Water', choices: ['Tree', 'Water', 'Road', 'Friend'], hint: 'نشربه كل يوم.', explanation: 'ماء تعني Water.' },
  { id: 'ar-school', game: 'words', lang: 'ar', topic: 'education', skill: 'vocabulary', difficulty: 1, prompt: 'مدرسة', answer: 'School', choices: ['School', 'Window', 'Moon', 'Book'], hint: 'مكان التعلّم.', explanation: 'مدرسة تعني School.' },
  { id: 'fr-livre', game: 'words', lang: 'fr', topic: 'daily-life', skill: 'vocabulary', difficulty: 1, prompt: 'livre', answer: 'Book', choices: ['Book', 'Water', 'School', 'Tree'], hint: 'On le lit.', explanation: 'livre signifie Book.' },
  { id: 'fr-ecole', game: 'words', lang: 'fr', topic: 'education', skill: 'vocabulary', difficulty: 1, prompt: 'école', answer: 'School', choices: ['School', 'Moon', 'Road', 'Friend'], hint: 'Lieu où l’on apprend.', explanation: 'école signifie School.' },
  { id: 'en-book', game: 'words', lang: 'en', topic: 'daily-life', skill: 'vocabulary', difficulty: 1, prompt: 'book', answer: 'كتاب', choices: ['كتاب', 'ماء', 'مدرسة', 'قمر'], hint: 'شيء نقرأه.', explanation: 'book تعني كتاب.' },
  { id: 'en-school', game: 'words', lang: 'en', topic: 'education', skill: 'vocabulary', difficulty: 1, prompt: 'school', answer: 'مدرسة', choices: ['شجرة', 'مدرسة', 'نافذة', 'طريق'], hint: 'مكان التعلّم.', explanation: 'school تعني مدرسة.' },
]

export const QUESTION_BANK: QuestionBankItem[] = vocabulary

export function getQuestionBank(game: GameId, lang: GameLanguage, difficulty?: Difficulty): QuestionBankItem[] {
  return QUESTION_BANK.filter((item) => item.game === game && item.lang === lang && (difficulty === undefined || item.difficulty <= difficulty))
}
