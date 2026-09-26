'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { PageLoading } from '@/components/ui/page-loading'
import { apiFetch } from '@/lib/api'
import { subscribeToLearningProgressUpdated } from '@/lib/learning-progress'
import { useLanguageStore } from '@/store/language'
import NoPlanBanner from '@/components/plan/NoPlanBanner'
import {
  getCurriculumUnits,
  type CurriculumUnit,
  type CEFRLevel,
} from '@/data/curriculum'
import type { VocabularySet } from '@/data/types'

// ── Types ──────────────────────────────────────────────────────────────────────

interface CompetencyRecord {
  unit_id: string
  score: number // 0–1 average
  mastered_count: number
  total_count: number
}

interface MasterySkillSummary {
  items: number
  average_score: number
  counts: Record<string, number>
}

interface MasterySummary {
  tracked_items: number
  average_score: number
  counts: Record<string, number>
  skills: Record<string, MasterySkillSummary>
}

interface ProgressSummary {
  total_xp: number
  current_streak: number
  total_lessons: number
  total_exercises: number
  exercises_correct: number
  accuracy: number
  skills: Record<string, number>
  mastery: MasterySummary
}

interface FlashcardProgress {
  id: number
  word: string
  repetitions: number
}

interface StudyPlan {
  id: number
  cefr_level: string
}

type CompetencyStatus = 'mastered' | 'in-progress' | 'not-started'

// ── Helpers ────────────────────────────────────────────────────────────────────

function getCompetencyStatus(
  itemIndex: number,
  masteredCount: number,
  totalCount: number,
  score: number
): CompetencyStatus {
  if (itemIndex < masteredCount) return 'mastered'
  if (score > 0 && itemIndex < totalCount) return 'in-progress'
  return 'not-started'
}

const STATUS_ICON: Record<CompetencyStatus, string> = {
  mastered: '✅',
  'in-progress': '🔄',
  'not-started': '⬜',
}

const STATUS_COLOR: Record<CompetencyStatus, string> = {
  mastered: 'text-[#202127]',
  'in-progress': 'text-amber-600 dark:text-amber-400',
  'not-started': 'text-[rgba(32,33,39,.52)]',
}

// ── Sub-components ────────────────────────────────────────────────────────────

