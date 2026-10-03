'use client'
import {Suspense,useCallback,useState} from 'react'
import {useRouter,useSearchParams} from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import {useTranslations} from 'next-intl'
import {ArrowRight,Eye,EyeOff,Globe2,Loader2,LockKeyhole,Mail,UserRound} from 'lucide-react'
import {apiFetch,readApiError} from '@/lib/api'
import {useAuthStore} from '@/store/auth'
import {readProductSelection,productQuery,rememberProductSelection} from '@/lib/subscription-selection'

const LANGUAGES=['en','es','fr','pt','de','it','pl','nl','ro','ru'] as const
const TARGET_LANGUAGES=['en-US','en-GB','de-DE','es-ES','fr-FR','it-IT','ja-JP','ko-KR','pt-PT','zh-CN'] as const
function RegisterForm(){
 const t=useTranslations('auth.register'),tLang=useTranslations('languages'),tCommon=useTranslations('common')
 const router=useRouter(),params=useSearchParams(),invite=params.get('invite'),selection=readProductSelection(params)
 const setTokens=useAuthStore(s=>s.setTokens)
 const [username,setUsername]=useState(''),[displayName,setDisplayName]=useState(''),[email,setEmail]=useState('')
 const [password,setPassword]=useState(''),[confirmPassword,setConfirmPassword]=useState('')
 const [nativeLanguage,setNativeLanguage]=useState('fr'),[targetLanguage,setTargetLanguage]=useState('en-GB')
 const [showPassword,setShowPassword]=useState(false),[showConfirmPassword,setShowConfirmPassword]=useState(false)
 const [termsAccepted,setTermsAccepted]=useState(false),[error,setError]=useState(''),[loading,setLoading]=useState(false)
 const selectionQuery=productQuery(selection)
 const handleSubmit=useCallback(async(e:React.FormEvent)=>{
  e.preventDefault();setError('')
  const cleanUsername=username.trim().replace(/\s+/g,'_').toLowerCase(),cleanEmail=email.trim().toLowerCase()
  if(!/^[a-zA-Z0-9._-]{3,50}$/.test(cleanUsername))return setError(t('invalidUsernameChars'))
  if(!cleanEmail)return setError(t('invalidEmail'))
  if(password!==confirmPassword)return setError(t('passwordMismatch'))
  if(!/^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{10,25}$/.test(password))return setError(t('invalidPassword'))
  if(!termsAccepted)return setError(t('termsRequired'))
  if(loading)return
  setLoading(true)
  try{
   const body:Record<string,string>={username:cleanUsername,email:cleanEmail,password,display_name:displayName.trim()||cleanUsername,native_language:nativeLanguage,target_language:targetLanguage}
   if(invite)body.invite_token=invite
   const res=await apiFetch('/api/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   if(!res.ok){const detail=await readApiError(res),normalized=detail.toLowerCase()
    if(normalized.includes('username already'))throw new Error(t('usernameTaken'))
    if(normalized.includes('email already'))throw new Error(t('emailTaken'))
    if(normalized.includes('registration is closed'))throw new Error(t('registrationClosed'))
    if(normalized.includes('invite'))throw new Error(t('invalidInvite'))
    throw new Error(detail)
   }
   const data=await res.json() as {access_token?:string}
   if(!data.access_token)throw new Error('Registration succeeded but no access token was returned.')
   rememberProductSelection(readProductSelection(new URLSearchParams(selectionQuery)))
   setTokens(data.access_token)
   router.replace(`/onboarding${selectionQuery?'?'+selectionQuery:''}`)
  }catch(err){setError(err instanceof Error?err.message:t('error'))}finally{setLoading(false)}
 },[username,displayName,email,password,confirmPassword,nativeLanguage,targetLanguage,termsAccepted,invite,selectionQuery,router,setTokens,t,loading])
 const inputClass='w-full rounded-2xl border border-black/[0.08] bg-[var(--juba-surface-muted)] px-4 py-3.5 text-sm outline-none focus:border-[var(--juba-primary)] focus:ring-4 focus:ring-[color-mix(in_srgb,var(--juba-primary)_18%,transparent)]'
 return <main className="juba-auth-mobile min-h-screen bg-[var(--juba-bg)] text-[var(--juba-text)]"><div className="mx-auto grid min-h-screen max-w-7xl lg:grid-cols-[.9fr_1.1fr]">
  <section className="hidden border-r border-black/[0.06] bg-[var(--juba-surface)] px-10 py-10 lg:flex lg:flex-col lg:justify-between xl:px-16">
   <div className="flex items-center gap-3"><Image src="/logo.png" alt="JUBA LISAN" width={30} height={30} priority/><span className="text-lg font-semibold">JUBA LISAN</span></div>
   <div className="max-w-xl"><div className="mb-5 inline-flex items-center gap-2 text-xs font-medium text-[var(--juba-primary-dark)]"><Globe2 size={16}/>{tCommon('tagline')}</div><h2 className="text-5xl font-semibold leading-tight">Your language journey starts with one account.</h2><p className="mt-6 text-base leading-7">Choose your languages, set your goals and let the platform adapt your practice over time.</p></div><p className="text-xs">One account · Multiple languages · Personal progress</p>
  </section><section className="flex items-center justify-center px-5 py-8 sm:px-8"><div className="w-full max-w-xl"><div className="rounded-[22px] border border-black/[0.08] bg-[var(--juba-surface)] p-6 sm:p-8">
   <h1 className="text-3xl font-semibold">{t('title')}</h1>{selection&&<p className="mt-2 text-sm">{selection.tier==='go'?'Go':selection.tier==='plus'?'Plus':'Free'} · {selection.interval}</p>}
   {invite&&<p className="my-4">{t('inviteActive')}</p>}{error&&<p role="alert" className="my-4 text-[var(--juba-danger)]">{error}</p>}
   <form onSubmit={handleSubmit} noValidate className="mt-7 space-y-5"><div className="grid gap-5 sm:grid-cols-2">
    <label><span className="mb-2 flex items-center gap-2 text-sm"><UserRound size={16}/>{t('username')}</span><input value={username} onChange={e=>setUsername(e.target.value)} required autoComplete="username" className={inputClass}/></label>
    <label><span className="mb-2 block text-sm">{t('displayName')}</span><input value={displayName} onChange={e=>setDisplayName(e.target.value)} placeholder={t('displayNamePlaceholder')} className={inputClass}/></label>
   </div><label className="block"><span className="mb-2 flex items-center gap-2 text-sm"><Mail size={16}/>{t('email')}</span><input type="email" value={email} onChange={e=>setEmail(e.target.value)} required autoComplete="email" autoCapitalize="none" autoCorrect="off" spellCheck={false} className={inputClass}/></label>
   <div className="grid gap-5 sm:grid-cols-2">{[{label:t('password'),value:password,set:setPassword,show:showPassword,toggle:()=>setShowPassword(v=>!v)},{label:t('confirmPassword'),value:confirmPassword,set:setConfirmPassword,show:showConfirmPassword,toggle:()=>setShowConfirmPassword(v=>!v)}].map(field=><label key={field.label}><span className="mb-2 flex items-center gap-2 text-sm"><LockKeyhole size={16}/>{field.label}</span><div className="relative"><input type={field.show?'text':'password'} value={field.value} onChange={e=>field.set(e.target.value)} required autoComplete="new-password" className={`${inputClass} pe-12`}/><button type="button" onClick={field.toggle} className="absolute end-2 top-2 p-2" aria-label={field.show?t('hidePassword'):t('showPassword')}>{field.show?<EyeOff size={16}/>:<Eye size={16}/>}</button></div></label>)}</div>
   <div className="grid gap-5 sm:grid-cols-2"><label><span className="mb-2 block text-sm">{t('nativeLanguage')}</span><select value={nativeLanguage} onChange={e=>setNativeLanguage(e.target.value)} className={inputClass}>{LANGUAGES.map(code=><option key={code} value={code}>{tLang(code)}</option>)}</select></label><label><span className="mb-2 block text-sm">Learning language</span><select value={targetLanguage} onChange={e=>setTargetLanguage(e.target.value)} className={inputClass}>{TARGET_LANGUAGES.map(code=><option key={code} value={code}>{code}</option>)}</select></label></div>
   <label className="flex items-start gap-3"><input type="checkbox" checked={termsAccepted} onChange={e=>setTermsAccepted(e.target.checked)} className="mt-1"/><span className="text-xs leading-5">{t('termsAccept')} <Link href="/terms?from=register" className="underline">{t('termsLink')}</Link> {t('andWord')} <Link href="/privacy?from=register" className="underline">{t('privacyLink')}</Link></span></label>
   <button disabled={loading} type="submit" className="flex w-full min-h-11 items-center justify-center gap-2 rounded-2xl bg-[var(--juba-primary)] px-4 py-3.5 text-[var(--juba-surface)]">{loading?<Loader2 size={16} className="animate-spin"/>:<ArrowRight size={16}/>} {loading?t('creatingAccount'):t('submit')}</button></form>
   <p className="mt-7 text-center text-sm">{t('hasAccount')} <Link href="/login" className="underline">{t('login')}</Link></p>
  </div></div></section></div></main>
}
export default function RegisterPage(){return <Suspense><RegisterForm/></Suspense>}
