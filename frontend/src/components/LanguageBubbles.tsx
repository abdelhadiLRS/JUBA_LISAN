'use client'

import { useMemo } from 'react'
import Image from 'next/image'

type DisplayLanguage = {
  code: string
  name: string
}

const DISPLAY_LANGUAGES: DisplayLanguage[] = [
  { code: 'en-US', name: 'English (US)' },
  { code: 'en-GB', name: 'English (UK)' },
  { code: 'fr', name: 'Français' },
  { code: 'es', name: 'Español' },
  { code: 'de', name: 'Deutsch' },
  { code: 'it', name: 'Italiano' },
  { code: 'pt', name: 'Português' },
  { code: 'nl', name: 'Nederlands' },
  { code: 'ru', name: 'Русский' },
  { code: 'tr', name: 'Türkçe' },
  { code: 'el', name: 'Ελληνικά' },
  { code: 'ro', name: 'Română' },
  { code: 'hu', name: 'Magyar' },
  { code: 'uk', name: 'Українська' },
  { code: 'fi', name: 'Suomi' },
  { code: 'sv', name: 'Svenska' },
  { code: 'vi', name: 'Tiếng Việt' },
  { code: 'ja', name: '日本語' },
  { code: 'ko', name: '한국어' },
  { code: 'zh', name: '中文' },
  { code: 'ar', name: 'العربية' },
  { code: 'he', name: 'עברית' },
  { code: 'mi', name: 'Māori' },
  { code: 'sm', name: 'Gagana Sāmoa' },
  { code: 'to', name: 'Lea faka-Tonga' },
  { code: 'sq', name: 'Shqip' },
  { code: 'eu', name: 'Euskara' },
  { code: 'gl', name: 'Galego' },
  { code: 'yo', name: 'Yorùbá' },
  { code: 'xh', name: 'isiXhosa' },
  { code: 'mg', name: 'Malagasy' },
  { code: 'ny', name: 'Chichewa' },
]

function circlePosition(index: number, total: number, radius: number) {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2
  const x = Math.cos(angle) * radius
  const y = Math.sin(angle) * radius
  // Round coordinates so SSR and browser serialization produce identical style strings.
  return { x: Math.round(x * 100) / 100, y: Math.round(y * 100) / 100 }
}

export function LanguageBubbles() {
  const positions = useMemo(
    () => DISPLAY_LANGUAGES.map((_, i) => circlePosition(i, DISPLAY_LANGUAGES.length, 155)),
    []
  )

  return (
    <div className="relative h-[360px] w-full sm:h-[380px]" aria-label="JUBA LISAN supported languages">
      <div
        className="absolute left-1/2 top-1/2 z-[1] flex h-[140px] w-[140px] -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full border-2 border-[var(--juba-app-ink)] bg-[var(--juba-app-yellow)] p-5 shadow-[5px_5px_0_var(--juba-app-ink)]"
        aria-label="JUBA LISAN"
      >
        <Image
          src="/logo.png"
          alt="JUBA LISAN"
          width={96}
          height={96}
          className="h-auto w-auto object-contain"
        />
      </div>

      {DISPLAY_LANGUAGES.map((lang, i) => {
        const { x, y } = positions[i]
        const greeting = lang.name
        const delay = i * 0.35
        return (
          <div
            key={lang.code}
            className="absolute z-0 w-max"
            style={{
              left: `calc(50% + ${x}px)`,
              top: `calc(50% + ${y}px)`,
              transform: 'translate(-50%, -50%)',
            }}
          >
            <div
              className="animate-float animate-bubble-in w-max"
              style={{
                animationDelay: `${delay}s, ${delay}s`,
                animationDuration: '3.4s, 0.4s',
              }}
            >
              <div className="flex items-center gap-1.5 rounded-full border border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] px-2.5 py-1 shadow-[2px_2px_0_rgba(24,37,27,.08)] transition-all hover:-translate-y-0.5 hover:shadow-[3px_3px_0_rgba(24,37,27,.12)]">
                <span className="whitespace-nowrap text-[11px] font-bold text-[var(--juba-app-ink)]">
                  {greeting}
                </span>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
