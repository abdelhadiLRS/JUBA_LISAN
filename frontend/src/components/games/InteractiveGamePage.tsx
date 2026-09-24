'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { InteractiveGameBoard } from './InteractiveGameBoard'
import { completeGameSession, startGameSession, type InteractiveGameChallenge, type InteractiveGameTrace, type GameId } from '@/lib/games/persist'
import { useProgressStore } from '@/store/progress'

type Mode = 'memory' | 'matching' | 'ordering'
type Lang = 'ar' | 'fr' | 'en'

export function InteractiveGamePage({ mode }: { mode: Mode }) {
  const searchParams = useSearchParams()
  const [lang, setLang] = useState<Lang>('ar')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [dailyChallenge, setDailyChallenge] = useState(false)
  const [dailyChallengeDate, setDailyChallengeDate] = useState('')
  const [challenge, setChallenge] = useState<InteractiveGameChallenge>()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const [difficulty, setDifficulty] = useState(1)
  const setProgress = useProgressStore((state) => state.setProgress)

  useEffect(() => {
    const value = searchParams.get('lang')
    if (value === 'ar' || value === 'fr' || value === 'en') setLang(value)
    const rawDifficulty = Number(searchParams.get('difficulty'))
    if (Number.isInteger(rawDifficulty) && rawDifficulty >= 1 && rawDifficulty <= 3) setDifficulty(rawDifficulty)
  }, [searchParams])

  useEffect(() => {
    let cancelled = false
    setLoading(true); setError(false); setSessionId(null); setDailyChallenge(false); setDailyChallengeDate(''); setChallenge(undefined)
    void startGameSession(mode as GameId, lang, difficulty).then((session) => {
      if (cancelled) return
      setSessionId(session.session_id); setDailyChallenge(session.daily_challenge); setDailyChallengeDate(session.daily_challenge_date); setChallenge(session.interaction); setLoading(false)
    }).catch(() => { if (!cancelled) { setLoading(false); setError(true) } })
    return () => { cancelled = true }
  }, [mode, lang, difficulty])

  async function complete(trace: InteractiveGameTrace[]) {
    if (!sessionId) return false
    try {
      const server = await completeGameSession(sessionId, [], dailyChallenge, dailyChallengeDate, trace)
      setProgress({ streak: useProgressStore.getState().streak, xp: server.total_xp, skills: server.skills, gameStats: { gamesPlayed: server.games_played, questionsAnswered: server.questions_answered, correctAnswers: server.correct_answers, bestRoundScore: server.best_round_score, dailyChallengesCompleted: server.daily_challenges_completed, lastDailyChallengeDate: server.last_daily_challenge_date, currentCorrectStreak: server.current_correct_streak, bestCorrectStreak: server.best_correct_streak }, achievements: server.achievements as import('@/lib/games/achievements').AchievementId[] })
      return true
    } catch { return false }
  }

  return <main className="juba-games" dir={lang === 'ar' ? 'rtl' : 'ltr'}><div className="games-shell">
    <div className="interactive-language-bar" role="group" aria-label="Language">
      {(['ar', 'fr', 'en'] as const).map((value) => <button key={value} type="button" onClick={() => setLang(value)} className={lang === value ? 'active' : ''}>{value.toUpperCase()}</button>)}
    </div>
    {loading ? <p className="interactive-instruction">Loading challenge…</p> : error ? <div className="interactive-instruction interactive-error"><p>Unable to load the challenge.</p><button type="button" onClick={() => window.location.reload()}>Retry</button></div> : !challenge ? <p className="interactive-instruction">No challenge available.</p> : <InteractiveGameBoard mode={mode} lang={lang} challenge={challenge} onComplete={complete} />}
  </div></main>
}
