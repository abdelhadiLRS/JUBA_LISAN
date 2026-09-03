'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, BookOpenCheck, RotateCcw, Trash2, Volume2 } from 'lucide-react'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { getGuestMemory, saveTranslatedWordLocally, type TranslatorSavedWord } from '@/lib/api'

const REVIEW_KEY = 'juba_lisan_review_state'
type ReviewState = Record<string, { repetitions: number; interval: number; ease: number; due: number }>

function loadReview(): ReviewState { try { const value = JSON.parse(localStorage.getItem(REVIEW_KEY) || '{}'); return value && typeof value === 'object' ? value : {} } catch { return {} } }
function storeReview(value: ReviewState) { try { localStorage.setItem(REVIEW_KEY, JSON.stringify(value)) } catch {} }

export default function SavedWordsPage() {
  const [words, setWords] = useState<TranslatorSavedWord[]>([])
  const [review, setReview] = useState<ReviewState>({})
  const [index, setIndex] = useState(0)
  const [revealed, setRevealed] = useState(false)

  useEffect(() => { setWords(getGuestMemory()); setReview(loadReview()) }, [])

  const dueWords = useMemo(() => words.filter((word) => !review[`${word.source}:${word.target}:${word.word}`] || review[`${word.source}:${word.target}:${word.word}`].due <= Date.now()), [words, review])
  const current = dueWords[index]
  const key = current ? `${current.source}:${current.target}:${current.word}` : ''

  function remove(word: TranslatorSavedWord) {
    const next = words.filter((item) => !(item.word === word.word && item.target === word.target && item.source === word.source))
    setWords(next)
    try { localStorage.setItem('juba_lisan_saved_vocabulary', JSON.stringify(next)) } catch {}
    setIndex(0)
  }

  function rate(quality: number) {
    if (!current) return
    const previous = review[key] || { repetitions: 0, interval: 0, ease: 2.5, due: Date.now() }
    const repetitions = quality < 3 ? 0 : previous.repetitions + 1
    const interval = quality < 3 ? 10 * 60 * 1000 : Math.max(24 * 60 * 60 * 1000, (previous.interval || 24 * 60 * 60 * 1000) * (quality === 5 ? 3 : quality === 4 ? 2 : 1.3))
    const next = { ...review, [key]: { repetitions, interval, ease: Math.max(1.3, previous.ease + (quality >= 3 ? 0.1 : -0.2)), due: Date.now() + interval } }
    setReview(next); storeReview(next); setRevealed(false); setIndex((value) => value + 1)
  }

  return <main className="min-h-screen bg-[var(--juba-bg)] px-4 py-8 sm:px-6"><div className="mx-auto max-w-5xl">
    <header className="mb-8 flex flex-wrap items-center justify-between gap-4"><div><p className="text-xs font-black uppercase tracking-[.18em] text-[var(--juba-muted)]">JUBA LISAN · Visitor mode</p><h1 className="mt-2 text-4xl font-black tracking-tight text-[var(--juba-text)]">Saved words</h1><p className="mt-2 text-sm font-medium text-[var(--juba-muted)]">Your vocabulary stays in this browser until you choose to sync it.</p></div><Link href="/" className="inline-flex items-center gap-2 rounded-full border-2 border-[var(--juba-border)] bg-[var(--juba-surface)] px-4 py-2.5 text-sm font-black text-[var(--juba-text)]"><ArrowLeft className="h-4 w-4" />Translator</Link></header>
    {words.length === 0 ? <section className="rounded-[32px] border-2 border-[var(--juba-border)] bg-[var(--juba-accent)] p-8 text-center shadow-[var(--juba-shadow-md)]"><BookOpenCheck className="mx-auto h-10 w-10" /><h2 className="mt-4 text-2xl font-black">Start building your vocabulary</h2><p className="mx-auto mt-2 max-w-md text-sm font-semibold text-neutral-800/70">Translate a word, tap Learn this, and it will appear here without requiring an account.</p><Link href="/" className="mt-6 inline-flex rounded-full border-2 border-neutral-950 bg-white px-5 py-3 text-sm font-black">Open translator</Link></section> : <div className="grid gap-6 lg:grid-cols-[1.1fr_.9fr]">
      <section className="rounded-[32px] border-2 border-[var(--juba-border)] bg-[var(--juba-surface)] p-5 shadow-[var(--juba-shadow-sm)]"><div className="mb-4 flex items-center justify-between"><h2 className="font-black">Your collection <span className="text-[var(--juba-muted)]">({words.length})</span></h2><Link href="/login" className="rounded-full bg-[var(--juba-text)] px-4 py-2 text-xs font-black text-[var(--juba-surface)]">Sign in to sync</Link></div><div className="space-y-2">{words.map((word) => <article key={`${word.source}:${word.target}:${word.word}`} className="flex items-center gap-3 rounded-2xl border border-[var(--juba-border)] bg-[var(--juba-surface-2)] p-4"><AudioPlayer text={word.word} size="sm" /><div className="min-w-0 flex-1"><p className="truncate text-sm font-black text-[var(--juba-text)]">{word.word}</p><p className="truncate text-sm font-semibold text-[var(--juba-muted)]">{word.translation}</p><p className="mt-1 text-[10px] font-bold uppercase tracking-wider text-[var(--juba-muted)]">{word.source} → {word.target}</p></div><button type="button" onClick={() => remove(word)} aria-label={`Remove ${word.word}`} className="rounded-full p-2 text-[var(--juba-muted)] hover:bg-red-100 hover:text-red-700"><Trash2 className="h-4 w-4" /></button></article>)}</div></section>
      <section className="rounded-[32px] border-2 border-neutral-950 bg-[var(--juba-accent)] p-5 shadow-[5px_5px_0_rgba(17,17,17,.85)]"><div className="flex items-center justify-between"><div><p className="text-[10px] font-black uppercase tracking-[.18em] text-neutral-950/55">Practice</p><h2 className="mt-1 text-2xl font-black">Quick review</h2></div><span className="rounded-full bg-neutral-950 px-3 py-1 text-xs font-black text-white">{dueWords.length} due</span></div>{current ? <><button type="button" onClick={() => setRevealed(v => !v)} className="mt-5 min-h-56 w-full rounded-[26px] border-2 border-neutral-950 bg-white p-7 text-center"><p className="text-xs font-black uppercase tracking-widest text-neutral-500">{revealed ? 'Translation' : 'Word'}</p><p className="mt-5 text-4xl font-black text-neutral-950">{revealed ? current.translation : current.word}</p><div className="mt-4 flex items-center justify-center gap-2 text-xs font-bold text-neutral-500"><Volume2 className="h-4 w-4" />Tap to reveal</div></button>{revealed && <div className="mt-3 grid grid-cols-3 gap-2"><button onClick={() => rate(2)} className="rounded-2xl border-2 border-neutral-950 bg-white px-3 py-3 text-xs font-black">Again</button><button onClick={() => rate(4)} className="rounded-2xl border-2 border-neutral-950 bg-white px-3 py-3 text-xs font-black">Good</button><button onClick={() => rate(5)} className="rounded-2xl border-2 border-neutral-950 bg-neutral-950 px-3 py-3 text-xs font-black text-white">Easy</button></div>}</> : <div className="mt-5 rounded-[26px] border-2 border-neutral-950 bg-white/75 p-8 text-center"><RotateCcw className="mx-auto h-8 w-8" /><p className="mt-3 font-black">Nothing due right now.</p><p className="mt-1 text-sm font-semibold text-neutral-700">Come back later or add more words.</p></div>}</section>
    </div>}
  </div></main>
}
