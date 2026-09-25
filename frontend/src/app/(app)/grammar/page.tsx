'use client'

import { useState, useMemo, useEffect, useCallback } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { getGrammarTopics, type GrammarTopic } from '@/data/grammar'
import type { GrammarCategory } from '@/data/types'
import { CEFR_LEVELS } from '@/data/curriculum'
import { useLanguageStore } from '@/store/language'
import { PageLoading } from '@/components/ui/page-loading'

function TopicCard({ topic }: { topic: GrammarTopic }) {
  return (
    <Link
      href={`/grammar/${topic.slug}`}
      className="border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] hover:border-[var(--juba-app-line)]-2 hover:bg-[var(--juba-app-surface)]-2 group block border transition-colors"
    >
      <div className="space-y-2 px-4 py-4">
        <div className="flex items-start justify-between gap-2">
          <p className="text-[var(--juba-app-ink)] group-hover:text-[var(--juba-app-ink)]-bright font-sans text-xs leading-snug font-bold tracking-wide transition-colors">
            {topic.title}
          </p>
          <span className="border-[var(--juba-app-line)] text-[var(--juba-app-ink)] text-[var(--juba-app-muted)] shrink-0 border px-1.5 py-0.5 font-sans tracking-widest uppercase">
            {topic.level}
          </span>
        </div>
        <p className="text-[var(--juba-app-ink)] text-[var(--juba-app-muted)] font-sans leading-relaxed">
          {topic.summary}
        </p>
        <span className="border-[var(--juba-app-line)] text-[var(--juba-app-ink)] text-[var(--juba-app-muted)] inline-block border px-2 py-0.5 font-sans tracking-widest uppercase">
          {topic.category}
        </span>
      </div>
    </Link>
  )
}

