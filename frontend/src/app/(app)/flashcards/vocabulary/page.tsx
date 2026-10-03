'use client'

import { useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { Library, Search, Trash2, ChevronLeft, ChevronRight } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { PageLoading } from '@/components/ui/page-loading'
import { Pagination } from '@/components/ui/pagination'
import '../../resource-reference.css'

interface VocabItem{id:number;word:string;definition:string;example_sentence:string;translation:string}
interface GuestVocabItem{id:string;sourceText:string;translation:string;sourceLanguage:string;targetLanguage:string;createdAt:string;mastery:number;nextReviewAt:string}
const LIMIT=10
const GUEST_VOCABULARY_KEY='juba_lisan_saved_vocabulary'
export default function VocabularyPage(){
  const t=useTranslations('flashcards')
  const tCommon=useTranslations('common')
  const rtl=useLocale()==='ar'
  const [items,setItems]=useState<VocabItem[]>([])
  const [guestItems,setGuestItems]=useState<GuestVocabItem[]>([])
  const [total,setTotal]=useState(0)
  const [page,setPage]=useState(1)
  const [pages,setPages]=useState(1)
  const [search,setSearch]=useState('')
  const [debouncedSearch,setDebouncedSearch]=useState('')
  const [loading,setLoading]=useState(true)
  const [deletingId,setDeletingId]=useState<number|null>(null)
  const [loadError,setLoadError]=useState(false)
  const [actionError,setActionError]=useState(false)
  useEffect(()=>{try{const stored=JSON.parse(localStorage.getItem(GUEST_VOCABULARY_KEY)||'[]');setGuestItems(Array.isArray(stored)?stored:[])}catch{setGuestItems([])}},[])
  useEffect(()=>{const timer=setTimeout(()=>{setDebouncedSearch(search);setPage(1)},300);return ()=>clearTimeout(timer)},[search])
  const loadPage=useCallback(async(p:number,q:string)=>{
    setLoading(true);setLoadError(false)
    try{
      const params=new URLSearchParams({page:String(p),limit:String(LIMIT),search:q})
      const res=await apiFetch(`/api/flashcards/vocabulary?${params}`)
      if(!res.ok)throw new Error()
      const data=await res.json();setItems(data.items);setTotal(data.total);setPage(data.page);setPages(data.pages)
    }catch{setLoadError(true)}finally{setLoading(false)}
  },[])
  useEffect(()=>{void loadPage(page,debouncedSearch)},[page,debouncedSearch,loadPage])
  async function deleteItem(id:number){
    setDeletingId(id);setActionError(false)
    try{const res=await apiFetch(`/api/flashcards/${id}`,{method:'DELETE'});if(!res.ok)throw new Error();await loadPage(page,debouncedSearch)}catch{setActionError(true)}finally{setDeletingId(null)}
  }
  function deleteGuestItem(id:string){
    const next=guestItems.filter(item=>item.id!==id)
    try{localStorage.setItem(GUEST_VOCABULARY_KEY,JSON.stringify(next));setGuestItems(next);setActionError(false)}catch{setActionError(true)}
  }
  const Back=rtl?ChevronRight:ChevronLeft
  return <div className="juba-page-shell reference-resource-page reference-flash-vocabulary" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-flash-vocab-header{display:flex;align-items:center;gap:16px;flex-wrap:wrap;}
      .juba-app-shell .reference-flash-vocab-header>.reference-resource-heading{flex:1;}
      .juba-app-shell .reference-flash-vocab-header>a{padding-inline:12px;}
      .juba-app-shell .reference-flash-vocab-search{display:flex;align-items:center;gap:12px;padding:16px;color:var(--juba-muted);}
      .juba-app-shell .reference-flash-vocab-search input{width:100%;min-width:0;flex:1;padding:8px 12px;}
      .juba-app-shell .reference-flash-vocab-row{display:flex;align-items:flex-start;gap:16px;padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-flash-vocab-row:last-child{border:0;}
      .juba-app-shell .reference-flash-vocab-row>div{flex:1;min-width:0;}
      .juba-app-shell .reference-flash-vocab-word{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
      .juba-app-shell .reference-flash-vocab-word strong{font-size:15px;font-weight:650;overflow-wrap:anywhere;}
      .juba-app-shell .reference-flash-vocab-word>span{font-size:10px;color:var(--juba-muted);padding:4px 6px;background:var(--juba-soft);border-radius:4px;}
      .juba-app-shell .reference-flash-vocab-row p{font-size:14px;line-height:1.6;color:var(--juba-muted);margin:6px 0 0;overflow-wrap:anywhere;}
      .juba-app-shell .reference-flash-vocab-remove{display:grid;place-items:center;flex:none;width:36px;height:36px;border:1px solid var(--juba-border);border-radius:5px;background:transparent;color:var(--juba-muted);}
      .juba-app-shell .reference-flash-vocab-remove:hover{color:var(--duo-red);border-color:var(--duo-red);}
      .juba-app-shell .reference-flash-vocab-guest-info{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-flash-vocab-guest-info p{flex:1;font-size:13px;line-height:1.6;color:var(--juba-muted);margin:0;}
      .juba-app-shell .reference-flash-vocab-guest-info a{padding-inline:12px;}
      .juba-app-shell .reference-flash-vocab-error{padding:12px 16px;border:1px solid var(--duo-red);border-radius:6px;font-size:13px;color:var(--duo-red);}
      @media(max-width:640px){.juba-app-shell .reference-flash-vocab-remove{width:44px;height:44px;}.juba-app-shell .reference-flash-vocab-header>a{width:100%;}}
    `}</style>
    <div className="reference-flash-vocab-header"><header className="reference-resource-heading"><Library size={40} aria-hidden="true"/><div><h1>{t('myVocabulary')}</h1>{!loading&&<p>{total}</p>}</div></header><Link href="/flashcards" className="juba-secondary-button"><Back size={16}/>{t('backToFlashcards')}</Link></div>
    {actionError&&<p className="reference-flash-vocab-error" role="alert">{tCommon('error')}</p>}
    {guestItems.length>0&&<section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{rtl?'محفوظ من المترجم':'Saved from Instant Translator'}</h2><span>{guestItems.length}</span></header><div className="reference-flash-vocab-guest-info"><p>{rtl?'هذه الكلمات محفوظة في هذا المتصفح.':'These items are saved in this browser.'}</p><Link className="juba-secondary-button" href="/register">{rtl?'إنشاء حساب':'Create account'}</Link></div>{guestItems.map(item=><article className="reference-flash-vocab-row" key={item.id}><div><div className="reference-flash-vocab-word"><strong dir="auto">{item.sourceText}</strong><span>{item.sourceLanguage}</span></div><p dir="auto">{item.translation}</p><p className="reference-resource-caption">{rtl?'الإتقان':'Mastery'} {item.mastery}%</p></div><button className="reference-flash-vocab-remove" onClick={()=>deleteGuestItem(item.id)} aria-label={(rtl?'إزالة':'Remove')+': '+item.sourceText}><Trash2 size={16}/></button></article>)}</section>}
    <section className="reference-resource-panel"><label className="reference-flash-vocab-search"><Search size={18} aria-hidden="true"/><input className="juba-input" type="search" value={search} onChange={event=>setSearch(event.target.value)} placeholder={t('vocabularySearch')} aria-label={t('vocabularySearch')}/></label></section>
    <section className="reference-resource-panel" aria-busy={loading}>{loading?<PageLoading fullScreen={false} className="block p-5"/>:loadError?<div className="reference-resource-state" role="alert"><p>{tCommon('error')}</p><button className="juba-secondary-button" onClick={()=>void loadPage(page,debouncedSearch)}>{tCommon('retry')}</button></div>:!items.length?<div className="reference-resource-state"><Library size={28}/><p>{debouncedSearch?t('myVocabularyNoResults'):t('myVocabularyEmpty')}</p></div>:items.map(item=><article className="reference-flash-vocab-row" key={item.id}><div><div className="reference-flash-vocab-word"><strong dir="auto">{item.word}</strong><AudioPlayer text={item.word} size="sm"/></div><p dir="auto">{item.definition}</p><p dir="auto">{item.translation}</p></div><button className="reference-flash-vocab-remove" onClick={()=>void deleteItem(item.id)} disabled={deletingId===item.id} aria-label={(rtl?'حذف':'Delete')+': '+item.word}>{deletingId===item.id?'…':<Trash2 size={16}/>}</button></article>)}</section>
    <Pagination page={page-1} totalPages={pages} loading={loading} onPageChange={value=>setPage(value+1)} prevLabel={t('vocabularyPrev')} nextLabel={t('vocabularyNext')} pageInfo={t('vocabularyPageInfo',{page,pages})} className="gap-2 border-0 bg-transparent"/>
  </div>
}
