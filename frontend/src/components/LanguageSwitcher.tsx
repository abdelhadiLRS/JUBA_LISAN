'use client'

import { useEffect, useState, useRef, useMemo } from 'react'
import Image from 'next/image'
import { Check, ChevronDown, ChevronUp, Languages, Loader2 } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { useLanguageStore } from '@/store/language'
import { getLanguageByCode } from '@/lib/target-languages'

export default function LanguageSwitcher() {
  const tLang = useTranslations('languages')
  const tTarget = useTranslations('targetLanguages')
  const router = useRouter()
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const userLanguages = useLanguageStore((s) => s.userLanguages)
  const isSwitching = useLanguageStore((s) => s.isSwitching)
  const fetchLanguages = useLanguageStore((s) => s.fetchLanguages)
  const switchLanguage = useLanguageStore((s) => s.switchLanguage)
  const [open, setOpen] = useState(false)
  const [toast, setToast] = useState(false)
  const [toastMsg, setToastMsg] = useState('')
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => { fetchLanguages() }, [fetchLanguages])
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    if (!open) return
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [open])

  async function handleSwitch(code: string) {
    setOpen(false)
    if (code === activeLanguage?.code) return
    const targetInfo = userLanguages.find((l) => l.target_language === code)
    const ok = await switchLanguage(code)
    if (ok) {
      const langName = tTarget(code)
      setToastMsg(targetInfo?.plan?.cefr_level ? tLang('switched', { language: langName, level: targetInfo.plan.cefr_level }) : langName)
      setToast(true)
      setTimeout(() => setToast(false), 2500)
      router.refresh()
    }
  }

  const skeleton = useMemo(() => (
    <div className="flex items-center gap-2 rounded-[14px] border border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] px-3 py-2.5 shadow-[2px_2px_0_var(--juba-app-ink)] animate-pulse" aria-label="Loading languages">
      <div className="h-3.5 w-5 rounded bg-[var(--juba-app-line)]" />
      <div className="h-3 w-20 rounded bg-[var(--juba-app-line)]" />
    </div>
  ), [])

  if (!activeLanguage) return skeleton
  const supportedUserLanguages = userLanguages.filter((ulang) => getLanguageByCode(ulang.target_language))
  const multiple = supportedUserLanguages.length > 1

  return (
    <div ref={ref} className="relative w-full">
      {toast && (
        <div className="pointer-events-none fixed inset-x-0 top-20 z-[100] flex justify-center px-4" role="status" aria-live="polite">
          <div className="pointer-events-auto flex items-center gap-2 rounded-[14px] border-2 border-[var(--juba-app-ink)] bg-[var(--juba-app-surface)] px-4 py-3 text-xs font-bold text-[var(--juba-app-ink)] shadow-[4px_4px_0_var(--juba-app-ink)]">
            <Check className="h-4 w-4 text-[var(--juba-app-green)]" aria-hidden="true" />
            {toastMsg}
          </div>
        </div>
      )}

      <button
        type="button"
        onClick={() => multiple && setOpen(!open)}
        disabled={!multiple || isSwitching}
        aria-expanded={multiple ? open : undefined}
        aria-haspopup={multiple ? 'listbox' : undefined}
        aria-label={multiple ? 'Switch target language' : `Current target language: ${tTarget(activeLanguage.code)}`}
        className="group flex w-full items-center gap-3 rounded-[14px] border border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] px-3.5 py-2.5 text-left text-sm font-bold text-[var(--juba-app-ink)] shadow-[2px_2px_0_var(--juba-app-ink)] transition-all hover:-translate-y-0.5 hover:shadow-[3px_3px_0_var(--juba-app-ink)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)] focus-visible:ring-offset-2 disabled:cursor-default disabled:hover:translate-y-0 disabled:hover:shadow-[2px_2px_0_var(--juba-app-ink)]"
      >
        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-[10px] bg-[var(--juba-app-green-soft)]">
          <Image src={activeLanguage.flagPath} alt="" width={22} height={15} className="rounded-sm object-cover ring-1 ring-black/10" />
        </span>
        <span className="min-w-0 flex-1 truncate">{isSwitching ? 'Switching…' : tTarget(activeLanguage.code)}</span>
        {isSwitching ? (
          <Loader2 className="h-4 w-4 shrink-0 animate-spin text-[var(--juba-app-green)]" aria-hidden="true" />
        ) : multiple && (open
          ? <ChevronUp className="h-4 w-4 shrink-0" aria-hidden="true" />
          : <ChevronDown className="h-4 w-4 shrink-0" aria-hidden="true" />)}
      </button>

      {open && multiple && (
        <div className="absolute left-0 right-0 top-[calc(100%+8px)] z-50 overflow-hidden rounded-[18px] border-2 border-[var(--juba-app-ink)] bg-[var(--juba-app-surface)] p-1.5 shadow-[5px_5px_0_var(--juba-app-ink)]" role="listbox" aria-label="Available target languages">
          <div className="flex items-center gap-2 px-2.5 py-2 text-[10px] font-black uppercase tracking-[.12em] text-[var(--juba-app-muted)]">
            <Languages className="h-3.5 w-3.5" aria-hidden="true" />
            Your languages
          </div>
          {[...supportedUserLanguages].sort((a, b) => tTarget(a.target_language).localeCompare(tTarget(b.target_language))).map((ulang) => {
            const lang = getLanguageByCode(ulang.target_language)
            if (!lang) return null
            return (
              <button
                key={ulang.target_language}
                type="button"
                role="option"
                aria-selected={ulang.is_active}
                disabled={isSwitching}
                onClick={() => handleSwitch(ulang.target_language)}
                className={`flex w-full items-center gap-3 rounded-[12px] px-3 py-2.5 text-left text-sm font-bold transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)] focus-visible:ring-inset disabled:cursor-wait disabled:opacity-60 ${
                  ulang.is_active
                    ? 'bg-[var(--juba-app-green-soft)] text-[var(--juba-app-ink)]'
                    : 'text-[var(--juba-app-ink)] hover:bg-[var(--juba-app-green-soft)]'
                }`}
              >
                <Image src={lang.flagPath} alt="" width={22} height={15} className="shrink-0 rounded-sm object-cover ring-1 ring-black/10" />
                <span className="min-w-0 flex-1 truncate">{tTarget(lang.code)}</span>
                {ulang.plan?.cefr_level && (
                  <span className="rounded-full bg-[var(--juba-app-yellow)] px-2 py-0.5 text-[10px] font-black text-[var(--juba-app-ink)]">
                    {ulang.plan.cefr_level}
                  </span>
                )}
                {ulang.is_active && <Check className="h-4 w-4 text-[var(--juba-app-green)]" aria-hidden="true" />}
              </button>
            )
          })}
        </div>
      )}
    </div>
  )
}
