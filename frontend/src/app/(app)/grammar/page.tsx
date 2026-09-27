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
      className="juba-card group block rounded-[24px] border-2 border-[#e1e5e2] p-0 transition-all hover:-translate-y-1 hover:shadow-lg"
    >
      <div className="space-y-2 px-4 py-4">
        <div className="flex items-start justify-between gap-2">
          <p className="text-[#30343b] group-hover:text-[#438600] text-xs leading-snug font-bold tracking-wide transition-colors">
            {topic.title}
          </p>
          <span className="border-[#e1e5e2] text-[#68736d] shrink-0 rounded-full border px-2 py-0.5 text-[10px] font-bold tracking-widest uppercase">
            {topic.level}
          </span>
        </div>
        <p className="text-[#68736d] text-xs leading-relaxed">
          {topic.summary}
        </p>
        <span className="bg-[#e1e5e2] text-[#438600] inline-block rounded-full px-2 py-0.5 text-[10px] font-bold tracking-widest uppercase">
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
        <p className="text-[#68736d] text-sm">{tCommon('error')}</p>
        <button onClick={() => fetchTopics(activeLanguage?.code ?? 'en-GB')} className="rounded-full bg-[#e1e5e2] px-4 py-2 text-xs font-bold tracking-widest text-[#438600] uppercase transition-colors hover:bg-[#438600]">
          {tCommon('retry')}
        </button>
      </div>
    )
  }

  return (
    <div className="juba-mobile-grammar mx-auto max-w-6xl space-y-8 p-4 sm:p-6">
      <div className="juba-card rounded-[30px] border-2 border-[#e1e5e2] p-0 shadow-[0 3px 0 rgba(31,41,51,.045)]">
        <div className="border-b border-[#e1e5e2] px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-[#58a700]" />
            <span className="juba-eyebrow">{t('title')}</span>
          </div>
        </div>
        <div className="space-y-4 px-6 py-5">
          <p className="text-[#68736d] text-xs leading-relaxed">
            {topics.length} topics · A1 – C2
          </p>
          <input type="text" value={search} onChange={(e) => setSearch(e.target.value)} placeholder={t('searchPlaceholder')} className="w-full max-w-sm rounded-[20px] border border-[#e1e5e2] bg-[#e1e5e2] px-4 py-2.5 text-sm text-[#30343b] placeholder:text-[#68736d] transition-colors focus:border-[#438600] focus:outline-none" />
          <div className="flex flex-wrap gap-2">
            <button onClick={() => setActiveCategory('All')} className={`rounded-full px-3 py-1.5 text-xs font-bold tracking-wide transition-colors ${activeCategory === 'All' ? 'bg-[#30343b] text-[white]' : 'border border-[#e1e5e2] text-[#68736d] hover:bg-[#e1e5e2]'}`}>
              {t('allCategories')}
            </button>
            {usedCategories.map((cat) => (
              <button key={cat} onClick={() => setActiveCategory(activeCategory === cat ? 'All' : cat)} className={`rounded-full px-3 py-1.5 text-xs font-bold tracking-wide transition-colors ${activeCategory === cat ? 'bg-[#e1e5e2] text-[#438600]' : 'border border-[#e1e5e2] text-[#68736d] hover:bg-[#e1e5e2]'}`}>
                {cat}
              </button>
            ))}
          </div>
        </div>
      </div>

      {(search || activeCategory !== 'All') && <p className="text-xs font-medium text-[#68736d]">{t('topicsFound', { count: filtered.length })}</p>}

      {CEFR_LEVELS.map((level) => {
        const levelTopics = filtered.filter((t) => t.level === level)
        if (!levelTopics.length) return null
        return (
          <section key={level} className="space-y-3">
            <div className="flex items-center gap-3">
              <span className="text-[#30343b] text-base font-bold tracking-widest">{level}</span>
              <div className="h-px flex-1 bg-[#e1e5e2]" />
              <span className="text-xs text-[#68736d]">{levelTopics.length} topic{levelTopics.length !== 1 ? 's' : ''}</span>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {levelTopics.map((t) => <TopicCard key={t.slug} topic={t} />)}
            </div>
          </section>
        )
      })}

      {filtered.length === 0 && (
        <div className="juba-card space-y-4 px-6 py-10 text-center">
          <p className="text-xs font-bold tracking-widest text-[#68736d] uppercase">{t('noResults')}</p>
          {(search || activeCategory !== 'All') && <button onClick={() => { setSearch(''); setActiveCategory('All') }} className="rounded-full border border-[#e1e5e2] px-4 py-2 text-xs font-bold text-[#68736d] transition-colors hover:bg-[#e1e5e2]">{tCommon('clearFilters')}</button>}
        </div>
      )}
    </div>
  )
}
