'use client'

import { useCallback, useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { BookOpen, Search, ChevronRight } from 'lucide-react'
import { getGrammarTopics, type GrammarTopic } from '@/data/grammar'
import type { GrammarCategory } from '@/data/types'
import { CEFR_LEVELS } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
import { PageLoading } from '@/components/ui/page-loading'

export default function GrammarIndexPage() {
  const t=useTranslations('grammar')
  const tCommon=useTranslations('common')
  const locale=useLocale()
  const rtl=locale==='ar'
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const [topics,setTopics]=useState<GrammarTopic[]>([])
  const [loading,setLoading]=useState(true)
  const [loadError,setLoadError]=useState(false)
  const [search,setSearch]=useState('')
  const [activeCategory,setActiveCategory]=useState<GrammarCategory|'All'>('All')
  const fetchTopics=useCallback(async(lang:string)=>{
    setLoading(true);setLoadError(false)
    try {setTopics(await getGrammarTopics(lang))} catch {setLoadError(true);setTopics([])} finally {setLoading(false)}
  },[])
  useEffect(()=>{void fetchTopics(activeLanguage?.code??'en-GB')},[activeLanguage?.code,fetchTopics])
  const categories=useMemo(()=>Array.from(new Set(topics.map(topic=>topic.category))).sort() as GrammarCategory[],[topics])
  const filtered=useMemo(()=>{const q=search.toLowerCase();return topics.filter(topic=>(!q||[topic.title,topic.summary,topic.category].some(value=>value.toLowerCase().includes(q)))&&(activeCategory==='All'||topic.category===activeCategory))},[topics,search,activeCategory])
  const hasFilters=Boolean(search)||activeCategory!=='All'
  return <div className="juba-page-shell reference-grammar" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-grammar{display:flex;flex-direction:column;gap:24px;}
      .juba-app-shell .reference-grammar-header{display:flex;align-items:center;gap:16px;min-height:100px;}
      .juba-app-shell .reference-grammar-header>svg{color:var(--juba-green);flex:none;}
      .juba-app-shell .reference-grammar-header h1{font-size:28px;font-weight:650;margin:0;}
      .juba-app-shell .reference-grammar-header p{font-size:13px;color:var(--juba-muted);margin:6px 0 0;}
      .juba-app-shell .reference-grammar-filters{display:flex;flex-direction:column;gap:16px;padding:16px;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);}
      .juba-app-shell .reference-grammar-search{display:flex;align-items:center;gap:8px;color:var(--juba-muted);max-width:480px;}
      .juba-app-shell .reference-grammar-search input{width:100%;padding:8px 12px;}
      .juba-app-shell .reference-grammar-categories{display:flex;flex-wrap:wrap;gap:8px;}
      .juba-app-shell .reference-grammar-categories button{min-height:36px;padding:6px 12px;border:1px solid var(--juba-border);border-radius:5px;font-size:12px;background:var(--juba-card);color:var(--juba-muted);}
      .juba-app-shell .reference-grammar-categories button[aria-pressed="true"]{color:var(--juba-green-dark);background:var(--juba-green-soft);border-color:var(--juba-green);}
      .juba-app-shell .reference-grammar-level{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
      .juba-app-shell .reference-grammar-level>header{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-grammar-level h2{font-size:15px;margin:0;font-weight:650;}
      .juba-app-shell .reference-grammar-level>header>span{font-size:11px;color:var(--juba-muted);}
      .juba-app-shell .reference-grammar-topic{display:grid;grid-template-columns:28px minmax(0,1fr) auto 16px;align-items:center;gap:12px;padding:14px 16px;border-block-end:1px solid var(--juba-border);text-decoration:none;color:var(--juba-ink);}
      .juba-app-shell .reference-grammar-topic:last-child{border:0;}
      .juba-app-shell .reference-grammar-topic:hover{background:var(--juba-green-soft);}
      .juba-app-shell .reference-grammar-topic>svg{color:var(--juba-green-dark);}
      .juba-app-shell .reference-grammar-topic strong{font-size:14px;font-weight:600;}
      .juba-app-shell .reference-grammar-topic p{margin:4px 0 0;font-size:13px;line-height:1.5;color:var(--juba-muted);}
      .juba-app-shell .reference-grammar-topic>span{font-size:11px;color:var(--juba-muted);padding:4px 8px;background:var(--juba-soft);border-radius:4px;}
      .juba-app-shell .reference-grammar[dir="rtl"] .reference-grammar-topic>svg:last-child{transform:scaleX(-1);}
      .juba-app-shell .reference-grammar-state{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;border:1px solid var(--juba-border);border-radius:6px;padding:32px;font-size:14px;color:var(--juba-muted);text-align:center;}
      .juba-app-shell .reference-grammar-count{font-size:12px;color:var(--juba-muted);margin:0;}
      @media(max-width:640px){.juba-app-shell .reference-grammar{gap:16px;}.juba-app-shell .reference-grammar-header h1{font-size:24px;}.juba-app-shell .reference-grammar-categories button{min-height:44px;}.juba-app-shell .reference-grammar-topic{grid-template-columns:24px minmax(0,1fr) 16px;gap:8px;}.juba-app-shell .reference-grammar-topic>span{grid-column:2;justify-self:start;grid-row:2;}.juba-app-shell .reference-grammar-topic>svg:last-child{grid-column:3;grid-row:1;}}
    `}</style>
    <header className="reference-grammar-header"><BookOpen size={40} aria-hidden="true"/><div><h1>{t('title')}</h1><p>{topics.length} · A1 - C2</p></div></header>
    {loading?<PageLoading/>:loadError?<div className="reference-grammar-state" role="alert"><p>{tCommon('error')}</p><button className="juba-secondary-button" onClick={()=>void fetchTopics(activeLanguage?.code??'en-GB')}>{tCommon('retry')}</button></div>:<>
      <section className="reference-grammar-filters" aria-label={t('searchPlaceholder')}><label className="reference-grammar-search"><Search size={18} aria-hidden="true"/><input className="juba-input" type="search" value={search} onChange={event=>setSearch(event.target.value)} placeholder={t('searchPlaceholder')} aria-label={t('searchPlaceholder')}/></label><div className="reference-grammar-categories" role="group" aria-label={t('allCategories')}><button aria-pressed={activeCategory==='All'} onClick={()=>setActiveCategory('All')}>{t('allCategories')}</button>{categories.map(category=><button key={category} aria-pressed={activeCategory===category} onClick={()=>setActiveCategory(activeCategory===category?'All':category)}>{category}</button>)}</div></section>
      {hasFilters&&<p className="reference-grammar-count" role="status">{t('topicsFound',{count:filtered.length})}</p>}
      {CEFR_LEVELS.map(level=>{const levelTopics=filtered.filter(topic=>topic.level===level);return levelTopics.length?<section className="reference-grammar-level" key={level} aria-labelledby={'grammar-'+level}><header><h2 id={'grammar-'+level}>{level}</h2><span>{levelTopics.length}</span></header>{levelTopics.map(topic=><Link key={topic.slug} href={'/grammar/'+topic.slug} className="reference-grammar-topic"><BookOpen size={20} aria-hidden="true"/><div><strong>{topic.title}</strong><p>{topic.summary}</p></div><span>{topic.category}</span><ChevronRight size={16} aria-hidden="true"/></Link>)}</section>:null})}
      {!filtered.length&&<div className="reference-grammar-state"><BookOpen size={28} aria-hidden="true"/><p>{t('noResults')}</p>{hasFilters&&<button className="juba-secondary-button" onClick={()=>{setSearch('');setActiveCategory('All')}}>{tCommon('clearFilters')}</button>}</div>}
    </>}
  </div>
}
