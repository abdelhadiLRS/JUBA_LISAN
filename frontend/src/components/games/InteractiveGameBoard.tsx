'use client'

import { useEffect, useMemo, useState } from 'react'

type Mode = 'memory' | 'matching' | 'ordering'
type Lang = 'ar' | 'fr' | 'en'

type Props = { mode: Mode; lang: Lang; onComplete?: () => void }
type MemoryCard = { id: number; pair: string; label: string; flipped: boolean; matched: boolean }

const copy = {
  ar: { memory: 'الذاكرة', matching: 'المطابقة', ordering: 'الترتيب', reset: 'إعادة', moves: 'المحاولات', pairs: 'الأزواج', match: 'طابق العنصرين المتشابهين', chooseLeft: 'اختر كلمة', chooseRight: 'اختر ترجمتها', order: 'اضغط العناصر بالترتيب الصحيح', selected: 'المختار', complete: 'أحسنت! أكملت التحدي.', up: 'أعلى', down: 'أسفل', undo: 'تراجع', clear: 'مسح' },
  fr: { memory: 'Mémoire', matching: 'Association', ordering: 'Classement', reset: 'Réinitialiser', moves: 'Coups', pairs: 'Paires', match: 'Associe les deux éléments identiques', chooseLeft: 'Choisis un mot', chooseRight: 'Choisis sa traduction', order: 'Appuie sur les éléments dans le bon ordre', selected: 'Sélection', complete: 'Bravo ! Défi terminé.', up: 'Monter', down: 'Descendre', undo: 'Annuler', clear: 'Effacer' },
  en: { memory: 'Memory', matching: 'Matching', ordering: 'Ordering', reset: 'Reset', moves: 'Moves', pairs: 'Pairs', match: 'Match the two identical items', chooseLeft: 'Choose a word', chooseRight: 'Choose its translation', order: 'Tap the items in the correct order', selected: 'Selected', complete: 'Great job! Challenge complete.', up: 'Up', down: 'Down', undo: 'Undo', clear: 'Clear' },
} as const

const WORD_PAIRS = {
  ar: [['كتاب', 'book'], ['ماء', 'water'], ['مدرسة', 'school'], ['قلم', 'pen']],
  fr: [['livre', 'book'], ['eau', 'water'], ['école', 'school'], ['stylo', 'pen']],
  en: [['book', 'livre'], ['water', 'eau'], ['school', 'école'], ['pen', 'stylo']],
} as const

const ORDER_ITEMS = { ar: ['الثاني', 'الرابع', 'الأول', 'الثالث'], fr: ['deux', 'quatre', 'un', 'trois'], en: ['two', 'four', 'one', 'three'] } as const

function makeMemory(lang: Lang): MemoryCard[] {
  const pairs = lang === 'ar'
    ? [['قمر', 'moon'], ['كتاب', 'book'], ['شمس', 'sun'], ['بحر', 'sea'], ['قلم', 'pen'], ['باب', 'door']]
    : lang === 'fr'
      ? [['lune', 'moon'], ['livre', 'book'], ['soleil', 'sun'], ['mer', 'sea'], ['stylo', 'pen'], ['porte', 'door']]
      : [['moon', 'lune'], ['book', 'livre'], ['sun', 'soleil'], ['sea', 'mer'], ['pen', 'stylo'], ['door', 'porte']]
  return pairs.flatMap(([label, pair], index) => [
    { id: index * 2, pair: String(index), label, flipped: false, matched: false },
    { id: index * 2 + 1, pair: String(index), label: pair, flipped: false, matched: false },
  ]).sort(() => Math.random() - 0.5)
}

