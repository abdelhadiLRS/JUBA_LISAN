'use client'

import { useMemo, useState } from 'react'
import { ArrowRight, Globe2, MapPinned } from 'lucide-react'

type RegionId = 'americas' | 'europe' | 'africa-middle-east' | 'asia' | 'pacific'

type DisplayLanguage = {
  code: string
  name: string
  region: RegionId
  x: number
  y: number
}

const REGIONS: Array<{ id: RegionId; label: string; short: string }> = [
  { id: 'americas', label: 'Americas', short: 'AM' },
  { id: 'europe', label: 'Europe', short: 'EU' },
  { id: 'africa-middle-east', label: 'Africa & Middle East', short: 'AF' },
  { id: 'asia', label: 'Asia', short: 'AS' },
  { id: 'pacific', label: 'Pacific', short: 'PA' },
]

const DISPLAY_LANGUAGES: DisplayLanguage[] = [
  { code: 'en-US', name: 'English (US)', region: 'americas', x: 23, y: 38 },
  { code: 'en-GB', name: 'English (UK)', region: 'europe', x: 47, y: 29 },
  { code: 'fr', name: 'Français', region: 'europe', x: 48, y: 34 },
  { code: 'es', name: 'Español', region: 'europe', x: 45, y: 39 },
  { code: 'de', name: 'Deutsch', region: 'europe', x: 52, y: 33 },
  { code: 'it', name: 'Italiano', region: 'europe', x: 52, y: 39 },
  { code: 'pt', name: 'Português', region: 'europe', x: 43, y: 41 },
  { code: 'nl', name: 'Nederlands', region: 'europe', x: 49, y: 30 },
  { code: 'ru', name: 'Русский', region: 'europe', x: 61, y: 28 },
  { code: 'tr', name: 'Türkçe', region: 'africa-middle-east', x: 57, y: 43 },
  { code: 'el', name: 'Ελληνικά', region: 'europe', x: 55, y: 45 },
  { code: 'ro', name: 'Română', region: 'europe', x: 56, y: 38 },
  { code: 'hu', name: 'Magyar', region: 'europe', x: 54, y: 36 },
  { code: 'uk', name: 'Українська', region: 'europe', x: 57, y: 33 },
  { code: 'fi', name: 'Suomi', region: 'europe', x: 55, y: 22 },
  { code: 'sv', name: 'Svenska', region: 'europe', x: 52, y: 23 },
  { code: 'ar', name: 'العربية', region: 'africa-middle-east', x: 56, y: 55 },
  { code: 'he', name: 'עברית', region: 'africa-middle-east', x: 59, y: 52 },
  { code: 'yo', name: 'Yorùbá', region: 'africa-middle-east', x: 48, y: 67 },
  { code: 'xh', name: 'isiXhosa', region: 'africa-middle-east', x: 52, y: 84 },
  { code: 'mg', name: 'Malagasy', region: 'africa-middle-east', x: 60, y: 78 },
  { code: 'ny', name: 'Chichewa', region: 'africa-middle-east', x: 55, y: 75 },
  { code: 'vi', name: 'Tiếng Việt', region: 'asia', x: 73, y: 57 },
  { code: 'ja', name: '日本語', region: 'asia', x: 84, y: 45 },
  { code: 'ko', name: '한국어', region: 'asia', x: 81, y: 43 },
  { code: 'zh', name: '中文', region: 'asia', x: 76, y: 43 },
  { code: 'mi', name: 'Māori', region: 'pacific', x: 92, y: 78 },
  { code: 'sm', name: 'Gagana Sāmoa', region: 'pacific', x: 88, y: 70 },
  { code: 'to', name: 'Lea faka-Tonga', region: 'pacific', x: 90, y: 74 },
  { code: 'sq', name: 'Shqip', region: 'europe', x: 53, y: 43 },
  { code: 'eu', name: 'Euskara', region: 'europe', x: 46, y: 36 },
  { code: 'gl', name: 'Galego', region: 'europe', x: 44, y: 38 },
]

const REGION_POSITION: Record<RegionId, { left: string; top: string }> = {
  americas: { left: '18%', top: '52%' },
  europe: { left: '48%', top: '31%' },
  'africa-middle-east': { left: '48%', top: '60%' },
  asia: { left: '73%', top: '43%' },
  pacific: { left: '84%', top: '73%' },
}

