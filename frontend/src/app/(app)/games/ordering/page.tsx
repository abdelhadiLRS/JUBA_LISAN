'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { InteractiveGameBoard } from '@/components/games/InteractiveGameBoard'
import '@/components/games/interactive-games.css'
import { persistGameEvent } from '@/lib/games/persist'
import { useProgressStore } from '@/store/progress'

type Lang = 'ar' | 'fr' | 'en'

export default function OrderingGamePage() {
  const searchParams = useSearchParams()
  const [lang, setLang] = useState<Lang>('ar')
  const addGameXP = useProgressStore((state) => state.addGameXP)
  const recordGameAttempt = useProgressStore((state) => state.recordGameAttempt)
  const completeGame = useProgressStore((state) => state.completeGame)
  const setProgress = useProgressStore((state) => state.setProgress)

  useEffect(() => {
    const value = searchParams.get('lang')
    if (value === 'ar' || value === 'fr' || value === 'en') setLang(value)
  }, [searchParams])

  function complete(result: { questionsAnswered: number; correctAnswers: number }) {
    const questionsAnswered = Math.max(0, Math.floor(result.questionsAnswered))
    const correctAnswers = Math.max(0, Math.min(questionsAnswered, Math.floor(result.correctAnswers)))
    const earnedXp = correctAnswers * 5 + (questionsAnswered - correctAnswers)
    const roundScore = questionsAnswered > 0
      ? Math.round((correctAnswers / questionsAnswered) * 25)
      : 0
    addGameXP(earnedXp, 'ordering', correctAnswers > 0)
    recordGameAttempt(correctAnswers === questionsAnswered && questionsAnswered > 0, questionsAnswered, correctAnswers)
    completeGame(roundScore, false)
    void persistGameEvent({
      gameId: 'ordering',
      questionsAnswered,
      correctAnswers,
      roundScore,
    }).then((server) => {
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
    }).catch(() => undefined)

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
      <InteractiveGameBoard mode="ordering" lang={lang} onComplete={complete} />
    </main>
  )
}
