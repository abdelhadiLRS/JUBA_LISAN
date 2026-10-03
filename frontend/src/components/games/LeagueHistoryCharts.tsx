'use client'

import {useCallback,useEffect,useId,useRef,useState} from 'react'
import {useLocale} from 'next-intl'
import {apiFetch} from '@/lib/api'
import {useLanguageStore} from '@/store/language'
import {subscribeToLearningProgressUpdated} from '@/lib/learning-progress'
import {chartPoints,chronologicalHistory,seasonValue,type HistoricalSeason,type HistoryMetric} from '@/lib/games/league-history'
import {settledMovement} from '@/lib/games/league-movement'
import './league-history-charts.css'

const PAGE=12
const arTiers:Record<string,string>={bronze:'البرونزي',silver:'الفضي',gold:'الذهبي',sapphire:'الياقوت الأزرق',ruby:'الياقوت الأحمر',diamond:'الماسي'}
export default function LeagueHistoryCharts(){
  const locale=useLocale(),arabic=locale.startsWith('ar')
  const language=useLanguageStore(s=>s.activeLanguage?.code)
  const switching=useLanguageStore(s=>s.isSwitching)
  const [seasons,setSeasons]=useState<HistoricalSeason[]>([])
  const [metric,setMetric]=useState<HistoryMetric>('xp')
  const [settledOnly,setSettledOnly]=useState(true)
  const [selected,setSelected]=useState<number|null>(null)
  const [loading,setLoading]=useState(true)
  const [error,setError]=useState(false)
  const [more,setMore]=useState(false)
  const [pages,setPages]=useState(1)
  const generation=useRef(0)
  const titleId=useId(),descriptionId=useId()
  const t=(ar:string,en:string)=>arabic?ar:en
  const tier=(value:string)=>arabic?arTiers[value]??value:value
  const metricLabel=metric==='xp'?'XP':metric==='rank'?t('الترتيب','Rank'):t('درجة الدوري','League tier')
  const load=useCallback(async()=>{
    if(!language||switching)return
    const request=++generation.current;setLoading(true);setError(false)
    try{
      // Re-read all loaded pages after progress changes; never append stale pages.
      const responses=await Promise.all(Array.from({length:pages},(_,index)=>apiFetch(`/api/leagues/history?target_language=${encodeURIComponent(language)}&limit=${PAGE}&offset=${index*PAGE}`).then(async r=>{if(!r.ok)throw new Error();const data=await r.json();if(!Array.isArray(data))throw new Error();return data as HistoricalSeason[]})))
      if(request!==generation.current)return
      setSeasons(responses.flat());setMore(responses.at(-1)?.length===PAGE)
    }catch{if(request===generation.current)setError(true)}finally{if(request===generation.current)setLoading(false)}
  },[language,switching,pages])
  useEffect(()=>{setSeasons([]);setSelected(null);setPages(1);setMore(false);return()=>{generation.current++}},[language,switching])
  useEffect(()=>{
    void load()
    const unsubscribe=subscribeToLearningProgressUpdated(()=>void load())
    const visible=()=>{if(document.visibilityState==='visible')void load()}
    document.addEventListener('visibilitychange',visible)
    return()=>{generation.current++;unsubscribe();document.removeEventListener('visibilitychange',visible)}
  },[load])
  const ordered=chronologicalHistory(seasons,settledOnly)
  const points=chartPoints(ordered,metric)
  const current=ordered.find(season=>season.season_id===selected)??ordered.at(-1)??null
  const movement=current?.finalized?settledMovement(current.tier,current.next_tier):null
  const latest=points.at(-1),previous=points.at(-2)
  const delta=latest&&previous?latest.value-previous.value:null
  function valueLabel(season:HistoricalSeason){const value=seasonValue(season,metric);return value===null?t('غير متاح','Unavailable'):metric==='tier'?tier(season.tier):metric==='rank'?'#'+value:value.toLocaleString(locale)+' XP'}
  return <section className="juba-page-shell league-history" dir={arabic?'rtl':'ltr'} aria-label={t('رسوم تاريخ الدوري','League history charts')}>
    <header className="league-history-heading"><div><h2>{t('رحلتك عبر المواسم','Your season journey')}</h2><p>{t('نقاط وترتيب ودرجات من سجل مشاركاتك الفعلي.','XP, ranks and tiers from your actual participation history.')} <b dir="ltr">{language}</b></p></div><button disabled={loading||!language||switching} onClick={()=>void load()}>{t('تحديث السجل','Refresh history')}</button></header>
    <div className="league-history-controls"><div role="group" aria-label={t('مقياس الرسم','Chart metric')}>{(['xp','rank','tier'] as HistoryMetric[]).map(value=><button key={value} aria-pressed={metric===value} onClick={()=>setMetric(value)}>{value==='xp'?'XP':value==='rank'?t('الترتيب','Rank'):t('درجة الدوري','League tier')}</button>)}</div><label><input type="checkbox" checked={settledOnly} onChange={event=>setSettledOnly(event.target.checked)}/>{t('المواسم المحسومة فقط','Settled seasons only')}</label></div>
    {loading||!language||switching?<p role="status">{t('جارٍ تحميل بيانات المواسم…','Loading season data…')}</p>:error?<div role="alert"><p>{t('تعذر تحديث السجل؛ لن نعرض البيانات القديمة على أنها محدثة.','Could not refresh history; older data is not presented as current.')}</p><button onClick={()=>void load()}>{t('إعادة المحاولة','Retry')}</button></div>:!ordered.length?<p>{settledOnly&&seasons.length?t('لا توجد مواسم محسومة ضمن السجل المحمّل. ألغِ المرشح لعرض المواسم المعلقة.','No settled seasons in the loaded history. Disable the filter to view pending seasons.'):t('لا توجد مشاركات تاريخية بعد. ستظهر مواسمك السابقة هنا دون بيانات تجريبية.','No historical participation yet. Previous seasons will appear here without demo data.')}</p>:<>
      <div className="league-history-chart-head"><h3>{metricLabel}</h3><span>{ordered.length} {t('موسمًا في العرض','seasons shown')}</span>{delta!==null&&<span>{t('التغير بين آخر مشاركتين','Change between latest participations')}: {delta>0?'+':''}{delta}{metric==='rank'?t(' (الأقل أفضل)',' (lower is better)'):''}</span>}</div>
      {points.length?<div className="league-chart-scroll"><svg viewBox="0 0 800 280" role="group" aria-labelledby={titleId} aria-describedby={descriptionId} className="league-chart" dir="ltr"><title id={titleId}>{t('تطور','History of')} {metricLabel}</title><desc id={descriptionId}>{t('اختر نقطة بالماوس أو لوحة المفاتيح لعرض تفاصيل الأسبوع. المسافة الأفقية تمثل الوقت الفعلي؛ الأسابيع بلا مشاركة لا تصبح صفرًا.','Select a point with mouse or keyboard for weekly details. Horizontal spacing represents real time; unplayed weeks are not converted to zero.')}</desc>
        {[40,86,132,178,224].map(y=><line key={y} x1="56" x2="744" y1={y} y2={y} className="league-grid-line"/>)}
        <text x="12" y="28" className="league-chart-label">{metricLabel}</text>
        {points.map((point,index)=>{const previousPoint=points[index-1];return <g key={point.season.season_id}>{previousPoint&&<line x1={previousPoint.x} y1={previousPoint.y} x2={point.x} y2={point.y} className="league-chart-trend" strokeDasharray={!point.season.finalized||!previousPoint.season.finalized?'6 5':undefined}/>}<g role="button" tabIndex={0} aria-label={`${point.season.week_start}: ${valueLabel(point.season)}, ${point.season.finalized?t('محسوم','settled'):t('معلق','pending')}`} aria-pressed={current?.season_id===point.season.season_id} onClick={()=>setSelected(point.season.season_id)} onKeyDown={event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();setSelected(point.season.season_id)}}} className="league-chart-point"><circle cx={point.x} cy={point.y} r="16" className="league-point-hit"/><circle cx={point.x} cy={point.y} r={current?.season_id===point.season.season_id?8:5} className="league-point-dot" data-pending={!point.season.finalized}/><title>{point.season.week_start}: {valueLabel(point.season)}</title></g>{(index===0||index===points.length-1)&&<text x={point.x} y="262" textAnchor="middle" className="league-chart-label">{point.season.week_start}</text>}</g>})}
      </svg></div>:<p>{t('هذا المقياس غير متاح للمواسم المعروضة. لا نستبدله بصفر.','This metric is unavailable for the displayed seasons. It is not replaced with zero.')}</p>}
      <p className="league-history-caption">{t('انقر نقطة لعرض قيمها. اختر الموسم من القائمة أيضًا. الرتبة 1 هي الأفضل؛ درجة الدوري تعني الدرجة التي شاركت بها، لا توقع الصعود.','Click a point for its values, or select a season below. Rank 1 is best; tier means the division you participated in, not a promotion forecast.')}</p>
      <label className="league-season-picker">{t('اختر موسمًا','Select season')}<select value={current?.season_id??''} onChange={event=>setSelected(Number(event.target.value))}>{ordered.map(season=><option key={season.season_id} value={season.season_id??''}>{season.week_start} / {season.week_end}{season.finalized?'':' · '+t('معلق','pending')}</option>)}</select></label>
      {current&&<section className="league-history-detail" aria-live="polite"><h3>{current.week_start} / {current.week_end}</h3><dl><div><dt>{t('الدرجة','Tier')}</dt><dd>{tier(current.tier)}</dd></div><div><dt>XP</dt><dd>{current.current_user?current.current_user.xp.toLocaleString(locale):t('غير متاح','Unavailable')}</dd></div><div><dt>{t('الترتيب','Rank')}</dt><dd>{current.current_user?'#'+current.current_user.rank:t('غير متاح','Unavailable')}</dd></div><div><dt>{t('المشاركون المعروضون في السجل','Participants reported in history')}</dt><dd>{current.total}</dd></div><div><dt>{t('حالة الموسم','Season status')}</dt><dd>{current.finalized?t('محسوم','Settled'):t('بانتظار الحسم، القيم غير نهائية','Pending settlement, values not final')}</dd></div><div><dt>{t('القرار المحفوظ','Persisted outcome')}</dt><dd>{movement?movement==='promotion'?t('صعود','Promoted'):movement==='demotion'?t('هبوط','Demoted'):t('ثبات','Retained'):t('لم يُحسم','Not settled')}{current.finalized&&current.next_tier?' → '+tier(current.next_tier):''}</dd></div></dl></section>}
      <details className="league-history-table"><summary>{t('عرض جدول البيانات','View data table')}</summary><div><table><caption>{t('القيم الفعلية للمواسم المعروضة','Actual values for displayed seasons')}</caption><thead><tr><th>{t('الأسبوع','Week')}</th><th>XP</th><th>{t('الرتبة','Rank')}</th><th>{t('الدرجة','Tier')}</th><th>{t('الحالة','Status')}</th></tr></thead><tbody>{ordered.map(season=><tr key={season.season_id}><td><button onClick={()=>setSelected(season.season_id)}>{season.week_start}</button></td><td>{seasonValue(season,'xp')??t('غير متاح','Unavailable')}</td><td>{seasonValue(season,'rank')??t('غير متاح','Unavailable')}</td><td>{tier(season.tier)}</td><td>{season.finalized?t('محسوم','Settled'):t('معلق','Pending')}</td></tr>)}</tbody></table></div></details>
    </>}
    {more&&<button className="league-history-more" disabled={loading||error} onClick={()=>setPages(value=>value+1)}>{t('تحميل مواسم أقدم','Load older seasons')}</button>}
    <p className="league-history-caption">{t('السجل يعرض المواسم التي شاركت فيها فقط. لا تتوفر لقطات ترتيب يومية داخل كل أسبوع؛ الرسم لا يختلقها. تُحسم المواسم عند أول انضمام للأسبوع التالي.','History contains enrolled seasons only. Daily rank snapshots within each week are unavailable and are not fabricated. Seasons settle on the first enrollment next week.')}</p>
  </section>
}
