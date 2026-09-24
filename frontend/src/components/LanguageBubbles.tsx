'use client'

import { useMemo } from 'react'
import Image from 'next/image'

type DisplayLanguage = {
  code: string
  name: string
  flag?: string
  flagPath?: string
}

const DISPLAY_LANGUAGES: DisplayLanguage[] = [
  { code: 'en-US', name: 'English (US)', flag: '🇺🇸' },
  { code: 'en-GB', name: 'English (UK)', flag: '🇬🇧' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  { code: 'it', name: 'Italiano', flag: '🇮🇹' },
  { code: 'pt', name: 'Português', flag: '🇵🇹' },
  { code: 'nl', name: 'Nederlands', flag: '🇳🇱' },
  { code: 'ru', name: 'Русский', flag: '🇷🇺' },
  { code: 'tr', name: 'Türkçe', flag: '🇹🇷' },
  { code: 'el', name: 'Ελληνικά', flag: '🇬🇷' },
  { code: 'ro', name: 'Română', flag: '🇷🇴' },
  { code: 'hu', name: 'Magyar', flag: '🇭🇺' },
  { code: 'uk', name: 'Українська', flag: '🇺🇦' },
  { code: 'fi', name: 'Suomi', flag: '🇫🇮' },
  { code: 'sv', name: 'Svenska', flag: '🇸🇪' },
  { code: 'vi', name: 'Tiếng Việt', flag: '🇻🇳' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' },
  { code: 'ko', name: '한국어', flag: '🇰🇷' },
  { code: 'zh', name: '中文', flag: '🇨🇳' },
  { code: 'ar', name: 'العربية', flagPath: '/flags/arab-league.svg' },
  { code: 'he', name: 'עברית', flagPath: '/flags/hebrew-star.svg' },
  { code: 'mi', name: 'Māori', flag: '🇳🇿' },
  { code: 'sm', name: 'Gagana Sāmoa', flag: '🇼🇸' },
  { code: 'to', name: 'Lea faka-Tonga', flag: '🇹🇴' },
  { code: 'sq', name: 'Shqip', flag: '🇦🇱' },
  { code: 'eu', name: 'Euskara', flag: '🇪🇺' },
  { code: 'gl', name: 'Galego', flag: '🇪🇸' },
  { code: 'yo', name: 'Yorùbá', flag: '🇳🇬' },
  { code: 'xh', name: 'isiXhosa', flag: '🇿🇦' },
  { code: 'mg', name: 'Malagasy', flag: '🇲🇬' },
  { code: 'ny', name: 'Chichewa', flag: '🇲🇼' },
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
                {lang.flagPath ? (
                  <Image
                    src={lang.flagPath}
                    alt=""
                    width={16}
                    height={11}
                    className="h-[11px] w-[16px] rounded-[2px] object-cover ring-1 ring-black/10"
                  />
                ) : (
                  <span className="text-[14px] leading-none" aria-hidden="true">{lang.flag}</span>
                )}
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
