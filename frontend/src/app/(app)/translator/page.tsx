'use client'

import { useEffect, useMemo, useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch, ensureGuestCookie, saveTranslatedWordLocally } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

const LANGUAGES = [['auto', 'Detect language'], ['ar', 'العربية'], ['en', 'English'], ['fr', 'Français'], ['es', 'Español'], ['it', 'Italiano'], ['de', 'Deutsch'], ['pt', 'Português'], ['tr', 'Türkçe'], ['ru', 'Русский']] as const

export default function TranslatorPage() {
  const t = useTranslations('translator')
  const [text, setText] = useState(''); const [source, setSource] = useState('auto'); const [target, setTarget] = useState('ar'); const [translation, setTranslation] = useState(''); const [detectedSource, setDetectedSource] = useState(''); const [loading, setLoading] = useState(false); const [saving, setSaving] = useState(false); const [error, setError] = useState(''); const [saved, setSaved] = useState(false)
  const user = useAuthStore((s) => s.user)
  const sourceLabel = useMemo(() => LANGUAGES.find(([code]) => code === source)?.[1] ?? source, [source]); const targetLabel = useMemo(() => LANGUAGES.find(([code]) => code === target)?.[1] ?? target, [target])
  useEffect(() => { if (!user) ensureGuestCookie() }, [user])
  async function translate() {
    if (!text.trim()) return
    setLoading(true)
    setError('')
    setSaved(false)
    try {
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text.trim(), source, target }),
      })
      const contentType = response.headers.get('content-type') || ''
      const raw = await response.text()
      let data: { translation?: unknown; source?: unknown; detail?: unknown; error?: unknown } = {}
      if (contentType.includes('application/json')) {
        try { data = JSON.parse(raw) as typeof data } catch { data = {} }
      }
      if (!response.ok) {
        const message = typeof data.detail === 'string'
          ? data.detail
          : typeof data.error === 'string'
            ? data.error
            : raw.trim()
        throw new Error(message || t('translationFailed'))
      }
      if (typeof data.translation !== 'string' || !data.translation.trim()) {
        throw new Error(t('translationFailed'))
      }
      setTranslation(data.translation)
      setDetectedSource(typeof data.source === 'string' ? data.source : source)
    } catch (err) {
      setTranslation('')
      setDetectedSource('')
      setError(err instanceof Error ? err.message : t('translationUnavailable'))
    } finally {
      setLoading(false)
    }
  }
  function swapLanguages() { if (source === 'auto') return; setSource(target); setTarget(source); setDetectedSource(''); setText(translation); setTranslation(text) }
  function speak(value: string, lang: string) { if (!value || typeof window === 'undefined' || !('speechSynthesis' in window)) return; window.speechSynthesis.cancel(); const utterance = new SpeechSynthesisUtterance(value); utterance.lang = lang === 'auto' ? 'en' : lang; window.speechSynthesis.speak(utterance) }
  async function saveWord() { if (!text.trim() || !translation.trim() || saving) return; setSaving(true); setError(''); try { if (user) { const response = await apiFetch('/api/flashcards/from-word', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ word: text.trim(), context: translation.trim(), cefr_level: 'B1' }) }); if (!response.ok) throw new Error(t('saveFailed')); setSaved(true) } else { ensureGuestCookie(); saveTranslatedWordLocally({ word: text.trim(), translation: translation.trim(), source: detectedSource || source, target }); setSaved(true) } } catch (err) { if (!user) saveTranslatedWordLocally({ word: text.trim(), translation: translation.trim(), source, target }); setError(err instanceof Error ? err.message : t('saveUnavailable')) } finally { setSaving(false) } }
  return <main className="card"><section className="card"><div className="juba-hero-glow -right-20 -top-20" aria-hidden="true" /><div className="relative z-10"><span className="page-pretitle">{t('eyebrow')}</span><h1 className="mt-5 text-4xl font-black tracking-tight sm:text-6xl">{t('title')}</h1><p className="mt-4 max-w-2xl text-base font-medium text-[rgba(32,33,39,.52)]">{t('description')}</p></div></section><section className="mt-6 grid gap-5 lg:grid-cols-[1fr_auto_1fr] lg:items-stretch" aria-label={t('ariaLabel')}><div className="card"><div className="flex items-center justify-between gap-3"><label className="text-sm font-black">{sourceLabel}</label><select value={source} onChange={(e) => setSource(e.target.value)} className="border border bg-white px-3 py-2 text-sm font-bold">{LANGUAGES.map(([code, label]) => <option key={code} value={code}>{label}</option>)}</select></div><textarea value={text} onChange={(e) => setText(e.target.value)} onKeyDown={(e) => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') translate() }} maxLength={2000} placeholder={t('inputPlaceholder')} className="mt-5 min-h-[235px] flex-1 resize-none border border bg-white p-5 text-xl font-semibold outline-none placeholder:text-[rgba(32,33,39,.52)]" dir="auto" /><div className="mt-3 flex items-center justify-between text-xs font-bold text-[rgba(32,33,39,.52)]"><span>{text.length}/2000</span><span>{source === 'auto' && detectedSource ? `t('detected', { language: detectedSource.toUpperCase() })` : sourceLabel}</span><button type="button" onClick={() => speak(text, source)} disabled={!text.trim()} className="rounded-full border border px-4 py-2 font-black disabled:opacity-40">🔊 {t('listen')}</button></div></div><div className="flex items-center justify-center"><button type="button" onClick={swapLanguages} disabled={source === 'auto'} aria-label={t('swap')} className="h-14 w-14 rounded-full border border bg-[#5862e2] text-2xl font-black shadow-[3px_3px_0_#202127] disabled:opacity-40">↔</button></div><div className="card"><div className="flex items-center justify-between gap-3"><label className="text-sm font-black">{targetLabel}</label><select value={target} onChange={(e) => setTarget(e.target.value)} className="border border bg-white px-3 py-2 text-sm font-bold">{LANGUAGES.filter(([code]) => code !== 'auto').map(([code, label]) => <option key={code} value={code}>{label}</option>)}</select></div><div className="mt-5 flex min-h-[235px] flex-1 items-start border border bg-white p-5 text-xl font-semibold" dir="auto">{loading ? <span className="animate-pulse">{t('translating')}</span> : translation || <span className="text-[rgba(32,33,39,.52)]">{t('translationPlaceholder')}</span>}</div><div className="mt-3 flex flex-wrap items-center justify-between gap-2"><button type="button" onClick={() => speak(translation, target)} disabled={!translation} className="rounded-full border border px-4 py-2 font-black disabled:opacity-40">🔊 Listen</button><button type="button" onClick={saveWord} disabled={!translation || saving} className="rounded-full border border bg-[#5862e2] px-5 py-2 font-black disabled:opacity-40">{saving ? t('saving') : `⭐ ${t('save')}`}</button></div></div></section><div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"><button type="button" onClick={translate} disabled={!text.trim() || loading} className="min-h-14 rounded-[28px] border border bg-[#5862e2] px-8 text-lg font-black shadow-[4px_4px_0_#202127] disabled:opacity-50">{loading ? t('translating') : t('translateNow')}</button><p className="text-sm font-semibold text-[rgba(32,33,39,.52)]">{t('visitorNote')}</p></div>{saved && <div className="card">✓ {user ? t('savedCloud') : t('savedLocal')}</div>}{error && <div role="alert" className="card">{error}</div>}</main>
}
