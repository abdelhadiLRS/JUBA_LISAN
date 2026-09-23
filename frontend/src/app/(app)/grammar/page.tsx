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
      className="juba-card group block rounded-[24px] border-2 border-[var(--juba-lilac)] p-0 transition-all hover:-translate-y-1 hover:shadow-lg"
    >
      <div className="space-y-2 px-4 py-4">
        <div className="flex items-start justify-between gap-2">
          <p className="text-[var(--juba-text)] group-hover:text-[var(--juba-violet-dark)] text-xs leading-snug font-bold tracking-wide transition-colors">
            {topic.title}
          </p>
          <span className="border-[var(--juba-lilac)] text-[var(--juba-muted)] shrink-0 rounded-full border px-2 py-0.5 text-[10px] font-bold tracking-widest uppercase">
            {topic.level}
          </span>
        </div>
        <p className="text-[var(--juba-muted)] text-xs leading-relaxed">
          {topic.summary}
        </p>
        <span className="bg-[var(--juba-lilac)] text-[var(--juba-violet-dark)] inline-block rounded-full px-2 py-0.5 text-[10px] font-bold tracking-widest uppercase">
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
  const [activeCategory, setActiveCategory] = useState<GrammarCategory | 'All'>('All')

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
    () => Array.from(new Set(topics.map((t) => t.category))).sort() as GrammarCategory[],
    [topics]
  )

  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return topics.filter((t) => {
      const matchesSearch = !q || t.title.toLowerCase().includes(q) || t.summary.toLowerCase().includes(q) || t.category.toLowerCase().includes(q)
      const matchesCategory = activeCategory === 'All' || t.category === activeCategory
      return matchesSearch && matchesCategory
    })
  }, [search, activeCategory, topics])

  const usedCategories = useMemo(() => {
    const cats = new Set(topics.map((t) => t.category))
    return allCategories.filter((c) => cats.has(c))
  }, [topics, allCategories])

  if (loading) return <PageLoading />

  if (loadError) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 px-6">
        <p className="text-[var(--juba-muted)] text-sm">{tCommon('error')}</p>
        <button onClick={() => fetchTopics(activeLanguage?.code ?? 'en-GB')} className="rounded-full bg-[var(--juba-lilac)] px-4 py-2 text-xs font-bold tracking-widest text-[var(--juba-violet-dark)] uppercase transition-colors hover:bg-[var(--juba-violet)]">
          {tCommon('retry')}
        </button>
      </div>
    )
  }

  return (
    <div className="juba-mobile-grammar mx-auto max-w-6xl space-y-8 p-4 sm:p-6">
      <div className="juba-card rounded-[30px] border-2 border-[var(--juba-lilac)] p-0 shadow-[0_18px_45px_rgba(61,42,130,0.08)]">
        <div className="border-b border-[var(--juba-lilac)] px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-[var(--juba-yellow)]" />
            <span className="juba-eyebrow">{t('title')}</span>
          </div>
        </div>
        <div className="space-y-4 px-6 py-5">
          <p className="text-[var(--juba-muted)] text-xs leading-relaxed">
            {topics.length} topics · A1 – C2
          </p>
          <input type="text" value={search} onChange={(e) => setSearch(e.target.value)} placeholder={t('searchPlaceholder')} className="w-full max-w-sm rounded-[20px] border border-[var(--juba-lilac)] bg-[var(--juba-lilac)] px-4 py-2.5 text-sm text-[var(--juba-text)] placeholder:text-[var(--juba-muted)] transition-colors focus:border-[var(--juba-violet-dark)] focus:outline-none" />
          <div className="flex flex-wrap gap-2">
            <button onClick={() => setActiveCategory('All')} className={`rounded-full px-3 py-1.5 text-xs font-bold tracking-wide transition-colors ${activeCategory === 'All' ? 'bg-[var(--juba-text)] text-[white]' : 'border border-[var(--juba-lilac)] text-[var(--juba-muted)] hover:bg-[var(--juba-lilac)]'}`}>
              {t('allCategories')}
            </button>
            {usedCategories.map((cat) => (
              <button key={cat} onClick={() => setActiveCategory(activeCategory === cat ? 'All' : cat)} className={`rounded-full px-3 py-1.5 text-xs font-bold tracking-wide transition-colors ${activeCategory === cat ? 'bg-[var(--juba-lilac)] text-[var(--juba-violet-dark)]' : 'border border-[var(--juba-lilac)] text-[var(--juba-muted)] hover:bg-[var(--juba-lilac)]'}`}>
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {(search || activeCategory !== 'All') && <p className="text-xs font-medium text-[var(--juba-muted)]">{t('topicsFound', { count: filtered.length })}</p>}

      {CEFR_LEVELS.map((level) => {
        const levelTopics = filtered.filter((t) => t.level === level)
        if (!levelTopics.length) return null
        return (
          <section key={level} className="space-y-3">
            <div className="flex items-center gap-3">
              <span className="text-[var(--juba-text)] text-base font-bold tracking-widest">{level}</span>
              <div className="h-px flex-1 bg-[var(--juba-lilac)]" />
              <span className="text-xs text-[var(--juba-muted)]">{levelTopics.length} topic{levelTopics.length !== 1 ? 's' : ''}</span>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {levelTopics.map((t) => <TopicCard key={t.slug} topic={t} />)}
            </div>
          </section>
        )
      })}

      {filtered.length === 0 && (
        <div className="juba-card space-y-4 px-6 py-10 text-center">
          <p className="text-xs font-bold tracking-widest text-[var(--juba-muted)] uppercase">{t('noResults')}</p>
          {(search || activeCategory !== 'All') && <button onClick={() => { setSearch(''); setActiveCategory('All') }} className="rounded-full border border-[var(--juba-lilac)] px-4 py-2 text-xs font-bold text-[var(--juba-muted)] transition-colors hover:bg-[var(--juba-lilac)]">{tCommon('clearFilters')}</button>}
        </div>
      )}
    </div>
  )
}
