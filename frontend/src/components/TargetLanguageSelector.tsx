'use client'

import { useTranslations } from 'next-intl'
import Image from 'next/image'
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
            className={`group relative flex min-h-16 items-center gap-3 rounded-[16px] border px-3 py-3 text-left text-sm font-extrabold transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#5862e2] focus-visible:ring-offset-2 ${
              selected
                ? 'border-[#635bff] bg-[#eeedff] text-[#202127] shadow-[0_6px_18px_rgba(43,45,90,.08)] -translate-y-0.5'
                : 'border-[#e6e7ef] bg-[#fff] text-[#202127] hover:-translate-y-0.5 hover:border-[#c9c7ff] hover:bg-[#f8f7ff]'
            }`}
          >
            <Image src={lang.flagPath} alt="" aria-hidden="true" width={34} height={24} unoptimized className="h-6 w-[34px] shrink-0 rounded-md border border-black/10 object-cover shadow-sm" />
            <span lang={lang.iso639} dir="auto" className="min-w-0 flex-1 truncate">{label(lang.code, lang.name)}</span>
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
