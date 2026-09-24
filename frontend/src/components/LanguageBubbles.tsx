'use client'

import { useMemo, useState } from 'react'
import { Globe2, MapPinned } from 'lucide-react'
import { WORLD_MAP_CENTROIDS, WORLD_MAP_PATHS } from './world-map-data'

type RegionId = 'americas' | 'europe' | 'africa-middle-east' | 'asia' | 'pacific'

type DisplayLanguage = {
  code: string
  name: string
  region: RegionId
  country: string
}

const REGIONS: Array<{ id: RegionId; label: string; short: string }> = [
  { id: 'americas', label: 'Americas', short: 'AM' },
  { id: 'europe', label: 'Europe', short: 'EU' },
  { id: 'africa-middle-east', label: 'Africa & Middle East', short: 'AF' },
  { id: 'asia', label: 'Asia', short: 'AS' },
  { id: 'pacific', label: 'Pacific', short: 'PA' },
]

const DISPLAY_LANGUAGES: DisplayLanguage[] = [
  { code: 'en-US', name: 'English (US)', region: 'americas', country: 'USA' },
  { code: 'en-GB', name: 'English (UK)', region: 'europe', country: 'GBR' },
  { code: 'fr', name: 'Français', region: 'europe', country: 'FRA' },
  { code: 'es', name: 'Español', region: 'europe', country: 'ESP' },
  { code: 'de', name: 'Deutsch', region: 'europe', country: 'DEU' },
  { code: 'it', name: 'Italiano', region: 'europe', country: 'ITA' },
  { code: 'pt', name: 'Português', region: 'europe', country: 'PRT' },
  { code: 'nl', name: 'Nederlands', region: 'europe', country: 'NLD' },
  { code: 'ru', name: 'Русский', region: 'europe', country: 'RUS' },
  { code: 'tr', name: 'Türkçe', region: 'africa-middle-east', country: 'TUR' },
  { code: 'el', name: 'Ελληνικά', region: 'europe', country: 'GRC' },
  { code: 'ro', name: 'Română', region: 'europe', country: 'ROU' },
  { code: 'hu', name: 'Magyar', region: 'europe', country: 'HUN' },
  { code: 'uk', name: 'Українська', region: 'europe', country: 'UKR' },
  { code: 'fi', name: 'Suomi', region: 'europe', country: 'FIN' },
  { code: 'sv', name: 'Svenska', region: 'europe', country: 'SWE' },
  { code: 'ar', name: 'العربية', region: 'africa-middle-east', country: 'SAU' },
  { code: 'he', name: 'עברית', region: 'africa-middle-east', country: 'ISR' },
  { code: 'yo', name: 'Yorùbá', region: 'africa-middle-east', country: 'NGA' },
  { code: 'xh', name: 'isiXhosa', region: 'africa-middle-east', country: 'ZAF' },
  { code: 'mg', name: 'Malagasy', region: 'africa-middle-east', country: 'MDG' },
  { code: 'ny', name: 'Chichewa', region: 'africa-middle-east', country: 'MWI' },
  { code: 'vi', name: 'Tiếng Việt', region: 'asia', country: 'VNM' },
  { code: 'ja', name: '日本語', region: 'asia', country: 'JPN' },
  { code: 'ko', name: '한국어', region: 'asia', country: 'KOR' },
  { code: 'zh', name: '中文', region: 'asia', country: 'CHN' },
  { code: 'mi', name: 'Māori', region: 'pacific', country: 'NZL' },
  { code: 'sm', name: 'Gagana Sāmoa', region: 'pacific', country: 'WSM' },
  { code: 'to', name: 'Lea faka-Tonga', region: 'pacific', country: 'TON' },
  { code: 'sq', name: 'Shqip', region: 'europe', country: 'ALB' },
  { code: 'eu', name: 'Euskara', region: 'europe', country: 'ESP' },
  { code: 'gl', name: 'Galego', region: 'europe', country: 'ESP' },
]

