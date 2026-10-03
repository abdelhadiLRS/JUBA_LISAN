'use client'
import {Suspense,useEffect,useState} from 'react'
import {useRouter,useSearchParams} from 'next/navigation'
import {useTranslations} from 'next-intl'
import {apiFetch} from '@/lib/api'
import {mapUser} from '@/lib/mappers'
import {useAuthStore} from '@/store/auth'
import {useLanguageStore} from '@/store/language'
import {useConfigStore} from '@/store/config'
import TargetLanguageSelector from '@/components/TargetLanguageSelector'
import {DEFAULT_TARGET_LANGUAGE} from '@/lib/target-languages'
import {readProductSelection,rememberProductSelection,productQuery} from '@/lib/subscription-selection'

const GOALS=['travel','work','academic','daily','media','emigration','exams','social'] as const
function OnboardingForm(){
 const t=useTranslations('onboarding'),common=useTranslations('common'),router=useRouter(),params=useSearchParams()
 const user=useAuthStore(s=>s.user),setUser=useAuthStore(s=>s.setUser)
 const fetchLanguages=useLanguageStore(s=>s.fetchLanguages),available=useLanguageStore(s=>s.availableLanguageCodes)
 const loadConfig=useConfigStore(s=>s.load)
 const selection=readProductSelection(params),query=productQuery(selection),isNew=params.get('new')==='true'
 const [step,setStep]=useState<1|2>(1),[language,setLanguage]=useState(params.get('language')||DEFAULT_TARGET_LANGUAGE)
 const [goals,setGoals]=useState<string[]>([]),[ready,setReady]=useState(false),[loading,setLoading]=useState(false),[error,setError]=useState('')
 useEffect(()=>{let active=true;void loadConfig();void fetchLanguages().then(()=>{if(active){setReady(true);const codes=useLanguageStore.getState().availableLanguageCodes;if(codes.length&&!codes.includes(language))setLanguage(codes[0])}})
  rememberProductSelection(readProductSelection(new URLSearchParams(query)))
  return()=>{active=false}
 // Initial language preference must not reload languages after every picker change.
 // eslint-disable-next-line react-hooks/exhaustive-deps
 },[fetchLanguages,loadConfig,query])
 async function save(){
  if(loading)return;setLoading(true);setError('')
  try{const res=await apiFetch('/api/auth/me',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_language:language,learning_goals:goals})})
   if(!res.ok)throw new Error(t('saveFailed'))
   setUser(mapUser(await res.json(),user));await fetchLanguages()
   // Never charge automatically: selected products are reviewed in the common catalog.
   router.push(selection&&selection.tier!=='free'?`/settings/subscription?${query}`:'/dashboard')
  }catch(err){setError(err instanceof Error?err.message:t('saveFailed'));setLoading(false)}
 }
 return <main className="juba-auth-mobile juba-onboarding-mobile flex min-h-screen items-center justify-center bg-[var(--juba-bg)] px-4 py-10"><div className="w-full max-w-md">
  <h1 className="mb-8 text-center text-xl font-semibold">JUBA LISAN</h1><div className="rounded-[20px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-6 sm:p-8">
   <div className="mb-6 flex justify-between"><h2 className="text-lg font-semibold">{step===1?(isNew?t('newLanguageHeadline'):t('title')):t('goals.title')}</h2><span>{step}/2</span></div>
   {error&&<p role="alert" className="mb-4 text-[var(--juba-danger)]">{error}</p>}
   {step===1?<form onSubmit={e=>{e.preventDefault();if(ready&&available.length)setStep(2)}} className="space-y-6"><p>{isNew?t('newLanguageSubtitle'):t('subtitle')}</p><label className="block">{t('chooseVariant')}</label>
    {!ready?<p role="status">{common('loading')}</p>:available.length?<TargetLanguageSelector value={language} onChange={setLanguage} availableCodes={available}/>:<button type="button" onClick={()=>{setReady(false);void fetchLanguages().finally(()=>setReady(true))}}>{common('retry')}</button>}
    <button disabled={!ready||!available.length} className="juba-primary-button w-full min-h-11" type="submit">{common('next')}</button></form>:<div className="space-y-5"><p>{t('goals.subtitle')}</p><div className="grid grid-cols-2 gap-2">{GOALS.map(goal=><button key={goal} type="button" aria-pressed={goals.includes(goal)} onClick={()=>setGoals(values=>values.includes(goal)?values.filter(x=>x!==goal):[...values,goal])} className={`min-h-11 rounded-md border p-3 ${goals.includes(goal)?'bg-[var(--duo-green)] text-[var(--duo-card)]':'border-[var(--duo-line)]'}`}>{t(`goals.${goal}`)}</button>)}</div>
    <button disabled={loading} onClick={()=>void save()} className="juba-primary-button w-full min-h-11">{loading?common('saving'):t('continue')}</button><button disabled={loading} onClick={()=>void save()} className="w-full min-h-11">{t('goals.skip')}</button></div>}
  </div></div></main>
}
export default function OnboardingPage(){return <Suspense><OnboardingForm/></Suspense>}
