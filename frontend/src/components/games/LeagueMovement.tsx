'use client'

import Link from 'next/link'
import {useCallback,useEffect,useRef,useState} from 'react'
import {useLocale} from 'next-intl'
import {apiFetch} from '@/lib/api'
import {useLanguageStore} from '@/store/language'
import {subscribeToLearningProgressUpdated} from '@/lib/learning-progress'
import {LEAGUE_TIERS,projectedMovement,settledMovement,type Movement} from '@/lib/games/league-movement'
import './league-movement.css'

type Entry={user_id:number;display_name:string;rank:number;xp:number;is_current_user:boolean}
type Season={season_id:number|null;joined:boolean;target_language:string;tier:string;next_tier:string|null;total:number;week_start:string;week_end:string;finalized:boolean;current_user:Entry|null;entries:Entry[]}
const names:Record<string,string>={bronze:'البرونزي',silver:'الفضي',gold:'الذهبي',sapphire:'الياقوت الأزرق',ruby:'الياقوت الأحمر',diamond:'الماسي'}
export default function LeagueMovement(){
  const arabic=useLocale().startsWith('ar')
  const language=useLanguageStore(s=>s.activeLanguage?.code)
  const switching=useLanguageStore(s=>s.isSwitching)
  const [season,setSeason]=useState<Season|null>(null)
  const [history,setHistory]=useState<Season[]>([])
  const [loading,setLoading]=useState(true)
  const [error,setError]=useState(false)
  const [historyError,setHistoryError]=useState(false)
  const [offset,setOffset]=useState(0)
  const epoch=useRef(0)
  const t=(ar:string,en:string)=>arabic?ar:en
  const tierName=(tier:string)=>arabic?names[tier]??tier:tier
  const label=(movement:Movement)=>movement==='promotion'?t('↑ منطقة الصعود','↑ Promotion zone'):movement==='demotion'?t('↓ منطقة الهبوط','↓ Demotion zone'):t('= منطقة الثبات','= Stay zone')
  const load=useCallback(async()=>{
    if(!language||switching)return
    const request=++epoch.current;setLoading(true)
    const query='target_language='+encodeURIComponent(language)
    const [current,past]=await Promise.allSettled([
      apiFetch(`/api/leagues/current?${query}&limit=10&offset=${offset}`).then(async r=>{if(!r.ok)throw new Error();return await r.json() as Season}),
      apiFetch(`/api/leagues/history?${query}&limit=8`).then(async r=>{if(!r.ok)throw new Error();return await r.json() as Season[]}),
    ])
    if(request!==epoch.current)return
    setError(current.status==='rejected');setHistoryError(past.status==='rejected')
    setSeason(current.status==='fulfilled'?current.value:null)
    setHistory(past.status==='fulfilled'?past.value:[]);setLoading(false)
  },[language,switching,offset])
  useEffect(()=>{setOffset(0);setSeason(null);setHistory([])},[language,switching])
  useEffect(()=>{
    void load()
    const unsubscribe=subscribeToLearningProgressUpdated(()=>void load())
    const visible=()=>{if(document.visibilityState==='visible')void load()}
    document.addEventListener('visibilitychange',visible)
    return()=>{epoch.current++;unsubscribe();document.removeEventListener('visibilitychange',visible)}
  },[load])
  const own=season?.current_user
  const movement=season&&own?projectedMovement(season.tier,own.rank,own.xp,season.total):null
  const quota=season&&season.total>=5?Math.max(1,Math.floor(season.total/5)):0
  const index=season?LEAGUE_TIERS.indexOf(season.tier as typeof LEAGUE_TIERS[number]):-1
  const destination=movement&&index>=0?LEAGUE_TIERS[Math.max(0,Math.min(5,index+(movement==='promotion'?1:movement==='demotion'?-1:0)))]:null
  return <section className="juba-page-shell league-movement" dir={arabic?'rtl':'ltr'} aria-label={t('الصعود والهبوط','Promotion and demotion')}>
    <header className="league-movement-heading"><div><h2>{t('مسار الدوري','League movement')}</h2><p>{t('التوقع يتغير مع النقاط. القرار النهائي يظهر بعد حسم الموسم.','Projections change with scores. Final decisions appear after season settlement.')}</p></div><button disabled={loading||switching||!language} onClick={()=>void load()}>{t('تحديث','Refresh')}</button></header>
    {!language||switching||loading?<p role="status">{t('جارٍ تحميل الدوري…','Loading league…')}</p>:error?<div role="alert"><p>{t('تعذر تحميل حالة الدوري.','Could not load league status.')}</p><button onClick={()=>void load()}>{t('أعد المحاولة','Retry')}</button></div>:season&&!season.joined?<p>{t('انضم إلى دوري هذا الأسبوع من لوحة الترتيب لتفعيل توقع الصعود والهبوط.','Join this week’s league in the standings panel to see your movement projection.')}</p>:season?<>
      <ol className="league-ladder" aria-label={t('درجات الدوري','League tiers')}>{LEAGUE_TIERS.map((tier,i)=><li key={tier} aria-current={tier===season.tier?'step':undefined}><span>{i+1}</span><strong>{tierName(tier)}</strong>{tier===season.tier&&<small>{t('دوريك الحالي','Current tier')}</small>}</li>)}</ol>
      {own&&movement&&destination?<div className="league-projection" data-movement={movement} role="status"><strong>{label(movement)}</strong><p>{t('إذا انتهى الأسبوع بهذا الترتيب:','If the week ended with these standings:')} <b>{tierName(season.tier)} → {tierName(destination)}</b></p><p>#{own.rank} · {own.xp.toLocaleString()} XP · {season.total} {t('مشاركين','participants')}</p><small>{t('توقع فقط، لم تُطبّق ترقية أو هبوط بعد.','Projection only. No promotion or demotion has been applied yet.')}</small></div>:<p>{t('لا يتوفر ترتيب مؤهل لحساب التوقع.','No eligible personal rank is available for projection.')}</p>}
      <div className="league-zones"><div data-movement="promotion"><strong>{t('↑ صعود','↑ Promotion')}</strong><p>{index===5?t('أنت في أعلى دوري.','You are in the highest tier.'):quota?t(`الرتب من 1 إلى ${quota}، بشرط XP أكبر من صفر.`,`Ranks 1 through ${quota}, with positive XP.`):t('يلزم خمسة مشاركين مؤهلين على الأقل.','Requires at least five eligible participants.')}</p></div><div data-movement="stay"><strong>{t('= ثبات','= Stay')}</strong><p>{t('ما بين منطقتي الصعود والهبوط، مع احترام التعادل.','Between movement zones, respecting shared ranks.')}</p></div><div data-movement="demotion"><strong>{t('↓ هبوط','↓ Demotion')}</strong><p>{index===0?t('لا هبوط تحت البرونزي.','No tier below Bronze.'):quota?t(`الرتب الأكبر من ${season.total-quota}.`,`Ranks greater than ${season.total-quota}.`):t('لا هبوط في مجموعة أقل من خمسة.','No demotion in groups smaller than five.')}</p></div></div>
      <p className="league-rule">{t('أصحاب النقاط المتساوية يتشاركون الرتبة؛ لا نفصل المتعادلين عند الحد.','Equal XP shares a rank; ties are never split at a boundary.')} {season.week_start} / {season.week_end}</p>
      <ol className="league-movement-rows">{season.entries.map(entry=>{const zone=projectedMovement(season.tier,entry.rank,entry.xp,season.total);return <li key={entry.user_id} data-movement={zone} data-current={entry.is_current_user}><span>#{entry.rank}</span><strong>{entry.display_name}{entry.is_current_user?' · '+t('أنت','You'):''}</strong><span>{entry.xp.toLocaleString()} XP</span><small>{label(zone)}</small></li>})}</ol>
      <nav className="league-page-controls" aria-label={t('صفحات الدوري','League pages')}><button disabled={offset===0} onClick={()=>setOffset(n=>Math.max(0,n-10))}>{t('السابق','Previous')}</button><span>{season.total?`${offset+1}-${Math.min(offset+10,season.total)} / ${season.total}`:'0'}</span><button disabled={offset+10>=season.total} onClick={()=>setOffset(n=>n+10)}>{t('التالي','Next')}</button><button disabled={!season.total} onClick={()=>setOffset(Math.max(0,Math.floor((season.total-1)/10)*10))}>{t('عرض نهاية الترتيب','View bottom ranks')}</button></nav>
    </>:null}
    <section className="league-outcomes"><h3>{t('نتائج الأسابيع السابقة','Previous weekly outcomes')}</h3>{historyError?<p role="alert">{t('تعذر تحميل السجل.','Could not load history.')}</p>:loading?null:history.length?history.map(past=>{const settled=past.finalized?settledMovement(past.tier,past.next_tier):null;return <div key={past.season_id} data-movement={settled??'pending'}><span>{past.week_start} / {past.week_end}</span><strong>{settled?settled==='promotion'?t('↑ صعود مؤكد','↑ Promoted'):settled==='demotion'?t('↓ هبوط مؤكد','↓ Demoted'):t('= ثبات مؤكد','= Tier retained'):t('بانتظار الحسم','Awaiting settlement')}</strong><p>{tierName(past.tier)}{settled&&past.next_tier?' → '+tierName(past.next_tier):''}{past.current_user?' · #'+past.current_user.rank+' · '+past.current_user.xp+' XP':''}</p></div>}):<p>{t('لا توجد مواسم سابقة مسجلة.','No previous seasons recorded.')}</p>}<p className="league-rule">{t('الحسم يتم عند أول انضمام للأسبوع التالي. السجل يعرض القرار المحفوظ، لا توقعًا محليًا.','Settlement happens on the first enrollment next week. History shows persisted decisions, not local predictions.')}</p></section>
    <Link href="/leagues">{t('فتح صفحة الدوري','Open league page')}</Link>
  </section>
}
