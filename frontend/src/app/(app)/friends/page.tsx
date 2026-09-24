'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { MessageCircle, Search, UserPlus, Users, Check, UserMinus } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'

type Person = { id:number; username:string; display_name:string; avatar?:string|null; target_language?:string; bio?:string|null }
type RequestItem = { id:number; user:Person }

export default function FriendsPage() {
  const [friends,setFriends]=useState<Person[]>([])
  const [incoming,setIncoming]=useState<RequestItem[]>([])
  const [outgoing,setOutgoing]=useState<RequestItem[]>([])
  const [results,setResults]=useState<Person[]>([])
  const [query,setQuery]=useState('')
  const [loading,setLoading]=useState(true)
  const [error,setError]=useState('')
  const [searching,setSearching]=useState(false)
  const [actionId,setActionId]=useState<number|null>(null)

  async function load() {
    setLoading(true); setError('')
    try {
      const [friendsRes, requestsRes] = await Promise.all([
        apiFetch('/api/social/friends'),
        apiFetch('/api/social/requests'),
      ])
      if (!friendsRes.ok || !requestsRes.ok) throw new Error()
      setFriends(await friendsRes.json())
      const req=await requestsRes.json()
      setIncoming(req.incoming ?? []); setOutgoing(req.outgoing ?? [])
    } catch { setError('Unable to load your learning community.') }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  async function search() {
    if (query.trim().length < 2) { setResults([]); return }
    setSearching(true); setError('')
    try {
      const res=await apiFetch('/api/social/users?q='+encodeURIComponent(query.trim()))
      if (!res.ok) throw new Error()
      setResults(await res.json())
    } catch { setError('Unable to search learners right now.') }
    finally { setSearching(false) }
  }

  async function addFriend(id:number) {
    setActionId(id)
    const res=await apiFetch('/api/social/requests',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:id})})
    if (res.ok) { setResults(prev=>prev.filter(p=>p.id!==id)); await load() }
    else setError((await res.json().catch(()=>({detail:'Unable to send friend request.'}))).detail || 'Unable to send friend request.')
    setActionId(null)
  }

  async function accept(id:number) {
    setActionId(id)
    const res=await apiFetch('/api/social/requests/'+id+'/accept',{method:'POST'})
    if (res.ok) await load()
    else setError('Unable to accept this request.')
    setActionId(null)
  }

  async function remove(id:number) {
    setActionId(id)
    const res=await apiFetch('/api/social/friends/'+id,{method:'DELETE'})
    if (res.ok) await load()
    else setError('Unable to remove this friend.')
    setActionId(null)
  }

  return (
    <div className="juba-friends-shell juba-page-shell space-y-6 px-4 py-6 sm:px-6">
      <section className="juba-page-hero">
        <div>
          <p className="juba-eyebrow"><Users className="inline h-4 w-4" /> LEARN TOGETHER</p>
          <h1 className="juba-page-title">Friends</h1>
          <p className="juba-page-subtitle">Find learners, practise together, and keep your language journey social.</p>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.35fr_.65fr]">
        <div className="juba-panel space-y-4">
          <div className="flex items-center gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--juba-app-muted)]" />
              <input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&search()} placeholder="Search learners by name or username" className="juba-input pl-10" />
            </div>
            <button onClick={search} disabled={searching} className="juba-primary-button"><Search className="h-4 w-4" /> {searching?'Searching…':'Search'}</button>
          </div>
          {results.length>0 && <div className="grid gap-3 md:grid-cols-2">{results.map(person=><PersonCard key={person.id} person={person}><button onClick={()=>addFriend(person.id)} disabled={actionId===person.id} className="juba-secondary-button"><UserPlus className="h-4 w-4"/> {actionId===person.id?'Adding…':'Add'}</button></PersonCard>)}</div>}
          <div className="flex items-center justify-between pt-2"><h2 className="juba-section-title">Your learning friends</h2><span className="juba-badge">{friends.length}</span></div>
          {loading ? <p className="juba-muted">Loading…</p> : friends.length===0 ? <Empty text="No friends yet. Search for another learner to start practising together."/> :
            <div className="grid gap-3 md:grid-cols-2">{friends.map(person=><PersonCard key={person.id} person={person}><div className="flex gap-2"><Link href={'/friends/chat/'+person.id} className="juba-primary-button"><MessageCircle className="h-4 w-4"/> Chat</Link><button onClick={()=>remove(person.id)} disabled={actionId===person.id} className="juba-secondary-button" title="Remove friend"><UserMinus className="h-4 w-4"/></button></div></PersonCard>)}</div>}
          {error && <p className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</p>}
        </div>

        <div className="juba-panel">
          <h2 className="juba-section-title">Friend requests</h2>
          <div className="mt-4 space-y-3">
            {incoming.map(item=><PersonCard key={item.id} person={item.user}><button onClick={()=>accept(item.id)} disabled={actionId===item.id} className="juba-primary-button"><Check className="h-4 w-4"/> {actionId===item.id?'Accepting…':'Accept'}</button></PersonCard>)}
            {outgoing.map(item=><PersonCard key={'o'+item.id} person={item.user}><span className="juba-badge">Pending</span></PersonCard>)}
            {!incoming.length&&!outgoing.length&&<Empty text="No pending requests."/>}
          </div>
        </div>
      </section>
    </div>
  )
}

function PersonCard({person,children}:{person:Person;children:React.ReactNode}) {
  return <div className="flex items-center gap-3 rounded-2xl border border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] p-3 shadow-sm">
    <div className="h-11 w-11 shrink-0 overflow-hidden rounded-full border border-[var(--juba-app-line)] bg-[var(--juba-app-bg)]">
      {person.avatar ? <AuthAvatarImage avatar={person.avatar} alt="" width={44} height={44} className="h-full w-full object-cover"/> : <div className="flex h-full w-full items-center justify-center font-bold text-[var(--juba-app-muted)]">{(person.display_name||person.username||'?')[0].toUpperCase()}</div>}
    </div>
    <div className="min-w-0 flex-1"><p className="truncate font-semibold">{person.display_name||person.username}</p><p className="truncate text-xs text-[var(--juba-app-muted)]">@{person.username}{person.target_language?' · '+person.target_language:''}</p></div>
    {children}
  </div>
}
function Empty({text}:{text:string}) { return <div className="rounded-2xl border border-dashed border-[var(--juba-app-line)] bg-[var(--juba-app-bg)] p-6 text-center text-sm text-[var(--juba-app-muted)]">{text}</div> }
