'use client'

import { useState } from 'react'
import { InteractiveGameBoard } from '@/components/games/InteractiveGameBoard'
import '@/components/games/interactive-games.css'
import { useProgressStore } from '@/store/progress'

export default function MemoryGamePage() {
  const [lang, setLang] = useState<'ar' | 'fr' | 'en'>('ar')
  const addGameXP = useProgressStore((state) => state.addGameXP)
  const recordGameAttempt = useProgressStore((state) => state.recordGameAttempt)
  const [completed, setCompleted] = useState(false)

  function complete() {
    if (completed) return
    setCompleted(true)
    addGameXP(25, 'memory', true)
    recordGameAttempt(true)
  }

  return (
    <main className="mx-auto w-full max-w-3xl px-4 py-8">
      <div className="mb-4 flex flex-wrap items-center gap-2">
        {(['ar', 'fr', 'en'] as const).map((value) => (
          <button key={value} type="button" onClick={() => { setLang(value); setCompleted(false) }} className="rounded-full border px-3 py-1.5 text-sm">
            {value.toUpperCase()}
          </button>
        ))}
      </div>
      <InteractiveGameBoard mode="memory" lang={lang} onComplete={complete} />
    </main>
  )
}