function WorldMap() {
  return (
    <svg
      viewBox="0 0 1000 507"
      className="pointer-events-none absolute inset-0 h-full w-full"
      aria-hidden="true"
      preserveAspectRatio="xMidYMid meet"
    >
      <defs>
        <pattern id="atlas-graticule" width="100" height="84.5" patternUnits="userSpaceOnUse">
          <path d="M100 0H0V84.5" fill="none" stroke="var(--juba-app-line)" strokeWidth="1" opacity=".32" />
        </pattern>
      </defs>

      <rect width="1000" height="507" fill="url(#atlas-graticule)" opacity=".42" />

      {Object.entries(WORLD_MAP_PATHS).map(([code, path]) => (
        <path
          key={code}
          d={path}
          fill="var(--juba-app-green-soft)"
          stroke="var(--juba-app-line)"
          strokeWidth="1.15"
          vectorEffect="non-scaling-stroke"
        />
      ))}
    </svg>
  )
}

export function LanguageBubbles() {
  const [activeRegion, setActiveRegion] = useState<RegionId | null>(null)
  const [activeLanguage, setActiveLanguage] = useState<string | null>(null)

  const visibleLanguages = useMemo(
    () => DISPLAY_LANGUAGES.filter((language) => !activeRegion || language.region === activeRegion),
    [activeRegion],
  )

  const selected = DISPLAY_LANGUAGES.find((language) => language.code === activeLanguage)
  const selectedRegion = selected ? REGIONS.find((region) => region.id === selected.region) : null

  const regionCountries = useMemo(() => {
    const map = new Map<RegionId, Set<string>>()
    for (const region of REGIONS) map.set(region.id, new Set())
    for (const language of DISPLAY_LANGUAGES) map.get(language.region)?.add(language.country)
    return map
  }, [])

  const selectedCountry = selected?.country ?? null

  return (
    <div className="relative overflow-hidden rounded-[36px] border-2 border-[var(--juba-app-ink)] bg-[var(--juba-app-surface)] p-3 shadow-[6px_6px_0_var(--juba-app-ink)] sm:p-5">
      <div className="relative min-h-[430px] overflow-hidden rounded-[28px] border border-[var(--juba-app-line)] bg-[#f5f8f1] sm:min-h-[560px]">
        <WorldMap />

        <div className="absolute inset-x-4 top-4 z-20 flex flex-wrap items-center justify-between gap-3 sm:inset-x-6 sm:top-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--juba-app-ink)] bg-white/95 px-3 py-2 text-[10px] font-black uppercase tracking-[.16em] text-[var(--juba-app-ink)] shadow-sm">
            <MapPinned className="h-3.5 w-3.5" aria-hidden="true" />
            Language atlas
          </div>

          <span className="hidden rounded-full border border-[var(--juba-app-line)] bg-white/95 px-3 py-2 text-[10px] font-bold text-[var(--juba-app-muted)] shadow-sm sm:inline">
            221 countries · {DISPLAY_LANGUAGES.length} learning languages
          </span>

          <button
            type="button"
            onClick={() => {
              setActiveRegion(null)
              setActiveLanguage(null)
            }}
            className="rounded-full border border-[var(--juba-app-line)] bg-white/95 px-3 py-2 text-[10px] font-black uppercase tracking-[.12em] text-[var(--juba-app-muted)] transition hover:border-[var(--juba-app-ink)] hover:text-[var(--juba-app-ink)]"
          >
            All regions
          </button>
        </div>

        <div className="absolute inset-0 z-10">
          <svg viewBox="0 0 1000 507" className="pointer-events-none absolute inset-0 h-full w-full" aria-hidden="true" preserveAspectRatio="xMidYMid meet">
            {Object.entries(WORLD_MAP_PATHS).map(([code, path]) => {
              const isSelected = selectedCountry === code
              const isRegionCountry = activeRegion ? regionCountries.get(activeRegion)?.has(code) : false

              return (
                <path
                  key={code}
                  d={path}
                  fill={isSelected ? 'var(--juba-app-yellow)' : isRegionCountry ? 'var(--juba-app-green)' : 'transparent'}
                  fillOpacity={isSelected ? '.75' : isRegionCountry ? '.12' : '0'}
                  stroke="none"
                />
              )
            })}
          </svg>

          {visibleLanguages.map((language) => {
            const point = WORLD_MAP_CENTROIDS[language.country]
            if (!point) return null

            const isActive = activeLanguage === language.code
            const left = (point.x / 1000) * 100
            const top = (point.y / 507) * 100

            return (
              <button
                key={language.code}
                type="button"
                onClick={() => setActiveLanguage(isActive ? null : language.code)}
                className="group absolute -translate-x-1/2 -translate-y-1/2"
                style={{ left: `${left}%`, top: `${top}%` }}
                aria-label={language.name}
                aria-pressed={isActive}
              >
                <span
                  className={[
                    'relative flex h-5 w-5 items-center justify-center rounded-full border-2 border-white bg-[var(--juba-app-green)] shadow-[0_2px_7px_rgba(24,37,27,.24)] transition-all duration-200',
                    isActive ? 'scale-125 bg-[var(--juba-app-yellow)] ring-2 ring-[var(--juba-app-ink)]' : 'group-hover:scale-125',
                  ].join(' ')}
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-white" aria-hidden="true" />
                </span>
                <span
                  className={[
                    'pointer-events-none absolute left-1/2 top-full mt-1 -translate-x-1/2 whitespace-nowrap rounded-md border px-2 py-1 text-[9px] font-black shadow-sm transition-opacity',
                    isActive
                      ? 'border-[var(--juba-app-ink)] bg-white text-[var(--juba-app-ink)] opacity-100'
                      : 'border-[var(--juba-app-line)] bg-white/95 text-[var(--juba-app-muted)] opacity-0 group-hover:opacity-100',
                  ].join(' ')}
                >
                  {language.name}
                </span>
              </button>
            )
          })}

          {selected && selectedRegion && (
            <div className="absolute bottom-20 left-3 z-20 max-w-[calc(100%-1.5rem)] rounded-2xl border-2 border-[var(--juba-app-ink)] bg-white p-4 shadow-[4px_4px_0_var(--juba-app-ink)] sm:bottom-24 sm:left-6 sm:max-w-[280px]">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <span className="text-[9px] font-black uppercase tracking-[.18em] text-[var(--juba-app-green)]">{selectedRegion.label}</span>
                  <h3 className="mt-1 text-lg font-black text-[var(--juba-app-ink)]">{selected.name}</h3>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveLanguage(null)}
                  className="text-xs font-black text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)]"
                  aria-label="Close language details"
                >
                  ×
                </button>
              </div>
              <p className="mt-2 text-xs leading-5 text-[var(--juba-app-muted)]">Explore this language in the JUBA LISAN learning experience.</p>
            </div>
          )}

          <div className="absolute bottom-3 left-1/2 z-20 w-[calc(100%-1.25rem)] -translate-x-1/2 sm:bottom-6 sm:w-auto">
            <div className="flex flex-wrap justify-center gap-1.5 rounded-2xl border border-[var(--juba-app-line)] bg-white/95 p-2 shadow-sm">
              {REGIONS.map((region) => (
                <button
                  type="button"
                  key={region.id}
                  onClick={() => {
                    setActiveRegion(region.id)
                    setActiveLanguage(null)
                  }}
                  className={[
                    'rounded-xl px-3 py-2 text-[10px] font-black uppercase tracking-[.1em] transition',
                    activeRegion === region.id
                      ? 'bg-[var(--juba-app-ink)] text-white'
                      : 'text-[var(--juba-app-muted)] hover:bg-[var(--juba-app-green-soft)] hover:text-[var(--juba-app-ink)]',
                  ].join(' ')}
                >
                  {region.short}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="mt-4 flex flex-col gap-3 rounded-2xl border border-[var(--juba-app-line)] bg-[var(--juba-app-green-soft)] p-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <Globe2 className="mt-0.5 h-5 w-5 shrink-0 text-[var(--juba-app-green)]" aria-hidden="true" />
          <div>
            <p className="text-sm font-black text-[var(--juba-app-ink)]">Languages by region</p>
            <p className="mt-1 text-xs leading-5 text-[var(--juba-app-muted)]">A real country-level atlas connects each learning language to its geographic home.</p>
          </div>
        </div>
        <span className="text-xs font-black text-[var(--juba-app-green)]">{DISPLAY_LANGUAGES.length} languages</span>
      </div>
    </div>
  )
}
