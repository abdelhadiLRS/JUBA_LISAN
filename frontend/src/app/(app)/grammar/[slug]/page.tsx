'use client'

import { use, useCallback, useEffect, useState, type ReactNode } from 'react'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { BookOpen, ChevronLeft, ChevronRight, ChevronDown, Languages, Check, X } from 'lucide-react'
import { getGrammarNativeHelp, getGrammarTopics, type GrammarNativeHelp, type GrammarTopic } from '@/data/grammar'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { PageLoading } from '@/components/ui/page-loading'
import '../../resource-reference.css'

function RichText({text}:{text:string}){return <>{text.split(/(\*\*[^*]+\*\*|`[^`]+`)/).map((part,index)=>part.startsWith('**')&&part.endsWith('**')?<strong key={index}>{part.slice(2,-2)}</strong>:part.startsWith('`')&&part.endsWith('`')?<code key={index}>{part.slice(1,-1)}</code>:<span key={index}>{part}</span>)}</>}
function Explanation({text}:{text:string}){
  const lines=text.split('\n')
  const blocks:ReactNode[]=[]
  let index=0
  while(index<lines.length){
    const line=lines[index]
    if(!line.trim()){index++;continue}
    if(line.startsWith('|')){
      const rows:string[]=[]
      const start=index
      while(index<lines.length&&lines[index].startsWith('|')){if(!/^\|?[\s:|\-]+$/.test(lines[index]))rows.push(lines[index]);index++}
      blocks.push(<div className="reference-resource-table" key={start}><table><tbody>{rows.map((row,rowIndex)=><tr key={rowIndex}>{row.split('|').filter(cell=>cell.trim()).map((cell,cellIndex)=><td dir="auto" key={cellIndex}><RichText text={cell.trim()}/></td>)}</tr>)}</tbody></table></div>)
    }else if(line.startsWith('- ')){
      const items:string[]=[]
      const start=index
      while(index<lines.length&&lines[index].startsWith('- ')){items.push(lines[index].slice(2));index++}
      blocks.push(<ul key={start}>{items.map((item,itemIndex)=><li key={itemIndex} dir="auto"><RichText text={item}/></li>)}</ul>)
    }else{blocks.push(<p key={index} dir="auto"><RichText text={line}/></p>);index++}
  }
  return <div className="reference-resource-prose">{blocks}</div>
}
function Panel({title,children}:{title:string;children:ReactNode}){return <section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{title}</h2></header><div className="reference-resource-body">{children}</div></section>}

export default function GrammarDetailPage({params}:{params:Promise<{slug:string}>}){
  const {slug}=use(params)
  const t=useTranslations('grammar')
  const tCommon=useTranslations('common')
  const tNav=useTranslations('nav')
  const tTargetLang=useTranslations('targetLanguages')
  const rtl=useLocale()==='ar'
  const activeLanguage=useLanguageStore(s=>s.activeLanguage)
  const user=useAuthStore(s=>s.user)
  const nativeLanguageName=user?.native_language?tTargetLang(user.native_language):''
  const targetLanguageCode=activeLanguage?.code??'en-GB'
  const [topics,setTopics]=useState<GrammarTopic[]>([])
  const [loading,setLoading]=useState(true)
  const [loadError,setLoadError]=useState(false)
  const [nativeHelpOpen,setNativeHelpOpen]=useState(false)
  const [nativeHelp,setNativeHelp]=useState<GrammarNativeHelp|null>(null)
  const [loadingNativeHelp,setLoadingNativeHelp]=useState(false)
  const [nativeHelpError,setNativeHelpError]=useState(false)
  const topic=topics.find(item=>item.slug===slug)
  const fetchTopics=useCallback(async(lang:string)=>{
    setLoading(true);setLoadError(false)
    try{setTopics(await getGrammarTopics(lang))}catch{setLoadError(true);setTopics([])}finally{setLoading(false)}
  },[])
  useEffect(()=>{void fetchTopics(targetLanguageCode)},[targetLanguageCode,fetchTopics])
  useEffect(()=>{
    setNativeHelp(null);setNativeHelpError(false)
    setNativeHelpOpen(topic?.level==='A1'||topic?.level==='A2')
  },[topic?.slug,topic?.level,targetLanguageCode])
  const generateNativeHelp=useCallback(async()=>{
    if(!topic||loadingNativeHelp)return
    setLoadingNativeHelp(true);setNativeHelpError(false)
    try{const help=await getGrammarNativeHelp(topic.slug,targetLanguageCode);if(help)setNativeHelp(help);else setNativeHelpError(true)}catch{setNativeHelpError(true)}finally{setLoadingNativeHelp(false)}
  },[loadingNativeHelp,targetLanguageCode,topic])
  useEffect(()=>{
    if(nativeLanguageName&&nativeHelpOpen&&topic&&!nativeHelp&&!loadingNativeHelp&&!nativeHelpError)void generateNativeHelp()
  },[nativeLanguageName,nativeHelpOpen,topic,nativeHelp,loadingNativeHelp,nativeHelpError,generateNativeHelp])
  if(loading)return <div className="juba-page-shell"><PageLoading/></div>
  if(loadError)return <div className="juba-page-shell"><section className="reference-resource-state" role="alert"><BookOpen size={28}/><p>{tCommon('error')}</p><button className="juba-secondary-button" onClick={()=>void fetchTopics(targetLanguageCode)}>{tCommon('retry')}</button></section></div>
  if(!topic)notFound()
  const relatedTopics=topic.related.map(related=>topics.find(item=>item.slug===related)).filter((item):item is GrammarTopic=>Boolean(item))
  const Back=rtl?ChevronRight:ChevronLeft
  const Forward=rtl?ChevronLeft:ChevronRight
  return <div className="juba-page-shell reference-resource-page" dir={rtl?'rtl':'ltr'}>
    <nav className="reference-resource-breadcrumb" aria-label={t('backToGrammar')}><Link href="/grammar"><Back size={14}/>{tNav('grammar')}</Link><span aria-hidden="true">/</span><span>{topic.level}</span><span aria-hidden="true">/</span><span dir="auto">{topic.title}</span></nav>
    <header className="reference-resource-heading"><BookOpen size={40} aria-hidden="true"/><div><h1 dir="auto">{topic.title}</h1><p dir="auto">{topic.summary}</p><div className="reference-resource-tags"><span>{topic.level}</span><span>{topic.category}</span></div></div></header>
    <div className="reference-resource-detail-grid"><div className="reference-resource-primary">
      {topic.structure&&<Panel title={t('structure')}><p className="reference-resource-formula" dir="auto">{topic.structure}</p></Panel>}
      <Panel title={t('explanation')}><Explanation text={topic.explanation}/></Panel>
      {topic.examples.length>0&&<Panel title={t('examples')}><div className="reference-resource-items">{topic.examples.map((example,index)=><article key={index}><TargetLanguageText as="p" languageCode={targetLanguageCode} dir="auto">{example.text}</TargetLanguageText>{example.note&&<p className="reference-resource-caption" dir="auto">{example.note}</p>}</article>)}</div></Panel>}
      {topic.common_mistakes.length>0&&<Panel title={t('commonMistakes')}><div className="reference-resource-items">{topic.common_mistakes.map((mistake,index)=><article className="reference-resource-mistake" key={index}>{mistake.wrong&&<div><X size={16} aria-hidden="true"/><p dir="auto"><s>{mistake.wrong}</s></p></div>}{mistake.correct&&<div><Check size={16} aria-hidden="true"/><p dir="auto">{mistake.correct}</p></div>}{mistake.note&&<p className="reference-resource-caption" dir="auto">{mistake.note}</p>}</article>)}</div></Panel>}
      {nativeLanguageName&&<section className="reference-resource-panel"><button className="reference-resource-help-toggle" aria-expanded={nativeHelpOpen} aria-controls="grammar-native-help" onClick={()=>setNativeHelpOpen(value=>!value)}><Languages size={20}/><span>{tCommon('nativeHelpTitle',{language:nativeLanguageName})}</span><ChevronDown size={16}/></button><div className="reference-resource-body reference-resource-native" id="grammar-native-help" hidden={!nativeHelpOpen}>{loadingNativeHelp?<p role="status">{tCommon('nativeHelpLoading',{language:nativeLanguageName})}</p>:nativeHelp?<>
        <p dir="auto">{nativeHelp.summary}</p><p dir="auto">{nativeHelp.explanation}</p>
        {nativeHelp.key_points.length>0&&<section><h3>{tCommon('nativeHelpKeyPoints')}</h3><ul>{nativeHelp.key_points.map((point,index)=><li key={index} dir="auto">{point}</li>)}</ul></section>}
        {nativeHelp.examples.length>0&&<section><h3>{t('examples')}</h3>{nativeHelp.examples.map((example,index)=><article key={index}><TargetLanguageText as="p" languageCode={targetLanguageCode} dir="auto">{example.sentence}</TargetLanguageText><p dir="auto">{example.note}</p></article>)}</section>}
        {nativeHelp.common_traps.length>0&&<section><h3>{tCommon('nativeHelpCommonTraps')}</h3>{nativeHelp.common_traps.map((trap,index)=><article key={index}><p dir="auto">{trap.mistake}</p><p dir="auto">{trap.fix}</p></article>)}</section>}
        {nativeHelp.mini_glossary.length>0&&<section><h3>{tCommon('nativeHelpMiniGlossary')}</h3>{nativeHelp.mini_glossary.map((item,index)=><article key={index}><TargetLanguageText languageCode={targetLanguageCode} dir="auto" className="font-semibold">{item.term}</TargetLanguageText><p dir="auto">{item.meaning}</p>{item.note&&<p dir="auto">{item.note}</p>}</article>)}</section>}
      </>:<div className="reference-resource-state">{nativeHelpError&&<p role="alert">{tCommon('error')}</p>}<button className="juba-secondary-button" onClick={()=>void generateNativeHelp()}>{nativeHelpError?tCommon('retry'):tCommon('nativeHelpShow',{language:nativeLanguageName})}</button></div>}</div></section>}
    </div><aside className="reference-resource-secondary">
      {topic.rules.length>0&&<Panel title={t('keyRules')}><ol className="reference-resource-rule-list">{topic.rules.map((rule,index)=><li key={index}><span>{index+1}</span><p dir="auto">{rule}</p></li>)}</ol></Panel>}
      {relatedTopics.length>0&&<section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{t('relatedTopics')}</h2></header>{relatedTopics.map(related=><Link className="reference-resource-link-row" key={related.slug} href={'/grammar/'+related.slug}><span><strong dir="auto">{related.title}</strong><small>{related.level}</small></span><Forward size={16}/></Link>)}</section>}
    </aside></div>
    <Link href="/grammar" className="reference-resource-back"><Back size={16}/>{t('backLink')}</Link>
  </div>
}
