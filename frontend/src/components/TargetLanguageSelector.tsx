'use client'

import { useTranslations } from 'next-intl'
import { Check } from 'lucide-react'
import { TARGET_LANGUAGE_CATALOG, normalizeLanguageCode } from '@/lib/target-languages'

interface Props {
  value: string
  onChange: (code: string) => void
  availableCodes: string[]
}

export default function TargetLanguageSelector({
  value,
  onChange,
  availableCodes,
}: Props) {
  const t = useTranslations('targetLanguages')
  const label = (code: string, fallback: string) => {
    const has = (t as typeof t & { has?: (key: string) => boolean }).has
    return typeof has === 'function' && has(code) ? t(code) : fallback
  }

  const availableCodeSet = new Set(
    availableCodes
      .map((code) => code.trim().toUpperCase())
      .filter(Boolean)
  )

  const filtered = TARGET_LANGUAGE_CATALOG.filter((lang) =>
    availableCodeSet.has(lang.code.toUpperCase())
  ).sort((a, b) => {
    const aLabel = label(a.code, a.nameEn).toLowerCase()
    const bLabel = label(b.code, b.nameEn).toLowerCase()
    return aLabel < bLabel ? -1 : aLabel > bLabel ? 1 : a.code < b.code ? -1 : a.code > b.code ? 1 : 0
  })

  return (
    <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3">
      {filtered.map((lang) => {
        const selected = normalizeLanguageCode(value) === lang.code
        return (
          <button
            key={lang.code}
            type="button"
            onClick={() => onChange(lang.code)}
            aria-pressed={selected}
            className={`group relative flex min-h-14 items-center gap-2.5 rounded-[14px] border-2 px-3 py-2.5 text-left text-xs font-black transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#5862e2] focus-visible:ring-offset-2 ${
              selected
                ? 'border-[#202127] bg-[#fff3d1] text-[#202127] shadow-[0_6px_18px_rgba(43,45,90,.08)] -translate-y-0.5'
                : 'border-[rgba(7,7,9,.08)] bg-[#fff] text-[rgba(32,33,39,.52)] hover:-translate-y-0.5 hover:border-[#5862e2] hover:bg-[#ededff] hover:text-[#202127]'
            }`}
          >
            <span className="min-w-0 truncate">{label(lang.code, lang.name)}</span>
            {selected && (
              <span className="ml-auto flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#202127] text-white">
                <Check className="h-3 w-3" aria-hidden="true" />
              </span>
            )}
          </button>
        )
      })}
    </div>
  )
}
