'use client'

import { useMemo, useState } from 'react'
import { saveTranslatedWordLocally } from '@/lib/api'

const LANGUAGES = [
  ['auto', 'Detect language'], ['ar', 'العربية'], ['en', 'English'], ['fr', 'Français'],
  ['es', 'Español'], ['it', 'Italiano'], ['de', 'Deutsch'], ['pt', 'Português'],
  ['tr', 'Türkçe'], ['ru', 'Русский'],
] as const

export default function TranslatorPage() {
  const [text, setText] = useState('')
  const [source, setSource] = useState('auto')
  const [target, setTarget] = useState('ar')
  const [translation, setTranslation] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)

  const sourceLabel = useMemo(() => LANGUAGES.find(([code]) => code === source)?.[1] ?? source, [source])
  const targetLabel = useMemo(() => LANGUAGES.find(([code]) => code === target)?.[1] ?? target, [target])

  async function translate() {
    if (!text.trim()) return
    setLoading(true); setError(''); setSaved(false)
    try {
      const response = await fetch('/api/translate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: text.trim(), source, target }) })
      const data = await response.json()
      if (!response.ok) throw new Error(data?.error || 'Translation failed.')
      setTranslation(data.translation || '')
    } catch (err) { setError(err instanceof Error ? err.message : 'Unable to translate right now.') }
    finally { setLoading(false) }
  }

  function swapLanguages() {
    if (source === 'auto') return
    setSource(target); setTarget(source); setText(translation); setTranslation(text)
  }

  function speak(value: string, lang: string) {
    if (!value || typeof window === 'undefined' || !('speechSynthesis' in window)) return
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(value); utterance.lang = lang === 'auto' ? 'en' : lang
    window.speechSynthesis.speak(utterance)
  }

  function saveWord() {
    if (!text.trim() || !translation.trim()) return
    saveTranslatedWordLocally({ word: text.trim(), translation: translation.trim(), sourceLanguage: source, targetLanguage: target, source: 'translator', createdAt: new Date().toISOString() })
    setSaved(true)
  }

  return (
    <main className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <section className="juba-card relative overflow-hidden p-6 sm:p-10">
        <div className="juba-hero-glow -right-20 -top-20" aria-hidden="true" />
        <div className="relative z-10">
          <span className="juba-eyebrow">JUBA LISAN · Instant Translator</span>
          <h1 className="mt-5 text-4xl font-black tracking-tight sm:text-6xl">Translate. Understand. Learn.</h1>
          <p className="mt-4 max-w-2xl text-base font-medium text-fl-muted-1 sm:text-lg">ترجمة فورية للزوار بدون تسجيل. احفظ الكلمات اختيارياً لتبني ذاكرتك اللغوية.</p>
        </div>
      </section>

      <section className="mt-6 grid gap-5 lg:grid-cols-[1fr_auto_1fr] lg:items-stretch" aria-label="Instant translator">
        <div className="juba-card flex min-h-[360px] flex-col p-5">
          <div className="flex items-center justify-between gap-3"><label className="text-sm font-black">{sourceLabel}</label><select value={source} onChange={(e) => setSource(e.target.value)} className="border-2 border-fl-border bg-fl-surface px-3 py-2 text-sm font-bold">{LANGUAGES.map(([code, label]) => <option key={code} value={code}>{label}</option>)}</select></div>
          <textarea value={text} onChange={(e) => setText(e.target.value)} onKeyDown={(e) => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') translate() }} maxLength={2000} placeholder="Type or paste anything…" className="mt-5 min-h-[235px] flex-1 resize-none border-2 border-fl-border bg-fl-surface p-5 text-xl font-semibold outline-none placeholder:text-fl-muted-2" dir="auto" />
          <div className="mt-3 flex items-center justify-between text-xs font-bold text-fl-muted-1"><span>{text.length}/2000</span><button type="button" onClick={() => speak(text, source)} disabled={!text.trim()} className="rounded-full border-2 border-fl-border px-4 py-2 font-black disabled:opacity-40">🔊 Listen</button></div>
        </div>

        <div className="flex items-center justify-center"><button type="button" onClick={swapLanguages} disabled={source === 'auto'} aria-label="Swap languages" className="h-14 w-14 rounded-full border-2 border-fl-border bg-fl-accent text-2xl font-black shadow-[3px_3px_0_var(--juba-border)] disabled:opacity-40">↔</button></div>

        <div className="juba-card flex min-h-[360px] flex-col p-5">
          <div className="flex items-center justify-between gap-3"><label className="text-sm font-black">{targetLabel}</label><select value={target} onChange={(e) => setTarget(e.target.value)} className="border-2 border-fl-border bg-fl-surface px-3 py-2 text-sm font-bold">{LANGUAGES.filter(([code]) => code !== 'auto').map(([code, label]) => <option key={code} value={code}>{label}</option>)}</select></div>
          <div className="mt-5 flex min-h-[235px] flex-1 items-start border-2 border-fl-border bg-fl-surface-soft p-5 text-xl font-semibold" dir="auto">{loading ? <span className="animate-pulse">Translating…</span> : translation || <span className="text-fl-muted-2">Your translation will appear here.</span>}</div>
          <div className="mt-3 flex flex-wrap items-center justify-between gap-2"><button type="button" onClick={() => speak(translation, target)} disabled={!translation} className="rounded-full border-2 border-fl-border px-4 py-2 font-black disabled:opacity-40">🔊 Listen</button><button type="button" onClick={saveWord} disabled={!translation} className="rounded-full border-2 border-fl-border bg-fl-accent px-5 py-2 font-black disabled:opacity-40">⭐ Learn this</button></div>
        </div>
      </section>

      <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"><button type="button" onClick={translate} disabled={!text.trim() || loading} className="min-h-14 rounded-2xl border-2 border-fl-border bg-fl-accent px-8 text-lg font-black shadow-[4px_4px_0_var(--juba-border)] disabled:opacity-50">{loading ? 'Translating…' : 'Translate now →'}</button><p className="text-sm font-semibold text-fl-muted-1">No account required · Translation stays open to everyone.</p></div>
      {saved && <div className="juba-card mt-5 border-2 p-4 font-black">✓ Added to JUBA Memory — saved locally on this device.</div>}
      {error && <div role="alert" className="juba-card mt-5 border-2 p-4 font-bold text-red-700">{error}</div>}
    </main>
  )
}