export default function GrammarIndexPage() {
  const t = useTranslations('grammar')
  const tCommon = useTranslations('common')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const [topics, setTopics] = useState<GrammarTopic[]>([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [search, setSearch] = useState('')
  const [activeCategory, setActiveCategory] = useState<GrammarCategory | 'All'>(
    'All'
  )

  const fetchTopics = useCallback(async (lang: string) => {
    setLoading(true)
    setLoadError(false)
    try {
      const data = await getGrammarTopics(lang)
      setTopics(data)
    } catch {
      setLoadError(true)
      setTopics([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchTopics(activeLanguage?.code ?? 'en-GB')
  }, [activeLanguage?.code, fetchTopics])

  const allCategories: GrammarCategory[] = useMemo(
    () =>
      Array.from(
        new Set(topics.map((t) => t.category))
      ).sort() as GrammarCategory[],
    [topics]
  )

  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return topics.filter((t) => {
      const matchesSearch =
        !q ||
        t.title.toLowerCase().includes(q) ||
        t.summary.toLowerCase().includes(q) ||
        t.category.toLowerCase().includes(q)
      const matchesCategory =
        activeCategory === 'All' || t.category === activeCategory
      return matchesSearch && matchesCategory
    })
  }, [search, activeCategory, topics])

  const usedCategories = useMemo(() => {
    const cats = new Set(topics.map((t) => t.category))
    return allCategories.filter((c) => cats.has(c))
  }, [topics, allCategories])

  if (loading) {
    return <PageLoading />
  }

  if (loadError) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
        <p className="text-[var(--juba-app-muted)] font-sans text-sm">{tCommon('error')}</p>
        <button
          onClick={() => fetchTopics(activeLanguage?.code ?? 'en-GB')}
          className="text-[var(--juba-app-green)] font-sans text-xs tracking-widest uppercase underline"
        >
          {tCommon('retry')}
        </button>
      </div>
    )
  }

  return (
    <div className="juba-grammar-shell mx-auto max-w-4xl space-y-8 p-6">
      <div className="border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] border">
        <div className="border-[var(--juba-app-line)] flex items-center gap-2 border-b px-6 py-4">
          <span className="text-[var(--juba-app-ink)] text-[var(--juba-app-muted)]">{'\u25cf'}</span>
          <span className="text-[var(--juba-app-ink)] text-[var(--juba-app-muted)] font-sans tracking-widest uppercase">
            {t('title')}
          </span>
        </div>
        <div className="space-y-4 px-6 py-5">
          <p className="text-[var(--juba-app-muted)] font-sans text-xs leading-relaxed">
            {topics.length} topics · A1 – C2
          </p>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t('searchPlaceholder')}
            className="bg-[var(--juba-app-bg)] border-[var(--juba-app-line)] text-[var(--juba-app-ink)] placeholder:text-[var(--juba-app-muted)] focus:border-[var(--juba-app-line)]-2 w-full max-w-sm border px-4 py-2.5 font-sans text-xs transition-colors focus:outline-none"
          />
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setActiveCategory('All')}
              className={`text-[var(--juba-app-ink)] border px-3 py-1.5 font-sans tracking-widest uppercase transition-colors ${
                activeCategory === 'All'
                  ? 'border-[var(--juba-app-ink)] text-[var(--juba-app-ink)] bg-[var(--juba-app-surface)]-2'
                  : 'border-[var(--juba-app-line)] text-[var(--juba-app-muted)] hover:border-[var(--juba-app-line)]-2 hover:text-[var(--juba-app-ink)]'
              }`}
            >
              {t('allCategories')}
            </button>
            {usedCategories.map((cat) => (
              <button
                key={cat}
                onClick={() =>
                  setActiveCategory(activeCategory === cat ? 'All' : cat)
                }
                className={`text-[var(--juba-app-ink)] border px-3 py-1.5 font-sans tracking-widest uppercase transition-colors ${
                  activeCategory === cat
                    ? 'border-[var(--juba-app-ink)] text-[var(--juba-app-ink)] bg-[var(--juba-app-surface)]-2'
                    : 'border-[var(--juba-app-line)] text-[var(--juba-app-muted)] hover:border-[var(--juba-app-line)]-2 hover:text-[var(--juba-app-ink)]'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {(search || activeCategory !== 'All') && (
        <p className="text-[var(--juba-app-ink)] text-[var(--juba-app-muted)] font-sans">
          {t('topicsFound', { count: filtered.length })}
        </p>
      )}

      {CEFR_LEVELS.map((level) => {
        const levelTopics = filtered.filter((t) => t.level === level)
        if (!levelTopics.length) return null
        return (
          <section key={level} className="space-y-3">
            <div className="flex items-center gap-3">
              <span className="text-[var(--juba-app-ink)] font-sans text-base font-bold tracking-widest">
                {level}
              </span>
              <div className="bg-[var(--juba-app-line)] h-px flex-1" />
              <span className="text-[var(--juba-app-ink)] text-[var(--juba-app-muted)] font-sans">
                {levelTopics.length} topic{levelTopics.length !== 1 ? 's' : ''}
              </span>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {levelTopics.map((t) => (
                <TopicCard key={t.slug} topic={t} />
              ))}
            </div>
          </section>
        )
      })}

      {filtered.length === 0 && (
        <div className="border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] space-y-4 border px-6 py-10 text-center">
          <p className="text-[var(--juba-app-muted)] font-sans text-xs tracking-widest uppercase">
            {t('noResults')}
          </p>
          {(search || activeCategory !== 'All') && (
            <button
              onClick={() => {
                setSearch('')
                setActiveCategory('All')
              }}
              className="text-[var(--juba-app-ink)] border-[var(--juba-app-line)] text-[var(--juba-app-muted)] hover:border-[var(--juba-app-line)]-2 hover:text-[var(--juba-app-ink)] border px-4 py-2 font-sans tracking-widest uppercase transition-colors"
            >
              {tCommon('clearFilters')}
            </button>
          )}
        </div>
      )}
    </div>
  )
}
