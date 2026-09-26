'use client'

import { FormEvent, useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import { Loader2, Trash2 } from 'lucide-react'
import { useTranslations } from 'next-intl'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import {
  MemoryApiError,
  clearMemories,
  createMemory,
  deleteMemory,
  fetchMemories,
} from '@/lib/memories'
import type { Memory } from '@/types/api'

export default function SettingsMemoriesPage() {
  const t = useTranslations('settings')
  const tCommon = useTranslations('common')
  const [memories, setMemories] = useState<Memory[]>([])
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [adding, setAdding] = useState(false)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [clearConfirm, setClearConfirm] = useState(false)
  const [clearing, setClearing] = useState(false)
  const [dialogError, setDialogError] = useState('')
  const [message, setMessage] = useState<{
    type: 'success' | 'error'
    text: string
  } | null>(null)
  const mutating = adding || deletingId !== null || clearing

  const loadMemories = useCallback(async () => {
    setLoading(true)
    setLoadError(false)
    try {
      const data = await fetchMemories()
      setMemories(data.memories)
    } catch {
      setLoadError(true)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void loadMemories()
  }, [loadMemories])

  async function handleAdd(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (loading || loadError || mutating) return
    const normalized = content.trim()
    if (!normalized) return
    setAdding(true)
    setMessage(null)
    try {
      const memory = await createMemory(normalized)
      setMemories((previous) => [...previous, memory].slice(-150))
      setContent('')
      setMessage({ type: 'success', text: t('memoryAddSuccess') })
    } catch (error) {
      setMessage({
        type: 'error',
        text:
          error instanceof MemoryApiError && error.status === 409
            ? t('memoryDuplicateError')
            : t('memoryAddError'),
      })
    } finally {
      setAdding(false)
    }
  }

  async function handleDelete(id: number) {
    if (mutating) return
    setDeletingId(id)
    setMessage(null)
    try {
      await deleteMemory(id)
      setMemories((previous) => previous.filter((memory) => memory.id !== id))
      setMessage({ type: 'success', text: t('memoryDeleteSuccess') })
    } catch {
      setMessage({ type: 'error', text: t('memoryDeleteError') })
    } finally {
      setDeletingId(null)
    }
  }

  async function handleClearAll() {
    if (mutating) return
    setClearing(true)
    setDialogError('')
    try {
      await clearMemories()
      setMemories([])
      setClearConfirm(false)
      setMessage({ type: 'success', text: t('memoryClearSuccess') })
    } catch {
      setDialogError(t('memoryClearError'))
    } finally {
      setClearing(false)
    }
  }

  function sourceLabel(source: string) {
    const labels: Record<string, string> = {
      chat: t('memorySourceChat'),
      voice: t('memorySourceVoice'),
      conversation: t('memorySourceVoice'),
      manual: t('memorySourceManual'),
    }
    return labels[source] ?? t('memorySourceUnknown')
  }

  return (
    <div className="mx-auto max-w-5xl space-y-6 p-4 sm:p-6">
      <nav
        aria-label={t('memoryBreadcrumb')}
        className="text-[#202127] text-[rgba(32,33,39,.52)] mb-8 flex items-center gap-2 font-sans"
      >
        <Link
          href="/settings"
          className="hover:text-[#202127] tracking-widest uppercase transition-colors"
        >
          {t('title')}
        </Link>
        <span aria-hidden="true">›</span>
        <h1 className="text-[#202127] tracking-widest uppercase">
          {t('sectionMemory')}
        </h1>
      </nav>

      <div className="rounded-[30px] border border-[#ededff] bg-white p-6 shadow-[0_12px_30px_rgba(43,45,90,.055)]">
        <div className="border-[#ededff] mb-4 flex items-center gap-2 border-b pb-4">
          <span aria-hidden="true" className="text-[#202127] text-[rgba(32,33,39,.52)]">
            ●
          </span>
          <h2 className="text-[#202127] text-[rgba(32,33,39,.52)] font-sans tracking-widest uppercase">
            {t('sectionMemory')}
          </h2>
        </div>

        <p className="text-[rgba(32,33,39,.52)] mb-5 font-sans text-xs leading-relaxed">
          {t('memoryDescription')}
        </p>

        <form
          onSubmit={handleAdd}
          aria-busy={adding}
          className="border-[#ededff] mb-6 border-b pb-6"
        >
          <label
            htmlFor="memory-content"
            className="text-[#202127] text-[rgba(32,33,39,.52)] mb-2 block font-sans tracking-widest uppercase"
          >
            {t('memoryInputLabel')}
          </label>
          <textarea
            id="memory-content"
            value={content}
            onChange={(event) => setContent(event.target.value)}
            maxLength={200}
            rows={3}
            required
            aria-describedby="memory-hint"
            placeholder={t('memoryInputPlaceholder')}
            className="border-[#ededff] bg-[#ededff]/40 text-[#202127] placeholder:text-[rgba(32,33,39,.52)] focus:border-[#5862e2] mb-2 w-full resize-y border p-3 font-sans text-sm outline-none"
          />
          <div className="flex items-center justify-between gap-4">
            <p
              id="memory-hint"
              className="text-[#202127] text-[rgba(32,33,39,.52)] font-sans"
            >
              {t('memoryInputHint', { max: 200 })}
            </p>
            <button
              type="submit"
              disabled={loading || loadError || mutating || !content.trim()}
              className="bg-[#5862e2] text-[#202127] text-[#202127] hover:bg-[#5862e2]-bright flex min-w-28 items-center justify-center gap-2 px-4 py-2 font-sans font-bold tracking-widest uppercase transition-colors disabled:cursor-not-allowed disabled:opacity-50"
            >
              {adding && (
                <Loader2
                  aria-hidden="true"
                  className="h-3.5 w-3.5 animate-spin"
                />
              )}
              {adding ? t('memoryAdding') : t('memoryAdd')}
            </button>
          </div>
        </form>

        <div aria-live="polite" className="min-h-5">
          {message && (
            <p
              role={message.type === 'error' ? 'alert' : 'status'}
              className={`mb-4 font-sans text-xs ${message.type === 'error' ? 'text-rose-600' : 'text-emerald-600'}`}
            >
              {message.text}
            </p>
          )}
        </div>

        {loading ? (
          <PageLoading fullScreen={false} />
        ) : loadError ? (
          <div role="alert" className="border-red-200/50 border p-4">
            <p className="text-rose-600 mb-3 font-sans text-xs">
              {t('memoryLoadError')}
            </p>
            <button
              onClick={() => void loadMemories()}
              className="border-[#ededff] text-[#202127] text-[rgba(32,33,39,.52)] hover:text-[#202127] border px-4 py-2 font-sans tracking-widest uppercase"
            >
              {tCommon('retry')}
            </button>
          </div>
        ) : memories.length === 0 ? (
          <p className="text-[rgba(32,33,39,.52)] text-[rgba(32,33,39,.52)] font-sans">
            {t('memoryEmpty')}
          </p>
        ) : (
          <>
            <ul className="mb-4 flex flex-col gap-3">
              {memories.map((memory) => (
                <li
                  key={memory.id}
                  className="border-[#ededff] flex items-start justify-between gap-3 border p-3"
                >
                  <div className="flex-1 space-y-1">
                    <p className="text-[rgba(32,33,39,.52)] font-sans text-xs leading-relaxed">
                      {memory.content}
                    </p>
                    <p className="text-[#202127] text-[rgba(32,33,39,.52)] font-sans tracking-widest uppercase">
                      {sourceLabel(memory.source)}
                    </p>
                  </div>
                  <button
                    onClick={() => void handleDelete(memory.id)}
                    disabled={mutating}
                    aria-label={t('memoryDeleteLabel', {
                      content: memory.content,
                    })}
                    aria-busy={deletingId === memory.id}
                    className="text-[rgba(32,33,39,.52)] hover:text-rose-600 shrink-0 p-2 transition-colors disabled:opacity-50"
                  >
                    {deletingId === memory.id ? (
                      <Loader2
                        aria-hidden="true"
                        className="h-4 w-4 animate-spin"
                      />
                    ) : (
                      <Trash2 aria-hidden="true" className="h-4 w-4" />
                    )}
                  </button>
                </li>
              ))}
            </ul>
            <button
              onClick={() => {
                setDialogError('')
                setClearConfirm(true)
              }}
              disabled={mutating}
              className="text-[rgba(32,33,39,.52)] text-[rgba(32,33,39,.52)] border-[#ededff] hover:text-rose-600 hover:border-red-200/50 w-full border py-2 font-sans tracking-widest uppercase transition-colors"
            >
              {t('memoryClearAll')}
            </button>
          </>
        )}
      </div>

      <ConfirmDialog
        open={clearConfirm}
        title={t('memoryClearAllTitle')}
        message={t('memoryClearAllMessage')}
        confirmLabel={
          clearing ? t('memoryClearing') : t('memoryClearAllConfirm')
        }
        danger
        confirming={clearing}
        error={dialogError}
        onConfirm={() => void handleClearAll()}
        onCancel={() => setClearConfirm(false)}
      />
    </div>
  )
}
