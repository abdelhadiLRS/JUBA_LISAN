'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { InteractiveGameBoard } from '@/components/games/InteractiveGameBoard'
import '@/components/games/interactive-games.css'
import { apiFetch } from '@/lib/api'
import { useProgressStore } from '@/store/progress'

type Lang = 'ar' | 'fr' | 'en'

export default function OrderingGamePage() {
  const searchParams = useSearchParams()
  const [lang, setLang] = useState<Lang>('ar')
  const addGameXP = useProgressStore((state) => state.addGameXP)
  const recordGameAttempt = useProgressStore((state) => state.recordGameAttempt)
  const completeGame = useProgressStore((state) => state.completeGame)

  useEffect(() => {
    const value = searchParams.get('lang')
    if (value === 'ar' || value === 'fr' || value === 'en') setLang(value)
  }, [searchParams])

  function complete(result: { questionsAnswered: number; correctAnswers: number }) {
    addGameXP(25, 'ordering', true)
    recordGameAttempt(true, result.questionsAnswered, result.correctAnswers)
    completeGame(25, false)
    void apiFetch('/api/progress/game', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        xp: 25,
        correct_answers: result.correctAnswers,
        questions_answered: result.questionsAnswered,
        skills: { ordering: 1 },
      }),
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
