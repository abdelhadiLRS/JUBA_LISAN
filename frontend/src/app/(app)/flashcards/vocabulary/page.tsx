'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { PageLoading } from '@/components/ui/page-loading'
import { Pagination } from '@/components/ui/pagination'

interface VocabItem {
  id: number
  word: string
  definition: string
  example_sentence: string
  translation: string
}

interface GuestVocabItem {
  id: string
  sourceText: string
  translation: string
  sourceLanguage: string
  targetLanguage: string
  createdAt: string
  mastery: number
  nextReviewAt: string
}

const LIMIT = 10
const GUEST_VOCABULARY_KEY = 'juba_lisan_saved_vocabulary'

export default function VocabularyPage() {
  const t = useTranslations('flashcards')

  const [items, setItems] = useState<VocabItem[]>([])
  const [guestItems, setGuestItems] = useState<GuestVocabItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [search, setSearch] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [deletingId, setDeletingId] = useState<number | null>(null)

  function loadGuestVocabulary() {
    try {
      const stored = JSON.parse(localStorage.getItem(GUEST_VOCABULARY_KEY) || '[]')
      setGuestItems(Array.isArray(stored) ? stored : [])
    } catch {
      setGuestItems([])
    }
  }

  useEffect(() => {
    loadGuestVocabulary()
  }, [])

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search)
      setPage(1)
    }, 300)
    return () => clearTimeout(timer)
  }, [search])

  const loadPage = useCallback(async (p: number, q: string) => {
    setLoading(true)
    try {
      const params = new URLSearchParams({
        page: String(p),
        limit: String(LIMIT),
        search: q,
      })
      const res = await apiFetch(`/api/flashcards/vocabulary?${params}`)
      if (res.ok) {
        const data = await res.json()
        setItems(data.items)
        setTotal(data.total)
        setPage(data.page)
        setPages(data.pages)
      }
    } catch {
      /* ignore */
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadPage(page, debouncedSearch)
  }, [page, debouncedSearch, loadPage])

  async function deleteItem(id: number) {
    setDeletingId(id)
    try {
      await apiFetch(`/api/flashcards/${id}`, { method: 'DELETE' })
      await loadPage(page, debouncedSearch)
    } catch {
      /* ignore */
    } finally {
      setDeletingId(null)
    }
  }

  function deleteGuestItem(id: string) {
    const next = guestItems.filter((item) => item.id !== id)
    setGuestItems(next)
    try {
      localStorage.setItem(GUEST_VOCABULARY_KEY, JSON.stringify(next))
    } catch {
      /* ignore */
    }
  }

  return (
    <div className="juba-flashcards-vocabulary-shell mx-auto max-w-6xl space-y-6 p-4 sm:p-6">
      <div className="flex items-center justify-between gap-4 rounded-[26px] border border-black/[0.07] bg-white p-4 shadow-[0_12px_30px_rgba(43,45,90,.055)]">
        <div className="flex items-center gap-2">
          <span className="text-[#202127] text-[rgba(32,33,39,.52)]">●</span>
          <span className="text-[#202127] text-[rgba(32,33,39,.52)] font-sans tracking-widest uppercase">
            {t('myVocabulary')}
          </span>
          {!loading && (
            <span className="text-[rgba(32,33,39,.52)] text-[rgba(32,33,39,.52)] font-sans tracking-widest">
              {total}
            </span>
          )}
        </div>
        <Link
          href="/flashcards"
          className="juba-secondary-button inline-flex items-center border border-black/[0.09] bg-white px-4 py-2 font-sans text-xs font-bold tracking-widest uppercase"
        >
          ← {t('backToFlashcards')}
        </Link>
      </div>

      {guestItems.length > 0 && (
        <section className="juba-card bg-[#fff3d1] p-5">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-[10px] font-black uppercase tracking-[0.16em] text-[#202127]/60">
                JUBA LISAN · Visitor learning
              </p>
              <h2 className="mt-1 text-xl font-black tracking-tight text-[#202127]">
                Saved from Instant Translator
              </h2>
              <p className="mt-1 text-xs font-semibold text-[#202127]/80/75">
                These items are saved in this browser. Sign in later to sync them with your account.
              </p>
            </div>
            <Link
              href="/register"
              className="juba-primary-button inline-flex shrink-0 items-center justify-center px-4 py-2 text-xs font-black"
            >
              Create account to sync
            </Link>
          </div>
          <div className="mt-4 grid gap-2">
            {guestItems.map((item) => (
              <div
                key={item.id}
                className="flex items-start justify-between gap-3 rounded-[20px] border border-black/[0.08] bg-white/80 px-4 py-3"
              >
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <p className="text-sm font-black text-[#202127]">{item.sourceText}</p>
                    <span className="rounded-full bg-[#202127] px-2 py-0.5 text-[9px] font-black uppercase tracking-wider text-white">
                      {item.sourceLanguage === 'auto' ? 'auto' : item.sourceLanguage}
                    </span>
                  </div>
                  <p className="mt-1 text-sm font-semibold text-[#202127]/80">{item.translation}</p>
                  <div className="mt-2 flex items-center gap-3 text-[10px] font-bold uppercase tracking-wider text-neutral-500">
                    <span>Mastery {item.mastery}%</span>
                    <span>Review ready</span>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => deleteGuestItem(item.id)}
                  className="shrink-0 rounded-full border border-black/[0.12] px-2.5 py-1 text-[10px] font-black text-[#202127]/70 transition hover:bg-[#202127] hover:text-white"
                  aria-label="Remove saved item"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        </section>
      )}

      <input
        type="search"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder={t('vocabularySearch')}
        className="w-full border px-4 py-3 font-sans text-sm transition-colors focus:outline-none"
      />

      <div className="juba-card overflow-hidden bg-white">
        {loading ? (
          <PageLoading fullScreen={false} className="block p-5" />
        ) : items.length === 0 ? (
          <p className="text-[rgba(32,33,39,.52)] p-5 font-sans text-xs tracking-widest uppercase">
            {debouncedSearch ? t('myVocabularyNoResults') : t('myVocabularyEmpty')}
          </p>
        ) : (
          <div className="divide-y divide-black/[0.07]">
            {items.map((item) => (
              <div key={item.id} className="flex items-start justify-between gap-4 px-5 py-4 transition hover:bg-[#fafaff]">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <p className="text-[#202127] font-sans text-xs font-bold">{item.word}</p>
                    <AudioPlayer text={item.word} size="sm" />
                  </div>
                  <p className="text-[rgba(32,33,39,.52)] mt-0.5 font-sans text-xs leading-relaxed">{item.definition}</p>
                  <p className="text-[rgba(32,33,39,.52)] text-[#202127] mt-1 font-sans tracking-widest uppercase">{item.translation}</p>
                </div>
                <button
                  onClick={() => deleteItem(item.id)}
                  disabled={deletingId === item.id}
                  className="text-[rgba(32,33,39,.52)] shrink-0 font-sans text-xs transition-colors hover:text-red-400 disabled:opacity-40"
                  aria-label="Delete"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <Pagination
        page={page - 1}
        totalPages={pages}
        loading={loading}
        onPageChange={(p) => setPage(p + 1)}
        prevLabel={`← ${t('vocabularyPrev')}`}
        nextLabel={`${t('vocabularyNext')} →`}
        pageInfo={t('vocabularyPageInfo', { page, pages })}
        className="gap-2 border-0 bg-transparent"
      />
    </div>
  )
}
