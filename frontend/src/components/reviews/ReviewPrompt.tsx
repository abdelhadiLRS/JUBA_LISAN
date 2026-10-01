'use client'

import { useEffect, useState } from 'react'
import { useTranslations } from 'next-intl'
import { Loader2, Star, X } from 'lucide-react'
import { createReview, fetchMyReview } from '@/lib/reviews'
import type { ReviewAdmin } from '@/types/api'

const DISMISS_KEY = 'freelingo:reviewPromptDismissed'

export function getReviewPromptDismissal(): {
  count: number
  lastDismissedAt: number
} {
  if (typeof window === 'undefined') return { count: 0, lastDismissedAt: 0 }
  try {
    const raw = window.localStorage.getItem(DISMISS_KEY)
    if (!raw) return { count: 0, lastDismissedAt: 0 }
    const parsed = JSON.parse(raw) as {
      count?: number
      lastDismissedAt?: number
    }
    return {
      count: Number(parsed.count) || 0,
      lastDismissedAt: Number(parsed.lastDismissedAt) || 0,
    }
  } catch {
    return { count: 0, lastDismissedAt: 0 }
  }
}

export function recordReviewPromptDismissal(): void {
  if (typeof window === 'undefined') return
  const current = getReviewPromptDismissal()
  window.localStorage.setItem(
    DISMISS_KEY,
    JSON.stringify({ count: current.count + 1, lastDismissedAt: Date.now() })
  )
}

interface ReviewPromptProps {
  open: boolean
  onClose: () => void
  onSubmitted?: (review: ReviewAdmin) => void
}

interface ReviewFormProps {
  initialReview?: ReviewAdmin | null
  submitLabel?: string
  cancelLabel?: string
  onCancel?: () => void
  onSubmit: (data: { rating: number; comment?: string }) => Promise<ReviewAdmin>
}

export function ReviewForm({
  initialReview,
  submitLabel,
  cancelLabel,
  onCancel,
  onSubmit,
}: ReviewFormProps) {
  const t = useTranslations('reviewPrompt')
  const [rating, setRating] = useState(initialReview?.rating ?? 0)
  const [comment, setComment] = useState(initialReview?.comment ?? '')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    setRating(initialReview?.rating ?? 0)
    setComment(initialReview?.comment ?? '')
  }, [initialReview])

  async function handleSubmit() {
    if (!rating) {
      setError(t('ratingRequiredError'))
      return
    }
    setSubmitting(true)
    setError('')
    try {
      await onSubmit({ rating, comment: comment.trim() || undefined })
    } catch {
      setError(t('saveError'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <>
      <div className="space-y-5 px-5 py-5">
        <div>
          <p className="text-[var(--duo-muted)] mb-3 font-mono tracking-widest uppercase">
            {t('ratingLabel')}
          </p>
          <div
            className="flex gap-2"
            role="radiogroup"
            aria-label={t('ratingGroupLabel')}
          >
            {[1, 2, 3, 4, 5].map((value) => (
              <button
                key={value}
                type="button"
                role="radio"
                aria-checked={rating === value}
                aria-label={`${value} ${t(value === 1 ? 'star' : 'stars')}`}
                onClick={() => setRating(value)}
                className={`rounded-[10px] border px-3 py-2 transition-colors ${
                  value <= rating
                    ? 'border-[var(--duo-yellow)] text-[var(--duo-yellow)]'
                    : 'border-[var(--duo-line)] text-[var(--duo-muted)] hover:text-[var(--duo-ink)]'
                }`}
              >
                <Star className="size-5 fill-current" />
              </button>
            ))}
          </div>
        </div>

        <div>
          <label
            htmlFor="review-comment"
            className="text-[var(--duo-muted)] mb-2 block font-mono tracking-widest uppercase"
          >
            {t('commentLabel')}
          </label>
          <textarea
            id="review-comment"
            value={comment}
            onChange={(event) => setComment(event.target.value)}
            maxLength={2000}
            rows={4}
            className="border-[var(--duo-line)] bg-[var(--duo-bg)] text-[var(--duo-ink)] placeholder:text-[var(--duo-muted)] focus:border-[var(--duo-green)] w-full resize-none rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] px-3 py-2 font-mono text-sm outline-none"
            placeholder={t('commentPlaceholder')}
          />
        </div>

        {error && <p className="text-[var(--duo-red)] font-mono text-xs">{error}</p>}
      </div>

      <div className="flex gap-2 px-5 pb-5">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 rounded-[10px] border border-[var(--duo-line)] py-3 font-mono font-bold tracking-widest text-[var(--duo-muted)] uppercase transition-colors hover:bg-[var(--duo-bg)] hover:text-[var(--duo-ink)]"
          >
            {cancelLabel ?? t('cancel')}
          </button>
        )}
        <button
          type="button"
          onClick={handleSubmit}
          disabled={submitting}
          className="flex flex-1 items-center justify-center gap-2 rounded-[10px] bg-[var(--duo-green)] py-3 font-mono font-bold tracking-widest text-white uppercase shadow-sm transition-colors hover:bg-[var(--duo-green-dark)] disabled:opacity-60"
        >
          {submitting && <Loader2 className="size-3.5 animate-spin" />}
          {submitLabel ?? t('submit')}
        </button>
      </div>
    </>
  )
}

