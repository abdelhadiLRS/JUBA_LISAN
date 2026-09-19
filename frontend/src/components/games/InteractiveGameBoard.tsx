'use client'

import { useEffect, useState } from 'react'
import type { InteractiveGameChallenge, InteractiveGameTrace } from '@/lib/games/persist'

type Mode = 'memory' | 'matching' | 'ordering'
type Lang = 'ar' | 'fr' | 'en'
type Props = {
  mode: Mode
  lang: Lang
  challenge?: InteractiveGameChallenge
  onComplete?: (trace: InteractiveGameTrace[]) => Promise<boolean> | boolean | void
}
type MemoryCard = { id: string; label: string; pair_key?: string; flipped: boolean; matched: boolean }

const copy = {
  ar: { memory: 'الذاكرة', matching: 'المطابقة', ordering: 'الترتيب', reset: 'إعادة', moves: 'المحاولات', match: 'طابق العنصرين المتشابهين', chooseLeft: 'اختر كلمة', chooseRight: 'اختر ترجمتها', order: 'اضغط العناصر بالترتيب الصحيح', complete: 'أحسنت! أكملت التحدي.', up: 'أعلى', down: 'أسفل', undo: 'تراجع', clear: 'مسح' },
  fr: { memory: 'Mémoire', matching: 'Association', ordering: 'Classement', reset: 'Réinitialiser', moves: 'Coups', match: 'Associe les deux éléments', chooseLeft: 'Choisis un mot', chooseRight: 'Choisis sa traduction', order: 'Appuie sur les éléments dans le bon ordre', complete: 'Bravo ! Défi terminé.', up: 'Monter', down: 'Descendre', undo: 'Annuler', clear: 'Effacer' },
  en: { memory: 'Memory', matching: 'Matching', ordering: 'Ordering', reset: 'Reset', moves: 'Moves', match: 'Match the two items', chooseLeft: 'Choose a word', chooseRight: 'Choose its translation', order: 'Tap the items in the correct order', complete: 'Great job! Challenge complete.', up: 'Up', down: 'Down', undo: 'Undo', clear: 'Clear' },
} as const

