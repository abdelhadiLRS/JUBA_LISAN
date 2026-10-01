'use client'

import { useState, useEffect } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { mapUser } from '@/lib/mappers'
import { useAuthStore } from '@/store/auth'

export function ConversationSection({ title }: { title?: string } = {}) {
  const t = useTranslations('settings')
  const user = useAuthStore((s) => s.user)
  const setUser = useAuthStore((s) => s.setUser)

  const [convMaxDuration, setConvMaxDuration] = useState<900 | 1800>(1800)
  const [convInactivityTimeout, setConvInactivityTimeout] = useState<
    60 | 180 | 300
  >(180)
  const [convMessage, setConvMessage] = useState<{
    type: 'ok' | 'err'
    text: string
  } | null>(null)
  const [savingConv, setSavingConv] = useState(false)

  useEffect(() => {
    if (user) {
      setConvMaxDuration((user.conversation_max_duration as 900 | 1800) || 1800)
      setConvInactivityTimeout(
        (user.conversation_inactivity_timeout as 60 | 180 | 300) || 180
      )
    }
  }, [user])

  async function handleSaveConversation() {
    setSavingConv(true)
    setConvMessage(null)
    try {
      const res = await apiFetch('/api/auth/me', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_max_duration: convMaxDuration,
          conversation_inactivity_timeout: convInactivityTimeout,
        }),
      })
      if (!res.ok) throw new Error(t('saveFailed'))
      const updated = await res.json()
      setUser(mapUser(updated, user))
      setConvMessage({ type: 'ok', text: t('conversationSaved') })
    } catch (err: unknown) {
      setConvMessage({
        type: 'err',
        text: err instanceof Error ? err.message : t('saveFailed'),
      })
    } finally {
      setSavingConv(false)
    }
  }

  return (
    <div className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-6 shadow-sm">
      <div className="mb-5 flex items-center gap-2 border-b border-[var(--duo-line)] pb-4">
        <span className="text-[var(--duo-muted)]">●</span>
        <span className="text-[var(--duo-muted)] font-mono tracking-widest uppercase">
          {title ?? t('sectionConversation')}
        </span>
      </div>

      <div className="space-y-5">
        <div>
          <label className="text-[var(--duo-muted)] mb-2 block font-mono tracking-widest uppercase">
            {t('conversationMaxDuration')}
          </label>
          <div className="flex gap-2">
            {([900, 1800] as const).map((val) => (
              <button
                key={val}
                type="button"
                onClick={() => setConvMaxDuration(val)}
                className={`flex-1 rounded-[10px] border py-3 font-mono text-xs tracking-widest uppercase transition-colors ${
                  convMaxDuration === val
                    ? 'border-[var(--duo-green)] bg-[var(--duo-green)] text-white'
                    : 'border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-green)] hover:text-[var(--duo-ink)]'
                }`}
              >
                {val === 900 ? t('min15') : t('min30')}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="text-[var(--duo-muted)] mb-2 block font-mono tracking-widest uppercase">
            {t('conversationInactivityTimeout')}
          </label>
          <div className="flex gap-2">
            {([60, 180, 300] as const).map((val) => (
              <button
                key={val}
                type="button"
                onClick={() => setConvInactivityTimeout(val)}
                className={`flex-1 rounded-[10px] border py-3 font-mono text-xs tracking-widest uppercase transition-colors ${
                  convInactivityTimeout === val
                    ? 'border-[var(--duo-green)] bg-[var(--duo-green)] text-white'
                    : 'border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-green)] hover:text-[var(--duo-ink)]'
                }`}
              >
                {val === 60 ? t('min1') : val === 180 ? t('min3') : t('min5')}
              </button>
            ))}
          </div>
        </div>

        {convMessage && (
          <div
            className={`rounded-[10px] border px-4 py-3 font-mono text-xs ${convMessage.type === 'ok' ? 'border-[var(--duo-line)] text-[var(--duo-muted)]' : 'border-[var(--duo-red)]/40 text-[var(--duo-red)]'}`}
          >
            {convMessage.type === 'ok' ? '✓ ' : '✕ '}
            {convMessage.text}
          </div>
        )}

        <button
          onClick={handleSaveConversation}
          disabled={savingConv}
          className="w-full rounded-[10px] bg-[var(--duo-green)] py-3 font-mono text-xs font-bold tracking-widest uppercase text-white transition-colors hover:bg-[var(--duo-green-dark)] disabled:opacity-40"
        >
          {savingConv ? t('saving') : t('saveConversation')}
        </button>
      </div>
    </div>
  )
}
