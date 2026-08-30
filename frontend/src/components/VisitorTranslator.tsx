'use client'

import { FormEvent, useState } from 'react'
import { ArrowRightLeft, Languages, Loader2, Sparkles, X } from 'lucide-react'

const LANGUAGES = [
  { code: 'ar', label: 'العربية', short: 'AR' },
  { code: 'en', label: 'English', short: 'EN' },
  { code: 'fr', label: 'Français', short: 'FR' },
  { code: 'es', label: 'Español', short: 'ES' },
  { code: 'it', label: 'Italiano', short: 'IT' },
  { code: 'de', label: 'Deutsch', short: 'DE' },
  { code: 'pt', label: 'Português', short: 'PT' },
]

function languageLabel(code: string) {
  if (code === 'auto') return 'Auto detect'
  return LANGUAGES.find((language) => language.code === code)?.label ?? code.toUpperCase()
}

export function VisitorTranslator() {
  const [open, setOpen] = useState(false)
  const [text, setText] = useState('')
  const [source, setSource] = useState('auto')
  const [target, setTarget] = useState('ar')
  const [translation, setTranslation] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function translate(event?: FormEvent) {
    event?.preventDefault()
    if (!text.trim()) return
    setLoading(true)
    setError('')
    try {
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, source, target }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data?.error || 'Translation failed')
      setTranslation(data.translation)
    } catch (err) {
      setTranslation('')
      setError(err instanceof Error ? err.message : 'Translation failed')
    } finally {
      setLoading(false)
    }
  }

  function swapLanguages() {
    if (source === 'auto') return
    setSource(target)
    setTarget(source)
    setTranslation('')
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label="Open instant translator"
        className="fixed bottom-5 end-5 z-40 inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-[#d8f53f] px-5 py-3 text-sm font-black text-neutral-950 shadow-[6px_6px_0_rgba(17,17,17,.9)] transition hover:-translate-y-0.5 hover:shadow-[8px_8px_0_rgba(17,17,17,.9)] dark:border-white dark:shadow-[5px_5px_0_rgba(255,255,255,.7)]"
      >
        <Languages className="h-4 w-4" />
        Translate
      </button>

      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-neutral-950/45 p-3 backdrop-blur-sm sm:p-6">
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="visitor-translator-title"
            className="w-full max-w-5xl overflow-hidden rounded-[30px] border-2 border-neutral-950 bg-[#f7f4ea] shadow-[10px_10px_0_rgba(17,17,17,.95)] dark:border-white dark:bg-neutral-950 dark:shadow-[8px_8px_0_rgba(255,255,255,.55)]"
          >
            <div className="flex items-start justify-between border-b-2 border-neutral-950 px-5 py-5 dark:border-white sm:px-8">
              <div>
                <div className="mb-2 inline-flex items-center gap-2 rounded-full border border-neutral-950 bg-[#d8f53f] px-3 py-1 text-[10px] font-black uppercase tracking-[0.16em] text-neutral-950">
                  <Sparkles className="h-3 w-3" /> JUBA LISAN
                </div>
                <h2 id="visitor-translator-title" className="text-3xl font-black tracking-[-0.04em] text-neutral-950 dark:text-white sm:text-4xl">Instant translator</h2>
                <p className="mt-1 max-w-xl text-sm font-medium text-neutral-600 dark:text-neutral-400">Translate a word, phrase, or sentence before you start learning.</p>
              </div>
              <button type="button" onClick={() => setOpen(false)} aria-label="Close translator" className="rounded-full border-2 border-neutral-950 bg-white p-2 text-neutral-950 transition hover:-rotate-6 dark:border-white dark:bg-neutral-900 dark:text-white">
                <X className="h-5 w-5" />
              </button>
            </div>

            <form onSubmit={translate} className="p-4 sm:p-7">
              <div className="grid gap-3 lg:grid-cols-[1fr_auto_1fr] lg:items-stretch">
                <section className="flex min-h-[300px] flex-col rounded-[24px] border-2 border-neutral-950 bg-white p-4 dark:border-white dark:bg-neutral-900 sm:p-5">
                  <div className="mb-4 flex flex-wrap items-center gap-2">
                    <span className="rounded-full bg-neutral-950 px-3 py-1.5 text-[11px] font-black uppercase tracking-wider text-white dark:bg-white dark:text-neutral-950">From</span>
                    <select value={source} onChange={(e) => { setSource(e.target.value); setTranslation('') }} className="max-w-full rounded-full border border-neutral-300 bg-transparent px-3 py-1.5 text-sm font-bold outline-none dark:border-neutral-700">
                      <option value="auto">Auto detect</option>
                      {LANGUAGES.map((language) => <option key={language.code} value={language.code}>{language.label}</option>)}
                    </select>
                  </div>
                  <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    maxLength={2000}
                    rows={7}
                    autoFocus
                    placeholder="Type or paste your text here…"
                    className="min-h-[190px] flex-1 resize-none bg-transparent text-xl font-semibold leading-relaxed text-neutral-950 outline-none placeholder:text-neutral-400 dark:text-white"
                  />
                  <div className="mt-3 flex items-center justify-between text-xs font-semibold text-neutral-400">
                    <span>{text.length}/2000</span>
                    <span>{source === 'auto' ? 'Automatic detection' : languageLabel(source)}</span>
                  </div>
                </section>

                <div className="flex items-center justify-center lg:px-1">
                  <button type="button" onClick={swapLanguages} disabled={source === 'auto'} aria-label="Swap languages" className="rounded-full border-2 border-neutral-950 bg-[#d8f53f] p-3 text-neutral-950 shadow-[3px_3px_0_rgba(17,17,17,.9)] transition hover:rotate-180 disabled:cursor-not-allowed disabled:opacity-35 dark:border-white dark:shadow-[2px_2px_0_rgba(255,255,255,.55)]">
                    <ArrowRightLeft className="h-5 w-5" />
                  </button>
                </div>

                <section className="flex min-h-[300px] flex-col rounded-[24px] border-2 border-neutral-950 bg-[#d8f53f] p-4 dark:border-white dark:bg-lime-300 sm:p-5">
                  <div className="mb-4 flex flex-wrap items-center gap-2">
                    <span className="rounded-full bg-neutral-950 px-3 py-1.5 text-[11px] font-black uppercase tracking-wider text-white">To</span>
                    <select value={target} onChange={(e) => { setTarget(e.target.value); setTranslation('') }} className="max-w-full rounded-full border border-neutral-950/30 bg-white/60 px-3 py-1.5 text-sm font-bold text-neutral-950 outline-none">
                      {LANGUAGES.map((language) => <option key={language.code} value={language.code}>{language.label}</option>)}
                    </select>
                  </div>
                  <div className="flex flex-1 items-start">
                    {error ? (
                      <p className="text-sm font-bold text-red-700">{error}</p>
                    ) : translation ? (
                      <p className="w-full text-xl font-black leading-relaxed text-neutral-950 sm:text-2xl">{translation}</p>
                    ) : (
                      <p className="text-lg font-semibold leading-relaxed text-neutral-700/70">Your translation will appear here.</p>
                    )}
                  </div>
                  <div className="mt-3 text-xs font-black uppercase tracking-wider text-neutral-950/55">{languageLabel(target)}</div>
                </section>
              </div>

              <div className="mt-5 flex flex-col-reverse gap-3 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-xs font-semibold leading-relaxed text-neutral-500">Quick visitor lookup. Save vocabulary and review it inside your JUBA LISAN learning journey.</p>
                <button type="submit" disabled={!text.trim() || loading} className="inline-flex min-h-12 items-center justify-center gap-2 rounded-full border-2 border-neutral-950 bg-neutral-950 px-7 py-3 text-sm font-black text-white shadow-[4px_4px_0_#d8f53f] transition hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-45 dark:border-white dark:bg-white dark:text-neutral-950 dark:shadow-[4px_4px_0_#a3c51f]">
                  {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Languages className="h-4 w-4" />}
                  {loading ? 'Translating…' : 'Translate'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}
