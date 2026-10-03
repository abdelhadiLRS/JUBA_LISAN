'use client'
import {useState,useRef,useEffect,useCallback} from 'react'
import {useRouter} from 'next/navigation'
import Image from 'next/image'
import Link from 'next/link'
import {useTranslations,useLocale} from 'next-intl'
import {apiFetch} from '@/lib/api'
import {useAuthStore} from '@/store/auth'
import {useProgressStore} from '@/store/progress'
import {useLanguageStore} from '@/store/language'
import {ConfirmDialog} from '@/components/ui/confirm-dialog'
import {AudioPlayer} from '@/components/ui/AudioPlayer'
import {MaintenanceGate} from '@/components/billing/MaintenanceBanner'
import {PaywallBanner} from '@/components/billing/PaywallBanner'
import {FreemiumQuotaBanner} from '@/components/billing/FreemiumQuotaBanner'
import {WordTooltip,useWordSave} from '@/components/ui/WordTooltip'
import {PageLoading} from '@/components/ui/page-loading'
import {TargetLanguageText} from '@/components/TargetLanguageText'
import {AuthAvatarImage} from '@/components/AuthAvatarImage'
import {MemorySavedToast} from '@/components/memory/MemorySavedToast'
import {useTransientToast} from '@/hooks/useTransientToast'
import {useAccountQuota} from '@/hooks/useAccountQuota'
import {readSseData} from '@/lib/sse'
import {Trophy,MessageCircle} from 'lucide-react'

