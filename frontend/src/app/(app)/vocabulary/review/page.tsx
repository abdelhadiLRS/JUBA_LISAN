'use client'

import { useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import { apiFetch, getGuestMemory, getGuestReviewState } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useTranslations } from 'next-intl'

const REVIEW_KEY = 'juba_lisan_review_state'
type Word = { word: string; translation: string; source?: string; target?: string; id?: number; definition?: string; example_sentence?: string }
type Rating = 'again' | 'hard' | 'good' | 'easy'
type ReviewState = { repetitions: number; interval: number; ease: number; due: number }
type ServerCard = Word & { id: number; next_review: string; repetitions: number; interval: number; ease_factor: number }

function readWords(): Word[] { return getGuestMemory() }
function readState(): Record<string, ReviewState> { return getGuestReviewState() }
function guestSchedule(prev: ReviewState, rating: Rating): ReviewState { if (rating === 'again') return { repetitions: 0, interval: 1, ease: Math.max(1.3, prev.ease - 0.2), due: Date.now() + 3600000 }; const ease = Math.max(1.3, prev.ease + (rating === 'easy' ? 0.15 : rating === 'hard' ? -0.15 : 0)); const repetitions = prev.repetitions + 1; const interval = prev.interval <= 1 ? (rating === 'easy' ? 4 : rating === 'hard' ? 1 : 2) : Math.max(1, Math.round(prev.interval * ease)); return { repetitions, interval, ease, due: Date.now() + interval * 86400000 } }
function quality(rating: Rating): number { return rating === 'again' ? 0 : rating === 'hard' ? 3 : rating === 'good' ? 4 : 5 }

