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
    <div className="grid grid-cols-1 gap-2.5 min-[420px]:grid-cols-2 sm:grid-cols-3">
      {filtered.map((lang) => {
        const selected = normalizeLanguageCode(value) === lang.code
        return (
          <button
            key={lang.code}
            type="button"
            onClick={() => onChange(lang.code)}
            aria-pressed={selected}
            className={`group relative flex min-h-16 items-center gap-3 rounded-[13px] border px-3 py-3 text-start text-sm font-extrabold transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--duo-blue)] focus-visible:ring-offset-2 ${
              selected
                ? 'border-[var(--duo-green)] bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] text-[var(--duo-ink)] shadow-sm -translate-y-0.5'
                : 'border-[var(--duo-line)] bg-[var(--duo-card)] text-[var(--duo-ink)] hover:-translate-y-0.5 hover:border-[var(--duo-green)] hover:bg-[color-mix(in_srgb,var(--duo-green)_8%,transparent)]'
            }`}
          >
            <Image src={lang.flagPath} alt="" aria-hidden="true" width={34} height={24} unoptimized className="h-6 w-[34px] shrink-0 rounded-md border border-[var(--duo-line)] object-cover shadow-sm" />
            <span lang={lang.iso639} dir="auto" className="min-w-0 flex-1 truncate">{label(lang.code, lang.name)}</span>
            {selected && (
              <span className="ms-auto flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[var(--duo-green-dark)] text-white">
                <Check className="h-3 w-3" aria-hidden="true" />
              </span>
            )}
          </button>
        )
      })}
    </div>
  )
}
