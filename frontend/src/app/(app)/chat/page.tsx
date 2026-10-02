'use client'

import { useState, useRef, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useProgressStore } from '@/store/progress'
import { useLanguageStore } from '@/store/language'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { MaintenanceGate } from '@/components/billing/MaintenanceBanner'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { useFreemiumStore } from '@/store/freemium'
import { useConfigStore } from '@/store/config'
import { isSubscribed, isFreemiumTrialActive } from '@/store/auth'
import { WordTooltip, useWordSave } from '@/components/ui/WordTooltip'
import { PageLoading } from '@/components/ui/page-loading'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'
import { MemorySavedToast } from '@/components/memory/MemorySavedToast'
import { useTransientToast } from '@/hooks/useTransientToast'
import { readSseData } from '@/lib/sse'
import { Trophy, MessageCircle } from 'lucide-react'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface Conversation {
  id: number
  title: string
  source: string
  created_at: string
  updated_at: string
}

interface ChatSseEvent {
  conversation_id?: number
  token?: string
  response_reset?: boolean
  error?: string
  done?: boolean
  memory_updated?: boolean
}

interface FriendItem {
  id: number
  username: string
  display_name: string
  avatar?: string | null
}

export default function ChatPage() {
  const t = useTranslations('chat')
  const tCommon = useTranslations('common')
  const tLang = useTranslations('targetLanguages')
  const router = useRouter()
  const user = useAuthStore((s) => s.user)
  const xp = useProgressStore((s) => s.xp)
  const streak = useProgressStore((s) => s.streak)
  const gameStats = useProgressStore((s) => s.gameStats)
  const [friends, setFriends] = useState<FriendItem[]>([])
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const {
    selectedWord,
    tooltipPos,
    saveState,
    handleTextSelection,
    handleSaveWord,
    dismissTooltip,
  } = useWordSave()
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [sendingWarn, setSendingWarn] = useState(false)
  const sendingTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const [error, setError] = useState('')
  const [loadingConvs, setLoadingConvs] = useState(true)
  const [convLoadError, setConvLoadError] = useState(false)
  const [loadingMsgs, setLoadingMsgs] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [deletePending, setDeletePending] = useState<number | null>(null)
  const {
    visible: memoryToast,
    announcementId: memoryToastId,
    show: showMemoryToast,
  } = useTransientToast()
  const bottomRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const targetLanguageCode = activeLanguage?.code ?? 'en-GB'

  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const freemiumStatus = useFreemiumStore((s) => s.status)
  const fetchFreemium = useFreemiumStore((s) => s.fetchStatus)
  const decrementFreemium = useFreemiumStore((s) => s.decrement)
  const accuracy = gameStats.questionsAnswered > 0 ? Math.round((gameStats.correctAnswers / gameStats.questionsAnswered) * 100) : 0
  const freemiumExhausted =
    stripeEnabled &&
    !isSubscribed(user, stripeEnabled) &&
    !isFreemiumTrialActive(user, stripeEnabled) &&
    freemiumStatus &&
    freemiumStatus.chat_remaining <= 0

  useEffect(() => {
    if (stripeEnabled && !isSubscribed(user, stripeEnabled)) {
      fetchFreemium()
    }
  }, [stripeEnabled, user, fetchFreemium])

  useEffect(() => {
    let cancelled = false
    apiFetch('/api/social/friends').then(async (res) => {
      if (!res.ok) return
      const data = await res.json()
      if (!cancelled) setFriends(Array.isArray(data) ? data.slice(0, 6) : [])
    }).catch(() => {
      if (!cancelled) setFriends([])
    })
    return () => { cancelled = true }
  }, [])

  const scrollBottom = useCallback(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  useEffect(() => {
    scrollBottom()
  }, [messages, scrollBottom])

  // Open sidebar by default only on desktop
  useEffect(() => {
    setSidebarOpen(window.innerWidth >= 1024)
  }, [])

  // Warn if LLM takes longer than 60 s
  useEffect(() => {
    if (sending) {
      setSendingWarn(false)
      sendingTimerRef.current = setTimeout(() => setSendingWarn(true), 60_000)
    } else {
      if (sendingTimerRef.current) clearTimeout(sendingTimerRef.current)
      setSendingWarn(false)
    }
    return () => {
      if (sendingTimerRef.current) clearTimeout(sendingTimerRef.current)
    }
  }, [sending])

  const loadConversations = useCallback(async () => {
    try {
      const res = await apiFetch('/api/chat/conversations')
      if (res.ok) {
        const data: Conversation[] = await res.json()
        setConversations(data)
        return data
      }
    } catch {
      /* ignore */
    }
    return null
  }, [])

  // Load conversations on mount, auto-select the most recent
  useEffect(() => {
    async function init() {
      setConvLoadError(false)
      setLoadingConvs(true)
      const data = await loadConversations()
      if (data === null) {
        setConvLoadError(true)
        setLoadingConvs(false)
        return
      }
      if (data.length > 0) {
        selectConversation(data[0].id)
      } else {
        setActiveId(null)
        setMessages([])
      }
      setLoadingConvs(false)
    }
    init()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeLanguage?.code])

  async function selectConversation(id: number) {
    dismissTooltip()
    if (window.innerWidth < 1024) setSidebarOpen(false)
    setActiveId(id)
    setMessages([])
    setError('')
    setLoadingMsgs(true)
    try {
      const res = await apiFetch(`/api/chat/conversations/${id}/messages`)
      if (res.ok) {
        const data = await res.json()
        setMessages(data.messages || [])
      }
    } catch {
      /* ignore */
    } finally {
      setLoadingMsgs(false)
    }
  }

  async function newChat() {
    // Don't create — let the first message auto-create the conversation
    dismissTooltip()
    setActiveId(null)
    setMessages([])
    setError('')
    if (window.innerWidth < 1024) setSidebarOpen(false)
    requestAnimationFrame(() => inputRef.current?.focus())
  }

  function continueInVoice() {
    const context = messages
      .filter((m) => m.content.trim().length > 0)
      .slice(-20)
    // Only pass the message context — no conversation_id.
    // The voice session will create its own new conversation record so the
    // original text chat stays clean and the two appear as separate entries
    // in the sidebar (the voice one gets the 🎤 icon).
    sessionStorage.setItem(
      'voice_context',
      JSON.stringify({
        messages: context,
      })
    )
    router.push('/conversation')
  }

  async function deleteConversation(id: number) {
    await apiFetch(`/api/chat/conversations/${id}`, { method: 'DELETE' })
    setDeletePending(null)
    const updated = await loadConversations()
    if (updated === null) {
      setConvLoadError(true)
      return
    }
    if (activeId === id) {
      if (updated.length > 0) {
        selectConversation(updated[0].id)
      } else {
        setActiveId(null)
        setMessages([])
      }
    }
  }

  async function sendMessage() {
    if (!input.trim() || sending) return
    const text = input.trim()
    setInput('')
    setError('')
    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setSending(true)

    try {
      const res = await apiFetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, conversation_id: activeId }),
      })

      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || `Error ${res.status}`)
      }

      let assistantContent = ''
      let streamCompleted = false
      setMessages((prev) => [...prev, { role: 'assistant', content: '' }])

      if (!res.body) throw new Error(t('errorMessage'))
      for await (const data of readSseData<ChatSseEvent>(res.body)) {
        if (data.conversation_id && !activeId) {
          setActiveId(data.conversation_id)
          loadConversations().then((list) => list && setConversations(list))
        }
        if (data.response_reset) {
          dismissTooltip()
          assistantContent = ''
          setMessages((prev) => {
            const copy = [...prev]
            copy[copy.length - 1] = { role: 'assistant', content: '' }
            return copy
          })
        }
        if (data.token) {
          assistantContent += data.token
          setMessages((prev) => {
            const copy = [...prev]
            copy[copy.length - 1] = {
              role: 'assistant',
              content: assistantContent,
            }
            return copy
          })
        }
        if (data.error) {
          streamCompleted = true
          setError(data.error)
        }
        if (data.done) {
          streamCompleted = true
          if (
            !isSubscribed(user, stripeEnabled) &&
            !isFreemiumTrialActive(user, stripeEnabled)
          ) {
            decrementFreemium('chat_remaining')
          }
          loadConversations().then((list) => list && setConversations(list))
        }
        if (data.memory_updated) showMemoryToast()
      }
      if (!streamCompleted) throw new Error(t('errorMessage'))
    } catch (e) {
      setError(e instanceof Error ? e.message : t('errorMessage'))
    } finally {
      setSending(false)
      inputRef.current?.focus()
    }
  }

  return (
    <MaintenanceGate>
      <style>{`
        .juba-mobile-chat .juba-chat-profile-rail{width:284px!important;flex:none!important;border-inline-start:1px solid var(--duo-line)!important;background:var(--duo-card)!important;padding:0 14px 18px!important;overflow-y:auto!important;position:sticky!important;top:0!important;height:100%!important}
        .juba-mobile-chat .juba-chat-profile-card{border:1px solid var(--duo-line)!important;border-radius:12px!important;background:var(--duo-card)!important;overflow:hidden!important;margin-bottom:14px!important}
        .juba-mobile-chat .juba-chat-profile-hero{display:flex!important;flex-direction:column!important;align-items:center!important;text-align:center!important;padding:22px 12px 13px!important}
        .juba-mobile-chat .juba-chat-profile-photo{width:104px!important;height:104px!important;border-radius:50%!important;overflow:hidden!important;border:4px solid var(--duo-card)!important;box-shadow:0 0 0 1px var(--duo-line)!important;background:var(--duo-soft)!important;display:grid!important;place-items:center!important;color:var(--duo-muted)!important}
        .juba-mobile-chat .juba-chat-profile-photo img{width:100%!important;height:100%!important;object-fit:cover!important}
        .juba-mobile-chat .juba-chat-profile-hero strong{margin-top:9px!important;color:var(--duo-ink)!important;font-size:15px!important}
        .juba-mobile-chat .juba-chat-profile-hero span{margin-top:3px!important;color:var(--duo-muted)!important;font-size:9px!important}
        .juba-mobile-chat .juba-chat-profile-metrics{display:grid!important;grid-template-columns:repeat(3,1fr)!important;border-top:1px solid var(--duo-line)!important}
        .juba-mobile-chat .juba-chat-profile-metrics div{display:flex!important;flex-direction:column!important;align-items:center!important;gap:2px!important;padding:10px 2px!important;border-inline-end:1px solid var(--duo-line)!important}
        .juba-mobile-chat .juba-chat-profile-metrics div:last-child{border-inline-end:0!important}
        .juba-mobile-chat .juba-chat-profile-metrics b{color:#58a91b!important;font-size:14px!important}
        .juba-mobile-chat .juba-chat-profile-metrics small{color:var(--duo-muted)!important;font-size:8px!important}
        .juba-mobile-chat .juba-chat-side-card{border:1px solid var(--duo-line)!important;border-radius:12px!important;background:var(--duo-card)!important;padding:16px!important;margin-bottom:14px!important}
        .juba-mobile-chat .juba-chat-side-card-head{display:flex!important;align-items:center!important;justify-content:space-between!important;gap:8px!important}
        .juba-mobile-chat .juba-chat-side-card-head h3{margin:3px 0 0!important;color:var(--duo-ink)!important;font-size:13px!important;font-weight:800!important}
        .juba-mobile-chat .juba-chat-side-label{color:var(--duo-muted)!important;font-size:9px!important;font-weight:800!important;text-transform:uppercase!important;letter-spacing:.04em!important}
        .juba-mobile-chat .juba-chat-achievement{display:flex!important;gap:10px!important;align-items:center!important;margin-top:13px!important}
        .juba-mobile-chat .juba-chat-achievement-icon{width:46px!important;height:46px!important;border-radius:11px!important;background:#eef9df!important;color:#58a91b!important;display:grid!important;place-items:center!important;flex:none!important}
        .juba-mobile-chat .juba-chat-achievement strong{display:block!important;color:var(--duo-ink)!important;font-size:10px!important}
        .juba-mobile-chat .juba-chat-achievement span{display:block!important;color:var(--duo-muted)!important;font-size:8px!important;margin-top:3px!important}
        .juba-mobile-chat .juba-chat-friends-list{margin-top:8px!important}
        .juba-mobile-chat .juba-chat-friends-empty{display:block!important;padding:12px 0!important;color:var(--duo-muted)!important;font-size:9px!important}
        .juba-mobile-chat .juba-chat-friend{display:flex!important;align-items:center!important;gap:9px!important;width:100%!important;padding:8px 0!important;border:0!important;border-top:1px solid #f0f0f0!important;background:var(--duo-card)!important;text-align:start!important}
        .juba-mobile-chat .juba-chat-friend-avatar{width:32px!important;height:32px!important;border-radius:50%!important;overflow:hidden!important;background:#f1f3f0!important;display:grid!important;place-items:center!important;color:#888!important;font-size:9px!important;font-weight:800!important;flex:none!important}
        .juba-mobile-chat .juba-chat-friend-avatar img{width:100%!important;height:100%!important;object-fit:cover!important}
        .juba-mobile-chat .juba-chat-friend-copy{min-width:0!important;display:flex!important;flex-direction:column!important;gap:2px!important}
        .juba-mobile-chat .juba-chat-friend-copy strong{font-size:9px!important;color:var(--duo-ink)!important;overflow:hidden!important;text-overflow:ellipsis!important;white-space:nowrap!important}
        .juba-mobile-chat .juba-chat-friend-copy small{font-size:8px!important;color:var(--duo-muted)!important}
        @media (max-width:1180px){.juba-mobile-chat .juba-chat-profile-rail{width:245px!important}}
        @media (max-width:1023px){.juba-mobile-chat .juba-chat-profile-rail{display:none!important}}

        /* Reference fidelity pass 5 — chat finishing */
        .juba-mobile-chat .chat-conversations-sidebar{overflow:hidden!important}
        .juba-mobile-chat .chat-conversations-sidebar .group{transition:background-color .16s ease,border-color .16s ease!important}
        .juba-mobile-chat .word-selectable{box-shadow:0 1px 1px rgba(30,50,20,.025)!important}
        .juba-mobile-chat .word-selectable.bg-\\[var\\(--duo-green\\)\\]{box-shadow:0 1px 1px rgba(50,100,30,.05)!important}
        .juba-mobile-chat .juba-chat-profile-rail{align-self:stretch!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{overflow:hidden!important}
        .juba-mobile-chat .juba-chat-side-card-head{padding-top:10px!important;padding-bottom:8px!important}
        .juba-mobile-chat .juba-chat-friend{transition:background .15s ease!important}
        .juba-mobile-chat .juba-chat-friend:hover{background:#f8fbf6!important}
        .juba-mobile-chat .border-t-2.border-\\[var\\(--duo-line\\)\\]{box-shadow:0 -1px 0 rgba(237,240,234,.35)!important}
        .juba-mobile-chat input{outline:none!important}
        @media (max-width:1023px){
          .juba-mobile-chat .juba-chat-profile-rail{display:none!important}
          .juba-mobile-chat .chat-conversations-sidebar{box-shadow:4px 0 18px rgba(30,50,20,.05)!important}
        }
        /* Reference fidelity pass 6 — final chat surface polish */
        .juba-mobile-chat{background:var(--duo-card)!important}
        .juba-mobile-chat .chat-conversations-sidebar{border-color:var(--duo-line)!important}
        .juba-mobile-chat>div.flex.flex-1>div:first-child{border-color:var(--duo-line)!important;background:var(--duo-card)!important}
        .juba-mobile-chat .word-selectable{border-radius:10px!important}
        .juba-mobile-chat .juba-chat-profile-rail{background:var(--duo-card)!important;border-color:var(--duo-line)!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border-color:var(--duo-line)!important;box-shadow:0 1px 2px rgba(30,50,20,.025)!important}
        .juba-mobile-chat .juba-chat-profile-card:hover,.juba-mobile-chat .juba-chat-side-card:hover{box-shadow:0 3px 10px rgba(30,50,20,.04)!important}
        .juba-mobile-chat input:focus-visible,.juba-mobile-chat button:focus-visible{outline:2px solid #58cc02!important;outline-offset:2px!important}

        /* Reference shell reconciliation — shared page geometry */
        .juba-mobile-chat{background:transparent!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border-radius:10px!important}
        .juba-mobile-chat .chat-conversations-sidebar .group{border-radius:0!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{box-shadow:0 1px 2px rgba(30,50,20,.025)!important}
        .juba-mobile-chat .juba-chat-profile-card:hover,.juba-mobile-chat .juba-chat-side-card:hover{box-shadow:0 2px 8px rgba(30,50,20,.035)!important}
        .juba-mobile-chat .chat-conversations-sidebar .group{transition:background-color .15s ease,border-color .15s ease!important}
        .juba-mobile-chat .chat-conversations-sidebar .group:hover{transform:none!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{max-width:960px!important}
        .juba-mobile-chat .border-t.border-\\[var\\(--duo-line\\)\\]{max-width:960px!important}
        @media(max-width:1023px){.juba-mobile-chat .chat-conversations-sidebar{box-shadow:4px 0 16px rgba(30,50,20,.045)!important}}
        
        /* Reference fidelity pass 30 — final chat geometry consolidation */
        .juba-mobile-chat .chat-conversations-sidebar{width:250px!important;border-right:1px solid #e8ede5!important}
        .juba-mobile-chat .chat-conversations-sidebar>div:first-child{height:60px!important;min-height:60px!important;padding:0 15px!important}
        .juba-mobile-chat .chat-conversations-sidebar .group{min-height:48px!important;padding:8px 13px!important;border-bottom:1px solid #f0f2ee!important;border-inline-start:3px solid transparent!important}
        .juba-mobile-chat .chat-conversations-sidebar .group.bg-\\[var\\(--duo-line\\)\\]{background:#edf8e6!important;border-inline-start-color:#58cc02!important}
        .juba-mobile-chat>div.flex.flex-1>div:first-child{height:60px!important;min-height:60px!important;padding:0 18px!important;border-bottom:1px solid #e8ede5!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{max-width:960px!important;padding:22px 28px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4>div.flex.items-end{margin-bottom:10px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4 .h-8.w-8{width:30px!important;height:30px!important;border:0!important;box-shadow:0 0 0 1px #e7ebe4!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4 .max-w-\\[72\\%\\].min-w-\\[8rem\\]{min-width:0!important;max-width:72%!important}
        .juba-mobile-chat .border-t.border-\\[var\\(--duo-line\\)\\]{max-width:960px!important;width:100%!important;margin:0 auto!important;padding:11px 24px 14px!important;border-top:1px solid #e8ede5!important}
        .juba-mobile-chat input{height:42px!important;padding:10px 13px!important;border-radius:10px!important}
        .juba-mobile-chat .juba-chat-profile-rail{width:276px!important;min-width:276px!important;padding:14px!important;border-inline-start:1px solid #e8ede5!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border-radius:11px!important}
        .juba-mobile-chat .juba-chat-profile-hero strong{font-size:14px!important;font-weight:800!important}
        .juba-mobile-chat .juba-chat-profile-metrics b{font-size:13px!important}
        .juba-mobile-chat .juba-chat-profile-metrics small{font-size:8px!important}
        @media (max-width:1023px){
          .juba-mobile-chat .chat-conversations-sidebar{width:min(84vw,300px)!important}
          .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:18px 14px!important}
          .juba-mobile-chat .border-t.border-\\[var\\(--duo-line\\)\\]{padding:10px 12px 12px!important}
          .juba-mobile-chat .min-h-0.flex-1.space-y-4 .max-w-\\[72\\%\\].min-w-\\[8rem\\]{max-width:82%!important}
        }
      `}</style>
      <style>{`
        /* JUBA LISAN — strict reference chat UI (route scoped) */
        .juba-mobile-chat{background:var(--duo-card)!important;color:var(--duo-ink)!important;gap:0!important}
        .juba-mobile-chat .chat-conversations-sidebar{width:270px!important;background:var(--duo-card)!important;border-right:1px solid var(--duo-line)!important;box-shadow:none!important}
        .juba-mobile-chat .chat-conversations-sidebar>div:first-child{height:62px!important;padding:0 16px!important;border-bottom:1px solid var(--duo-line)!important;display:flex!important;align-items:center!important}
        .juba-mobile-chat .chat-conversations-sidebar>div:first-child span{color:#777!important;font-size:11px!important;font-weight:800!important;text-transform:uppercase!important}
        .juba-mobile-chat .chat-conversations-sidebar>div:first-child button{border:0!important;background:#58cc02!important;color:var(--duo-card)!important;border-radius:7px!important;padding:7px 10px!important;font-size:9px!important;font-weight:800!important;box-shadow:0 2px 0 #46a302!important}
        .juba-mobile-chat .chat-conversations-sidebar .group{min-height:50px!important;border-bottom:1px solid #f1f1f1!important;border-inline-start:3px solid transparent!important;padding:9px 14px!important}
        .juba-mobile-chat .chat-conversations-sidebar .group:hover{background:#fafdf8!important}
        .juba-mobile-chat .chat-conversations-sidebar .group.bg-\[var\(--duo-line\)\]{background:#f0fae9!important;border-inline-start-color:#58cc02!important}
        .juba-mobile-chat .chat-conversations-sidebar .group span{font-size:10px!important;color:#666!important}
        .juba-mobile-chat>div:last-of-type{background:var(--duo-card)!important}
        .juba-mobile-chat>div:last-of-type>div:first-child{height:62px!important;background:var(--duo-card)!important;border-bottom:1px solid var(--duo-line)!important;padding:0 22px!important}
        .juba-mobile-chat>div:last-of-type>div:first-child button{color:#777!important;font-size:12px!important}
        .juba-mobile-chat>div:last-of-type>div:first-child>span{color:var(--duo-muted)!important;font-size:10px!important}
        .juba-mobile-chat .word-selectable{border:0!important;border-radius:12px!important;box-shadow:none!important;padding:12px 15px!important;font-size:13px!important;line-height:1.55!important}
        .juba-mobile-chat .word-selectable.bg-\[var\(--duo-green\)\]{background:#dcf8c6!important;color:#3d5c34!important}
        .juba-mobile-chat .word-selectable.bg-\[var\(--duo-card\)\]{background:#f6f7f6!important;color:var(--duo-ink)!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{max-width:920px!important;width:100%!important;margin:0 auto!important;padding:28px 34px!important;scrollbar-width:thin!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4>div.flex.items-end{margin-bottom:4px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4 .h-7.w-7{width:30px!important;height:30px!important;border:0!important;box-shadow:0 0 0 1px #e9ece8!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4 .max-w-\[75\%\].min-w-\[10rem\]{min-width:0!important;max-width:68%!important}
        .juba-mobile-chat .border-t-2.border-\[var\(--duo-line\)\]{max-width:920px!important;width:100%!important;margin:0 auto!important;border-top:1px solid var(--duo-line)!important;background:var(--duo-card)!important;padding:14px 28px 18px!important}
        .juba-mobile-chat input{border:1px solid #e4e8e2!important;border-radius:10px!important;background:var(--duo-card)!important;box-shadow:none!important;padding:12px 14px!important;color:var(--duo-ink)!important}
        .juba-mobile-chat input:focus{border-color:#58cc02!important;box-shadow:0 0 0 3px rgba(88,204,2,.1)!important}
        .juba-mobile-chat button.rounded-xl.border-2.border-\[var\(--duo-green-dark\)\]{border:0!important;border-radius:9px!important;background:#58cc02!important;box-shadow:0 2px 0 #46a302!important;padding-inline:20px!important}
        .juba-mobile-chat .chat-sidebar-backdrop{background:rgba(0,0,0,.18)!important}
        @media (max-width:1023px){
          .juba-mobile-chat .chat-conversations-sidebar{width:min(86vw,300px)!important}
          .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:20px 14px!important}
          .juba-mobile-chat .min-h-0.flex-1.space-y-4 .max-w-\[75\%\].min-w-\[10rem\]{max-width:82%!important}
          .juba-mobile-chat .border-t-2.border-\[var\(--duo-line\)\]{padding:12px!important}
        }
        /* Reference fidelity pass — chat composition */
        .juba-mobile-chat{background:var(--duo-card)!important}
        .juba-mobile-chat .chat-conversations-sidebar{width:224px!important;background:var(--duo-card)!important;border-right:1px solid var(--duo-line)!important}
        .juba-mobile-chat>div.flex.flex-1>div:first-child{height:60px!important;min-height:60px!important;padding-inline:20px!important;background:var(--duo-card)!important;border-bottom:1px solid var(--duo-line)!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{max-width:900px!important;padding:24px 30px!important;gap:0!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4>div.flex.items-end{margin-bottom:12px!important}
        .juba-mobile-chat .word-selectable{border-radius:11px!important;padding:11px 14px!important;font-size:13px!important;line-height:1.55!important}
        .juba-mobile-chat .border-t-2.border-\[var\(--duo-line\)\]{border-top:1px solid var(--duo-line)!important;padding:12px 24px 16px!important;background:var(--duo-card)!important}
        .juba-mobile-chat input{height:44px!important;border-radius:9px!important}
        .juba-mobile-chat button.rounded-xl.border-2.border-\[var\(--duo-green-dark\)\]{height:44px!important;border-radius:9px!important}
        .juba-mobile-chat .juba-chat-profile-rail{width:276px!important;min-width:276px!important;background:var(--duo-card)!important;border-left:1px solid var(--duo-line)!important;padding:18px!important;gap:12px!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border:1px solid #e8ece5!important;border-radius:12px!important;box-shadow:0 1px 2px rgba(30,50,20,.025)!important}
        .juba-mobile-chat .juba-chat-profile-hero{padding:18px 16px 14px!important}
        .juba-mobile-chat .juba-chat-profile-photo{width:68px!important;height:68px!important;border-radius:50%!important}
        .juba-mobile-chat .juba-chat-profile-metrics{min-height:56px!important;border-top:1px solid #eef1ec!important}
        @media (max-width:1023px){.juba-mobile-chat .juba-chat-profile-rail{display:none!important}.juba-mobile-chat .chat-conversations-sidebar{width:min(82vw,300px)!important}}

        /* Reference fidelity pass 2 — message rhythm and profile rail */
        .juba-mobile-chat .juba-chat-profile-rail{width:276px!important;min-width:276px!important}
        .juba-mobile-chat .juba-chat-side-card{overflow:hidden!important}
        .juba-mobile-chat .juba-chat-side-card-head{min-height:42px!important}
        .juba-mobile-chat .juba-chat-friend{min-height:48px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:24px 30px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4>div.flex.items-end{margin-bottom:11px!important}
        .juba-mobile-chat .max-w-\[75\%\].min-w-\[10rem\]{min-width:0!important}
        @media (max-width:1023px){.juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:20px 14px!important}}

        /* Reference fidelity pass 3 — exact visual alignment */

        .juba-mobile-chat{background:var(--duo-card)!important}
        .juba-mobile-chat .chat-conversations-sidebar{width:228px!important}
        .juba-mobile-chat .chat-conversations-sidebar>div:first-child{min-height:58px!important;padding:0 15px!important}
        .juba-mobile-chat .chat-conversations-sidebar .group{min-height:46px!important;padding:9px 13px!important}
        .juba-mobile-chat .chat-conversations-sidebar .group span{font-size:9.5px!important}
        .juba-mobile-chat>div.flex.flex-1>div:first-child{height:58px!important;min-height:58px!important;padding-inline:18px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{max-width:920px!important;padding:22px 28px!important}
        .juba-mobile-chat .word-selectable{border-radius:10px!important;padding:10px 13px!important;font-size:12.5px!important;line-height:1.58!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4>div.flex.items-end{margin-bottom:10px!important}
        .juba-mobile-chat .juba-chat-profile-rail{width:272px!important;min-width:272px!important;padding:16px!important;gap:11px!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border-radius:11px!important}
        .juba-mobile-chat .juba-chat-profile-hero{padding:16px 14px 12px!important}
        .juba-mobile-chat .juba-chat-profile-photo{width:64px!important;height:64px!important}
        .juba-mobile-chat .juba-chat-profile-metrics{min-height:54px!important}
        .juba-mobile-chat .juba-chat-side-card-head{min-height:40px!important;padding-inline:13px!important}
        .juba-mobile-chat .juba-chat-friend{min-height:46px!important;padding:7px 13px!important}
        .juba-mobile-chat .border-t-2.border-\[var\(--duo-line\)\]{padding:11px 22px 14px!important}
        .juba-mobile-chat input{height:42px!important;padding-inline:13px!important;font-size:13px!important}
        .juba-mobile-chat button.rounded-xl.border-2.border-\[var\(--duo-green-dark\)\]{height:42px!important;padding-inline:18px!important}
        @media (max-width:1180px) and (min-width:1024px){
          .juba-mobile-chat .chat-conversations-sidebar{width:200px!important}
          .juba-mobile-chat .juba-chat-profile-rail{width:248px!important;min-width:248px!important}
        }
        @media (max-width:1023px){
          .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:20px 14px!important}
        }


        /* Reference fidelity pass 4 — final proportion pass */

        .juba-mobile-chat .chat-conversations-sidebar{width:228px!important}
        .juba-mobile-chat .chat-conversations-sidebar>div:first-child{height:56px!important;min-height:56px!important}
        .juba-mobile-chat .chat-conversations-sidebar .group{min-height:44px!important}
        .juba-mobile-chat>div.flex.flex-1>div:first-child{height:56px!important;min-height:56px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{max-width:900px!important;padding:20px 26px!important}
        .juba-mobile-chat .word-selectable{padding:10px 13px!important;border-radius:10px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4>div.flex.items-end{margin-bottom:9px!important}
        .juba-mobile-chat .juba-chat-profile-rail{width:270px!important;min-width:270px!important;padding:15px!important;gap:10px!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border-radius:10px!important}
        .juba-mobile-chat .juba-chat-profile-hero{padding:15px 13px 11px!important}
        .juba-mobile-chat .juba-chat-profile-photo{width:62px!important;height:62px!important}
        .juba-mobile-chat .juba-chat-side-card-head{min-height:38px!important}
        .juba-mobile-chat .juba-chat-friend{min-height:44px!important}
        .juba-mobile-chat .border-t-2.border-\[var\(--duo-line\)\]{padding:10px 20px 13px!important}
        .juba-mobile-chat input,.juba-mobile-chat button.rounded-xl.border-2.border-\[var\(--duo-green-dark\)]{height:40px!important}
        @media (max-width:1180px) and (min-width:1024px){
          .juba-mobile-chat .chat-conversations-sidebar{width:196px!important}
          .juba-mobile-chat .juba-chat-profile-rail{width:244px!important;min-width:244px!important}
        }
        @media (max-width:1023px){
          .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:18px 12px!important}
          .juba-mobile-chat .border-t-2.border-\[var\(--duo-line\)]{padding:10px 12px 12px!important}
        }

        /* reference fidelity pass 7 — screenshot-level chat shell and message rhythm */
        .juba-mobile-chat .chat-conversations-sidebar{border-right:1px solid #e8ede5!important;background:var(--duo-card)!important}
        .juba-mobile-chat .juba-chat-profile-rail{border-left:1px solid #e8ede5!important;background:var(--duo-card)!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border:1px solid #e7ece3!important;border-radius:14px!important;background:var(--duo-card)!important}
        .juba-mobile-chat .juba-chat-profile-hero{padding:18px 16px 15px!important}
        .juba-mobile-chat .juba-chat-profile-metrics{border-top:1px solid var(--duo-line)!important}
        .juba-mobile-chat .juba-chat-friend{min-height:48px!important;border-bottom:1px solid #f0f2ed!important}
        .juba-mobile-chat .juba-chat-friend:last-child{border-bottom:0!important}
        .juba-mobile-chat .juba-chat-achievement{border:1px solid var(--duo-line)!important;border-radius:12px!important;background:#fbfff8!important}
        .juba-mobile-chat .chat-message{max-width:min(680px,82%)!important}
        .juba-mobile-chat input{height:44px!important;border-radius:12px!important}
        @media (max-width:1023px){.juba-mobile-chat .juba-chat-profile-rail{display:none!important}}


        /* Reference fidelity pass 8 — final chat screenshot alignment */
        .juba-mobile-chat{background:var(--duo-card)!important;color:var(--duo-ink)!important}
        .juba-mobile-chat .chat-conversations-sidebar{width:220px!important;min-width:220px!important}
        .juba-mobile-chat>div.flex.flex-1>div:first-child{height:58px!important;min-height:58px!important;background:var(--duo-card)!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{max-width:920px!important;padding:22px 28px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4>div.flex.items-end{margin-bottom:12px!important}
        .juba-mobile-chat .word-selectable{border-radius:12px!important;box-shadow:0 1px 2px rgba(30,50,20,.025)!important}
        .juba-mobile-chat .juba-chat-profile-rail{width:276px!important;min-width:276px!important;padding:16px!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border-radius:14px!important;box-shadow:0 1px 2px rgba(30,50,20,.025)!important}
        .juba-mobile-chat .juba-chat-profile-photo{width:68px!important;height:68px!important}
        .juba-mobile-chat .juba-chat-friend{min-height:48px!important}
        .juba-mobile-chat .border-t-2.border-\[var\(--duo-line\)\]{padding:12px 24px 15px!important;background:var(--duo-card)!important}
        .juba-mobile-chat input{height:44px!important;border-radius:12px!important}
        .juba-mobile-chat button.rounded-xl.border-2.border-\[var\(--duo-green-dark\)]{height:44px!important;border-radius:12px!important}
        @media (max-width:1180px) and (min-width:1024px){
          .juba-mobile-chat .chat-conversations-sidebar{width:196px!important;min-width:196px!important}
          .juba-mobile-chat .juba-chat-profile-rail{width:244px!important;min-width:244px!important}
        }
        @media (max-width:1023px){
          .juba-mobile-chat .chat-conversations-sidebar{width:min(82vw,300px)!important;min-width:0!important}
          .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:18px 12px!important}
          .juba-mobile-chat .border-t-2.border-\[var\(--duo-line\)]{padding:10px 12px 12px!important}
        }

        /* Reference fidelity pass 9 — chat optical hierarchy */
        .juba-mobile-chat .chat-conversations-sidebar{box-shadow:none!important}
        .juba-mobile-chat .chat-conversations-sidebar .group{transition:background-color .14s ease,border-color .14s ease!important}
        .juba-mobile-chat>div.flex.flex-1>div:first-child{box-shadow:0 1px 0 rgba(232,237,229,.7)!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{scrollbar-width:thin!important;scrollbar-color:#dfe7da transparent!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4::-webkit-scrollbar{width:7px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4::-webkit-scrollbar-thumb{background:#dfe7da!important;border-radius:99px!important}
        .juba-mobile-chat .chat-message{line-height:1.55!important}
        .juba-mobile-chat .juba-chat-profile-rail{overflow-y:auto!important;scrollbar-width:thin!important;scrollbar-color:#dfe7da transparent!important}
        .juba-mobile-chat .juba-chat-profile-rail::-webkit-scrollbar{width:6px!important}
        .juba-mobile-chat .juba-chat-profile-rail::-webkit-scrollbar-thumb{background:#dfe7da!important;border-radius:99px!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{box-shadow:0 1px 3px rgba(30,50,20,.03)!important}
        @media (max-width:640px){
          .juba-mobile-chat>div.flex.flex-1>div:first-child{height:54px!important;min-height:54px!important;padding-inline:14px!important}
          .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:16px 10px!important}
          .juba-mobile-chat .word-selectable{max-width:88%!important;font-size:12.5px!important}
          .juba-mobile-chat input{height:42px!important}
          .juba-mobile-chat button.rounded-xl.border-2.border-\[var\(--duo-green-dark\)\]{height:42px!important;padding-inline:14px!important}
        }
              /* Reference fidelity pass 10 — chat screenshot geometry */
        .juba-mobile-chat{background:var(--duo-card)!important}
        .juba-mobile-chat .chat-conversations-sidebar{width:216px!important;min-width:216px!important;background:var(--duo-card)!important;border-right:1px solid var(--duo-line)!important}
        .juba-mobile-chat .chat-conversations-sidebar>div:first-child{height:56px!important;padding-inline:14px!important;background:var(--duo-card)!important;border-bottom:1px solid var(--duo-line)!important}
        .juba-mobile-chat .chat-conversations-sidebar .group{min-height:48px!important;padding:10px 12px!important;border-bottom:1px solid #f0f2ef!important}
        .juba-mobile-chat>div.flex.flex-1>div:first-child{height:58px!important;min-height:58px!important;padding-inline:18px!important;background:var(--duo-card)!important;border-bottom:1px solid var(--duo-line)!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:22px 24px!important;background:var(--duo-card)!important}
        .juba-mobile-chat .word-selectable{border-radius:13px!important;box-shadow:none!important;padding:11px 14px!important;line-height:1.5!important}
        .juba-mobile-chat .juba-chat-profile-rail{width:264px!important;min-width:264px!important;padding:14px!important;background:var(--duo-card)!important;border-left:1px solid var(--duo-line)!important;gap:12px!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border-radius:13px!important;border:1px solid var(--duo-line)!important;background:var(--duo-card)!important}
        .juba-mobile-chat .juba-chat-profile-hero{padding:18px 14px 14px!important}
        .juba-mobile-chat .juba-chat-profile-metrics{padding:10px 8px!important}
        .juba-mobile-chat .juba-chat-side-card-head{padding:13px 14px!important}
        .juba-mobile-chat .juba-chat-friend{min-height:52px!important;padding:8px 12px!important}
        .juba-mobile-chat>div.flex.flex-1>div:last-child{padding:10px 16px 12px!important;background:var(--duo-card)!important;border-top:1px solid var(--duo-line)!important}
        .juba-mobile-chat input{height:44px!important;border-radius:10px!important;box-shadow:none!important}
        .juba-mobile-chat button.rounded-xl.border-2.border-\\[var\\(--duo-green-dark\\)\\]{height:44px!important;border-radius:10px!important;box-shadow:0 2px 0 var(--duo-green-dark)!important}
        @media (max-width:1180px) and (min-width:1024px){
          .juba-mobile-chat .juba-chat-profile-rail{width:244px!important;min-width:244px!important}
          .juba-mobile-chat .chat-conversations-sidebar{width:204px!important;min-width:204px!important}
        }
        @media (max-width:1023px){
          .juba-mobile-chat .chat-conversations-sidebar{width:min(82vw,292px)!important;min-width:0!important}
          .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:18px 14px!important}
        }
        @media (max-width:640px){
          .juba-mobile-chat>div.flex.flex-1>div:first-child{height:54px!important;min-height:54px!important;padding-inline:12px!important}
          .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:14px 10px!important}
          .juba-mobile-chat .word-selectable{max-width:90%!important;border-radius:12px!important}
          .juba-mobile-chat>div.flex.flex-1>div:last-child{padding:8px 10px 10px!important}
        }

        /* Reference fidelity pass 11 — chat optical alignment */
        .juba-chat-profile-rail{width:264px!important;min-width:264px!important}
        .juba-chat-profile-card,.juba-chat-side-card{border-radius:13px!important;box-shadow:0 1px 2px rgba(35,55,25,.035)!important}
        .juba-chat-profile-hero{min-height:92px!important}
        .juba-chat-profile-photo{width:52px!important;height:52px!important}
        .juba-chat-profile-metrics{gap:8px!important}
        .juba-chat-side-card-head{min-height:30px!important}
        .juba-chat-friend{min-height:50px!important}
        .juba-chat-friend-avatar{width:34px!important;height:34px!important}
        .juba-chat-friend-copy{min-width:0!important}
        .juba-chat-achievement{min-height:74px!important;border-radius:11px!important}
        @media (max-width:1180px) and (min-width:901px){
          .juba-chat-profile-rail{width:244px!important;min-width:244px!important}
        }
        @media (max-width:900px){
          .juba-chat-profile-rail{display:none!important}
          .juba-mobile-chat{height:calc(100dvh - 54px)!important}
        }


        /* Reference fidelity pass 12 — chat surface hierarchy */
        .juba-mobile-chat{background:#f8faf7!important}
        .juba-mobile-chat .chat-conversations-sidebar,
        .juba-mobile-chat>div.flex.flex-1>div:first-child,
        .juba-mobile-chat .juba-chat-profile-rail{background:var(--duo-card)!important}
        .juba-mobile-chat .chat-conversations-sidebar{border-right:1px solid #edf1ea!important}
        .juba-mobile-chat>div.flex.flex-1>div:first-child{border-bottom:1px solid #edf1ea!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{background:#f8faf7!important}
        .juba-mobile-chat .word-selectable{background:var(--duo-card)!important;border:1px solid #edf1ea!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border-color:#edf1ea!important;background:var(--duo-card)!important}
        .juba-mobile-chat .juba-chat-side-label{color:#92988f!important;letter-spacing:.09em!important}
        .juba-mobile-chat .juba-chat-profile-hero strong{color:#30362f!important}
        .juba-mobile-chat .juba-chat-profile-metrics{border-top:1px solid #f0f2ed!important}
        .juba-mobile-chat .juba-chat-friend{transition:background-color .14s ease!important}
        .juba-mobile-chat .juba-chat-friend:hover{background:#f7fbf4!important}
        .juba-mobile-chat>div.flex.flex-1>div:last-child{background:var(--duo-card)!important;border-top:1px solid #edf1ea!important}
        @media (max-width:900px){.juba-mobile-chat{background:var(--duo-card)!important}.juba-mobile-chat .min-h-0.flex-1.space-y-4{background:var(--duo-card)!important}}

      `}</style>
      <style>{`
        /* Reference fidelity pass 13 — compact chat proportions */
        .juba-mobile-chat .chat-conversations-sidebar{width:270px!important}
        .juba-mobile-chat .chat-conversations-sidebar>div:first-child{height:60px!important;padding-inline:15px!important}
        .juba-mobile-chat .chat-conversations-sidebar .group{min-height:48px!important;padding:8px 13px!important}
        .juba-mobile-chat>div.flex.flex-1>div:first-child{min-height:60px!important;padding:0 18px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:18px 22px!important;gap:12px!important}
        .juba-mobile-chat .min-h-0.flex-1.space-y-4>div{margin-top:0!important}
        .juba-mobile-chat .word-selectable{padding:11px 14px!important;border-radius:10px!important}
        .juba-mobile-chat>div.flex.flex-1>div:last-child{padding:12px 16px!important}
        .juba-mobile-chat>div.flex.flex-1>div:last-child input{min-height:42px!important;border-radius:10px!important}
        .juba-mobile-chat>div.flex.flex-1>div:last-child button{min-height:42px!important;border-radius:10px!important}
        .juba-mobile-chat .juba-chat-profile-rail{width:284px!important;padding-inline:13px!important}
        .juba-mobile-chat .juba-chat-profile-card,.juba-mobile-chat .juba-chat-side-card{border-radius:11px!important}
        @media (max-width:1180px) and (min-width:901px){
          .juba-mobile-chat .juba-chat-profile-rail{width:244px!important}
        }
        @media (max-width:900px){
          .juba-mobile-chat .min-h-0.flex-1.space-y-4{padding:14px 14px!important}
          .juba-mobile-chat>div.flex.flex-1>div:first-child{padding-inline:14px!important}
          .juba-mobile-chat>div.flex.flex-1>div:last-child{padding:10px 12px!important}
        }
      `}</style>
      <div className="juba-mobile-chat flex h-full min-h-0 w-full max-w-[1480px] mx-auto overflow-hidden box-border">
        <MemorySavedToast
          visible={memoryToast}
          announcementId={memoryToastId}
        />
        {/* Sidebar backdrop — mobile only */}
        {sidebarOpen && (
          <div
            className="chat-sidebar-backdrop fixed inset-x-0 top-14 bottom-0 z-10 bg-black/40 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Sidebar */}
        {sidebarOpen && (
          <aside className="chat-conversations-sidebar border-[var(--duo-line)] bg-[var(--duo-bg)]/70 fixed top-14 bottom-0 start-0 z-20 flex w-56 shrink-0 flex-col overflow-hidden border-e-2 lg:relative lg:top-auto lg:bottom-auto lg:start-auto lg:z-auto">
            <div className="border-[var(--duo-line)] flex items-center justify-between border-b-2 px-4 py-3">
              <span className="text-[var(--duo-muted)] font-semibold tracking-wide">
                {t('conversations')}
              </span>
              <button
                onClick={newChat}
                className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] font-semibold tracking-wide transition-colors"
                title={t('newConversation')}
              >
                + {t('newConversation')}
              </button>
            </div>
            <div className="flex-1 overflow-y-auto">
              {loadingConvs ? (
                <PageLoading fullScreen={false} className="block px-4 py-4" />
              ) : convLoadError ? (
                <div className="flex flex-col items-center gap-3 px-4 py-6">
                  <p className="text-[var(--duo-red)] font-sans text-xs">
                    {tCommon('error')}
                  </p>
                  <button
                    onClick={() => {
                      setConvLoadError(false)
                      setLoadingConvs(true)
                      loadConversations()
                        .then((data) => {
                          if (data === null) {
                            setConvLoadError(true)
                          } else if (data.length > 0) {
                            selectConversation(data[0].id)
                          }
                        })
                        .finally(() => setLoadingConvs(false))
                    }}
                    className="rounded-xl border border-[var(--duo-line)] bg-[var(--duo-card)] px-4 py-2 font-semibold tracking-wide text-[var(--duo-ink)] shadow-sm transition-colors hover:border-[var(--duo-green)]"
                  >
                    {tCommon('retry')}
                  </button>
                </div>
              ) : conversations.length === 0 ? (
                <p className="text-[var(--duo-muted)] px-4 py-4 font-sans">
                  {t('noConversation')}
                </p>
              ) : (
                conversations.map((c) => (
                  <div
                    key={c.id}
                    onClick={() => selectConversation(c.id)}
                    className={`group border-[var(--duo-line)] flex cursor-pointer items-center justify-between border-b px-4 py-3 transition-colors ${
                      activeId === c.id
                        ? 'bg-[var(--duo-line)] border-s-2 border-s-[var(--duo-green)]'
                        : 'hover:bg-[var(--duo-card)] border-s-2 border-s-transparent'
                    }`}
                  >
                    <span
                      className={`text-[var(--duo-ink)] truncate pe-1 font-sans leading-tight ${activeId === c.id ? 'text-[var(--duo-ink)]' : 'text-[var(--duo-muted)]'}`}
                    >
                      {c.source === 'voice' && (
                        <span
                          className="text-[var(--duo-muted)] me-1.5"
                          title="Voice session"
                        >
                          🎤
                        </span>
                      )}
                      {c.title}
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        setDeletePending(c.id)
                      }}
                      className="text-[var(--duo-ink)] text-[var(--duo-red)] hover:text-[var(--duo-red)] shrink-0 font-sans opacity-0 transition-colors group-hover:opacity-100"
                      title="Delete"
                    >
                      ✕
                    </button>
                  </div>
                ))
              )}
            </div>
          </aside>
        )}

        {/* Main chat area */}
        <div className="flex flex-1 flex-col overflow-hidden">
          {/* Header */}
          <div className="border-[var(--duo-line)] bg-[var(--duo-bg)]/70 flex shrink-0 items-center gap-2 border-b px-5 py-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] me-1 text-lg transition-colors"
              title={
                sidebarOpen ? t('toggleSidebarHide') : t('toggleSidebarShow')
              }
            >
              {sidebarOpen ? '◀' : '☰'}
            </button>
            <span className="text-[var(--duo-muted)]">●</span>
            <span className="text-[var(--duo-muted)] font-semibold tracking-wide">
              {activeId
                ? (conversations.find((c) => c.id === activeId)?.title ??
                  t('title'))
                : t('newConversation')}
            </span>
            {sending ? (
              <div className="ms-auto flex flex-col items-end gap-0.5">
                <span className="text-[var(--duo-muted)] animate-pulse font-semibold tracking-wide">
                  {t('thinking')}
                </span>
                {sendingWarn && (
                  <span className="text-[var(--duo-muted)] font-sans tracking-widest text-[var(--duo-green-dark)] uppercase">
                    {t('takingLonger')}
                  </span>
                )}
              </div>
            ) : messages.length > 0 ? (
              <button
                onClick={continueInVoice}
                className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] ms-auto font-semibold tracking-wide transition-colors"
              >
                {t('continueInVoice')}
              </button>
            ) : null}
          </div>

          <FreemiumQuotaBanner feature="chat" />

          {/* Messages */}
          <div className="min-h-0 flex-1 space-y-4 overflow-y-auto px-6 py-4">
            {loadingMsgs ? (
              <div className="flex h-full items-center justify-center">
                <PageLoading fullScreen={false} />
              </div>
            ) : messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center gap-3 text-center">
                <p className="text-[var(--duo-muted)] font-semibold tracking-wide">
                  {t('title')}
                </p>
                <p className="text-[var(--duo-muted)] max-w-xs font-sans text-xs leading-relaxed">
                  {t('subtitle', {
                    language: activeLanguage
                      ? tLang(activeLanguage.code)
                      : tLang('en-GB'),
                  })}
                </p>
              </div>
            ) : (
              messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex items-end gap-2 ${msg.role === 'user' ? 'ms-auto max-w-[75%] flex-row-reverse' : 'flex-row'}`}
                >
                  {/* Avatar */}
                  <div className="border-[var(--duo-line)] mb-0.5 h-7 w-7 flex-shrink-0 overflow-hidden rounded-full border-2 border-[var(--duo-line)]">
                    {msg.role === 'assistant' ? (
                      <Image
                        src="/logo_head.png"
                        alt="Tutor"
                        width={32}
                        height={32}
                        className="h-full w-full object-cover"
                      />
                    ) : user?.avatar ? (
                      <AuthAvatarImage
                        avatar={user.avatar}
                        alt=""
                        width={32}
                        height={32}
                        className="h-full w-full object-cover"
                        fallback={
                          <div className="bg-[var(--duo-line)] flex h-full w-full items-center justify-center">
                            <span className="text-[var(--duo-muted)] font-sans select-none">
                              {(user?.displayName ||
                                user?.username ||
                                '?')[0].toUpperCase()}
                            </span>
                          </div>
                        }
                      />
                    ) : (
                      <div className="bg-[var(--duo-line)] flex h-full w-full items-center justify-center">
                        <span className="text-[var(--duo-muted)] font-sans select-none">
                          {(user?.displayName ||
                            user?.username ||
                            '?')[0].toUpperCase()}
                        </span>
                      </div>
                    )}
                  </div>
                  <div className={`max-w-[72%] min-w-[8rem] text-left`}>
                    <TargetLanguageText
                      as="div"
                      languageCode={targetLanguageCode}
                      className={`word-selectable rounded-[10px] border px-3.5 py-2.5 text-left shadow-sm ${
                        msg.role === 'user'
                          ? 'bg-[var(--duo-green)] text-white border-[var(--duo-green)]'
                          : 'bg-[var(--duo-card)] text-[var(--duo-ink)] border-[var(--duo-line)]'
                      }`}
                      onPointerUp={
                        msg.role === 'assistant' &&
                        !(sending && i === messages.length - 1)
                          ? () => handleTextSelection(msg.content)
                          : undefined
                      }
                    >
                      {msg.content ||
                        (sending && i === messages.length - 1 ? (
                          <span className="text-[var(--duo-muted)] animate-pulse">
                            ▌
                          </span>
                        ) : null)}
                    </TargetLanguageText>
                    {msg.role === 'assistant' &&
                      msg.content &&
                      !(sending && i === messages.length - 1) && (
                        <div className="mt-1">
                          <AudioPlayer text={msg.content} size="sm" />
                        </div>
                      )}
                  </div>
                </div>
              ))
            )}
            {error && (
              <div className="text-[var(--duo-ink)] text-[var(--duo-red)] rounded-xl border-2 border-[color-mix(in_srgb,var(--duo-red)_30%,transparent)] bg-[color-mix(in_srgb,var(--duo-red)_8%,transparent)] px-4 py-2 font-sans">
                ✕{' '}
                {error === 'No active study plan found'
                  ? tCommon('noActivePlan')
                  : t('errorMessage')}
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="border-t border-[var(--duo-line)] bg-[var(--duo-bg)]/70 shrink-0 px-4 py-3">
            {freemiumExhausted ? (
              <PaywallBanner feature="chat" compact />
            ) : (
              <>
                <div className="flex items-center gap-2">
                  <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) =>
                      e.key === 'Enter' && !e.shiftKey && sendMessage()
                    }
                    disabled={sending || loadingMsgs}
                    placeholder={t('placeholder')}
                    className="flex-1 rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] px-3.5 py-2.5 font-sans text-base text-[var(--duo-ink)] shadow-sm transition-colors placeholder:text-[var(--duo-muted)] focus:border-[var(--duo-green)] focus:outline-none focus:ring-2 focus:ring-[var(--duo-green)]/15 disabled:opacity-40"
                  />
                  <button
                    onClick={sendMessage}
                    disabled={sending || !input.trim() || loadingMsgs}
                    className="rounded-[10px] border border-[var(--duo-green)] bg-[var(--duo-green)] px-4 py-2.5 font-sans font-bold uppercase tracking-widest text-white shadow-sm transition-colors hover:bg-[var(--duo-green-dark)] active:translate-y-px disabled:opacity-30"
                  >
                    {sending ? '...' : t('send')}
                  </button>
                </div>
                <p className="text-[var(--duo-muted)] mt-2 font-sans tracking-wide">
                  {t('enterToSend')}
                </p>
              </>
            )}
          </div>
        </div>

        <aside className="juba-chat-profile-rail" aria-label="Profile">
          <section className="juba-chat-profile-card">
            <div className="juba-chat-profile-hero">
              <div className="juba-chat-profile-photo">
                {user?.avatar ? <AuthAvatarImage avatar={user.avatar} alt="" width={104} height={104} className="h-full w-full object-cover" /> : <MessageCircle size={30} />}
              </div>
              <strong>{user?.displayName || user?.username}</strong>
              <span>{activeLanguage ? tLang(activeLanguage.code) : tLang('en-GB')}</span>
            </div>
            <div className="juba-chat-profile-metrics">
              <div><b>{xp}</b><small>{t("xp")}</small></div>
              <div><b>{streak}</b><small>{t("streak")}</small></div>
              <div><b>{accuracy}%</b><small>{t("accuracy")}</small></div>
            </div>

          </section>
          <section className="juba-chat-side-card">
            <div className="juba-chat-side-card-head"><div><span className="juba-chat-side-label">NEXT</span><h3>{t('title')}</h3></div></div>
            <div className="juba-chat-achievement">
              <div className="juba-chat-achievement-icon"><Trophy size={24}/></div>
              <div><strong>{t('continueInVoice')}</strong><span>{streak} day streak</span></div>
            </div>
          </section>
          <section className="juba-chat-side-card">
            <div className="juba-chat-side-card-head"><div><span className="juba-chat-side-label">FRIENDS</span><h3>Friends</h3></div></div>
            <div className="juba-chat-friends-list">
              {friends.length ? friends.map((friend) => (
                <button key={friend.id} type="button" className="juba-chat-friend" onClick={() => router.push('/friends/chat/' + friend.id)}>
                  <span className="juba-chat-friend-avatar">
                    {friend.avatar ? <AuthAvatarImage avatar={friend.avatar} alt="" width={32} height={32} className="h-full w-full object-cover" /> : (friend.display_name || friend.username || '?')[0].toUpperCase()}
                  </span>
                  <span className="juba-chat-friend-copy"><strong>{friend.display_name || friend.username}</strong><small>@{friend.username}</small></span>
                </button>
              )) : <span className="juba-chat-friends-empty">{t("title")}</span>}
            </div>
          </section>
        </aside>

        <ConfirmDialog
          open={deletePending !== null}
          title={t('deleteTitle')}
          message={t('deleteMessage')}
          confirmLabel={t('deleteConfirm')}
          danger
          onConfirm={() =>
            deletePending !== null && deleteConversation(deletePending)
          }
          onCancel={() => setDeletePending(null)}
        />

        {/* Word-save tooltip */}
        {selectedWord && (
          <WordTooltip
            word={selectedWord}
            pos={tooltipPos}
            saveState={saveState}
            onSave={() => handleSaveWord()}
            onDismiss={dismissTooltip}
            labels={{
              saveWord: tCommon('saveWord'),
              wordSaved: tCommon('wordSaved'),
              wordSaveError: tCommon('wordSaveError'),
            }}
          />
        )}
      </div>
    </MaintenanceGate>
  )
}
