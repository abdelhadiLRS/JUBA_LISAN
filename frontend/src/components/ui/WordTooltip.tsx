'use client'

import { useState, useCallback } from 'react'
import { Check, Loader2, Save, X, AlertCircle } from 'lucide-react'
import { apiFetch, readApiError, saveTranslatedWordLocally } from '@/lib/api'
import { useLanguageStore } from '@/store/language'

export type SaveState = 'idle' | 'saving' | 'saved' | 'error'

export interface TooltipPos { x: number; y: number }

export function WordTooltip({ word, pos, saveState, onSave, onDismiss, labels }: { word: string; pos: TooltipPos; saveState: SaveState; onSave: () => void; onDismiss: () => void; labels: { saveWord: string; wordSaved: string; wordSaveError: string } }) {
  return (
    <div style={{ left: pos.x, top: pos.y }} className="pointer-events-auto fixed z-50 -translate-x-1/2 -translate-y-full">
      <div className="juba-card flex items-center gap-3 border-2 border-[var(--juba-app-line)] px-3 py-2.5 text-xs shadow-[4px_4px_0_var(--juba-app-line)]">
        <span className="text-[var(--juba-app-ink)] font-semibold">{word}</span>
        {saveState === 'idle' && <button type="button" onClick={onSave} className="inline-flex items-center gap-1.5 border-2 border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] text-[var(--juba-app-green-dark)] hover:bg-[var(--juba-app-green-soft)] rounded-xl px-2.5 py-1 shadow-[2px_2px_0_var(--juba-app-line)] text-[11px] font-semibold tracking-wide uppercase transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)] focus-visible:ring-offset-1"><Save className="h-3.5 w-3.5" aria-hidden="true" />{labels.saveWord}</button>}
        {saveState === 'saving' && <span className="inline-flex items-center gap-1.5 text-[var(--juba-app-muted)] tracking-widest uppercase"><Loader2 className="h-3.5 w-3.5 animate-spin" aria-hidden="true" />Saving</span>}
        {saveState === 'saved' && <span className="inline-flex items-center gap-1.5 text-[var(--juba-app-green-dark)] font-semibold tracking-wide uppercase"><Check className="h-3.5 w-3.5" aria-hidden="true" />{labels.wordSaved}</span>}
        {saveState === 'error' && <span className="inline-flex items-center gap-1.5 text-[#b33a32] font-semibold tracking-wide uppercase"><AlertCircle className="h-3.5 w-3.5" aria-hidden="true" />{labels.wordSaveError}</span>}
        <button type="button" onClick={onDismiss} className="ml-1 rounded-lg border-2 border-transparent px-1 text-[var(--juba-app-muted)] transition-colors hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-ink)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)] focus-visible:ring-offset-1" aria-label="dismiss"><X className="h-3.5 w-3.5" aria-hidden="true" /></button>
      </div>
      <div className="border-t-[var(--juba-app-line)] mx-auto mt-px h-0 w-0 border-x-4 border-t-4 border-x-transparent" />
    </div>
  )
}

export function useWordSave() {
  const [selectedWord, setSelectedWord] = useState<string | null>(null)
  const [selectedContext, setSelectedContext] = useState('')
  const [selectedCefrLevel, setSelectedCefrLevel] = useState('B1')
  const [tooltipPos, setTooltipPos] = useState<TooltipPos>({ x: 0, y: 0 })
  const [saveState, setSaveState] = useState<SaveState>('idle')
  const activeLanguage = useLanguageStore((state) => state.activeLanguage)

  const dismissTooltip = useCallback(() => {
    setSelectedWord(null)
    setSaveState('idle')
    window.getSelection()?.removeAllRanges()
  }, [])

  function handleTextSelection(context: string, cefrLevel = 'B1') {
    window.setTimeout(() => {
      const selection = window.getSelection()
      if (!selection || selection.isCollapsed || selection.rangeCount === 0) return
      const raw = selection.toString().trim()
      if (!raw || /\s/.test(raw)) return
      const range = selection.getRangeAt(0)
      const rect = range.getBoundingClientRect()
      setSelectedContext(context)
      setSelectedCefrLevel(cefrLevel)
      setSelectedWord(raw)
      setSaveState('idle')
      setTooltipPos({ x: rect.left + rect.width / 2, y: Math.max(rect.top - 8, 56) })
    }, 0)
  }

  async function saveGuestWord(word: string) {
    const target = activeLanguage?.iso639 || 'ar'
    const res = await apiFetch('/api/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: word, source: 'auto', target }),
    })
    if (!res.ok) throw new Error()
    const data = await res.json() as { translation?: string; source?: string; target?: string }
    if (!data.translation?.trim()) throw new Error()
    saveTranslatedWordLocally({ word, translation: data.translation.trim(), source: data.source || 'auto', target: data.target || target })
  }

  async function handleSaveWord() {
    if (!selectedWord) return
    setSaveState('saving')
    try {
      const res = await apiFetch('/api/flashcards/from-word', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word: selectedWord, context: selectedContext, cefr_level: selectedCefrLevel }),
      })
      if (res.ok) {
        setSaveState('saved')
        setTimeout(() => dismissTooltip(), 1500)
        return
      }
      if (res.status === 401 || res.status === 403) {
        await saveGuestWord(selectedWord)
        setSaveState('saved')
        setTimeout(() => dismissTooltip(), 1500)
        return
      }
      if (res.status === 404 && (await readApiError(res)) === 'No active study plan found') {
        await saveGuestWord(selectedWord)
        setSaveState('saved')
        setTimeout(() => dismissTooltip(), 1500)
        return
      }
      throw new Error()
    } catch {
      setSaveState('error')
    }
  }

  return { selectedWord, tooltipPos, saveState, handleTextSelection, handleSaveWord, dismissTooltip }
}
