'use client'

import { useState, useRef, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
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

export default function ChatPage() {
  const t = useTranslations('chat')
  const tCommon = useTranslations('common')
  const tLang = useTranslations('targetLanguages')
  const router = useRouter()
  const user = useAuthStore((s) => s.user)
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
      <div className="juba-mobile-chat flex h-[calc(100dvh-56px)] w-full overflow-hidden lg:h-screen">
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
                  <p className="text-rose-600 font-sans text-xs">
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
                    className="rounded-xl border-2 border-[var(--duo-line)] bg-white px-4 py-2 font-semibold tracking-wide text-[var(--duo-ink)] shadow-[2px_2px_0_var(--duo-line)] transition-all hover:-translate-y-0.5 hover:border-[var(--duo-green)]"
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
                        : 'hover:bg-white border-s-2 border-s-transparent'
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
                      className="text-[var(--duo-ink)] text-rose-600 hover:text-rose-600 shrink-0 font-sans opacity-0 transition-all group-hover:opacity-100"
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
                        width={28}
                        height={28}
                        className="h-full w-full object-cover"
                      />
                    ) : user?.avatar ? (
                      <AuthAvatarImage
                        avatar={user.avatar}
                        alt=""
                        width={28}
                        height={28}
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
                  <div className={`max-w-[75%] min-w-[10rem] text-left`}>
                    <TargetLanguageText
                      as="div"
                      languageCode={targetLanguageCode}
                      className={`word-selectable border-2 border-[var(--duo-line)] px-4 py-3 text-left ${
                        msg.role === 'user'
                          ? 'bg-[var(--duo-green)] text-white border-[var(--duo-green-dark)] shadow-[3px_3px_0_var(--duo-green-dark)]'
                          : 'bg-white text-[var(--duo-ink)] border-2 border-[var(--duo-line)] shadow-[2px_2px_0_var(--duo-line)]'
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
              <div className="text-[var(--duo-ink)] text-rose-600 rounded-xl border-2 border-rose-300 bg-rose-50 px-4 py-2 font-sans">
                ✕{' '}
                {error === 'No active study plan found'
                  ? tCommon('noActivePlan')
                  : t('errorMessage')}
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="border-t-2 border-[var(--duo-line)] bg-[var(--duo-bg)]/70 shrink-0 px-4 py-4">
            {freemiumExhausted ? (
              <PaywallBanner feature="chat" compact />
            ) : (
              <>
                <div className="flex gap-2">
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
                    className="flex-1 rounded-xl border-2 border-[var(--duo-line)] bg-white px-4 py-3 font-sans text-base text-[var(--duo-ink)] shadow-[2px_2px_0_var(--duo-line)] transition-all placeholder:text-[#8a918c] focus:border-[var(--duo-green)] focus:outline-none focus:ring-2 focus:ring-[var(--duo-green)]/15 disabled:opacity-40"
                  />
                  <button
                    onClick={sendMessage}
                    disabled={sending || !input.trim() || loadingMsgs}
                    className="rounded-xl border-2 border-[var(--duo-green-dark)] bg-[var(--duo-green)] px-5 font-sans font-bold uppercase tracking-widest text-white shadow-[3px_3px_0_var(--duo-green-dark)] transition-all hover:-translate-y-0.5 hover:bg-[var(--duo-green)] hover:shadow-[4px_4px_0_var(--duo-green-dark)] active:translate-y-0.5 active:shadow-[1px_1px_0_var(--duo-green-dark)] disabled:opacity-30"
                  >
                    {sending ? '...' : t('send')}
                  </button>
                </div>
                <p className="text-[var(--duo-muted)] text-[#8a918c] mt-2 font-sans tracking-wide">
                  {t('enterToSend')}
                </p>
              </>
            )}
          </div>
        </div>

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
