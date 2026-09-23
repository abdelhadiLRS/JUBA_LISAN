'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { ArrowRight, Globe2, Plus, Sparkles, Flame, Trophy } from 'lucide-react'
import { useLanguageStore } from '@/store/language'
import {
  getLanguageByCode,
  TARGET_LANGUAGE_CATALOG,
} from '@/lib/target-languages'
import TargetLanguageSelector from '@/components/TargetLanguageSelector'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import type { UserLanguageInfo } from '@/store/language'

export default function MyLanguagesPage() {
  const t = useTranslations('languages')
  const tTarget = useTranslations('targetLanguages')
  const tSettings = useTranslations('settings')
  const tCommon = useTranslations('common')
  const router = useRouter()
  const userLanguages = useLanguageStore((s) => s.userLanguages)
  const fetchLanguages = useLanguageStore((s) => s.fetchLanguages)
  const switchLanguage = useLanguageStore((s) => s.switchLanguage)
  const addLanguage = useLanguageStore((s) => s.addLanguage)
  const removeLanguage = useLanguageStore((s) => s.removeLanguage)

  const [addModalOpen, setAddModalOpen] = useState(false)
  const [deleteTarget, setDeleteTarget] = useState<UserLanguageInfo | null>(
    null
  )
  const [addingCode, setAddingCode] = useState('')
  const [switchingCode, setSwitchingCode] = useState<string | null>(null)
  const [toast, setToast] = useState('')
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    await fetchLanguages()
    setLoading(false)
  }, [fetchLanguages])

  useEffect(() => {
    load()
  }, [load])

  function getLangInfo(code: string) {
    return getLanguageByCode(code)
  }

  async function handleSwitch(info: UserLanguageInfo) {
    if (info.is_active) return
    setSwitchingCode(info.target_language)
    const ok = await switchLanguage(info.target_language)
    setSwitchingCode(null)
    if (ok) {
      const level = info.plan?.cefr_level ?? ''
      setToast(
        t('switched', { language: tTarget(info.target_language), level })
      )
      setTimeout(() => setToast(''), 2500)
      router.refresh()
    }
  }

  async function handleDelete() {
    if (!deleteTarget) return
    const ok = await removeLanguage(deleteTarget.target_language)
    if (!ok) {
      setToast(
        t('deleteError', {
          language: tTarget(deleteTarget.target_language),
        })
      )
      setDeleteTarget(null)
      return
    }
    setDeleteTarget(null)
  }

  async function handleAdd() {
    if (!addingCode) return
    const ok = await addLanguage(addingCode)
    if (!ok) return
    setAddModalOpen(false)
    setAddingCode('')
    router.push(`/assessment`)
  }

  const availableLanguageCodes = useLanguageStore(
    (s) => s.availableLanguageCodes
  )
  const addedCodes = userLanguages.map((ul) => ul.target_language)
  // Only show operator-enabled languages that the user hasn't added yet
  const unusedCodes = TARGET_LANGUAGE_CATALOG.filter(
    (l) =>
      availableLanguageCodes.includes(l.code) && !addedCodes.includes(l.code)
  ).map((l) => l.code)
  const hasMultiple = userLanguages.length > 1

  return (
    <div className="mx-auto max-w-5xl space-y-6 p-4 sm:p-6">
      {/* Toast */}
      {toast && (
        <div className="pointer-events-none fixed inset-x-0 top-16 z-50 flex justify-center">
          <div className="animate-in fade-in slide-in-from-top-2 border-fl-border bg-fl-surface text-fl-muted-1 pointer-events-auto border px-4 py-2 font-mono text-xs tracking-widest uppercase shadow-lg">
            {toast}
          </div>
        </div>
      )}

      {/* Breadcrumb */}
      <nav className="text-fl-label text-fl-muted-3 mb-8 flex items-center gap-2 font-mono">
        <Link
          href="/settings"
          className="hover:text-fl-fg tracking-widest uppercase transition-colors"
        >
          {tSettings('title')}
        </Link>
        <span>›</span>
        <span className="text-fl-fg tracking-widest uppercase">
          {t('myLanguages')}
        </span>
      </nav>

      <section className="juba-card relative overflow-hidden p-6 sm:p-8">
        <div className="relative z-10 flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="juba-eyebrow"><Globe2 className="h-4 w-4" /> {t('myLanguages')}</div>
            <h1 className="mt-3 text-3xl font-black tracking-tight text-fl-fg sm:text-4xl">{t('myLanguages')}</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-fl-muted-2">{t('sectionLanguages')}</p>
          </div>
          {unusedCodes.length > 0 && (
            <button onClick={() => setAddModalOpen(true)} className="inline-flex items-center justify-center gap-2 rounded-xl bg-[var(--juba-primary)] px-5 py-3 text-sm font-bold text-white transition hover:bg-[var(--juba-primary-dark)]">
              <Plus className="h-4 w-4" /> {t('addLanguage')}
            </button>
          )}
        </div>
        <div className="juba-hero-glow" aria-hidden="true" />
      </section>

      {/* Header + Add button */}
      <div className="mb-2 flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-[.16em] text-fl-muted-2"><Sparkles className="h-4 w-4" /> {t('myLanguages')}</div>
      </div>

      {/* Language cards */}
      {loading ? (
        <PageLoading />
      ) : userLanguages.length === 0 ? (
        <div className="border-fl-border bg-fl-surface border px-6 py-10 text-center">
          <p className="text-fl-muted-2 font-mono text-sm">
            {t('noLanguages')}
          </p>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {[...userLanguages]
            .sort((a, b) =>
              tTarget(a.target_language).localeCompare(
                tTarget(b.target_language)
              )
            )
            .map((ulang) => {
              const lang = getLangInfo(ulang.target_language)
              const isActive = ulang.is_active
              const plan = ulang.plan
              const progress = ulang.progress

              return (
                <div
                  key={ulang.target_language}
                  className={`juba-card relative overflow-hidden p-5 transition-all hover:-translate-y-0.5 hover:shadow-[0_12px_35px_rgba(15,23,42,0.08)] ${isActive ? 'ring-2 ring-[var(--juba-primary)]' : ''}`}
                >
                  {/* Top row: flag + name + status */}
                  <div className="mb-3 flex items-center gap-3">
                    {lang && (
                      <Image
                        src={lang.flagPath}
                        alt={lang.code}
                        width={28}
                        height={20}
                        className="shrink-0 object-cover"
                      />
                    )}
                    <span className="text-fl-fg flex-1 text-base font-black">
                      {tTarget(ulang.target_language)}
                    </span>
                    {isActive ? (
                      <span className="rounded-full bg-[var(--juba-primary-soft)] px-2.5 py-1 text-[10px] font-black uppercase tracking-widest text-[var(--juba-primary-dark)]">
                        {t('activeLanguage')}
                      </span>
                    ) : plan?.cefr_level ? (
                      <span className="rounded-full bg-fl-surface-2 px-2.5 py-1 text-[10px] font-black tracking-widest text-fl-muted-2">
                        {plan.cefr_level}
                      </span>
                    ) : null}
                  </div>

                  {/* Stats */}
                  {plan && (
                    <div className="mb-4 grid grid-cols-2 gap-2 text-xs">
                      <span>
                        {t('levelLabel')}: {plan.cefr_level ?? '—'}
                      </span>
                      <span>
                        {t('progressLabel')}: {plan.completion_pct}%
                      </span>
                      {progress && (
                        <>
                          <span className="rounded-xl bg-[var(--juba-primary-soft)] px-3 py-2 font-bold"><Sparkles className="mr-1 inline h-3.5 w-3.5" />{progress.total_xp.toLocaleString()} XP</span>
                          <span className="rounded-xl bg-[var(--juba-warm-soft)] px-3 py-2 font-bold"><Flame className="mr-1 inline h-3.5 w-3.5" />{progress.current_streak}d</span>
                          <span className="rounded-xl bg-fl-surface-2 px-3 py-2 font-bold"><Trophy className="mr-1 inline h-3.5 w-3.5" />{progress.lessons_completed}</span>
                        </>
                      )}
                    </div>
                  )}

                  {/* Actions */}
                  <div className="mt-4 flex items-center gap-2">
                    {isActive ? (
                      <button
                        onClick={() => router.push(`/plan`)}
                        className="inline-flex items-center gap-1 rounded-xl bg-[var(--juba-primary-soft)] px-3 py-2 text-xs font-bold text-[var(--juba-primary-dark)] transition-colors hover:bg-[var(--juba-primary)] hover:text-white"
                      >
                        {t('viewDetails')} →
                      </button>
                    ) : (
                      <>
                        <button
                          onClick={() => handleSwitch(ulang)}
                          disabled={switchingCode === ulang.target_language}
                          className="text-fl-label text-fl-bg bg-fl-fg hover:bg-fl-accent/90 px-3 py-1 font-mono text-xs tracking-widest uppercase transition-colors disabled:opacity-40"
                        >
                          {switchingCode === ulang.target_language
                            ? '...'
                            : t('switchTo')}
                        </button>
                        {hasMultiple && (
                          <button
                            onClick={() => setDeleteTarget(ulang)}
                            className="text-fl-label text-fl-muted-3 hover:text-fl-error font-mono text-xs tracking-widest uppercase transition-colors"
                          >
                            {t('removeLanguage')}
                          </button>
                        )}
                      </>
                    )}
                  </div>
                </div>
              )
            })}
        </div>
      )}

      {/* Add language modal */}
      {addModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-fl-bg border-fl-border w-full max-w-lg border p-6 shadow-xl">
            <h2 className="text-fl-fg mb-4 font-mono text-sm font-bold tracking-widest uppercase">
              {t('selectLanguage')}
            </h2>
            <TargetLanguageSelector
              value={addingCode}
              onChange={setAddingCode}
              availableCodes={unusedCodes}
            />
            <div className="mt-5 flex justify-end gap-2">
              <button
                onClick={() => setAddModalOpen(false)}
                className="text-fl-label text-fl-muted-3 hover:text-fl-fg px-4 py-2 font-mono text-xs tracking-widest uppercase transition-colors"
              >
                {tCommon('cancel')}
              </button>
              <button
                onClick={handleAdd}
                disabled={!addingCode}
                className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 px-4 py-2 font-mono text-xs font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
              >
                {t('addLanguage')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Delete confirmation */}
      <ConfirmDialog
        open={deleteTarget !== null}
        title={t('removeConfirmTitle', {
          language: deleteTarget ? tTarget(deleteTarget.target_language) : '',
        })}
        message={t('removeConfirmMessage')}
        confirmLabel={t('removeConfirmButton')}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
