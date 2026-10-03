'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams } from 'next/navigation'
import { useLocale } from 'next-intl'
import Link from 'next/link'
import { ArrowLeft, Send, Users } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'

type Message={id:number;sender_id:number;recipient_id:number;content:string;created_at:string}

export default function FriendChatPage() {
  const params=useParams<{id:string}>()
  const locale=useLocale()
  const rtl=locale==='ar'
  const user=useAuthStore(s=>s.user)
  const friendId=Number(params.id)
  const [friend,setFriend]=useState<any>(null)
  const [messages,setMessages]=useState<Message[]>([])
  const [input,setInput]=useState('')
  const [loading,setLoading]=useState(true)
  const [sending,setSending]=useState(false)
  const [error,setError]=useState('')
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
    if (msgRes.ok) {
      const incoming=await msgRes.json()
      setMessages((prev)=>{
        const byId=new Map(prev.map((item)=>[item.id,item]))
        incoming.forEach((item:Message)=>byId.set(item.id,item))
        return Array.from(byId.values()).sort((a,b)=>a.id-b.id)
      })
      setError('')
    } else if (msgRes.status===403 || msgRes.status===404) {
      setError('This learner is not available for direct chat. Please return to Friends.')
    } else {
      setError('Unable to load the conversation. Please try again.')
    }
    setLoading(false)
  }
  useEffect(()=>{load(); const timer=window.setInterval(load,4000); return()=>window.clearInterval(timer)},[friendId])
  useEffect(()=>{bottom.current?.scrollIntoView({behavior:'smooth'})},[messages])

  async function send() {
    const content=input.trim()
    if(!content||sending||!friend)return
    setSending(true); setError(''); setInput('')
    const res=await apiFetch('/api/social/messages/'+friendId,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({content})})
    if(res.ok) {
      const message=await res.json()
      setMessages(prev=>prev.some(item=>item.id===message.id)?prev:[...prev,message])
    } else {
      setInput(content)
      setError(res.status===403?'You can only message accepted friends.':'Message could not be sent. Please try again.')
    }
    setSending(false)
  }

  const avatar=(avatarValue:string|undefined,name:string)=> <span className="reference-peer-avatar">{avatarValue?<AuthAvatarImage avatar={avatarValue} alt="" width={32} height={32} className="h-full w-full object-cover"/>:<span aria-hidden="true">{name.charAt(0).toUpperCase()||'?'}</span>}</span>

  return <section className="juba-page-shell reference-peer-chat" dir={rtl?'rtl':'ltr'} aria-label={rtl?'محادثة الأصدقاء':'Friend conversation'}>
    <style>{`
      .juba-app-shell .reference-peer-chat{display:flex;flex-direction:column;height:calc(100dvh - 64px);min-height:400px;gap:24px;padding:12px 24px 24px!important;color:var(--juba-ink,var(--duo-ink));}
      .juba-app-shell .reference-peer-header{display:flex;align-items:center;gap:12px;min-height:52px;padding:8px 16px;background:var(--juba-soft,var(--duo-soft));border-radius:6px;flex-shrink:0;}
      .juba-app-shell .reference-peer-back{display:inline-flex;align-items:center;gap:8px;min-height:36px;color:var(--juba-muted,var(--duo-muted));font-size:11px;text-decoration:none;}
      .juba-app-shell .reference-peer-chat[dir="rtl"] .reference-peer-back svg{transform:scaleX(-1);}
      .juba-app-shell .reference-peer-avatar{display:grid;place-items:center;width:32px;height:32px;flex-shrink:0;overflow:hidden;border-radius:50%;background:var(--juba-soft,var(--duo-soft));color:var(--juba-green,var(--duo-green));font-size:12px;font-weight:700;}
      .juba-app-shell .reference-peer-title{font-size:14px;line-height:1.4;font-weight:700;margin:0;}
      .juba-app-shell .reference-peer-subtitle{display:flex;align-items:center;gap:4px;font-size:11px;color:var(--juba-muted,var(--duo-muted));margin:2px 0 0;}
      .juba-app-shell .reference-peer-history{flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;display:flex;flex-direction:column;gap:28px;padding:12px clamp(8px,5vw,64px);}
      .juba-app-shell .reference-peer-message{display:flex;flex-direction:column;align-items:flex-start;gap:8px;max-width:min(78%,440px);align-self:flex-start;}
      .juba-app-shell .reference-peer-message[data-outgoing="true"]{align-self:flex-end;align-items:flex-end;}
      .juba-app-shell .reference-peer-meta{display:flex;align-items:center;gap:8px;color:var(--juba-muted,var(--duo-muted));font-size:11px;}
      .juba-app-shell .reference-peer-meta time{font-size:10px;font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-peer-bubble{padding:12px 16px;background:oklch(98% .012 130);border-radius:6px;font-size:14px;line-height:1.6;max-width:100%;}
      .juba-app-shell .reference-peer-message[data-outgoing="true"] .reference-peer-bubble{background:var(--juba-soft,var(--duo-soft));}
      .juba-app-shell .reference-peer-bubble p{margin:0;white-space:pre-wrap;overflow-wrap:anywhere;text-align:start;}
      .juba-app-shell .reference-peer-composer{display:flex;align-items:center;gap:12px;flex-shrink:0;margin-inline:clamp(0px,4vw,48px);padding:8px 12px;border:1px solid var(--juba-border,var(--duo-line));border-radius:6px;background:var(--juba-card,var(--duo-card));}
      .juba-app-shell .reference-peer-composer input{flex:1;min-width:0;border:0;background:transparent;color:inherit;padding:8px;font-size:14px;min-height:36px;text-align:start;}
      .juba-app-shell .reference-peer-send{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:40px;padding:8px 12px;border:0;border-radius:5px;background:var(--juba-muted,var(--duo-muted));color:var(--juba-card,var(--duo-card));font-size:12px;font-weight:700;}
      .juba-app-shell .reference-peer-send:disabled{opacity:.45;cursor:not-allowed;}
      .juba-app-shell .reference-peer-send:not(:disabled):hover{background:var(--juba-green-dark,var(--duo-green-dark));}
      .juba-app-shell .reference-peer-state{display:grid;place-items:center;flex:1;min-height:160px;text-align:center;color:var(--juba-muted,var(--duo-muted));font-size:14px;}
      .juba-app-shell .reference-peer-error{padding:12px 16px;border:1px solid var(--duo-red);border-radius:6px;color:var(--duo-red);font-size:14px;}
      .juba-app-shell .reference-peer-skeleton{height:48px;width:42%;background:var(--juba-soft,var(--duo-soft));border-radius:6px;}
      .juba-app-shell .reference-peer-skeleton:nth-child(2){align-self:flex-end;width:54%;}
      @media(max-width:900px){.juba-app-shell .reference-peer-chat{height:calc(100dvh - 54px);min-height:0;padding:12px 16px 16px!important;gap:16px;}.juba-app-shell .reference-peer-history{padding:8px 0;gap:20px;}.juba-app-shell .reference-peer-message{max-width:88%;}.juba-app-shell .reference-peer-composer{margin-inline:0;gap:8px;}.juba-app-shell .reference-peer-send,.juba-app-shell .reference-peer-back{min-height:44px;}.juba-app-shell .reference-peer-composer input{font-size:16px;}}
    `}</style>
    <header className="reference-peer-header">
      <Link href="/friends" className="reference-peer-back" aria-label={rtl?'العودة إلى الأصدقاء':'Back to friends'}><ArrowLeft size={16}/><span>{rtl?'الأصدقاء':'Friends'}</span></Link>
      {avatar(friend?.avatar,friend?.display_name||'?')}
      <div><h1 className="reference-peer-title">{friend?.display_name||(rtl?'صديق التعلّم':'Learning friend')}</h1><p className="reference-peer-subtitle"><Users size={12}/>{rtl?'محادثة تعلّم':'Learning chat'}</p></div>
    </header>
    <div className="reference-peer-history" role="log" aria-live="polite" aria-relevant="additions" aria-busy={loading}>
      {error&&<div className="reference-peer-error" role="alert">{error}</div>}
      {loading?<div className="reference-peer-state" role="status"><span>{rtl?'جارٍ تحميل المحادثة…':'Loading conversation…'}</span><div className="reference-peer-skeleton" aria-hidden="true"/><div className="reference-peer-skeleton" aria-hidden="true"/></div>:messages.length===0?<div className="reference-peer-state">{rtl?'ابدأ محادثة ودّية لتعلّم اللغة.':'Start a friendly language-learning conversation.'}</div>:
        messages.map(message=>{const outgoing=message.sender_id===user?.id;const name=outgoing?(user?.displayName||user?.username||''):(friend?.display_name||'');return <article key={message.id} className="reference-peer-message" data-outgoing={outgoing}>
          <div className="reference-peer-meta">{avatar(outgoing?user?.avatar:friend?.avatar,name)}<span>{name}</span><time dateTime={message.created_at}>{new Date(message.created_at).toLocaleTimeString(locale,{hour:'2-digit',minute:'2-digit'})}</time></div>
          <div className="reference-peer-bubble"><p dir="auto">{message.content}</p></div>
        </article>})}
      <div ref={bottom}/>
    </div>
    <div className="reference-peer-composer"><input aria-label={rtl?'رسالتك':'Your message'} disabled={!friend||!!error} value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==='Enter'&&!e.shiftKey&&send()} placeholder={rtl?'اكتب رسالة…':'Write a message…'} dir="auto"/><button onClick={send} disabled={!input.trim()||sending} className="reference-peer-send"><Send size={16}/>{sending?(rtl?'جارٍ الإرسال':'Sending'):(rtl?'إرسال':'Send')}</button></div>
  </section>
}
