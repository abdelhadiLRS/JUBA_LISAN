'use client'

import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { Check } from 'lucide-react'
import { TARGET_LANGUAGE_CATALOG } from '@/lib/target-languages'

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

  const filtered = TARGET_LANGUAGE_CATALOG.filter((lang) =>
    availableCodes.includes(lang.code)
  ).sort((a, b) => t(a.code).localeCompare(t(b.code)))

  return (
    <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3">
      {filtered.map((lang) => {
        const selected = value === lang.code
        return (
          <button
            key={lang.code}
            type="button"
            onClick={() => onChange(lang.code)}
            aria-pressed={selected}
            className={`group relative flex min-h-14 items-center gap-2.5 rounded-[14px] border-2 px-3 py-2.5 text-left text-xs font-black transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)] focus-visible:ring-offset-2 ${
              selected
                ? 'border-[var(--juba-app-ink)] bg-[var(--juba-app-yellow)] text-[var(--juba-app-ink)] shadow-[3px_3px_0_var(--juba-app-ink)] -translate-y-0.5'
                : 'border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] text-[var(--juba-app-muted)] hover:-translate-y-0.5 hover:border-[var(--juba-app-ink)] hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-ink)]'
            }`}
          >
            <Image
              src={lang.flagPath}
              alt=""
              width={22}
              height={16}
              className="shrink-0 rounded-sm object-cover ring-1 ring-black/10"
            />
            <span className="min-w-0 truncate">{t(lang.code)}</span>
            {selected && (
              <span className="ml-auto flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[var(--juba-app-ink)] text-white">
                <Check className="h-3 w-3" aria-hidden="true" />
              </span>
            )}
          </button>
        )
      })}
    </div>
  )
}
