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
  pending: 'border-[var(--juba-lilac)] text-[var(--juba-muted)]',
  planned: 'border-blue-500/40 text-blue-400',
  in_progress: 'border-yellow-500/40 text-yellow-400',
  done: 'border-green-500/40 text-green-400',
  declined: 'border-rose-200/30 text-rose-700',
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
      className={`text-[var(--juba-muted)] border-2 px-2 py-0.5 font-semibold tracking-wide ${cls}`}
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
    'w-full bg-[var(--juba-bg)] border-2 border-[var(--juba-lilac)] px-4 py-3 text-sm text-[var(--juba-text)] placeholder:text-[var(--juba-muted)] focus:outline-none focus:border-[var(--juba-violet)] transition-colors resize-none'
  const textareaCls =
    'w-full bg-[var(--juba-bg)] border-2 border-[var(--juba-lilac)] px-4 py-3 text-sm text-[var(--juba-text)] placeholder:text-[var(--juba-muted)] focus:outline-none focus:border-[var(--juba-violet)] transition-colors resize-y min-h-[106px]'

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
        backgroundColor: 'rgba(0,0,0,0.7)',
        backdropFilter: 'blur(2px)',
      }}
      onClick={onClose}
    >
      <div
        className="border-[var(--juba-lilac)] bg-white w-full max-w-md border-2 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="border-[var(--juba-lilac)] flex items-center justify-between border-b px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="text-[var(--juba-text)] text-[var(--juba-muted)]">●</span>
            <span className="text-[var(--juba-text)] text-[var(--juba-muted)] font-semibold tracking-wide">
              {type === 'feature'
                ? t('modalCreateTitleFeature')
                : t('modalCreateTitleBug')}
            </span>
          </div>
          <button
            onClick={onClose}
            className="text-[var(--juba-text)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] font-mono transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-3 p-6">
          {error && (
            <div className="border-rose-200/40 text-rose-700 border-2 px-4 py-3 text-sm">
              ✕ {error}
            </div>
          )}
          <div>
            <label className="text-[var(--juba-muted)] text-[var(--juba-muted)] mb-1 block font-semibold tracking-wide">
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
            <label className="text-[var(--juba-muted)] text-[var(--juba-muted)] mb-1 block font-semibold tracking-wide">
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
              className="border-[var(--juba-lilac)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)] flex-1 border-2 px-4 py-3 text-sm tracking-widest uppercase transition-colors"
            >
              {t('cancel')}
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="bg-[var(--juba-violet)] text-white hover:bg-[var(--juba-violet)]/90 flex-1 py-3 text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-50"
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
        className="text-[var(--juba-text)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] font-semibold tracking-wide transition-colors"
      >
        {t('backToList')}
      </button>

      {/* Entry card */}
      <div className="rounded-[28px] border-2 border-[var(--juba-lilac)] bg-white shadow-[var(--juba-shadow-sm)]">
        <div className="border-[var(--juba-lilac)] space-y-3 border-b px-6 py-5">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <h2 className="text-[var(--juba-text)] min-w-0 flex-1 font-mono text-base leading-snug font-bold">
              {entry.title}
            </h2>
            <StatusBadge status={entry.status} label={statusLabel} />
          </div>
          <p className="text-[var(--juba-muted)] text-sm leading-relaxed whitespace-pre-wrap">
            {entry.description}
          </p>
          <div className="flex flex-wrap items-center gap-3 pt-1">
            <span className="text-[var(--juba-muted)] text-[var(--juba-muted)] inline-flex flex-wrap items-center gap-x-1 font-mono">
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
                className={`text-[var(--juba-muted)] border-2 px-3 py-1 font-semibold tracking-wide transition-colors disabled:opacity-50 ${
                  entry.voted_by_me
                    ? 'border-[var(--juba-violet)]/60 text-fl-accent bg-[var(--juba-violet)]/10'
                    : 'border-[var(--juba-lilac)] text-[var(--juba-muted)] hover:border-[var(--juba-violet)] hover:text-[var(--juba-text)]'
                }`}
              >
                ▲ {entry.vote_count}
              </button>
            )}
            {/* Delete — author or admin */}
            {(currentUserId === entry.author.id || isAdmin) && (
              <button
                onClick={() => setDeleteEntryPending(true)}
                className="text-[var(--juba-muted)] border-rose-200/30 text-rose-700 hover:border-rose-200 ml-auto border-2 px-3 py-1 font-semibold tracking-wide transition-colors"
              >
                {t('deleteEntry')}
              </button>
            )}
          </div>
        </div>

        {/* Comments */}
        <div className="divide-fl-border-2 divide-y">
          {comments.length === 0 ? (
            <p className="text-[var(--juba-muted)] px-6 py-6 text-center text-sm">
              {t('addComment')}
            </p>
          ) : (
            comments.map((c) => (
              <div key={c.id} className="space-y-1 px-6 py-4">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[var(--juba-muted)] text-[var(--juba-muted)] inline-flex flex-wrap items-center gap-x-1 font-mono">
                    <span>{c.author.display_name}</span>
                    <AdminAuthorBadge role={c.author.role} />
                    <span>· {formatDate(c.created_at)}</span>
                  </span>
                  {currentUserId === c.author.id && (
                    <button
                      onClick={() => setDeletePendingComment(c)}
                      className="text-[var(--juba-muted)] text-[var(--juba-muted)] hover:text-rose-700 font-semibold tracking-wide transition-colors"
                    >
                      {t('deleteComment')}
                    </button>
                  )}
                </div>
                <p className="text-[var(--juba-muted)] text-sm leading-relaxed whitespace-pre-wrap">
                  {c.body}
                </p>
              </div>
            ))
          )}
        </div>

        {/* Add comment form */}
        <form
          onSubmit={handlePostComment}
          className="border-[var(--juba-lilac)] space-y-2 border-t px-6 py-4"
        >
          {error && (
            <div className="border-rose-200/40 text-rose-700 border-2 px-4 py-2 text-sm">
              ✕ {error}
            </div>
          )}
          <textarea
            rows={2}
            value={commentBody}
            onChange={(e) => setCommentBody(e.target.value)}
            placeholder={t('commentPlaceholder')}
            maxLength={2000}
            className="bg-[var(--juba-bg)] border-[var(--juba-lilac)] text-[var(--juba-text)] placeholder:text-[var(--juba-muted)] focus:border-[var(--juba-violet)] min-h-[50px] w-full resize-y border-2 px-4 py-2 text-sm transition-colors focus:outline-none"
          />
          <button
            type="submit"
            disabled={postingComment || !commentBody.trim()}
            className="border-[var(--juba-lilac)] text-[var(--juba-text)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] hover:border-[var(--juba-violet)] border-2 px-4 py-2 font-semibold tracking-wide transition-colors disabled:cursor-not-allowed disabled:opacity-30"
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
      <div className="mx-auto max-w-5xl space-y-6 p-5 sm:p-8">
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
    <div className="mx-auto max-w-4xl space-y-4 p-6">
      {/* Page header */}
      <div className="border-[var(--juba-lilac)] border-b pb-4">
        <p className="text-[var(--juba-text)] text-[var(--juba-muted)] mb-1 font-semibold tracking-wide">
          {t('title')}
        </p>
        <h1 className="text-[var(--juba-text)] font-mono text-2xl font-bold tracking-tight">
          {t('subtitle')}
        </h1>
      </div>

      {/* Tabs */}
      <div className="border-[var(--juba-lilac)] flex border-b">
        {(['feature', 'bug'] as Tab[]).map((tabOption) => (
          <button
            key={tabOption}
            onClick={() => setTab(tabOption)}
            className={`text-[var(--juba-text)] -mb-px border-b-2 px-5 py-2 font-semibold tracking-wide transition-colors ${
              tab === tabOption
                ? 'border-fl-fg text-[var(--juba-text)]'
                : 'text-[var(--juba-muted)] hover:text-[var(--juba-text)] border-transparent'
            }`}
          >
            {tabOption === 'feature' ? t('tabFeatures') : t('tabBugs')}
          </button>
        ))}
        <div className="flex-1" />
        <button
          onClick={() => setShowCreate(true)}
          className="text-[var(--juba-text)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] px-4 py-2 font-semibold tracking-wide transition-colors"
        >
          {tab === 'feature' ? t('newFeature') : t('newBug')}
        </button>
      </div>

      {/* Filters + sort row */}
      <div className="flex flex-wrap items-center gap-3">
        <span className="text-[var(--juba-muted)] text-[var(--juba-muted)] font-semibold tracking-wide">
          {t('sortBy')}
        </span>
        {(['votes', 'date'] as SortOption[]).map((s) => (
          <button
            key={s}
            onClick={() => setSort(s)}
            className={`text-[var(--juba-muted)] border-2 px-3 py-1 font-semibold tracking-wide transition-colors ${
              sort === s
                ? 'border-fl-fg/40 text-[var(--juba-text)]'
                : 'border-[var(--juba-lilac)] text-[var(--juba-muted)] hover:border-[var(--juba-violet)] hover:text-[var(--juba-text)]'
            }`}
          >
            {s === 'votes' ? t('sortVotes') : t('sortDate')}
          </button>
        ))}

        <span className="text-[var(--juba-muted)] text-[var(--juba-muted)] ml-2 font-semibold tracking-wide">
          {t('filterStatus')}
        </span>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="bg-[var(--juba-bg)] border-[var(--juba-lilac)] text-[var(--juba-muted)] text-[var(--juba-muted)] focus:border-[var(--juba-violet)] appearance-none border-2 px-3 py-1 font-mono transition-colors focus:outline-none"
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
        <div className="border-rose-200/40 text-rose-700 border-2 px-4 py-3 text-sm">
          ✕ {error}
        </div>
      )}

      {/* List */}
      <div className="rounded-[28px] border-2 border-[var(--juba-lilac)] bg-white shadow-[var(--juba-shadow-sm)]">
        {loading ? (
          <PageLoading
            fullScreen={false}
            className="block px-6 py-10 text-center"
          />
        ) : entries.length === 0 ? (
          <p className="text-[var(--juba-muted)] px-6 py-10 text-center text-sm">
            {t('noEntries')}
          </p>
        ) : (
          <div>
            {entries.map((entry, i) => {
              const canDelete = currentUserId === entry.author.id || isAdmin
              return (
                <div
                  key={entry.id}
                  className={`hover:bg-[var(--juba-lilac)] flex cursor-pointer gap-4 px-5 py-4 transition-colors ${
                    i < entries.length - 1 ? 'border-[var(--juba-lilac)] border-b' : ''
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
                        className={`border-2 px-2 py-1 text-sm leading-none transition-colors ${
                          entry.voted_by_me
                            ? 'border-[var(--juba-violet)]/60 text-fl-accent bg-[var(--juba-violet)]/10'
                            : 'border-[var(--juba-lilac)] text-[var(--juba-muted)] hover:border-[var(--juba-violet)] hover:text-[var(--juba-text)]'
                        }`}
                        title={entry.voted_by_me ? 'Remove vote' : 'Vote'}
                      >
                        ▲
                      </button>
                      <span className="text-[var(--juba-muted)] text-[var(--juba-muted)] font-mono tabular-nums">
                        {entry.vote_count}
                      </span>
                    </div>
                  )}
                  {/* Bug entries — show placeholder column for alignment */}
                  {entry.type === 'bug' && <div className="w-8 shrink-0" />}

                  {/* Content */}
                  <div className="min-w-0 flex-1 space-y-1.5">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-[var(--juba-text)] truncate text-sm font-semibold">
                        {entry.title}
                      </span>
                      <StatusBadge
                        status={entry.status}
                        label={getStatusLabel(entry.status)}
                      />
                      {entry.unread_by_me && (
                        <span className="border-2 border-red-500/40 px-2 py-0.5 font-mono text-[10px] leading-none font-bold tracking-widest text-red-400 uppercase">
                          {t('unread')}
                        </span>
                      )}
                    </div>
                    <p className="text-[var(--juba-muted)] line-clamp-2 text-sm leading-relaxed">
                      {entry.description}
                    </p>
                    <div className="flex flex-wrap items-center gap-3">
                      <span className="text-[var(--juba-muted)] text-[var(--juba-muted)] inline-flex flex-wrap items-center gap-x-1 font-mono">
                        <span>
                          {t('by')} {entry.author.display_name}
                        </span>
                        <AdminAuthorBadge role={entry.author.role} />
                        <span>· {formatDate(entry.created_at)}</span>
                      </span>
                      {entry.comment_count > 0 && (
                        <span className="text-[var(--juba-muted)] text-[var(--juba-muted)] font-mono">
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
                          className="text-[var(--juba-muted)] text-[var(--juba-muted)] hover:text-rose-700 ml-auto font-semibold tracking-wide transition-colors"
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
