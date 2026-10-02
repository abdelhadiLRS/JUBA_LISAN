'use client'

import { useState, useMemo, useEffect, useCallback } from 'react'
import { useTranslations } from 'next-intl'
import {
  getPhrasebookCategories,
  getPhrasebookNativeHelp,
  type PhrasebookNativeHelp,
  type PhrasebookCategory,
  type Register,
} from '@/data/phrasebook'
import type { CEFRLevel } from '@/data/types'
import { useLanguageStore } from '@/store/language'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { PageLoading } from '@/components/ui/page-loading'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { useAuthStore } from '@/store/auth'

const CEFR_LEVELS: CEFRLevel[] = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
const REGISTERS: Register[] = ['formal', 'neutral', 'informal']

const REGISTER_COLORS: Record<string, string> = {
  formal: 'text-[var(--duo-green-dark)]',
  neutral: 'text-[var(--duo-muted)]',
  informal: 'text-[var(--duo-ink)]',
}

function CategoryCard({
  cat,
  registerFilter,
  search,
  language,
}: {
  cat: PhrasebookCategory
  registerFilter: Register | 'All'
  search: string
  language: string
}) {
  const t = useTranslations('phrasebook')
  const tCommon = useTranslations('common')
  const tTargetLang = useTranslations('targetLanguages')
  const user = useAuthStore((s) => s.user)
  const nativeLanguageName = user?.native_language
    ? tTargetLang(user.native_language)
    : ''
  const [nativeHelpOpen, setNativeHelpOpen] = useState(
    cat.level === 'A1' || cat.level === 'A2'
  )
  const [nativeHelp, setNativeHelp] = useState<PhrasebookNativeHelp | null>(
    null
  )
  const [loadingNativeHelp, setLoadingNativeHelp] = useState(false)
  const [nativeHelpError, setNativeHelpError] = useState(false)
  const phrases = cat.phrases.filter((p) => {
    const matchesRegister =
      registerFilter === 'All' || p.register === registerFilter
    const matchesSearch =
      !search || p.text.toLowerCase().includes(search.toLowerCase())
    return matchesRegister && matchesSearch
  })

  if (!phrases.length) return null

  async function generateNativeHelp() {
    if (loadingNativeHelp) return
    setLoadingNativeHelp(true)
    setNativeHelpError(false)
    try {
      const help = await getPhrasebookNativeHelp(cat.id, language)
      if (help) {
        setNativeHelp(help)
      } else {
        setNativeHelpError(true)
      }
    } catch {
      setNativeHelpError(true)
    } finally {
      setLoadingNativeHelp(false)
    }
  }

  return (
    <div className="juba-reference-list-card overflow-hidden p-0">
      <div className="flex min-h-[50px] items-center gap-3 border-b border-[var(--duo-line)] bg-[var(--duo-card)] px-5 py-3">
        <span className="flex h-9 w-9 items-center justify-center rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-bg)] text-sm">{cat.icon}</span>
        <div className="min-w-0 flex-1">
          <p className="truncate font-sans text-sm font-semibold tracking-wide text-[var(--duo-ink)]">
            {cat.situation}
          </p>
        </div>
        <span className="shrink-0 rounded-[10px] border border-[var(--duo-line)] px-2.5 py-1 font-sans text-[10px] font-bold tracking-widest uppercase text-[var(--duo-muted)]">
          {cat.level}
        </span>
      </div>

      {nativeLanguageName && (
        <div className="border-b border-[var(--duo-line)] px-5 py-3">
          <button
            type="button"
            onClick={() => setNativeHelpOpen((open) => !open)}
            className="flex w-full items-center justify-between font-sans text-[10px] tracking-widest uppercase text-[var(--duo-muted)] transition-colors hover:text-[var(--duo-ink)]"
            aria-expanded={nativeHelpOpen}
          >
            <span>
              {tCommon('nativeHelpTitle', { language: nativeLanguageName })}
            </span>
            <span>{nativeHelpOpen ? '−' : '+'}</span>
          </button>
          {nativeHelpOpen && (
            <div className="mt-3 space-y-3">
              {loadingNativeHelp ? (
                <p className="text-[var(--duo-muted)] font-sans text-xs">
                  {tCommon('nativeHelpLoading', {
                    language: nativeLanguageName,
                  })}
                </p>
              ) : nativeHelp ? (
                <>
                  <p className="text-[var(--duo-muted)] text-sm leading-relaxed">
                    {nativeHelp.summary}
                  </p>

                  {nativeHelp.usage_tips.length > 0 && (
                    <div className="space-y-1">
                      <p className="text-[var(--duo-muted)] font-sans text-[10px] font-bold tracking-widest uppercase">
                        {tCommon('nativeHelpUsageTips')}
                      </p>
                      <ul className="space-y-1">
                        {nativeHelp.usage_tips.map((tip, i) => (
                          <li key={i} className="text-[var(--duo-muted)] text-sm leading-relaxed">
                            <span className="text-[var(--duo-muted)] me-2">·</span>
                            {tip}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {nativeHelp.register_notes.length > 0 && (
                    <div className="border-[var(--duo-line)] space-y-1 border-t pt-3">
                      <p className="font-sans text-[10px] font-bold tracking-[0.14em] uppercase text-[var(--duo-muted)]">
                        {tCommon('nativeHelpRegisterNotes')}
                      </p>
                      {nativeHelp.register_notes.map((note, i) => (
                        <p key={i} className="text-[var(--duo-muted)] text-sm">
                          {note}
                        </p>
                      ))}
                    </div>
                  )}

                  {nativeHelp.phrase_notes.length > 0 && (
                    <div className="border-[var(--duo-line)] space-y-2 border-t pt-3">
                      <p className="font-sans text-[10px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">
                        {tCommon('nativeHelpPhraseNotes')}
                      </p>
                      {nativeHelp.phrase_notes.map((item, i) => (
                        <div key={i} className="space-y-0.5">
                          <TargetLanguageText
                            languageCode={language}
                            className="text-[var(--duo-muted)] text-sm italic"
                          >
                            {item.phrase}
                          </TargetLanguageText>
                          <p className="text-[var(--duo-muted)] text-sm">{item.note}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {nativeHelp.common_traps.length > 0 && (
                    <div className="border-[var(--duo-line)] space-y-2 border-t pt-3">
                      <p className="font-sans text-xs font-bold tracking-widest uppercase text-[var(--duo-ink)]">
                        {tCommon('nativeHelpCommonTraps')}
                      </p>
                      {nativeHelp.common_traps.map((trap, i) => (
                        <div key={i} className="space-y-0.5">
                          <p className="text-[var(--duo-muted)] text-sm">
                            {trap.mistake}
                          </p>
                          <p className="text-[var(--duo-muted)] text-sm">{trap.fix}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {nativeHelp.mini_glossary.length > 0 && (
                    <div className="border-[var(--duo-line)] space-y-2 border-t pt-3">
                      <p className="font-sans text-[10px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">
                        {tCommon('nativeHelpMiniGlossary')}
                      </p>
                      {nativeHelp.mini_glossary.map((item, i) => (
                        <div key={i}>
                          <TargetLanguageText
                            languageCode={language}
                            className="text-[var(--duo-muted)] text-sm font-bold"
                          >
                            {item.term}
                          </TargetLanguageText>
                          <p className="text-[var(--duo-muted)] text-sm">
                            {item.meaning}
                          </p>
                          {item.note && (
                            <p className="text-[var(--duo-muted)] text-sm">
                              {item.note}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <button
                  type="button"
                  onClick={generateNativeHelp}
                  className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] font-sans text-sm transition-colors"
                >
                  {nativeHelpError
                    ? tCommon('retry')
                    : tCommon('nativeHelpShow', {
                        language: nativeLanguageName,
                      })}
                </button>
              )}
            </div>
          )}
        </div>
      )}

      <ul className="divide-[var(--duo-line)] divide-y">
        {phrases.map((phrase, i) => (
          <li key={i} className="group space-y-1.5 px-4 py-3.5 transition-colors hover:bg-[var(--duo-bg)] sm:px-5">
            <div className="flex items-start justify-between gap-3">
              <TargetLanguageText
                as="p"
                languageCode={language}
                className="text-[var(--duo-ink)] flex-1"
              >
                {phrase.text}
              </TargetLanguageText>
              <div className="flex shrink-0 items-center gap-1">
                <span
                  className={`text-[var(--duo-ink)] font-sans text-[10px] font-semibold tracking-widest uppercase ${REGISTER_COLORS[phrase.register]}`}
                >
                  {t(phrase.register)}
                </span>
                <AudioPlayer
                  text={phrase.text}
                  size="sm"
                  audioUrl={`/api/phrasebook/audio/${encodeURIComponent(cat.id)}/${cat.phrases.indexOf(phrase)}?language=${encodeURIComponent(language)}`}
                />
                <CopyButton text={phrase.text} />
              </div>
            </div>
            {phrase.context && (
              <TargetLanguageText
                as="p"
                languageCode={language}
                className="text-[var(--duo-muted)] text-sm italic"
              >
                {phrase.context}
              </TargetLanguageText>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      /* ignore */
    }
  }

  return (
    <button
      onClick={handleCopy}
      className="min-h-8 rounded-[10px] px-2 py-1 font-sans text-xs text-[var(--duo-muted)] transition-colors hover:bg-[var(--duo-line)] hover:text-[var(--duo-ink)]"
      title="Copy"
      aria-label="Copy phrase"
    >
      {copied ? '\u2713' : '\u{1f4cb}'}
    </button>
  )
}

export default function PhrasebookPage() {
  const t = useTranslations('phrasebook')
  const tCommon = useTranslations('common')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const [categories, setCategories] = useState<PhrasebookCategory[]>([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [activeLevel, setActiveLevel] = useState<CEFRLevel | 'All'>('All')
  const [activeRegister, setActiveRegister] = useState<Register | 'All'>('All')
  const [search, setSearch] = useState('')

  const fetchCategories = useCallback(async (lang: string) => {
    setLoading(true)
    setLoadError(false)
    try {
      const data = await getPhrasebookCategories(lang)
      setCategories(data)
    } catch {
      setLoadError(true)
      setCategories([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchCategories(activeLanguage?.code ?? 'en-GB')
  }, [activeLanguage?.code, fetchCategories])

  const filteredCategories = useMemo(() => {
    return categories.filter((cat) => {
      const matchesLevel = activeLevel === 'All' || cat.level === activeLevel
      const matchesRegister =
        activeRegister === 'All' ||
        cat.phrases.some((p) => p.register === activeRegister)
      const matchesSearch =
        !search ||
        cat.phrases.some((p) =>
          p.text.toLowerCase().includes(search.toLowerCase())
        )
      return matchesLevel && matchesRegister && matchesSearch
    })
  }, [activeLevel, activeRegister, search, categories])

  const totalPhrases = categories.reduce((acc, c) => acc + c.phrases.length, 0)

  if (loading) {
    return <PageLoading />
  }

  if (loadError) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
        <p className="text-[var(--duo-muted)] font-sans text-sm">{tCommon('error')}</p>
        <button
          onClick={() => fetchCategories(activeLanguage?.code ?? 'en-GB')}
          className="text-[var(--duo-green-dark)] font-sans text-xs tracking-widest uppercase underline"
        >
          {tCommon('retry')}
        </button>
      </div>
    )
  }

  const hasActiveFilters =
    activeLevel !== 'All' || activeRegister !== 'All' || !!search

  return (
    <div className="juba-mobile-phrasebook w-full space-y-6 px-4 py-5 sm:px-6 sm:py-6 lg:px-8">
      <section className="juba-reference-hero min-h-[112px] px-5 py-5 sm:px-6 sm:py-6">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-end lg:justify-between">
          <div className="w-full max-w-[760px] space-y-2">
            <p className="juba-eyebrow">{t('title')}</p>
            <h1 className="text-[28px] font-extrabold tracking-tight text-[var(--duo-ink)] sm:text-4xl">{t('title')}</h1>
            <p className="text-sm leading-relaxed text-[var(--duo-muted)]">{t('statsLine', { situationCount: categories.length, phraseCount: totalPhrases, range: `${CEFR_LEVELS[0]} – ${CEFR_LEVELS[CEFR_LEVELS.length - 1]}` })}</p>
          </div>
          <div className="grid grid-cols-2 gap-2 sm:min-w-[216px] lg:min-w-[224px]">
            <div className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] px-3.5 py-2 text-center"><p className="text-lg font-extrabold text-[var(--duo-green-dark)]">{categories.length}</p><p className="font-sans text-[9px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">Situations</p></div>
            <div className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] px-4 py-2.5 text-center"><p className="text-lg font-extrabold text-[var(--duo-ink)]">{totalPhrases}</p><p className="font-sans text-[9px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">Phrases</p></div>
          </div>
        </div>
      </section>
      <div className="juba-reference-filter-panel overflow-hidden">
        <div className="flex items-center gap-2 border-b border-[var(--duo-line)] bg-[var(--duo-card)] px-5 py-3">
          <span className="text-sm font-bold text-[var(--duo-green-dark)]">{'\u25cf'}</span>
          <span className="font-sans text-[10px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">
            {t('title')}
          </span>
        </div>
        <div className="space-y-3 px-4 py-4 sm:px-5">
          <div className="grid gap-3 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-end">
            <div className="space-y-2">
              <p className="font-sans text-[10px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">
                {t('searchPlaceholder')}
              </p>
              <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={t('searchPlaceholder')}
              className="juba-input w-full font-sans text-sm"
              />
            </div>
            <div className="flex items-end justify-start">
              <span className="min-h-9 rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-bg)] px-3 py-2 font-sans text-[10px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">
                {filteredCategories.length} {t('title')}
              </span>
            </div>
          </div>

          <div className="space-y-2">
            <p className="font-sans text-[10px] font-semibold tracking-widest uppercase text-[var(--duo-muted)]">
              {t('level')}
            </p>
            <div className="flex flex-wrap gap-2">
              {(['All', ...CEFR_LEVELS] as const).map((lvl) => (
                <button
                  key={lvl}
                  onClick={() => setActiveLevel(lvl)}
                  className={`text-[var(--duo-ink)] min-h-9 rounded-[10px] border px-3 py-1.5 font-sans text-[10px] font-bold tracking-widest uppercase transition-colors ${
                    activeLevel === lvl
                      ? 'border-[var(--duo-green-dark)] bg-[var(--duo-green-dark)] text-white'
                      : 'border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-green-dark)] hover:text-[var(--duo-ink)]'
                  }`}
                >
                  {lvl === 'All' ? tCommon('all') : lvl}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <p className="font-sans text-[10px] tracking-widest uppercase text-[var(--duo-muted)]">
              {t('register')}
            </p>
            <div className="flex flex-wrap gap-2">
              {(['All', ...REGISTERS] as const).map((reg) => (
                <button
                  key={reg}
                  onClick={() => setActiveRegister(reg)}
                  className={`text-[var(--duo-ink)] rounded-[10px] border px-3 py-1.5 font-sans tracking-widest uppercase transition-colors ${
                    activeRegister === reg
                      ? 'border-[var(--duo-green-dark)] bg-[var(--duo-green-dark)] text-white'
                      : 'border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-green-dark)] hover:text-[var(--duo-ink)]'
                  }`}
                >
                  {reg === 'All' ? tCommon('all') : t(reg)}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {hasActiveFilters && (
        <p className="font-sans text-xs text-[var(--duo-muted)]">
          {t('situationsShown', { count: filteredCategories.length })}
        </p>
      )}

      {CEFR_LEVELS.map((level) => {
        const cats = filteredCategories.filter((c) => c.level === level)
        if (!cats.length) return null
        return (
          <section key={level} className="juba-reference-section space-y-3">
            <div className="flex items-center gap-3">
              <span className="font-sans text-xs font-bold tracking-[0.18em] text-[var(--duo-green-dark)]">
                {level}
              </span>
              <div className="bg-[var(--duo-line)] h-px flex-1" />
            </div>
            <div className="grid gap-4 xl:grid-cols-2">
              {cats.map((cat) => (
                <CategoryCard
                  key={cat.id}
                  cat={cat}
                  registerFilter={activeRegister}
                  search={search}
                  language={activeLanguage?.code ?? 'en-GB'}
                />
              ))}
            </div>
          </section>
        )
      })}

      {filteredCategories.length === 0 && (
        <div className="juba-reference-list-card space-y-3 px-5 py-9 text-center">
          <p className="text-[var(--duo-muted)] font-sans text-[11px] tracking-widest uppercase">
            {t('noResults')}
          </p>
          {hasActiveFilters && (
            <button
              onClick={() => {
                setActiveLevel('All')
                setActiveRegister('All')
                setSearch('')
              }}
              className="rounded-[10px] border border-[var(--duo-line)] px-4 py-2 font-sans text-[11px] font-bold tracking-widest uppercase text-[var(--duo-muted)] transition-colors hover:border-[var(--duo-green-dark)] hover:text-[var(--duo-ink)]"
            >
              {tCommon('clearFilters')}
            </button>
          )}
        </div>
      )}
    </div>
  )
}