interface Message{role:'user'|'assistant';content:string}
interface Conversation{id:number;title:string;source:string;created_at:string;updated_at:string}
interface ChatEvent{conversation_id?:number;token?:string;response_reset?:boolean;error?:string;done?:boolean;memory_updated?:boolean}
interface Friend{id:number;username:string;display_name:string;avatar?:string|null}
export default function ChatPage(){
 const t=useTranslations('chat'),common=useTranslations('common'),lang=useTranslations('targetLanguages'),ar=useLocale().startsWith('ar'),router=useRouter()
 const user=useAuthStore(s=>s.user),xp=useProgressStore(s=>s.xp),streak=useProgressStore(s=>s.streak),stats=useProgressStore(s=>s.gameStats)
 const activeLanguage=useLanguageStore(s=>s.activeLanguage),target=activeLanguage?.code??'en-GB'
 const {selectedWord,tooltipPos,saveState,handleTextSelection,handleSaveWord,dismissTooltip}=useWordSave()
 const [friends,setFriends]=useState<Friend[]>([]),[conversations,setConversations]=useState<Conversation[]>([]),[activeId,setActiveId]=useState<number|null>(null)
 const [messages,setMessages]=useState<Message[]>([]),[input,setInput]=useState(''),[sending,setSending]=useState(false),[warn,setWarn]=useState(false)
 const [error,setError]=useState(''),[loadingConvs,setLoadingConvs]=useState(true),[convError,setConvError]=useState(false),[loadingMsgs,setLoadingMsgs]=useState(false)
 const [sidebar,setSidebar]=useState(false),[deletePending,setDeletePending]=useState<number|null>(null),[blocked,setBlocked]=useState(false),[resetAt,setResetAt]=useState<string|null>(null)
 const {visible:memoryToast,announcementId:memoryToastId,show:showMemoryToast}=useTransientToast()
 const {exhausted,refresh:refreshQuota}=useAccountQuota('chat')
 const bottom=useRef<HTMLDivElement>(null),inputRef=useRef<HTMLInputElement>(null),epoch=useRef(0),sendLock=useRef(false),abort=useRef<AbortController|null>(null)
 const accuracy=stats.questionsAnswered>0?Math.round(stats.correctAnswers/stats.questionsAnswered*100):0
 useEffect(()=>{setSidebar(window.innerWidth>=1024)},[])
 useEffect(()=>{bottom.current?.scrollIntoView({behavior:'smooth'})},[messages])
 useEffect(()=>{if(!sending){setWarn(false);return}const timer=setTimeout(()=>setWarn(true),60000);return()=>clearTimeout(timer)},[sending])
 useEffect(()=>{let active=true;void apiFetch('/api/social/friends').then(async res=>{if(res.ok){const data=await res.json();if(active)setFriends(Array.isArray(data)?data.slice(0,6):[])}}).catch(()=>{});return()=>{active=false}},[])
 const loadConversations=useCallback(async()=>{try{const res=await apiFetch('/api/chat/conversations');if(res.ok)return await res.json() as Conversation[]}catch{}return null},[])
 async function selectConversation(id:number){
  abort.current?.abort();const version=++epoch.current;setSending(false);dismissTooltip();setActiveId(id);setMessages([]);setError('');setLoadingMsgs(true)
  if(window.innerWidth<1024)setSidebar(false)
  try{const res=await apiFetch(`/api/chat/conversations/${id}/messages`);if(!res.ok)throw new Error();const data=await res.json();if(version===epoch.current)setMessages(data.messages||[])}catch{if(version===epoch.current)setError(common('error'))}finally{if(version===epoch.current)setLoadingMsgs(false)}
 }
 useEffect(()=>{
  abort.current?.abort();const version=++epoch.current;setSending(false);setBlocked(false);setResetAt(null);setConvError(false);setLoadingConvs(true);setActiveId(null);setMessages([])
  void loadConversations().then(data=>{if(version!==epoch.current)return;if(data===null){setConvError(true);return}setConversations(data);if(data.length)void selectConversation(data[0].id)}).finally(()=>{if(version===epoch.current||version+1===epoch.current)setLoadingConvs(false)})
  return()=>{epoch.current++;abort.current?.abort()}
 // Only reload conversations on a language transition.
 // eslint-disable-next-line react-hooks/exhaustive-deps
 },[target,loadConversations])
 function newChat(){abort.current?.abort();epoch.current++;dismissTooltip();setSending(false);setActiveId(null);setMessages([]);setError('');if(window.innerWidth<1024)setSidebar(false);requestAnimationFrame(()=>inputRef.current?.focus())}
 function voice(){sessionStorage.setItem('voice_context',JSON.stringify({messages:messages.filter(item=>item.content.trim()).slice(-20)}));router.push('/conversation')}
 async function removeConversation(id:number){
  const res=await apiFetch(`/api/chat/conversations/${id}`,{method:'DELETE'});if(!res.ok){setError(common('error'));return}
  setDeletePending(null);const values=await loadConversations();if(values===null){setConvError(true);return}setConversations(values)
  if(activeId===id){if(values.length)void selectConversation(values[0].id);else newChat()}
 }
 async function sendMessage(){
  if(!input.trim()||sendLock.current||loadingMsgs||blocked||exhausted||input.trim().length>2000)return
  sendLock.current=true;const controller=new AbortController();abort.current=controller
  const version=epoch.current,text=input.trim(),previous=messages;let done=false
  setInput('');setError('');setMessages([...previous,{role:'user',content:text}]);setSending(true)
  try{
   const res=await apiFetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text,conversation_id:activeId}),signal:controller.signal})
   if(!res.ok){const data=await res.json().catch(()=>({}));if(res.status===402){
     if(version===epoch.current){setBlocked(true);setResetAt(typeof data.detail?.resets_at==='string'?data.detail.resets_at:null);void refreshQuota()}
     throw new Error(ar?'وصلت إلى حد حصة المعلم. راجع موعد التجديد أو باقتك.':'Tutor allowance reached. Check your reset time or plan.')
    }throw new Error(typeof data.detail==='string'?data.detail:common('error'))}
   if(!res.body)throw new Error(t('errorMessage'))
   let content=''
   if(version===epoch.current)setMessages([...previous,{role:'user',content:text},{role:'assistant',content:''}])
   for await(const event of readSseData<ChatEvent>(res.body)){
    if(version!==epoch.current)break
    if(event.response_reset){dismissTooltip();content=''}
    if(event.token)content+=event.token
    if(event.response_reset||event.token)setMessages([...previous,{role:'user',content:text},{role:'assistant',content}])
    if(event.error)throw new Error(event.error)
    if(event.conversation_id)setActiveId(event.conversation_id)
    if(event.memory_updated)showMemoryToast()
    if(event.done){done=true;void refreshQuota();const values=await loadConversations();if(values&&version===epoch.current)setConversations(values)}
   }
   if(!done&&!controller.signal.aborted)throw new Error(t('errorMessage'))
  }catch(err){if(version===epoch.current&&!controller.signal.aborted){setError(err instanceof Error?err.message:t('errorMessage'));if(!done){setMessages(previous);setInput(text)}}}
  finally{sendLock.current=false;if(version===epoch.current){setSending(false);inputRef.current?.focus()}}
 }
 return <MaintenanceGate><style>{`
 .juba-mobile-chat{display:flex;height:100%;min-height:0;overflow:hidden;background:var(--juba-card,var(--duo-card));color:var(--juba-ink,var(--duo-ink))}
 .juba-mobile-chat .chat-conversations-sidebar{width:228px;flex:none;border-inline-end:1px solid var(--juba-border,var(--duo-line));display:flex;flex-direction:column}
 .juba-mobile-chat .chat-profile-rail{width:264px;flex:none;border-inline-start:1px solid var(--juba-border,var(--duo-line));padding:16px;overflow-y:auto}
 .juba-mobile-chat .chat-profile-panel{border:1px solid var(--juba-border,var(--duo-line));border-radius:10px;padding:16px;margin-block-end:14px}
 .juba-mobile-chat .chat-profile-metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;text-align:center;margin-block-start:16px;font-variant-numeric:tabular-nums}
 .juba-mobile-chat .chat-profile-metrics b,.juba-mobile-chat .chat-profile-metrics small{display:block}
 .juba-mobile-chat .chat-profile-metrics small{font-size:11px;color:var(--juba-muted,var(--duo-muted))}
 .juba-mobile-chat .chat-row{display:flex;align-items:flex-end;gap:8px;margin-block-end:12px}
 .juba-mobile-chat .chat-row[data-role=user]{flex-direction:row-reverse}
 .juba-mobile-chat .chat-bubble{border:1px solid var(--juba-border,var(--duo-line));border-radius:10px;padding:11px 14px;line-height:1.55}
 .juba-mobile-chat .chat-row[data-role=user] .chat-bubble{background:var(--juba-green-soft,var(--duo-soft))}
 .juba-mobile-chat .chat-messages{padding:22px 28px}
 .juba-mobile-chat button:focus-visible,.juba-mobile-chat input:focus-visible{outline:2px solid var(--duo-green);outline-offset:2px}
 @media(max-width:1023px){.juba-mobile-chat .chat-profile-rail{display:none}.juba-mobile-chat .chat-conversations-sidebar{position:fixed;inset-block:56px 0;inset-inline-start:0;z-index:20;width:min(82vw,292px);background:var(--duo-card)}.juba-mobile-chat .chat-messages{padding:18px 14px}}
 `}</style><div className="juba-page-shell juba-mobile-chat w-full max-w-[1480px] mx-auto"><MemorySavedToast visible={memoryToast} announcementId={memoryToastId}/>
 {sidebar&&<><div className="fixed inset-x-0 top-14 bottom-0 z-10 bg-black/40 lg:hidden" onClick={()=>setSidebar(false)}/><aside className="chat-conversations-sidebar"><div className="flex min-h-[56px] items-center justify-between border-b border-[var(--duo-line)] px-4"><span>{t('conversations')}</span><button onClick={newChat}>+ {t('newConversation')}</button></div><div className="flex-1 overflow-y-auto">{loadingConvs?<PageLoading fullScreen={false}/>:convError?<div className="p-4"><p>{common('error')}</p><button onClick={()=>void loadConversations().then(data=>{if(data){setConversations(data);setConvError(false)}})}>{common('retry')}</button></div>:!conversations.length?<p className="p-4">{t('noConversation')}</p>:conversations.map(conv=><div key={conv.id} className={`flex items-center border-b border-[var(--duo-line)] ${activeId===conv.id?'bg-[var(--duo-soft)]':''}`}><button className="min-h-11 flex-1 truncate p-3 text-start" onClick={()=>void selectConversation(conv.id)}>{conv.source==='voice'?'🎤 ':''}{conv.title}</button><button className="min-h-11 px-3" onClick={()=>setDeletePending(conv.id)} aria-label={t('deleteTitle')}>✕</button></div>)}</div></aside></>}
 <div className="flex min-w-0 flex-1 flex-col overflow-hidden"><header className="flex min-h-[56px] items-center gap-3 border-b border-[var(--duo-line)] px-5"><button className="min-h-11 px-2" onClick={()=>setSidebar(v=>!v)} aria-label={sidebar?t('toggleSidebarHide'):t('toggleSidebarShow')}>☰</button><span className="truncate">{activeId?conversations.find(conv=>conv.id===activeId)?.title??t('title'):t('newConversation')}</span>{sending?<div className="ms-auto text-sm"><span>{t('thinking')}</span>{warn&&<p>{t('takingLonger')}</p>}</div>:messages.length>0&&<button className="ms-auto min-h-11" onClick={voice}>{t('continueInVoice')}</button>}</header>
 <FreemiumQuotaBanner feature="chat"/><div className="chat-messages min-h-0 flex-1 overflow-y-auto">{loadingMsgs?<PageLoading fullScreen={false}/>:!messages.length?<div className="flex h-full flex-col items-center justify-center gap-3 text-center"><p>{t('title')}</p><p>{t('subtitle',{language:lang(target)})}</p></div>:messages.map((item,index)=><div className="chat-row" data-role={item.role} key={index}><div className="h-8 w-8 shrink-0 overflow-hidden rounded-full">{item.role==='assistant'?<Image src="/logo_head.png" alt="Tutor" width={32} height={32}/>:user?.avatar?<AuthAvatarImage avatar={user.avatar} alt="" width={32} height={32}/>:<span>{(user?.displayName||user?.username||'?')[0]}</span>}</div><div className="max-w-[78%]"><TargetLanguageText as="div" languageCode={target} className="chat-bubble word-selectable" onPointerUp={item.role==='assistant'&&!(sending&&index===messages.length-1)?()=>handleTextSelection(item.content):undefined}>{item.content||(sending?'▌':'')}</TargetLanguageText>{item.role==='assistant'&&item.content&&!(sending&&index===messages.length-1)&&<AudioPlayer text={item.content} size="sm"/>}</div></div>)}
 {error&&<div role="alert" className="my-4 border border-[var(--duo-red)] p-3"><p>{error}</p>{resetAt&&<p>{ar?'التجديد':'Resets'}: {new Date(resetAt).toLocaleString()}</p>}{blocked&&<Link href="/settings/subscription" className="underline">{ar?'الباقة والحصص':'Plan and allowances'}</Link>}</div>}<div ref={bottom}/></div>
 <footer className="border-t border-[var(--duo-line)] p-4">{blocked||exhausted?<><PaywallBanner feature="chat" compact/><button className="min-h-11 mt-2" onClick={()=>void refreshQuota().then(data=>{if(data&&(!data.metered||data.features.chat.remaining>0)){setBlocked(false);setError('')}})}>{common('retry')}</button></>:<><div className="flex gap-2"><input ref={inputRef} value={input} onChange={e=>setInput(e.target.value)} maxLength={2000} disabled={sending||loadingMsgs} placeholder={t('placeholder')} onKeyDown={e=>{if(e.key==='Enter'&&!e.shiftKey)void sendMessage()}} className="min-h-11 min-w-0 flex-1 rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] px-3"/><button disabled={sending||!input.trim()||loadingMsgs} onClick={()=>void sendMessage()} className="min-h-11 rounded-[10px] bg-[var(--duo-green)] px-5 font-semibold text-[var(--duo-card)]">{sending?'...':t('send')}</button></div><p className="mt-2 text-xs">{t('enterToSend')} · {input.length}/2000</p></>}</footer></div>
 <aside className="chat-profile-rail" aria-label="Profile"><section className="chat-profile-panel"><div className="flex flex-col items-center text-center">{user?.avatar?<AuthAvatarImage avatar={user.avatar} alt="" width={68} height={68} className="rounded-full"/>:<MessageCircle size={30}/>}<strong className="mt-3">{user?.displayName||user?.username}</strong><span className="text-sm">{lang(target)}</span></div><div className="chat-profile-metrics"><div><b>{xp}</b><small>{t('xp')}</small></div><div><b>{streak}</b><small>{t('streak')}</small></div><div><b>{accuracy}%</b><small>{t('accuracy')}</small></div></div></section><section className="chat-profile-panel"><Trophy size={24}/><button className="mt-3 text-start" onClick={voice}>{t('continueInVoice')}</button></section><section className="chat-profile-panel"><h3>{ar?'الأصدقاء':'Friends'}</h3>{friends.map(friend=><button key={friend.id} className="flex min-h-11 w-full items-center gap-2 border-t border-[var(--duo-line)] py-2 text-start" onClick={()=>router.push('/friends/chat/'+friend.id)}>{friend.avatar&&<AuthAvatarImage avatar={friend.avatar} alt="" width={32} height={32}/>}<span>{friend.display_name||friend.username}</span></button>)}</section></aside>
 <ConfirmDialog open={deletePending!==null} title={t('deleteTitle')} message={t('deleteMessage')} confirmLabel={t('deleteConfirm')} danger onConfirm={()=>deletePending!==null&&void removeConversation(deletePending)} onCancel={()=>setDeletePending(null)}/>
 {selectedWord&&<WordTooltip word={selectedWord} pos={tooltipPos} saveState={saveState} onSave={()=>handleSaveWord()} onDismiss={dismissTooltip} labels={{saveWord:common('saveWord'),wordSaved:common('wordSaved'),wordSaveError:common('wordSaveError')}}/>}</div></MaintenanceGate>
}
