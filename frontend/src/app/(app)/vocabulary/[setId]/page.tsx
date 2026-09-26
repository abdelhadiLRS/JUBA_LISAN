'use client'

import { useState, useEffect, use, useCallback } from 'react'
import { notFound, useRouter } from 'next/navigation'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { PageLoading } from '@/components/ui/page-loading'
import type { VocabularyNativeHelp, VocabularySet } from '@/data/types'
import { useLanguageStore } from '@/store/language'
import { useAuthStore } from '@/store/auth'
import { apiFetch } from '@/lib/api'
import { TargetLanguageText } from '@/components/TargetLanguageText'

const POS_LABELS: Record<string, string> = {
  noun: 'n.',
  verb: 'v.',
  adjective: 'adj.',
  adverb: 'adv.',
  phrase: 'phr.',
  conjunction: 'conj.',
  preposition: 'prep.',
  numeral: 'num.',
  pronoun: 'pron.',
}

export default function VocabularySetPage({
  params,
}: {
  params: Promise<{ setId: string }>
}) {
  const { setId } = use(params)
  const router = useRouter()
  const t = useTranslations('vocabulary')
  const tCommon = useTranslations('common')
  const tTargetLang = useTranslations('targetLanguages')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const user = useAuthStore((s) => s.user)
  const [vocabSet, setVocabSet] = useState<VocabularySet | null>(null)
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [addedCount, setAddedCount] = useState<number | null>(null)
  const [error, setError] = useState('')
  const [nativeHelpOpen, setNativeHelpOpen] = useState(false)
  const [nativeHelp, setNativeHelp] = useState<VocabularyNativeHelp | null>(
    null
  )
  const [loadingNativeHelp, setLoadingNativeHelp] = useState(false)
  const [nativeHelpError, setNativeHelpError] = useState(false)
  const nativeLanguageName = user?.native_language
    ? tTargetLang(user.native_language)
    : ''

  useEffect(() => {
    const lang = activeLanguage?.code ?? 'en-GB'
    setLoading(true)
    apiFetch(`/api/vocabulary/${encodeURIComponent(setId)}?language=${lang}`)
      .then((r) => {
        if (!r.ok) throw new Error('not found')
        return r.json()
      })
      .then((d: { set: VocabularySet }) => setVocabSet(d.set))
      .catch(() => setVocabSet(null))
      .finally(() => setLoading(false))
  }, [setId, activeLanguage?.code])

  useEffect(() => {
    setNativeHelpOpen(false)
    setNativeHelp(null)
    setNativeHelpError(false)
  }, [setId, activeLanguage?.code])

  const targetLanguageCode = activeLanguage?.code ?? 'en-GB'

  const generateNativeHelp = useCallback(async () => {
    if (loadingNativeHelp) return
    setLoadingNativeHelp(true)
    setNativeHelpError(false)
    try {
      const res = await apiFetch(
        `/api/vocabulary/${encodeURIComponent(setId)}/native-help?language=${targetLanguageCode}`,
        { method: 'POST' }
      )
      if (!res.ok) throw new Error('native help failed')
      const data = (await res.json()) as { native_help: VocabularyNativeHelp }
      setNativeHelp(data.native_help)
    } catch {
      setNativeHelpError(true)
    } finally {
      setLoadingNativeHelp(false)
    }
  }, [loadingNativeHelp, setId, targetLanguageCode])

  if (loading) {
    return <PageLoading />
  }

  if (!vocabSet) notFound()

  async function handleAddAll() {
    if (!vocabSet) return
    setAdding(true)
    setError('')
    try {
      const cards = vocabSet.words.map((w) => ({
        word: w.word,
        definition: w.definition,
        example_sentence: w.example,
        translation: '', // user's native language translation will be added by LLM generation
      }))
      const res = await apiFetch('/api/flashcards/bulk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ flashcards: cards }),
      })
      if (!res.ok) {
        const d = await res.json().catch(() => ({}))
        throw new Error(
          (d as { detail?: string }).detail ?? `Error ${res.status}`
        )
      }
      const data = (await res.json()) as { created: number }
      setAddedCount(data.created)
    } catch (err) {
      const msg = err instanceof Error ? err.message : ''
      setError(
        msg === 'No active study plan found'
          ? tCommon('noActivePlan')
          : msg || 'Failed to add flashcards.'
      )
    } finally {
      setAdding(false)
    }
  }

  return (
    <div className="juba-vocabulary-set-shell mx-auto max-w-5xl space-y-6 p-5 sm:p-8">
      {/* Breadcrumb */}
      <nav className="text-[#202127] text-[rgba(32,33,39,.52)] flex items-center gap-2 font-sans">
        <Link
          href="/vocabulary"
          className="hover:text-[#202127] tracking-widest uppercase transition-colors"
        >
          {t('title')}
        </Link>
        <span>›</span>
        <span className="text-[rgba(32,33,39,.52)] tracking-widest uppercase">
          {vocabSet.level}
        </span>
        <span>›</span>
        <span className="text-[#202127] tracking-wide">{vocabSet.topic}</span>
      </nav>

      {/* Header */}
      <div className="juba-card rounded-[26px] border border-black/[0.07] bg-white shadow-[0_12px_30px_rgba(43,45,90,.055)]">
        <div className="flex items-center gap-2 border-b border-black/[0.07] px-6 py-4">
          <span className="text-[#202127] text-[rgba(32,33,39,.52)]">●</span>
          <span className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
            {t('vocabularySet')}
          </span>
        </div>
        <div className="space-y-3 px-6 py-5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full border border-black/[0.08] bg-[#ededff] px-3 py-1 text-xs font-bold tracking-wide text-[#373fb8]">
              {vocabSet.level}
            </span>
            <span className="border-[#ededff] text-[#202127] text-[rgba(32,33,39,.52)] border px-2 py-0.5 font-semibold tracking-wide">
              {vocabSet.unit_ref}
            </span>
          </div>
          <h1 className="text-[#202127] font-sans text-xl font-bold tracking-wide">
            {vocabSet.topic}
          </h1>
          <p className="text-[#202127] text-[rgba(32,33,39,.52)] font-sans">
            {vocabSet.words.length} {t('words')}
          </p>

          {/* Add to flashcards */}
          {addedCount !== null ? (
            <div className="rounded-[14px] border border-[#c9caff] bg-[#ededff] px-4 py-3">
              <p className="text-sm font-semibold text-[#373fb8]">
                ✓ {t('cardsAdded', { count: addedCount })}{' '}
                <button
                  onClick={() => router.push('/flashcards')}
                  className="underline hover:no-underline"
                >
                  {t('goToFlashcards')}
                </button>
              </p>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <button
                onClick={handleAddAll}
                disabled={adding}
                className="juba-primary-button px-5 py-2.5 text-sm font-bold tracking-wide disabled:opacity-40"
              >
                {adding ? '...' : t('addAll', { count: vocabSet.words.length })}
              </button>
            </div>
          )}
          {error && <p className="text-sm text-red-500">{error}</p>}
        </div>
      </div>

      {nativeLanguageName && (
        <div className="juba-card rounded-[26px] border border-black/[0.07] bg-white shadow-[0_12px_30px_rgba(43,45,90,.055)]">
          <button
            type="button"
            onClick={() => setNativeHelpOpen((open) => !open)}
            className="flex w-full items-center justify-between border-b border-black/[0.07] px-6 py-4 font-semibold tracking-wide text-[#202127] transition-colors hover:text-[#373fb8]"
            aria-expanded={nativeHelpOpen}
          >
            <span>
              {tCommon('nativeHelpTitle', { language: nativeLanguageName })}
            </span>
            <span>{nativeHelpOpen ? '−' : '+'}</span>
          </button>
          {nativeHelpOpen && (
            <div className="space-y-4 px-6 py-5">
              {loadingNativeHelp ? (
                <p className="text-[rgba(32,33,39,.52)] text-sm">
                  {tCommon('nativeHelpLoading', {
                    language: nativeLanguageName,
                  })}
                </p>
              ) : nativeHelp ? (
                <>
                  <p className="text-[rgba(32,33,39,.52)] text-sm leading-relaxed">
                    {nativeHelp.summary}
                  </p>

                  {nativeHelp.study_tips.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
                        {tCommon('nativeHelpStudyTips')}
                      </p>
                      <ul className="space-y-1">
                        {nativeHelp.study_tips.map((tip, i) => (
                          <li key={i} className="text-[rgba(32,33,39,.52)] text-sm">
                            <span className="text-[rgba(32,33,39,.52)] mr-2">·</span>
                            {tip}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {nativeHelp.word_notes.length > 0 && (
                    <div className="space-y-2 border-t border-black/[0.07] pt-3">
                      <p className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
                        {tCommon('nativeHelpWordNotes')}
                      </p>
                      {nativeHelp.word_notes.map((item, i) => (
                        <div key={i} className="space-y-0.5">
                          <TargetLanguageText
                            languageCode={targetLanguageCode}
                            className="text-[rgba(32,33,39,.52)] text-sm font-bold"
                          >
                            {item.word}
                          </TargetLanguageText>
                          <p className="text-[rgba(32,33,39,.52)] text-sm">
                            {item.meaning}
                          </p>
                          <p className="text-[rgba(32,33,39,.52)] text-sm">{item.note}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {nativeHelp.common_traps.length > 0 && (
                    <div className="space-y-2 border-t border-black/[0.07] pt-3">
                      <p className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
                        {tCommon('nativeHelpCommonTraps')}
                      </p>
                      {nativeHelp.common_traps.map((trap, i) => (
                        <div key={i} className="space-y-0.5">
                          <p className="text-[rgba(32,33,39,.52)] text-sm">
                            {trap.mistake}
                          </p>
                          <p className="text-[rgba(32,33,39,.52)] text-sm">{trap.fix}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {nativeHelp.mini_glossary.length > 0 && (
                    <div className="border-[#ededff] space-y-2 border-t pt-3">
                      <p className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
                        {tCommon('nativeHelpMiniGlossary')}
                      </p>
                      {nativeHelp.mini_glossary.map((item, i) => (
                        <div key={i}>
                          <TargetLanguageText
                            languageCode={targetLanguageCode}
                            className="text-[rgba(32,33,39,.52)] text-sm font-bold"
                          >
                            {item.term}
                          </TargetLanguageText>
                          <p className="text-[rgba(32,33,39,.52)] text-sm">
                            {item.meaning}
                          </p>
                          {item.note && (
                            <p className="text-[rgba(32,33,39,.52)] text-sm">
                              {item.note}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}

                  {nativeHelp.practice_prompts.length > 0 && (
                    <div className="border-[#ededff] space-y-2 border-t pt-3">
                      <p className="text-[#202127] text-[rgba(32,33,39,.52)] font-semibold tracking-wide">
                        {tCommon('nativeHelpPractice')}
                      </p>
                      <ul className="space-y-1">
                        {nativeHelp.practice_prompts.map((prompt, i) => (
                          <li key={i} className="text-[rgba(32,33,39,.52)] text-sm">
                            <span className="text-[rgba(32,33,39,.52)] mr-2">·</span>
                            {prompt}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </>
              ) : (
                <div className="text-center">
                  <button
                    type="button"
                    onClick={generateNativeHelp}
                    className="text-[rgba(32,33,39,.52)] hover:text-[#202127] text-sm transition-colors"
                  >
                    {nativeHelpError
                      ? tCommon('retry')
                      : tCommon('nativeHelpShow', {
                          language: nativeLanguageName,
                        })}
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Word list */}
      <div className="border-[#ededff] bg-white divide-fl-border divide-y border">
        {vocabSet.words.map((word, i) => (
          <div key={i} className="space-y-1.5 px-5 py-4">
            <div className="flex items-baseline gap-3">
              <TargetLanguageText
                languageCode={targetLanguageCode}
                className="text-[#202127] font-bold"
              >
                {word.word}
              </TargetLanguageText>
              <span className="text-[#202127] text-[rgba(32,33,39,.52)] font-sans italic">
                {POS_LABELS[word.pos] ?? word.pos}
              </span>
              {word.ipa && (
                <span className="text-[#202127] text-[rgba(32,33,39,.52)] font-sans">
                  {word.ipa}
                </span>
              )}
              {word.frequency_rank && (
                <span className="text-[#202127] text-[rgba(32,33,39,.52)] ml-auto font-sans">
                  #{word.frequency_rank}
                </span>
              )}
            </div>
            <TargetLanguageText
              as="p"
              languageCode={targetLanguageCode}
              className="text-[rgba(32,33,39,.52)]"
            >
              {word.definition}
            </TargetLanguageText>
            <TargetLanguageText
              as="p"
              languageCode={targetLanguageCode}
              className="text-[rgba(32,33,39,.52)] italic"
            >
              &ldquo;{word.example}&rdquo;
            </TargetLanguageText>
          </div>
        ))}
      </div>

      <Link
        href="/vocabulary"
        className="text-[#202127] text-[rgba(32,33,39,.52)] hover:text-[#202127] inline-block font-semibold tracking-wide transition-colors"
      >
        ← {t('backToVocabulary')}
      </Link>
    </div>
  )
}
