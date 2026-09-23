'use client'

import { useState, useEffect, useCallback } from 'react'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import { use } from 'react'
import { useTranslations } from 'next-intl'
import {
  getGrammarNativeHelp,
  getGrammarTopics,
  type GrammarNativeHelp,
  type GrammarTopic,
} from '@/data/grammar'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { PageLoading } from '@/components/ui/page-loading'

function renderExplanation(text: string) {
  const lines = text.split('\n')
  return lines.map((line, i) => {
    if (line.startsWith('- ')) {
      return (
        <li
          key={i}
          className="text-[var(--juba-muted)] font-mono text-xs leading-relaxed"
        >
          <span className="text-[var(--juba-muted)] mr-2">{'\u00b7'}</span>
          <RichText text={line.slice(2)} />
        </li>
      )
    }
    if (line.trim() === '') return null
    if (line.startsWith('|')) {
      return (
        <tr key={i}>
          {line
            .split('|')
            .filter(Boolean)
            .map((cell, ci) => (
              <td
                key={ci}
                className="text-[var(--juba-text)] text-[var(--juba-muted)] border-[var(--juba-lilac)] border px-3 py-1.5 font-mono"
              >
                <RichText text={cell.trim()} />
              </td>
            ))}
        </tr>
      )
    }
    return (
      <p key={i} className="text-[var(--juba-muted)] font-mono text-xs leading-relaxed">
        <RichText text={line} />
      </p>
    )
  })
}

function RichText({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/)
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return (
            <strong key={i} className="text-[var(--juba-text)] font-bold">
              {part.slice(2, -2)}
            </strong>
          )
        }
        if (part.startsWith('`') && part.endsWith('`')) {
          return (
            <code key={i} className="bg-[var(--juba-lilac)] text-[var(--juba-text)] px-1 font-mono">
              {part.slice(1, -1)}
            </code>
          )
        }
        return <span key={i}>{part}</span>
      })}
    </>
  )
}

