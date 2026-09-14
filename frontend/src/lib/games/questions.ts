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
  // Arabic -> English
  { id: 'ar-book', game: 'words', lang: 'ar', topic: 'daily-life', skill: 'vocabulary', difficulty: 1, prompt: 'كتاب', answer: 'Book', choices: ['Book', 'Water', 'School', 'Moon'], hint: 'شيء نقرأه.', explanation: 'كتاب تعني Book.' },
  { id: 'ar-water', game: 'words', lang: 'ar', topic: 'daily-life', skill: 'vocabulary', difficulty: 1, prompt: 'ماء', answer: 'Water', choices: ['Tree', 'Water', 'Road', 'Friend'], hint: 'نشربه كل يوم.', explanation: 'ماء تعني Water.' },
  { id: 'ar-school', game: 'words', lang: 'ar', topic: 'education', skill: 'vocabulary', difficulty: 1, prompt: 'مدرسة', answer: 'School', choices: ['School', 'Window', 'Moon', 'Book'], hint: 'مكان التعلّم.', explanation: 'مدرسة تعني School.' },
  { id: 'ar-sun', game: 'words', lang: 'ar', topic: 'nature', skill: 'vocabulary', difficulty: 1, prompt: 'شمس', answer: 'Sun', choices: ['Sun', 'Rain', 'Door', 'Pen'], hint: 'تضيء السماء نهارًا.', explanation: 'شمس تعني Sun.' },
  { id: 'ar-pen', game: 'words', lang: 'ar', topic: 'school', skill: 'vocabulary', difficulty: 1, prompt: 'قلم', answer: 'Pen', choices: ['Pen', 'Chair', 'Sea', 'House'], hint: 'نكتب به.', explanation: 'قلم تعني Pen.' },
  { id: 'ar-friend', game: 'words', lang: 'ar', topic: 'people', skill: 'vocabulary', difficulty: 1, prompt: 'صديق', answer: 'Friend', choices: ['Friend', 'Teacher', 'Book', 'Road'], hint: 'شخص تحبه وتثق به.', explanation: 'صديق تعني Friend.' },
  { id: 'ar-teacher', game: 'words', lang: 'ar', topic: 'education', skill: 'vocabulary', difficulty: 2, prompt: 'معلّم', answer: 'Teacher', choices: ['Teacher', 'Student', 'Doctor', 'Driver'], hint: 'شخص يساعدك على التعلّم.', explanation: 'معلّم تعني Teacher.' },
  { id: 'ar-window', game: 'words', lang: 'ar', topic: 'home', skill: 'vocabulary', difficulty: 2, prompt: 'نافذة', answer: 'Window', choices: ['Window', 'Kitchen', 'Garden', 'Table'], hint: 'نرى من خلالها الخارج.', explanation: 'نافذة تعني Window.' },
  { id: 'ar-journey', game: 'words', lang: 'ar', topic: 'travel', skill: 'vocabulary', difficulty: 3, prompt: 'رحلة', answer: 'Journey', choices: ['Journey', 'Lesson', 'Answer', 'Morning'], hint: 'انتقال من مكان إلى آخر.', explanation: 'رحلة تعني Journey.' },
  { id: 'ar-environment', game: 'words', lang: 'ar', topic: 'science', skill: 'vocabulary', difficulty: 3, prompt: 'بيئة', answer: 'Environment', choices: ['Environment', 'Language', 'Calendar', 'Village'], hint: 'المحيط الذي نعيش فيه.', explanation: 'بيئة تعني Environment.' },

  // French -> English
  { id: 'fr-livre', game: 'words', lang: 'fr', topic: 'daily-life', skill: 'vocabulary', difficulty: 1, prompt: 'livre', answer: 'Book', choices: ['Book', 'Water', 'School', 'Tree'], hint: 'On le lit.', explanation: 'livre signifie Book.' },
  { id: 'fr-eau', game: 'words', lang: 'fr', topic: 'daily-life', skill: 'vocabulary', difficulty: 1, prompt: 'eau', answer: 'Water', choices: ['Water', 'Road', 'Friend', 'Window'], hint: 'On la boit.', explanation: 'eau signifie Water.' },
  { id: 'fr-ecole', game: 'words', lang: 'fr', topic: 'education', skill: 'vocabulary', difficulty: 1, prompt: 'école', answer: 'School', choices: ['School', 'Moon', 'Road', 'Friend'], hint: 'Lieu où l’on apprend.', explanation: 'école signifie School.' },
  { id: 'fr-soleil', game: 'words', lang: 'fr', topic: 'nature', skill: 'vocabulary', difficulty: 1, prompt: 'soleil', answer: 'Sun', choices: ['Sun', 'Rain', 'Door', 'Pen'], hint: 'Il éclaire le jour.', explanation: 'soleil signifie Sun.' },
  { id: 'fr-stylo', game: 'words', lang: 'fr', topic: 'school', skill: 'vocabulary', difficulty: 1, prompt: 'stylo', answer: 'Pen', choices: ['Pen', 'Chair', 'Sea', 'House'], hint: 'On écrit avec.', explanation: 'stylo signifie Pen.' },
  { id: 'fr-ami', game: 'words', lang: 'fr', topic: 'people', skill: 'vocabulary', difficulty: 1, prompt: 'ami', answer: 'Friend', choices: ['Friend', 'Teacher', 'Book', 'Road'], hint: 'Une personne proche de toi.', explanation: 'ami signifie Friend.' },
  { id: 'fr-professeur', game: 'words', lang: 'fr', topic: 'education', skill: 'vocabulary', difficulty: 2, prompt: 'professeur', answer: 'Teacher', choices: ['Teacher', 'Student', 'Doctor', 'Driver'], hint: 'Il aide les élèves à apprendre.', explanation: 'professeur signifie Teacher.' },
  { id: 'fr-fenetre', game: 'words', lang: 'fr', topic: 'home', skill: 'vocabulary', difficulty: 2, prompt: 'fenêtre', answer: 'Window', choices: ['Window', 'Kitchen', 'Garden', 'Table'], hint: 'On regarde dehors à travers elle.', explanation: 'fenêtre signifie Window.' },
  { id: 'fr-voyage', game: 'words', lang: 'fr', topic: 'travel', skill: 'vocabulary', difficulty: 3, prompt: 'voyage', answer: 'Journey', choices: ['Journey', 'Lesson', 'Answer', 'Morning'], hint: 'Déplacement vers un autre lieu.', explanation: 'voyage signifie Journey.' },
  { id: 'fr-environnement', game: 'words', lang: 'fr', topic: 'science', skill: 'vocabulary', difficulty: 3, prompt: 'environnement', answer: 'Environment', choices: ['Environment', 'Language', 'Calendar', 'Village'], hint: 'Le milieu dans lequel nous vivons.', explanation: 'environnement signifie Environment.' },

  // English -> Arabic
  { id: 'en-book', game: 'words', lang: 'en', topic: 'daily-life', skill: 'vocabulary', difficulty: 1, prompt: 'book', answer: 'كتاب', choices: ['كتاب', 'ماء', 'مدرسة', 'قمر'], hint: 'شيء نقرأه.', explanation: 'book تعني كتاب.' },
  { id: 'en-water', game: 'words', lang: 'en', topic: 'daily-life', skill: 'vocabulary', difficulty: 1, prompt: 'water', answer: 'ماء', choices: ['شجرة', 'ماء', 'طريق', 'صديق'], hint: 'نشربه كل يوم.', explanation: 'water تعني ماء.' },
  { id: 'en-school', game: 'words', lang: 'en', topic: 'education', skill: 'vocabulary', difficulty: 1, prompt: 'school', answer: 'مدرسة', choices: ['شجرة', 'مدرسة', 'نافذة', 'طريق'], hint: 'مكان التعلّم.', explanation: 'school تعني مدرسة.' },
  { id: 'en-sun', game: 'words', lang: 'en', topic: 'nature', skill: 'vocabulary', difficulty: 1, prompt: 'sun', answer: 'شمس', choices: ['شمس', 'مطر', 'باب', 'قلم'], hint: 'تضيء السماء نهارًا.', explanation: 'sun تعني شمس.' },
  { id: 'en-pen', game: 'words', lang: 'en', topic: 'school', skill: 'vocabulary', difficulty: 1, prompt: 'pen', answer: 'قلم', choices: ['قلم', 'كرسي', 'بحر', 'بيت'], hint: 'نكتب به.', explanation: 'pen تعني قلم.' },
  { id: 'en-friend', game: 'words', lang: 'en', topic: 'people', skill: 'vocabulary', difficulty: 1, prompt: 'friend', answer: 'صديق', choices: ['صديق', 'معلّم', 'كتاب', 'طريق'], hint: 'شخص تحبه وتثق به.', explanation: 'friend تعني صديق.' },
  { id: 'en-teacher', game: 'words', lang: 'en', topic: 'education', skill: 'vocabulary', difficulty: 2, prompt: 'teacher', answer: 'معلّم', choices: ['معلّم', 'طالب', 'طبيب', 'سائق'], hint: 'شخص يساعدك على التعلّم.', explanation: 'teacher تعني معلّم.' },
  { id: 'en-window', game: 'words', lang: 'en', topic: 'home', skill: 'vocabulary', difficulty: 2, prompt: 'window', answer: 'نافذة', choices: ['نافذة', 'مطبخ', 'حديقة', 'طاولة'], hint: 'نرى من خلالها الخارج.', explanation: 'window تعني نافذة.' },
  { id: 'en-journey', game: 'words', lang: 'en', topic: 'travel', skill: 'vocabulary', difficulty: 3, prompt: 'journey', answer: 'رحلة', choices: ['رحلة', 'درس', 'إجابة', 'صباح'], hint: 'انتقال من مكان إلى آخر.', explanation: 'journey تعني رحلة.' },
  { id: 'en-environment', game: 'words', lang: 'en', topic: 'science', skill: 'vocabulary', difficulty: 3, prompt: 'environment', answer: 'بيئة', choices: ['بيئة', 'لغة', 'تقويم', 'قرية'], hint: 'المحيط الذي نعيش فيه.', explanation: 'environment تعني بيئة.' },

  // Math question bank for curated, explainable learning items.
  { id: 'math-add-1', game: 'math', lang: 'ar', topic: 'arithmetic', skill: 'math', difficulty: 1, prompt: '7 + 5 = ?', answer: '12', choices: ['10', '11', '12', '13'], hint: 'اجمع 7 ثم 5.', explanation: '7 + 5 = 12.' },
  { id: 'math-sub-1', game: 'math', lang: 'ar', topic: 'arithmetic', skill: 'math', difficulty: 1, prompt: '15 - 6 = ?', answer: '9', choices: ['8', '9', '10', '11'], hint: 'اطرح 6 من 15.', explanation: '15 - 6 = 9.' },
  { id: 'math-add-2', game: 'math', lang: 'fr', topic: 'arithmetic', skill: 'math', difficulty: 2, prompt: '24 + 18 = ?', answer: '42', choices: ['40', '41', '42', '44'], hint: 'Additionne les dizaines puis les unités.', explanation: '24 + 18 = 42.' },
  { id: 'math-sub-2', game: 'math', lang: 'en', topic: 'arithmetic', skill: 'math', difficulty: 2, prompt: '50 - 17 = ?', answer: '33', choices: ['31', '32', '33', '34'], hint: 'Subtract 17 from 50.', explanation: '50 - 17 = 33.' },
]

export const QUESTION_BANK: QuestionBankItem[] = vocabulary

export function getQuestionBank(game: GameId, lang: GameLanguage, difficulty?: Difficulty): QuestionBankItem[] {
  return QUESTION_BANK.filter(
    (item) =>
      item.game === game &&
      item.lang === lang &&
      (difficulty === undefined || item.difficulty <= difficulty)
  )
}
