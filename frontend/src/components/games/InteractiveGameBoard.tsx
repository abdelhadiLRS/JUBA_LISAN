'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import type { InteractiveGameChallenge, InteractiveGameTrace } from '@/lib/games/persist'

type Mode = 'memory' | 'matching' | 'ordering'
type Lang = 'ar' | 'fr' | 'en' | 'es' | 'de' | 'it' | 'pt' | 'ja' | 'ko' | 'zh'
type Props = {
  mode: Mode
  lang: Lang
  challenge?: InteractiveGameChallenge
  onComplete?: (trace: InteractiveGameTrace[]) => Promise<boolean> | boolean | void
  title?: string
}
type MemoryCard = { id: string; label: string; pair_key?: string; flipped: boolean; matched: boolean }

const copy = {
  ar: { memory: 'الذاكرة', matching: 'المطابقة', ordering: 'الترتيب', reset: 'إعادة', moves: 'المحاولات', match: 'طابق العنصرين المتشابهين', chooseLeft: 'اختر كلمة', chooseRight: 'اختر ترجمتها', order: 'اضغط العناصر بالترتيب الصحيح', complete: 'أحسنت! أكملت التحدي.', up: 'أعلى', down: 'أسفل', undo: 'تراجع', clear: 'مسح' },
  fr: { memory: 'Mémoire', matching: 'Association', ordering: 'Classement', reset: 'Réinitialiser', moves: 'Coups', match: 'Associe les deux éléments', chooseLeft: 'Choisis un mot', chooseRight: 'Choisis sa traduction', order: 'Appuie sur les éléments dans le bon ordre', complete: 'Bravo ! Défi terminé.', up: 'Monter', down: 'Descendre', undo: 'Annuler', clear: 'Effacer' },
  en: { memory: 'Memory', matching: 'Matching', ordering: 'Ordering', reset: 'Reset', moves: 'Moves', match: 'Match the two items', chooseLeft: 'Choose a word', chooseRight: 'Choose its translation', order: 'Tap the items in the correct order', complete: 'Great job! Challenge complete.', up: 'Up', down: 'Down', undo: 'Undo', clear: 'Clear' },
  es: { memory: 'Memoria', matching: 'Emparejar', ordering: 'Ordenar', reset: 'Reiniciar', moves: 'Movimientos', match: 'Empareja los dos elementos', chooseLeft: 'Elige una palabra', chooseRight: 'Elige su traducción', order: 'Pulsa los elementos en el orden correcto', complete: '¡Muy bien! Desafío completado.', up: 'Arriba', down: 'Abajo', undo: 'Deshacer', clear: 'Borrar' },
  de: { memory: 'Memory', matching: 'Zuordnen', ordering: 'Ordnen', reset: 'Zurücksetzen', moves: 'Züge', match: 'Ordne die beiden Elemente zu', chooseLeft: 'Wähle ein Wort', chooseRight: 'Wähle seine Übersetzung', order: 'Tippe die Elemente in der richtigen Reihenfolge an', complete: 'Gut gemacht! Herausforderung abgeschlossen.', up: 'Nach oben', down: 'Nach unten', undo: 'Rückgängig', clear: 'Löschen' },
  it: { memory: 'Memoria', matching: 'Abbinamento', ordering: 'Ordine', reset: 'Reimposta', moves: 'Mosse', match: 'Abbina i due elementi', chooseLeft: 'Scegli una parola', chooseRight: 'Scegli la traduzione', order: 'Tocca gli elementi nell’ordine corretto', complete: 'Ottimo! Sfida completata.', up: 'Su', down: 'Giù', undo: 'Annulla', clear: 'Cancella' },
  pt: { memory: 'Memória', matching: 'Correspondência', ordering: 'Ordenação', reset: 'Repor', moves: 'Movimentos', match: 'Liga os dois elementos', chooseLeft: 'Escolhe uma palavra', chooseRight: 'Escolhe a tradução', order: 'Toca nos elementos pela ordem correta', complete: 'Muito bem! Desafio concluído.', up: 'Cima', down: 'Baixo', undo: 'Desfazer', clear: 'Limpar' },
  ja: { memory: 'メモリー', matching: 'マッチング', ordering: '並べ替え', reset: 'リセット', moves: '手数', match: '2つの要素を合わせてください', chooseLeft: '単語を選んでください', chooseRight: '翻訳を選んでください', order: '正しい順番でタップしてください', complete: 'よくできました！チャレンジ完了です。', up: '上へ', down: '下へ', undo: '元に戻す', clear: 'クリア' },
  ko: { memory: '기억', matching: '짝맞추기', ordering: '순서 맞추기', reset: '재설정', moves: '횟수', match: '두 요소를 짝지어 보세요', chooseLeft: '단어를 선택하세요', chooseRight: '번역을 선택하세요', order: '올바른 순서로 항목을 눌러 보세요', complete: '잘했어요! 도전 완료.', up: '위', down: '아래', undo: '실행 취소', clear: '지우기' },
  zh: { memory: '记忆', matching: '配对', ordering: '排序', reset: '重置', moves: '操作次数', match: '匹配两个元素', chooseLeft: '选择一个词', chooseRight: '选择它的翻译', order: '按正确顺序点击元素', complete: '做得好！挑战完成。', up: '上移', down: '下移', undo: '撤销', clear: '清除' },
} as const

