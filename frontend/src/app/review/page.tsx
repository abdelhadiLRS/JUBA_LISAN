'use client'

import { useEffect, useMemo, useState } from 'react'
import { Check, Clock3, RotateCcw, Sparkles, Zap } from 'lucide-react'

const KEY = 'juba_lisan_saved_vocabulary'
type Item = { id: string; sourceText: string; translation: string; mastery?: number; nextReviewAt?: string; sourceLanguage?: string; targetLanguage?: string }

function readItems(): Item[] {
  try { return JSON.parse(localStorage.getItem(KEY) || '[]') } catch { return [] }
}

function nextDate(rating: 'again'|'hard'|'good'|'easy') {
  const minutes = { again: 10, hard: 24 * 60, good: 3 * 24 * 60, easy: 7 * 24 * 60 }[rating]
  return new Date(Date.now() + minutes * 60_000).toISOString()
}

export default function ReviewPage() {
  const [items, setItems] = useState<Item[]>([])
  const [index, setIndex] = useState(0)
  const [revealed, setRevealed] = useState(false)
  const [done, setDone] = useState(false)

  useEffect(() => setItems(readItems()), [])
  const due = useMemo(() => items.filter((item) => !item.nextReviewAt || new Date(item.nextReviewAt).getTime() <= Date.now()), [items])
  const current = due[index]

  function rate(rating: 'again'|'hard'|'good'|'easy') {
    if (!current) return
    const gain = { again: 0, hard: 8, good: 18, easy: 28 }[rating]
    const updated = items.map((item) => item.id === current.id ? { ...item, mastery: Math.min(100, (item.mastery || 0) + gain), nextReviewAt: nextDate(rating) } : item)
    localStorage.setItem(KEY, JSON.stringify(updated))
    setItems(updated)
    setRevealed(false)
    if (index + 1 >= due.length) setDone(true); else setIndex(index + 1)
  }

  if (done || (!current && items.length)) return <main className="mx-auto max-w-3xl px-5 py-16"><div className="rounded-[32px] border-2 border-neutral-950 bg-[#d8f53f] p-8 text-center shadow-[8px_8px_0_rgba(17,17,17,.9)]"><Sparkles className="mx-auto mb-4 h-9 w-9" /><h1 className="text-4xl font-black tracking-tight">Review complete!</h1><p className="mt-3 font-semibold">Your next reviews are scheduled. Keep the streak going.</p></div></main>
  if (!current) return <main className="mx-auto max-w-3xl px-5 py-16"><div className="rounded-[32px] border-2 border-neutral-950 bg-white p-8 text-center shadow-[8px_8px_0_rgba(17,17,17,.9)]"><Clock3 className="mx-auto mb-4 h-9 w-9" /><h1 className="text-3xl font-black">You're all caught up</h1><p className="mt-2 font-semibold text-neutral-600">Come back when your next review is due.</p></div></main>

  return <main className="mx-auto max-w-4xl px-5 py-10"><header className="mb-7 flex items-center justify-between"><div><p className="text-xs font-black uppercase tracking-[.2em] text-neutral-500">JUBA LISAN · SMART REVIEW</p><h1 className="mt-2 text-4xl font-black tracking-tight">Build your memory.</h1></div><div className="rounded-full border-2 border-neutral-950 bg-[#d8f53f] px-4 py-2 text-sm font-black">{index + 1}/{due.length}</div></header><section className="rounded-[32px] border-2 border-neutral-950 bg-white p-7 shadow-[8px_8px_0_rgba(17,17,17,.9)] dark:bg-neutral-900"><div className="mb-7 flex items-center justify-between"><span className="rounded-full bg-neutral-950 px-3 py-1 text-xs font-black text-white">{current.mastery || 0}% mastery</span><span className="text-xs font-bold text-neutral-500">Recall before reveal</span></div><div className="min-h-64 rounded-[24px] border-2 border-dashed border-neutral-300 p-8 text-center"><p className="text-3xl font-black">{current.sourceText}</p>{revealed ? <p className="mt-7 text-xl font-bold text-neutral-600">{current.translation}</p> : <button onClick={() => setRevealed(true)} className="mt-10 rounded-full border-2 border-neutral-950 bg-[#d8f53f] px-7 py-3 font-black shadow-[4px_4px_0_rgba(17,17,17,.9)]">Reveal answer</button>}</div>{revealed && <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4"><button onClick={() => rate('again')} className="rounded-2xl border-2 border-neutral-950 px-4 py-4 font-black"><RotateCcw className="mx-auto mb-1 h-4 w-4"/>Again</button><button onClick={() => rate('hard')} className="rounded-2xl border-2 border-neutral-950 px-4 py-4 font-black">Hard</button><button onClick={() => rate('good')} className="rounded-2xl border-2 border-neutral-950 bg-[#d8f53f] px-4 py-4 font-black"><Check className="mx-auto mb-1 h-4 w-4"/>Good</button><button onClick={() => rate('easy')} className="rounded-2xl border-2 border-neutral-950 px-4 py-4 font-black"><Zap className="mx-auto mb-1 h-4 w-4"/>Easy</button></div>}</section></main>
}
