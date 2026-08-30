'use client'

import { FormEvent, useState } from 'react'
import { ArrowRightLeft, Languages, Loader2, X } from 'lucide-react'

const LANGUAGES = [
  { code: 'ar', label: 'العربية' },
  { code: 'en', label: 'English' },
  { code: 'fr', label: 'Français' },
  { code: 'es', label: 'Español' },
  { code: 'it', label: 'Italiano' },
  { code: 'de', label: 'Deutsch' },
  { code: 'pt', label: 'Português' },
]

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
        className="fixed bottom-5 end-5 z-40 inline-flex items-center gap-2 rounded-full border border-black/10 bg-[#d8f53f] px-4 py-3 text-sm font-extrabold text-neutral-950 shadow-[0_10px_30px_rgba(0,0,0,.16)] transition-transform hover:-translate-y-0.5 dark:border-white/10"
      >
        <Languages className="h-4 w-4" />
        Translate
      </button>

      {open && (
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-neutral-950/35 p-4 backdrop-blur-sm sm:items-center">
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="visitor-translator-title"
            className="w-full max-w-2xl rounded-[28px] border border-black/10 bg-[#f8f7f1] p-5 shadow-2xl dark:border-white/10 dark:bg-neutral-900 sm:p-7"
          >
            <div className="mb-5 flex items-start justify-between gap-4">
              <div>
                <p className="mb-1 text-xs font-black uppercase tracking-[0.18em] text-neutral-500">JUBA LISAN</p>
                <h2 id="visitor-translator-title" className="text-2xl font-black tracking-tight text-neutral-950 dark:text-white">Instant translation</h2>
                <p className="mt-1 text-sm text-neutral-600 dark:text-neutral-400">Translate a word, phrase, or short sentence before you start learning.</p>
              </div>
              <button type="button" onClick={() => setOpen(false)} aria-label="Close translator" className="rounded-full border border-black/10 p-2 text-neutral-700 hover:bg-white dark:border-white/10 dark:text-neutral-200 dark:hover:bg-neutral-800">
                <X className="h-5 w-5" />
              </button>
            </div>

            <form onSubmit={translate} className="space-y-4">
              <div className="flex flex-wrap items-center gap-2 rounded-2xl border border-black/10 bg-white p-2 dark:border-white/10 dark:bg-neutral-950">
                <select value={source} onChange={(e) => { setSource(e.target.value); setTranslation('') }} className="min-w-32 flex-1 rounded-xl bg-transparent px-3 py-2.5 text-sm font-bold outline-none">
                  <option value="auto">Auto detect</option>
                  {LANGUAGES.map((language) => <option key={language.code} value={language.code}>{language.label}</option>)}
                </select>
                <button type="button" onClick={swapLanguages} disabled={source === 'auto'} aria-label="Swap languages" className="rounded-xl border border-black/10 p-2 disabled:cursor-not-allowed disabled:opacity-40 dark:border-white/10">
                  <ArrowRightLeft className="h-4 w-4" />
                </button>
                <select value={target} onChange={(e) => { setTarget(e.target.value); setTranslation('') }} className="min-w-32 flex-1 rounded-xl bg-transparent px-3 py-2.5 text-sm font-bold outline-none">
                  {LANGUAGES.map((language) => <option key={language.code} value={language.code}>{language.label}</option>)}
                </select>
              </div>

              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                maxLength={2000}
                rows={5}
                placeholder="Type something to translate…"
                className="w-full resize-none rounded-2xl border border-black/10 bg-white p-4 text-base outline-none ring-offset-2 focus:ring-2 focus:ring-[#b9d528] dark:border-white/10 dark:bg-neutral-950"
              />

              <div className="flex items-center justify-between gap-3">
                <span className="text-xs text-neutral-500">{text.length}/2000</span>
                <button type="submit" disabled={!text.trim() || loading} className="inline-flex items-center gap-2 rounded-full bg-neutral-950 px-5 py-3 text-sm font-extrabold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-45 dark:bg-white dark:text-neutral-950">
                  {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Languages className="h-4 w-4" />}
                  {loading ? 'Translating…' : 'Translate now'}
                </button>
              </div>
            </form>

            {(translation || error) && (
              <div className="mt-5 rounded-2xl border border-black/10 bg-[#d8f53f]/45 p-5 dark:border-white/10 dark:bg-lime-300/10">
                <p className="mb-2 text-xs font-black uppercase tracking-[0.16em] text-neutral-600 dark:text-neutral-400">Translation</p>
                {error ? <p className="text-sm font-semibold text-red-600 dark:text-red-400">{error}</p> : <p className="text-lg font-bold leading-relaxed text-neutral-950 dark:text-white">{translation}</p>}
              </div>
            )}

            <p className="mt-4 text-[11px] leading-relaxed text-neutral-500">Visitor translation is intended for quick lookups. Learning, vocabulary mastery, and review remain inside the JUBA LISAN learning experience.</p>
          </div>
        </div>
      )}
    </>
  )
}
