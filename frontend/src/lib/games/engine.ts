export type GameId = 'math' | 'words' | 'sequence';
export type GameLanguage = 'ar' | 'fr' | 'en';
export type Difficulty = 1 | 2 | 3;

export interface GameQuestion {
  prompt: string;
  choices: string[];
  answer: string;
  hint: string;
  skill: string;
  difficulty: Difficulty;
}

export interface GameResult {
  correct: boolean;
  xp: number;
  skill: string;
  difficulty: Difficulty;
}

export function shuffle<T>(items: T[]): T[] {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function clampDifficulty(level: number): Difficulty {
  if (level >= 5) return 3;
  if (level >= 3) return 2;
  return 1;
}

export function getDifficulty(level: number): Difficulty {
  return clampDifficulty(level);
}

export function buildQuestion(game: GameId, lang: GameLanguage, level = 1): GameQuestion {
  const difficulty = getDifficulty(level);

  if (game === 'math') {
    const max = difficulty === 1 ? 18 : difficulty === 2 ? 60 : 150;
    const a = 2 + Math.floor(Math.random() * max);
    const b = 2 + Math.floor(Math.random() * max);
    const subtraction = Math.random() > 0.5;
    const left = subtraction ? Math.max(a, b) : a;
    const right = subtraction ? Math.min(a, b) : b;
    const answer = subtraction ? left - right : left + right;
    const spread = difficulty === 1 ? 2 : difficulty === 2 ? 5 : 10;
    const choices = shuffle([answer, answer + 1, answer - 1, answer + spread].map(String));
    return {
      prompt: `${left} ${subtraction ? '-' : '+'} ${right} = ?`,
      choices,
      answer: String(answer),
      hint: lang === 'ar' ? 'قسّم العملية إلى خطوات صغيرة.' : lang === 'fr' ? 'Découpe le calcul en petites étapes.' : 'Break the calculation into small steps.',
      skill: 'math',
      difficulty,
    };
  }

  if (game === 'words') {
    const bank = lang === 'ar'
      ? [['كتاب', 'Book'], ['ماء', 'Water'], ['مدرسة', 'School'], ['قمر', 'Moon'], ['شجرة', 'Tree'], ['نافذة', 'Window'], ['طريق', 'Road'], ['صديق', 'Friend']]
      : lang === 'fr'
        ? [['livre', 'Book'], ['eau', 'Water'], ['école', 'School'], ['lune', 'Moon'], ['arbre', 'Tree'], ['fenêtre', 'Window'], ['route', 'Road'], ['ami', 'Friend']]
        : [['book', 'كتاب'], ['water', 'ماء'], ['school', 'مدرسة'], ['moon', 'قمر'], ['tree', 'شجرة'], ['window', 'نافذة'], ['road', 'طريق'], ['friend', 'صديق']];
    const pair = bank[Math.floor(Math.random() * bank.length)];
    return {
      prompt: pair[0],
      choices: shuffle(bank.map((item) => item[1])),
      answer: pair[1],
      hint: lang === 'ar' ? 'فكّر في معنى الكلمة في سياق يومي.' : lang === 'fr' ? 'Pense au sens du mot dans la vie quotidienne.' : 'Think of the word in an everyday context.',
      skill: 'vocabulary',
      difficulty,
    };
  }

  const start = 2 + Math.floor(Math.random() * (difficulty * 4));
  const step = 2 + Math.floor(Math.random() * (difficulty * 4));
  const answer = start + step * 4;
  const values = [start, start + step, start + step * 2, start + step * 3];
  return {
    prompt: `${values.join('  →  ')}  →  ?`,
    choices: shuffle([answer, answer + step, answer - step, answer + 2 * step].map(String)),
    answer: String(answer),
    hint: lang === 'ar' ? 'ابحث عن مقدار الزيادة الثابتة.' : lang === 'fr' ? 'Trouve l’écart constant.' : 'Find the constant step.',
    skill: 'logic',
    difficulty,
  };
}

export function scoreAnswer(question: GameQuestion, choice: string): GameResult {
  const correct = choice === question.answer;
  const xp = correct ? 10 + (question.difficulty - 1) * 5 : 0;
  return { correct, xp, skill: question.skill, difficulty: question.difficulty };
}
