'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'

const KEY = 'juba_lisan_saved_vocabulary'
const REVIEW_KEY = 'juba_lisan_review_state'
type Word = { word: string; translation: string; source?: string; target?: string }
type Rating = 'again' | 'hard' | 'good' | 'easy'
type ReviewState = { repetitions: number; interval: number; ease: number; due: number }

function readWords(): Word[] {
  if (typeof window === 'undefined') return []
  try { const value: unknown = JSON.parse(window.localStorage.getItem(KEY) || '[]'); return Array.isArray(value) ? value.filter((x): x is Word => !!x && typeof x === 'object' && typeof x.word === 'string' && typeof x.translation === 'string') : [] } catch { return [] }
}
function readState(): Record<string, ReviewState> {
  if (typeof window === 'undefined') return {}
  try { const value: unknown = JSON.parse(window.localStorage.getItem(REVIEW_KEY) || '{}'); return value && typeof value === 'object' && !Array.isArray(value) ? value as Record<string, ReviewState> : {} } catch { return {} }
}
function schedule(prev: ReviewState, rating: Rating): ReviewState {
  if (rating === 'again') return { repetitions: 0, interval: 1, ease: Math.max(1.3, prev.ease - 0.2), due: Date.now() + 60 * 60 * 1000 }
  const ease = Math.max(1.3, prev.ease + (rating === 'easy' ? 0.15 : rating === 'hard' ? -0.15 : 0))
  const repetitions = prev.repetitions + 1
  const interval = prev.interval <= 1 ? (rating === 'easy' ? 4 : rating === 'hard' ? 1 : 2) : Math.max(1, Math.round(prev.interval * ease))
  return { repetitions, interval, ease, due: Date.now() + interval * 86400000 }
}

export default function VocabularyReviewPage() {
  const [words, setWords] = useState<Word[]>([]); const [states, setStates] = useState<Record<string, ReviewState>>({}); const [index, setIndex] = useState(0); const [revealed, setRevealed] = useState(false); const [done, setDone] = useState(0)
  useEffect(() => { setWords(readWords()); setStates(readState()) }, [])
  const current = words[index]
  const dueWords = useMemo(() => words.filter((w) => { const s = states[`${w.word.trim().toLowerCase()}::${w.target || ''}`]; return !s || s.due <= Date.now() }), [words, states])
  const progress = words.length ? Math.round(done / words.length * 100) : 0

  function review(rating: Rating) {
    if (!current) return
    const id = `${current.word.trim().toLowerCase()}::${current.target || ''}`
    const next = { ...states, [id]: schedule(states[id] || { repetitions: 0, interval: 0, ease: 2.5, due: 0 }, rating) }
    setStates(next); if (typeof window !== 'undefined') window.localStorage.setItem(REVIEW_KEY, JSON.stringify(next)); setDone((n) => n + 1)
    if (index + 1 < words.length) { setTimeout(() => { setIndex((n) => n + 1); setRevealed(false) }, 150) }
  }
  function restart() { setIndex(0); setDone(0); setRevealed(false) }
  function speak() { if (!current || typeof window === 'undefined' || !('speechSynthesis' in window)) return; window.speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(current.word); u.lang = current.source || 'en-US'; window.speechSynthesis.speak(u) }

  if (!words.length) return <main className="mx-auto max-w-3xl p-6"><div className="juba-card p-8 text-center"><span className="juba-eyebrow">JUBA MEMORY</span><h1 className="mt-3 text-3xl font-black">Your review deck is empty</h1><p className="mt-3 text-fl-muted-1">Save words from Instant Translator first. No account is required.</p><Link href="/translator" className="mt-6 inline-block rounded-full border-2 border-fl-border bg-fl-accent px-6 py-3 font-black">Open Translator →</Link></div></main>

  const finished = done >= words.length
  return <main className="mx-auto max-w-4xl p-6 sm:p-10"><div className="mb-6 flex items-center justify-between gap-4"><div><span className="juba-eyebrow">JUBA MEMORY · REVIEW</span><h1 className="mt-2 text-3xl font-black sm:text-4xl">Spaced review</h1><p className="mt-1 text-sm font-bold text-fl-muted-1">{dueWords.length} due now · {words.length} saved</p></div><Link href="/vocabulary" className="font-bold underline">Vocabulary</Link></div><div className="mb-6 h-2 overflow-hidden rounded-full bg-fl-surface-2"><div className="h-full bg-fl-accent transition-all" style={{ width: `${progress}%` }} /></div>
    {finished ? <div className="juba-card p-10 text-center"><div className="text-5xl">✓</div><h2 className="mt-4 text-3xl font-black">Review complete</h2><p className="mt-2 text-fl-muted-1">You reviewed {words.length} saved {words.length === 1 ? 'word' : 'words'}.</p><button onClick={restart} className="mt-6 rounded-full border-2 border-fl-border bg-fl-accent px-6 py-3 font-black">Review again</button></div> : <div className="juba-card overflow-hidden p-6 sm:p-10"><div className="flex items-center justify-between text-sm font-bold text-fl-muted-1"><span>{index + 1} / {words.length}</span><span>{current.source || 'source'} → {current.target || 'target'}</span></div><button type="button" onClick={speak} className="mx-auto mt-10 block text-5xl font-black sm:text-7xl" dir="auto">{current.word}</button><p className="mt-3 text-center text-sm font-bold text-fl-muted-1">Tap the word to hear it</p>{revealed && <div className="mt-10 border-2 border-fl-border bg-fl-surface-soft p-8 text-center"><p className="text-3xl font-black" dir="auto">{current.translation}</p></div>}<div className="mt-8 text-center"><button onClick={() => setRevealed(true)} disabled={revealed} className="rounded-full border-2 border-fl-border bg-fl-accent px-8 py-3 font-black disabled:opacity-40">Reveal translation</button></div>{revealed && <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4"><button onClick={() => review('again')} className="rounded-xl border-2 border-fl-border px-4 py-3 font-black">Again</button><button onClick={() => review('hard')} className="rounded-xl border-2 border-fl-border px-4 py-3 font-black">Hard</button><button onClick={() => review('good')} className="rounded-xl border-2 border-fl-border bg-fl-accent px-4 py-3 font-black">Good</button><button onClick={() => review('easy')} className="rounded-xl border-2 border-fl-border px-4 py-3 font-black">Easy</button></div>}</div>}
  </main>
}
