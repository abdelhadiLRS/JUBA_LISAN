'use client'

import FlashcardsPage from '../flashcards/page'

/**
 * JUBA LISAN Review is the learner-facing entry point for spaced repetition.
 * The existing flashcard engine remains the single source of truth for due
 * items and review scheduling, while this route gives the product a stable,
 * language-first destination for the Review navigation item.
 */
export default function ReviewPage() {
  return <FlashcardsPage />
}