function MapSilhouette() {
  return (
    <svg viewBox="0 0 1000 500" className="pointer-events-none absolute inset-0 h-full w-full" aria-hidden="true" preserveAspectRatio="none">
      <path d="M95 118c45-37 93-48 133-31l35 29 17 47-22 34-34 5-18 43-32 16-19-22-31 6-21-30-27-18 8-29-19-22z" className="fill-[var(--juba-app-green-soft)] stroke-[var(--juba-app-line)]" strokeWidth="3" />
      <path d="M238 257l42 16 32 35 15 51-20 56-35 38-31-12-9-42-25-36 13-44-18-34z" className="fill-[var(--juba-app-green-soft)] stroke-[var(--juba-app-line)]" strokeWidth="3" />
      <path d="M446 105l37-25 50 7 34 28 38 8 30 34-18 28-43-2-24 25-43-5-32-31-39-9-19-28z" className="fill-[var(--juba-app-green-soft)] stroke-[var(--juba-app-line)]" strokeWidth="3" />
      <path d="M492 211l52-12 44 25 26 48-14 45-38 27-15 63-38 26-29-26 9-58-25-42 16-45z" className="fill-[var(--juba-app-green-soft)] stroke-[var(--juba-app-line)]" strokeWidth="3" />
      <path d="M624 137l54-35 74 12 49 34 74 10 42 35-18 37-61-3-25 31-61-8-41-30-53 7-27-32z" className="fill-[var(--juba-app-green-soft)] stroke-[var(--juba-app-line)]" strokeWidth="3" />
      <path d="M812 331l55-10 45 24 20 37-35 29-52-10-35-29z" className="fill-[var(--juba-app-green-soft)] stroke-[var(--juba-app-line)]" strokeWidth="3" />
    </svg>
  )
}

