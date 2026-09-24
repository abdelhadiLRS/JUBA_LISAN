'use client'

import { useEffect, useState, useRef, useMemo } from 'react'
import Image from 'next/image'
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
    function handleClick(e: MouseEvent) { if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false) }
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
    <div className="flex items-center gap-2 rounded-2xl border border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] px-4 py-2.5 shadow-[3px_3px_0_var(--juba-app-ink)] animate-pulse">
      <div className="h-3.5 w-5 rounded bg-[var(--juba-app-line)]" />
      <div className="h-3 w-20 rounded bg-[var(--juba-app-line)]" />
    </div>
  ), [])

  if (!activeLanguage) return skeleton
  const supportedUserLanguages = userLanguages.filter((ulang) => getLanguageByCode(ulang.target_language))
  const multiple = supportedUserLanguages.length > 1

  return (
    <div ref={ref} className="relative w-full">
      {toast && <div className="pointer-events-none fixed inset-x-0 top-20 z-[100] flex justify-center px-4"><div className="pointer-events-auto rounded-2xl border-2 border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] px-5 py-3 text-xs font-bold tracking-wide text-[var(--juba-app-ink)] shadow-[4px_4px_0_var(--juba-app-ink)]">{toastMsg}</div></div>}
      <button onClick={() => multiple && setOpen(!open)} disabled={!multiple} className="group flex w-full items-center gap-3 rounded-2xl border border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] px-4 py-2.5 text-left text-sm font-bold text-[var(--juba-app-ink)] shadow-[3px_3px_0_var(--juba-app-ink)] transition-all hover:-translate-y-0.5 hover:shadow-[4px_4px_0_var(--juba-app-ink)] disabled:cursor-default disabled:hover:translate-y-0 disabled:hover:shadow-[3px_3px_0_var(--juba-app-ink)]">
        <Image src={activeLanguage.flagPath} alt={activeLanguage.code} width={22} height={15} className="shrink-0 rounded-sm object-cover" />
        <span className="truncate">{isSwitching ? '...' : tTarget(activeLanguage.code)}</span>
        {multiple && <span className="ml-auto rounded-full bg-[var(--juba-app-green-soft)] px-2 py-0.5 text-xs text-[var(--juba-app-muted)]">{open ? '⌃' : '⌄'}</span>}
      </button>
      {open && multiple && <div className="absolute left-0 right-0 top-[calc(100%+8px)] z-50 overflow-hidden rounded-2xl border-2 border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] p-1.5 shadow-[5px_5px_0_var(--juba-app-ink)]">
        {[...supportedUserLanguages].sort((a, b) => tTarget(a.target_language).localeCompare(tTarget(b.target_language))).map((ulang) => {
          const lang = getLanguageByCode(ulang.target_language)
          if (!lang) return null
          return <button key={ulang.target_language} onClick={() => handleSwitch(ulang.target_language)} className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-bold transition-colors ${ulang.is_active ? 'bg-[var(--juba-app-green-soft)] text-[var(--juba-app-ink)]' : 'text-[var(--juba-app-ink)] hover:bg-[var(--juba-app-green-soft)]'}`}>
            <Image src={lang.flagPath} alt={lang.code} width={22} height={15} className="shrink-0 rounded-sm object-cover" />
            <span className="truncate">{tTarget(lang.code)}</span>
            {ulang.plan?.cefr_level && <span className="ml-1 rounded-full bg-[var(--juba-app-green-soft)] px-2 py-0.5 text-[11px] font-black text-[var(--juba-app-green-dark)]">{ulang.plan.cefr_level}</span>}
            {ulang.is_active && <span className="ml-auto font-black">✓</span>}
          </button>
        })}
      </div>}
    </div>
  )
}
