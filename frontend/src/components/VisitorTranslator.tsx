'use client'

import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { useTranslations } from 'next-intl'
import { ArrowRightLeft, BookOpenCheck, Check, Copy, Languages, Loader2, Volume2, X } from 'lucide-react'
import Link from 'next/link'
import { saveTranslatedWordLocally } from '@/lib/api'
import { TARGET_LANGUAGE_CATALOG } from '@/lib/target-languages'

const LANGUAGES = TARGET_LANGUAGE_CATALOG.map((language) => ({
  code: language.iso639,
  label: language.name,
}))
const UNIQUE_LANGUAGES = LANGUAGES.filter(
  (language, index, all) => all.findIndex((item) => item.code === language.code) === index,
)

function languageLabel(code: string) {
  return UNIQUE_LANGUAGES.find((language) => language.code === code)?.label ?? code.toUpperCase()
}

export function VisitorTranslator() {
  const t = useTranslations('visitorTranslator')
  const [open, setOpen] = useState(false)
  const [text, setText] = useState('')
  const [source, setSource] = useState('auto')
  const [target, setTarget] = useState('ar')
  const [translation, setTranslation] = useState('')
  const [detectedSource, setDetectedSource] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (!open) return
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpen(false)
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [open])

  async function translate(event?: FormEvent) {
    event?.preventDefault()
    if (!text.trim()) return
    setLoading(true)
    setError('')
    setSaved(false)
    try {
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, source, target }),
      })
      const contentType = response.headers.get('content-type') || ''
      const raw = await response.text()
      let data: { translation?: unknown; source?: unknown; detail?: unknown; error?: unknown } = {}
      if (contentType.includes('application/json')) {
        try {
          data = JSON.parse(raw) as typeof data
        } catch {
          data = {}
        }
      }
      if (!response.ok) {
        const serverMessage =
          typeof data.detail === 'string'
            ? data.detail
            : typeof data.error === 'string'
              ? data.error
              : raw.trim()
        throw new Error(serverMessage || t('translationFailed'))
      }
      if (typeof data.translation !== 'string') {
        throw new Error(t('translationFailed'))
      }
      setTranslation(data.translation)
      setDetectedSource(typeof data.source === 'string' ? data.source : source)
    } catch (err) {
      setTranslation('')
      setDetectedSource('')
      setError(err instanceof Error ? err.message : t('translationFailed'))
    } finally {
      setLoading(false)
    }
  }

  function saveToLearning() {
    if (!text.trim() || !translation.trim()) return
    saveTranslatedWordLocally({
      source: detectedSource || source,
      target,
      word: text.trim(),
      translation: translation.trim(),
    })
    setSaved(true)
  }

  function swapLanguages() {
    if (source === 'auto') return
    setSource(target)
    setTarget(source)
    setTranslation('')
    setDetectedSource('')
    setSaved(false)
  }

  async function copyTranslation() {
    if (!translation) return
    try {
      await navigator.clipboard?.writeText(translation)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 1600)
    } catch {
      setCopied(false)
    }
  }

  function speakTranslation() {
    if (!translation || typeof window === 'undefined' || !('speechSynthesis' in window)) return
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(translation)
    utterance.lang = target
    window.speechSynthesis.speak(utterance)
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label={t('open')}
        className="fixed bottom-5 end-5 z-40 inline-flex items-center gap-2 rounded-2xl border border-[var(--juba-app-ink)] bg-white px-5 py-3 text-sm font-black text-[var(--juba-app-ink)] shadow-[0_8px_24px_rgba(24,37,27,.16)] transition hover:-translate-y-0.5 hover:shadow-[0_12px_30px_rgba(24,37,27,.2)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)] focus-visible:ring-offset-2"
      >
        <Languages className="h-4 w-4" aria-hidden="true" />
        {t('translate')}
      </button>

      {open && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-black/45 p-3 backdrop-blur-sm sm:p-6"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) setOpen(false)
          }}
        >
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="visitor-translator-title"
            aria-describedby="visitor-translator-description"
            className="w-full max-w-6xl overflow-hidden rounded-[22px] border border-black/10 bg-white shadow-[0_28px_80px_rgba(0,0,0,.22)]"
          >
            <header className="flex items-center justify-between border-b border-black/10 px-5 py-4 sm:px-7">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[var(--juba-app-green)] text-white">
                  <Languages className="h-5 w-5" aria-hidden="true" />
                </div>
                <div>
                  <h2 id="visitor-translator-title" className="text-xl font-black tracking-tight text-[var(--juba-app-ink)] sm:text-2xl">
                    {t('title')}
                  </h2>
                  <p id="visitor-translator-description" className="sr-only">{t('description')}</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setOpen(false)}
                aria-label={t('close')}
                className="rounded-full p-2 text-black/55 transition hover:bg-black/5 hover:text-black focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)]"
              >
                <X className="h-5 w-5" aria-hidden="true" />
              </button>
            </header>

            <div className="border-b border-black/10 px-5 pt-4 sm:px-7">
              <div className="flex gap-6 text-sm font-bold">
                <button type="button" className="border-b-2 border-[var(--juba-app-green)] pb-3 text-[var(--juba-app-ink)]">
                  {t('translate')}
                </button>
              </div>
            </div>

            <form onSubmit={translate} className="p-4 sm:p-7">
              <div className="grid overflow-hidden rounded-2xl border border-black/10 lg:grid-cols-[1fr_auto_1fr]">
                <section className="flex min-h-[360px] flex-col bg-white">
                  <div className="flex flex-wrap items-center justify-between gap-3 border-b border-black/10 px-4 py-3 sm:px-5">
                    <label className="sr-only" htmlFor="visitor-translator-source">{t('sourceLanguage')}</label>
                    <select
                      id="visitor-translator-source"
                      value={source}
                      onChange={(e) => {
                        setSource(e.target.value)
                        setTranslation('')
                        setDetectedSource('')
                        setSaved(false)
                      }}
                      className="min-w-[150px] rounded-lg bg-transparent px-2 py-2 text-sm font-bold text-[var(--juba-app-ink)] outline-none hover:bg-black/5 focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)]"
                    >
                      <option value="auto">{t('autoDetect')}</option>
                      {UNIQUE_LANGUAGES.map((language) => (
                        <option key={language.code} value={language.code}>{language.label}</option>
                      ))}
                    </select>
                    <span className="text-xs font-medium text-black/45">
                      {detectedSource && source === 'auto' ? `${t('detected')}: ${languageLabel(detectedSource)}` : ''}
                    </span>
                  </div>
                  <textarea
                    value={text}
                    onChange={(e) => {
                      setText(e.target.value)
                      setSaved(false)
                    }}
                    maxLength={2000}
                    rows={8}
                    autoFocus
                    placeholder={t('inputPlaceholder')}
                    aria-label={t('textToTranslate')}
                    className="min-h-[255px] flex-1 resize-none bg-transparent px-5 py-5 text-lg leading-8 text-[var(--juba-app-ink)] outline-none placeholder:text-black/35 focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-[var(--juba-app-green)]"
                  />
                  <div className="flex items-center justify-between px-5 pb-4 text-xs text-black/40">
                    <span>{text.length}/2000</span>
                    <span>{source === 'auto' ? t('automaticDetection') : languageLabel(source)}</span>
                  </div>
                </section>

                <div className="flex items-center justify-center border-y border-black/10 bg-[#fafafa] p-3 lg:border-x lg:border-y-0">
                  <button
                    type="button"
                    onClick={swapLanguages}
                    disabled={source === 'auto' || loading}
                    aria-label={t('swap')}
                    className="rounded-full border border-black/10 bg-white p-2.5 text-[var(--juba-app-ink)] shadow-sm transition hover:scale-105 disabled:opacity-35"
                  >
                    <ArrowRightLeft className="h-4 w-4" aria-hidden="true" />
                  </button>
                </div>

                <section className="flex min-h-[360px] flex-col bg-[#fafafa]">
                  <div className="flex items-center justify-between border-b border-black/10 px-4 py-3 sm:px-5">
                    <label className="sr-only" htmlFor="visitor-translator-target">{t('targetLanguage')}</label>
                    <select
                      id="visitor-translator-target"
                      value={target}
                      onChange={(e) => {
                        setTarget(e.target.value)
                        setTranslation('')
                        setSaved(false)
                      }}
                      className="min-w-[150px] rounded-lg bg-transparent px-2 py-2 text-sm font-bold text-[var(--juba-app-ink)] outline-none hover:bg-black/5 focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)]"
                    >
                      {UNIQUE_LANGUAGES.map((language) => (
                        <option key={language.code} value={language.code}>{language.label}</option>
                      ))}
                    </select>
                    <span className="text-xs text-black/40">{languageLabel(target)}</span>
                  </div>
                  <div className="flex flex-1 items-start px-5 py-5">
                    {error ? (
                      <p className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-bold text-red-700" role="alert">{error}</p>
                    ) : translation ? (
                      <div className="w-full">
                        <p className="text-lg leading-8 text-[var(--juba-app-ink)] sm:text-xl">{translation}</p>
                        <div className="mt-6 flex flex-wrap items-center gap-2">
                          <button type="button" onClick={speakTranslation} aria-label="Listen" className="rounded-lg p-2 text-black/55 transition hover:bg-black/10 hover:text-black">
                            <Volume2 className="h-5 w-5" aria-hidden="true" />
                          </button>
                          <button type="button" onClick={copyTranslation} aria-label="Copy" className="rounded-lg p-2 text-black/55 transition hover:bg-black/10 hover:text-black">
                            {copied ? <Check className="h-5 w-5" aria-hidden="true" /> : <Copy className="h-5 w-5" aria-hidden="true" />}
                          </button>
                          <button type="button" onClick={saveToLearning} className="inline-flex items-center gap-2 rounded-lg bg-white px-3 py-2 text-xs font-black text-[var(--juba-app-ink)] shadow-sm ring-1 ring-black/10 hover:bg-black/5">
                            <BookOpenCheck className="h-4 w-4" aria-hidden="true" />
                            {saved ? t('savedLocally') : t('learnThis')}
                          </button>
                        </div>
                        {saved && <p className="mt-3 text-xs font-bold text-[var(--juba-app-ink)]" role="status">{t('savedNote')}</p>}
                      </div>
                    ) : (
                      <p className="text-lg text-black/35">{t('translationPlaceholder')}</p>
                    )}
                  </div>
                </section>
              </div>

              <div className="mt-4 flex flex-col-reverse gap-3 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-xs text-black/45">{t('workflow')}</p>
                <button
                  type="submit"
                  disabled={!text.trim() || loading}
                  className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--juba-app-green)] px-7 py-3 text-sm font-black text-white transition hover:opacity-90 disabled:opacity-45"
                >
                  {loading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Languages className="h-4 w-4" aria-hidden="true" />}
                  {loading ? t('translating') : t('translate')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}