export function InteractiveGameBoard({ mode, lang, challenge, onComplete, title }: Props) {
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
  const [completionError, setCompletionError] = useState(false)
  const [saving, setSaving] = useState(false)
  const [retryStage, setRetryStage] = useState<'initial' | 'retry' | 'focused_retrieval' | 'guided_retrieval'>('initial')
  const memoryTimer = useRef<number | null>(null)

  useEffect(() => {
    if (!challenge || challenge.type !== mode) return
    setFirst(null); setLocked(false); setMoves(0); setCompleted(false); setRetryStage('initial')
    setMemoryTrace([]); setLeft(null); setRight(null); setMatched([]); setMatchingTrace([])
    setOrder([]); setOrderingTrace([])
    if (challenge.type === 'memory') {
      setMemoryCards(challenge.cards.map(card => ({ ...card, flipped: false, matched: false })))
    } else {
      setMemoryCards([])
    }
  }, [challenge, mode])

  const finish = useCallback(async (trace: InteractiveGameTrace[]) => {
    if (completed || saving) return
    setSaving(true)
    setCompletionError(false)
    try {
      const accepted = await onComplete?.(trace)
      if (accepted !== false) setCompleted(true)
      else setCompletionError(true)
    } catch {
      setCompletionError(true)
    } finally {
      setSaving(false)
    }
  }, [completed, onComplete, saving])

  const memoryRetryCount = (id: string) => memoryTrace.filter(attempt => {
    if (attempt.first !== id && attempt.second !== id) return false
    const firstCard = challenge?.type === 'memory' ? challenge.cards.find(card => card.id === attempt.first) : undefined
    const secondCard = challenge?.type === 'memory' ? challenge.cards.find(card => card.id === attempt.second) : undefined
    return Boolean(firstCard && secondCard && firstCard.pair_key !== secondCard.pair_key)
  }).length

  const matchingRetryCount = (id: string) => matchingTrace.filter(attempt => {
    if (attempt.left !== id) return false
    const leftItem = challenge?.type === 'matching' ? challenge.left.find(item => item.id === attempt.left) : undefined
    const rightItem = challenge?.type === 'matching' ? challenge.right.find(item => item.id === attempt.right) : undefined
    return Boolean(leftItem && rightItem && leftItem.pair_key !== rightItem.pair_key)
  }).length

  const retryInstruction = retryStage === 'focused_retrieval'
    ? (lang === 'ar' ? 'ركّز على هذا العنصر وحاول الاسترجاع مرة أخرى.' : lang === 'fr' ? 'Concentre-toi sur cet élément et récupère-le à nouveau.' : 'Focus on this item and retrieve it again.')
    : retryStage === 'guided_retrieval'
      ? (lang === 'ar' ? 'خذ وقتك. أعد المحاولة بأسلوب أبطأ وأكثر تركيزًا.' : lang === 'fr' ? 'Prends ton temps. Réessaie plus lentement et avec plus de concentration.' : 'Take your time. Retry more slowly and deliberately.')
      : retryStage === 'retry'
        ? (lang === 'ar' ? 'محاولة ثانية: استرجع الإجابة بدل التخمين.' : lang === 'fr' ? 'Deuxième essai : retrouve la réponse plutôt que de deviner.' : 'Second attempt: retrieve the answer instead of guessing.')
        : ''

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
    memoryTimer.current = window.setTimeout(() => {
      setLocked(false)
      setMemoryCards(current => {
        const a = current.find(item => item.id === firstId)
        const b = current.find(item => item.id === card.id)
        const samePair = Boolean(a && b && a.pair_key === b.pair_key)
        if (!samePair) {
          const misses = memoryRetryCount(firstId) + 1
          setRetryStage(misses >= 3 ? 'guided_retrieval' : misses >= 2 ? 'focused_retrieval' : 'retry')
          return current.map(item => item.id === firstId || item.id === card.id ? { ...item, flipped: false } : item)
        }
        setRetryStage('initial')
        return current.map(item => item.id === firstId || item.id === card.id ? { ...item, matched: true } : item)
      })
    }, 350)
  }

  useEffect(() => {
    return () => {
      if (memoryTimer.current !== null) {
        window.clearTimeout(memoryTimer.current)
        memoryTimer.current = null
      }
    }
  }, [])

  useEffect(() => {
    if (!completed && mode === 'memory' && memoryCards.length > 0 && memoryCards.every(card => card.matched)) {
      void finish(memoryTrace)
    }
  }, [completed, mode, memoryCards, memoryTrace, finish])

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
    if (!correct) {
      const misses = matchingRetryCount(left) + 1
      setRetryStage(misses >= 3 ? 'guided_retrieval' : misses >= 2 ? 'focused_retrieval' : 'retry')
    } else {
      setRetryStage('initial')
    }
    if (correct) setMatched(current => [...current, left, right])
    setLeft(null); setRight(null)
    if (matched.length + (correct ? 2 : 0) >= challenge.left.length * 2) void finish(trace)
  }, [left, right, completed, mode, challenge, matchingTrace, matched.length, finish])

  function submitOrder() {
    if (completed || !challenge || challenge.type !== 'ordering' || order.length !== challenge.items.length) return
    const trace = [...orderingTrace, { order: [...order] } as InteractiveGameTrace]
    setOrderingTrace(trace)
    const target = challenge.items.map(item => item.id)
    const correct = order.every((id, index) => id === target[index])
    if (!correct) {
      const misses = orderingTrace.length + 1
      setRetryStage(misses >= 3 ? 'guided_retrieval' : misses >= 2 ? 'focused_retrieval' : 'retry')
    } else {
      setRetryStage('initial')
    }
    setMoves(value => value + 1)
    void finish(trace)
  }

  function reset() {
    if (!challenge || challenge.type !== mode) return
    if (memoryTimer.current !== null) {
      window.clearTimeout(memoryTimer.current)
      memoryTimer.current = null
    }
    setCompleted(false); setCompletionError(false); setSaving(false); setFirst(null); setLocked(false); setMoves(0); setRetryStage('initial')
    setMemoryTrace([]); setLeft(null); setRight(null); setMatched([]); setMatchingTrace([])
    setOrder([]); setOrderingTrace([])
    if (challenge.type === 'memory') setMemoryCards(challenge.cards.map(card => ({ ...card, flipped: false, matched: false })))
  }

  const items = challenge?.type === 'ordering' ? challenge.items : []
  return (
    <div className="interactive-game" dir={lang === 'ar' ? 'rtl' : 'ltr'}>
      <div className="interactive-toolbar">
        <strong>{title ?? (mode === 'memory' ? t.memory : mode === 'matching' ? t.matching : t.ordering)}</strong>
        <span>{t.moves}: {moves}</span>
        <button type="button" onClick={reset} disabled={!challenge || completed || locked || saving}>{saving ? '…' : t.reset}</button>
      </div>

      {!challenge && <p className="interactive-instruction">Loading challenge…</p>}

      {challenge?.type === 'memory' && <>
        <p className="interactive-instruction">{t.match}</p>
        <div className="memory-board">{memoryCards.map((card, index) =>
          <button key={card.id} type="button" className={`memory-card ${card.flipped || card.matched ? 'revealed' : ''} ${card.matched ? 'matched' : ''} ${memoryRetryCount(card.id) >= 2 ? 'retry-focus' : ''}`} onClick={() => flipCard(index)} aria-label={card.flipped || card.matched ? card.label : 'Hidden card'}>
            <span>{card.flipped || card.matched ? card.label : '✦'}</span>
          </button>)}</div>
      </>}

      {challenge?.type === 'matching' && <>
        <p className="interactive-instruction">{t.chooseLeft} → {t.chooseRight}</p>
        <div className="matching-board">{retryInstruction && <p className="interactive-retry" role="status">{retryInstruction}</p>}
          <div>{challenge.left.map(item => <button key={item.id} type="button" disabled={matched.includes(item.id)} className={`match-option ${left === item.id ? 'selected' : ''} ${matchingRetryCount(item.id) >= 2 ? 'retry-focus' : ''}`} onClick={() => chooseMatching('left', item.id)}>{item.label}</button>)}</div>
          <div>{challenge.right.map(item => <button key={item.id} type="button" disabled={matched.includes(item.id)} className={`match-option ${right === item.id ? 'selected' : ''}`} onClick={() => chooseMatching('right', item.id)}>{item.label}</button>)}</div>
        </div>
      </>}

      {challenge?.type === 'ordering' && <>
        <p className="interactive-instruction">{t.order}</p>{retryInstruction && <p className="interactive-retry" role="status">{retryInstruction}</p>}
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
        <button type="button" className="interactive-secondary" onClick={submitOrder} disabled={order.length !== items.length || saving}>{saving ? '…' : '✓'}</button>
      </>}

      {completionError && !completed && <div className="interactive-error" role="alert"><p>Unable to save the result. Reset and try again.</p><button type="button" onClick={reset}>{t.reset}</button></div>}
      {completed && <div className="interactive-complete" role="status">🏆 {t.complete}</div>}
    </div>
  )
}
