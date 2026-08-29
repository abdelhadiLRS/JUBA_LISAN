'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { BookMarked, Layers, Sparkles, Volume2 } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { VoiceRecorder } from '@/components/ui/VoiceRecorder'
import { PageLoading } from '@/components/ui/page-loading'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { CEFR_LEVELS } from '@/data/curriculum'

interface CardData {
  id: number
  word: string
  definition: string
  example_sentence: string
  translation: string
  ease_factor: number
  interval: number
  repetitions: number
  source?: string | null
}

const btnPrimary =
  'inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold text-white transition-colors disabled:opacity-50'
const btnSecondary =
  'inline-flex items-center justify-center gap-2 rounded-xl border border-fl-border px-4 py-2.5 text-sm font-medium transition-colors hover:bg-[var(--juba-surface-soft)]'

export default function FlashcardsPage() {
  const t = useTranslations('flashcards')
  const tCommon = useTranslations('common')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const [cards, setCards] = useState<CardData[]>([])
  const [current, setCurrent] = useState(0)
  const [flipped, setFlipped] = useState(false)
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [showGenerate, setShowGenerate] = useState(false)
  const [genTopic, setGenTopic] = useState('')
  const [genCount, setGenCount] = useState(10)
  const [genCefr, setGenCefr] = useState('B1')
  const [generating, setGenerating] = useState(false)
  const [genError, setGenError] = useState('')
  const [speakingMode, setSpeakingMode] = useState(false)

  const loadDue = useCallback(async () => {
    setLoading(true)
    try {
      const res = await apiFetch('/api/flashcards/due')
      if (res.ok) {
        const data = await res.json()
        setCards(data.due)
        setTotal(data.total)
        setCurrent(0)
        setFlipped(false)
      }
    } catch {
      /* ignore */
    } finally {
      setLoading(false)
    }
  }, [])

  const activeLangCode = activeLanguage?.code

  useEffect(() => {
    loadDue()
  }, [loadDue, activeLangCode])

  async function reviewCard(quality: number) {
    if (cards.length === 0) return
    const card = cards[current]
    await apiFetch(`/api/flashcards/${card.id}/review`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quality }),
    })
    if (current < cards.length - 1) {
      setCurrent(current + 1)
      setFlipped(false)
    } else {
      await loadDue()
    }
  }

  async function handleSpeakingTranscription(transcription: string) {
    if (cards.length === 0) return
    const card = cards[current]
    const norm = (s: string) =>
      s
        .trim()
        .toLowerCase()
        .replace(/[\p{P}\p{S}\s]+/gu, '')
    const isCorrect = norm(transcription) === norm(card.word)
    await reviewCard(isCorrect ? 5 : 2)
  }

  async function generateCards(e: React.FormEvent) {
    e.preventDefault()
    if (!genTopic.trim()) return
    setGenerating(true)
    setGenError('')
    try {
      const res = await apiFetch('/api/flashcards/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: genTopic.trim(),
          count: genCount,
          cefr_level: genCefr,
          target_language: activeLanguage?.code,
        }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || `Error ${res.status}`)
      }
      setShowGenerate(false)
      setGenTopic('')
      await loadDue()
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : ''
      setGenError(
        msg === 'No active study plan found'
          ? tCommon('noActivePlan')
          : tCommon('errorMessage')
      )
    } finally {
      setGenerating(false)
    }
  }

  if (loading) {
    return <PageLoading />
  }

  const targetLanguageCode = activeLanguage?.code ?? 'en-GB'
  const sessionProgress =
    cards.length > 0 ? Math.round((current / cards.length) * 100) : 0

  return (
    <div className="mx-auto max-w-4xl space-y-5 px-4 py-6 sm:px-6 md:py-8">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-fl-fg text-xl font-bold tracking-tight">
            {t('title')}
          </h1>
          <p className="text-fl-muted-2 mt-1 text-sm">
            {total} {t('total')} ·{' '}
            <span
              className="font-semibold"
              style={{ color: 'var(--juba-warm)' }}
            >
              {cards.length} {t('due')}
            </span>
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link href="/flashcards/vocabulary" className={btnSecondary}>
            <BookMarked className="h-4 w-4" aria-hidden="true" />
            {t('myVocabularyBtn')}
          </Link>
          <button
            onClick={() => {
              setShowGenerate(!showGenerate)
            }}
            className={`${btnPrimary} ${showGenerate ? 'bg-[var(--juba-primary-dark)]' : 'bg-[var(--juba-primary)] hover:bg-[var(--juba-primary-dark)]'}`}
          >
            <Sparkles className="h-4 w-4" aria-hidden="true" />
            {t('generateBtn')}
          </button>
        </div>
      </div>

      {/* Generate panel */}
      {showGenerate && (
        <div className="border-fl-border bg-fl-surface rounded-2xl border p-5">
          <p className="text-fl-muted-2 mb-4 text-xs font-semibold tracking-wide uppercase">
            {t('generate')}
          </p>
          {genError && (
            <div
              className="mb-4 rounded-xl px-4 py-3 text-sm"
              role="alert"
              style={{
                color: 'var(--juba-danger)',
                background:
                  'color-mix(in srgb, var(--juba-danger) 8%, transparent)',
                border:
                  '1px solid color-mix(in srgb, var(--juba-danger) 30%, transparent)',
              }}
            >
              {genError}
            </div>
          )}
          <form onSubmit={generateCards} className="space-y-4">
            <div>
              <label className="text-fl-muted-1 mb-2 block text-xs font-semibold tracking-wide uppercase">
                {t('topic')}
              </label>
              <input
                type="text"
                value={genTopic}
                onChange={(e) => setGenTopic(e.target.value)}
                required
                placeholder={t('topicPlaceholder')}
                className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-border-2 focus:border-fl-border-2 w-full rounded-xl border px-4 py-3 text-sm transition-colors focus:outline-none"
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-fl-muted-1 mb-2 block text-xs font-semibold tracking-wide uppercase">
                  {t('count')}
                </label>
                <select
                  value={genCount}
                  onChange={(e) => setGenCount(Number(e.target.value))}
                  className="bg-fl-bg border-fl-border text-fl-fg focus:border-fl-border-2 w-full rounded-xl border px-4 py-3 text-sm focus:outline-none"
                >
                  {[5, 10, 15, 20].map((n) => (
                    <option key={n} value={n}>
                      {n} {t('cards')}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-fl-muted-1 mb-2 block text-xs font-semibold tracking-wide uppercase">
                  {t('level')}
                </label>
                <select
                  value={genCefr}
                  onChange={(e) => setGenCefr(e.target.value)}
                  className="bg-fl-bg border-fl-border text-fl-fg focus:border-fl-border-2 w-full rounded-xl border px-4 py-3 text-sm focus:outline-none"
                >
                  {CEFR_LEVELS.map((l) => (
                    <option key={l} value={l}>
                      {l}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <button
              type="submit"
              disabled={generating || !genTopic.trim()}
              className={`${btnPrimary} w-full bg-[var(--juba-primary)] hover:bg-[var(--juba-primary-dark)]`}
            >
              {generating ? (
                <>
                  <Layers
                    className="h-4 w-4 animate-pulse"
                    aria-hidden="true"
                  />
                  {t('generating')}
                </>
              ) : (
                t('submit')
              )}
            </button>
          </form>
        </div>
      )}

      {/* No cards */}
      {cards.length === 0 && (
        <div className="border-fl-border bg-fl-surface rounded-2xl border px-6 py-12 text-center">
          <span
            className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-2xl"
            style={{
              color: 'var(--juba-primary)',
              background: 'var(--juba-primary-soft)',
            }}
          >
            <CheckBadgeIcon />
          </span>
          <p className="text-fl-muted-1 text-sm font-medium">{t('noDue')}</p>
          {total === 0 && (
            <p className="text-fl-muted-2 mt-2 text-sm">{t('noCardsHint')}</p>
          )}
          <button onClick={loadDue} className={btnSecondary + ' mt-6'}>
            {t('refresh')}
          </button>
        </div>
      )}

      {/* Card review */}
      {cards.length > 0 && (
        <>
          {/* Session progress */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-fl-muted-2 text-xs font-semibold">
                {current + 1} / {cards.length} due
              </span>
              {/* Mode toggle */}
              <div className="bg-fl-surface-2 inline-flex rounded-xl p-1">
                <button
                  onClick={() => {
                    setSpeakingMode(false)
                    setFlipped(false)
                  }}
                  className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                    !speakingMode
                      ? 'text-fl-fg bg-[var(--juba-surface)] shadow-sm'
                      : 'text-fl-muted-2 hover:text-fl-fg'
                  }`}
                >
                  {t('standardMode')}
                </button>
                <button
                  onClick={() => {
                    setSpeakingMode(true)
                    setFlipped(false)
                  }}
                  className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                    speakingMode
                      ? 'text-fl-fg bg-[var(--juba-surface)] shadow-sm'
                      : 'text-fl-muted-2 hover:text-fl-fg'
                  }`}
                >
                  {t('speakingMode')}
                </button>
              </div>
            </div>
            <div className="bg-fl-surface-2 h-1.5 overflow-hidden rounded-full">
              <div
                className="h-full rounded-full transition-all duration-500"
                style={{
                  width: `${sessionProgress}%`,
                  background: 'var(--juba-primary)',
                }}
              />
            </div>
          </div>

          {/* ── Standard mode ── */}
          {!speakingMode && (
            <>
              <div
                className="juba-card cursor-pointer select-none"
                onClick={() => setFlipped(!flipped)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    setFlipped(!flipped)
                  }
                }}
                aria-label={flipped ? t('tapToHide') : t('tapToReveal')}
              >
                <div className="border-fl-border flex items-center justify-between border-b px-6 py-3.5">
                  <span className="text-fl-muted-2 text-xs font-semibold tracking-wide uppercase">
                    {flipped ? t('back') : t('front')}
                  </span>
                  <span className="text-fl-muted-3 text-xs">
                    {flipped ? t('tapToHide') : t('tapToReveal')}
                  </span>
                </div>

                <div className="flex flex-col items-center justify-center gap-4 p-10 text-center">
                  {!flipped ? (
                    <div className="flex items-center gap-3">
                      <TargetLanguageText
                        as="p"
                        languageCode={targetLanguageCode}
                        className="text-fl-fg text-3xl font-bold"
                      >
                        {cards[current].word}
                      </TargetLanguageText>
                      <span onClick={(e) => e.stopPropagation()}>
                        <AudioPlayer text={cards[current].word} size="md" />
                      </span>
                    </div>
                  ) : (
                    <>
                      <TargetLanguageText
                        as="p"
                        languageCode={targetLanguageCode}
                        className="text-fl-fg-2"
                      >
                        {cards[current].definition}
                      </TargetLanguageText>
                      {cards[current].example_sentence && (
                        <TargetLanguageText
                          as="p"
                          languageCode={targetLanguageCode}
                          className="text-fl-muted-1 italic"
                        >
                          {cards[current].example_sentence}
                        </TargetLanguageText>
                      )}
                      {cards[current].translation && (
                        <p className="text-fl-muted-3 border-fl-border mt-1 border-t pt-3 text-sm">
                          {cards[current].translation}
                        </p>
                      )}
                    </>
                  )}
                </div>
              </div>

              {flipped && (
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                  {[
                    {
                      key: 'again',
                      q: 0,
                      style: { color: 'var(--juba-danger)' },
                    },
                    {
                      key: 'hard',
                      q: 3,
                      style: { color: 'var(--juba-muted)' },
                    },
                    { key: 'good', q: 4, style: { color: 'var(--juba-text)' } },
                    {
                      key: 'easy',
                      q: 5,
                      style: {
                        color: 'var(--juba-primary-dark)',
                        borderColor:
                          'color-mix(in srgb, var(--juba-primary) 45%, var(--juba-border))',
                      },
                    },
                  ].map(({ key, q, style }) => (
                    <button
                      key={q}
                      onClick={() => reviewCard(q)}
                      className="border-fl-border min-w-[80px] rounded-xl border py-3 text-sm font-semibold transition-all hover:border-[color-mix(in_srgb,var(--juba-border)_60%,var(--juba-text))] hover:bg-[var(--juba-surface-soft)]"
                      style={style}
                    >
                      {t(key)}
                    </button>
                  ))}
                </div>
              )}
            </>
          )}

          {/* ── Speaking mode ── */}
          {speakingMode && (
            <div className="border-fl-border bg-fl-surface rounded-2xl border">
              <div className="border-fl-border flex items-center justify-between border-b px-5 py-3.5">
                <p className="text-fl-muted-2 text-xs font-semibold tracking-wide uppercase">
                  {t('speakingMode')}
                </p>
                <span className="flex items-center gap-1.5 text-xs text-[var(--juba-muted)]">
                  <Volume2 className="h-3.5 w-3.5" aria-hidden="true" />
                  {t('sayWord')}
                </span>
              </div>

              <div className="flex flex-col items-center justify-center gap-5 p-10 text-center">
                <TargetLanguageText
                  as="p"
                  languageCode={targetLanguageCode}
                  className="text-fl-fg-2"
                >
                  {cards[current].definition}
                </TargetLanguageText>
                {cards[current].example_sentence && (
                  <TargetLanguageText
                    as="p"
                    languageCode={targetLanguageCode}
                    className="text-fl-muted-1 italic"
                  >
                    {cards[current].example_sentence}
                  </TargetLanguageText>
                )}
                {cards[current].translation && (
                  <p className="text-fl-muted-3 border-fl-border mt-1 border-t pt-3 text-sm">
                    {cards[current].translation}
                  </p>
                )}
                <VoiceRecorder
                  onTranscription={handleSpeakingTranscription}
                  maxSeconds={5}
                  className="mt-2"
                />
              </div>
            </div>
          )}

          <p className="text-fl-muted-4 text-center text-xs tabular-nums">
            EF {cards[current].ease_factor.toFixed(2)} · {t('interval')}{' '}
            {cards[current].interval}d · {t('repetitions')}{' '}
            {cards[current].repetitions}
          </p>
        </>
      )}
    </div>
  )
}

function CheckBadgeIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-6 w-6"
      aria-hidden="true"
    >
      <path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z" />
      <path d="m9 12 2 2 4-4" />
    </svg>
  )
}
