'use client'

import Image from 'next/image'
import { Globe2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import type { Locale } from '@/lib/locales'

const LANGUAGE_COUNTRY: Record<string, string> = {
  ar: 'dz', en: 'gb', fr: 'fr', es: 'es', pt: 'pt', de: 'de', it: 'it',
  pl: 'pl', nl: 'nl', ro: 'ro', ru: 'ru', ja: 'jp', ko: 'kr', tr: 'tr',
  zh: 'cn', he: 'il', hi: 'in', bn: 'bd', id: 'id', ms: 'my', th: 'th',
}

const TIMEZONE_COUNTRY: Record<string, string> = {
  'Africa/Algiers': 'dz', 'Europe/Paris': 'fr', 'Europe/London': 'gb',
  'Europe/Madrid': 'es', 'Europe/Lisbon': 'pt', 'Europe/Berlin': 'de',
  'Europe/Rome': 'it', 'Europe/Warsaw': 'pl', 'Europe/Amsterdam': 'nl',
  'Europe/Bucharest': 'ro', 'Europe/Moscow': 'ru', 'Asia/Tokyo': 'jp',
  'Asia/Seoul': 'kr', 'Asia/Shanghai': 'cn',
}

function countryFromBrowser(fallback: string) {
  try {
    const language = navigator.language || ''
    const region = language.match(/[-_]([A-Za-z]{2}|\d{3})$/)?.[1]
    if (region && /^[A-Za-z]{2}$/.test(region)) return region.toLowerCase()
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone
    return TIMEZONE_COUNTRY[timezone] ?? fallback
  } catch {
    return fallback
  }
}

export function VisitorLocaleBadge({ locale }: { locale: Locale }) {
  const fallback = LANGUAGE_COUNTRY[locale] ?? 'dz'
  const [country, setCountry] = useState(fallback)
  const [language, setLanguage] = useState(locale.toUpperCase())

  useEffect(() => {
    setCountry(countryFromBrowser(fallback))
    setLanguage((navigator.language || locale).split(/[-_]/)[0].toUpperCase())
  }, [fallback, locale])

  return (
    <div className="juba-busuu-visitor-locale" title="Your region and language">
      <span className="juba-busuu-visitor-flag" aria-hidden="true">
        <Image
          src={`https://flagcdn.com/w80/${country}.png`}
          alt=""
          width={80}
          height={60}
          unoptimized
        />
      </span>
      <span className="juba-busuu-visitor-code">{language}</span>
      <Globe2 aria-hidden="true" />
    </div>
  )
}
