'use client';

import { useEffect, useMemo, useState } from 'react';
import './games.css';

type GameId = 'math' | 'words' | 'sequence';
type Lang = 'ar' | 'fr' | 'en';

type Question = {
  prompt: string;
  choices: string[];
  answer: string;
  hint: string;
};

const STORAGE_KEY = 'juba-edu-progress-v1';

const copy = {
  ar: {
    title: 'JUBA EDU', subtitle: 'تعلّم باللعب، وتقدّم كل يوم', points: 'النقاط', streak: 'سلسلة', level: 'المستوى',
    games: 'الألعاب التعليمية', math: 'تحدي الحساب', words: 'صيد الكلمات', sequence: 'أكمل النمط',
    mathDesc: 'عمليات حسابية قصيرة مع مكافآت فورية.', wordsDesc: 'طابق الكلمة مع معناها.', sequenceDesc: 'اكتشف الرقم التالي في السلسلة.',
    start: 'ابدأ اللعبة', next: 'السؤال التالي', correct: 'إجابة صحيحة!', wrong: 'ليست صحيحة',
    hint: 'تلميح', back: 'الألعاب', score: 'نتيجة الجولة', done: 'أحسنت! أكملت الجولة.',
    choose: 'اختر الإجابة الصحيحة', reset: 'إعادة التقدم', lang: 'اللغة',
  },
  fr: {
    title: 'JUBA EDU', subtitle: 'Apprendre en jouant, progresser chaque jour', points: 'Points', streak: 'Série', level: 'Niveau',
    games: 'Jeux éducatifs', math: 'Défi de calcul', words: 'Chasse aux mots', sequence: 'Complète la suite',
    mathDesc: 'De courts calculs avec récompenses immédiates.', wordsDesc: 'Associe le mot à sa signification.', sequenceDesc: 'Trouve le prochain nombre.',
    start: 'Commencer', next: 'Question suivante', correct: 'Bonne réponse !', wrong: 'Pas encore',
    hint: 'Indice', back: 'Jeux', score: 'Score de la partie', done: 'Bravo ! Partie terminée.',
    choose: 'Choisis la bonne réponse', reset: 'Réinitialiser', lang: 'Langue',
  },
  en: {
    title: 'JUBA EDU', subtitle: 'Learn through play. Improve every day.', points: 'Points', streak: 'Streak', level: 'Level',
    games: 'Educational games', math: 'Math challenge', words: 'Word hunt', sequence: 'Complete the pattern',
    mathDesc: 'Short calculations with instant rewards.', wordsDesc: 'Match each word with its meaning.', sequenceDesc: 'Find the next number in the sequence.',
    start: 'Start game', next: 'Next question', correct: 'Correct!', wrong: 'Not quite',
    hint: 'Hint', back: 'Games', score: 'Round score', done: 'Great job! Round complete.',
    choose: 'Choose the correct answer', reset: 'Reset progress', lang: 'Language',
  },
} as const;

function shuffle<T>(items: T[]): T[] {
  return [...items].sort(() => Math.random() - 0.5);
}

function buildQuestion(game: GameId, lang: Lang): Question {
  if (game === 'math') {
    const a = 2 + Math.floor(Math.random() * 18);
    const b = 2 + Math.floor(Math.random() * 18);
    const op = Math.random() > 0.5 ? '+' : '-';
    const answer = op === '+' ? a + b : a - b;
    const choices = shuffle([answer, answer + 1, answer - 1, answer + 2].map(String));
    return {
      prompt: `${a} ${op} ${b} = ?`, choices, answer: String(answer),
      hint: lang === 'ar' ? 'احسب بهدوء خطوة بخطوة.' : lang === 'fr' ? 'Calcule étape par étape.' : 'Work it out step by step.',
    };
  }

  if (game === 'words') {
    const bank = lang === 'ar'
      ? [['كتاب', 'Book'], ['ماء', 'Water'], ['مدرسة', 'School'], ['قمر', 'Moon'], ['شجرة', 'Tree']]
      : lang === 'fr'
        ? [['livre', 'Book'], ['eau', 'Water'], ['école', 'School'], ['lune', 'Moon'], ['arbre', 'Tree']]
        : [['book', 'كتاب'], ['water', 'ماء'], ['school', 'مدرسة'], ['moon', 'قمر'], ['tree', 'شجرة']];
    const pair = bank[Math.floor(Math.random() * bank.length)];
    const choices = shuffle(bank.map((item) => item[1]));
    return { prompt: pair[0], choices, answer: pair[1], hint: lang === 'ar' ? 'فكّر في معنى الكلمة.' : lang === 'fr' ? 'Pense au sens du mot.' : 'Think about the meaning.' };
  }

  const start = 2 + Math.floor(Math.random() * 6);
  const step = 2 + Math.floor(Math.random() * 5);
  const answer = start + step * 4;
  const values = [start, start + step, start + step * 2, start + step * 3];
  const choices = shuffle([answer, answer + step, answer - step, answer + 2 * step].map(String));
  return { prompt: `${values.join('  →  ')}  →  ?`, choices, answer: String(answer), hint: lang === 'ar' ? `ابحث عن مقدار الزيادة بين الأرقام.` : lang === 'fr' ? 'Trouve l’écart constant entre les nombres.' : 'Find the constant step between numbers.' };
}

