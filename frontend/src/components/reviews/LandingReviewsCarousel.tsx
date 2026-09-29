'use client'

import { useEffect, useRef } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { Star } from 'lucide-react'
import { getLanguageByCode } from '@/lib/target-languages'
import type { ReviewPublic } from '@/types/api'

function Stars({ rating, label }: { rating: number; label: string }) {
  return (
    <div className="flex gap-1" aria-label={label}>
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          className={`size-4 ${star <= rating ? 'fill-yellow-400 text-yellow-400' : 'text-[var(--busuu-muted)]'}`}
          aria-hidden="true"
        />
      ))}
    </div>
  )
}

export function LandingReviewsCarousel({
  reviews,
}: {
  reviews: ReviewPublic[]
}) {
  const t = useTranslations('landingReviews')
  const tTarget = useTranslations('targetLanguages')
  const locale = useLocale()
  const scrollerRef = useRef<HTMLDivElement | null>(null)

  function languageLabel(code: string) {
    const language = getLanguageByCode(code)
    return language ? tTarget(language.iso639) : code
  }

  useEffect(() => {
    const scroller = scrollerRef.current
    if (!scroller || reviews.length <= 1) return
    const interval = window.setInterval(() => {
      const nextLeft = scroller.scrollLeft + 320
      const maxLeft = scroller.scrollWidth - scroller.clientWidth
      const isAtEnd = scroller.scrollLeft >= maxLeft - 1
      scroller.scrollTo({
        left: isAtEnd ? 0 : Math.min(nextLeft, maxLeft),
        behavior: 'smooth',
      })
    }, 3500)
    return () => window.clearInterval(interval)
  }, [reviews.length])

  if (!reviews.length) return null

  const averageRating =
    reviews.reduce((total, review) => total + review.rating, 0) / reviews.length
  const formattedAverage = new Intl.NumberFormat(locale, {
    maximumFractionDigits: 1,
    minimumFractionDigits: 1,
  }).format(averageRating)

  return (
    <section
      className="juba-ff-reviews mx-auto w-full max-w-5xl scroll-mt-16 px-6 pb-24 text-[var(--busuu-ink)]"
      aria-labelledby="reviews-title"
    >
      <div className="mb-8 flex flex-col gap-3 text-center">
        <span className="text-[var(--busuu-muted)] font-sans text-xs font-bold tracking-wide">
          {t('eyebrow')}
        </span>
        <h2
          id="reviews-title"
          className="text-[var(--busuu-ink)] font-sans text-2xl font-bold tracking-tight md:text-4xl"
        >
          {t('title')}
        </h2>
        <p className="text-[var(--busuu-muted)] mx-auto max-w-2xl font-sans text-sm leading-7">
          {t('subtitle')}
        </p>
        <div className="border-[var(--busuu-line)] bg-[var(--busuu-card)]/60 text-[var(--busuu-muted)] mx-auto inline-flex items-center gap-2 border px-3 py-2 font-sans text-xs font-bold tracking-wide">
          <Star
            className="size-3.5 fill-yellow-400 text-yellow-400"
            aria-hidden="true"
          />
          <span>
            {t('averageLabel', {
              average: formattedAverage,
              count: reviews.length,
            })}
          </span>
        </div>
      </div>

      <div
        ref={scrollerRef}
        className={`scrollbar-thumb-[var(--landing-border)] flex snap-x scrollbar-thin scrollbar-track-transparent gap-4 overflow-x-auto pb-3 ${reviews.length === 1 ? 'justify-center' : ''}`}
      >
        {reviews.map((review) => (
          <article
            key={review.id}
            className="juba-ff-review-card border-[var(--busuu-line)] bg-[var(--busuu-card)] flex min-h-52 w-[280px] flex-none snap-start flex-col border p-5 sm:w-[340px]"
          >
            <div className="mb-4 flex items-start justify-between gap-4">
              <div>
                <h3 className="text-[var(--busuu-ink)] font-sans text-sm font-semibold tracking-tight">
                  {review.user_display_name}
                </h3>
                <p className="text-[var(--busuu-muted)] mt-1 font-sans text-xs font-bold tracking-wide">
                  {t('learningLanguage', {
                    language: languageLabel(review.target_language),
                  })}
                </p>
              </div>
              <Stars
                rating={review.rating}
                label={t('starsLabel', { rating: review.rating })}
              />
            </div>
            <p className="text-[var(--busuu-muted)] line-clamp-6 font-sans text-sm leading-7">
              {review.comment || t('ratingOnly')}
            </p>
          </article>
        ))}
      </div>
    </section>
  )
}