export default function VocabularyReviewPage() {
  const t = useTranslations('vocabularyReview')
  const authenticated = !!useAuthStore((s) => s.accessToken)
  const [words, setWords] = useState<Word[]>([]); const [states, setStates] = useState<Record<string, ReviewState>>({}); const [index, setIndex] = useState(0); const [revealed, setRevealed] = useState(false); const [done, setDone] = useState(0); const [loading, setLoading] = useState(true); const [reviewing, setReviewing] = useState(false); const [error, setError] = useState('')

  const loadReviewCards = useCallback(async () => {
    setLoading(true)
    setError('')
    if (!authenticated) {
      const savedWords = readWords()
      const savedStates = readState()
      const dueWords = savedWords.filter((w) => {
        const state = savedStates[`${w.word.trim().toLowerCase()}::${w.target || ''}`]
        return !state || state.due <= Date.now()
      })
      setStates(savedStates)
      setWords(dueWords)
      setIndex(0)
      setDone(0)
      setRevealed(false)
      setLoading(false)
      return
    }
    try {
      const res = await apiFetch('/api/flashcards/due')
      if (!res.ok) throw new Error(t('loadError'))
      const data = await res.json() as { due?: ServerCard[] }
      setWords((data.due || []).map((c) => ({ ...c, translation: c.translation || c.definition || '', source: c.source, target: c.target })))
      setIndex(0)
      setDone(0)
      setRevealed(false)
      setLoading(false)
    } catch (e) {
      setError(e instanceof Error ? e.message : t('loadError'))
      setLoading(false)
    }
  }, [authenticated, t])

  useEffect(() => {
    void loadReviewCards()
  }, [loadReviewCards])

  const current = words[index]
  const remainingDue = Math.max(0, words.length - done)
  const progress = words.length ? Math.min(100, Math.round(done / words.length * 100)) : 0

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null
      if (target?.tagName === 'INPUT' || target?.tagName === 'TEXTAREA' || target?.isContentEditable) return
      if (!current || loading || reviewing) return
      if (event.key === ' ' && !revealed) {
        event.preventDefault()
        setRevealed(true)
        return
      }
      if (!revealed) return
      const ratings: Record<string, Rating> = { '1': 'again', '2': 'hard', '3': 'good', '4': 'easy' }
      const rating = ratings[event.key]
      if (rating) {
        event.preventDefault()
        void review(rating)
      }
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [current, loading, reviewing, revealed])

  async function review(rating: Rating) {
    if (!current || reviewing) return
    setReviewing(true)
    if (authenticated && current.id) {
      try {
        const res = await apiFetch(`/api/flashcards/${current.id}/review`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ quality: quality(rating) }) })
        if (!res.ok) throw new Error(t('saveError'))
      } catch (e) {
        setError(e instanceof Error ? e.message : t('saveError'))
        setReviewing(false)
        return
      }
    } else {
      const id = `${current.word.trim().toLowerCase()}::${current.target || ''}`
      const next = { ...states, [id]: guestSchedule(states[id] || { repetitions: 0, interval: 0, ease: 2.5, due: 0 }, rating) }
      setStates(next)
      if (typeof window !== 'undefined') window.localStorage.setItem(REVIEW_KEY, JSON.stringify(next))
    }
    setError('')
    setDone((n) => n + 1)
    if (index + 1 < words.length) {
      setTimeout(() => {
        setIndex((n) => n + 1)
        setRevealed(false)
        setReviewing(false)
      }, 120)
    } else {
      setReviewing(false)
    }
  }
  function restart() { void loadReviewCards() }
  function speak() {
    if (!current || typeof window === 'undefined' || !('speechSynthesis' in window)) return
    window.speechSynthesis.cancel()
    const u = new SpeechSynthesisUtterance(current.word)
    const rawSource = current.source && current.source !== 'account' ? current.source.replace(/_/g, '-') : 'en-US'
    const languageDefaults: Record<string, string> = {
      en: 'en-US', es: 'es-ES', de: 'de-DE', fr: 'fr-FR', it: 'it-IT',
      nl: 'nl-NL', pl: 'pl-PL', pt: 'pt-PT', ro: 'ro-RO', ru: 'ru-RU',
    }
    const normalized = rawSource.toLowerCase()
    u.lang = normalized.includes('-') ? normalized : (languageDefaults[normalized] || normalized)
    window.speechSynthesis.speak(u)
  }

  if (loading) return <main className="mx-auto max-w-4xl p-6 sm:p-10"><div className="juba-card p-10 text-center font-bold">{t('loading')}</div></main>
  if (error && !words.length) return <main className="mx-auto max-w-4xl p-6 sm:p-10"><div className="juba-card rounded-[30px] border-2 border-[var(--juba-lilac)] p-10 text-center shadow-[0_22px_55px_rgba(61,42,130,0.1)]" aria-live="polite"><h1 className="text-2xl font-black">{t('unavailable')}</h1><p className="mt-3 text-[var(--juba-muted)]">{error}</p><button type="button" onClick={() => void loadReviewCards()} disabled={loading} className="mt-6 rounded-full border-2 border-[var(--juba-lilac)] bg-[var(--juba-violet)] px-6 py-3 font-black disabled:opacity-40">{t('tryAgain')}</button></div></main>
  if (!words.length) return <main className="mx-auto max-w-3xl p-6"><div className="juba-card p-8 text-center"><h1 className="mt-3 text-3xl font-black">{t('noDue')}</h1><p className="mt-3 text-[var(--juba-muted)]">{authenticated ? t('caughtUp') : t('guestHint')}</p><Link href={authenticated ? '/vocabulary' : '/translator'} className="mt-6 inline-block rounded-full border-2 border-[var(--juba-lilac)] bg-[var(--juba-violet)] px-6 py-3 font-black">{authenticated ? `${t('openVocabulary')} →` : `${t('openTranslator')} →`}</Link></div></main>

  const finished = done >= words.length
  return <main className="mx-auto max-w-4xl p-6 sm:p-10"><div className="mb-6 flex items-center justify-between gap-4"><div><h1 className="mt-2 text-3xl font-black sm:text-4xl">{t('title')}</h1><p className="mt-1 text-sm font-bold text-[var(--juba-muted)]">{authenticated ? `${words.length} ${t('cardsDue')}` : `${remainingDue} ${t('dueNow')} · ${words.length} ${t('saved')}`}</p></div><Link href="/vocabulary" className="font-bold underline">{t('vocabulary')}</Link></div><div className="mb-6 h-2 overflow-hidden rounded-full bg-[var(--juba-lilac)]" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress} aria-label={t('progressLabel')}><div className="h-full bg-[var(--juba-violet)] transition-all" style={{ width: `${progress}%` }} /></div>{error && <div className="mb-4 rounded-[20px] border-2 border-[var(--juba-lilac)] p-3 text-sm font-bold" role="alert">{error}</div>}
    {finished ? <div className="juba-card p-10 text-center"><div className="text-5xl">✓</div><h2 className="mt-4 text-3xl font-black">{t('complete')}</h2><p className="mt-2 text-[var(--juba-muted)]">{t('reviewed', { count: words.length })}</p><button type="button" onClick={restart} className="mt-6 rounded-full border-2 border-[var(--juba-lilac)] bg-[var(--juba-violet)] px-6 py-3 font-black">{t('reviewAgain')}</button></div> : <div className="juba-card overflow-hidden rounded-[32px] border-2 border-[var(--juba-lilac)] p-6 shadow-[0_24px_60px_rgba(61,42,130,0.12)] sm:p-10"><div className="flex items-center justify-between text-sm font-bold text-[var(--juba-muted)]"><span>{index + 1} / {words.length}</span><span>{authenticated ? t('account') : `${current.source || t('source')} → ${current.target || t('target')}`}</span></div><button type="button" onClick={speak} className="mx-auto mt-10 block text-5xl font-black sm:text-7xl" dir="auto">{current.word}</button><p className="mt-3 text-center text-sm font-bold text-[var(--juba-muted)]">{t('tapToHear')}</p><p className="mt-1 text-center text-xs font-medium text-[var(--juba-muted)]" aria-label={t('shortcutHint')}>{revealed ? t('rateKeys') : t('spaceShortcut')}</p>{revealed && <div className="mt-10 border-2 border-[var(--juba-lilac)] bg-white-soft p-8 text-center"><p className="text-3xl font-black" dir="auto">{current.translation || current.definition}</p>{current.example_sentence && <p className="mt-3 text-[var(--juba-muted)]" dir="auto">{current.example_sentence}</p>}</div>}<div className="mt-8 text-center"><button type="button" aria-label={t('reveal')} aria-expanded={revealed} onClick={() => setRevealed(true)} disabled={revealed} className="rounded-full border-2 border-[var(--juba-lilac)] bg-[var(--juba-violet)] px-8 py-3 font-black disabled:opacity-40">{t('reveal')}</button></div>{revealed && <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4"><button type="button" aria-label={t('again')} onClick={() => review('again')} className="rounded-[20px] border-2 border-[var(--juba-lilac)] px-4 py-3 font-black disabled:opacity-40" disabled={reviewing}>{t('again')}</button><button type="button" aria-label={t('hard')} onClick={() => review('hard')} className="rounded-[20px] border-2 border-[var(--juba-lilac)] px-4 py-3 font-black disabled:opacity-40" disabled={reviewing}>{t('hard')}</button><button type="button" aria-label={t('good')} onClick={() => review('good')} className="rounded-[20px] border-2 border-[var(--juba-lilac)] bg-[var(--juba-violet)] px-4 py-3 font-black disabled:opacity-40" disabled={reviewing}>{t('good')}</button><button type="button" aria-label={t('easy')} onClick={() => review('easy')} className="rounded-[20px] border-2 border-[var(--juba-lilac)] px-4 py-3 font-black disabled:opacity-40" disabled={reviewing}>{t('easy')}</button></div>}</div>}
  </main>
}