export default function GamesPage() {
  const [lang, setLang] = useState<Lang>('ar');
  const [game, setGame] = useState<GameId | null>(null);
  const [question, setQuestion] = useState<Question | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [roundScore, setRoundScore] = useState(0);
  const [round, setRound] = useState(0);
  const [progress, setProgress] = useState({ points: 0, streak: 0, level: 1 });
  const t = copy[lang];

  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) setProgress(JSON.parse(saved));
    } catch {
      // Ignore invalid local progress and start fresh.
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }, [progress]);

  const direction = lang === 'ar' ? 'rtl' : 'ltr';
  const gameCards = useMemo(() => [
    { id: 'math' as const, title: t.math, desc: t.mathDesc, icon: '➗' },
    { id: 'words' as const, title: t.words, desc: t.wordsDesc, icon: '🔤' },
    { id: 'sequence' as const, title: t.sequence, desc: t.sequenceDesc, icon: '🧩' },
  ], [t]);

  function startGame(id: GameId) {
    setGame(id);
    setRound(0);
    setRoundScore(0);
    setSelected(null);
    setQuestion(buildQuestion(id, lang));
  }

  function answer(choice: string) {
    if (!question || selected) return;
    setSelected(choice);
    const correct = choice === question.answer;
    if (correct) {
      setRoundScore((value) => value + 10);
      setProgress((value) => ({
        points: value.points + 10,
        streak: value.streak + 1,
        level: Math.floor((value.points + 10) / 100) + 1,
      }));
    } else {
      setProgress((value) => ({ ...value, streak: 0 }));
    }
  }

  function next() {
    if (!game) return;
    if (round >= 4) {
      setGame(null);
      setQuestion(null);
      return;
    }
    setRound((value) => value + 1);
    setSelected(null);
    setQuestion(buildQuestion(game, lang));
  }

  function reset() {
    setProgress({ points: 0, streak: 0, level: 1 });
    setGame(null);
    setQuestion(null);
  }

  return (
    <main className="juba-games" dir={direction}>
      <section className="games-shell">
        <header className="games-header">
          <div>
            <div className="games-brand">{t.title}</div>
            <h1>{t.subtitle}</h1>
          </div>
          <div className="language-control">
            <span>{t.lang}</span>
            {(['ar', 'fr', 'en'] as Lang[]).map((value) => (
              <button key={value} className={lang === value ? 'active' : ''} onClick={() => setLang(value)}>{value.toUpperCase()}</button>
            ))}
          </div>
        </header>

        <section className="stats-grid" aria-label="progress">
          <div><span>⭐</span><strong>{progress.points}</strong><small>{t.points}</small></div>
          <div><span>🔥</span><strong>{progress.streak}</strong><small>{t.streak}</small></div>
          <div><span>🏆</span><strong>{progress.level}</strong><small>{t.level}</small></div>
        </section>

        {!game ? (
          <>
            <div className="section-heading"><h2>{t.games}</h2><button className="reset" onClick={reset}>{t.reset}</button></div>
            <section className="game-grid">
              {gameCards.map((card) => (
                <button key={card.id} className="game-card" onClick={() => startGame(card.id)}>
                  <span className="game-icon">{card.icon}</span>
                  <span className="game-title">{card.title}</span>
                  <span className="game-desc">{card.desc}</span>
                  <span className="start">{t.start} →</span>
                </button>
              ))}
            </section>
          </>
        ) : (
          <section className="play-card">
            <button className="back" onClick={() => setGame(null)}>← {t.back}</button>
            <div className="round-meta">{round + 1} / 5 · +10 XP</div>
            {question && <>
              <h2>{question.prompt}</h2>
              <p className="choose">{t.choose}</p>
              <div className="choices">
                {question.choices.map((choice) => {
                  const state = selected ? (choice === question.answer ? 'correct' : choice === selected ? 'wrong' : '') : '';
                  return <button key={choice} className={`choice ${state}`} onClick={() => answer(choice)}>{choice}</button>;
                })}
              </div>
              {selected && <div className={`feedback ${selected === question.answer ? 'good' : 'bad'}`}>
                <strong>{selected === question.answer ? t.correct : t.wrong}</strong>
                <span>{selected === question.answer ? '+10 XP' : `${t.hint}: ${question.hint}`}</span>
              </div>}
              {selected && <button className="next" onClick={next}>{round >= 4 ? t.done : t.next} →</button>}
            </>}
            <div className="round-score">{t.score}: <strong>{roundScore}</strong></div>
          </section>
        )}
      </section>
    </main>
  );
}
