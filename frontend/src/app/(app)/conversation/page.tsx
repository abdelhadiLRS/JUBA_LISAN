/** 
 * /conversation — Voice conversation page.
 *
 * ConversationMode uses @ricky0123/vad-react (ONNX/WASM) and the Web Audio
 * API, neither of which are compatible with SSR. It is loaded client-side only
 * via `dynamic({ ssr: false })`.
 */
'use client'

import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import type { ChatContextItem } from '@/lib/conversation-ws'
import { PageLoading } from '@/components/ui/page-loading'
import { FreemiumQuotaBanner } from '@/components/billing/FreemiumQuotaBanner'
import { PaywallBanner } from '@/components/billing/PaywallBanner'
import { MaintenanceGate } from '@/components/billing/MaintenanceBanner'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'
import { useAuthStore, isSubscribed, isFreemiumTrialActive } from '@/store/auth'
import { useFreemiumStore } from '@/store/freemium'
import { useTranslations } from 'next-intl'

function ConversationLoading() {
  return <PageLoading />
}

const ConversationMode = dynamic(
  () => import('@/components/conversation/ConversationMode'),
  {
    ssr: false,
    loading: ConversationLoading,
  }
)

export default function ConversationPage() {
  const t = useTranslations('conversation')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const user = useAuthStore((s) => s.user)
  const fetchFreemium = useFreemiumStore((s) => s.fetchStatus)
  const freemiumStatus = useFreemiumStore((s) => s.status)
  const freemiumExhausted =
    stripeEnabled &&
    !isSubscribed(user, stripeEnabled) &&
    !isFreemiumTrialActive(user, stripeEnabled) &&
    freemiumStatus &&
    freemiumStatus.voice_remaining_seconds <= 0

  const freemiumVoiceRemaining = freemiumStatus
    ? Math.ceil(freemiumStatus.voice_remaining_seconds / 60)
    : undefined
  const freemiumVoiceLimit = freemiumStatus
    ? Math.ceil(freemiumStatus.voice_limit_seconds / 60)
    : undefined
  const showFreemiumVoicePill =
    stripeEnabled &&
    !isSubscribed(user, stripeEnabled) &&
    !isFreemiumTrialActive(user, stripeEnabled) &&
    freemiumStatus &&
    freemiumStatus.voice_limit_seconds > 0

  const [initialContext, setInitialContext] = useState<
    ChatContextItem[] | undefined
  >(undefined)
  const [autoStart, setAutoStart] = useState(false)
  const [cefrLevel, setCefrLevel] = useState<string | null>(null)
  const [planReady, setPlanReady] = useState(false)
  const [voiceTrial, setVoiceTrial] = useState<{
    token: string
    durationSeconds: number
    cefrLevel?: string
    targetLanguage?: string
  } | null>(null)

  useEffect(() => {
    if (stripeEnabled && !isSubscribed(user, stripeEnabled)) {
      fetchFreemium()
    }
  }, [stripeEnabled, user, fetchFreemium])

  useEffect(() => {
    const raw = sessionStorage.getItem('voice_context')
    if (raw) {
      sessionStorage.removeItem('voice_context')
      try {
        const parsed = JSON.parse(raw) as unknown
        if (
          typeof parsed === 'object' &&
          parsed !== null &&
          'messages' in (parsed as Record<string, unknown>)
        ) {
          const pkg = parsed as { messages: unknown }
          if (Array.isArray(pkg.messages)) {
            setInitialContext(pkg.messages as ChatContextItem[])
          }
          setAutoStart(true)
        } else if (Array.isArray(parsed)) {
          setInitialContext(parsed as ChatContextItem[])
          setAutoStart(true)
        }
      } catch {
        // malformed — ignore
      }
    }
    const trialRaw = sessionStorage.getItem('assessment_voice_trial')
    if (trialRaw) {
      sessionStorage.removeItem('assessment_voice_trial')
      try {
        const parsed = JSON.parse(trialRaw) as {
          token?: unknown
          durationSeconds?: unknown
          cefrLevel?: unknown
          targetLanguage?: unknown
        }
        if (typeof parsed.token === 'string' && parsed.token.length > 0) {
          setVoiceTrial({
            token: parsed.token,
            durationSeconds:
              typeof parsed.durationSeconds === 'number'
                ? parsed.durationSeconds
                : 300,
            cefrLevel:
              typeof parsed.cefrLevel === 'string'
                ? parsed.cefrLevel
                : undefined,
            targetLanguage:
              typeof parsed.targetLanguage === 'string'
                ? parsed.targetLanguage
                : undefined,
          })
          setInitialContext([
            {
              role: 'user',
              content:
                t('assessmentVoiceContext'),
            },
          ])
          setAutoStart(true)
        }
      } catch {
        // malformed — ignore
      }
    }
    setPlanReady(false)
    apiFetch('/api/study-plan/today')
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data?.cefr_level) setCefrLevel(data.cefr_level)
      })
      .catch(() => {
        /* sin plan — usa default 1500ms */
      })
      .finally(() => setPlanReady(true))
  }, [activeLanguage?.code, t])

  if (!planReady) return <PageLoading minHeight="min-h-[calc(100vh-56px)] md:min-h-[60vh]" />

  return (
    <div className="juba-conversation-page">
      <MaintenanceGate>
        {voiceTrial ? (
          <ConversationMode
            initialContext={initialContext}
            autoStart={autoStart}
            cefrLevel={voiceTrial.cefrLevel ?? cefrLevel}
            targetLanguage={voiceTrial.targetLanguage ?? activeLanguage?.code}
            voiceTrialToken={voiceTrial.token}
            voiceTrialDurationSeconds={voiceTrial.durationSeconds}
            trialMode
          />
        ) : freemiumExhausted ? (
          <div className="juba-conversation-gated">
            <FreemiumQuotaBanner feature="voice" className="mb-4" />
            <PaywallBanner feature="voice" compact />
          </div>
        ) : (
          <ConversationMode
            initialContext={initialContext}
            autoStart={autoStart}
            cefrLevel={cefrLevel}
            targetLanguage={activeLanguage?.code}
            freemiumVoiceRemaining={
              showFreemiumVoicePill ? freemiumVoiceRemaining : undefined
            }
            freemiumVoiceLimit={
              showFreemiumVoicePill ? freemiumVoiceLimit : undefined
            }
          />
        )}
      </MaintenanceGate>
      <style jsx global>{`
        .juba-conversation-page {
          min-height: calc(100vh - 56px);
          padding: 20px 12px 40px;
          background: var(--juba-learning-bg);
          color: var(--juba-learning-ink);
          font-family: 'Nunito Sans', 'Noto Sans Arabic', system-ui, sans-serif;
        }
        .juba-conversation-page .juba-conversation-shell {
          max-width: 920px !important;
          min-height: calc(100vh - 120px) !important;
          padding: 0 !important;
          overflow: visible !important;
        }
        .juba-conversation-page .juba-conversation-shell > div:first-child {
          margin-bottom: 18px !important;
          padding: 18px 20px !important;
          border: 2px solid var(--juba-learning-green-dark) !important;
          border-radius: 22px !important;
          background: var(--juba-learning-green) !important;
          box-shadow: 0 5px 0 var(--juba-learning-green-dark) !important;
        }
        .juba-conversation-page .juba-conversation-shell > div:first-child p,
        .juba-conversation-page .juba-conversation-shell > div:first-child h1,
        .juba-conversation-page .juba-conversation-shell > div:first-child button {
          color: #fff !important;
          font-family: inherit !important;
        }
        .juba-conversation-page .juba-conversation-shell > div:first-child h1 {
          font-size: 1.7rem !important;
          font-weight: 900 !important;
          letter-spacing: -.02em !important;
        }
        .juba-conversation-page .juba-conversation-shell > div:first-child p {
          opacity: .86;
          font-size: .72rem !important;
          font-weight: 900 !important;
        }
        .juba-conversation-page .juba-conversation-shell > div:nth-child(3) {
          min-height: 340px !important;
          margin-bottom: 16px !important;
          padding: 18px !important;
          border: 2px solid var(--juba-learning-border) !important;
          border-radius: 20px !important;
          background: #fff !important;
          box-shadow: var(--juba-learning-shadow) !important;
        }
        .juba-conversation-page .juba-conversation-shell button {
          font-family: inherit !important;
          font-weight: 900 !important;
        }
        .juba-conversation-page .juba-conversation-shell button:not([disabled]) {
          transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease, background .12s ease !important;
        }
        .juba-conversation-page .juba-conversation-shell button:focus-visible {
          outline: 3px solid var(--juba-learning-blue) !important;
          outline-offset: 3px !important;
        }
        .juba-conversation-page .juba-conversation-shell > div:last-child {
          gap: 14px !important;
        }
        .juba-conversation-page .juba-conversation-shell [class*="font-mono"] {
          font-family: inherit !important;
          letter-spacing: normal !important;
        }
        .juba-conversation-page .juba-conversation-shell [class*="border-[rgba(7,7,9,.08)]"] {
          border-color: var(--juba-learning-border) !important;
          border-radius: 14px !important;
        }
        .juba-conversation-page .juba-conversation-shell [class*="bg-[#5862e2]"] {
          background: var(--juba-learning-green) !important;
          border: 2px solid var(--juba-learning-green-dark) !important;
          border-radius: 14px !important;
          box-shadow: 0 3px 0 var(--juba-learning-green-dark) !important;
        }
        .juba-conversation-page .juba-conversation-shell [class*="bg-[#5862e2]"]:hover {
          background: var(--juba-learning-green-dark) !important;
        }
        .juba-conversation-page .juba-conversation-shell [class*="text-[#5862e2]"] {
          color: var(--juba-learning-green-dark) !important;
        }
        .juba-conversation-page .juba-conversation-shell .juba-gated,
        .juba-conversation-gated {
          max-width: 720px;
          margin: 0 auto;
          padding-top: 12px;
        }
        @media (max-width: 767px) {
          .juba-conversation-page {
            padding: 12px 10px 30px;
          }
          .juba-conversation-page .juba-conversation-shell {
            min-height: calc(100vh - 90px) !important;
          }
          .juba-conversation-page .juba-conversation-shell > div:first-child {
            padding: 16px !important;
            border-radius: 18px !important;
            box-shadow: 0 4px 0 var(--juba-learning-green-dark) !important;
          }
          .juba-conversation-page .juba-conversation-shell > div:first-child h1 {
            font-size: 1.35rem !important;
          }
          .juba-conversation-page .juba-conversation-shell > div:nth-child(3) {
            min-height: 300px !important;
            padding: 12px !important;
            border-radius: 18px !important;
          }
        }
      `}</style>
    </div>
  )
}
