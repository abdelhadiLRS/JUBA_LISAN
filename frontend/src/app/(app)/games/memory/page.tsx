'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { InteractiveGameBoard } from '@/components/games/InteractiveGameBoard'
import '@/components/games/interactive-games.css'
import { completeGameSession, startGameSession, type InteractiveGameChallenge, type InteractiveGameTrace } from '@/lib/games/persist'
import { useProgressStore } from '@/store/progress'

type Lang = 'ar' | 'fr' | 'en'

export default function MemoryGamePage() {
  const searchParams = useSearchParams()
  const [lang, setLang] = useState<Lang>('ar')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [challenge, setChallenge] = useState<InteractiveGameChallenge>()
  const [loading, setLoading] = useState(true)
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
    setLoading(true)
    setSessionId(null)
    setChallenge(undefined)
    void startGameSession('memory', lang, difficulty).then((session) => {
      if (cancelled) return
      setSessionId(session.session_id)
      setChallenge(session.interaction)
      setLoading(false)
    }).catch(() => {
      if (!cancelled) setLoading(false)
    })
    return () => { cancelled = true }
  }, [lang, difficulty])

  async function complete(trace: InteractiveGameTrace[]) {
    if (!sessionId) return false
    try {
      const server = await completeGameSession(sessionId, [], false, '', trace)
      setProgress({
        streak: useProgressStore.getState().streak,
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
        achievements: server.achievements as import('@/lib/games/achievements').AchievementId[],
      })
      return true
    } catch {
      return false
    }
  }

  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-8">
      <div className="mb-4 flex flex-wrap items-center gap-2">
        {(['ar', 'fr', 'en'] as const).map((value) => (
          <button key={value} type="button" onClick={() => setLang(value)} className="rounded-full border px-3 py-1.5 text-sm">
            {value.toUpperCase()}
          </button>
        ))}
      </div>
      {loading || !challenge ? <p className="interactive-instruction">Loading challenge…</p> : (
        <InteractiveGameBoard mode="memory" lang={lang} challenge={challenge} onComplete={complete} />
      )}
    </main>
  )
}
