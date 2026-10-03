'use client'

import { useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { Languages, Plus, Trash2, ChevronLeft, ChevronRight } from 'lucide-react'
import { useLanguageStore, type UserLanguageInfo } from '@/store/language'
import { getLanguageByCode, TARGET_LANGUAGE_CATALOG } from '@/lib/target-languages'
import TargetLanguageSelector from '@/components/TargetLanguageSelector'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import { SettingsPageHeader } from '@/components/settings/SettingsShell'
import '../../resource-reference.css'

export default function MyLanguagesPage(){
  const t=useTranslations('languages')
  const tTarget=useTranslations('targetLanguages')
  const tSettings=useTranslations('settings')
  const tCommon=useTranslations('common')
  const locale=useLocale()
  const rtl=locale==='ar'
  const router=useRouter()
  const userLanguages=useLanguageStore(s=>s.userLanguages)
  const fetchLanguages=useLanguageStore(s=>s.fetchLanguages)
  const switchLanguage=useLanguageStore(s=>s.switchLanguage)
  const addLanguage=useLanguageStore(s=>s.addLanguage)
  const removeLanguage=useLanguageStore(s=>s.removeLanguage)
  const availableLanguageCodes=useLanguageStore(s=>s.availableLanguageCodes)
  const [addOpen,setAddOpen]=useState(false)
  const [deleteTarget,setDeleteTarget]=useState<UserLanguageInfo|null>(null)
  const [addingCode,setAddingCode]=useState('')
  const [adding,setAdding]=useState(false)
  const [switchingCode,setSwitchingCode]=useState<string|null>(null)
  const [toast,setToast]=useState('')
  const [error,setError]=useState('')
  const [loading,setLoading]=useState(true)
  const load=useCallback(async()=>{
    setLoading(true);setError('')
    try{await fetchLanguages()}catch{setError(tCommon('error'))}finally{setLoading(false)}
  },[fetchLanguages,tCommon])
  useEffect(()=>{void load()},[load])
  useEffect(()=>{if(!toast)return;const timer=window.setTimeout(()=>setToast(''),2500);return ()=>window.clearTimeout(timer)},[toast])
  async function handleSwitch(info:UserLanguageInfo){
    if(info.is_active||switchingCode)return
    setSwitchingCode(info.target_language);setError('')
    try{const ok=await switchLanguage(info.target_language);if(ok){setToast(t('switched',{language:tTarget(info.target_language),level:info.plan?.cefr_level??''}));router.refresh()}else setError(tCommon('error'))}catch{setError(tCommon('error'))}finally{setSwitchingCode(null)}
  }
  async function handleDelete(){
    if(!deleteTarget)return
    try{const ok=await removeLanguage(deleteTarget.target_language);if(!ok)setError(t('deleteError',{language:tTarget(deleteTarget.target_language)}))}catch{setError(t('deleteError',{language:tTarget(deleteTarget.target_language)}))}finally{setDeleteTarget(null)}
  }
  async function handleAdd(){
    if(!addingCode||adding)return
    setAdding(true);setError('')
    try{const ok=await addLanguage(addingCode);if(!ok){setError(tCommon('error'));return}setAddOpen(false);setAddingCode('');router.push('/assessment')}catch{setError(tCommon('error'))}finally{setAdding(false)}
  }
  const addedCodes=userLanguages.map(item=>item.target_language)
  const unusedCodes=TARGET_LANGUAGE_CATALOG.filter(language=>availableLanguageCodes.includes(language.code)&&!addedCodes.includes(language.code)).map(language=>language.code)
  const hasMultiple=userLanguages.length>1
  const Back=rtl?ChevronRight:ChevronLeft
  const Forward=rtl?ChevronLeft:ChevronRight
  return <div className="juba-page-shell reference-resource-page reference-language-settings" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-language-title{display:flex;align-items:center;gap:16px;flex-wrap:wrap;}
      .juba-app-shell .reference-language-title>svg{color:var(--juba-green);flex:none;}
      .juba-app-shell .reference-language-title>header{flex:1;min-width:0;}
      .juba-app-shell .reference-language-title>button{padding-inline:12px;}
      .juba-app-shell .reference-language-notice{padding:12px 16px;border:1px solid var(--juba-border);border-radius:6px;font-size:13px;color:var(--juba-green-dark);background:var(--juba-green-soft);}
      .juba-app-shell .reference-language-notice[data-error="true"]{color:var(--duo-red);background:var(--juba-card);border-color:var(--duo-red);}
      .juba-app-shell .reference-language-notice button{margin-inline-start:12px;text-decoration:underline;min-height:32px;}
      .juba-app-shell .reference-language-add{display:flex;flex-direction:column;gap:16px;padding:16px;border:1px solid var(--juba-border);border-radius:6px;}
      .juba-app-shell .reference-language-add h2{font-size:14px;font-weight:650;margin:0;}
      .juba-app-shell .reference-language-add-actions{display:flex;justify-content:flex-end;gap:8px;}
      .juba-app-shell .reference-language-add-actions button{padding-inline:16px;}
      .juba-app-shell .reference-language-row{padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-language-row:last-child{border:0;}
      .juba-app-shell .reference-language-row[data-active="true"]{background:var(--juba-green-soft);}
      .juba-app-shell .reference-language-row-head{display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
      .juba-app-shell .reference-language-row-head img{flex:none;}
      .juba-app-shell .reference-language-row-head h2{font-size:15px;font-weight:650;margin:0;flex:1;min-width:0;}
      .juba-app-shell .reference-language-stats{display:flex;align-items:center;gap:12px 20px;flex-wrap:wrap;margin:16px 0;font-size:12px;color:var(--juba-muted);}
      .juba-app-shell .reference-language-stats>div{display:flex;align-items:center;gap:6px;}
      .juba-app-shell .reference-language-stats dd{margin:0;color:var(--juba-ink);font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-language-track{height:8px;border-radius:3px;overflow:hidden;background:var(--juba-soft);max-width:520px;margin-block-end:16px;}
      .juba-app-shell .reference-language-track>span{display:block;height:100%;background:var(--juba-yellow);}
      .juba-app-shell .reference-language-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
      .juba-app-shell .reference-language-actions :is(a,button){padding-inline:12px;}
      .juba-app-shell .reference-language-remove{display:flex;align-items:center;gap:8px;min-height:40px;border:1px solid var(--juba-border);border-radius:6px;background:transparent;color:var(--juba-muted);font-size:13px;}
      .juba-app-shell .reference-language-remove:hover{color:var(--duo-red);border-color:var(--duo-red);}
      @media(max-width:640px){.juba-app-shell .reference-language-title>svg{width:32px;height:32px;}.juba-app-shell .reference-language-remove{min-height:44px;}}
    `}</style>
    <nav className="reference-resource-breadcrumb" aria-label={t('myLanguages')}><Link href="/settings"><Back size={14}/>{tSettings('title')}</Link><span aria-hidden="true">/</span><span>{t('myLanguages')}</span></nav>
    <div className="reference-language-title"><Languages size={40} aria-hidden="true"/><SettingsPageHeader eyebrow={tSettings('sectionLanguages')} title={t('myLanguages')}/>{unusedCodes.length>0&&<button className="juba-primary-button" onClick={()=>setAddOpen(value=>!value)} aria-expanded={addOpen} aria-controls="add-language-form"><Plus size={16}/>{t('addLanguage')}</button>}</div>
    {toast&&<p className="reference-language-notice" role="status">{toast}</p>}
    {error&&<div className="reference-language-notice" data-error="true" role="alert">{error}<button onClick={()=>void load()} disabled={loading}>{tCommon('retry')}</button></div>}
    {addOpen&&<section className="reference-language-add" id="add-language-form" aria-labelledby="add-language-title"><h2 id="add-language-title">{t('selectLanguage')}</h2><TargetLanguageSelector value={addingCode} onChange={setAddingCode} availableCodes={unusedCodes}/><div className="reference-language-add-actions"><button className="juba-secondary-button" onClick={()=>setAddOpen(false)} disabled={adding}>{tCommon('cancel')}</button><button className="juba-primary-button" onClick={()=>void handleAdd()} disabled={!addingCode||adding}>{adding?'…':t('addLanguage')}</button></div></section>}
    {loading?<PageLoading/>:!userLanguages.length?<section className="reference-resource-panel reference-resource-state"><Languages size={28}/><p>{t('noLanguages')}</p></section>:<section className="reference-resource-panel">{[...userLanguages].sort((a,b)=>tTarget(a.target_language).localeCompare(tTarget(b.target_language))).map(info=>{
      const language=getLanguageByCode(info.target_language)
      const plan=info.plan
      const progress=info.progress
      const pct=Math.max(0,Math.min(100,plan?.completion_pct??0))
      return <article className="reference-language-row" data-active={info.is_active} key={info.target_language}><header className="reference-language-row-head">{language&&<Image src={language.flagPath} alt="" width={28} height={20}/>}<h2>{tTarget(info.target_language)}</h2>{info.is_active?<span className="juba-badge">{t('activeLanguage')}</span>:plan?.cefr_level?<span className="juba-badge">{plan.cefr_level}</span>:null}</header>{plan&&<><dl className="reference-language-stats"><div><dt>{t('levelLabel')}</dt><dd>{plan.cefr_level??'…'}</dd></div><div><dt>{t('progressLabel')}</dt><dd>{plan.completion_pct}%</dd></div>{progress&&<><div><dt>{t('xpLabel')}</dt><dd>{progress.total_xp.toLocaleString(locale)}</dd></div><div><dt>{t('streakLabel')}</dt><dd>{progress.current_streak}</dd></div><div><dt>{t('lessonsLabel')}</dt><dd>{progress.lessons_completed}</dd></div></>}</dl><div className="reference-language-track" role="progressbar" aria-label={tTarget(info.target_language)+' '+t('progressLabel')} aria-valuemin={0} aria-valuemax={100} aria-valuenow={pct}><span style={{width:pct+'%'}}/></div></>}<div className="reference-language-actions">{info.is_active?<Link className="juba-secondary-button" href="/plan">{t('viewDetails')}<Forward size={16}/></Link>:<><button className="juba-secondary-button" onClick={()=>void handleSwitch(info)} disabled={switchingCode!==null}>{switchingCode===info.target_language?'…':t('switchTo')}</button>{hasMultiple&&<button className="reference-language-remove" onClick={()=>setDeleteTarget(info)}><Trash2 size={16}/>{t('removeLanguage')}</button>}</>}</div></article>
    })}</section>}
    <ConfirmDialog open={deleteTarget!==null} title={t('removeConfirmTitle',{language:deleteTarget?tTarget(deleteTarget.target_language):''})} message={t('removeConfirmMessage')} confirmLabel={t('removeConfirmButton')} onConfirm={handleDelete} onCancel={()=>setDeleteTarget(null)}/>
  </div>
}
