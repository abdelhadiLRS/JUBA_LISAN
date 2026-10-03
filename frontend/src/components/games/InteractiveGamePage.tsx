'use client'

import { useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useLocale } from 'next-intl'
import { useLanguageStore } from '@/store/language'
import { gameLanguageForTargetLanguage } from '@/lib/games/persist'
import { EducationalGameSession } from './EducationalGameSession'
import '@/app/(app)/games/educational-games.css'

type Mode = 'memory' | 'matching' | 'ordering' | 'sentence_builder'
export function InteractiveGamePage({mode}: {mode: Mode}) {
  const router = useRouter()
  const params = useSearchParams()
  const arabic = useLocale().startsWith('ar')
  const language = useLanguageStore(state => state.activeLanguage)
  const code = language?.code ?? 'en-GB'
  const [round, setRound] = useState(0)
  const requested = Number(params.get('difficulty'))
  const difficulty = Number.isInteger(requested) && requested >= 1 && requested <= 3 ? requested : 1
  // The old ordering challenge was a shuffled arbitrary vocabulary list with
  // no recoverable ordering rule. Teach sentence order instead, using the
  // authored sentence's server-only solution, not its shuffled public array.
  const gameId = mode === 'ordering' ? 'sentence_builder' : mode
  const title = gameId === 'memory' ? (arabic ? 'ذاكرة الكلمات' : 'Word memory') : gameId === 'matching' ? (arabic ? 'وصل المعنى' : 'Meaning match') : (arabic ? 'مهندس الجمل' : 'Sentence architect')
  return <main className="juba-page-shell educational-games" dir={arabic ? 'rtl' : 'ltr'}><EducationalGameSession key={`${gameId}:${code}:${difficulty}:${round}`} gameId={gameId} language={gameLanguageForTargetLanguage(code)} targetLanguage={code} difficulty={difficulty} arabic={arabic} title={title} onExit={() => router.push('/games')} onReplay={() => setRound(value => value + 1)} /></main>
}
