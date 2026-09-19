'use client'

import { useEffect, useMemo, useState } from 'react'
import {
  buildDailyQuestion,
  buildQuestion,
  scoreAnswer,
  type GameId,
  type GameLanguage,
  type GameQuestion,
} from '@/lib/games/engine'
import {
  ACHIEVEMENTS,
  evaluateAchievements,
  emptyGameStats,
  type AchievementId,
} from '@/lib/games/achievements'
import { useProgressStore } from '@/store/progress'
import './games.css'

type Lang = GameLanguage
type SavedProgress = {
  points?: number
  streak?: number
  skills?: Record<string, number>
  gameStats?: ReturnType<typeof emptyGameStats>
  achievements?: AchievementId[]
}

const STORAGE_KEY = 'juba-edu-progress-v2'
const DAILY_GAMES: GameId[] = ['math', 'words', 'sequence', 'memory', 'matching', 'ordering']
const ROUND_SIZE = 5

const copy = {
  ar: {
    title: 'JUBA EDU',
    subtitle: 'تعلّم باللعب، وتقدّم كل يوم',
    points: 'النقاط', streak: 'سلسلة', level: 'المستوى', games: 'الألعاب التعليمية',
    daily: 'تحدي اليوم', dailyDesc: 'تحدٍ واحد ثابت يوميًا. أكمله لتحصل على XP وتبني عادتك التعليمية.',
    math: 'تحدي الحساب', words: 'صيد الكلمات', sequence: 'أكمل النمط', memory: 'اختبار الذاكرة',
    matching: 'لعبة المطابقة', ordering: 'لعبة الترتيب',
    mathDesc: 'عمليات حسابية قصيرة مع مكافآت فورية.', wordsDesc: 'طابق الكلمة مع معناها.',
    sequenceDesc: 'اكتشف الرقم التالي في السلسلة.', memoryDesc: 'تذكّر ترتيب العناصر واختره من البدائل.',
    matchingDesc: 'طابق الكلمة مع ترجمتها الصحيحة.', orderingDesc: 'رتّب العناصر بالترتيب الصحيح.',
    start: 'ابدأ اللعبة', next: 'السؤال التالي', correct: 'إجابة صحيحة!', wrong: 'ليست صحيحة',
    hint: 'تلميح', back: 'الألعاب', score: 'نتيجة الجولة', done: 'أحسنت! أكملت الجولة.', choose: 'اختر الإجابة الصحيحة',
    reset: 'إعادة التقدم', lang: 'اللغة', xp: 'XP', skills: 'المهارات', stats: 'إحصائياتك', gamesPlayed: 'الألعاب',
    questions: 'الأسئلة', accuracy: 'الدقة', best: 'أفضل نتيجة', badges: 'الإنجازات', unlocked: 'مفتوح', newBadge: 'إنجاز جديد!',
  },
  fr: {
    title: 'JUBA EDU', subtitle: 'Apprendre en jouant, progresser chaque jour', points: 'Points', streak: 'Série', level: 'Niveau',
    games: 'Jeux éducatifs', daily: 'Défi du jour', dailyDesc: 'Un défi fixe chaque jour pour gagner de l’XP et construire une habitude.',
    math: 'Défi de calcul', words: 'Chasse aux mots', sequence: 'Complète la suite', memory: 'Défi mémoire',
    matching: 'Jeu d’association', ordering: 'Jeu de classement', mathDesc: 'De courts calculs avec récompenses immédiates.',
    wordsDesc: 'Associe le mot à sa signification.', sequenceDesc: 'Trouve le prochain nombre.', memoryDesc: 'Mémorise l’ordre et retrouve la bonne séquence.',
    matchingDesc: 'Associe le mot à sa bonne traduction.', orderingDesc: 'Classe les éléments dans le bon ordre.', start: 'Commencer', next: 'Question suivante',
    correct: 'Bonne réponse !', wrong: 'Pas encore', hint: 'Indice', back: 'Jeux', score: 'Score de la partie', done: 'Bravo ! Partie terminée.',
    choose: 'Choisis la bonne réponse', reset: 'Réinitialiser', lang: 'Langue', xp: 'XP', skills: 'Compétences', stats: 'Tes statistiques',
    gamesPlayed: 'Parties', questions: 'Questions', accuracy: 'Précision', best: 'Meilleur score', badges: 'Succès', unlocked: 'débloqué', newBadge: 'Nouveau succès !',
  },
  en: {
    title: 'JUBA EDU', subtitle: 'Learn through play. Improve every day.', points: 'Points', streak: 'Streak', level: 'Level',
    games: 'Educational games', daily: 'Daily Challenge', dailyDesc: 'One consistent challenge each day. Complete it to earn XP and build your habit.',
    math: 'Math challenge', words: 'Word hunt', sequence: 'Complete the pattern', memory: 'Memory challenge',
    matching: 'Matching game', ordering: 'Ordering game', mathDesc: 'Short calculations with instant rewards.', wordsDesc: 'Match each word with its meaning.',
    sequenceDesc: 'Find the next number in the sequence.', memoryDesc: 'Remember the order and choose the matching sequence.',
    matchingDesc: 'Match each word with the correct translation.', orderingDesc: 'Put the items in the correct order.', start: 'Start game', next: 'Next question',
    correct: 'Correct!', wrong: 'Not quite', hint: 'Hint', back: 'Games', score: 'Round score', done: 'Great job! Round complete.',
    choose: 'Choose the correct answer', reset: 'Reset progress', lang: 'Language', xp: 'XP', skills: 'Skills', stats: 'Your stats',
    gamesPlayed: 'Games', questions: 'Questions', accuracy: 'Accuracy', best: 'Best score', badges: 'Achievements', unlocked: 'unlocked', newBadge: 'New achievement!',
  },
} as const

