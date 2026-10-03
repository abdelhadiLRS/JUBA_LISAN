'use client'

import Link from 'next/link'
import {useEffect,useRef,useState} from 'react'
import {useLocale} from 'next-intl'
import {apiFetch} from '@/lib/api'
import {useLanguageStore} from '@/store/language'
import {useAuthStore} from '@/store/auth'
import {subscribeToLearningProgressUpdated} from '@/lib/learning-progress'
import {leagueRisk,type LeagueRisk,type LeagueRiskInput} from '@/lib/games/league-risk'
import './league-risk-alert.css'

/** In-app alerts only: no browser permission, email or remote message is sent. */
export default function LeagueRiskAlert(){
  const arabic=useLocale().startsWith('ar')
  const language=useLanguageStore(state=>state.activeLanguage?.code)
  const switching=useLanguageStore(state=>state.isSwitching)
  const userId=useAuthStore(state=>state.user?.id)
  const [risk,setRisk]=useState<LeagueRisk|null>(null)
  const [dismissed,setDismissed]=useState<string|null>(null)
  const [checking,setChecking]=useState(false)
  const sequence=useRef(0)
  const mounted=useRef(false)
  const t=(ar:string,en:string)=>arabic?ar:en
  useEffect(()=>{
    mounted.current=true
    setRisk(null);setDismissed(null);setChecking(false)
    let controller:AbortController|null=null
    let timer:ReturnType<typeof setInterval>|null=null
    const check=async()=>{
      if(!language||switching||!userId||document.visibilityState==='hidden')return
      const request=++sequence.current
      controller?.abort();controller=new AbortController()
      setChecking(true)
      const timeout=setTimeout(()=>controllerForRequest.abort(),15000)
      const controllerForRequest=controller
      try{
        const response=await apiFetch(`/api/leagues/current?target_language=${encodeURIComponent(language)}&limit=1`,{signal:controllerForRequest.signal})
        if(!response.ok)throw new Error()
        const data=await response.json() as LeagueRiskInput
        if(mounted.current&&request===sequence.current)setRisk(leagueRisk(data))
      }catch{
        // Do not keep an old risk displayed as a current server-verified alert.
        if(mounted.current&&request===sequence.current)setRisk(null)
      }finally{
        clearTimeout(timeout)
        if(mounted.current&&request===sequence.current)setChecking(false)
      }
    }
    const visibility=()=>{
      if(document.visibilityState==='visible')void check()
      else{sequence.current++;controller?.abort();setRisk(null);setChecking(false)}
    }
    void check()
    timer=setInterval(()=>void check(),60000)
    const unsubscribe=subscribeToLearningProgressUpdated(()=>void check())
    document.addEventListener('visibilitychange',visibility)
    return()=>{mounted.current=false;sequence.current++;controller?.abort();if(timer)clearInterval(timer);unsubscribe();document.removeEventListener('visibilitychange',visibility)}
  },[language,switching,userId])
  const visible=risk&&risk.signature!==dismissed&&!checking
  return <div className="league-risk-live" role="status" aria-live="polite" aria-atomic="true">{visible&&risk&&<aside className="juba-page-shell league-risk-alert" data-risk={risk.level} dir={arabic?'rtl':'ltr'} aria-label={t('تنبيه خطر الهبوط','Demotion risk alert')}>
    <span className="league-risk-symbol" aria-hidden="true">{risk.level==='danger'?'↓':'!'}</span>
    <div><h2>{risk.level==='danger'?t('أنت حاليًا في منطقة الهبوط','You are currently in the demotion zone'):t('ترتيبك يقترب من منطقة الهبوط','Your rank is approaching the demotion zone')}</h2><p>{t('ترتيبك','Your rank')}: <strong>#{risk.rank}</strong> · {t('منطقة الهبوط تبدأ بعد الرتبة','The demotion zone starts after rank')} <strong>#{risk.cutoff}</strong>.</p>{risk.expiresSoon&&<p className="league-risk-deadline">{t('باقي 48 ساعة أو أقل لنهاية الأسبوع.','48 hours or less remain in this weekly season.')}</p>}<p className="league-risk-note">{t('تنبيه حسب الترتيب الحالي، وليس هبوطًا مؤكدًا. يمكن أن تتغير الرتب، والمتعادلون لا يُفصلون.','This is a current-rank warning, not confirmed demotion. Rankings can change; tied ranks are not split.')}</p><div className="league-risk-actions"><Link href="/games">{t('تدرّب واكسب XP','Practise and earn XP')}</Link><Link href="/leagues">{t('راجع الدوري','View league')}</Link></div></div>
    <button onClick={()=>setDismissed(risk.signature)} aria-label={t('إخفاء هذا التنبيه','Dismiss this warning')}>×</button>
  </aside>}</div>
}
