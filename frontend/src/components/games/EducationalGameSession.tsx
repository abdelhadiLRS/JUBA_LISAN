'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { Heart, Target, RotateCcw, Volume2, Move, Check } from 'lucide-react'
import { startArena, readArena, moveArena, type ArenaState, type ArenaMove, startGameSession, answerGameSessionQuestion, completeGameSession, type GameId, type GameLanguage, type GameSessionQuestion, type GameSessionStartResponse, type GameSessionNextResponse, type GameSessionResult, type InteractiveGameTrace } from '@/lib/games/persist'
import { useAuthStore } from '@/store/auth'
import { useProgressStore } from '@/store/progress'
import type { AchievementId } from '@/lib/games/achievements'
import { markLearningProgressUpdated } from '@/lib/learning-progress'

type Props = {gameId: GameId; language: GameLanguage; targetLanguage: string; difficulty: number; arabic: boolean; title: string; onExit: () => void; onReplay: () => void}
const ARCADE_GAMES=new Set(['quick_choice','spelling','word_scramble','memory','matching'])
function publishResult(saved:GameSessionResult){
  useProgressStore.getState().setProgress({
    streak:useProgressStore.getState().streak,xp:saved.total_xp,skills:saved.skills,
    achievements:saved.achievements as AchievementId[],
    gameStats:{gamesPlayed:saved.games_played,questionsAnswered:saved.questions_answered,correctAnswers:saved.correct_answers,bestRoundScore:saved.best_round_score,dailyChallengesCompleted:saved.daily_challenges_completed,lastDailyChallengeDate:saved.last_daily_challenge_date,currentCorrectStreak:saved.current_correct_streak,bestCorrectStreak:saved.best_correct_streak},
  })
  markLearningProgressUpdated()
}
export function EducationalGameSession(props:Props){
  return ARCADE_GAMES.has(props.gameId)?<ArenaGame {...props}/>:<LegacyGameSession {...props}/>
}

