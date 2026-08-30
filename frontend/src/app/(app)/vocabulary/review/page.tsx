'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'

const KEY = 'juba_lisan_saved_vocabulary'
type Word = { word: string; translation: string; source?: string; target?: string }

type Rating = 'again' | 'hard' | 'good' | 'easy'

function readWords(): Word[] {
  if (typeof window === 'undefined') return []
  try {
    const value: unknown = JSON.parse(window.localStorage.getItem(KEY) || '[]')
    return Array.isArray(value) ? value.filter((x): x is Word => !!x && typeof x === 'object' && typeof x.word === 'string' && typeof x.translation === 'string') : []
  } catch { return [] }
}

export default function VocabularyReviewPage() {
  const [words, setWords] = useState<Word[]>([])
  const [index, setIndex] = useState(0)
  const [revealed, setRevealed] = useState(false)
  const [done, setDone] = useState(0)
  const [rating, setRating] = useState<Rating | null>(null)

  useEffect(() => setWords(readWords()), [])

  const current = words[index]
  const progress = useMemo(() => words.length ? Math.round((done / words.length) * 100) : 0, [done, words.length])

  function review(value: Rating) {
    if (!current) return
    setRating(value)
    setDone((n) => n + 1)
    if (index + 1 < words.length) {
      setTimeout(() => { setIndex((n) => n + 1); setRevealed(false); setRating(null) }, 180)
    }
  }

  function speak() {
    if (!current || typeof window === 'undefined' || !('speechSynthesis' in window)) return
    window.speechSynthesis.cancel()
    const u = new SpeechSynthesisUtterance(current.word); u.lang = current.source || 'en-US'; window.speechSynthesis.speak(u)
  }

  if (!words.length) return <main className="mx-auto max-w-3xl p-6"><div className="juba-card p-8 text-center"><span className="juba-eyebrow">JUBA MEMORY</span><h1 className="mt-3 text-3xl font-black">Your review deck is empty</h1><p className="mt-3 text-fl-muted-1">Save words from Instant Translator first. You can use this review without creating an account.</p><Link href="/translator" className="mt-6 inline-block rounded-full border-2 border-fl-border bg-fl-accent px-6 py-3 font-black">Open Translator →</Link></div></main>

  const finished = done >= words.length
  return <main className="mx-auto max-w-4xl p-6 sm:p-10">
    <div className="mb-6 flex items-center justify-between gap-4"><div><span className="juba-eyebrow">JUBA MEMORY · REVIEW</span><h1 className="mt-2 text-3xl font-black sm:text-4xl">Quick review</h1></div><Link href="/vocabulary" className="font-bold underline">Vocabulary</Link></div>
    <div className="mb-6 h-2 overflow-hidden rounded-full bg-fl-surface-2"><div className="h-full bg-fl-accent transition-all" style={{ width: `${progress}%` }} /></div>
    {finished ? <div className="juba-card p-10 text-center"><div className="text-5xl">✓</div><h2 className="mt-4 text-3xl font-black">Review complete</h2><p className="mt-2 text-fl-muted-1">You reviewed {words.length} saved {words.length === 1 ? 'word' : 'words'}.</p><button onClick={() => { setIndex(0); setDone(0); setRevealed(false); setRating(null) }} className="mt-6 rounded-full border-2 border-fl-border bg-fl-accent px-6 py-3 font-black">Review again</button></div> : <div className="juba-card overflow-hidden p-6 sm:p-10">
      <div className="flex items-center justify-between text-sm font-bold text-fl-muted-1"><span>{index + 1} / {words.length}</span><span>{current.source || 'source'} → {current.target || 'target'}</span></div>
      <button type="button" onClick={speak} className="mx-auto mt-10 block text-5xl font-black sm:text-7xl" dir="auto" aria-label="Listen to word">{current.word}</button>
      <p className="mt-3 text-center text-sm font-bold text-fl-muted-1">Tap the word to hear it · Tap reveal to check your answer</p>
      {revealed && <div className="mt-10 border-2 border-fl-border bg-fl-surface-soft p-8 text-center"><p className="text-3xl font-black" dir="auto">{current.translation}</p></div>}
      <div className="mt-8 text-center"><button onClick={() => setRevealed(true)} disabled={revealed} className="rounded-full border-2 border-fl-border bg-fl-accent px-8 py-3 font-black disabled:opacity-40">Reveal translation</button></div>
      {revealed && <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4"><button onClick={() => review('again')} className="rounded-xl border-2 border-fl-border px-4 py-3 font-black">Again</button><button onClick={() => review('hard')} className="rounded-xl border-2 border-fl-border px-4 py-3 font-black">Hard</button><button onClick={() => review('good')} className="rounded-xl border-2 border-fl-border bg-fl-accent px-4 py-3 font-black">Good</button><button onClick={() => review('easy')} className="rounded-xl border-2 border-fl-border px-4 py-3 font-black">Easy</button></div>}
      {rating && <p className="mt-4 text-center text-sm font-bold">Recorded: {rating}</p>}
    </div>}
  </main>
}
