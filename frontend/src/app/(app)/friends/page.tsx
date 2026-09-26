'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
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
  const [inviteUrl,setInviteUrl]=useState('')
  const [inviteCopied,setInviteCopied]=useState(false)
  const [inviteLoading,setInviteLoading]=useState(false)

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

  async function createInvite() {
    setInviteLoading(true); setError(''); setInviteCopied(false)
    try {
      const res=await apiFetch('/api/invites/create',{method:'POST'})
      const data=await res.json().catch(()=>({}))
      if (!res.ok) throw new Error(data.detail || 'Unable to create invitation.')
      setInviteUrl(window.location.origin + data.invite_url)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to create invitation.')
    } finally { setInviteLoading(false) }
  }

  async function copyInvite() {
    if (!inviteUrl) return
    try {
      await navigator.clipboard.writeText(inviteUrl)
      setInviteCopied(true)
      window.setTimeout(()=>setInviteCopied(false),2000)
    } catch { setError('Unable to copy invitation link.') }
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
    <div className="card">
      <section className="card">
        <div>
          <p className="page-pretitle"><Users className="inline h-4 w-4" /> LEARN TOGETHER</p>
          <h1 className="juba-page-title">Friends</h1>
          <p className="juba-page-subtitle">Find learners, practise together, and keep your language journey social.</p>
        </div>
      </section>

      <section className="card">
        <div className="min-w-0">
          <p className="page-pretitle"><LinkIcon className="inline h-4 w-4" /> INVITE MEMBERS</p>
          <h2 className="juba-section-title mt-1">Invite a learner to JUBA LISAN</h2>
          <p className="juba-muted mt-1">Create a registration link and share it with someone you want to learn with.</p>
        </div>
        <button onClick={createInvite} disabled={inviteLoading} className="btn btn-primary shrink-0">
          <UserPlus className="h-4 w-4" /> {inviteLoading ? 'Creating…' : 'Create invite'}
        </button>
        {inviteUrl && (
          <div className="w-full rounded-2xl border border bg-[#f4f4f2] p-3">
            <div className="flex flex-wrap items-center gap-2">
              <p className="min-w-0 flex-1 break-all text-xs text-[rgba(32,33,39,.52)]">{inviteUrl}</p>
              <button onClick={copyInvite} className="btn btn-outline-secondary shrink-0">
                {inviteCopied ? <CheckCheck className="h-4 w-4"/> : <Clipboard className="h-4 w-4"/>}
                {inviteCopied ? 'Copied' : 'Copy link'}
              </button>
            </div>
          </div>
        )}
      </section>

      <section className="grid gap-4 lg:grid-cols-[1.35fr_.65fr]">
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[rgba(32,33,39,.52)]" />
              <input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&search()} placeholder="Search learners by name or username" className="form-control pl-10" />
            </div>
            <button onClick={search} disabled={searching} className="btn btn-primary"><Search className="h-4 w-4" /> {searching?'Searching…':'Search'}</button>
          </div>
          {results.length>0 && <div className="grid gap-3 md:grid-cols-2">{results.map(person=><PersonCard key={person.id} person={person}><button onClick={()=>addFriend(person.id)} disabled={actionId===person.id} className="btn btn-outline-secondary"><UserPlus className="h-4 w-4"/> {actionId===person.id?'Adding…':'Add'}</button></PersonCard>)}</div>}
          <div className="flex items-center justify-between pt-2"><h2 className="juba-section-title">Your learning friends</h2><span className="juba-badge">{friends.length}</span></div>
          {loading ? <p className="juba-muted">Loading…</p> : friends.length===0 ? <Empty text="No friends yet. Search for another learner to start practising together."/> :
            <div className="grid gap-3 md:grid-cols-2">{friends.map(person=><PersonCard key={person.id} person={person}><div className="flex gap-2"><Link href={'/friends/chat/'+person.id} className="btn btn-primary"><MessageCircle className="h-4 w-4"/> Chat</Link><button onClick={()=>remove(person.id)} disabled={actionId===person.id} className="btn btn-outline-secondary" title="Remove friend"><UserMinus className="h-4 w-4"/></button></div></PersonCard>)}</div>}
          {error && <p className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</p>}
        </div>

        <div className="card">
          <h2 className="juba-section-title">Friend requests</h2>
          <div className="mt-4 space-y-3">
            {incoming.map(item=><PersonCard key={item.id} person={item.user}><button onClick={()=>accept(item.id)} disabled={actionId===item.id} className="btn btn-primary"><Check className="h-4 w-4"/> {actionId===item.id?'Accepting…':'Accept'}</button></PersonCard>)}
            {outgoing.map(item=><PersonCard key={'o'+item.id} person={item.user}><span className="juba-badge">Pending</span></PersonCard>)}
            {!incoming.length&&!outgoing.length&&<Empty text="No pending requests."/>}
          </div>
        </div>
      </section>
    </div>
  )
}

function PersonCard({person,children}:{person:Person;children:React.ReactNode}) {
  return <div className="flex items-center gap-3 rounded-2xl border border bg-[#fff] p-3 shadow-sm">
    <div className="h-11 w-11 shrink-0 overflow-hidden rounded-full border border bg-[#f4f4f2]">
      {person.avatar ? <AuthAvatarImage avatar={person.avatar} alt="" width={44} height={44} className="h-full w-full object-cover"/> : <div className="flex h-full w-full items-center justify-center font-bold text-[rgba(32,33,39,.52)]">{(person.display_name||person.username||'?')[0].toUpperCase()}</div>}
    </div>
    <div className="min-w-0 flex-1"><p className="truncate font-semibold">{person.display_name||person.username}</p><p className="truncate text-xs text-[rgba(32,33,39,.52)]">@{person.username}{person.target_language?' · '+person.target_language:''}</p></div>
    {children}
  </div>
}
function Empty({text}:{text:string}) { return <div className="rounded-2xl border border-dashed border bg-[#f4f4f2] p-6 text-center text-sm text-[rgba(32,33,39,.52)]">{text}</div> }
