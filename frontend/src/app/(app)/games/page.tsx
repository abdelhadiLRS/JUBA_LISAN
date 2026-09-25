'use client'

import { useEffect, useMemo, useState } from 'react'
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
const DAILY_GAMES: GameId[] = ['matching', 'quick_choice', 'sentence_builder', 'listen_choose', 'spelling', 'memory']
const ROUND_SIZE = 5

const copy = {
  ar: {
    title: 'JUBA LISAN',
    subtitle: 'تعلّم باللعب، وتقدّم كل يوم',
    points: 'النقاط', streak: 'سلسلة', level: 'المستوى', games: 'الألعاب التعليمية',
    daily: 'تحدي اليوم', dailyDesc: 'تحدٍ واحد ثابت يوميًا. أكمله لتحصل على XP وتبني عادتك التعليمية.',
    wordMatch: 'مطابقة الكلمات', quickChoice: 'اختيار سريع', sentenceBuilder: 'بناء الجملة',
    listenChoose: 'استمع واختر', spelling: 'تحدي الإملاء', memory: 'بطاقات الذاكرة',
    wordMatchDesc: 'طابق الكلمة مع ترجمتها الصحيحة.', quickChoiceDesc: 'اختر الإجابة قبل انتهاء الوقت.',
    sentenceBuilderDesc: 'رتّب الكلمات لبناء جملة صحيحة.', listenChooseDesc: 'استمع إلى الكلمة ثم اخترها.',
    spellingDesc: 'اكتب الكلمة المطلوبة من التلميح.', memoryDesc: 'اكشف البطاقات وطابق الأزواج الحقيقية.',
    start: 'ابدأ اللعبة', next: 'السؤال التالي', correct: 'إجابة صحيحة!', wrong: 'ليست صحيحة',
    hint: 'تلميح', back: 'الألعاب', score: 'نتيجة الجولة', done: 'أحسنت! أكملت الجولة.', choose: 'اختر الإجابة الصحيحة',
lang: 'اللغة', xp: 'XP', skills: 'المهارات', stats: 'إحصائياتك', gamesPlayed: 'الألعاب',
    questions: 'الأسئلة', accuracy: 'الدقة', best: 'أفضل نتيجة', badges: 'الإنجازات', unlocked: 'مفتوح', newBadge: 'إنجاز جديد!', answered: 'تم تسجيل إجابتك.',
  },
  fr: {
    title: 'JUBA LISAN', subtitle: 'Apprendre en jouant, progresser chaque jour', points: 'Points', streak: 'Série', level: 'Niveau',
    games: 'Jeux éducatifs', daily: 'Défi du jour', dailyDesc: 'Un défi fixe chaque jour pour gagner de l’XP et construire une habitude.',
    wordMatch: 'Association de mots', quickChoice: 'Choix rapide', sentenceBuilder: 'Constructeur de phrases',
    listenChoose: 'Écoute et choisis', spelling: 'Défi d’orthographe', memory: 'Cartes mémoire',
    wordMatchDesc: 'Associe chaque mot à sa bonne traduction.', quickChoiceDesc: 'Choisis avant la fin du temps.',
    sentenceBuilderDesc: 'Remets les mots dans le bon ordre.', listenChooseDesc: 'Écoute le mot puis choisis-le.',
    spellingDesc: 'Écris le mot demandé à partir de l’indice.', memoryDesc: 'Retourne les cartes et forme les vraies paires.', start: 'Commencer', next: 'Question suivante',
    correct: 'Bonne réponse !', wrong: 'Pas encore', hint: 'Indice', back: 'Jeux', score: 'Score de la partie', done: 'Bravo ! Partie terminée.',
    choose: 'Choisis la bonne réponse', lang: 'Langue', xp: 'XP', skills: 'Compétences', stats: 'Tes statistiques',
    gamesPlayed: 'Parties', questions: 'Questions', accuracy: 'Précision', best: 'Meilleur score', badges: 'Succès', unlocked: 'débloqué', newBadge: 'Nouveau succès !', answered: 'Réponse enregistrée.',
  },
  en: {
    title: 'JUBA LISAN', subtitle: 'Learn through play. Improve every day.', points: 'Points', streak: 'Streak', level: 'Level',
    games: 'Educational games', daily: 'Daily Challenge', dailyDesc: 'One consistent challenge each day. Complete it to earn XP and build your habit.',
    wordMatch: 'Word Match', quickChoice: 'Quick Choice', sentenceBuilder: 'Sentence Builder',
    listenChoose: 'Listen & Choose', spelling: 'Spelling Challenge', memory: 'Memory Cards',
    wordMatchDesc: 'Match each word with its correct translation.', quickChoiceDesc: 'Choose before the timer runs out.',
    sentenceBuilderDesc: 'Arrange the words to build a correct sentence.', listenChooseDesc: 'Listen to the word and choose it.',
    spellingDesc: 'Type the word requested by the clue.', memoryDesc: 'Reveal cards and match the real pairs.', start: 'Start game', next: 'Next question',
    correct: 'Correct!', wrong: 'Not quite', hint: 'Hint', back: 'Games', score: 'Round score', done: 'Great job! Round complete.',
    choose: 'Choose the correct answer', lang: 'Language', xp: 'XP', skills: 'Skills', stats: 'Your stats',
    gamesPlayed: 'Games', questions: 'Questions', accuracy: 'Accuracy', best: 'Best score', badges: 'Achievements', unlocked: 'unlocked', newBadge: 'New achievement!', answered: 'Answer recorded.',
  },
} as const