// Retain the existing question/ordering API and reward flow for other games.
function LegacyGameSession({gameId,language,targetLanguage,difficulty,arabic,title,onExit,onReplay}:Props){
  const [session,setSession]=useState<GameSessionStartResponse|null>(null)
  const [question,setQuestion]=useState<GameSessionQuestion|null>(null)
  const [feedback,setFeedback]=useState<GameSessionNextResponse|null>(null)
  const [result,setResult]=useState<GameSessionResult|null>(null)
  const [loading,setLoading]=useState(true)
  const [busy,setBusy]=useState(false)
  const [error,setError]=useState('')
  const [input,setInput]=useState('')
  const [selected,setSelected]=useState('')
  const [answered,setAnswered]=useState(0)
  const [total,setTotal]=useState(5)
  const [order,setOrder]=useState<string[]>([])
  const [audioError,setAudioError]=useState(false)
  const version=useRef(0),lock=useRef(false)
  const answers=useRef<Array<{question_id:string;choice:string}>>([])
  const trace=useRef<InteractiveGameTrace[]>([])
  const speech=useRef<SpeechSynthesisUtterance|null>(null)
  const copy=(ar:string,en:string)=>arabic?ar:en
  useEffect(()=>{
    const epoch=++version.current
    void startGameSession(gameId,language,difficulty,gameId==='review_mix').then(data=>{
      if(epoch!==version.current)return
      if(!data.interaction&&!data.questions.length)throw new Error('empty')
      setSession(data);setQuestion(data.questions[0]??null);setLoading(false)
    }).catch(()=>{if(epoch===version.current){setLoading(false);setError(copy('تعذر بدء اللعبة. تحقق من وجود خطة نشطة ثم أعد المحاولة.','Could not start the game. Check that you have an active plan and retry.'))}})
    return()=>{version.current+=1;if(speech.current)window.speechSynthesis?.cancel()}
  },[gameId,language,difficulty,arabic])
  async function submit(choice:string){
    if(!session||!question||lock.current||feedback||!choice.trim())return
    lock.current=true;setBusy(true);setError('');const epoch=version.current
    try{
      const next=await answerGameSessionQuestion(session.session_id,question.id,choice.trim())
      if(epoch!==version.current)return
      if(next.correct)answers.current=[...answers.current.filter(a=>a.question_id!==question.id),{question_id:question.id,choice:choice.trim()}]
      setSelected(choice);setFeedback(next);setAnswered(next.answered);setTotal(next.total)
    }catch{if(epoch===version.current)setError(copy('لم يصل التصحيح. يمكنك إعادة المحاولة.','Validation failed. Retry your answer.'))}
    finally{if(epoch===version.current){lock.current=false;setBusy(false)}}
  }
  async function finish(){
    if(!session||lock.current||result)return
    lock.current=true;setBusy(true);setError('');const epoch=version.current
    try{
      const saved=await completeGameSession(session.session_id,answers.current,session.daily_challenge,session.daily_challenge_date,trace.current)
      if(epoch!==version.current)return
      setResult(saved);publishResult(saved)
    }catch{if(epoch===version.current)setError(copy('تعذر حفظ الجولة. أعد الحفظ؛ حركاتك محفوظة هنا.','Could not save the round. Your moves are kept here; retry saving.'))}
    finally{if(epoch===version.current){lock.current=false;setBusy(false)}}
  }
  function advance(){
    if(!feedback||busy)return
    if(feedback.finished){void finish();return}
    setQuestion(feedback.question);setFeedback(null);setSelected('');setInput('');setAudioError(false)
    if(speech.current){window.speechSynthesis?.cancel();speech.current=null}
  }
  function playAudio(){
    if(!question?.audio_text)return
    if(!window.speechSynthesis||typeof SpeechSynthesisUtterance==='undefined'){setAudioError(true);return}
    const utterance=new SpeechSynthesisUtterance(question.audio_text)
    utterance.lang=question.audio_language??targetLanguage
    const voice=window.speechSynthesis.getVoices().find(v=>v.lang.toLowerCase().split('-')[0]===utterance.lang.toLowerCase().split('-')[0])
    if(!voice){setAudioError(true);return}
    window.speechSynthesis.cancel();utterance.voice=voice;utterance.rate=.85
    utterance.onerror=()=>setAudioError(true);speech.current=utterance;setAudioError(false);window.speechSynthesis.speak(utterance)
  }
  const challenge=session?.interaction
  const targetDir=targetLanguage.startsWith('ar')?'rtl':'ltr'
  if(loading)return <section className="edu-stage" aria-busy="true"><p role="status">{copy('جارٍ تجهيز الجولة من محتوى التعلم…','Preparing a round from learning content…')}</p><button onClick={onExit}>{copy('العودة','Back')}</button></section>
  return <section className="edu-stage" aria-busy={busy}><header className="edu-session-head"><button onClick={onExit} disabled={busy}>{copy('الألعاب','Games')}</button><h2>{title}</h2><span>{answered}/{total}</span></header>{error&&<p className="edu-error" role="alert">{error}</p>}{!session&&<button className="edu-primary" onClick={onReplay}>{copy('إعادة المحاولة','Retry')}</button>}{result?<div className="edu-result" role="status"><h3>{copy('تم حفظ الجولة','Round saved')}</h3><p>{result.round_correct}/{result.round_questions} · +{result.xp_earned} XP</p><button className="edu-primary" onClick={onReplay}>{copy('جولة جديدة','New round')}</button><button onClick={onExit}>{copy('اختيار لعبة أخرى','Choose another game')}</button></div>:session&&<>
    {!challenge&&question&&<><progress value={answered} max={total} aria-label={copy('تقدم الجولة','Round progress')}/><h3 className="edu-prompt" dir="auto">{question.prompt}</h3>{question.audio_text&&<div className="edu-audio"><button onClick={playAudio}>{copy('استمع','Listen')}</button>{audioError&&<p role="alert">{copy('لا يتوفر صوت لهذه اللغة في المتصفح.','No voice for this language is available in your browser.')}</p>}</div>}{question.input_mode==='text'?<form className="edu-answer-form" onSubmit={e=>{e.preventDefault();void submit(input)}}><label htmlFor="game-answer">{copy('إجابتك','Your answer')}</label><input id="game-answer" dir={targetDir} value={input} onChange={e=>setInput(e.target.value)} autoComplete="off" spellCheck={false} disabled={busy||!!feedback}/><button className="edu-primary" disabled={busy||!!feedback||!input.trim()}>{copy('تحقّق','Check')}</button></form>:<div className="edu-choices">{question.choices.map((choice,i)=><button key={`${i}:${choice}`} disabled={busy||!!feedback} aria-pressed={selected===choice} onClick={()=>void submit(choice)}><span>{i+1}</span><b dir="auto">{choice}</b></button>)}</div>}{feedback&&<div className="edu-feedback" data-correct={feedback.correct} role="status"><strong>{feedback.correct?copy('صحيح!','Correct!'):copy('ليست صحيحة. سنراجع نفس العنصر.','Not quite. We’ll revisit this item.')}</strong><p>{question.hint}</p><button className="edu-primary" onClick={advance} disabled={busy}>{feedback.finished?copy('حفظ الجولة','Save round'):feedback.correct?copy('التالي','Next'):copy('حاول مجددًا','Try again')}</button></div>}</>}
    {challenge?.type==='ordering'&&<><p>{copy('ابنِ جملة صحيحة من الكلمات. احذف كلمة بالنقر عليها لإعادة وضعها.','Build a grammatical sentence. Tap a placed word to reposition it.')}</p><div className="edu-sentence" dir={targetDir} aria-label={copy('الجملة التي تبنيها','Your sentence')}>{order.length?order.map((id,i)=><button key={id} disabled={busy} onClick={()=>setOrder(value=>value.filter(item=>item!==id))}><small>{i+1}</small> {challenge.items.find(item=>item.id===id)?.label}</button>):<span>{copy('اختر الكلمات بالترتيب','Select words in order')}</span>}</div><div className="edu-word-pool" dir={targetDir}>{challenge.items.map(item=><button key={item.id} disabled={busy||order.includes(item.id)} onClick={()=>setOrder(value=>value.includes(item.id)?value:[...value,item.id])}>{item.label}</button>)}</div><button disabled={busy||!order.length} onClick={()=>setOrder([])}>{copy('إعادة الترتيب','Clear order')}</button><button className="edu-primary" disabled={busy||order.length!==challenge.items.length} onClick={()=>{if(lock.current)return;trace.current=[{order:[...order]}];void finish()}}>{copy('تصحيح وحفظ الجملة','Score and save sentence')}</button></>}
  </>}</section>
}

