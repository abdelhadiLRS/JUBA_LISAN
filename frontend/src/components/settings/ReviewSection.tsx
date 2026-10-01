'use client'

import { useEffect, useState } from 'react'
import { useTranslations } from 'next-intl'
import { Loader2, Trash2 } from 'lucide-react'
import { ReviewForm } from '@/components/reviews/ReviewPrompt'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import {
  createReview,
  deleteMyReview,
  fetchMyReview,
  updateMyReview,
} from '@/lib/reviews'
import type { ReviewAdmin } from '@/types/api'

export function ReviewSection({ title }: { title?: string } = {}) {
  const t = useTranslations('settings')
  const tReview = useTranslations('reviewPrompt')
  const [review, setReview] = useState<ReviewAdmin | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)
  const [deleted, setDeleted] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState(false)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError('')
    fetchMyReview()
      .then((data) => {
        if (!cancelled) setReview(data.review)
      })
      .catch(() => {
        if (!cancelled) setError(tReview('statusError'))
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [tReview])

  async function handleDelete() {
    setDeleting(true)
    setError('')
    try {
      await deleteMyReview()
      setReview(null)
      setDeleteConfirm(false)
      setDeleted(true)
      window.setTimeout(() => setDeleted(false), 2500)
    } catch {
      setError(t('reviewDeleteError'))
    } finally {
      setDeleting(false)
    }
  }

  return (
    <>
      <div className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-5 shadow-sm sm:p-6">
        <div className="mb-4 flex items-center gap-2 border-b border-[var(--duo-line)] pb-4">
          <span className="text-[var(--duo-muted)]">●</span>
          <span className="text-[10px] font-bold uppercase tracking-[0.12em] text-[var(--duo-muted)]">
            {title ?? t('sectionReview')}
          </span>
        </div>

        <p className="mb-1 text-sm leading-relaxed text-[var(--duo-muted)]">
          {t('reviewDescription')}
        </p>
        {review?.is_approved === false && (
          <p className="mb-4 text-xs font-semibold text-[var(--duo-muted)]">
            {t('reviewPending')}
          </p>
        )}

        {loading ? (
          <div className="flex items-center gap-2 py-5 text-xs text-[var(--duo-muted)]">
            <Loader2 className="size-4 animate-spin" /> {tReview('checking')}
          </div>
        ) : error ? (
          <p className="py-5 text-xs text-[var(--duo-red)]">{error}</p>
        ) : (
          <div className="-mx-5 border-t border-[var(--duo-line)] pt-1">
            <ReviewForm
              initialReview={review}
              submitLabel={review ? t('reviewUpdate') : tReview('submit')}
              onSubmit={async (data) => {
                const savedReview = review
                  ? await updateMyReview(data)
                  : await createReview(data)
                setReview(savedReview)
                setSaved(true)
                setDeleted(false)
                window.setTimeout(() => setSaved(false), 2500)
                return savedReview
              }}
            />
            {review && (
              <div className="px-5 pb-5">
                <button
                  type="button"
                  onClick={() => setDeleteConfirm(true)}
                  disabled={deleting}
                  className="flex w-full items-center justify-center gap-2 rounded-[10px] border border-[var(--duo-red)]/30 px-4 py-3 text-xs font-bold uppercase tracking-[0.08em] text-[var(--duo-red)] transition-colors hover:bg-[var(--duo-red)]/10 focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-red)] disabled:opacity-60"
                >
                  {deleting ? (
                    <Loader2 className="size-3.5 animate-spin" />
                  ) : (
                    <Trash2 className="size-3.5" />
                  )}
                  {t('reviewDelete')}
                </button>
              </div>
            )}
            {saved && (
              <p className="px-5 pb-5 text-xs font-semibold text-[var(--duo-green-dark)]">
                {t('reviewSaved')}
              </p>
            )}
            {deleted && (
              <p className="px-5 pb-5 text-xs font-semibold text-[var(--duo-green-dark)]">
                {t('reviewDeleted')}
              </p>
            )}
          </div>
        )}
      </div>

      <ConfirmDialog
        open={deleteConfirm}
        title={t('reviewDeleteTitle')}
        message={t('reviewDeleteMessage')}
        confirmLabel={t('reviewDeleteConfirm')}
        danger
        onCancel={() => setDeleteConfirm(false)}
        onConfirm={handleDelete}
      />
    </>
  )
}