export default function GamesPage() {
  const [lang, setLang] = useState<Lang>('ar')
  const [game, setGame] = useState<GameId | null>(null)
  const [dailyMode, setDailyMode] = useState(false)
  const [question, setQuestion] = useState<GameQuestion | null>(null)
  const [selected, setSelected] = useState<string | null>(null)
  const [roundScore, setRoundScore] = useState(0)
  const [roundCorrect, setRoundCorrect] = useState(0)
  const [round, setRound] = useState(0)
  const [hydrated, setHydrated] = useState(false)
  const [newAchievements, setNewAchievements] = useState<AchievementId[]>([])

  const {
    xp, streak, skills, gameStats, achievements, setProgress,
    addGameXP, recordGameAttempt, completeGame, unlockAchievements, resetGameProgress,
  } = useProgressStore()

  const level = Math.floor(xp / 100) + 1
  const t = copy[lang]
  const today = new Date().toISOString().slice(0, 10)
  const dayIndex = new Date(`${today}T00:00:00Z`).getUTCDay()
  const dailyGame = DAILY_GAMES[dayIndex % DAILY_GAMES.length]
  const accuracy = gameStats.questionsAnswered
    ? Math.round((gameStats.correctAnswers / gameStats.questionsAnswered) * 100)
    : 0

  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved) {
        const parsed = JSON.parse(saved) as SavedProgress
        setProgress({
          streak: parsed.streak ?? 0,
          xp: parsed.points ?? 0,
          skills: parsed.skills ?? {},
          gameStats: parsed.gameStats,
          achievements: parsed.achievements,
        })
      }
    } catch {
      // Ignore malformed local progress and keep the in-memory defaults.
    } finally {
      setHydrated(true)
    }
  }, [setProgress])

  useEffect(() => {
    if (!hydrated) return
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ points: xp, streak, level, skills, gameStats, achievements })
    )
  }, [hydrated, xp, streak, level, skills, gameStats, achievements])

  const direction = lang === 'ar' ? 'rtl' : 'ltr'
  const gameCards = useMemo(
    () => [
      { id: 'math' as const, title: t.math, desc: t.mathDesc, icon: '➗' },
      { id: 'words' as const, title: t.words, desc: t.wordsDesc, icon: '🔤' },
      { id: 'sequence' as const, title: t.sequence, desc: t.sequenceDesc, icon: '🧩' },
      { id: 'memory' as const, title: t.memory, desc: t.memoryDesc, icon: '🧠' },
      { id: 'matching' as const, title: t.matching, desc: t.matchingDesc, icon: '🔗' },
      { id: 'ordering' as const, title: t.ordering, desc: t.orderingDesc, icon: '🔢' },
    ],
    [t]
  )

  function startGame(id: GameId, daily = false) {
    setGame(id)
    setDailyMode(daily)
    setRound(0)
    setRoundScore(0)
    setRoundCorrect(0)
    setSelected(null)
    setNewAchievements([])
    setQuestion(
      daily
        ? buildDailyQuestion(id, lang, level, today, 0)
        : buildQuestion(id, lang, level)
    )
  }

  function answer(choice: string) {
    if (!question || selected) return
    setSelected(choice)
    const result = scoreAnswer(question, choice)
    if (result.correct) {
      setRoundScore((value) => value + result.xp)
      setRoundCorrect((value) => value + 1)
    }
    addGameXP(result.xp, result.skill, result.correct)
    recordGameAttempt(result.correct)
  }

  function finishRound() {
    const perfect = roundCorrect === ROUND_SIZE
    const projectedStats = {
      ...gameStats,
      gamesPlayed: gameStats.gamesPlayed + 1,
      bestRoundScore: Math.max(gameStats.bestRoundScore, roundScore),
      dailyChallengesCompleted:
        gameStats.dailyChallengesCompleted +
        (dailyMode && gameStats.lastDailyChallengeDate !== today ? 1 : 0),
      lastDailyChallengeDate:
        dailyMode && gameStats.lastDailyChallengeDate !== today
          ? today
          : gameStats.lastDailyChallengeDate,
      currentCorrectStreak: gameStats.currentCorrectStreak,
      bestCorrectStreak: Math.max(
        gameStats.bestCorrectStreak,
        gameStats.currentCorrectStreak ?? 0
      ),
    }
    const unlocked = evaluateAchievements(
      {
        xp: xp + roundScore,
        skills,
        stats: projectedStats,
        roundScore,
        perfectRound: perfect,
        dailyChallengeCompleted: dailyMode,
      },
      achievements
    )
    const fresh = unlocked.filter((id) => !achievements.includes(id))
    completeGame(roundScore, dailyMode, today)
    if (fresh.length) {
      unlockAchievements(fresh)
      setNewAchievements(fresh)
    }
  }

  function next() {
    if (!game) return
    if (round >= ROUND_SIZE - 1) {
      finishRound()
      setGame(null)
      setDailyMode(false)
      setQuestion(null)
      return
    }
    const nextRound = round + 1
    setRound(nextRound)
    setSelected(null)
    setQuestion(
      dailyMode
        ? buildDailyQuestion(game, lang, level, today, nextRound)
        : buildQuestion(game, lang, level)
    )
  }

  function reset() {
    resetGameProgress()
    setGame(null)
    setDailyMode(false)
    setQuestion(null)
    setRound(0)
    setRoundScore(0)
    setRoundCorrect(0)
    setSelected(null)
    setNewAchievements([])
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
              <button key={value} className={lang === value ? 'active' : ''} onClick={() => setLang(value)}>
                {value.toUpperCase()}
              </button>
            ))}
          </div>
        </header>

        <section className="stats-grid" aria-label="progress">
          <div><span>⭐</span><strong>{xp}</strong><small>{t.points}</small></div>
          <div><span>🔥</span><strong>{streak}</strong><small>{t.streak}</small></div>
          <div><span>🏆</span><strong>{level}</strong><small>{t.level}</small></div>
        </section>

        {!game ? (
          <>
            <div className="achievement-toast" style={{ display: newAchievements.length ? 'block' : 'none' }}>
              🏅 <strong>{t.newBadge}</strong> {newAchievements.map((id) => ACHIEVEMENTS[id].title).join(' · ')}
            </div>
            <button className="daily-challenge" onClick={() => startGame(dailyGame, true)}>
              <span className="daily-icon">📅</span>
              <span><strong>{t.daily}</strong><small>{t.dailyDesc}</small></span>
              <span className="start">{t.start} →</span>
            </button>

            <div className="section-heading">
              <h2>{t.games}</h2>
              <button className="reset" onClick={reset}>{t.reset}</button>
            </div>

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

            <section className="games-dashboard">
              <div className="games-panel">
                <h3>{t.stats}</h3>
                <div className="mini-stats">
                  <span><b>{gameStats.gamesPlayed}</b>{t.gamesPlayed}</span>
                  <span><b>{gameStats.questionsAnswered}</b>{t.questions}</span>
                  <span><b>{accuracy}%</b>{t.accuracy}</span>
                  <span><b>{gameStats.bestRoundScore}</b>{t.best}</span>
                </div>
              </div>
              <div className="games-panel">
                <h3>{t.badges}</h3>
                <div className="badges">
                  {Object.entries(ACHIEVEMENTS).map(([id, badge]) => (
                    <span
                      key={id}
                      className={achievements.includes(id as AchievementId) ? 'badge unlocked' : 'badge'}
                      title={badge.description}
                    >
                      🏅 {badge.title}{achievements.includes(id as AchievementId) ? ` · ${t.unlocked}` : ''}
                    </span>
                  ))}
                </div>
              </div>
            </section>

            <div className="games-skill-summary">
              <strong>{t.skills}</strong>
              {Object.entries(skills).map(([skill, value]) => (
                <span key={skill}>{skill}: {Math.round(value * 100)}%</span>
              ))}
            </div>
          </>
        ) : (
          <section className="play-card">
            <button className="back" onClick={() => { setGame(null); setDailyMode(false) }}>← {t.back}</button>
            <div className="round-meta">{dailyMode ? `📅 ${t.daily} · ` : ''}{round + 1} / {ROUND_SIZE} · +XP</div>
            {question && (
              <>
                <h2 style={{ whiteSpace: 'pre-line' }}>{question.prompt}</h2>
                <p className="choose">{t.choose}</p>
                <div className="choices">
                  {question.choices.map((choice) => {
                    const state = selected
                      ? choice === question.answer
                        ? 'correct'
                        : choice === selected
                          ? 'wrong'
                          : ''
                      : ''
                    return (
                      <button key={choice} className={`choice ${state}`} onClick={() => answer(choice)}>
                        {choice}
                      </button>
                    )
                  })}
                </div>
                {selected && (
                  <div className={`feedback ${selected === question.answer ? 'good' : 'bad'}`}>
                    <strong>{selected === question.answer ? t.correct : t.wrong}</strong>
                    <span>
                      {selected === question.answer
                        ? `+${scoreAnswer(question, selected).xp} ${t.xp}`
                        : `${t.hint}: ${question.hint}`}
                    </span>
                  </div>
                )}
                {selected && <button className="next" onClick={next}>{round >= ROUND_SIZE - 1 ? t.done : t.next} →</button>}
              </>
            )}
            <div className="round-score">{t.score}: <strong>{roundScore}</strong></div>
          </section>
        )}
      </section>
    </main>
  )
}