export function LanguageBubbles() {
  const [activeRegion, setActiveRegion] = useState<RegionId | null>(null)
  const [activeLanguage, setActiveLanguage] = useState<string | null>(null)

  const languagesByRegion = useMemo(
    () =>
      Object.fromEntries(
        REGIONS.map((region) => [
          region.id,
          DISPLAY_LANGUAGES.filter((language) => language.region === region.id),
        ])
      ) as Record<RegionId, DisplayLanguage[]>,
    []
  )

  const visibleRegions = activeRegion
    ? REGIONS.filter((region) => region.id === activeRegion)
    : REGIONS

  return (
    <div className="relative overflow-hidden rounded-[36px] border-2 border-[var(--juba-app-ink)] bg-[var(--juba-app-surface)] p-3 shadow-[6px_6px_0_var(--juba-app-ink)] sm:p-5">
      <div className="relative min-h-[560px] overflow-hidden rounded-[28px] border border-[var(--juba-app-line)] bg-[#f5f8f1]">
        <MapSilhouette />

        <div className="absolute inset-x-4 top-4 z-20 flex flex-wrap items-center justify-between gap-3 sm:inset-x-6 sm:top-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--juba-app-ink)] bg-white/90 px-3 py-2 text-[10px] font-black uppercase tracking-[.16em] text-[var(--juba-app-ink)] backdrop-blur">
            <MapPinned className="h-3.5 w-3.5" aria-hidden="true" />
            Language atlas
          </div>
          <button type="button" onClick={() => { setActiveRegion(null); setActiveLanguage(null) }} className="rounded-full border border-[var(--juba-app-line)] bg-white/90 px-3 py-2 text-[10px] font-black uppercase tracking-[.12em] text-[var(--juba-app-muted)] transition hover:border-[var(--juba-app-ink)] hover:text-[var(--juba-app-ink)]">
            All regions
          </button>
        </div>

        <div className="absolute inset-0 z-10">
          <div className="absolute inset-0">
            {DISPLAY_LANGUAGES.filter((language) => !activeRegion || language.region === activeRegion).map((language) => {
              const isActive = activeLanguage === language.code
              return (
                <button
                  key={language.code}
                  type="button"
                  onClick={() => setActiveLanguage(isActive ? null : language.code)}
                  className="group absolute -translate-x-1/2 -translate-y-1/2"
                  style={{ left: language.x + '%', top: language.y + '%' }}
                  aria-label={language.name}
                  aria-pressed={isActive}
                >
                  <span className={[
                    'flex h-4 w-4 items-center justify-center rounded-full border-2 border-white shadow-[0_1px_5px_rgba(24,37,27,.2)] transition-all',
                    isActive ? 'h-5 w-5 bg-[var(--juba-app-yellow)] ring-2 ring-[var(--juba-app-ink)]' : 'bg-[var(--juba-app-green)] group-hover:scale-125',
                  ].join(' ')}>
                    <span className="h-1.5 w-1.5 rounded-full bg-white" aria-hidden="true" />
                  </span>
                  <span className={[
                    'pointer-events-none absolute left-1/2 top-full mt-1 -translate-x-1/2 whitespace-nowrap rounded-full border px-2 py-1 text-[9px] font-black shadow-sm transition-opacity',
                    isActive ? 'border-[var(--juba-app-ink)] bg-white text-[var(--juba-app-ink)] opacity-100' : 'border-[var(--juba-app-line)] bg-white/95 text-[var(--juba-app-muted)] opacity-0 group-hover:opacity-100',
                  ].join(' ')}>
                    {language.name}
                  </span>
                </button>
              )
            })}
          </div>
          {visibleRegions.map((region) => {
            const languages = languagesByRegion[region.id]
            const position = REGION_POSITION[region.id]
            const isActive = activeRegion === region.id

            return (
              <button
                type="button"
                key={region.id}
                onClick={() => { setActiveRegion(isActive ? null : region.id); setActiveLanguage(null) }}
                className="group absolute -translate-x-1/2 -translate-y-1/2 text-left"
                style={position}
                aria-pressed={isActive}
                aria-label={region.label + ': ' + languages.length + ' languages'}
              >
                <span className={[
                  'block w-[190px] rounded-[22px] border-2 p-3 shadow-[3px_3px_0_rgba(24,37,27,.12)] transition-all sm:w-[230px] sm:p-4',
                  isActive
                    ? 'border-[var(--juba-app-ink)] bg-[var(--juba-app-yellow)] shadow-[5px_5px_0_var(--juba-app-ink)]'
                    : 'border-[var(--juba-app-line)] bg-white/95 hover:-translate-y-1 hover:border-[var(--juba-app-ink)]',
                ].join(' ')}>
                  <span className="flex items-center justify-between gap-2">
                    <span>
                      <span className="block text-[9px] font-black uppercase tracking-[.18em] text-[var(--juba-app-green)]">{region.short}</span>
                      <span className="mt-1 block text-sm font-black text-[var(--juba-app-ink)] sm:text-base">{region.label}</span>
                    </span>
                    <ArrowRight className="h-4 w-4 shrink-0 text-[var(--juba-app-green)] transition-transform group-hover:translate-x-1" aria-hidden="true" />
                  </span>

                  <span className="mt-3 flex flex-wrap gap-1.5">
                    {languages.map((language) => (
                      <span key={language.code} className="rounded-full border border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] px-2 py-1 text-[10px] font-bold text-[var(--juba-app-ink)]">
                        {language.name}
                      </span>
                    ))}
                  </span>
                </span>
              </button>
            )
          })}
        </div>

        <div className="absolute bottom-4 left-1/2 z-20 w-[calc(100%-2rem)] -translate-x-1/2 sm:bottom-6 sm:w-auto">
          <div className="flex flex-wrap justify-center gap-1.5 rounded-2xl border border-[var(--juba-app-line)] bg-white/90 p-2 backdrop-blur">
            {REGIONS.map((region) => (
              <button type="button" key={region.id} onClick={() => { setActiveRegion(region.id); setActiveLanguage(null) }} className={[
                'rounded-xl px-3 py-2 text-[10px] font-black uppercase tracking-[.1em] transition',
                activeRegion === region.id
                  ? 'bg-[var(--juba-app-ink)] text-white'
                  : 'text-[var(--juba-app-muted)] hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-ink)]',
              ].join(' ')}>
                {region.short}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-4 flex flex-col gap-3 rounded-2xl border border-[var(--juba-app-line)] bg-[var(--juba-app-green-soft)] p-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <Globe2 className="mt-0.5 h-5 w-5 shrink-0 text-[var(--juba-app-green)]" aria-hidden="true" />
          <div>
            <p className="text-sm font-black text-[var(--juba-app-ink)]">Languages by region</p>
            <p className="mt-1 text-xs leading-5 text-[var(--juba-app-muted)]">Explore the JUBA LISAN language catalog geographically instead of as one long list.</p>
          </div>
        </div>
        <span className="text-xs font-black text-[var(--juba-app-green)]">{DISPLAY_LANGUAGES.length} languages</span>
      </div>

    </div>
  )
}