export function InteractiveGameBoard({ mode, lang, onComplete }: Props) {
  const t = copy[lang]
  const [memoryCards, setMemoryCards] = useState(() => makeMemory(lang))
  const [first, setFirst] = useState<number | null>(null)
  const [locked, setLocked] = useState(false)
  const [moves, setMoves] = useState(0)
  const [left, setLeft] = useState<number | null>(null)
  const [right, setRight] = useState<number | null>(null)
  const [matchedPairs, setMatchedPairs] = useState<number[]>([])
  const [order, setOrder] = useState<string[]>([])
  const [completed, setCompleted] = useState(false)

  const pairs = useMemo(() => WORD_PAIRS[lang], [lang])
  const targetOrder = lang === 'ar' ? ['الأول', 'الثاني', 'الثالث', 'الرابع'] : lang === 'fr' ? ['un', 'deux', 'trois', 'quatre'] : ['one', 'two', 'three', 'four']

  useEffect(() => {
    setMemoryCards(makeMemory(lang)); setFirst(null); setLeft(null); setRight(null); setMatchedPairs([]); setOrder([]); setMoves(0); setCompleted(false); setLocked(false)
  }, [lang, mode])

  useEffect(() => {
    if (completed) return
    if (mode === 'memory' && memoryCards.length > 0 && memoryCards.every((card) => card.matched)) {
      setCompleted(true); onComplete?.()
    }
  }, [completed, memoryCards, mode, onComplete])

  useEffect(() => {
    if (completed || mode !== 'matching' || left === null || right === null) return
    const currentLeft = left
    const currentRight = right
    const correct = currentLeft === currentRight
    const timer = window.setTimeout(() => {
      setMoves((value) => value + 1)
      if (correct) {
        setMatchedPairs((current) => {
          const next = current.includes(currentLeft) ? current : [...current, currentLeft]
          if (next.length === pairs.length) { setCompleted(true); onComplete?.() }
          return next
        })
      }
      setLeft(null); setRight(null)
    }, 300)
    return () => window.clearTimeout(timer)
  }, [completed, left, right, mode, pairs.length, onComplete])

  function flipCard(index: number) {
    if (locked || completed) return
    const card = memoryCards[index]
    if (card.flipped || card.matched) return
    const next = memoryCards.map((item, itemIndex) => itemIndex === index ? { ...item, flipped: true } : item)
    setMemoryCards(next)
    if (first === null) { setFirst(index); return }
    setMoves((value) => value + 1); setLocked(true)
    if (next[first].pair === next[index].pair) {
      setTimeout(() => {
        setMemoryCards((current) => current.map((item, itemIndex) => itemIndex === first || itemIndex === index ? { ...item, matched: true } : item))
        setFirst(null); setLocked(false)
      }, 250)
    } else {
      setTimeout(() => {
        setMemoryCards((current) => current.map((item, itemIndex) => itemIndex === first || itemIndex === index ? { ...item, flipped: false } : item))
        setFirst(null); setLocked(false)
      }, 700)
    }
  }

  function reset() {
    setMemoryCards(makeMemory(lang)); setFirst(null); setLeft(null); setRight(null); setMatchedPairs([]); setOrder([]); setMoves(0); setCompleted(false); setLocked(false)
  }

  function chooseOrder(item: string) {
    if (completed || order.includes(item)) return
    const next = [...order, item]; setOrder(next)
    if (next.length === targetOrder.length) {
      if (next.every((value, index) => value === targetOrder[index])) { setCompleted(true); onComplete?.() }
      else setMoves((value) => value + 1)
    }
  }

  function removeLast() { setOrder((value) => value.slice(0, -1)) }

  function shiftOrder(index: number, direction: -1 | 1) {
    setOrder((value) => {
      const next = [...value]; const target = index + direction
      if (target < 0 || target >= next.length) return value
      ;[next[index], next[target]] = [next[target], next[index]]
      if (next.length === targetOrder.length && next.every((item, itemIndex) => item === targetOrder[itemIndex])) { setCompleted(true); onComplete?.() }
      return next
    })
  }

  return (
    <div className="interactive-game" dir={lang === 'ar' ? 'rtl' : 'ltr'}>
      <div className="interactive-toolbar">
        <strong>{mode === 'memory' ? t.memory : mode === 'matching' ? t.matching : t.ordering}</strong>
        <span>{t.moves}: {moves}</span>
        <button type="button" onClick={reset}>{t.reset}</button>
      </div>

      {mode === 'memory' && <>
        <p className="interactive-instruction">{t.match}</p>
        <div className="memory-board">{memoryCards.map((card, index) => <button key={card.id} type="button" className={`memory-card ${card.flipped || card.matched ? 'revealed' : ''} ${card.matched ? 'matched' : ''}`} onClick={() => flipCard(index)} aria-label={card.flipped || card.matched ? card.label : 'Hidden card'}><span>{card.flipped || card.matched ? card.label : '✦'}</span></button>)}</div>
      </>}

      {mode === 'matching' && <>
        <p className="interactive-instruction">{t.chooseLeft} → {t.chooseRight}</p>
        <div className="matching-board">
          <div>{pairs.map((pair, index) => <button key={pair[0]} type="button" disabled={matchedPairs.includes(index)} className={`match-option ${left === index ? 'selected' : ''}`} onClick={() => !matchedPairs.includes(index) && setLeft(index)}>{pair[0]}</button>)}</div>
          <div>{pairs.map((pair, index) => <button key={pair[1]} type="button" disabled={matchedPairs.includes(index)} className={`match-option ${right === index ? 'selected' : ''}`} onClick={() => !matchedPairs.includes(index) && setRight(index)}>{pair[1]}</button>)}</div>
        </div>
      </>}

      {mode === 'ordering' && <>
        <p className="interactive-instruction">{t.order}</p>
        <div className="ordering-pool">{ORDER_ITEMS[lang].map((item) => <button key={item} type="button" disabled={order.includes(item)} onClick={() => chooseOrder(item)}>{item}</button>)}</div>
        <div className="ordering-result">{order.map((item, index) => <div key={item} className="order-row"><span>{index + 1}. {item}</span><button type="button" onClick={() => shiftOrder(index, -1)} disabled={index === 0}>{t.up}</button><button type="button" onClick={() => shiftOrder(index, 1)} disabled={index === order.length - 1}>{t.down}</button></div>)}</div>
        <button type="button" className="interactive-secondary" onClick={removeLast} disabled={!order.length}>{t.undo}</button>
        <button type="button" className="interactive-secondary" onClick={() => setOrder([])} disabled={!order.length}>{t.clear}</button>
      </>}

      {completed && <div className="interactive-complete">🏆 {t.complete}</div>}
    </div>
  )
}
