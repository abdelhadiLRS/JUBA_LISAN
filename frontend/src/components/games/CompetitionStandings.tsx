'use client'

import {useCallback, useEffect, useRef, useState} from 'react'
import {useLocale} from 'next-intl'
import {apiFetch} from '@/lib/api'
import {useLanguageStore} from '@/store/language'
import {subscribeToLearningProgressUpdated} from '@/lib/learning-progress'
import './competition-standings.css'

type Entry = {user_id:number;username:string;display_name:string;xp:number;rank:number;is_current_user:boolean}
type Board = {target_language:string;period:string;total:number;offset:number;limit:number;entries:Entry[];current_user:Entry|null}
type League = {season_id:number|null;target_language:string;week_start:string;week_end:string;ends_at:string;joined:boolean;tier:string;finalized:boolean;next_tier:string|null;total:number;entries:Entry[];current_user:Entry|null}
const PAGE_SIZE=10
const arabicTiers:Record<string,string>={bronze:'البرونزي',silver:'الفضي',gold:'الذهبي',sapphire:'الياقوت الأزرق',ruby:'الياقوت الأحمر',diamond:'الماسي'}

export default function CompetitionStandings(){
  const arabic=useLocale().startsWith('ar')
  const language=useLanguageStore(state=>state.activeLanguage?.code)
  const switching=useLanguageStore(state=>state.isSwitching)
  const [board,setBoard]=useState<Board|null>(null)
  const [league,setLeague]=useState<League|null>(null)
  const [period,setPeriod]=useState('week')
  const [offset,setOffset]=useState(0)
  const [loading,setLoading]=useState(true)
  const [joining,setJoining]=useState(false)
  const [boardError,setBoardError]=useState(false)
  const [leagueError,setLeagueError]=useState(false)
  const [joinError,setJoinError]=useState(false)
  const [updated,setUpdated]=useState(false)
  const generation=useRef(0)
  const joinLock=useRef(false)
  const context=useRef(0)
  const refresh=useRef<()=>Promise<void>>(async()=>{})
  const text=(ar:string,en:string)=>arabic?ar:en
  const load=useCallback(async()=>{
    if(!language||switching)return
    const epoch=++generation.current
    setLoading(true);setUpdated(false)
    const query='target_language='+encodeURIComponent(language)
    const [rankings,division]=await Promise.allSettled([
      apiFetch(`/api/leaderboard?${query}&period=${period}&limit=${PAGE_SIZE}&offset=${offset}`).then(async response=>{if(!response.ok)throw new Error();return await response.json() as Board}),
      apiFetch(`/api/leagues/current?${query}&limit=${PAGE_SIZE}`).then(async response=>{if(!response.ok)throw new Error();return await response.json() as League}),
    ])
    if(epoch!==generation.current)return
    setBoardError(rankings.status==='rejected');setLeagueError(division.status==='rejected')
    setBoard(rankings.status==='fulfilled'?rankings.value:null)
    setLeague(division.status==='fulfilled'?division.value:null)
    setLoading(false);setUpdated(rankings.status==='fulfilled'&&division.status==='fulfilled')
  },[language,switching,period,offset])
  refresh.current=load
  useEffect(()=>{
    context.current+=1;setBoard(null);setLeague(null);setOffset(0);setJoinError(false)
    return()=>{context.current+=1;generation.current+=1}
  },[language,switching])
  useEffect(()=>{
    void load()
    const unsubscribe=subscribeToLearningProgressUpdated(()=>{void load()})
    const onVisible=()=>{if(document.visibilityState==='visible')void load()}
    document.addEventListener('visibilitychange',onVisible)
    return()=>{generation.current+=1;unsubscribe();document.removeEventListener('visibilitychange',onVisible)}
  },[load])
  async function join(){
    if(!language||switching||joinLock.current||league?.joined)return
    joinLock.current=true;setJoining(true);setJoinError(false)
    const current=context.current
    try{
      const response=await apiFetch('/api/leagues/join',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_language:language})})
      if(!response.ok)throw new Error()
      // GET supplies the same canonical view as subsequent progress refreshes.
      if(current===context.current)await refresh.current()
    }catch{if(current===context.current)setJoinError(true)}finally{
      joinLock.current=false
      // Always reload the latest language after an old-language join settles.
      setJoining(false)
      if(current!==context.current)void refresh.current()
    }
  }
  function rows(entries:Entry[]){
    return <ol className="competition-rows">{entries.map(entry=><li key={entry.user_id} data-current={entry.is_current_user}><span className="competition-rank">{entry.rank}</span><span><strong>{entry.display_name}</strong><small>@{entry.username}{entry.is_current_user?' · '+text('أنت','You'):''}</small></span><b>{entry.xp.toLocaleString()} XP</b></li>)}</ol>
  }
  function own(entry:Entry|null){
    return entry?<p className="competition-own">{text('ترتيبك','Your rank')}: <strong>#{entry.rank}</strong> · {entry.xp.toLocaleString()} XP</p>:null
  }
  if(!language||switching)return <section className="juba-page-shell competition-panel" role="status">{text('جارٍ تحديد لغة المنافسة…','Loading your competition language…')}</section>
  return <section className="juba-page-shell competition-panel" dir={arabic?'rtl':'ltr'} aria-label={text('الترتيب والدوريات','Leaderboard and Leagues')}>
    <header className="competition-heading"><div><h2>{text('الترتيب والدوريات','Leaderboard and Leagues')}</h2><p>{text('نتائج الألعاب المحفوظة تُحتسب تلقائيًا. لا نضيف النقاط مرة ثانية.','Saved game results count automatically. Points are never added a second time.')} <b dir="ltr">{language}</b></p></div><button disabled={loading||joining} onClick={()=>void load()}>{text('تحديث','Refresh')}</button></header>
    {updated&&<p className="competition-sync" role="status">{text('تمت مزامنة الترتيب مع النقاط المحفوظة.','Standings synced with saved XP.')}</p>}
    <div className="competition-columns">
      <section className="competition-section" aria-busy={loading}><header><h3>{text('لوحة المتصدرين','Leaderboard')}</h3><label>{text('الفترة','Period')}<select value={period} disabled={joining} onChange={event=>{setPeriod(event.target.value);setOffset(0)}}><option value="day">{text('اليوم','Today')}</option><option value="week">{text('هذا الأسبوع','This week')}</option><option value="month">{text('هذا الشهر','This month')}</option><option value="all">{text('كل الوقت','All time')}</option></select></label></header>
        {loading?<p role="status">{text('جارٍ تحديث الترتيب…','Refreshing standings…')}</p>:boardError?<div role="alert"><p>{text('تعذر تحميل الترتيب. نتيجة اللعبة المحفوظة لم تتغير.','Could not load rankings. Your saved game result is unchanged.')}</p><button onClick={()=>void load()}>{text('إعادة المحاولة','Retry')}</button></div>:board?<>{own(board.current_user)}{board.entries.length?rows(board.entries):<p>{text('لا يوجد مشاركون في هذه الصفحة.','No participants on this page.')}</p>}<nav className="competition-pager" aria-label={text('صفحات الترتيب','Leaderboard pages')}><button disabled={offset===0} onClick={()=>setOffset(value=>Math.max(0,value-PAGE_SIZE))}>{text('السابق','Previous')}</button><span>{board.total?`${offset+1}-${Math.min(offset+PAGE_SIZE,board.total)} / ${board.total}`:'0'}</span><button disabled={offset+PAGE_SIZE>=board.total} onClick={()=>setOffset(value=>value+PAGE_SIZE)}>{text('التالي','Next')}</button></nav></>:null}
      </section>
      <section className="competition-section" aria-busy={loading||joining}><header><h3>{text('دوريك الأسبوعي','Your weekly league')}</h3>{league?.joined&&<strong>{arabic?arabicTiers[league.tier]??league.tier:league.tier}</strong>}</header>
        {loading?<p role="status">{text('جارٍ تحديث الدوري…','Refreshing league…')}</p>:leagueError?<div role="alert"><p>{text('تعذر تحميل الدوري.','Could not load your league.')}</p><button onClick={()=>void load()}>{text('إعادة المحاولة','Retry')}</button></div>:league?.joined?<><p>{league.week_start} / {league.week_end}</p>{own(league.current_user)}{league.entries.length?rows(league.entries):<p>{text('لم يُسجّل مشاركون بعد.','No participants recorded yet.')}</p>}{league.total>PAGE_SIZE&&<p>{text('نعرض أول عشرة مشاركين، وترتيبك ظاهر حتى إن كنت خارجهم.','Showing the top ten; your rank is shown even outside this page.')}</p>}</>:<div className="competition-enroll"><p>{text('انضم لهذا الأسبوع ليظهر ترتيبك وتشارك في الترقيات. سيظهر اسمك العام ونقاطك للمشاركين.','Join this week to appear in standings and compete for promotion. Your public name and XP will be visible to participants.')}</p><button className="competition-primary" disabled={joining||leagueError} onClick={()=>void join()}>{joining?text('جارٍ الانضمام…','Joining…'):text('انضم إلى الدوري','Join league')}</button><p>{text('تُحتسب نقاط اللغة المسجّلة لهذا الأسبوع، بما فيها الألعاب السابقة للانضمام.','Saved XP for this language and week counts, including games played before joining.')}</p></div>}
        {joinError&&<p role="alert">{text('تعذر الانضمام. نقاطك محفوظة؛ أعد المحاولة.','Could not join. Your XP is saved; retry enrollment.')}</p>}
      </section>
    </div><p className="competition-footnote">{text('الترتيب يشمل XP الألعاب والتعلم ومكافآتها حسب اللغة والفترة. تتساوى الرتب عند تساوي النقاط، وتُطبّق ترقيات الأسبوع عند أول انضمام للأسبوع التالي.','Rankings include game, learning and reward XP for the selected language and period. Equal scores share a rank. Weekly promotions settle on the first enrollment in the next week.')}</p>
  </section>
}