export function InteractiveGameBoard({ mode, lang, challenge, onComplete }: Props) {
  const t = copy[lang]
  const [memoryCards, setMemoryCards] = useState<MemoryCard[]>([])
  const [first, setFirst] = useState<string | null>(null)
  const [locked, setLocked] = useState(false)
  const [moves, setMoves] = useState(0)
  const [memoryTrace, setMemoryTrace] = useState<InteractiveGameTrace[]>([])
  const [left, setLeft] = useState<string | null>(null)
  const [right, setRight] = useState<string | null>(null)
  const [matched, setMatched] = useState<string[]>([])
  const [matchingTrace, setMatchingTrace] = useState<InteractiveGameTrace[]>([])
  const [order, setOrder] = useState<string[]>([])
  const [orderingTrace, setOrderingTrace] = useState<InteractiveGameTrace[]>([])
  const [completed, setCompleted] = useState(false)

  useEffect(() => {
    if (!challenge || challenge.type !== mode) return
    setFirst(null); setLocked(false); setMoves(0); setCompleted(false)
    setMemoryTrace([]); setLeft(null); setRight(null); setMatched([]); setMatchingTrace([])
    setOrder([]); setOrderingTrace([])
    if (challenge.type === 'memory') {
      setMemoryCards(challenge.cards.map(card => ({ ...card, flipped: false, matched: false })))
    } else {
      setMemoryCards([])
    }
  }, [challenge, mode])

  async function finish(trace: InteractiveGameTrace[]) {
    if (completed) return
    const accepted = await onComplete?.(trace)
    if (accepted !== false) setCompleted(true)
  }

  function flipCard(index: number) {
    if (locked || completed || !memoryCards[index] || memoryCards[index].flipped || memoryCards[index].matched) return
    const card = memoryCards[index]
    const next = memoryCards.map((item, i) => i === index ? { ...item, flipped: true } : item)
    setMemoryCards(next)
    if (first === null) {
      setFirst(card.id)
      return
    }
    const firstId = first
    setFirst(null)
    setLocked(true)
    const trace = [...memoryTrace, { first: firstId, second: card.id } as InteractiveGameTrace]
    setMemoryTrace(trace)
    setMoves(value => value + 1)
    const timer = window.setTimeout(() => {
      setLocked(false)
      setMemoryCards(current => {
        const a = current.find(item => item.id === firstId)
        const b = current.find(item => item.id === card.id)
        const samePair = Boolean(a && b && a.pair_key === b.pair_key)
        if (!samePair) return current.map(item => item.id === firstId || item.id === card.id ? { ...item, flipped: false } : item)
        const updated = current.map(item => item.id === firstId || item.id === card.id ? { ...item, matched: true } : item)
        if (updated.every(item => item.matched)) finish(trace)
        return updated
      })
    }, 350)
  }

  function chooseMatching(side: 'left' | 'right', id: string) {
    if (completed || matched.includes(id)) return
    if (side === 'left') setLeft(id); else setRight(id)
  }

  useEffect(() => {
    if (completed || mode !== 'matching' || left === null || right === null || !challenge || challenge.type !== 'matching') return
    const pair = { left, right } as InteractiveGameTrace
    const trace = [...matchingTrace, pair]
    setMatchingTrace(trace)
    setMoves(value => value + 1)
    const leftItem = challenge.left.find(item => item.id === left)
    const rightItem = challenge.right.find(item => item.id === right)
    const correct = Boolean(leftItem && rightItem && leftItem.pair_key === rightItem.pair_key)
    if (correct) setMatched(current => [...current, left, right])
    setLeft(null); setRight(null)
    if (matched.length + (correct ? 2 : 0) >= challenge.left.length * 2) finish(trace)
  }, [left, right, completed, mode, challenge, matchingTrace, matched.length])

  function submitOrder() {
    if (completed || !challenge || challenge.type !== 'ordering' || order.length !== challenge.items.length) return
    const trace = [...orderingTrace, { order: [...order] } as InteractiveGameTrace]
    setOrderingTrace(trace)
    setMoves(value => value + 1)
    void Promise.resolve(onComplete?.(trace)).then((accepted) => {
      if (accepted !== false) setCompleted(true)
      else setOrder([])
    })
  }

  function reset() {
    if (!challenge || challenge.type !== mode) return
    setCompleted(false); setFirst(null); setLocked(false); setMoves(0)
    setMemoryTrace([]); setLeft(null); setRight(null); setMatched([]); setMatchingTrace([])
    setOrder([]); setOrderingTrace([])
    if (challenge.type === 'memory') setMemoryCards(challenge.cards.map(card => ({ ...card, flipped: false, matched: false })))
  }

  const items = challenge?.type === 'ordering' ? challenge.items : []
  return (
    <div className="interactive-game" dir={lang === 'ar' ? 'rtl' : 'ltr'}>
      <div className="interactive-toolbar">
        <strong>{mode === 'memory' ? t.memory : mode === 'matching' ? t.matching : t.ordering}</strong>
        <span>{t.moves}: {moves}</span>
        <button type="button" onClick={reset} disabled={!challenge}>{t.reset}</button>
      </div>

      {!challenge && <p className="interactive-instruction">Loading challenge…</p>}

      {challenge?.type === 'memory' && <>
        <p className="interactive-instruction">{t.match}</p>
        <div className="memory-board">{memoryCards.map((card, index) =>
          <button key={card.id} type="button" className={`memory-card ${card.flipped || card.matched ? 'revealed' : ''} ${card.matched ? 'matched' : ''}`} onClick={() => flipCard(index)} aria-label={card.flipped || card.matched ? card.label : 'Hidden card'}>
            <span>{card.flipped || card.matched ? card.label : '✦'}</span>
          </button>)}</div>
      </>}

      {challenge?.type === 'matching' && <>
        <p className="interactive-instruction">{t.chooseLeft} → {t.chooseRight}</p>
        <div className="matching-board">
          <div>{challenge.left.map(item => <button key={item.id} type="button" disabled={matched.includes(item.id)} className={`match-option ${left === item.id ? 'selected' : ''}`} onClick={() => chooseMatching('left', item.id)}>{item.label}</button>)}</div>
          <div>{challenge.right.map(item => <button key={item.id} type="button" disabled={matched.includes(item.id)} className={`match-option ${right === item.id ? 'selected' : ''}`} onClick={() => chooseMatching('right', item.id)}>{item.label}</button>)}</div>
        </div>
      </>}

      {challenge?.type === 'ordering' && <>
        <p className="interactive-instruction">{t.order}</p>
        <div className="ordering-pool">{items.map(item => <button key={item.id} type="button" disabled={order.includes(item.id)} onClick={() => setOrder(current => [...current, item.id])}>{item.label}</button>)}</div>
        <div className="ordering-result">{order.map((id, index) => {
          const item = items.find(entry => entry.id === id)
          return <div key={id} className="order-row"><span>{index + 1}. {item?.label}</span>
            <button type="button" onClick={() => setOrder(current => { const next=[...current]; [next[index-1], next[index]]=[next[index], next[index-1]]; return next })} disabled={index === 0}>{t.up}</button>
            <button type="button" onClick={() => setOrder(current => { const next=[...current]; [next[index], next[index+1]]=[next[index+1], next[index]]; return next })} disabled={index === order.length - 1}>{t.down}</button>
          </div>
        })}</div>
        <button type="button" className="interactive-secondary" onClick={() => setOrder(value => value.slice(0, -1))} disabled={!order.length}>{t.undo}</button>
        <button type="button" className="interactive-secondary" onClick={() => setOrder([])} disabled={!order.length}>{t.clear}</button>
        <button type="button" className="interactive-secondary" onClick={submitOrder} disabled={order.length !== items.length}>✓</button>
      </>}

      {completed && <div className="interactive-complete">🏆 {t.complete}</div>}
    </div>
  )
}
