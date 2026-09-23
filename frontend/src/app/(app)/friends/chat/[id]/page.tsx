'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft, Send, Users } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'

type Message={id:number;sender_id:number;recipient_id:number;content:string;created_at:string}

export default function FriendChatPage() {
  const params=useParams<{id:string}>()
  const user=useAuthStore(s=>s.user)
  const friendId=Number(params.id)
  const [friend,setFriend]=useState<any>(null)
  const [messages,setMessages]=useState<Message[]>([])
  const [input,setInput]=useState('')
  const [loading,setLoading]=useState(true)
  const [sending,setSending]=useState(false)
  const bottom=useRef<HTMLDivElement>(null)

  async function load() {
    if (!friendId) return
    const [friendsRes,msgRes]=await Promise.all([
      apiFetch('/api/social/friends'),
      apiFetch('/api/social/messages/'+friendId),
    ])
    if (friendsRes.ok) {
      const list=await friendsRes.json()
      setFriend(list.find((item:any)=>item.id===friendId)||null)
    }
    if (msgRes.ok) setMessages(await msgRes.json())
    setLoading(false)
  }
  useEffect(()=>{load(); const timer=window.setInterval(load,4000); return()=>window.clearInterval(timer)},[friendId])
  useEffect(()=>{bottom.current?.scrollIntoView({behavior:'smooth'})},[messages])

  async function send() {
    const content=input.trim()
    if(!content||sending)return
    setSending(true); setInput('')
    const res=await apiFetch('/api/social/messages/'+friendId,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({content})})
    if(res.ok) setMessages(prev=>[...prev,await res.json()])
    else setInput(content)
    setSending(false)
  }

  return <div className="mx-auto flex h-[calc(100dvh-110px)] max-w-5xl flex-col px-4 py-5 sm:px-6">
    <div className="mb-4 flex items-center gap-3"><Link href="/friends" className="juba-icon-button"><ArrowLeft className="h-4 w-4"/></Link><div className="h-10 w-10 overflow-hidden rounded-full border border-[var(--juba-border)] bg-[var(--juba-bg)]">{friend?.avatar?<AuthAvatarImage avatar={friend.avatar} alt="" width={40} height={40} className="h-full w-full object-cover"/>:<div className="flex h-full w-full items-center justify-center font-bold text-[var(--juba-muted)]">{(friend?.display_name||'?')[0]}</div>}</div><div><h1 className="font-bold">{friend?.display_name||'Learning friend'}</h1><p className="text-xs text-[var(--juba-muted)]"><Users className="mr-1 inline h-3 w-3"/> Learning chat</p></div></div>
    <div className="juba-panel flex min-h-0 flex-1 flex-col p-0">
      <div className="flex-1 space-y-3 overflow-y-auto p-4 sm:p-6">
        {loading?<p className="juba-muted">Loading…</p>:messages.length===0?<div className="flex h-full items-center justify-center text-center text-sm text-[var(--juba-muted)]">Start a friendly language-learning conversation.</div>:
        messages.map(message=><div key={message.id} className={'flex '+(message.sender_id===user?.id?'justify-end':'justify-start')}><div className={'max-w-[78%] rounded-2xl px-4 py-3 text-sm '+(message.sender_id===user?.id?'bg-[#39751d] text-white shadow-[3px_3px_0_#25302a]':'border border-[var(--juba-border)] bg-[var(--juba-surface)]')}><p className="whitespace-pre-wrap break-words">{message.content}</p><p className={'mt-1 text-[10px] '+(message.sender_id===user?.id?'text-white/70':'text-[var(--juba-muted)]')}>{new Date(message.created_at).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</p></div></div>)}
        <div ref={bottom}/>
      </div>
      <div className="border-t border-[var(--juba-border)] p-3 sm:p-4"><div className="flex gap-2"><input value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==='Enter'&&!e.shiftKey&&send()} placeholder="Write a message…" className="juba-input flex-1"/><button onClick={send} disabled={!input.trim()||sending} className="juba-primary-button"><Send className="h-4 w-4"/>{sending?'Sending':'Send'}</button></div></div>
    </div>
  </div>
}
