'use client'

import { useCallback, useEffect, useMemo, useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import { Pagination } from '@/components/ui/pagination'
import { AdminAuthorBadge } from '@/components/feedback/AdminAuthorBadge'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface FeedbackAuthor {
  id: number
  username: string
  display_name: string
  role: 'admin' | 'user'
}

interface FeedbackEntry {
  id: number
  type: 'feature' | 'bug'
  title: string
  description: string
  status: string
  author: FeedbackAuthor
  vote_count: number
  voted_by_me: boolean
  unread_by_me: boolean
  comment_count: number
  created_at: string
}

interface FeedbackComment {
  id: number
  entry_id: number
  author: FeedbackAuthor
  body: string
  created_at: string
}

type Tab = 'feature' | 'bug'
type SortOption = 'votes' | 'date'

const PAGE_SIZE = 10

const STATUS_STYLES: Record<string, string> = {
  pending: 'border-[var(--duo-line)] text-[var(--duo-muted)]',
  planned: 'border-[var(--duo-green-dark)]/40 text-[var(--duo-green-dark)]',
  in_progress: 'border-[var(--duo-yellow)]/40 text-[var(--duo-ink)]',
  done: 'border-[var(--duo-green-dark)]/40 text-[var(--duo-green-dark)]',
  declined: 'border-rose-200/30 text-[var(--duo-red)]',
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function StatusBadge({ status, label }: { status: string; label: string }) {
  const cls = STATUS_STYLES[status] ?? STATUS_STYLES.pending
  return (
    <span
      className={`text-[var(--duo-muted)] rounded-[10px] border px-2 py-0.5 font-semibold tracking-wide ${cls}`}
    >
      {label}
    </span>
  )
}

// ---------------------------------------------------------------------------
// Create modal
// ---------------------------------------------------------------------------

interface CreateModalProps {
  type: Tab
  onClose: () => void
  onCreated: () => void
}

function CreateModal({ type, onClose, onCreated }: CreateModalProps) {
  const t = useTranslations('feedback')
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const inputCls =
    'w-full rounded-[10px] bg-white border border-[var(--duo-line)] px-4 py-3 text-sm text-[var(--duo-ink)] placeholder:text-[var(--duo-muted)] focus:outline-none focus:border-[var(--duo-green-dark)] transition-colors resize-none'
  const textareaCls =
    'w-full rounded-[10px] bg-white border border-[var(--duo-line)] px-4 py-3 text-sm text-[var(--duo-ink)] placeholder:text-[var(--duo-muted)] focus:outline-none focus:border-[var(--duo-green-dark)] transition-colors resize-y min-h-[106px]'

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      const res = await apiFetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type,
          title: title.trim(),
          description: description.trim(),
        }),
      })
      if (!res.ok) throw new Error()
      onCreated()
    } catch {
      setError(t('errorSubmit'))
    } finally {
      setSubmitting(false)
    }
  }

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  return (
    <div
      className="fixed inset-0 z-[200] flex items-center justify-center p-4"
      style={{
        backgroundColor: 'rgba(0,0,0,0.45)',
        backdropFilter: 'blur(4px)',
      }}
      onClick={onClose}
    >
      <div
        className="juba-reference-list-card w-full max-w-md overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="border-[var(--duo-line)] flex items-center justify-between border-b px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="text-[var(--duo-muted)]">●</span>
            <span className="font-sans text-[10px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">
              {type === 'feature'
                ? t('modalCreateTitleFeature')
                : t('modalCreateTitleBug')}
            </span>
          </div>
          <button
            onClick={onClose}
            className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] font-sans transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-3 p-6">
          {error && (
            <div className="rounded-[10px] border border-[var(--duo-red)]/40 px-4 py-3 text-sm text-[var(--duo-red)]">
              ✕ {error}
            </div>
          )}
          <div>
            <label className="text-[var(--duo-muted)] mb-1 block font-semibold tracking-wide">
              {t('labelTitle')}
            </label>
            <input
              type="text"
              required
              maxLength={200}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder={
                type === 'feature'
                  ? t('placeholderTitleFeature')
                  : t('placeholderTitleBug')
              }
              className={inputCls}
              autoFocus
            />
          </div>
          <div>
            <label className="text-[var(--duo-muted)] mb-1 block font-semibold tracking-wide">
              {t('labelDescription')}
            </label>
            <textarea
              required
              maxLength={5000}
              rows={5}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder={
                type === 'feature'
                  ? t('placeholderDescriptionFeature')
                  : t('placeholderDescriptionBug')
              }
              className={textareaCls}
            />
          </div>
          <div className="flex gap-2 pt-1">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 rounded-[10px] border border-[var(--duo-line)] px-4 py-2.5 text-sm tracking-widest uppercase text-[var(--duo-muted)] transition-colors hover:border-[var(--duo-green-dark)] hover:text-[var(--duo-ink)]"
            >
              {t('cancel')}
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 rounded-[10px] bg-[var(--duo-green-dark)] py-2.5 font-sans text-[10px] font-bold tracking-widest uppercase text-white transition-colors hover:opacity-90 disabled:opacity-50"
            >
              {submitting ? t('submitting') : t('submit')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Detail view
// ---------------------------------------------------------------------------

interface DetailViewProps {
  entry: FeedbackEntry
  currentUserId: number | undefined
  isAdmin: boolean
  getStatusLabel: (status: string) => string
  onBack: () => void
  onVoteToggled: (entryId: number, voted: boolean, voteCount: number) => void
  onEntryRead: (entryId: number) => void
  onEntryDeleted: (entryId: number) => void
}

function DetailView({
  entry: initialEntry,
  currentUserId,
  isAdmin,
  getStatusLabel,
  onBack,
  onVoteToggled,
  onEntryRead,
  onEntryDeleted,
}: DetailViewProps) {
  const t = useTranslations('feedback')
  const [entry, setEntry] = useState(initialEntry)
  const [comments, setComments] = useState<FeedbackComment[]>([])
  const [commentBody, setCommentBody] = useState('')
  const [postingComment, setPostingComment] = useState(false)
  const [deletePendingComment, setDeletePendingComment] =
    useState<FeedbackComment | null>(null)
  const [deleteEntryPending, setDeleteEntryPending] = useState(false)
  const [voting, setVoting] = useState(false)
  const [error, setError] = useState('')

  // Load comments on mount
  useEffect(() => {
    apiFetch(`/api/feedback/${entry.id}/read`, { method: 'POST' })
      .then((r) => {
        if (r.ok) {
          onEntryRead(entry.id)
          window.dispatchEvent(new Event('freelingo:feedback-read'))
        }
      })
      .catch(() => {})

    apiFetch(`/api/feedback/${entry.id}/comments`)
      .then((r) => r.json())
      .then((d) => setComments(d.items ?? []))
      .catch(() => {})
  }, [entry.id, onEntryRead])

  async function handleVote() {
    if (voting) return
    setVoting(true)
    try {
      const res = await apiFetch(`/api/feedback/${entry.id}/vote`, {
        method: 'POST',
      })
      if (res.ok) {
        const data = await res.json()
        setEntry((e) => ({
          ...e,
          voted_by_me: data.voted,
          vote_count: data.vote_count,
        }))
        onVoteToggled(entry.id, data.voted, data.vote_count)
      }
    } finally {
      setVoting(false)
    }
  }

  async function handlePostComment(e: React.FormEvent) {
    e.preventDefault()
    if (!commentBody.trim()) return
    setPostingComment(true)
    setError('')
    try {
      const res = await apiFetch(`/api/feedback/${entry.id}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ body: commentBody.trim() }),
      })
      if (!res.ok) throw new Error()
      const comment: FeedbackComment = await res.json()
      setComments((prev) => [...prev, comment])
      setEntry((e) => ({ ...e, comment_count: e.comment_count + 1 }))
      setCommentBody('')
    } catch {
      setError(t('errorSubmit'))
    } finally {
      setPostingComment(false)
    }
  }

  async function handleDeleteComment(comment: FeedbackComment) {
    await apiFetch(`/api/feedback/${entry.id}/comments/${comment.id}`, {
      method: 'DELETE',
    })
    setComments((prev) => prev.filter((c) => c.id !== comment.id))
    setEntry((e) => ({ ...e, comment_count: Math.max(0, e.comment_count - 1) }))
    setDeletePendingComment(null)
  }

  async function handleDeleteEntry() {
    await apiFetch(`/api/feedback/${entry.id}`, { method: 'DELETE' })
    setDeleteEntryPending(false)
    onEntryDeleted(entry.id)
    onBack()
  }

  const statusLabel = getStatusLabel(entry.status)

  return (
    <div className="space-y-4">
      {/* Back */}
      <button
        onClick={onBack}
        className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] font-semibold tracking-wide transition-colors"
      >
        {t('backToList')}
      </button>

      {/* Entry card */}
      <div className="juba-reference-list-card overflow-hidden">
        <div className="border-[var(--duo-line)] space-y-3 border-b bg-white px-6 py-5">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <h2 className="text-[var(--duo-ink)] min-w-0 flex-1 font-sans text-base leading-snug font-bold">
              {entry.title}
            </h2>
            <StatusBadge status={entry.status} label={statusLabel} />
          </div>
          <p className="text-[var(--duo-muted)] text-sm leading-relaxed whitespace-pre-wrap">
            {entry.description}
          </p>
          <div className="flex flex-wrap items-center gap-2.5 pt-1">
            <span className="text-[var(--duo-muted)] inline-flex flex-wrap items-center gap-x-1 font-sans">
              <span>
                {t('by')} {entry.author.display_name}
              </span>
              <AdminAuthorBadge role={entry.author.role} />
              <span>· {formatDate(entry.created_at)}</span>
            </span>
            {/* Vote button — only for features */}
            {entry.type === 'feature' && (
              <button
                onClick={handleVote}
                disabled={voting}
                className={`text-[var(--duo-muted)] border px-3 py-1 font-semibold tracking-wide transition-colors disabled:opacity-50 ${
                  entry.voted_by_me
                    ? 'border-[var(--duo-green-dark)]/60 text-[var(--duo-green-dark)] bg-[var(--duo-green-dark)]/10'
                    : 'border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-green-dark)] hover:text-[var(--duo-ink)]'
                }`}
              >
                ▲ {entry.vote_count}
              </button>
            )}
            {/* Delete — author or admin */}
            {(currentUserId === entry.author.id || isAdmin) && (
              <button
                onClick={() => setDeleteEntryPending(true)}
                className="text-[var(--duo-muted)] border-rose-200/30 text-[var(--duo-red)] hover:border-rose-200 ml-auto border px-3 py-1 font-semibold tracking-wide transition-colors"
              >
                {t('deleteEntry')}
              </button>
            )}
          </div>
        </div>

        {/* Comments */}
        <div className="divide-[var(--duo-line)] divide-y">
          {comments.length === 0 ? (
            <p className="text-[var(--duo-muted)] px-6 py-6 text-center text-sm">
              {t('addComment')}
            </p>
          ) : (
            comments.map((c) => (
              <div key={c.id} className="space-y-1 px-6 py-4">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[var(--duo-muted)] inline-flex flex-wrap items-center gap-x-1 font-sans">
                    <span>{c.author.display_name}</span>
                    <AdminAuthorBadge role={c.author.role} />
                    <span>· {formatDate(c.created_at)}</span>
                  </span>
                  {currentUserId === c.author.id && (
                    <button
                      onClick={() => setDeletePendingComment(c)}
                      className="text-[var(--duo-muted)] hover:text-[var(--duo-red)] font-semibold tracking-wide transition-colors"
                    >
                      {t('deleteComment')}
                    </button>
                  )}
                </div>
                <p className="text-[var(--duo-muted)] text-sm leading-relaxed whitespace-pre-wrap">
                  {c.body}
                </p>
              </div>
            ))
          )}
        </div>

        {/* Add comment form */}
        <form
          onSubmit={handlePostComment}
          className="border-[var(--duo-line)] space-y-2 border-t px-6 py-4"
        >
          {error && (
            <div className="rounded-[10px] border border-[var(--duo-red)]/40 px-4 py-2 text-sm text-[var(--duo-red)]">
              ✕ {error}
            </div>
          )}
          <textarea
            rows={2}
            value={commentBody}
            onChange={(e) => setCommentBody(e.target.value)}
            placeholder={t('commentPlaceholder')}
            maxLength={2000}
            className="juba-input w-full"
          />
          <button
            type="submit"
            disabled={postingComment || !commentBody.trim()}
            className="rounded-[10px] border border-[var(--duo-line)] px-4 py-2 font-sans text-[10px] font-bold tracking-widest uppercase text-[var(--duo-muted)] transition-colors hover:border-[var(--duo-green-dark)] hover:text-[var(--duo-ink)] disabled:cursor-not-allowed disabled:opacity-30"
          >
            {postingComment ? t('postingComment') : t('postComment')}
          </button>
        </form>
      </div>

      {/* Confirm delete entry */}
      <ConfirmDialog
        open={deleteEntryPending}
        title={t('deleteEntryConfirmTitle')}
        message={t('deleteEntryConfirmMessage')}
        confirmLabel={t('deleteEntryConfirm')}
        danger
        onConfirm={handleDeleteEntry}
        onCancel={() => setDeleteEntryPending(false)}
      />

      {/* Confirm delete comment */}
      <ConfirmDialog
        open={deletePendingComment !== null}
        title={t('deleteCommentConfirmTitle')}
        message={t('deleteCommentConfirmMessage')}
        confirmLabel={t('deleteCommentConfirm')}
        danger
        onConfirm={() =>
          deletePendingComment && handleDeleteComment(deletePendingComment)
        }
        onCancel={() => setDeletePendingComment(null)}
      />
    </div>
  )
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export default function FeedbackPage() {
  const t = useTranslations('feedback')
  const currentUserId = useAuthStore((s) => s.user?.id)
  const isAdmin = useAuthStore((s) => s.user?.role === 'admin')

  const [tab, setTab] = useState<Tab>('feature')
  const [sort, setSort] = useState<SortOption>('votes')
  const [statusFilter, setStatusFilter] = useState<string>('')
  const [entries, setEntries] = useState<FeedbackEntry[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showCreate, setShowCreate] = useState(false)

  // Detail view
  const [selectedEntry, setSelectedEntry] = useState<FeedbackEntry | null>(null)

  // Delete confirm (from list)
  const [deletePending, setDeletePending] = useState<FeedbackEntry | null>(null)

  const loadEntries = useCallback(
    async (
      pageIndex: number,
      currentTab: Tab,
      currentSort: SortOption,
      currentStatus: string
    ) => {
      setLoading(true)
      setError('')
      try {
        const params = new URLSearchParams({
          type: currentTab,
          sort: currentSort,
          order: 'desc',
          skip: String(pageIndex * PAGE_SIZE),
          limit: String(PAGE_SIZE),
        })
        if (currentStatus) params.set('status', currentStatus)
        const res = await apiFetch(`/api/feedback?${params.toString()}`)
        if (!res.ok) throw new Error()
        const data = await res.json()
        setEntries(data.items)
        setTotal(data.total)
      } catch {
        setError(t('errorLoad'))
      } finally {
        setLoading(false)
      }
    },
    [t]
  )

  // Reload when page changes
  useEffect(() => {
    loadEntries(page, tab, sort, statusFilter)
  }, [loadEntries, page]) // eslint-disable-line react-hooks/exhaustive-deps

  // Reset to page 0 when tab/sort/filter changes
  useEffect(() => {
    if (page !== 0) {
      setPage(0)
    } else {
      loadEntries(0, tab, sort, statusFilter)
    }
  }, [tab, sort, statusFilter]) // eslint-disable-line react-hooks/exhaustive-deps

  function handleVoteToggled(
    entryId: number,
    voted: boolean,
    voteCount: number
  ) {
    setEntries((prev) =>
      prev.map((e) =>
        e.id === entryId
          ? { ...e, voted_by_me: voted, vote_count: voteCount }
          : e
      )
    )
  }

  const handleEntryRead = useCallback((entryId: number) => {
    setEntries((prev) =>
      prev.map((e) => (e.id === entryId ? { ...e, unread_by_me: false } : e))
    )
    setSelectedEntry((entry) =>
      entry?.id === entryId ? { ...entry, unread_by_me: false } : entry
    )
  }, [])

  function handleEntryDeleted(entryId: number) {
    const newTotal = total - 1
    setTotal(newTotal)
    setEntries((prev) => prev.filter((e) => e.id !== entryId))
    const maxPage = Math.max(0, Math.ceil(newTotal / PAGE_SIZE) - 1)
    const targetPage = Math.min(page, maxPage)
    if (targetPage !== page) {
      setPage(targetPage)
    } else {
      loadEntries(targetPage, tab, sort, statusFilter)
    }
  }

  async function handleDeleteFromList(entry: FeedbackEntry) {
    await apiFetch(`/api/feedback/${entry.id}`, { method: 'DELETE' })
    setDeletePending(null)
    handleEntryDeleted(entry.id)
  }

  const statusOptions = useMemo(
    () => [
      { value: '', label: t('filterAll') },
      ...[
        { value: 'pending', label: t('statusPending') },
        { value: 'planned', label: t('statusPlanned') },
        { value: 'in_progress', label: t('statusInProgress') },
        { value: 'done', label: t('statusDone') },
        { value: 'declined', label: t('statusDeclined') },
      ].sort((a, b) => a.label.localeCompare(b.label)),
    ],
    [t]
  )

  function getStatusLabel(status: string) {
    return statusOptions.find((o) => o.value === status)?.label ?? status
  }

  // If a detail view is open, render it instead
  if (selectedEntry) {
    return (
      <div className="w-full px-4 py-5 sm:px-6 sm:py-6 lg:px-8">
        <DetailView
          entry={selectedEntry}
          currentUserId={currentUserId}
          isAdmin={isAdmin}
          getStatusLabel={getStatusLabel}
          onBack={() => setSelectedEntry(null)}
          onVoteToggled={handleVoteToggled}
          onEntryRead={handleEntryRead}
          onEntryDeleted={handleEntryDeleted}
        />
      </div>
    )
  }

  return (
    <div className="juba-reference-page mx-auto w-full max-w-[1480px] space-y-5 px-4 py-5 sm:px-6 sm:py-6 lg:px-8">
      {/* Page header */}
      <section className="juba-reference-hero min-h-[112px] px-5 py-5 sm:px-6 sm:py-6">
        <p className="juba-eyebrow mb-1">
          {t('title')}
        </p>
        <h1 className="text-3xl font-extrabold tracking-tight text-[var(--duo-ink)] sm:text-4xl">
          {t('subtitle')}
        </h1>
      </section>

      {/* Tabs */}
      <div className="juba-reference-filter-panel flex flex-wrap items-center gap-1 p-2.5">
        {(['feature', 'bug'] as Tab[]).map((tabOption) => (
          <button
            key={tabOption}
            onClick={() => setTab(tabOption)}
            className={`text-[var(--duo-ink)] rounded-[10px] px-4 py-2 font-semibold tracking-wide transition-colors ${
              tab === tabOption
                ? 'bg-[var(--duo-green-dark)] text-white'
                : 'text-[var(--duo-muted)] hover:bg-[var(--duo-bg)] hover:text-[var(--duo-ink)]'
            }`}
          >
            {tabOption === 'feature' ? t('tabFeatures') : t('tabBugs')}
          </button>
        ))}
        <div className="flex-1" />
        <button
          onClick={() => setShowCreate(true)}
          className="rounded-[10px] px-3 py-2 font-sans text-[10px] font-bold tracking-widest uppercase text-[var(--duo-muted)] transition-colors hover:bg-[var(--duo-bg)] hover:text-[var(--duo-ink)]"
        >
          {tab === 'feature' ? t('newFeature') : t('newBug')}
        </button>
      </div>

      {/* Filters + sort row */}
      <div className="flex flex-wrap items-center gap-2.5">
        <span className="text-[var(--duo-muted)] font-semibold tracking-wide">
          {t('sortBy')}
        </span>
        {(['votes', 'date'] as SortOption[]).map((s) => (
          <button
            key={s}
            onClick={() => setSort(s)}
            className={`text-[var(--duo-muted)] rounded-[10px] border px-3 py-1 font-semibold tracking-wide transition-colors ${
              sort === s
                ? 'border-[var(--duo-green-dark)]/40 text-[var(--duo-ink)]'
                : 'border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-green-dark)] hover:text-[var(--duo-ink)]'
            }`}
          >
            {s === 'votes' ? t('sortVotes') : t('sortDate')}
          </button>
        ))}

        <span className="ml-2 font-sans text-[10px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">
          {t('filterStatus')}
        </span>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="h-9 rounded-[10px] border border-[var(--duo-line)] bg-white px-3 text-xs text-[var(--duo-muted)] outline-none transition-colors focus:border-[var(--duo-green-dark)]"
        >
          {statusOptions.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      </div>

      {/* Error */}
      {error && (
        <div className="rounded-[10px] border border-[var(--duo-red)]/40 px-4 py-3 text-sm text-[var(--duo-red)]">
          ✕ {error}
        </div>
      )}

      {/* List */}
      <div className="juba-reference-list-card overflow-hidden">
        {loading ? (
          <PageLoading
            fullScreen={false}
            className="block px-6 py-10 text-center"
          />
        ) : entries.length === 0 ? (
          <p className="text-[var(--duo-muted)] px-6 py-10 text-center text-sm">
            {t('noEntries')}
          </p>
        ) : (
          <div>
            {entries.map((entry, i) => {
              const canDelete = currentUserId === entry.author.id || isAdmin
              return (
                <div
                  key={entry.id}
                  className={`hover:bg-[var(--duo-bg)] flex cursor-pointer gap-4 px-5 py-4 transition-colors ${
                    i < entries.length - 1 ? 'border-[var(--duo-line)] border-b' : ''
                  }`}
                  onClick={() => setSelectedEntry(entry)}
                >
                  {/* Vote column — only for features */}
                  {entry.type === 'feature' && (
                    <div
                      className="flex shrink-0 flex-col items-center gap-0.5 pt-0.5"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <button
                        onClick={async (e) => {
                          e.stopPropagation()
                          const res = await apiFetch(
                            `/api/feedback/${entry.id}/vote`,
                            {
                              method: 'POST',
                            }
                          )
                          if (res.ok) {
                            const data = await res.json()
                            handleVoteToggled(
                              entry.id,
                              data.voted,
                              data.vote_count
                            )
                          }
                        }}
                        className={`rounded-[10px] border px-2 py-1 text-sm leading-none transition-colors ${
                          entry.voted_by_me
                            ? 'border-[var(--duo-green-dark)]/60 text-[var(--duo-green-dark)] bg-[var(--duo-green-dark)]/10'
                            : 'border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-green-dark)] hover:text-[var(--duo-ink)]'
                        }`}
                        title={entry.voted_by_me ? 'Remove vote' : 'Vote'}
                      >
                        ▲
                      </button>
                      <span className="text-[var(--duo-muted)] font-sans tabular-nums">
                        {entry.vote_count}
                      </span>
                    </div>
                  )}
                  {/* Bug entries — show placeholder column for alignment */}
                  {entry.type === 'bug' && <div className="w-8 shrink-0" />}

                  {/* Content */}
                  <div className="min-w-0 flex-1 space-y-1.5">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-[var(--duo-ink)] truncate text-sm font-semibold">
                        {entry.title}
                      </span>
                      <StatusBadge
                        status={entry.status}
                        label={getStatusLabel(entry.status)}
                      />
                      {entry.unread_by_me && (
                        <span className="rounded-[10px] border border-[var(--duo-red)]/30 bg-[#fff5f4] px-2 py-0.5 font-sans text-[10px] leading-none font-bold tracking-wide text-[var(--duo-red)] uppercase">
                          {t('unread')}
                        </span>
                      )}
                    </div>
                    <p className="text-[var(--duo-muted)] line-clamp-2 text-sm leading-relaxed">
                      {entry.description}
                    </p>
                    <div className="flex flex-wrap items-center gap-3">
                      <span className="text-[var(--duo-muted)] inline-flex flex-wrap items-center gap-x-1 font-sans">
                        <span>
                          {t('by')} {entry.author.display_name}
                        </span>
                        <AdminAuthorBadge role={entry.author.role} />
                        <span>· {formatDate(entry.created_at)}</span>
                      </span>
                      {entry.comment_count > 0 && (
                        <span className="text-[var(--duo-muted)] font-sans">
                          ◌{' '}
                          {entry.comment_count === 1
                            ? t('comment')
                            : t('comments', { count: entry.comment_count })}
                        </span>
                      )}
                      {canDelete && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            setDeletePending(entry)
                          }}
                          className="text-[var(--duo-muted)] hover:text-[var(--duo-red)] ml-auto font-semibold tracking-wide transition-colors"
                        >
                          {t('deleteEntry')}
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Pagination */}
      <Pagination
        page={page}
        totalPages={Math.ceil(total / PAGE_SIZE)}
        onPageChange={setPage}
        prevLabel={t('prevPage')}
        nextLabel={t('nextPage')}
      />

      {/* Create modal */}
      {showCreate && (
        <CreateModal
          type={tab}
          onClose={() => setShowCreate(false)}
          onCreated={() => {
            setShowCreate(false)
            setPage(0)
            loadEntries(0, tab, sort, statusFilter)
          }}
        />
      )}

      {/* Confirm delete from list */}
      <ConfirmDialog
        open={deletePending !== null}
        title={t('deleteEntryConfirmTitle')}
        message={t('deleteEntryConfirmMessage')}
        confirmLabel={t('deleteEntryConfirm')}
        danger
        onConfirm={() => deletePending && handleDeleteFromList(deletePending)}
        onCancel={() => setDeletePending(null)}
      />
    </div>
  )
}
