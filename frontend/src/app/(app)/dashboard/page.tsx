'use client'

import { useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { BookOpen, Check, Flame, Library, Play, Trophy, UserRound, Sparkles, Users, Settings, CircleHelp, MessageCircle, RefreshCw } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { isSubscribed, needsPaymentRecovery, isFreemiumTrialActive, useAuthStore } from '@/store/auth'
import { useProgressStore } from '@/store/progress'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'
import OnboardingTour from '@/components/tour/OnboardingTour'
import WhatsNew from '@/components/whats-new/WhatsNew'
import { PageLoading } from '@/components/ui/page-loading'
import { SubscriptionPlanButtons } from '@/components/billing/SubscriptionPlanButtons'
import { subscribeToLearningProgressUpdated } from '@/lib/learning-progress'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'
import './dashboard-reference.css'

interface TodayLessonItem { id:number|null;title:string;lesson_type:string;week:number;day:number;objectives:string[];estimated_minutes:number;is_completed:boolean }
interface CompletionState { state:'in_progress'|'ready'|'taken';score:number|null;recommendation:string|null;next_level:string|null }
interface FriendItem { id:number;username:string;display_name:string;avatar?:string|null;target_language?:string }
interface HistoryEntry { date:string;xp_earned:number;lessons_completed:number;exercises_correct:number;exercises_total:number;streak_day:number;skills:Record<string,number> }
type HistoryRange='week'|'month'|'all'

function ProgressTrack({value,label}:{value:number;label:string}) {
  const safe=Math.max(0,Math.min(100,Number.isFinite(value)?value:0))
  return <div className="reference-dashboard-track" role="progressbar" aria-label={label} aria-valuemin={0} aria-valuemax={100} aria-valuenow={safe}><span style={{width:safe+'%'}}/></div>
}

export default function DashboardPage() {
  const locale=useLocale()
  const rtl=locale==='ar'
  const t=useTranslations('dashboard')
  const tBilling=useTranslations('billing')
  const tNav=useTranslations('nav')
  const tTarget=useTranslations('targetLanguages')
  const tError=useTranslations('error')
  const user=useAuthStore(s=>s.user)
  const accessToken=useAuthStore(s=>s.accessToken)
  const stripeEnabled=useConfigStore(s=>s.stripeEnabled)
  const freemiumTrialActive=isFreemiumTrialActive(user,stripeEnabled)
  const [freemiumTrialDaysLeft,setFreemiumTrialDaysLeft]=useState(0)
  const {streak,xp,todayLessons,completedToday,setProgress,setTodayLessons}=useProgressStore()
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const [loading,setLoading]=useState(true)
  const [loadError,setLoadError]=useState(false)
  const [hasPlan,setHasPlan]=useState(false)
  const [completion,setCompletion]=useState<CompletionState|null>(null)
  const [cefrLevel,setCefrLevel]=useState<string|null>(null)
  const [progressDay,setProgressDay]=useState(0)
  const [totalDays,setTotalDays]=useState(0)
  const [accuracy,setAccuracy]=useState(0)
  const [vocabularyLevel,setVocabularyLevel]=useState<string|null>(null)
  const [vocabularyMastered,setVocabularyMastered]=useState(0)
  const [vocabularyTotal,setVocabularyTotal]=useState(0)
  const [vocabularyProgress,setVocabularyProgress]=useState(0)
  const [portalLoading,setPortalLoading]=useState(false)
  const [portalError,setPortalError]=useState<string|null>(null)
  const [historyRange,setHistoryRange]=useState<HistoryRange>('week')
  const [historyEntries,setHistoryEntries]=useState<HistoryEntry[]>([])
  const [refreshing,setRefreshing]=useState(false)
  const [friends,setFriends]=useState<FriendItem[]>([])

  useEffect(()=>{
    if(freemiumTrialActive&&user?.freemium_trial_ends_at) setFreemiumTrialDaysLeft(Math.max(1,Math.ceil((new Date(user.freemium_trial_ends_at).getTime()-Date.now())/86400000)))
  },[freemiumTrialActive,user?.freemium_trial_ends_at])

  const loadData=useCallback(async()=>{
    try {
      const [progRes,planRes,historyRes,friendsRes]=await Promise.all([
        apiFetch('/api/progress/summary'),apiFetch('/api/study-plan/today'),apiFetch('/api/progress/history?range='+historyRange),apiFetch('/api/social/friends'),
      ])
      if(progRes.ok) {
        const prog=await progRes.json()
        setProgress({streak:prog.current_streak??0,xp:prog.total_xp??0,skills:prog.skills??{}})
        setAccuracy(prog.accuracy??0)
        setVocabularyLevel(prog.vocabulary_level??null)
        setVocabularyMastered(prog.vocabulary_mastered??0)
        setVocabularyTotal(prog.vocabulary_total??0)
        setVocabularyProgress(prog.vocabulary_progress??0)
      } else {
        setProgress({streak:0,xp:0,skills:{}})
        setAccuracy(0);setVocabularyLevel(null);setVocabularyMastered(0);setVocabularyTotal(0);setVocabularyProgress(0)
      }
      if(historyRes.ok) {const history=await historyRes.json();setHistoryEntries(Array.isArray(history.entries)?history.entries:[])} else setHistoryEntries([])
      if(friendsRes.ok) {const socialFriends=await friendsRes.json();setFriends(Array.isArray(socialFriends)?socialFriends.slice(0,6):[])} else setFriends([])
      if(planRes.ok) {
        const plan=await planRes.json()
        setCefrLevel(plan.cefr_level??null);setCompletion(plan.completion??null);setProgressDay(plan.progress_day??0);setTotalDays(plan.total_days??0)
        setTodayLessons(plan.lessons.map((lesson:TodayLessonItem)=>({id:lesson.id,title:lesson.title,lessonType:lesson.lesson_type,week:lesson.week,day:lesson.day,objectives:lesson.objectives||[],estimatedMinutes:lesson.estimated_minutes||25,isCompleted:lesson.is_completed})))
        setHasPlan(true)
      } else {setCefrLevel(null);setCompletion(null);setProgressDay(0);setTotalDays(0);setTodayLessons([]);setHasPlan(false)}
    } catch {setLoadError(true)} finally {setLoading(false)}
  },[setProgress,setTodayLessons,activeLanguage?.code,historyRange])

  useEffect(()=>{if(user&&accessToken) void loadData()},[loadData,user,accessToken])
  const refreshDashboardData=useCallback(async()=>{
    if(refreshing)return
    setRefreshing(true);setLoadError(false)
    try {await loadData()} finally {setRefreshing(false)}
  },[loadData,refreshing])
  useEffect(()=>{
    if(!user||!accessToken)return
    const handleVisibility=()=>{if(document.visibilityState==='visible') void refreshDashboardData()}
    const handleFocus=()=>{void refreshDashboardData()}
    window.addEventListener('focus',handleFocus);document.addEventListener('visibilitychange',handleVisibility)
    return ()=>{window.removeEventListener('focus',handleFocus);document.removeEventListener('visibilitychange',handleVisibility)}
  },[user,accessToken,refreshDashboardData])
  useEffect(()=>{
    if(!user||!accessToken)return
    return subscribeToLearningProgressUpdated(()=>{void refreshDashboardData()})
  },[user,accessToken,refreshDashboardData])

  async function handleManageSubscription() {
    setPortalLoading(true);setPortalError(null)
    try {
      const res=await apiFetch('/api/billing/portal',{method:'POST'})
      if(!res.ok)throw new Error(tBilling('portalError'))
      const {url}=await res.json();window.location.assign(url)
    } catch(err) {setPortalError(err instanceof Error?err.message:tBilling('portalError'));setPortalLoading(false)}
  }

  if(loading)return <PageLoading label={t('loadingProgress')} minHeight="min-h-screen"/>
  const completedLessonCount=todayLessons.filter(lesson=>(lesson.id&&completedToday.includes(lesson.id))||lesson.isCompleted).length
  const nextLesson=todayLessons.find(lesson=>lesson.id&&!completedToday.includes(lesson.id)&&!lesson.isCompleted)
  const positionComplete=completion?.state==='ready'||completion?.state==='taken'
  const planCompletion=hasPlan&&totalDays>0?positionComplete?100:Math.min(100,Math.round(progressDay/totalDays*100)):0
  const currentDay=positionComplete?totalDays:Math.min(progressDay+1,totalDays)
  const dailyProgress=todayLessons.length?Math.min(100,Math.round(completedLessonCount/todayLessons.length*100)):0
  const vocabularyPct=Math.max(0,Math.min(100,Math.round(vocabularyProgress*100)))
  const showPremiumBanner=stripeEnabled&&!isSubscribed(user,stripeEnabled)
  const paymentRecovery=needsPaymentRecovery(user)
  const chartEntries=historyEntries.slice(historyRange==='week'?-7:historyRange==='month'?-31:-60)
  const chartMax=Math.max(1,...chartEntries.map(entry=>entry.xp_earned))
  const name=user?.displayName||user?.username||''

  return <>
    <OnboardingTour/><WhatsNew/>
    <div className="juba-page-shell reference-dashboard" dir={rtl?'rtl':'ltr'} data-dashboard-version="reference-v3">
      {loadError&&<div className="reference-dashboard-alert" role="alert"><span>{tError('body')}</span><button className="juba-secondary-button" disabled={refreshing} onClick={()=>void refreshDashboardData()}>{tError('retry')}</button></div>}
      <div className="reference-dashboard-layout">
        <div className="reference-dashboard-main">
          <header className="reference-dashboard-welcome"><BookOpen size={48} aria-hidden="true"/><div><h1>{rtl?'مرحبًا بعودتك، ':'Welcome back, '}<strong>{name}!</strong></h1><p><strong>{dailyProgress}%</strong> {t('todayGoal')}</p></div><button className="reference-dashboard-refresh" aria-label={rtl?'تحديث لوحة التحكم':'Refresh dashboard'} disabled={refreshing} onClick={()=>void refreshDashboardData()}><RefreshCw size={18}/></button></header>
          <div className="reference-dashboard-overview">
            <section className="reference-dashboard-card"><div className="reference-dashboard-card-head"><h2>{tNav('progress')}</h2><Link href="/plan">{t('goToMyPlan')}</Link></div><div className="reference-dashboard-progress-row"><span className="reference-dashboard-tile"><BookOpen size={23}/></span><div><span>{t('nextStep')} · {cefrLevel||'A1'}</span><ProgressTrack value={planCompletion} label={tNav('progress')}/></div><small>{currentDay}/{totalDays}</small></div><div className="reference-dashboard-progress-row"><span className="reference-dashboard-tile green"><Library size={23}/></span><div><span>{t('vocabularyProgress',{level:vocabularyLevel||'A1'})}</span><ProgressTrack value={vocabularyPct} label={tNav('vocabulary')}/></div><small>{vocabularyMastered}/{vocabularyTotal}</small></div><div className="reference-dashboard-progress-row"><span className="reference-dashboard-tile purple"><Check size={23}/></span><div><span>{t('completedToday',{completed:completedLessonCount,total:todayLessons.length})}</span><ProgressTrack value={dailyProgress} label={t('todayGoal')}/></div><small>{completedLessonCount}/{todayLessons.length}</small></div></section>
            <section className="reference-dashboard-card"><div className="reference-dashboard-card-head"><h2>{t('todayGoal')}</h2><Link href="/settings">{tNav('settings')}</Link></div><div className="reference-dashboard-progress-row"><span className="reference-dashboard-tile"><Flame size={23}/></span><div><span>{t('today')}</span><ProgressTrack value={dailyProgress} label={t('todayGoal')}/></div><small>{dailyProgress}%</small></div><dl className="reference-dashboard-daily"><div><dt>{t('xp')}</dt><dd>{xp}</dd></div><div><dt>{t('streak')}</dt><dd>{streak}</dd></div><div><dt>{t('accuracy')}</dt><dd>{accuracy}%</dd></div></dl></section>
          </div>
          <section className="reference-dashboard-card reference-dashboard-history"><div className="reference-dashboard-card-head"><h2>{t('recentPerformance')}</h2><div className="reference-dashboard-ranges" role="group" aria-label={t('recentPerformance')}>{(['week','month','all'] as const).map(range=><button key={range} aria-pressed={historyRange===range} onClick={()=>setHistoryRange(range)}>{rtl?({week:'أسبوع',month:'شهر',all:'الكل'})[range]:({week:'Week',month:'Month',all:'All'})[range]}</button>)}</div></div>{chartEntries.length?<><div className="reference-dashboard-chart" aria-label={t('xp')}>{chartEntries.map(entry=><div key={entry.date} className="reference-dashboard-bar" title={`${entry.date}: ${entry.xp_earned} XP`}><div><span style={{height:(entry.xp_earned/chartMax*100)+'%'}}/></div><small>{new Date(entry.date+'T00:00:00').toLocaleDateString(locale,{month:'short',day:'numeric'})}</small></div>)}</div><details className="reference-dashboard-chart-data"><summary>{rtl?'عرض بيانات الرسم':'View chart data'}</summary><div className="reference-dashboard-table"><table><thead><tr><th>{t('today')}</th><th>{t('xp')}</th><th>{tNav('courses')}</th></tr></thead><tbody>{chartEntries.map(entry=><tr key={entry.date}><td>{entry.date}</td><td>{entry.xp_earned}</td><td>{entry.lessons_completed}</td></tr>)}</tbody></table></div></details></>:<div className="reference-dashboard-empty"><ChartEmpty/><p>{rtl?'لا يوجد نشاط مسجل لهذه الفترة.':'No recorded activity for this period.'}</p><Link className="juba-secondary-button" href="/plan">{t('goToMyPlan')}</Link></div>}</section>
          <section className="reference-dashboard-card"><div className="reference-dashboard-card-head"><h2>{t('nextStep')}</h2><Link href="/plan">{t('goToMyPlan')}</Link></div><div className="reference-dashboard-lessons">{todayLessons.length?todayLessons.map((lesson,index)=>{
            const done=Boolean((lesson.id&&completedToday.includes(lesson.id))||lesson.isCompleted)
            const current=!done&&(!nextLesson||lesson.id===nextLesson.id)
            return <div className="reference-dashboard-lesson" key={lesson.id??lesson.title} data-current={current} aria-current={current?'step':undefined}><span className="reference-dashboard-node" data-done={done}>{done?<Check size={16}/>:current?<Play size={14}/>:index+1}</span><div><small>{lesson.lessonType} · {lesson.estimatedMinutes} {rtl?'دقيقة':'min'}</small><strong>{lesson.title}</strong><p>{lesson.objectives?.[0]||''}</p></div>{current&&lesson.id?<Link className="juba-primary-button" href={'/lesson/'+lesson.id}>{t('startLesson')}</Link>:done?<span className="juba-badge"><Check size={14}/></span>:null}</div>
          }):<div className="reference-dashboard-empty"><BookOpen size={24}/><p>{t('startWithAssessment')}</p><Link className="juba-primary-button" href="/plan">{t('goToMyPlan')}</Link></div>}</div></section>
        </div>
        <aside className="reference-dashboard-rail" aria-label={rtl?'ملخص التعلّم':'Learning summary'}>
          <section className="reference-dashboard-profile"><span className="reference-dashboard-avatar">{user?.avatar?<AuthAvatarImage avatar={user.avatar} alt="" width={96} height={96} className="h-full w-full object-cover"/>:<UserRound size={40}/>}</span><strong>{name}</strong><p>{cefrLevel||'A1'} · {activeLanguage?tTarget(activeLanguage.code):''}</p><dl className="reference-dashboard-profile-stats"><div><dt>XP</dt><dd>{xp}</dd></div><div><dt><Flame size={16}/><span className="sr-only">{t('streak')}</span></dt><dd>{streak}</dd></div><div><dt><Check size={16}/><span className="sr-only">{t('today')}</span></dt><dd>{completedLessonCount}</dd></div></dl></section>
          <nav className="reference-dashboard-utilities" aria-label={rtl?'أدوات الحساب':'Account utilities'}><Link href="/friends" aria-label={tNav('friends')}><Users size={17}/></Link><Link href="/chat" aria-label={tNav('tutor')}><MessageCircle size={17}/></Link><Link href="/faq" aria-label={tNav('faq')}><CircleHelp size={17}/></Link><Link href="/settings" aria-label={tNav('settings')}><Settings size={17}/></Link></nav>
          <section className="reference-dashboard-card"><div className="reference-dashboard-card-head"><h2>{t('achievements')}</h2><Link href="/progress">{tNav('progress')}</Link></div><div className="reference-dashboard-achievement"><span className="reference-dashboard-achievement-icon"><Trophy size={28}/><small>{cefrLevel||'A1'}</small></span><div><strong>{nextLesson?.title||t('startWithAssessment')}</strong><p>{currentDay}/{totalDays} · {planCompletion}%</p><ProgressTrack value={planCompletion} label={t('achievements')}/></div></div></section>
          <section className="reference-dashboard-card"><div className="reference-dashboard-card-head"><h2>{t('friends')}</h2><Link href="/friends">{tNav('friends')}</Link></div>{friends.length?<div className="reference-dashboard-friends">{friends.map(friend=><Link href={'/friends/chat/'+friend.id} key={friend.id}><span className="reference-dashboard-friend-avatar">{friend.avatar?<AuthAvatarImage avatar={friend.avatar} alt="" width={32} height={32} className="h-full w-full object-cover"/>:(friend.display_name||friend.username).slice(0,1).toUpperCase()}</span><span><strong>{friend.display_name||friend.username}</strong><small>{friend.target_language||''}</small></span><MessageCircle size={14}/></Link>)}</div>:<div className="reference-dashboard-empty compact"><Users size={22}/><Link href="/friends">{t('friends')}</Link></div>}</section>
          <section className="reference-dashboard-card"><div className="reference-dashboard-card-head"><h2>{tNav('vocabulary')}</h2><Link href="/vocabulary">{tNav('vocabulary')}</Link></div><p className="reference-dashboard-vocabulary">{vocabularyMastered.toLocaleString(locale)} / {vocabularyTotal.toLocaleString(locale)}</p><ProgressTrack value={vocabularyPct} label={tNav('vocabulary')}/><p className="reference-dashboard-caption">{vocabularyLevel||'A1'} · {vocabularyPct}%</p></section>
          {showPremiumBanner&&<section className="reference-dashboard-card reference-dashboard-premium"><Sparkles size={22}/><h2>{tBilling('upgrade')}</h2><p>{freemiumTrialActive?`${freemiumTrialDaysLeft} ${rtl?'أيام':'days'}`:tBilling('description')}</p>{paymentRecovery?<button className="juba-primary-button" onClick={handleManageSubscription} disabled={portalLoading}>{portalLoading?'…':tBilling('manageSubscription')}</button>:<SubscriptionPlanButtons/>}{portalError&&<p role="alert">{portalError}</p>}</section>}
        </aside>
      </div>
    </div>
  </>
}
function ChartEmpty(){return <Library size={24} aria-hidden="true"/>}
