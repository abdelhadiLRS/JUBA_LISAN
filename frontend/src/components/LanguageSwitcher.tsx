'use client'

import { useEffect, useState, useRef, useMemo } from 'react'
import { Check, ChevronDown, ChevronUp, Languages, Loader2 } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { useLanguageStore } from '@/store/language'
import { getLanguageByCode, normalizeLanguageCode } from '@/lib/target-languages'

export default function LanguageSwitcher() {
  const tLang = useTranslations('languages')
  const tTarget = useTranslations('targetLanguages')
  const targetLabel = (code: string, fallback?: string) => {
    const has = (tTarget as typeof tTarget & { has?: (key: string) => boolean }).has
    return typeof has === 'function' && has(code)
      ? tTarget(code)
      : fallback ?? getLanguageByCode(code)?.name ?? code
  }
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
    const canonicalCode = normalizeLanguageCode(code)
    if (canonicalCode === activeLanguage?.code) return
    const targetInfo = userLanguages.find((l) => l.target_language === canonicalCode)
    const ok = await switchLanguage(canonicalCode)
    if (ok) {
      const langName = targetLabel(code)
      setToastMsg(targetInfo?.plan?.cefr_level ? tLang('switched', { language: langName, level: targetInfo.plan.cefr_level }) : langName)
      setToast(true)
      setTimeout(() => setToast(false), 2500)
      router.refresh()
    }
  }

  const skeleton = useMemo(() => (
    <div className="flex items-center gap-2 rounded-[14px] border border-[rgba(7,7,9,.08)] bg-[#fff] px-3 py-2.5 shadow-[0_4px_14px_rgba(43,45,90,.06)] animate-pulse" aria-label="Loading languages">
      <div className="h-3 w-20 rounded bg-[rgba(7,7,9,.08)]" />
    </div>
  ), [])

  if (!activeLanguage) return skeleton
  const supportedUserLanguages = userLanguages.filter((ulang) => getLanguageByCode(ulang.target_language))
  const multiple = supportedUserLanguages.length > 1

  return (
    <div ref={ref} className="relative w-full">
      {toast && (
        <div className="pointer-events-none fixed inset-x-0 top-20 z-[100] flex justify-center px-4" role="status" aria-live="polite">
          <div className="pointer-events-auto flex items-center gap-2 rounded-[14px] border border-[rgba(7,7,9,.08)] bg-[#fff] px-4 py-3 text-xs font-bold text-[#202127] shadow-[0_8px_22px_rgba(43,45,90,.10)]">
            <Check className="h-4 w-4 text-[#5862e2]" aria-hidden="true" />
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
        aria-label={multiple ? 'Switch target language' : `Current target language: ${targetLabel(activeLanguage.code, getLanguageByCode(activeLanguage.code)?.name ?? activeLanguage.code)}`}
        className="group flex w-full items-center gap-3 rounded-[14px] border border-[rgba(7,7,9,.08)] bg-[#fff] px-3.5 py-2.5 text-left text-sm font-bold text-[#202127] shadow-[0_4px_14px_rgba(43,45,90,.06)] transition-all hover:-translate-y-0.5 hover:shadow-[0_6px_18px_rgba(43,45,90,.08)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#5862e2] focus-visible:ring-offset-2 disabled:cursor-default disabled:hover:translate-y-0 disabled:hover:shadow-[0_4px_14px_rgba(43,45,90,.06)]"
      >
        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-[10px] bg-[#ededff]">
          <Languages className="h-4 w-4 text-[#5862e2]" aria-hidden="true" />
        </span>
        <span className="min-w-0 flex-1 truncate">{isSwitching ? 'Switching…' : targetLabel(activeLanguage.code, getLanguageByCode(activeLanguage.code)?.name)}</span>
        {isSwitching ? (
          <Loader2 className="h-4 w-4 shrink-0 animate-spin text-[#5862e2]" aria-hidden="true" />
        ) : multiple && (open
          ? <ChevronUp className="h-4 w-4 shrink-0" aria-hidden="true" />
          : <ChevronDown className="h-4 w-4 shrink-0" aria-hidden="true" />)}
      </button>

      {open && multiple && (
        <div className="absolute left-0 right-0 top-[calc(100%+8px)] z-50 overflow-hidden rounded-[18px] border border-[rgba(7,7,9,.08)] bg-[#fff] p-1.5 shadow-[0_12px_30px_rgba(43,45,90,.10)]" role="listbox" aria-label="Available target languages">
          <div className="flex items-center gap-2 px-2.5 py-2 text-[10px] font-black uppercase tracking-[.12em] text-[rgba(32,33,39,.52)]">
            <Languages className="h-3.5 w-3.5" aria-hidden="true" />
            Your languages
          </div>
          {[...supportedUserLanguages].sort((a, b) => {
            const aLabel = targetLabel(a.target_language, getLanguageByCode(a.target_language)?.nameEn).toLowerCase()
            const bLabel = targetLabel(b.target_language, getLanguageByCode(b.target_language)?.nameEn).toLowerCase()
            return aLabel < bLabel ? -1 : aLabel > bLabel ? 1 : a.target_language < b.target_language ? -1 : a.target_language > b.target_language ? 1 : 0
          }).map((ulang) => {
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
                className={`flex w-full items-center gap-3 rounded-[12px] px-3 py-2.5 text-left text-sm font-bold transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#5862e2] focus-visible:ring-inset disabled:cursor-wait disabled:opacity-60 ${
                  ulang.is_active
                    ? 'bg-[#ededff] text-[#202127]'
                    : 'text-[#202127] hover:bg-[#ededff]'
                }`}
              >
                <Languages className="h-4 w-4 shrink-0 text-[#5862e2]" aria-hidden="true" />
                <span className="min-w-0 flex-1 truncate">{targetLabel(lang.code, lang.name)}</span>
                {ulang.plan?.cefr_level && (
                  <span className="rounded-full bg-[#fff3d1] px-2 py-0.5 text-[10px] font-black text-[#202127]">
                    {ulang.plan.cefr_level}
                  </span>
                )}
                {ulang.is_active && <Check className="h-4 w-4 text-[#5862e2]" aria-hidden="true" />}
              </button>
            )
          })}
        </div>
      )}
    </div>
  )
}
