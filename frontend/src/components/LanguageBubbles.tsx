'use client'

import { useMemo } from 'react'
import { useTranslations } from 'next-intl'
import Image from 'next/image'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

function circlePosition(index: number, total: number, radius: number) {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2
  const x = Math.cos(angle) * radius
  const y = Math.sin(angle) * radius
  return { x, y }
}

export function LanguageBubbles() {
  const t = useTranslations('landing')
  const positions = useMemo(
    () =>
      SUPPORTED_TARGET_LANGUAGES.map((_, i) =>
        circlePosition(i, SUPPORTED_TARGET_LANGUAGES.length, 135)
      ),
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

      {SUPPORTED_TARGET_LANGUAGES.map((lang, i) => {
        const { x, y } = positions[i]
        const greeting = t(`languageGreetings.${lang.code}`) ?? lang.name
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
                <Image
                  src={lang.flagPath}
                  alt=""
                  width={14}
                  height={10}
                  className="rounded-[2px] object-cover ring-1 ring-black/10"
                />
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
