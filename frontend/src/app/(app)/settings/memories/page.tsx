'use client'

import { useCallback, useEffect, useState, type FormEvent } from 'react'
import Link from 'next/link'
import { useLocale, useTranslations } from 'next-intl'
import { Brain, Plus, Trash2, ChevronLeft, ChevronRight } from 'lucide-react'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import { MemoryApiError, clearMemories, createMemory, deleteMemory, fetchMemories } from '@/lib/memories'
import type { Memory } from '@/types/api'
import { SettingsPageHeader } from '@/components/settings/SettingsShell'
import '../../resource-reference.css'

export default function SettingsMemoriesPage(){
  const t=useTranslations('settings')
  const tCommon=useTranslations('common')
  const rtl=useLocale()==='ar'
  const [memories,setMemories]=useState<Memory[]>([])
  const [content,setContent]=useState('')
  const [loading,setLoading]=useState(true)
  const [loadError,setLoadError]=useState(false)
  const [adding,setAdding]=useState(false)
  const [deletingId,setDeletingId]=useState<number|null>(null)
  const [clearConfirm,setClearConfirm]=useState(false)
  const [clearing,setClearing]=useState(false)
  const [dialogError,setDialogError]=useState('')
  const [message,setMessage]=useState<{type:'success'|'error';text:string}|null>(null)
  const mutating=adding||deletingId!==null||clearing
  const loadMemories=useCallback(async()=>{
    setLoading(true);setLoadError(false)
    try{const data=await fetchMemories();setMemories(data.memories)}catch{setLoadError(true)}finally{setLoading(false)}
  },[])
  useEffect(()=>{void loadMemories()},[loadMemories])
  async function handleAdd(event:FormEvent<HTMLFormElement>){
    event.preventDefault()
    if(loading||loadError||mutating)return
    const normalized=content.trim()
    if(!normalized)return
    setAdding(true);setMessage(null)
    try{const memory=await createMemory(normalized);setMemories(previous=>[...previous,memory].slice(-150));setContent('');setMessage({type:'success',text:t('memoryAddSuccess')})}catch(error){setMessage({type:'error',text:error instanceof MemoryApiError&&error.status===409?t('memoryDuplicateError'):t('memoryAddError')})}finally{setAdding(false)}
  }
  async function handleDelete(id:number){
    if(mutating)return
    setDeletingId(id);setMessage(null)
    try{await deleteMemory(id);setMemories(previous=>previous.filter(memory=>memory.id!==id));setMessage({type:'success',text:t('memoryDeleteSuccess')})}catch{setMessage({type:'error',text:t('memoryDeleteError')})}finally{setDeletingId(null)}
  }
  async function handleClearAll(){
    if(mutating)return
    setClearing(true);setDialogError('')
    try{await clearMemories();setMemories([]);setClearConfirm(false);setMessage({type:'success',text:t('memoryClearSuccess')})}catch{setDialogError(t('memoryClearError'))}finally{setClearing(false)}
  }
  function sourceLabel(source:string){const labels:Record<string,string>={chat:t('memorySourceChat'),voice:t('memorySourceVoice'),conversation:t('memorySourceVoice'),manual:t('memorySourceManual')};return labels[source]??t('memorySourceUnknown')}
  const Back=rtl?ChevronRight:ChevronLeft
  return <div className="juba-page-shell reference-resource-page reference-memories" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-memory-title{display:flex;align-items:center;gap:16px;}
      .juba-app-shell .reference-memory-title>svg{color:var(--juba-green);flex:none;}
      .juba-app-shell .reference-memory-title>header{flex:1;min-width:0;}
      .juba-app-shell .reference-memory-layout{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:24px;align-items:start;}
      .juba-app-shell .reference-memory-primary{display:flex;flex-direction:column;gap:16px;min-width:0;}
      .juba-app-shell .reference-memory-description{font-size:13px;line-height:1.7;color:var(--juba-muted);margin:0;}
      .juba-app-shell .reference-memory-form{padding:16px;display:flex;flex-direction:column;gap:12px;}
      .juba-app-shell .reference-memory-form label{font-size:13px;font-weight:600;color:var(--juba-ink);}
      .juba-app-shell .reference-memory-form textarea{width:100%;padding:12px;resize:vertical;min-height:120px;}
      .juba-app-shell .reference-memory-form-hint{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:11px;color:var(--juba-muted);}
      .juba-app-shell .reference-memory-form-hint p{margin:0;}
      .juba-app-shell .reference-memory-form button{padding-inline:16px;align-self:flex-start;}
      .juba-app-shell .reference-memory-list{list-style:none;padding:0;margin:0;}
      .juba-app-shell .reference-memory-row{display:flex;align-items:flex-start;gap:12px;padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-memory-row:last-child{border:0;}
      .juba-app-shell .reference-memory-row>div{flex:1;min-width:0;}
      .juba-app-shell .reference-memory-row p{font-size:14px;line-height:1.7;color:var(--juba-ink);margin:0 0 8px;overflow-wrap:anywhere;}
      .juba-app-shell .reference-memory-source{display:inline-block;font-size:10px;padding:4px 8px;border-radius:4px;background:var(--juba-green-soft);color:var(--juba-green-dark);}
      .juba-app-shell .reference-memory-delete{display:grid;place-items:center;flex:none;width:36px;height:36px;border:1px solid var(--juba-border);border-radius:5px;color:var(--juba-muted);background:transparent;}
      .juba-app-shell .reference-memory-delete:hover:not(:disabled){border-color:var(--duo-red);color:var(--duo-red);}
      .juba-app-shell .reference-memory-clear{display:flex;align-items:center;gap:8px;min-height:40px;align-self:flex-start;padding:8px 12px;border:1px solid var(--juba-border);border-radius:6px;font-size:13px;color:var(--juba-muted);background:transparent;}
      .juba-app-shell .reference-memory-clear:hover:not(:disabled){color:var(--duo-red);border-color:var(--duo-red);}
      .juba-app-shell .reference-memory-message{padding:12px 16px;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-green-soft);color:var(--juba-green-dark);font-size:13px;}
      .juba-app-shell .reference-memory-message[data-type="error"]{background:var(--juba-card);border-color:var(--duo-red);color:var(--duo-red);}
      @media(max-width:1000px){.juba-app-shell .reference-memory-layout{grid-template-columns:1fr;}.juba-app-shell .reference-memory-form-panel{grid-row:1;}}
      @media(max-width:640px){.juba-app-shell .reference-memory-layout{gap:16px;}.juba-app-shell .reference-memory-delete,.juba-app-shell .reference-memory-clear{min-height:44px;}.juba-app-shell .reference-memory-title>svg{width:32px;height:32px;}}
    `}</style>
    <nav className="reference-resource-breadcrumb" aria-label={t('memoryBreadcrumb')}><Link href="/settings"><Back size={14}/>{t('title')}</Link><span aria-hidden="true">/</span><span>{t('sectionMemory')}</span></nav>
    <div className="reference-memory-title"><Brain size={40} aria-hidden="true"/><SettingsPageHeader eyebrow={t('title')} title={t('sectionMemory')}/></div>
    <p className="reference-memory-description">{t('memoryDescription')}</p>
    {message&&<div className="reference-memory-message" data-type={message.type} role={message.type==='error'?'alert':'status'}>{message.text}</div>}
    <div className="reference-memory-layout"><div className="reference-memory-primary"><section className="reference-resource-panel"><header className="reference-resource-panel-head"><h2>{t('sectionMemory')}</h2><span>{memories.length}</span></header>{loading?<PageLoading fullScreen={false}/>:loadError?<div className="reference-resource-state" role="alert"><p>{t('memoryLoadError')}</p><button className="juba-secondary-button" onClick={()=>void loadMemories()}>{tCommon('retry')}</button></div>:!memories.length?<div className="reference-resource-state"><Brain size={28}/><p>{t('memoryEmpty')}</p></div>:<ul className="reference-memory-list">{memories.map(memory=><li className="reference-memory-row" key={memory.id}><div><p dir="auto">{memory.content}</p><span className="reference-memory-source">{sourceLabel(memory.source)}</span></div><button className="reference-memory-delete" onClick={()=>void handleDelete(memory.id)} disabled={mutating} aria-label={t('memoryDeleteLabel',{content:memory.content})} aria-busy={deletingId===memory.id}>{deletingId===memory.id?'…':<Trash2 size={16} aria-hidden="true"/>}</button></li>)}</ul>}</section>{!loading&&!loadError&&memories.length>0&&<button className="reference-memory-clear" disabled={mutating} onClick={()=>{setDialogError('');setClearConfirm(true)}}><Trash2 size={16}/>{t('memoryClearAll')}</button>}</div>
    <section className="reference-resource-panel reference-memory-form-panel"><header className="reference-resource-panel-head"><h2>{t('memoryAdd')}</h2></header><form className="reference-memory-form" onSubmit={handleAdd} aria-busy={adding}><label htmlFor="memory-content">{t('memoryInputLabel')}</label><textarea id="memory-content" className="juba-input" value={content} onChange={event=>setContent(event.target.value)} maxLength={200} rows={3} required aria-describedby="memory-hint memory-count" placeholder={t('memoryInputPlaceholder')} dir="auto"/><div className="reference-memory-form-hint"><p id="memory-hint">{t('memoryInputHint',{max:200})}</p><span id="memory-count">{content.length}/200</span></div><button className="juba-primary-button" type="submit" disabled={loading||loadError||mutating||!content.trim()}><Plus size={16}/>{adding?t('memoryAdding'):t('memoryAdd')}</button></form></section></div>
    <ConfirmDialog open={clearConfirm} title={t('memoryClearAllTitle')} message={t('memoryClearAllMessage')} confirmLabel={clearing?t('memoryClearing'):t('memoryClearAllConfirm')} danger confirming={clearing} error={dialogError} onConfirm={()=>void handleClearAll()} onCancel={()=>setClearConfirm(false)}/>
  </div>
}
