'use client'

import { useEffect, useState, type ReactNode } from 'react'
import Link from 'next/link'
import { useLocale } from 'next-intl'
import { MessageCircle, Search, UserPlus, Users, Check, UserMinus } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'

type Person={id:number;username:string;display_name:string;avatar?:string|null;target_language?:string;bio?:string|null}
type RequestItem={id:number;user:Person}
export default function FriendsPage(){
  const rtl=useLocale()==='ar'
  const copy=rtl?{title:'الأصدقاء',subtitle:'ابحث عن متعلمين ومارس معهم وحافظ على التواصل في رحلة اللغة.',search:'بحث',searching:'جارٍ البحث…',searchPlaceholder:'ابحث باسم المتعلم أو اسم المستخدم',friends:'أصدقاؤك في التعلم',requests:'طلبات الصداقة',incoming:'الواردة',outgoing:'المرسلة',pending:'قيد الانتظار',add:'إضافة',adding:'جارٍ الإضافة…',accept:'قبول',accepting:'جارٍ القبول…',chat:'محادثة',remove:'إزالة الصديق',empty:'لا يوجد أصدقاء بعد. ابحث عن متعلم لبدء الممارسة معًا.',noRequests:'لا توجد طلبات معلقة.',noResults:'لا توجد نتائج. جرّب اسمًا آخر.',loading:'جارٍ التحميل…',retry:'إعادة المحاولة',loadError:'تعذر تحميل مجتمع التعلم.',searchError:'تعذر البحث عن المتعلمين حاليًا.',addError:'تعذر إرسال طلب الصداقة.',acceptError:'تعذر قبول الطلب.',removeError:'تعذر إزالة الصديق.',searchHint:'اكتب حرفين على الأقل للبحث.'}:{title:'Friends',subtitle:'Find learners, practise together, and keep your language journey social.',search:'Search',searching:'Searching…',searchPlaceholder:'Search learners by name or username',friends:'Your learning friends',requests:'Friend requests',incoming:'Incoming',outgoing:'Outgoing',pending:'Pending',add:'Add',adding:'Adding…',accept:'Accept',accepting:'Accepting…',chat:'Chat',remove:'Remove friend',empty:'No friends yet. Search for another learner to start practising together.',noRequests:'No pending requests.',noResults:'No learners found. Try another name.',loading:'Loading…',retry:'Retry',loadError:'Unable to load your learning community.',searchError:'Unable to search learners right now.',addError:'Unable to send friend request.',acceptError:'Unable to accept this request.',removeError:'Unable to remove this friend.',searchHint:'Enter at least two characters to search.'}
  const [friends,setFriends]=useState<Person[]>([])
  const [incoming,setIncoming]=useState<RequestItem[]>([])
  const [outgoing,setOutgoing]=useState<RequestItem[]>([])
  const [results,setResults]=useState<Person[]>([])
  const [query,setQuery]=useState('')
  const [loading,setLoading]=useState(true)
  const [error,setError]=useState('')
  const [searching,setSearching]=useState(false)
  const [searched,setSearched]=useState(false)
  const [actionId,setActionId]=useState<number|null>(null)
  async function load(){
    setLoading(true);setError('')
    try{
      const [friendsRes,requestsRes]=await Promise.all([apiFetch('/api/social/friends'),apiFetch('/api/social/requests')])
      if(!friendsRes.ok||!requestsRes.ok)throw new Error()
      setFriends(await friendsRes.json())
      const requests=await requestsRes.json();setIncoming(requests.incoming??[]);setOutgoing(requests.outgoing??[])
    }catch{setError(copy.loadError)}finally{setLoading(false)}
  }
  useEffect(()=>{void load()},[])
  async function search(){
    if(query.trim().length<2){setResults([]);setSearched(false);return}
    setSearching(true);setError('');setSearched(false)
    try{const res=await apiFetch('/api/social/users?q='+encodeURIComponent(query.trim()));if(!res.ok)throw new Error();setResults(await res.json());setSearched(true)}catch{setError(copy.searchError)}finally{setSearching(false)}
  }
  async function addFriend(id:number){
    setActionId(id)
    try{
      const res=await apiFetch('/api/social/requests',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:id})})
      if(res.ok){setResults(prev=>prev.filter(person=>person.id!==id));await load()}
      else setError((await res.json().catch(()=>({detail:copy.addError}))).detail||copy.addError)
    }catch{setError(copy.addError)}finally{setActionId(null)}
  }
  async function accept(id:number){
    setActionId(id)
    try{const res=await apiFetch('/api/social/requests/'+id+'/accept',{method:'POST'});if(res.ok)await load();else setError(copy.acceptError)}catch{setError(copy.acceptError)}finally{setActionId(null)}
  }
  async function remove(id:number){
    setActionId(id)
    try{const res=await apiFetch('/api/social/friends/'+id,{method:'DELETE'});if(res.ok)await load();else setError(copy.removeError)}catch{setError(copy.removeError)}finally{setActionId(null)}
  }
  return <div className="juba-page-shell reference-friends" dir={rtl?'rtl':'ltr'}>
    <style>{`
      .juba-app-shell .reference-friends{display:flex;flex-direction:column;gap:24px;}
      .juba-app-shell .reference-friends-header{display:flex;align-items:center;gap:16px;min-height:100px;}
      .juba-app-shell .reference-friends-header>svg{color:var(--juba-green);flex:none;}
      .juba-app-shell .reference-friends-header h1{font-size:28px;font-weight:650;line-height:1.3;margin:0;}
      .juba-app-shell .reference-friends-header p{font-size:14px;color:var(--juba-muted);line-height:1.6;margin:6px 0 0;}
      .juba-app-shell .reference-friends-layout{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:24px;align-items:start;}
      .juba-app-shell .reference-friends-primary{display:flex;flex-direction:column;gap:24px;min-width:0;}
      .juba-app-shell .reference-friends-panel{border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);overflow:hidden;}
      .juba-app-shell .reference-friends-panel-head{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-friends-panel-head h2{font-size:14px;font-weight:650;margin:0;}
      .juba-app-shell .reference-friends-panel-head span{font-size:11px;color:var(--juba-muted);}
      .juba-app-shell .reference-friends-search{padding:16px;}
      .juba-app-shell .reference-friends-search-form{display:flex;align-items:center;gap:12px;}
      .juba-app-shell .reference-friends-search label{flex:1;min-width:0;position:relative;display:flex;align-items:center;}
      .juba-app-shell .reference-friends-search label>svg{position:absolute;inset-inline-start:12px;color:var(--juba-muted);}
      .juba-app-shell .reference-friends-search input{width:100%;padding:8px 12px;padding-inline-start:38px;}
      .juba-app-shell .reference-friends-search button{padding-inline:12px;}
      .juba-app-shell .reference-friends-hint{font-size:11px;color:var(--juba-muted);margin:8px 0 0;}
      .juba-app-shell .reference-friend-row{display:flex;align-items:center;gap:12px;padding:14px 16px;border-block-end:1px solid var(--juba-border);}
      .juba-app-shell .reference-friend-row:last-child{border:0;}
      .juba-app-shell .reference-friend-avatar{display:grid;place-items:center;width:36px;height:36px;border-radius:50%;overflow:hidden;flex:none;background:var(--juba-soft);font-size:13px;color:var(--juba-green-dark);}
      .juba-app-shell .reference-friend-copy{flex:1;min-width:0;}
      .juba-app-shell .reference-friend-copy strong{display:block;font-size:13px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
      .juba-app-shell .reference-friend-copy p{font-size:11px;color:var(--juba-muted);margin:4px 0 0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
      .juba-app-shell .reference-friend-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
      .juba-app-shell .reference-friend-actions :is(a,button){padding-inline:10px;min-height:36px;font-size:12px;}
      .juba-app-shell .reference-friends-request-heading{font-size:11px;color:var(--juba-muted);font-weight:600;margin:0;padding:12px 16px;background:var(--juba-soft);}
      .juba-app-shell .reference-friends-requests .reference-friend-row{flex-wrap:wrap;}
      .juba-app-shell .reference-friends-requests .reference-friend-actions{margin-inline-start:48px;}
      .juba-app-shell .reference-friends-empty{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:32px 16px;font-size:13px;color:var(--juba-muted);line-height:1.6;text-align:center;}
      .juba-app-shell .reference-friends-empty p{margin:0;}
      .juba-app-shell .reference-friends-error{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 16px;border:1px solid var(--duo-red);border-radius:6px;font-size:13px;flex-wrap:wrap;}
      .juba-app-shell .reference-friends-loading{display:flex;flex-direction:column;gap:12px;padding:16px;}
      .juba-app-shell .reference-friends-loading span{display:block;height:44px;border-radius:5px;background:var(--juba-soft);}
      @media(max-width:1000px){.juba-app-shell .reference-friends-layout{grid-template-columns:1fr;}.juba-app-shell .reference-friends-requests .reference-friend-actions{margin-inline-start:0;}}
      @media(max-width:640px){.juba-app-shell .reference-friends,.juba-app-shell .reference-friends-primary{gap:16px;}.juba-app-shell .reference-friends-header h1{font-size:24px;}.juba-app-shell .reference-friends-header>svg{width:32px;height:32px;}.juba-app-shell .reference-friend-row{flex-wrap:wrap;gap:8px;}.juba-app-shell .reference-friend-actions{margin-inline-start:44px;}.juba-app-shell .reference-friend-actions :is(a,button){min-height:44px;}.juba-app-shell .reference-friends-search-form{flex-wrap:wrap;}.juba-app-shell .reference-friends-search label{flex-basis:100%;}}
    `}</style>
    <header className="reference-friends-header"><Users size={40} aria-hidden="true"/><div><h1>{copy.title}</h1><p>{copy.subtitle}</p></div></header>
    {error&&<div className="reference-friends-error" role="alert"><span>{error}</span><button className="juba-secondary-button" onClick={()=>void load()} disabled={loading}>{copy.retry}</button></div>}
    <div className="reference-friends-layout"><div className="reference-friends-primary">
      <section className="reference-friends-panel"><form className="reference-friends-search" onSubmit={event=>{event.preventDefault();void search()}}><div className="reference-friends-search-form"><label><Search size={18} aria-hidden="true"/><input className="juba-input" type="search" value={query} onChange={event=>setQuery(event.target.value)} placeholder={copy.searchPlaceholder} aria-label={copy.searchPlaceholder} aria-describedby="friend-search-hint"/></label><button className="juba-primary-button" disabled={searching||query.trim().length<2}><Search size={16}/>{searching?copy.searching:copy.search}</button></div><p className="reference-friends-hint" id="friend-search-hint">{copy.searchHint}</p></form>{searching?<LoadingRows label={copy.searching}/>:searched?<div aria-live="polite">{results.length?results.map(person=><PersonRow key={person.id} person={person}><button className="juba-secondary-button" onClick={()=>void addFriend(person.id)} disabled={actionId===person.id}><UserPlus size={16}/>{actionId===person.id?copy.adding:copy.add}</button></PersonRow>):<Empty text={copy.noResults}/>}</div>:null}</section>
      <section className="reference-friends-panel"><header className="reference-friends-panel-head"><h2>{copy.friends}</h2><span>{friends.length}</span></header>{loading?<LoadingRows label={copy.loading}/>:friends.length?friends.map(person=><PersonRow person={person} key={person.id}><Link className="juba-secondary-button" href={'/friends/chat/'+person.id}><MessageCircle size={16}/>{copy.chat}</Link><button className="juba-secondary-button" onClick={()=>void remove(person.id)} disabled={actionId===person.id} title={copy.remove} aria-label={copy.remove+': '+(person.display_name||person.username)}><UserMinus size={16}/></button></PersonRow>):<Empty text={copy.empty}/>}</section>
    </div><aside className="reference-friends-panel reference-friends-requests"><header className="reference-friends-panel-head"><h2>{copy.requests}</h2><span>{incoming.length+outgoing.length}</span></header>{loading?<LoadingRows label={copy.loading}/>:<>{incoming.length>0&&<><h3 className="reference-friends-request-heading">{copy.incoming}</h3>{incoming.map(item=><PersonRow key={item.id} person={item.user}><button className="juba-primary-button" onClick={()=>void accept(item.id)} disabled={actionId===item.id}><Check size={16}/>{actionId===item.id?copy.accepting:copy.accept}</button></PersonRow>)}</>}{outgoing.length>0&&<><h3 className="reference-friends-request-heading">{copy.outgoing}</h3>{outgoing.map(item=><PersonRow key={'out-'+item.id} person={item.user}><span className="juba-badge">{copy.pending}</span></PersonRow>)}</>}{!incoming.length&&!outgoing.length&&<Empty text={copy.noRequests}/>}</>}</aside></div>
  </div>
}
function PersonRow({person,children}:{person:Person;children:ReactNode}){return <div className="reference-friend-row"><span className="reference-friend-avatar">{person.avatar?<AuthAvatarImage avatar={person.avatar} alt="" width={36} height={36} className="h-full w-full object-cover"/>:(person.display_name||person.username||'?')[0].toUpperCase()}</span><div className="reference-friend-copy"><strong dir="auto">{person.display_name||person.username}</strong><p><bdi>@{person.username}</bdi>{person.target_language?' · '+person.target_language:''}</p></div><div className="reference-friend-actions">{children}</div></div>}
function Empty({text}:{text:string}){return <div className="reference-friends-empty"><Users size={24} aria-hidden="true"/><p>{text}</p></div>}
function LoadingRows({label}:{label:string}){return <div className="reference-friends-loading" role="status" aria-label={label}><span aria-hidden="true"/><span aria-hidden="true"/><span aria-hidden="true"/></div>}
