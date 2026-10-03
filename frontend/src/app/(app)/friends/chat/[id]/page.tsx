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
type Friend={id:number;display_name:string;username?:string;avatar?:string|null}
function Avatar({value,name}:{value?:string|null;name:string}){return <span className="reference-peer-avatar">{value?<AuthAvatarImage avatar={value} alt="" width={32} height={32} className="h-full w-full object-cover"/>:<span aria-hidden="true">{name.charAt(0).toUpperCase()||'?'}</span>}</span>}
export default function FriendChatPage(){
  const params=useParams<{id:string}>()
  const locale=useLocale()
  const rtl=locale==='ar'
  const user=useAuthStore(s=>s.user)
  const friendId=Number(params.id)
  const [friend,setFriend]=useState<Friend|null>(null)
  const [messages,setMessages]=useState<Message[]>([])
  const [input,setInput]=useState('')
  const [loading,setLoading]=useState(true)
  const [sending,setSending]=useState(false)
  const [error,setError]=useState('')
  const [blocked,setBlocked]=useState(false)
  const bottom=useRef<HTMLDivElement>(null)
  const copy={unavailable:rtl?'هذا المتعلم غير متاح للمحادثة المباشرة. عُد إلى الأصدقاء.':'This learner is not available for direct chat. Please return to Friends.',loadError:rtl?'تعذر تحميل المحادثة. ستُعاد المحاولة تلقائيًا.':'Unable to load the conversation. Retrying automatically.',sendError:rtl?'تعذر إرسال الرسالة. أعد المحاولة.':'Message could not be sent. Please try again.',acceptedOnly:rtl?'يمكنك مراسلة الأصدقاء المقبولين فقط.':'You can only message accepted friends.'}
  useEffect(()=>{
    let cancelled=false
    let inFlight=false
    setLoading(true);setMessages([]);setFriend(null);setBlocked(false);setError('')
    async function load(){
      if(inFlight||cancelled)return
      if(!Number.isInteger(friendId)||friendId<=0){setError(copy.unavailable);setBlocked(true);setLoading(false);return}
      inFlight=true
      try{
        const [friendsRes,msgRes]=await Promise.all([apiFetch('/api/social/friends'),apiFetch('/api/social/messages/'+friendId)])
        const list:Friend[]=friendsRes.ok?await friendsRes.json():[]
        const incoming:Message[]=msgRes.ok?await msgRes.json():[]
        if(cancelled)return
        if(friendsRes.ok)setFriend(list.find(item=>item.id===friendId)||null)
        if(msgRes.ok){
          setMessages(previous=>{
            const byId=new Map(previous.map(item=>[item.id,item]))
            incoming.forEach(item=>byId.set(item.id,item))
            const next=Array.from(byId.values()).sort((a,b)=>a.id-b.id)
            return next.length===previous.length&&next.every((item,index)=>item.id===previous[index].id&&item.content===previous[index].content)?previous:next
          })
          setError('');setBlocked(false)
        }else if(msgRes.status===403||msgRes.status===404){setError(copy.unavailable);setBlocked(true)}
        else setError(copy.loadError)
      }catch{if(!cancelled)setError(copy.loadError)}finally{inFlight=false;if(!cancelled)setLoading(false)}
    }
    void load()
    const timer=window.setInterval(()=>void load(),4000)
    return ()=>{cancelled=true;window.clearInterval(timer)}
  },[friendId,locale])
  useEffect(()=>{bottom.current?.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})},[messages])
  async function send(){
    const content=input.trim()
    if(!content||sending||!friend||blocked)return
    setSending(true);setError('');setInput('')
    try{
      const res=await apiFetch('/api/social/messages/'+friendId,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({content})})
      if(res.ok){const message=await res.json() as Message;setMessages(previous=>previous.some(item=>item.id===message.id)?previous:[...previous,message])}
      else{setInput(previous=>previous||content);setError(res.status===403?copy.acceptedOnly:copy.sendError);if(res.status===403)setBlocked(true)}
    }catch{setInput(previous=>previous||content);setError(copy.sendError)}finally{setSending(false)}
  }
  return <section className="juba-page-shell reference-peer-chat" dir={rtl?'rtl':'ltr'} aria-label={rtl?'محادثة الأصدقاء':'Friend conversation'}>
    <style>{`
      .juba-app-shell .reference-peer-chat{display:flex;flex-direction:column;height:calc(100dvh - 64px);min-height:400px;gap:24px;padding:12px 24px 24px!important;color:var(--juba-ink);box-sizing:border-box;}
      .juba-app-shell .reference-peer-header{display:flex;align-items:center;gap:12px;min-height:52px;padding:8px 16px;background:var(--juba-soft);border-radius:6px;flex-shrink:0;}
      .juba-app-shell .reference-peer-back{display:inline-flex;align-items:center;gap:8px;min-height:36px;color:var(--juba-muted);font-size:11px;text-decoration:none;}
      .juba-app-shell .reference-peer-chat[dir="rtl"] .reference-peer-back svg{transform:scaleX(-1);}
      .juba-app-shell .reference-peer-avatar{display:grid;place-items:center;width:32px;height:32px;flex-shrink:0;overflow:hidden;border-radius:50%;background:var(--juba-soft);color:var(--juba-green-dark);font-size:12px;font-weight:700;}
      .juba-app-shell .reference-peer-title{font-size:14px;line-height:1.4;font-weight:650;margin:0;}
      .juba-app-shell .reference-peer-subtitle{display:flex;align-items:center;gap:4px;font-size:11px;color:var(--juba-muted);margin:2px 0 0;}
      .juba-app-shell .reference-peer-history{flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;display:flex;flex-direction:column;gap:28px;padding:12px clamp(8px,5vw,64px);}
      .juba-app-shell .reference-peer-message{display:flex;flex-direction:column;align-items:flex-start;gap:8px;max-width:min(78%,440px);align-self:flex-start;}
      .juba-app-shell .reference-peer-message[data-outgoing="true"]{align-self:flex-end;align-items:flex-end;}
      .juba-app-shell .reference-peer-meta{display:flex;align-items:center;gap:8px;color:var(--juba-muted);font-size:11px;}
      .juba-app-shell .reference-peer-meta time{font-size:10px;font-variant-numeric:tabular-nums;}
      .juba-app-shell .reference-peer-bubble{padding:12px 16px;background:var(--juba-green-soft);border-radius:6px;font-size:14px;line-height:1.6;max-width:100%;}
      .juba-app-shell .reference-peer-message[data-outgoing="true"] .reference-peer-bubble{background:var(--juba-soft);}
      .juba-app-shell .reference-peer-bubble p{margin:0;white-space:pre-wrap;overflow-wrap:anywhere;text-align:start;}
      .juba-app-shell .reference-peer-composer{display:flex;align-items:center;gap:12px;flex-shrink:0;margin-inline:clamp(0px,4vw,48px);padding:8px 12px;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);}
      .juba-app-shell .reference-peer-composer input{flex:1;min-width:0;border:0;background:transparent;color:inherit;padding:8px;font-size:14px;min-height:36px;text-align:start;}
      .juba-app-shell .reference-peer-send{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:40px;padding:8px 12px;border:0;border-radius:5px;background:var(--juba-muted);color:var(--juba-card);font-size:12px;font-weight:700;}
      .juba-app-shell .reference-peer-send:disabled{opacity:.45;cursor:not-allowed;}
      .juba-app-shell .reference-peer-send:not(:disabled):hover{background:var(--juba-green-dark);}
      .juba-app-shell .reference-peer-state{display:grid;place-items:center;flex:1;min-height:160px;text-align:center;color:var(--juba-muted);font-size:14px;gap:12px;}
      .juba-app-shell .reference-peer-error{padding:12px 16px;border:1px solid var(--duo-red);border-radius:6px;color:var(--duo-red);font-size:14px;}
      .juba-app-shell .reference-peer-skeleton{height:48px;width:42%;background:var(--juba-soft);border-radius:6px;}
      @media(max-width:900px){.juba-app-shell .reference-peer-chat{height:calc(100dvh - 54px);min-height:0;padding:12px 16px 16px!important;gap:16px;}.juba-app-shell .reference-peer-history{padding:8px 0;gap:20px;}.juba-app-shell .reference-peer-message{max-width:88%;}.juba-app-shell .reference-peer-composer{margin-inline:0;gap:8px;}.juba-app-shell .reference-peer-send,.juba-app-shell .reference-peer-back{min-height:44px;}.juba-app-shell .reference-peer-composer input{font-size:16px;}}
    `}</style>
    <header className="reference-peer-header"><Link href="/friends" className="reference-peer-back" aria-label={rtl?'العودة إلى الأصدقاء':'Back to friends'}><ArrowLeft size={16}/><span>{rtl?'الأصدقاء':'Friends'}</span></Link><Avatar value={friend?.avatar} name={friend?.display_name||'?'}/><div><h1 className="reference-peer-title" dir="auto">{friend?.display_name||(rtl?'صديق التعلم':'Learning friend')}</h1><p className="reference-peer-subtitle"><Users size={12}/>{rtl?'محادثة تعلم':'Learning chat'}</p></div></header>
    <div className="reference-peer-history" role="log" aria-live="polite" aria-relevant="additions" aria-busy={loading}>
      {error&&<div className="reference-peer-error" role="alert">{error}</div>}
      {loading?<div className="reference-peer-state" role="status"><span>{rtl?'جارٍ تحميل المحادثة…':'Loading conversation…'}</span><div className="reference-peer-skeleton" aria-hidden="true"/></div>:!messages.length?<div className="reference-peer-state">{rtl?'ابدأ محادثة ودية لتعلم اللغة.':'Start a friendly language-learning conversation.'}</div>:messages.map(message=>{const outgoing=message.sender_id===user?.id;const name=outgoing?(user?.displayName||user?.username||''):(friend?.display_name||'');return <article className="reference-peer-message" data-outgoing={outgoing} key={message.id}><div className="reference-peer-meta"><Avatar value={outgoing?user?.avatar:friend?.avatar} name={name}/><span dir="auto">{name}</span><time dateTime={message.created_at}>{new Date(message.created_at).toLocaleTimeString(locale,{hour:'2-digit',minute:'2-digit'})}</time></div><div className="reference-peer-bubble"><p dir="auto">{message.content}</p></div></article>})}<div ref={bottom}/>
    </div>
    <form className="reference-peer-composer" onSubmit={event=>{event.preventDefault();void send()}}><input aria-label={rtl?'رسالتك':'Your message'} disabled={!friend||blocked} value={input} onChange={event=>setInput(event.target.value)} placeholder={rtl?'اكتب رسالة…':'Write a message…'} dir="auto"/><button type="submit" className="reference-peer-send" disabled={!input.trim()||sending||!friend||blocked}><Send size={16}/>{sending?(rtl?'جارٍ الإرسال':'Sending'):(rtl?'إرسال':'Send')}</button></form>
  </section>
}
