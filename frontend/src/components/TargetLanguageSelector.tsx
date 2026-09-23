'use client'

import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { Check, Sparkles } from 'lucide-react'
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
    <div className="grid gap-3 sm:grid-cols-2">
      {filtered.map((lang) => {
        const selected = value === lang.code

        return (
          <button
            key={lang.code}
            type="button"
            onClick={() => onChange(lang.code)}
            aria-pressed={selected}
            className={`group relative flex min-h-20 items-center gap-3 rounded-2xl border p-4 text-left transition-all ${
              selected
                ? 'border-[var(--juba-primary)] bg-[var(--juba-primary-soft)] shadow-[0_8px_25px_rgba(15,23,42,0.08)]'
                : 'border-fl-border bg-fl-surface hover:-translate-y-0.5 hover:border-[var(--juba-primary)]/40 hover:shadow-sm'
            }`}
          >
            <span className="flex h-10 w-12 shrink-0 items-center justify-center overflow-hidden rounded-xl bg-fl-surface-2 shadow-sm">
              <Image
                src={lang.flagPath}
                alt=""
                width={28}
                height={20}
                className="object-cover"
              />
            </span>
            <span className="min-w-0 flex-1">
              <span className="block text-sm font-black text-fl-fg">{t(lang.code)}</span>
              <span className="mt-0.5 block truncate text-xs text-fl-muted-2">
                {t(`${lang.code}-description`)}
              </span>
            </span>
            {selected ? (
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[var(--juba-primary)] text-white">
                <Check className="h-4 w-4" />
              </span>
            ) : (
              <Sparkles className="h-4 w-4 shrink-0 text-fl-muted-3 opacity-0 transition-opacity group-hover:opacity-100" />
            )}
          </button>
        )
      })}
    </div>
  )
}