export default function GrammarDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const t = useTranslations('grammar')
  const tCommon = useTranslations('common')
  const tNav = useTranslations('nav')
  const tTargetLang = useTranslations('targetLanguages')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const user = useAuthStore((s) => s.user)
  const nativeLanguageName = user?.native_language
    ? tTargetLang(user.native_language)
    : ''
  const { slug } = use(params)

  const [topics, setTopics] = useState<GrammarTopic[]>([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [nativeHelpOpen, setNativeHelpOpen] = useState(false)
  const [nativeHelp, setNativeHelp] = useState<GrammarNativeHelp | null>(null)
  const [loadingNativeHelp, setLoadingNativeHelp] = useState(false)
  const [nativeHelpError, setNativeHelpError] = useState(false)

  const topic = topics.find((t) => t.slug === slug)
  const targetLanguageCode = activeLanguage?.code ?? 'en-GB'

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
    fetchTopics(targetLanguageCode)
  }, [targetLanguageCode, fetchTopics])

  useEffect(() => {
    if (!topic) return
    setNativeHelp(null)
    setNativeHelpError(false)
    setNativeHelpOpen(topic.level === 'A1' || topic.level === 'A2')
    // eslint-disable-next-line react-hooks/exhaustive-deps -- topic?.slug and topic?.level avoid unnecessary runs; topic object identity changes every render
  }, [topic?.slug, topic?.level, targetLanguageCode])

  const generateNativeHelp = useCallback(async () => {
    if (!topic || loadingNativeHelp) return
    setLoadingNativeHelp(true)
    setNativeHelpError(false)
    try {
      const help = await getGrammarNativeHelp(topic.slug, targetLanguageCode)
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
  }, [loadingNativeHelp, targetLanguageCode, topic])

  useEffect(() => {
    if (nativeHelpOpen && topic && !nativeHelp && !loadingNativeHelp) {
      generateNativeHelp()
    }
  }, [generateNativeHelp, loadingNativeHelp, nativeHelp, nativeHelpOpen, topic])

  if (loading) {
    return <PageLoading />
  }

  if (loadError) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
        <p className="text-[var(--juba-muted)] font-mono text-sm">{tCommon('error')}</p>
        <button
          onClick={() => fetchTopics(targetLanguageCode)}
          className="text-[var(--juba-violet)] font-mono text-xs tracking-widest uppercase underline"
        >
          {tCommon('retry')}
        </button>
      </div>
    )
  }

  if (!topic) notFound()

  const hasTable = topic.explanation.includes('|')
  const explanationLines = topic.explanation.split('\n')
  const hasList = explanationLines.some((l) => l.startsWith('- '))

  const relatedTopics = topic.related
    .map((s) => topics.find((t) => t.slug === s))
    .filter(Boolean)

  return (
    <div className="mx-auto max-w-5xl space-y-4 p-6">
      <nav className="text-[var(--juba-text)] text-[var(--juba-muted)] flex items-center gap-2 font-mono">
        <Link
          href="/grammar"
          className="hover:text-[var(--juba-text)] tracking-widest uppercase transition-colors"
        >
          {tNav('grammar')}
        </Link>
        <span>{'\u203a'}</span>
        <span className="text-[var(--juba-muted)] tracking-widest uppercase">
          {topic.level}
        </span>
        <span>{'\u203a'}</span>
        <span className="text-[var(--juba-text)] tracking-wide">{topic.title}</span>
      </nav>

      <div className="border-[var(--juba-lilac)] bg-white border">
        <div className="border-[var(--juba-lilac)] flex items-center gap-2 border-b px-6 py-4">
          <span className="text-[var(--juba-text)] text-[var(--juba-muted)]">{'\u25cf'}</span>
          <span className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
            {t('backToGrammar')}
          </span>
        </div>
        <div className="space-y-3 px-6 py-5">
          <div className="flex flex-wrap items-center gap-2">
            <span className="border-[var(--juba-lilac)] text-[var(--juba-text)] text-[var(--juba-muted)] border px-2 py-0.5 font-mono tracking-widest uppercase">
              {topic.level}
            </span>
            <span className="border-[var(--juba-lilac)] text-[var(--juba-text)] text-[var(--juba-muted)] border px-2 py-0.5 font-mono tracking-widest uppercase">
              {topic.category}
            </span>
          </div>
          <h1 className="text-[var(--juba-text)] font-mono text-xl font-bold tracking-wide">
            {topic.title}
          </h1>
          <p className="text-[var(--juba-muted)] font-mono text-xs leading-relaxed">
            {topic.summary}
          </p>
          {topic.structure && (
            <div className="border-[var(--juba-lilac)] bg-[var(--juba-lilac)]/40 border px-4 py-3">
              <p className="text-[var(--juba-text)] text-[var(--juba-muted)] mb-1 font-mono tracking-widest uppercase">
                {t('structure')}
              </p>
              <p className="text-[var(--juba-text)] font-mono text-xs">{topic.structure}</p>
            </div>
          )}
        </div>
      </div>

      <div className="border-[var(--juba-lilac)] bg-white border">
        <div className="border-[var(--juba-lilac)] flex items-center gap-2 border-b px-6 py-4">
          <span className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
            {t('explanation')}
          </span>
        </div>
        <div className="space-y-2 px-6 py-5">
          {hasTable ? (
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <tbody>{renderExplanation(topic.explanation)}</tbody>
              </table>
            </div>
          ) : hasList ? (
            <ul className="space-y-1">
              {renderExplanation(topic.explanation)}
            </ul>
          ) : (
            <div className="space-y-2">
              {renderExplanation(topic.explanation)}
            </div>
          )}
        </div>
      </div>

      {nativeLanguageName && (
        <div className="border-[var(--juba-lilac)] bg-white border">
          <button
            type="button"
            onClick={() => setNativeHelpOpen((open) => !open)}
            className="border-[var(--juba-lilac)] text-[var(--juba-text)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] flex w-full items-center justify-between border-b px-6 py-4 font-mono tracking-widest uppercase transition-colors"
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
                <p className="text-[var(--juba-muted)] font-mono text-xs">
                  {tCommon('nativeHelpLoading', {
                    language: nativeLanguageName,
                  })}
                </p>
              ) : nativeHelp ? (
                <>
                  <div className="space-y-2">
                    <p className="text-[var(--juba-muted)] text-sm leading-relaxed">
                      {nativeHelp.summary}
                    </p>
                    <p className="text-[var(--juba-muted)] text-sm leading-relaxed">
                      {nativeHelp.explanation}
                    </p>
                  </div>

                  {nativeHelp.key_points.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpKeyPoints')}
                      </p>
                      <ul className="space-y-1">
                        {nativeHelp.key_points.map((point, i) => (
                          <li key={i} className="text-[var(--juba-muted)] text-sm">
                            <span className="text-[var(--juba-muted)] mr-2">·</span>
                            {point}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {nativeHelp.examples.length > 0 && (
                    <div className="border-[var(--juba-lilac)] space-y-2 border-t pt-3">
                      <p className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
                        {t('examples')}
                      </p>
                      {nativeHelp.examples.map((ex, i) => (
                        <div key={i} className="space-y-0.5">
                          <TargetLanguageText
                            languageCode={targetLanguageCode}
                            className="text-[var(--juba-muted)] text-sm italic"
                          >
                            {ex.sentence}
                          </TargetLanguageText>
                          <p className="text-[var(--juba-muted)] text-sm">{ex.note}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {nativeHelp.common_traps.length > 0 && (
                    <div className="border-[var(--juba-lilac)] space-y-2 border-t pt-3">
                      <p className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpCommonTraps')}
                      </p>
                      {nativeHelp.common_traps.map((trap, i) => (
                        <div key={i} className="space-y-0.5">
                          <p className="text-[var(--juba-muted)] text-sm">
                            {trap.mistake}
                          </p>
                          <p className="text-[var(--juba-muted)] text-sm">{trap.fix}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {nativeHelp.mini_glossary.length > 0 && (
                    <div className="border-[var(--juba-lilac)] space-y-2 border-t pt-3">
                      <p className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
                        {tCommon('nativeHelpMiniGlossary')}
                      </p>
                      {nativeHelp.mini_glossary.map((item, i) => (
                        <div key={i}>
                          <TargetLanguageText
                            languageCode={targetLanguageCode}
                            className="text-[var(--juba-muted)] text-sm font-bold"
                          >
                            {item.term}
                          </TargetLanguageText>
                          <p className="text-[var(--juba-muted)] text-sm">
                            {item.meaning}
                          </p>
                          {item.note && (
                            <p className="text-[var(--juba-muted)] text-sm">
                              {item.note}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <div className="text-center">
                  <button
                    type="button"
                    onClick={generateNativeHelp}
                    className="text-[var(--juba-muted)] hover:text-[var(--juba-text)] font-mono text-sm transition-colors"
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

      {topic.rules.length > 0 && (
        <div className="border-[var(--juba-lilac)] bg-white border">
          <div className="border-[var(--juba-lilac)] flex items-center gap-2 border-b px-6 py-4">
            <span className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
              {t('keyRules')}
            </span>
          </div>
          <ul className="space-y-2 px-6 py-5">
            {topic.rules.map((rule, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-[var(--juba-text)] text-[var(--juba-muted)] mt-0.5 shrink-0 font-mono">
                  {i + 1}.
                </span>
                <p className="text-[var(--juba-muted)] font-mono text-xs leading-relaxed">
                  {rule}
                </p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {topic.examples.length > 0 && (
        <div className="border-[var(--juba-lilac)] bg-white border">
          <div className="border-[var(--juba-lilac)] flex items-center gap-2 border-b px-6 py-4">
            <span className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
              {t('examples')}
            </span>
          </div>
          <div className="space-y-3 px-6 py-5">
            {topic.examples.map((ex, i) => (
              <div
                key={i}
                className="border-[var(--juba-lilac)] space-y-0.5 border-l-2 pl-4"
              >
                <p className="text-[var(--juba-text)] font-mono text-xs">{ex.text}</p>
                {ex.note && (
                  <p className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono italic">
                    {ex.note}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {topic.common_mistakes.length > 0 && (
        <div className="border-[var(--juba-lilac)] bg-white border">
          <div className="border-[var(--juba-lilac)] flex items-center gap-2 border-b px-6 py-4">
            <span className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
              {t('commonMistakes')}
            </span>
          </div>
          <div className="space-y-4 px-6 py-5">
            {topic.common_mistakes.map((m, i) => (
              <div key={i} className="space-y-1.5">
                {m.wrong && (
                  <div className="flex items-start gap-2">
                    <span className="text-[var(--juba-text)] shrink-0 font-mono text-red-500">
                      {'\u2717'}
                    </span>
                    <p className="text-[var(--juba-muted)] font-mono text-xs line-through">
                      {m.wrong}
                    </p>
                  </div>
                )}
                {m.correct && (
                  <div className="flex items-start gap-2">
                    <span className="text-[var(--juba-text)] shrink-0 font-mono text-green-500">
                      {'\u2713'}
                    </span>
                    <p className="text-[var(--juba-text)] font-mono text-xs">{m.correct}</p>
                  </div>
                )}
                {m.note && (
                  <p className="text-[var(--juba-text)] text-[var(--juba-muted)] pl-5 font-mono">
                    {m.note}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {relatedTopics.length > 0 && (
        <div className="border-[var(--juba-lilac)] bg-white border">
          <div className="border-[var(--juba-lilac)] flex items-center gap-2 border-b px-6 py-4">
            <span className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
              {t('relatedTopics')}
            </span>
          </div>
          <div className="flex flex-wrap gap-2 px-6 py-5">
            {relatedTopics.map(
              (rt) =>
                rt && (
                  <Link
                    key={rt.slug}
                    href={`/grammar/${rt.slug}`}
                    className="border-[var(--juba-lilac)] text-[var(--juba-text)] text-[var(--juba-muted)] hover:border-[var(--juba-violet)] hover:text-[var(--juba-text)] border px-3 py-2 font-mono tracking-widest uppercase transition-colors"
                  >
                    {'\u25cf'} {rt.title}
                    <span className="text-[var(--juba-muted)] ml-2">{rt.level}</span>
                  </Link>
                )
            )}
          </div>
        </div>
      )}

      <Link
        href="/grammar"
        className="text-[var(--juba-text)] text-[var(--juba-muted)] hover:text-[var(--juba-text)] inline-block font-mono tracking-widest uppercase transition-colors"
      >
        {'\u2190'} {t('backLink')}
      </Link>
    </div>
  )
}