export function ReviewPrompt({
  open,
  onClose,
  onSubmitted,
}: ReviewPromptProps) {
  const t = useTranslations('reviewPrompt')
  const [checking, setChecking] = useState(false)
  const [hasReview, setHasReview] = useState(false)
  const [error, setError] = useState('')
  const [statusCheckFailed, setStatusCheckFailed] = useState(false)

  useEffect(() => {
    if (!open) return
    let cancelled = false
    setChecking(true)
    setError('')
    setStatusCheckFailed(false)
    fetchMyReview()
      .then((data) => {
        if (cancelled) return
        setHasReview(data.has_review)
      })
      .catch(() => {
        if (cancelled) return
        setStatusCheckFailed(true)
        setError(t('statusError'))
      })
      .finally(() => {
        if (!cancelled) setChecking(false)
      })
    return () => {
      cancelled = true
    }
  }, [open, t])

  if (!open || hasReview) return null

  function handleCancel() {
    recordReviewPromptDismissal()
    onClose()
  }

  return (
    <div className="fixed inset-0 z-[180] flex items-center justify-center bg-[color-mix(in_srgb,var(--duo-ink)_55%,transparent)] p-4 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] shadow-sm">
        <div className="flex items-center justify-between border-b border-[var(--duo-line)] px-5 py-4">
          <div>
            <p className="text-[var(--duo-muted)] font-mono tracking-widest uppercase">
              {t('eyebrow')}
            </p>
            <h2 className="text-[var(--duo-ink)] mt-1 font-sans text-lg font-semibold tracking-tight">
              {t('title')}
            </h2>
          </div>
          <button
            type="button"
            onClick={handleCancel}
            className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] p-2 transition-colors"
            aria-label={t('closeLabel')}
          >
            <X className="size-4" />
          </button>
        </div>

        {checking ? (
          <div className="px-5 py-5">
            <div className="text-[var(--duo-muted)] flex items-center gap-2 font-mono text-xs">
              <Loader2 className="size-4 animate-spin" /> {t('checking')}
            </div>
          </div>
        ) : statusCheckFailed ? (
          <div className="px-5 py-5">
            <p className="text-[var(--duo-red)] font-mono text-xs">{error}</p>
          </div>
        ) : (
          <ReviewForm
            onCancel={handleCancel}
            onSubmit={async (data) => {
              const review = await createReview(data)
              onSubmitted?.(review)
              onClose()
              return review
            }}
          />
        )}
      </div>
    </div>
  )
}