export function ArenaGame({gameId,targetLanguage,difficulty,arabic,title,onExit,onReplay}:Props) {
  const userId=useAuthStore(s=>s.user?.id)
  const [state,setState]=useState<ArenaState|null>(null)
  const [busy,setBusy]=useState(false)
  const [error,setError]=useState('')
  const [relaxed,setRelaxed]=useState(false)
  const [still,setStill]=useState(false)
  const [order,setOrder]=useState<string[]>([])
  const [left,setLeft]=useState<string|null>(null)
  const [seconds,setSeconds]=useState(0)
  const [audioError,setAudioError]=useState(false)
  const lock=useRef(false)
  const mounted=useRef(true)
  const pending=useRef<ArenaMove|null>(null)
  const snapshot=useRef<ArenaState|null>(null)
  const published=useRef('')
  const key=`juba:arcade:${userId}:${targetLanguage}:${gameId}:${difficulty}`
  const text=(ar:string,en:string)=>arabic?ar:en
  const accept=useCallback((next:ArenaState)=>{
    if(!mounted.current)return
    snapshot.current=next;setState(next);setOrder([]);setLeft(null);setError('')
    try {
      if(next.phase==='finished')sessionStorage.removeItem(key)
      else sessionStorage.setItem(key,next.session_id)
    } catch {}
    if(next.result&&published.current!==next.session_id){published.current=next.session_id;publishResult(next.result)}
  },[key])

  useEffect(()=>{
    mounted.current=true
    let cancelled=false
    let saved:string|null=null
    try{saved=sessionStorage.getItem(key)}catch{}
    if(saved){
      lock.current=true;setBusy(true)
      void readArena(saved).then(next=>{if(!cancelled)accept(next)}).catch(()=>{
        if(!cancelled){try{sessionStorage.removeItem(key)}catch{};setError(text('تعذر استعادة الجولة. يمكنك بدء جولة جديدة.','Could not restore the round. Start a new round.'))}
      }).finally(()=>{if(!cancelled){lock.current=false;setBusy(false)}})
    }
    return()=>{cancelled=true;mounted.current=false;window.speechSynthesis?.cancel()}
  },[accept,key])

  async function start(){
    if(lock.current)return
    lock.current=true;setBusy(true);setError('')
    try{accept(await startArena(gameId,targetLanguage,difficulty,relaxed))}
    catch(err){if(mounted.current)setError(err instanceof Error?err.message:text('تعذر بدء الجولة','Could not start round'))}
    finally{if(mounted.current){lock.current=false;setBusy(false)}}
  }
  const send=useCallback(async(kind:ArenaMove['kind'],value='',tiles:string[]=[]):Promise<void>=>{
    const current=snapshot.current
    if(!current||lock.current)return
    lock.current=true;setBusy(true);setError('')
    const request=pending.current??{action_id:crypto.randomUUID(),version:current.version,kind,value,order:tiles}
    pending.current=request
    try{
      const next=await moveArena(current.session_id,request)
      pending.current=null;accept(next)
    }catch{
      // Re-read after a lost response; retry the same action ID if uncommitted.
      try{
        const next=await readArena(current.session_id)
        if(next.version>request.version){pending.current=null;accept(next)}
        else if(mounted.current)setError(text('لم تُحفظ الحركة. أعد إرسالها بالزر أدناه.','Move not saved. Retry it below.'))
      }catch{if(mounted.current)setError(text('انقطع الاتصال. حركتك محفوظة لإعادة الإرسال.','Connection lost. Your move is kept for retry.'))}
    }finally{if(mounted.current){lock.current=false;setBusy(false)}}
  },[accept,arabic])

  useEffect(()=>{
    if(!state?.deadline||state.phase!=='playing')return
    const tick=()=>{
      const remain=Math.max(0,Math.ceil(state.deadline!-Date.now()/1000))
      setSeconds(remain)
      if(remain===0&&!lock.current&&!pending.current)void send('timeout')
    }
    tick();const interval=setInterval(tick,250)
    return()=>clearInterval(interval)
  },[state?.deadline,state?.phase,send])
  useEffect(()=>{
    if(state?.game!=='memory'||state.phase!=='playing'||state.cards?.filter(c=>c.opened).length!==2||pending.current)return
    const timer=setTimeout(()=>void send('hide'),1100)
    return()=>clearTimeout(timer)
  },[state,send])

  function listen(){
    const utteranceText=state?.question?.prompt
    if(!utteranceText||!window.speechSynthesis){setAudioError(true);return}
    const voice=window.speechSynthesis.getVoices().find(v=>v.lang.toLowerCase().split('-')[0]===targetLanguage.toLowerCase().split('-')[0])
    if(!voice){setAudioError(true);return}
    window.speechSynthesis.cancel()
    const utterance=new SpeechSynthesisUtterance(utteranceText)
    utterance.voice=voice;utterance.lang=targetLanguage;utterance.rate=.85
    utterance.onerror=()=>{if(mounted.current)setAudioError(true)}
    window.speechSynthesis.speak(utterance)
  }
  const frozen=busy||!!pending.current||state?.phase!=='playing'
  const tiles=state?.question?.tiles??[]
  const dir=targetLanguage.startsWith('ar')?'rtl':'ltr'
  return <section className="edu-stage arcade-stage" aria-busy={busy} data-game={gameId}>
    <header className="edu-session-head"><button onClick={onExit} disabled={busy}>{text('العودة للألعاب','Back to games')}</button><h2>{title}</h2><Target size={24}/></header>
    {error&&<div className="edu-error" role="alert"><p>{error}</p>{pending.current&&<button onClick={()=>void send(pending.current!.kind)} disabled={busy}>{text('إعادة إرسال الحركة','Retry move')}</button>}</div>}
    {!state?<div className="arcade-rules"><h3>{text('تحدٍ يمكنك الفوز به أو خسارته','A challenge you can win or lose')}</h3><p>{gameId==='memory'?text('اقلب بطاقتين وابحث عن الكلمة ومعناها. أكمل الأزواج قبل نفاد الحركات.','Flip two cards to find a word and its meaning. Find every pair before running out of moves.'):gameId==='matching'?text('اختر كلمة ثم معناها. لديك ثلاث محاولات خاطئة قبل انتهاء الجولة.','Pick a word and its meaning. Three mistakes end the round.'):gameId==='quick_choice'?text('اصطد المعنى الصحيح للكلمة من الأهداف المتحركة. خمس جولات وثلاث فرص.','Catch the correct meaning among moving targets. Five rounds, three lives.'):text('ركّب حروف الكلمة التي يصفها المعنى. كل حرف يُستخدم مرة واحدة. خمس جولات وثلاث فرص.','Build the word described by its meaning. Use each letter once. Five rounds, three lives.')}</p>
      {gameId==='quick_choice'&&<label><input type="checkbox" checked={relaxed} onChange={e=>setRelaxed(e.target.checked)}/> {text('تدريب دون مؤقت، بنفس XP','Untimed practice, same XP')}</label>}
      <button className="edu-primary" onClick={()=>void start()} disabled={busy}>{busy?text('جارٍ التحضير…','Preparing…'):text('ابدأ اللعب','Start playing')}</button></div>:<>
      <div className="arcade-hud"><span><Check size={18}/> {state.correct}/{state.total}</span>{gameId==='memory'?<span><RotateCcw size={18}/> {state.attempts}/{state.max_moves} {text('حركة','moves')}</span>:<span aria-label={text('الفرص المتبقية','Lives remaining')}>{[0,1,2].map(i=><Heart key={i} size={22} fill={i<state.lives?'currentColor':'none'} data-empty={i>=state.lives}/>)}</span>}{state.deadline&&<span className="arcade-clock" aria-label={text('الثواني المتبقية','Seconds remaining')}>{seconds}s</span>}</div>
      <progress value={state.correct} max={state.total} aria-label={text('تقدم الجولة','Round progress')}/>
      {state.result?<div className="arcade-result" role="status"><strong className="arcade-emblem">{state.result.won?'★':'↻'}</strong><h3>{state.result.won?text('اجتزت التحدي!','Challenge cleared!'):text('انتهت الجولة، جرّب من جديد','Round over. Try again')}</h3><p>{state.result.round_correct}/{state.result.round_questions} · +{state.result.xp_earned} XP</p><p>{text('حُفظت النتيجة ونقاط التعلم على الخادم.','Result and learning XP saved by the server.')}</p><button className="edu-primary" onClick={onReplay}>{text('جولة جديدة','New round')}</button><button onClick={onExit}>{text('اختر لعبة أخرى','Choose another game')}</button></div>:<>
      {gameId==='quick_choice'&&state.question&&<><div className="arcade-cue"><small>{text('اصطد معناها','Catch its meaning')}</small><h3 dir={dir}>{state.question.prompt}</h3><button onClick={listen} aria-label={text('نطق الكلمة','Hear the word')}><Volume2 size={20}/></button></div><label className="arcade-motion"><input type="checkbox" checked={still} onChange={e=>setStill(e.target.checked)}/><Move size={16}/>{text('إيقاف حركة الأهداف','Keep targets still')}</label><div className="arcade-hunt" data-still={still||state.phase!=='playing'}>{state.question.choices?.map((choice,i)=><button key={choice} className={`arcade-target target-${i}`} disabled={frozen} onClick={()=>void send('answer',choice)}><span>{i+1}</span><b dir="auto">{choice}</b></button>)}</div>{audioError&&<p role="status">{text('النطق غير متاح. يمكنك اللعب بالنص الظاهر.','Audio unavailable. You can play using the visible word.')}</p>}</>}
      {(gameId==='spelling'||gameId==='word_scramble')&&state.question&&<><h3 className="edu-prompt" dir="auto">{state.question.prompt}</h3><div className="arcade-letter-slots" dir={dir} aria-label={text('الكلمة التي تركّبها','Word you are building')}>{tiles.map((tile,i)=>{const placed=tiles.find(t=>t.id===order[i]);return <button key={tile.id} disabled={frozen||!placed} onClick={()=>setOrder(items=>items.filter((_,index)=>index!==i))} aria-label={placed?text(`إزالة ${placed.label}`,`Remove ${placed.label}`):text(`موضع ${i+1}`,`Slot ${i+1}`)}>{placed?.label??'·'}</button>})}</div><div className="arcade-letter-pool" dir={dir}>{tiles.map(tile=><button key={tile.id} disabled={frozen||order.includes(tile.id)} onClick={()=>setOrder(ids=>ids.includes(tile.id)?ids:[...ids,tile.id])}>{tile.label}</button>)}</div><div className="arcade-actions"><button onClick={()=>setOrder([])} disabled={frozen||!order.length}><RotateCcw size={18}/> {text('مسح','Clear')}</button><button className="edu-primary" disabled={frozen||order.length!==tiles.length} onClick={()=>void send('answer','',order)}>{text('تحقّق من الكلمة','Check word')}</button></div></>}
      {gameId==='memory'&&<div className="arcade-memory">{state.cards?.map((card,i)=><button key={card.id} className="arcade-card" data-face={card.opened||card.matched} data-matched={card.matched} disabled={frozen||card.matched||card.opened||state.cards!.filter(c=>c.opened).length===2} onClick={()=>void send('flip',card.id)} aria-label={card.label??text(`بطاقة مخفية ${i+1}`,`Hidden card ${i+1}`)}><span className="arcade-card-back" aria-hidden="true">✦</span><span className="arcade-card-front" dir="auto">{card.label??''}</span></button>)}</div>}
      {gameId==='matching'&&<div className="edu-matching">{(['word','meaning'] as const).map(side=><div key={side}>{state.cards?.filter(c=>c.side===side).map(card=><button key={card.id} disabled={frozen||card.matched||(side==='meaning'&&!left)} aria-pressed={left===card.id} onClick={()=>{if(side==='word')setLeft(card.id);else if(left)void send('pair','',[left,card.id])}} dir="auto">{card.label}</button>)}</div>)}</div>}
      {state.feedback&&<div className="edu-feedback" data-correct={state.feedback.correct} role="status"><strong>{state.feedback.correct?text('أحسنت!','Nice catch!'):text('ليست مطابقة. تذكّرها للمرة القادمة.','Not a match. Remember it for next time.')}</strong>{state.feedback.answer&&<p dir="auto">{state.feedback.answer} · {state.feedback.meaning}</p>}{state.phase==='feedback'&&<button className="edu-primary" disabled={busy||!!pending.current} onClick={()=>void send('continue')}>{text('الجولة التالية','Next round')}</button>}</div>}
      <button className="arcade-end" disabled={busy||!!pending.current} onClick={()=>void send('leave')}>{text('إنهاء وحفظ ما تعلمته','End and save learning')}</button>
      </>}
    </>}
  </section>
}