function UnitCompetencyBlock({
  unit,
  record,
}: {
  unit: CurriculumUnit
  record: CompetencyRecord | undefined
}) {
  const t = useTranslations('progress')
  const tPlan = useTranslations('plan')
  const masteredCount = record?.mastered_count ?? 0
  const totalCount = unit.competency_checklist.length
  const score = record?.score ?? 0
  const pct =
    totalCount > 0 ? Math.round((masteredCount / totalCount) * 100) : 0

  return (
    <div className="card">
      {/* Unit header */}
      <div className="card-header d-flex align-items-center justify-content-between">
        <div className="flex items-center gap-2">
          <span className="text-[rgba(32,33,39,.52)] font-sans tracking-[.12em] uppercase">
            {tPlan('unitLabel')} {unit.unit_number}
          </span>
          <span className="text-[#202127] font-mono text-xs font-bold">
            {unit.title}
          </span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-[rgba(32,33,39,.52)] font-mono">
            {masteredCount}/{totalCount} {t('mastered')}
          </span>
          {record && (
            <span className="text-[rgba(32,33,39,.52)] font-mono">
              {Math.round(score * 100)}%
            </span>
          )}
        </div>
      </div>

      {/* Progress bar */}
      <div className="bg-[rgba(7,7,9,.08)] h-0.5">
        <div
          className="bg-[#5862e2] h-full transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>

      {/* Competency list */}
      <ul className="space-y-2 px-5 py-3">
        {unit.competency_checklist.map((text, idx) => {
          const status = getCompetencyStatus(
            idx,
            masteredCount,
            record?.total_count ?? 0,
            score
          )
          return (
            <li key={idx} className="flex items-start gap-3">
              <span className="mt-0.5 shrink-0 text-base leading-none">
                {STATUS_ICON[status]}
              </span>
              <span
                className={`font-mono text-xs leading-relaxed ${STATUS_COLOR[status]}`}
              >
                {text}
              </span>
              {status === 'in-progress' && record && (
                <span className="text-[rgba(32,33,39,.52)] ml-auto shrink-0 font-mono">
                  {Math.round(score * 100)}%
                </span>
              )}
            </li>
          )
        })}
      </ul>
    </div>
  )
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function ProgressPage() {
  const t = useTranslations('progress')
  const tVocab = useTranslations('vocabulary')
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const [summary, setSummary] = useState<ProgressSummary | null>(null)
  const [competencies, setCompetencies] = useState<CompetencyRecord[]>([])
  const [plan, setPlan] = useState<StudyPlan | null>(null)
  const [loading, setLoading] = useState(true)
  const [levelUnits, setLevelUnits] = useState<CurriculumUnit[]>([])
  const [flashcards, setFlashcards] = useState<FlashcardProgress[]>([])
  const [showAllLevels, setShowAllLevels] = useState(false)
  const [refreshToken, setRefreshToken] = useState(0)

  useEffect(() => {
    async function load() {
      try {
        const [sumRes, compRes, planRes, flashRes] = await Promise.all([
          apiFetch('/api/progress/summary'),
          apiFetch('/api/progress/competencies'),
          apiFetch('/api/study-plan/current'),
          apiFetch('/api/flashcards/all').catch(() => null),
        ])
        if (sumRes.ok) setSummary((await sumRes.json()) as ProgressSummary)
        if (compRes.ok)
          setCompetencies((await compRes.json()) as CompetencyRecord[])
        if (planRes.ok) setPlan((await planRes.json()) as StudyPlan)
        if (flashRes?.ok)
          setFlashcards((await flashRes.json()) as FlashcardProgress[])
      } catch {
        /* ignore */
      } finally {
        setLoading(false)
      }
    }
    void load()
  }, [activeLanguage?.code, refreshToken])

  useEffect(() => {
    return subscribeToLearningProgressUpdated(() => {
      setRefreshToken((value) => value + 1)
    })
  }, [])

  const targetLanguageCode = activeLanguage?.code ?? 'en-GB'

  useEffect(() => {
    if (plan?.cefr_level) {
      getCurriculumUnits(plan.cefr_level, targetLanguageCode)
        .then(setLevelUnits)
        .catch(() => setLevelUnits([]))
    }
  }, [plan?.cefr_level, targetLanguageCode])

  const [vocabSets, setVocabSets] = useState<VocabularySet[]>([])

  useEffect(() => {
    apiFetch(`/api/vocabulary?language=${targetLanguageCode}`)
      .then((r) => r.json())
      .then((d: { sets: VocabularySet[] }) => setVocabSets(d.sets))
      .catch(() => setVocabSets([]))
  }, [targetLanguageCode])

  const compMap = Object.fromEntries(competencies.map((c) => [c.unit_id, c]))

  if (loading) {
    return <PageLoading label={t('loading')} />
  }

  if (!plan) {
    return <NoPlanBanner />
  }

  const cefrLevel = plan.cefr_level as CEFRLevel
  const displayVocabSets = showAllLevels
    ? vocabSets
    : vocabSets.filter((s) => s.level === cefrLevel)
  const totalDisplayWords = displayVocabSets.reduce(
    (a, s) => a + s.words.length,
    0
  )

  const masteredWordSet = new Set(
    flashcards.filter((f) => f.repetitions > 0).map((f) => f.word.toLowerCase())
  )
  const totalMastered = displayVocabSets.reduce(
    (a, s) =>
      a +
      s.words.filter((w) => masteredWordSet.has(w.word.toLowerCase())).length,
    0
  )

  return (
    <div className="container-xl page-body py-4">
      {/* Header */}
      <div className="border-[rgba(7,7,9,.08)] bg-[#fff] border">
        <div className="card-header d-flex align-items-center gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-2xl bg-[#ededff] text-[#5862e2]"><i className="ti ti-target icon" aria-hidden="true" /></span>
          <span className="text-[rgba(32,33,39,.52)] font-sans tracking-[.12em] uppercase">
            {t('subtitle')}
          </span>
          {activeLanguage && cefrLevel && (
            <span className="border-[rgba(7,7,9,.08)] text-[rgba(32,33,39,.52)] ml-auto border px-2 py-0.5 font-sans tracking-[.12em] uppercase">
              {activeLanguage.name} · {cefrLevel}
            </span>
          )}
        </div>

        {/* XP + streak */}
        {summary && (
          <div className="juba-progress-metrics divide-fl-border border-[rgba(7,7,9,.08)] grid grid-cols-2 divide-x border-b sm:grid-cols-4">
            {[
              { label: t('xp'), value: summary.total_xp.toLocaleString() },
              { label: t('streak'), value: `${summary.current_streak}d 🔥` },
              { label: t('lessons'), value: summary.total_lessons },
              {
                label: t('accuracy'),
                value: `${Math.round(summary.accuracy * 100)}%`,
              },
            ].map(({ label, value }) => (
              <div key={label} className="px-5 py-4 text-center">
                <p className="text-[rgba(32,33,39,.52)] mb-1 font-sans tracking-[.12em] uppercase">
                  {label}
                </p>
                <p className="text-[#202127] font-mono text-sm font-bold">
                  {value}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Tracked item mastery */}
      {summary && summary.mastery && summary.mastery.tracked_items > 0 && (
        <section className="juba-progress-section space-y-4">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#ededff] text-[#5862e2]"><i className="ti ti-trophy icon" aria-hidden="true" /></span>
            <span className="text-[#202127] font-mono text-base font-bold tracking-widest">
              {t('skills')} · {t('mastered')}
            </span>
            <div className="bg-[rgba(7,7,9,.08)] h-px flex-1" />
            <span className="text-[rgba(32,33,39,.52)] font-mono text-xs">
              {summary.mastery.tracked_items} {tVocab('words')}
            </span>
          </div>
          <div className="card">
            <div className="mb-4 flex items-center justify-between">
              <span className="text-[rgba(32,33,39,.52)] font-sans tracking-[.12em] uppercase">{t('accuracy')}</span>
              <span className="text-[#202127] font-mono text-lg font-bold">{Math.round(summary.mastery.average_score * 100)}%</span>
            </div>
            <div className="bg-[rgba(7,7,9,.08)] mb-5 h-1.5">
              <div className="bg-[#5862e2] h-full transition-all" style={{ width: (Math.round(summary.mastery.average_score * 100) + '%') }} />
            </div>
            <div className="grid grid-cols-2 gap-2 sm:grid-cols-5">
              {(['new', 'learning', 'reviewing', 'weak', 'mastered'] as const).map((state) => {
                const count = summary.mastery.counts?.[state] ?? 0
                const label = state === 'mastered' ? t('mastered') : state === 'new' ? t('notStarted') : t('inProgress')
                return (
                  <div key={state} className="border-[rgba(7,7,9,.08)] border px-3 py-3 text-center">
                    <p className="text-[rgba(32,33,39,.52)] mb-1 font-sans text-[10px] tracking-[.12em] uppercase">{label}</p>
                    <p className="text-[#202127] font-mono text-sm font-bold">{count}</p>
                  </div>
                )
              })}
            </div>
          </div>
          {Object.keys(summary.mastery.skills).length > 0 && (
            <div className="card">
              {Object.entries(summary.mastery.skills).map(([skill, data]) => (
                <div key={skill} className="px-5 py-4">
                  <div className="mb-2 flex items-center justify-between gap-4">
                    <span className="text-[rgba(32,33,39,.52)] font-sans tracking-[.12em] uppercase">{skill}</span>
                    <span className="text-[rgba(32,33,39,.52)] font-mono text-xs">{Math.round(data.average_score * 100)}% · {data.items}</span>
                  </div>
                  <div className="bg-[rgba(7,7,9,.08)] h-1.5">
                    <div className="bg-[#5862e2] h-full transition-all" style={{ width: (Math.round(data.average_score * 100) + '%') }} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      )}
      {/* Grammar Competencies */}
      {levelUnits.length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-[#fff3d1] text-[#9a6500]"><i className="ti ti-book-2 icon" aria-hidden="true" /></span>
            <span className="text-[#202127] font-mono text-base font-bold tracking-widest">
              {cefrLevel
                ? t('competenciesSection', { level: cefrLevel })
                : t('competencies')}
            </span>
            <div className="bg-[rgba(7,7,9,.08)] h-px flex-1" />
          </div>

          {levelUnits.map((unit) => (
            <UnitCompetencyBlock
              key={unit.id}
              unit={unit}
              record={compMap[unit.id]}
            />
          ))}

          {competencies.length === 0 && (
            <div className="border-[rgba(7,7,9,.08)] bg-[#fff] border px-6 py-8 text-center">
              <p className="text-[rgba(32,33,39,.52)] font-mono text-xs leading-relaxed">
                {t('noCompetencies')}
              </p>
              <Link
                href="/plan"
                className="text-[rgba(32,33,39,.52)] text-[rgba(32,33,39,.52)] hover:text-[#202127] mt-4 inline-block font-sans tracking-[.12em] uppercase transition-colors"
              >
                {t('goToMyPlan')}
              </Link>
            </div>
          )}
        </section>
      )}

      {/* Vocabulary Progress */}
      {displayVocabSets.length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center gap-3">
            <span className="text-[#202127] font-mono text-base font-bold tracking-widest">
              {showAllLevels
                ? t('vocabularySection')
                : cefrLevel
                  ? t('vocabularyHeader', { level: cefrLevel })
                  : t('vocabularySection')}
            </span>
            <div className="bg-[rgba(7,7,9,.08)] h-px flex-1" />
            <span className="text-[rgba(32,33,39,.52)] font-mono">
              {totalMastered}/{totalDisplayWords} {tVocab('words')}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowAllLevels(false)}
              className={`text-[rgba(32,33,39,.52)] border px-3 py-1.5 font-sans tracking-[.12em] uppercase transition-colors ${
                !showAllLevels
                  ? 'border-[#202127] text-[#202127] bg-[#ededff]'
                  : 'border-[rgba(7,7,9,.08)] text-[rgba(32,33,39,.52)] hover:border-[#202127] hover:text-[#202127]'
              }`}
            >
              {t('currentLevelOnly')}
            </button>
            <button
              onClick={() => setShowAllLevels(true)}
              className={`text-[rgba(32,33,39,.52)] border px-3 py-1.5 font-sans tracking-[.12em] uppercase transition-colors ${
                showAllLevels
                  ? 'border-[#202127] text-[#202127] bg-[#ededff]'
                  : 'border-[rgba(7,7,9,.08)] text-[rgba(32,33,39,.52)] hover:border-[#202127] hover:text-[#202127]'
              }`}
            >
              {t('allLevels')}
            </button>
          </div>

          <div className="border-[rgba(7,7,9,.08)] bg-[#fff] divide-fl-border divide-y border">
            {displayVocabSets.map((s) => {
              const mastered = s.words.filter((w) =>
                masteredWordSet.has(w.word.toLowerCase())
              ).length
              const pct =
                s.words.length > 0
                  ? Math.round((mastered / s.words.length) * 100)
                  : 0
              return (
                <div key={s.id} className="flex items-center gap-4 px-5 py-3">
                  <Link
                    href={`/vocabulary/${s.id}`}
                    className="text-[rgba(32,33,39,.52)] hover:text-[#202127] min-w-0 flex-1 truncate font-mono text-xs transition-colors"
                  >
                    {s.topic}
                  </Link>
                  <div className="flex items-center gap-3">
                    <div className="bg-[rgba(7,7,9,.08)] h-1.5 w-24">
                      <div
                        className="bg-[#5862e2] h-full transition-all"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    <span className="text-[rgba(32,33,39,.52)] w-12 text-right font-mono">
                      {mastered}/{s.words.length}
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        </section>
      )}

      {/* Skills breakdown */}
      {summary && Object.keys(summary.skills).length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center gap-3">
            <span className="text-[#202127] font-mono text-base font-bold tracking-widest">
              {t('skills')}
            </span>
            <div className="bg-[rgba(7,7,9,.08)] h-px flex-1" />
          </div>
          <div className="border-[rgba(7,7,9,.08)] bg-[#fff] divide-fl-border divide-y border">
            {Object.entries(summary.skills).map(([skill, value]) => (
              <div key={skill} className="flex items-center gap-4 px-5 py-3">
                <span className="text-[rgba(32,33,39,.52)] w-24 font-sans tracking-[.12em] uppercase">
                  {skill}
                </span>
                <div className="bg-[rgba(7,7,9,.08)] h-1.5 flex-1">
                  <div
                    className="bg-[#5862e2] h-full"
                    style={{ width: `${Math.round(value * 100)}%` }}
                  />
                </div>
                <span className="text-[rgba(32,33,39,.52)] text-[rgba(32,33,39,.52)] w-10 text-right font-mono">
                  {Math.round(value * 100)}%
                </span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
