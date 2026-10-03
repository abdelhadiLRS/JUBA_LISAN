'use client'

import { useEffect, useRef, useState } from 'react'
import { startGameSession, answerGameSessionQuestion, completeGameSession, type GameId, type GameLanguage, type GameSessionQuestion, type GameSessionStartResponse, type GameSessionNextResponse, type GameSessionResult, type InteractiveGameTrace } from '@/lib/games/persist'
import { useProgressStore } from '@/store/progress'
import type { AchievementId } from '@/lib/games/achievements'
import { markLearningProgressUpdated } from '@/lib/learning-progress'

type Props = {gameId: GameId; language: GameLanguage; targetLanguage: string; difficulty: number; arabic: boolean; title: string; onExit: () => void; onReplay: () => void}
export function EducationalGameSession({gameId, language, targetLanguage, difficulty, arabic, title, onExit, onReplay}: Props) {
  const [session, setSession] = useState<GameSessionStartResponse | null>(null)
  const [question, setQuestion] = useState<GameSessionQuestion | null>(null)
  const [feedback, setFeedback] = useState<GameSessionNextResponse | null>(null)
  const [result, setResult] = useState<GameSessionResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [input, setInput] = useState('')
  const [selected, setSelected] = useState('')
  const [answered, setAnswered] = useState(0)
  const [total, setTotal] = useState(5)
  const [revealed, setRevealed] = useState<string[]>([])
  const [matched, setMatched] = useState<string[]>([])
  const [left, setLeft] = useState<string | null>(null)
  const [order, setOrder] = useState<string[]>([])
  const [moves, setMoves] = useState(0)
  const [boardFeedback, setBoardFeedback] = useState('')
  const [audioError, setAudioError] = useState(false)
  const version = useRef(0)
  const lock = useRef(false)
  const boardLock = useRef(false)
  const first = useRef<string | null>(null)
  const trace = useRef<InteractiveGameTrace[]>([])
  const answers = useRef<Array<{question_id: string; choice: string}>>([])
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const chooseLeft = useRef<string | null>(null)
  const speech = useRef<SpeechSynthesisUtterance | null>(null)
  const copy = (ar: string, en: string) => arabic ? ar : en

  useEffect(() => {
    const epoch = ++version.current
    void startGameSession(gameId, language, difficulty, gameId === 'review_mix').then(data => {
      if (epoch !== version.current) return
      if (!data.interaction && !data.questions.length) throw new Error('empty')
      setSession(data); setQuestion(data.questions[0] ?? null); setLoading(false)
    }).catch(() => {
      if (epoch === version.current) {setLoading(false); setError(arabic ? 'تعذر بدء اللعبة. تحقق من وجود خطة نشطة ثم أعد المحاولة.' : 'Could not start the game. Check that you have an active plan and retry.')}
    })
    return () => {
      version.current += 1
      if (timer.current) clearTimeout(timer.current)
      if (speech.current && typeof window !== 'undefined') window.speechSynthesis?.cancel()
    }
  }, [gameId, language, difficulty, arabic])

  async function submit(choice: string) {
    if (!session || !question || lock.current || feedback || !choice.trim()) return
    lock.current = true; setBusy(true); setError('')
    const epoch = version.current
    try {
      const next = await answerGameSessionQuestion(session.session_id, question.id, choice.trim())
      if (epoch !== version.current) return
      if (next.correct) answers.current = [...answers.current.filter(item => item.question_id !== question.id), {question_id: question.id, choice: choice.trim()}]
      setSelected(choice); setFeedback(next); setAnswered(next.answered); setTotal(next.total)
    } catch {
      if (epoch === version.current) setError(copy('لم يصل التصحيح. لم نسجل نجاحًا؛ يمكنك إعادة المحاولة.', 'Validation failed. No success was recorded; retry your answer.'))
    } finally {
      if (epoch === version.current) {lock.current = false; setBusy(false)}
    }
  }

  async function finish() {
    if (!session || lock.current || result) return
    lock.current = true; setBusy(true); setError('')
    const epoch = version.current
    try {
      const saved = await completeGameSession(session.session_id, answers.current, session.daily_challenge, session.daily_challenge_date, trace.current)
      if (epoch !== version.current) return
      setResult(saved)
      useProgressStore.getState().setProgress({
        streak: useProgressStore.getState().streak, xp: saved.total_xp, skills: saved.skills,
        achievements: saved.achievements as AchievementId[],
        gameStats: {gamesPlayed:saved.games_played,questionsAnswered:saved.questions_answered,correctAnswers:saved.correct_answers,bestRoundScore:saved.best_round_score,dailyChallengesCompleted:saved.daily_challenges_completed,lastDailyChallengeDate:saved.last_daily_challenge_date,currentCorrectStreak:saved.current_correct_streak,bestCorrectStreak:saved.best_correct_streak},
      })
      markLearningProgressUpdated()
    } catch {
      if (epoch === version.current) setError(copy('تعذر حفظ الجولة. حركاتك محفوظة هنا؛ اضغط الحفظ مجددًا.', 'Could not save the round. Your moves are kept here; retry saving.'))
    } finally {
      if (epoch === version.current) {lock.current = false; setBusy(false)}
    }
  }

  function advance() {
    if (!feedback || busy) return
    if (feedback.finished) {void finish(); return}
    setQuestion(feedback.question); setFeedback(null); setSelected(''); setInput(''); setAudioError(false)
    if (speech.current) {window.speechSynthesis?.cancel(); speech.current = null}
  }

  function playAudio() {
    if (!question?.audio_text) return
    if (!window.speechSynthesis || typeof SpeechSynthesisUtterance === 'undefined') {setAudioError(true); return}
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(question.audio_text)
    utterance.lang = question.audio_language ?? targetLanguage
    const code = utterance.lang.toLowerCase().split('-')[0]
    const voice = window.speechSynthesis.getVoices().find(item => item.lang.toLowerCase().split('-')[0] === code)
    if (!voice) {setAudioError(true); return}
    utterance.voice = voice; utterance.rate = 0.85
    utterance.onerror = () => setAudioError(true)
    speech.current = utterance; setAudioError(false); window.speechSynthesis.speak(utterance)
  }

  function flip(id: string) {
    const challenge = session?.interaction
    if (!challenge || challenge.type !== 'memory' || boardLock.current || busy || result || matched.includes(id) || first.current === id) return
    if (!first.current) {first.current = id; setRevealed([id]); return}
    const a = first.current; first.current = null; boardLock.current = true
    trace.current.push({first:a,second:id}); setMoves(value => value+1); setRevealed([a,id])
    const one = challenge.cards.find(card => card.id === a)
    const two = challenge.cards.find(card => card.id === id)
    const correct = one?.pair_key !== undefined && one.pair_key === two?.pair_key
    setBoardFeedback(correct ? copy('زوج صحيح', 'Pair found') : copy('تذكّر المكان وحاول من جديد', 'Remember their positions and try again'))
    timer.current = setTimeout(() => {
      if (correct) setMatched(value => [...value,a,id])
      setRevealed([]); boardLock.current = false
    }, correct ? 300 : 1000)
  }

  function pair(id: string) {
    const challenge = session?.interaction
    const a = chooseLeft.current
    if (!challenge || challenge.type !== 'matching' || !a || busy || result || matched.includes(id)) return
    chooseLeft.current = null; setLeft(null)
    trace.current.push({left:a,right:id}); setMoves(value => value+1)
    const one = challenge.left.find(item => item.id === a)
    const two = challenge.right.find(item => item.id === id)
    const correct = one?.pair_key !== undefined && one.pair_key === two?.pair_key
    if (correct) setMatched(value => [...value,a,id])
    setBoardFeedback(correct ? copy('مطابقة صحيحة', 'Correct match') : copy('المعنى لا يطابق. جرّب مرة أخرى.', 'That meaning does not match. Try again.'))
  }

  const challenge = session?.interaction
  const boardDone = challenge?.type === 'memory' ? matched.length === challenge.cards.length : challenge?.type === 'matching' ? matched.length === challenge.left.length * 2 : false
  const targetDir = targetLanguage.startsWith('ar') ? 'rtl' : 'ltr'
  if (loading) return <section className="edu-stage" aria-busy="true"><p role="status">{copy('جارٍ تجهيز الجولة من محتوى التعلم…','Preparing a round from learning content…')}</p><button onClick={onExit}>{copy('العودة','Back')}</button></section>
  return <section className="edu-stage" aria-busy={busy}>
    <header className="edu-session-head"><button onClick={onExit} disabled={busy}>{copy('الألعاب ←','← Games')}</button><h2>{title}</h2>{challenge ? <span>{copy('الحركات','Moves')}: {moves}</span> : <span>{answered}/{total}</span>}</header>
    {error && <p className="edu-error" role="alert">{error}</p>}
    {!session && <button className="edu-primary" onClick={onReplay}>{copy('إعادة المحاولة','Retry')}</button>}
    {result ? <div className="edu-result" role="status"><span className="edu-result-symbol" aria-hidden="true">✓</span><h3>{copy('تم حفظ الجولة','Round saved')}</h3><p>{result.round_correct}/{result.round_questions} {copy('إجابات صحيحة','correct')} · +{result.xp_earned} XP</p><p>{copy('النتيجة من الخادم، وليست تقديرًا محليًا.','Scored by the server, not estimated locally.')}</p><button className="edu-primary" onClick={onReplay}>{copy('جولة جديدة','New round')}</button><button onClick={onExit}>{copy('اختيار لعبة أخرى','Choose another game')}</button></div> : session && <>
      {!challenge && question && <>
        <progress value={answered} max={total} aria-label={copy('تقدم الجولة','Round progress')} />
        <h3 className="edu-prompt" dir="auto">{question.prompt}</h3>
        {question.audio_text && <div className="edu-audio"><button onClick={playAudio}>{copy('▶ استمع','▶ Listen')}</button>{audioError && <p role="alert">{copy('لا يتوفر صوت لهذه اللغة في المتصفح. لا يمكن إكمال تمرين الاستماع بدون صوت.','No voice for this language is available in your browser. Listening practice needs audio.')}</p>}</div>}
        {question.input_mode === 'text' ? <form className="edu-answer-form" onSubmit={event => {event.preventDefault(); void submit(input)}}><label htmlFor="game-answer">{copy('إجابتك','Your answer')}</label><input id="game-answer" dir={targetDir} value={input} onChange={event => setInput(event.target.value)} autoComplete="off" spellCheck={false} disabled={busy || !!feedback} /><button className="edu-primary" disabled={busy || !!feedback || !input.trim()}>{copy('تحقّق','Check')}</button></form> : <div className="edu-choices">{question.choices.map((choice,index) => <button key={`${index}:${choice}`} disabled={busy || !!feedback} aria-pressed={selected === choice} onClick={() => void submit(choice)}><span>{index+1}</span><b dir="auto">{choice}</b></button>)}</div>}
        {feedback && <div className="edu-feedback" data-correct={feedback.correct} role="status"><strong>{feedback.correct ? copy('صحيح!','Correct!') : copy('ليست صحيحة. سنراجع نفس العنصر.','Not quite. We’ll revisit this item.')}</strong><p>{question.hint}</p><button className="edu-primary" onClick={advance} disabled={busy}>{feedback.finished ? copy('حفظ الجولة','Save round') : feedback.correct ? copy('التالي','Next') : copy('حاول مجددًا','Try again')}</button></div>}
      </>}
      {challenge?.type === 'memory' && <><p>{copy('اقلب بطاقتين: ابحث عن الكلمة وتعريفها.','Flip two cards: find a word and its definition.')}</p><div className="edu-memory">{challenge.cards.map((card,index) => <button key={card.id} disabled={matched.includes(card.id) || busy} data-revealed={revealed.includes(card.id) || matched.includes(card.id)} aria-label={revealed.includes(card.id) || matched.includes(card.id) ? card.label : copy(`بطاقة مخفية ${index+1}`,`Hidden card ${index+1}`)} onClick={() => flip(card.id)}><span dir="auto">{revealed.includes(card.id) || matched.includes(card.id) ? card.label : '✦'}</span></button>)}</div></>}
      {challenge?.type === 'matching' && <><p>{copy('اختر كلمة، ثم تعريفها من العمود الآخر.','Select a word, then its definition in the other column.')}</p><div className="edu-matching"><div>{challenge.left.map(item => <button key={item.id} disabled={busy || matched.includes(item.id)} aria-pressed={left === item.id} onClick={() => {chooseLeft.current=item.id; setLeft(item.id)}} dir="auto">{item.label}</button>)}</div><div>{challenge.right.map(item => <button key={item.id} disabled={busy || !left || matched.includes(item.id)} onClick={() => pair(item.id)} dir="auto">{item.label}</button>)}</div></div></>}
      {challenge?.type === 'ordering' && <><p>{copy('ابنِ جملة صحيحة من الكلمات. يمكنك حذف كلمة بالنقر عليها وإعادة وضعها.','Build a grammatical sentence. Tap a placed word to remove and reposition it.')}</p><div className="edu-sentence" dir={targetDir} aria-label={copy('الجملة التي تبنيها','Your sentence')}>{order.length ? order.map((id,index) => <button key={id} disabled={busy} onClick={() => setOrder(value => value.filter(item => item !== id))}><small>{index+1}</small> {challenge.items.find(item => item.id === id)?.label}</button>) : <span>{copy('اختر الكلمات بالترتيب','Select words in order')}</span>}</div><div className="edu-word-pool" dir={targetDir}>{challenge.items.map(item => <button key={item.id} disabled={busy || order.includes(item.id)} onClick={() => setOrder(value => value.includes(item.id) ? value : [...value,item.id])}>{item.label}</button>)}</div><button disabled={busy || !order.length} onClick={() => setOrder([])}>{copy('إعادة الترتيب','Clear order')}</button><button className="edu-primary" disabled={busy || order.length !== challenge.items.length} onClick={() => {if(lock.current)return; trace.current=[{order:[...order]}]; setMoves(value => value+1); void finish()}}>{copy('تصحيح وحفظ الجملة','Score and save sentence')}</button><p className="edu-note">{copy('لا نفترض أن ترتيب الكلمات الظاهر هو الحل؛ الخادم وحده يصحّح الجملة.','The displayed tile order is not treated as the solution; the server scores your sentence.')}</p></>}
      {boardFeedback && <p role="status" className="edu-board-feedback">{boardFeedback}</p>}
      {boardDone && <button className="edu-primary" onClick={() => void finish()} disabled={busy}>{copy('حفظ الجولة','Save round')}</button>}
    </>}
  </section>
}
