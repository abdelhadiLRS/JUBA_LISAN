'use client'

import { useMemo, useState } from 'react'
import {
  ACHIEVEMENTS,
  type AchievementId,
} from '@/lib/games/achievements'
import {
  completeGameSession,
  startGameSession,
  type GameSessionQuestion,
  type GameId,
  type GameLanguage,
} from '@/lib/games/persist'
import { useProgressStore } from '@/store/progress'
import './games.css'

type Lang = GameLanguage
function getLocalDateKey() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}
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
    questions: 'الأسئلة', accuracy: 'الدقة', best: 'أفضل نتيجة', badges: 'الإنجازات', unlocked: 'مفتوح', newBadge: 'إنجاز جديد!', answered: 'تم تسجيل إجابتك.',
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
    gamesPlayed: 'Parties', questions: 'Questions', accuracy: 'Précision', best: 'Meilleur score', badges: 'Succès', unlocked: 'débloqué', newBadge: 'Nouveau succès !', answered: 'Réponse enregistrée.',
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
    gamesPlayed: 'Games', questions: 'Questions', accuracy: 'Accuracy', best: 'Best score', badges: 'Achievements', unlocked: 'unlocked', newBadge: 'New achievement!', answered: 'Answer recorded.',
  },
} as const

export default function GamesPage() {
  const [lang, setLang] = useState<Lang>('ar')
  const [game, setGame] = useState<GameId | null>(null)
  const [dailyMode, setDailyMode] = useState(false)
  const [question, setQuestion] = useState<GameSessionQuestion | null>(null)
  const [sessionQuestions, setSessionQuestions] = useState<GameSessionQuestion[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [answers, setAnswers] = useState<Array<{ question_id: string; choice: string }>>([])
  const [selected, setSelected] = useState<string | null>(null)
  const [roundScore, setRoundScore] = useState(0)
  const [round, setRound] = useState(0)
  const [newAchievements, setNewAchievements] = useState<AchievementId[]>([])
  const [dailyCompletedToday, setDailyCompletedToday] = useState(false)

  const {
    xp, streak, skills, gameStats, achievements, setProgress,
    resetGameProgress,
  } = useProgressStore()

  const level = Math.floor(xp / 100) + 1
  const t = copy[lang]
  const today = getLocalDateKey()
  // Keep the daily rotation aligned with the server: Date#getDay() is
  // Sunday=0..Saturday=6, and the server normalizes Python's weekday() to
  // the same numbering before applying the six-game rotation.
  const dayIndex = new Date(`${today}T00:00:00`).getDay()
  const dailyGame = DAILY_GAMES[dayIndex % DAILY_GAMES.length]
  const accuracy = gameStats.questionsAnswered
    ? Math.round((gameStats.correctAnswers / gameStats.questionsAnswered) * 100)
    : 0

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

  async function startGame(id: GameId, daily = false) {
    if (daily && dailyCompletedToday) return
    try {
      const session = await startGameSession(id, lang, level)
      setGame(id)
      setDailyMode(daily)
      setRound(0)
      setRoundScore(0)
      setSelected(null)
      setAnswers([])
      setSessionId(session.session_id)
      setSessionQuestions(session.questions)
      setNewAchievements([])
      setQuestion(session.questions[0] ?? null)
    } catch {
      setGame(null)
      setQuestion(null)
      setSessionId(null)
    }
  }

  function answer(choice: string) {
    if (!question || selected) return
    setSelected(choice)
    setAnswers((current) => [...current, { question_id: question.id, choice }])
  }

  async function finishRound() {
    if (!sessionId) return
    const previousAchievements = new Set(achievements)
    try {
      const server = await completeGameSession(
        sessionId,
        answers,
        dailyMode,
        dailyMode ? today : '',
      )
      const fresh = (server.new_achievements as AchievementId[]).filter(
        (id) => !previousAchievements.has(id)
      )
      if (fresh.length) setNewAchievements(fresh)
      if (dailyMode) setDailyCompletedToday(true)
      setRoundScore(server.round_score)
      setProgress({
        streak,
        xp: server.total_xp,
        skills: server.skills,
        gameStats: {
          gamesPlayed: server.games_played,
          questionsAnswered: server.questions_answered,
          correctAnswers: server.correct_answers,
          bestRoundScore: server.best_round_score,
          dailyChallengesCompleted: server.daily_challenges_completed,
          lastDailyChallengeDate: server.last_daily_challenge_date,
          currentCorrectStreak: server.current_correct_streak,
          bestCorrectStreak: server.best_correct_streak,
        },
        achievements: server.achievements as AchievementId[],
      })
    } catch {
      return
    }
  }

  function next() {
    if (!game || !question) return
    if (round >= ROUND_SIZE - 1) {
      void finishRound()
      setGame(null)
      setDailyMode(false)
      setQuestion(null)
      setSessionId(null)
      return
    }
    const nextRound = round + 1
    setRound(nextRound)
    setSelected(null)
    setQuestion(sessionQuestions[nextRound] ?? null)
  }

  function reset() {
    resetGameProgress()
    setGame(null)
    setDailyMode(false)
    setQuestion(null)
    setSessionId(null)
    setSessionQuestions([])
    setAnswers([])
    setRound(0)
    setRoundScore(0)
    setSelected(null)
    setNewAchievements([])
    setDailyCompletedToday(false)
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
            <button className={`daily-challenge${dailyCompletedToday ? ' completed' : ''}`} onClick={() => startGame(dailyGame, true)} disabled={dailyCompletedToday} aria-disabled={dailyCompletedToday}>
              <span className="daily-icon">📅</span>
              <span><strong>{t.daily}</strong><small>{t.dailyDesc}</small></span>
              <span className="start">{dailyCompletedToday ? '✓' : t.start} {dailyCompletedToday ? '' : '→'}</span>
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
                    const state = selected === choice ? 'selected' : ''
                    return (
                      <button key={choice} className={`choice ${state}`} onClick={() => answer(choice)}>
                        {choice}
                      </button>
                    )
                  })}
                </div>
                {selected && (
                  <div className="feedback good">
                    <strong>{t.answered}</strong>
                    <span>{question.hint}</span>
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