export default function GamesPage() {
  const [lang, setLang] = useState<Lang>('ar')
  const [game, setGame] = useState<GameId | null>(null)
  const [dailyMode, setDailyMode] = useState(false)
  const [dailyChallengeDate, setDailyChallengeDate] = useState('')
  const [question, setQuestion] = useState<GameSessionQuestion | null>(null)
  const [sessionQuestions, setSessionQuestions] = useState<GameSessionQuestion[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [answers, setAnswers] = useState<Array<{ question_id: string; choice: string }>>([])
  const [selected, setSelected] = useState<string | null>(null)
  const [roundScore, setRoundScore] = useState(0)
  const [round, setRound] = useState(0)
  const [newAchievements, setNewAchievements] = useState<AchievementId[]>([])
  const [inputValue, setInputValue] = useState('')
  const [timeLeft, setTimeLeft] = useState(8)

  const {
    xp, streak, skills, gameStats, achievements, setProgress,
  } = useProgressStore()

  const level = Math.floor(xp / 100) + 1
  const t = copy[lang]
  const today = getLocalDateKey()
  const dailyCompletedToday = gameStats.lastDailyChallengeDate === today
  // The client mirrors only the deterministic display rotation; it never grants rewards.
  // Sunday=0..Saturday=6, and the server normalizes Python's weekday() to
  // the same numbering before applying the six-game rotation.
  const dayIndex = new Date(`${today}T00:00:00`).getDay()
  const dailyGame = DAILY_GAMES[dayIndex % DAILY_GAMES.length]
  const accuracy = gameStats.questionsAnswered
    ? Math.round((gameStats.correctAnswers / gameStats.questionsAnswered) * 100)
    : 0

  const direction = lang === 'ar' ? 'rtl' : 'ltr'

  function difficultyForGame(id: GameId) {
    const skill = id === 'matching' || id === 'quick_choice' ? 'vocabulary'
      : id === 'listen_choose' ? 'listening'
      : id === 'spelling' ? 'writing'
      : id === 'sentence_builder' ? 'grammar'
      : 'memory'
    const mastery = skills[skill] ?? 0
    if (mastery < 0.4) return 1
    if (mastery < 0.75) return 2
    return 3
  }
  const gameCards = useMemo(
    () => [
      { id: 'matching' as const, title: t.wordMatch, desc: t.wordMatchDesc, icon: '🔗' },
      { id: 'quick_choice' as const, title: t.quickChoice, desc: t.quickChoiceDesc, icon: '⚡' },
      { id: 'sentence_builder' as const, title: t.sentenceBuilder, desc: t.sentenceBuilderDesc, icon: '🧩' },
      { id: 'listen_choose' as const, title: t.listenChoose, desc: t.listenChooseDesc, icon: '🎧' },
      { id: 'spelling' as const, title: t.spelling, desc: t.spellingDesc, icon: '✍️' },
      { id: 'memory' as const, title: t.memory, desc: t.memoryDesc, icon: '🧠' },
    ],
    [t]
  )

  async function startGame(id: GameId, daily = false) {
    if (daily && dailyCompletedToday) return

    // Interactive games have their own board and completion flow. The generic
    // question renderer expects a non-interactive question payload, so route
    // these game types to their dedicated pages instead of opening an empty
    // round shell.
    if (id === 'memory' || id === 'matching' || id === 'sentence_builder') {
      const route = id === 'sentence_builder' ? 'sentence-builder' : id
      const difficulty = difficultyForGame(id)
      window.location.assign(`/games/${route}?lang=${lang}&difficulty=${difficulty}`)
      return
    }

    try {
      // A game session is persisted against the active study plan. Avoid
      // sending a request that can only return 404 when a learner has not
      // created a plan yet; send them to plan setup instead.
      const planResponse = await fetch('/api/study-plan/current', {
        credentials: 'include',
        cache: 'no-store',
      })
      if (!planResponse.ok) {
        window.location.assign('/plan')
        return
      }
      const plan = await planResponse.json().catch(() => null)
      if (!plan || typeof plan !== 'object' || !('id' in plan)) {
        window.location.assign('/plan')
        return
      }

      const session = await startGameSession(id, lang, difficultyForGame(id))
      setGame(id)
      setDailyMode(session.daily_challenge)
      setDailyChallengeDate(session.daily_challenge_date)
      setRound(0)
      setRoundScore(0)
      setSelected(null)
      setInputValue('')
      setTimeLeft(id === 'quick_choice' ? 8 : 0)
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

  function submitTextAnswer() {
    if (!question || selected || !inputValue.trim()) return
    setSelected(inputValue.trim())
    setAnswers((current) => [...current, { question_id: question.id, choice: inputValue.trim() }])
  }

  useEffect(() => {
    if (!game || !question || selected || game !== 'quick_choice') return
    setTimeLeft(8)
    const timer = window.setInterval(() => {
      setTimeLeft((value) => {
        if (value <= 1) {
          window.clearInterval(timer)
          setSelected('__timeout__')
          setAnswers((current) => [...current, { question_id: question.id, choice: '__timeout__' }])
          return 0
        }
        return value - 1
      })
    }, 1000)
    return () => window.clearInterval(timer)
  }, [game, question, selected])

  function playAudio() {
    if (!question?.audio_text || typeof window === 'undefined' || !('speechSynthesis' in window)) return
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(question.audio_text)
    utterance.lang = question.audio_language || 'en-GB'
    utterance.rate = 0.9
    window.speechSynthesis.speak(utterance)
  }

  async function finishRound() {
    if (!sessionId) return
    const previousAchievements = new Set(achievements)
    try {
      const server = await completeGameSession(
        sessionId,
        answers,
        dailyMode,
        dailyMode ? dailyChallengeDate : '',
      )
      const fresh = (server.new_achievements as AchievementId[]).filter(
        (id) => !previousAchievements.has(id)
      )
      if (fresh.length) setNewAchievements(fresh)
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
      setDailyChallengeDate('')
      setQuestion(null)
      setSessionId(null)
      return
    }
    const nextRound = round + 1
    setRound(nextRound)
    setSelected(null)
    setQuestion(sessionQuestions[nextRound] ?? null)
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
              <button type="button" key={value} className={lang === value ? 'active' : ''} onClick={() => setLang(value)}>
                {value.toUpperCase()}
              </button>
            ))}
          </div>
        </header>

        <section className="stats-grid" aria-label={t.stats}>
          <div><span>⭐</span><strong>{xp}</strong><small>{t.points}</small></div>
          <div><span>🔥</span><strong>{streak}</strong><small>{t.streak}</small></div>
          <div><span>🏆</span><strong>{level}</strong><small>{t.level}</small></div>
        </section>

        {!game ? (
          <>
            <div className="achievement-toast" style={{ display: newAchievements.length ? 'block' : 'none' }}>
              🏅 <strong>{t.newBadge}</strong> {newAchievements.map((id) => ACHIEVEMENTS[id].title).join(' · ')}
            </div>
            <button type="button" className={`daily-challenge${dailyCompletedToday ? ' completed' : ''}`} onClick={() => startGame(dailyGame, true)} disabled={dailyCompletedToday} aria-disabled={dailyCompletedToday}>
              <span className="daily-icon">📅</span>
              <span><strong>{t.daily}</strong><small>{t.dailyDesc}</small></span>
              <span className="start">{dailyCompletedToday ? '✓' : t.start} {dailyCompletedToday ? '' : '→'}</span>
            </button>

            <div className="section-heading">
              <h2>{t.games}</h2>
            </div>

            <section className="game-grid">
              {gameCards.map((card) => (
                <button type="button" key={card.id} className="game-card" onClick={() => startGame(card.id)}>
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
            <button type="button" className="back" onClick={() => { setGame(null); setDailyMode(false) }}>← {t.back}</button>
            <div className="round-meta">{dailyMode ? `📅 ${t.daily} · ` : ''}{round + 1} / {ROUND_SIZE} · +XP</div>
            {question && (
              <>
                <h2 style={{ whiteSpace: 'pre-line' }}>{question.prompt}</h2>
                {game === 'quick_choice' && !selected && <div className="quick-timer" aria-live="polite">⏱ {timeLeft}s</div>}
                {game === 'listen_choose' && (
                  <button type="button" className="audio-play" onClick={playAudio}>🎧 {lang === 'ar' ? 'تشغيل الصوت' : lang === 'fr' ? 'Écouter' : 'Play audio'}</button>
                )}
                {question.input_mode === 'text' ? (
                  <form className="spelling-form" onSubmit={(event) => { event.preventDefault(); submitTextAnswer() }}>
                    <input value={inputValue} onChange={(event) => setInputValue(event.target.value)} placeholder={lang === 'ar' ? 'اكتب الإجابة' : lang === 'fr' ? 'Écris ta réponse' : 'Type your answer'} autoComplete="off" disabled={Boolean(selected)} />
                    <button type="submit" className="next" disabled={Boolean(selected) || !inputValue.trim()}>{lang === 'ar' ? 'تحقق' : lang === 'fr' ? 'Vérifier' : 'Check'}</button>
                  </form>
                ) : (
                  <>
                    <p className="choose">{t.choose}</p>
                    <div className="choices">
                      {question.choices.map((choice) => {
                        const state = selected === choice ? 'selected' : ''
                        return (
                          <button type="button" key={choice} className={`choice ${state}`} onClick={() => answer(choice)} disabled={Boolean(selected)}>
                            {choice}
                          </button>
                        )
                      })}
                    </div>
                  </>
                )}
                {selected && (
                  <div className="feedback good">
                    <strong>{selected === '__timeout__' ? '⏱ Time!' : t.answered}</strong>
                    <span>{question.hint}</span>
                  </div>
                )}
                {selected && <button type="button" className="next" onClick={next}>{round >= ROUND_SIZE - 1 ? t.done : t.next} →</button>}
              </>
            )}
            <div className="round-score">{t.score}: <strong>{roundScore}</strong></div>
          </section>
        )}
      </section>
    </main>
  )
}
