'use client'

import Image from 'next/image'
import { useTranslations } from 'next-intl'
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
    <div className="grid grid-cols-2 gap-2">
      {filtered.map((lang) => (
        <button
          key={lang.code}
          type="button"
          onClick={() => onChange(lang.code)}
          className={`flex items-center gap-2 rounded-xl border-2 px-3 py-3 text-xs font-bold tracking-wide uppercase transition-colors ${
            value === lang.code
              ? 'border-[var(--juba-primary-dark)] bg-[var(--juba-yellow)] text-[var(--juba-text)] shadow-[2px_2px_0_var(--juba-border)]'
              : 'border-[var(--juba-border)] bg-[var(--juba-surface)] text-[var(--juba-muted)] hover:border-[var(--juba-primary)] hover:text-[var(--juba-text)]'
          }`}
        >
          <Image
            src={lang.flagPath}
            alt={lang.code}
            width={20}
            height={16}
            className="object-cover"
          />
          {t(lang.code)}
        </button>
      ))}
    </div>
  )
}
