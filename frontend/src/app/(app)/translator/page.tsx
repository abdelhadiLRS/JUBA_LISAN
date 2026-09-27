'use client'

import { useEffect, useMemo, useState } from 'react'
import { apiFetch, ensureGuestCookie, saveTranslatedWordLocally } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

const LANGUAGES = [['auto', 'Detect language'], ['ar', 'العربية'], ['en', 'English'], ['fr', 'Français'], ['es', 'Español'], ['it', 'Italiano'], ['de', 'Deutsch'], ['pt', 'Português'], ['tr', 'Türkçe'], ['ru', 'Русский']] as const

export default function TranslatorPage() {
  const [text, setText] = useState(''); const [source, setSource] = useState('auto'); const [target, setTarget] = useState('ar'); const [translation, setTranslation] = useState(''); const [loading, setLoading] = useState(false); const [saving, setSaving] = useState(false); const [error, setError] = useState(''); const [saved, setSaved] = useState(false)
  const user = useAuthStore((s) => s.user)
  const sourceLabel = useMemo(() => LANGUAGES.find(([code]) => code === source)?.[1] ?? source, [source]); const targetLabel = useMemo(() => LANGUAGES.find(([code]) => code === target)?.[1] ?? target, [target])
  useEffect(() => { if (!user) ensureGuestCookie() }, [user])
  async function translate() { if (!text.trim()) return; setLoading(true); setError(''); setSaved(false); try { const response = await fetch('/api/translate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: text.trim(), source, target }) }); const data = await response.json(); if (!response.ok) throw new Error(data?.error || 'Translation failed.'); setTranslation(data.translation || '') } catch (err) { setError(err instanceof Error ? err.message : 'Unable to translate right now.') } finally { setLoading(false) } }
  function swapLanguages() { if (source === 'auto') return; setSource(target); setTarget(source); setText(translation); setTranslation(text) }
  function speak(value: string, lang: string) { if (!value || typeof window === 'undefined' || !('speechSynthesis' in window)) return; window.speechSynthesis.cancel(); const utterance = new SpeechSynthesisUtterance(value); utterance.lang = lang === 'auto' ? 'en' : lang; window.speechSynthesis.speak(utterance) }
  async function saveWord() { if (!text.trim() || !translation.trim() || saving) return; setSaving(true); setError(''); try { if (user) { const response = await apiFetch('/api/flashcards/from-word', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ word: text.trim(), context: translation.trim(), cefr_level: 'B1' }) }); if (!response.ok) throw new Error('Could not save this word to your learning deck.'); setSaved(true) } else { ensureGuestCookie(); saveTranslatedWordLocally({ word: text.trim(), translation: translation.trim(), source, target }); setSaved(true) } } catch (err) { if (!user) saveTranslatedWordLocally({ word: text.trim(), translation: translation.trim(), source, target }); setError(err instanceof Error ? err.message : 'Unable to save this word right now.') } finally { setSaving(false) } }

  return (
    <main className="juba-mobile-translator juba-page-shell">
      <section className="juba-page-hero">
        <span className="juba-eyebrow">JUBA LISAN · Instant Translator</span>
        <h1 className="juba-page-title">Translate. Understand. Learn.</h1>
        <p className="juba-page-subtitle">ترجمة فورية للزوار بدون تسجيل. احفظ الكلمات اختيارياً لتبني ذاكرتك اللغوية.</p>
      </section>

      <section className="juba-translator-grid" aria-label="Instant translator">
        <div className="juba-panel juba-translator-panel">
          <div className="juba-translator-toolbar">
            <label className="juba-section-title">{sourceLabel}</label>
            <select value={source} onChange={(e) => setSource(e.target.value)} className="juba-input juba-translator-select">
              {LANGUAGES.map(([code, label]) => <option key={code} value={code}>{label}</option>)}
            </select>
          </div>
          <textarea value={text} onChange={(e) => setText(e.target.value)} onKeyDown={(e) => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') translate() }} maxLength={2000} placeholder="Type or paste anything…" className="juba-translator-textarea" dir="auto" />
          <div className="juba-translator-footer">
            <span>{text.length}/2000</span>
            <button type="button" onClick={() => speak(text, source)} disabled={!text.trim()} className="juba-secondary-button juba-translator-tool">🔊 Listen</button>
          </div>
        </div>

        <div className="juba-translator-swap-wrap">
          <button type="button" onClick={swapLanguages} disabled={source === 'auto'} aria-label="Swap languages" className="juba-primary-button juba-translator-swap">↔</button>
        </div>

        <div className="juba-panel juba-translator-panel">
          <div className="juba-translator-toolbar">
            <label className="juba-section-title">{targetLabel}</label>
            <select value={target} onChange={(e) => setTarget(e.target.value)} className="juba-input juba-translator-select">
              {LANGUAGES.filter(([code]) => code !== 'auto').map(([code, label]) => <option key={code} value={code}>{label}</option>)}
            </select>
          </div>
          <div className="juba-translator-result" dir="auto">
            {loading ? <span className="juba-muted">Translating…</span> : translation || <span className="juba-muted">Your translation will appear here.</span>}
          </div>
          <div className="juba-translator-footer">
            <button type="button" onClick={() => speak(translation, target)} disabled={!translation} className="juba-secondary-button juba-translator-tool">🔊 Listen</button>
            <button type="button" onClick={saveWord} disabled={!translation || saving} className="juba-primary-button juba-translator-learn">{saving ? 'Saving…' : '⭐ Learn this'}</button>
          </div>
        </div>
      </section>

      <div className="juba-translator-actions">
        <button type="button" onClick={translate} disabled={!text.trim() || loading} className="juba-primary-button juba-translator-submit">{loading ? 'Translating…' : 'Translate now →'}</button>
        <p className="juba-muted">No account required · Translation stays open to everyone.</p>
      </div>

      {saved && <div className="juba-panel juba-translator-status">✓ {user ? 'Added to your JUBA learning deck.' : 'Added to JUBA Memory — saved locally on this device.'}</div>}
      {error && <div role="alert" className="juba-panel juba-translator-error">{error}</div>}
    </main>
  )
}
