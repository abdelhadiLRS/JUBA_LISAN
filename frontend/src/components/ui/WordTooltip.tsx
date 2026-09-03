'use client'

import { useState, useCallback } from 'react'
import { apiFetch, saveTranslatedWordLocally } from '@/lib/api'

export type SaveState = 'idle' | 'saving' | 'saved' | 'error'

export interface TooltipPos { x: number; y: number }

export function WordTooltip({ word, pos, saveState, onSave, onDismiss, labels }: { word: string; pos: TooltipPos; saveState: SaveState; onSave: () => void; onDismiss: () => void; labels: { saveWord: string; wordSaved: string; wordSaveError: string } }) {
  return (
    <div style={{ left: pos.x, top: pos.y }} className="pointer-events-auto fixed z-50 -translate-x-1/2 -translate-y-full">
      <div className="border-fl-border bg-fl-surface flex items-center gap-3 border px-3 py-2 font-mono text-xs shadow-lg">
        <span className="text-fl-fg font-bold">{word}</span>
        {saveState === 'idle' && <button onClick={onSave} className="text-fl-muted-2 hover:text-fl-fg border-fl-border border px-2 py-0.5 tracking-widest uppercase transition-colors">{labels.saveWord}</button>}
        {saveState === 'saving' && <span className="text-fl-muted-3 animate-pulse tracking-widest uppercase">...</span>}
        {saveState === 'saved' && <span className="tracking-widest text-green-400 uppercase">✓ {labels.wordSaved}</span>}
        {saveState === 'error' && <span className="tracking-widest text-red-400 uppercase">{labels.wordSaveError}</span>}
        <button onClick={onDismiss} className="text-fl-muted-3 hover:text-fl-fg ml-1 transition-colors" aria-label="dismiss">✕</button>
      </div>
      <div className="border-t-fl-border mx-auto mt-px h-0 w-0 border-x-4 border-t-4 border-x-transparent" />
    </div>
  )
}

export function useWordSave() {
  const [selectedWord, setSelectedWord] = useState<string | null>(null)
  const [selectedContext, setSelectedContext] = useState('')
  const [selectedCefrLevel, setSelectedCefrLevel] = useState('B1')
  const [tooltipPos, setTooltipPos] = useState<TooltipPos>({ x: 0, y: 0 })
  const [saveState, setSaveState] = useState<SaveState>('idle')

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
    const res = await apiFetch('/api/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: word, source: 'auto', target: 'ar' }),
    })
    if (!res.ok) throw new Error()
    const data = await res.json() as { translation?: string; source?: string; target?: string }
    if (!data.translation?.trim()) throw new Error()
    saveTranslatedWordLocally({ word, translation: data.translation.trim(), source: data.source || 'auto', target: data.target || 'ar' })
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
      throw new Error()
    } catch {
      setSaveState('error')
    }
  }

  return { selectedWord, tooltipPos, saveState, handleTextSelection, handleSaveWord, dismissTooltip }
}
