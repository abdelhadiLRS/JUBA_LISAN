'use client'

import { useMemo, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import { Globe2, MapPinned } from 'lucide-react'
import { WORLD_MAP_CENTROIDS, WORLD_MAP_PATHS } from './world-map-data'
import { COUNTRY_NAMES } from './country-names'

type RegionId = 'americas' | 'europe' | 'africa-middle-east' | 'asia' | 'pacific'

type DisplayLanguage = {
  code: string
  name: string
  regions: RegionId[]
  countries: string[]
  markerCountry: string
}

const REGIONS: Array<{ id: RegionId; key: string; short: string }> = [
  { id: 'americas', key: 'regionAmericas', short: 'AM' },
  { id: 'europe', key: 'regionEurope', short: 'EU' },
  { id: 'africa-middle-east', key: 'regionAfricaMiddleEast', short: 'AF' },
  { id: 'asia', key: 'regionAsia', short: 'AS' },
  { id: 'pacific', key: 'regionPacific', short: 'PA' },
]

// Coverage uses established native, official, or major regional use.
// Diaspora communities are not plotted as separate territories.
const DISPLAY_LANGUAGES: DisplayLanguage[] = [
  { code: 'en', name: 'English', regions: ['americas','europe','africa-middle-east','asia','pacific'], markerCountry: 'USA', countries: ['USA','CAN','GBR','IRL','AUS','NZL','ZAF','NAM','BWA','ZMB','ZWE','UGA','KEN','TZA','NGA','GHA','SLE','LBR','GMB','GUY','JAM','TTO','BHS','BRB','BLZ','GRD','DMA','ATG','KNA','LCA','VCT','SGP','IND','PHL','PAK','FJI','WSM','TON','PNG','SLB','VUT','MLT','CYP'] },
  { code: 'fr', name: 'Français', regions: ['americas','europe','africa-middle-east','pacific'], markerCountry: 'FRA', countries: ['FRA','BEL','CHE','LUX','MCO','CAN','HTI','USA','MAR','DZA','TUN','MRT','SEN','MLI','NER','BFA','CIV','GHA','TGO','BEN','GIN','GNB','SLE','LBR','CMR','CAF','TCD','GAB','COG','COD','RWA','BDI','DJI','COM','MDG','MUS','SYC','VUT','NCL','PYF'] },
  { code: 'es', name: 'Español', regions: ['americas','europe','africa-middle-east'], markerCountry: 'ESP', countries: ['ESP','MEX','GTM','BLZ','HND','SLV','NIC','CRI','PAN','CUB','DOM','PRI','COL','VEN','ECU','PER','BOL','PRY','CHL','ARG','URY','GNQ','USA'] },
  { code: 'de', name: 'Deutsch', regions: ['europe'], markerCountry: 'DEU', countries: ['DEU','AUT','CHE','LIE','LUX','BEL','ITA','POL','CZE','HUN','ROU','NAM'] },
  { code: 'it', name: 'Italiano', regions: ['europe','africa-middle-east'], markerCountry: 'ITA', countries: ['ITA','SMR','CHE','VAT','SLO','HRV','LUX','MCO','ALB','MDA','MNE','ERI','SOM','LBY'] },
  { code: 'pt', name: 'Português', regions: ['americas','europe','africa-middle-east','asia'], markerCountry: 'PRT', countries: ['PRT','BRA','AGO','MOZ','GNB','CPV','STP','TLS','GNQ','MAC','LUX'] },
  { code: 'nl', name: 'Nederlands', regions: ['europe','americas','africa-middle-east','asia'], markerCountry: 'NLD', countries: ['NLD','BEL','SUR','ABW','CUW','SXM','BES','IDN','ZAF'] },
  { code: 'ru', name: 'Русский', regions: ['europe','asia'], markerCountry: 'RUS', countries: ['RUS','BLR','KAZ','KGZ','TJK','TKM','UZB','UKR','MDA','LVA','EST','LTU','GEO','ARM','AZE','MNG','ISR'] },
  { code: 'tr', name: 'Türkçe', regions: ['europe','asia'], markerCountry: 'TUR', countries: ['TUR','CYP'] },
  { code: 'el', name: 'Ελληνικά', regions: ['europe'], markerCountry: 'GRC', countries: ['GRC','CYP'] },
  { code: 'ro', name: 'Română', regions: ['europe'], markerCountry: 'ROU', countries: ['ROU','MDA','UKR','HUN','SRB'] },
  { code: 'hu', name: 'Magyar', regions: ['europe'], markerCountry: 'HUN', countries: ['HUN','ROU','SVK','SRB','UKR','HRV','AUT','SLO'] },
  { code: 'uk', name: 'Українська', regions: ['europe'], markerCountry: 'UKR', countries: ['UKR','POL','SVK','HUN','ROU','MDA'] },
  { code: 'fi', name: 'Suomi', regions: ['europe'], markerCountry: 'FIN', countries: ['FIN','SWE','EST'] },
  { code: 'sv', name: 'Svenska', regions: ['europe'], markerCountry: 'SWE', countries: ['SWE','FIN'] },
  { code: 'ar', name: 'العربية', regions: ['africa-middle-east','asia'], markerCountry: 'SAU', countries: ['SAU','ARE','QAT','KWT','BHR','OMN','YEM','IRQ','JOR','SYR','LBN','PSE','EGY','LBY','TUN','DZA','MAR','MRT','SDN','SOM','DJI','COM','TCD'] },
  { code: 'he', name: 'עברית', regions: ['africa-middle-east','asia'], markerCountry: 'ISR', countries: ['ISR'] },
  { code: 'yo', name: 'Yorùbá', regions: ['africa-middle-east'], markerCountry: 'NGA', countries: ['NGA','BEN','TGO'] },
  { code: 'xh', name: 'isiXhosa', regions: ['africa-middle-east'], markerCountry: 'ZAF', countries: ['ZAF','LSO'] },
  { code: 'mg', name: 'Malagasy', regions: ['africa-middle-east'], markerCountry: 'MDG', countries: ['MDG','COM','REU'] },
  { code: 'ny', name: 'Chichewa', regions: ['africa-middle-east'], markerCountry: 'MWI', countries: ['MWI','ZMB','MOZ','ZWE'] },
  { code: 'vi', name: 'Tiếng Việt', regions: ['asia'], markerCountry: 'VNM', countries: ['VNM'] },
  { code: 'ja', name: '日本語', regions: ['asia'], markerCountry: 'JPN', countries: ['JPN'] },
  { code: 'ko', name: '한국어', regions: ['asia'], markerCountry: 'KOR', countries: ['KOR','PRK'] },
  { code: 'zh', name: '中文', regions: ['asia'], markerCountry: 'CHN', countries: ['CHN','TWN','SGP'] },
  { code: 'mi', name: 'Māori', regions: ['pacific'], markerCountry: 'NZL', countries: ['NZL'] },
  { code: 'sm', name: 'Gagana Sāmoa', regions: ['pacific'], markerCountry: 'WSM', countries: ['WSM','ASM'] },
  { code: 'to', name: 'Lea faka-Tonga', regions: ['pacific'], markerCountry: 'TON', countries: ['TON'] },
  { code: 'sq', name: 'Shqip', regions: ['europe'], markerCountry: 'ALB', countries: ['ALB','XKX','MKD','MNE','SRB'] },
  { code: 'eu', name: 'Euskara', regions: ['europe'], markerCountry: 'ESP', countries: ['ESP','FRA'] },
  { code: 'gl', name: 'Galego', regions: ['europe'], markerCountry: 'ESP', countries: ['ESP'] },
  { code: 'no', name: 'Norsk', regions: ['europe'], markerCountry: 'NOR', countries: ['NOR'] },
  { code: 'da', name: 'Dansk', regions: ['europe'], markerCountry: 'DNK', countries: ['DNK'] },
  { code: 'pl', name: 'Polski', regions: ['europe'], markerCountry: 'POL', countries: ['POL','LTU','BLR','UKR','CZE','SVK'] },
  { code: 'cs', name: 'Čeština', regions: ['europe'], markerCountry: 'CZE', countries: ['CZE','SVK'] },
  { code: 'sk', name: 'Slovenčina', regions: ['europe'], markerCountry: 'SVK', countries: ['SVK','CZE'] },
  { code: 'fa', name: 'فارسی', regions: ['asia','africa-middle-east'], markerCountry: 'IRN', countries: ['IRN','AFG','TJK'] },
  { code: 'hi', name: 'हिन्दी', regions: ['asia'], markerCountry: 'IND', countries: ['IND','FJI'] },
  { code: 'bn', name: 'বাংলা', regions: ['asia'], markerCountry: 'BGD', countries: ['BGD','IND'] },
  { code: 'id', name: 'Bahasa Indonesia', regions: ['asia'], markerCountry: 'IDN', countries: ['IDN'] },
  { code: 'ms', name: 'Bahasa Melayu', regions: ['asia'], markerCountry: 'MYS', countries: ['MYS','BRN','SGP','IDN'] },
  { code: 'th', name: 'ไทย', regions: ['asia'], markerCountry: 'THA', countries: ['THA'] },
]

function WorldMap({
  highlightedCountries,
  selectedCountry,
  onCountrySelect,
  ariaLabel,
}: {
  highlightedCountries: Set<string>
  selectedCountry: string | null
  onCountrySelect: (country: string) => void
  ariaLabel: string
  countryName: (code: string) => string
}) {
  return (
    <div className="absolute inset-0">
      <svg
        viewBox="0 0 1000 507"
        className="absolute inset-0 h-full w-full"
        preserveAspectRatio="xMidYMid meet"
        aria-label={ariaLabel}
        role="img"
      >
        <defs>
          <pattern id="atlas-graticule" width="100" height="84" patternUnits="userSpaceOnUse">
            <path d="M 100 0 L 0 0 0 84" fill="none" stroke="var(--juba-app-line)" strokeWidth="0.7" opacity="0.32" />
          </pattern>
        </defs>
        <rect width="1000" height="507" fill="url(#atlas-graticule)" />
        <g>
          {Object.entries(WORLD_MAP_PATHS).map(([code, path]) => {
            const highlighted = highlightedCountries.has(code)
            const selected = selectedCountry === code
            return (
              <path
                key={code}
                d={path}
                fill={selected ? 'var(--juba-app-yellow)' : highlighted ? 'var(--juba-app-green)' : 'var(--juba-app-green-soft)'}
                fillOpacity={selected || highlighted ? 0.92 : 0.72}
                stroke={selected ? 'var(--juba-app-ink)' : 'var(--juba-app-line)'}
                strokeWidth={selected ? 1.8 : highlighted ? 1.25 : 1.05}
                vectorEffect="non-scaling-stroke"
                className="cursor-pointer transition-[fill,fill-opacity,stroke-width] duration-200"
                tabIndex={0}
                onClick={() => onCountrySelect(code)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault()
                    onCountrySelect(code)
                  }
                }}
                aria-label={countryName(code)}
                role="button"
              />
            )
          })}
        </g>
      </svg>
    </div>
  )
}

export function LanguageBubbles() {
  const t = useTranslations('landing')
  const locale = useLocale() === 'ar' ? 'ar' : 'en'
  const countryName = (code: string) => COUNTRY_NAMES[code]?.[locale] ?? code
  const [activeRegion, setActiveRegion] = useState<RegionId | null>(null)
  const [activeLanguage, setActiveLanguage] = useState<string | null>(null)
  const [activeCountry, setActiveCountry] = useState<string | null>(null)

  const visibleLanguages = useMemo(
    () => DISPLAY_LANGUAGES.filter((language) => !activeRegion || language.regions.includes(activeRegion)),
    [activeRegion],
  )

  const selected = DISPLAY_LANGUAGES.find((language) => language.code === activeLanguage)
  const selectedRegion = selected ? REGIONS.find((region) => selected.regions.includes(region.id)) : null

  const regionCountries = useMemo(() => {
    const map = new Map<RegionId, Set<string>>()
    for (const region of REGIONS) map.set(region.id, new Set())
    for (const language of DISPLAY_LANGUAGES) for (const region of language.regions) map.get(region)?.add(...language.countries)
    return map
  }, [])

  const selectedCountries = selected ? new Set(selected.countries) : new Set<string>()

  const markerOffsets = useMemo(() => {
    const groups = new Map<string, DisplayLanguage[]>()
    for (const language of visibleLanguages) {
      const group = groups.get(language.markerCountry) ?? []
      group.push(language)
      groups.set(language.markerCountry, group)
    }

    const offsets = new Map<string, { x: number; y: number }>()
    for (const languages of groups.values()) {
      if (languages.length === 1) {
        offsets.set(languages[0].code, { x: 0, y: 0 })
        continue
      }

      const radius = languages.length <= 3 ? 14 : 18
      languages.forEach((language, index) => {
        const angle = (index / languages.length) * 2 * Math.PI - Math.PI / 2
        offsets.set(language.code, {
          x: Math.round(Math.cos(angle) * radius * 100) / 100,
          y: Math.round(Math.sin(angle) * radius * 100) / 100,
        })
      })
    }

    return offsets
  }, [visibleLanguages])
  const countryLanguages = useMemo(() => {
    const map = new Map<string, string[]>()
    for (const language of DISPLAY_LANGUAGES) {
      for (const country of language.countries) {
        const list = map.get(country) ?? []
        list.push(language.name)
        map.set(country, list)
      }
    }
    return map
  }, [])

  return (
    <div className="relative overflow-hidden rounded-[36px] border-2 border-[var(--juba-app-ink)] bg-[var(--juba-app-surface)] p-3 shadow-[6px_6px_0_var(--juba-app-ink)] sm:p-5">
      <div className="relative min-h-[430px] overflow-hidden rounded-[28px] border border-[var(--juba-app-line)] bg-[#f5f8f1] sm:min-h-[560px]">
        <WorldMap
          highlightedCountries={activeRegion ? (regionCountries.get(activeRegion) ?? new Set<string>()) : selectedCountries}
          selectedCountry={activeCountry}
          onCountrySelect={(country) => {
            setActiveCountry((current) => (current === country ? null : country))
            setActiveLanguage(null)
          }}
          ariaLabel={t('worldMapLabel')}
          countryName={countryName}
        />

        <div className="absolute inset-x-4 top-4 z-20 flex flex-wrap items-center justify-between gap-3 sm:inset-x-6 sm:top-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-[var(--juba-app-ink)] bg-white/95 px-3 py-2 text-[10px] font-black uppercase tracking-[.16em] text-[var(--juba-app-ink)] shadow-sm">
            <MapPinned className="h-3.5 w-3.5" aria-hidden="true" />
            {t('languageAtlasLabel')}
          </div>

          <span className="hidden rounded-full border border-[var(--juba-app-line)] bg-white/95 px-3 py-2 text-[10px] font-bold text-[var(--juba-app-muted)] shadow-sm sm:inline">
            {t('atlasCoverage', { count: DISPLAY_LANGUAGES.length })}
          </span>

          <button
            type="button"
            onClick={() => {
              setActiveRegion(null)
              setActiveLanguage(null)
            }}
            className="rounded-full border border-[var(--juba-app-line)] bg-white/95 px-3 py-2 text-[10px] font-black uppercase tracking-[.12em] text-[var(--juba-app-muted)] transition hover:border-[var(--juba-app-ink)] hover:text-[var(--juba-app-ink)]"
          >
            {t('allRegions')}
          </button>
        </div>

        <div className="absolute inset-0 z-10">
          <div className="absolute right-3 top-20 z-20 hidden max-w-[230px] rounded-2xl border border-[var(--juba-app-line)] bg-white/95 p-3 shadow-sm lg:block">
            <p className="text-[9px] font-black uppercase tracking-[.16em] text-[var(--juba-app-green)]">{t('mapCoverage')}</p>
            <p className="mt-1 text-xs leading-5 text-[var(--juba-app-muted)]">
              {t('mapCoverageDescription')}
            </p>
          </div>

          {visibleLanguages.map((language) => {
            const point = WORLD_MAP_CENTROIDS[language.markerCountry]
            if (!point) return null

            const isActive = activeLanguage === language.code
            const left = (point.x / 1000) * 100
            const top = (point.y / 507) * 100

            return (
              <button
                key={language.code}
                type="button"
                onClick={() => setActiveLanguage(isActive ? null : language.code)}
                className="group absolute"
                style={{
                  left: `${left}%`,
                  top: `${top}%`,
                  transform: `translate(calc(-50% + ${markerOffsets.get(language.code)?.x ?? 0}px), calc(-50% + ${markerOffsets.get(language.code)?.y ?? 0}px))`,
                }}
                aria-label={language.name}
                aria-pressed={isActive}
                title={countryLanguages.get(language.markerCountry)?.join(' · ')}
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

          {activeCountry && (
            <div className="absolute right-3 top-20 z-20 max-w-[250px] rounded-2xl border border-[var(--juba-app-line)] bg-white p-4 shadow-sm lg:right-6">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <span className="text-[9px] font-black uppercase tracking-[.16em] text-[var(--juba-app-green)]">{t('countryLanguages')}</span>
                  <h3 className="mt-1 text-lg font-black text-[var(--juba-app-ink)]">{countryName(activeCountry)}</h3>
                </div>
                <button type="button" onClick={() => setActiveCountry(null)} className="text-xs font-black text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)]" aria-label={t('closeCountryDetails')}>×</button>
              </div>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {(countryLanguages.get(activeCountry) ?? []).map((name) => {
                  const language = DISPLAY_LANGUAGES.find((item) => item.name === name)
                  const active = activeLanguage === language?.code
                  return (
                    <button
                      key={name}
                      type="button"
                      onClick={() => {
                        if (!language) return
                        setActiveLanguage(language.code)
                        setActiveRegion(language.regions[0] ?? null)
                      }}
                      className={`rounded-full border px-2 py-1 text-[10px] font-bold transition-colors ${active ? 'border-[var(--juba-app-green)] bg-[var(--juba-app-green-soft)] text-[var(--juba-app-ink)]' : 'border-[var(--juba-app-line)] text-[var(--juba-app-muted)] hover:border-[var(--juba-app-green)] hover:text-[var(--juba-app-ink)]'}`}
                    >
                      {name}
                    </button>
                  )
                })}
              </div>
            </div>
          )}

          {selected && selectedRegion && (
            <div className="absolute bottom-20 left-3 z-20 max-w-[calc(100%-1.5rem)] rounded-2xl border-2 border-[var(--juba-app-ink)] bg-white p-4 shadow-[4px_4px_0_var(--juba-app-ink)] sm:bottom-24 sm:left-6 sm:max-w-[280px]">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <span className="text-[9px] font-black uppercase tracking-[.18em] text-[var(--juba-app-green)]">{t(selectedRegion.key)}</span>
                  <h3 className="mt-1 text-lg font-black text-[var(--juba-app-ink)]">{selected.name}</h3>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveLanguage(null)}
                  className="text-xs font-black text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)]"
                  aria-label={t('closeLanguageDetails')}
                >
                  ×
                </button>
              </div>
              <p className="mt-2 text-xs leading-5 text-[var(--juba-app-muted)]">{t('exploreLanguage')}</p>
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
                  {t(region.key)}
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
            <p className="text-sm font-black text-[var(--juba-app-ink)]">{t('languagesByRegion')}</p>
            <p className="mt-1 text-xs leading-5 text-[var(--juba-app-muted)]">{t('atlasDescription')}</p>
          </div>
        </div>
        <span className="text-xs font-black text-[var(--juba-app-green)]">{t('languagesCount', { count: DISPLAY_LANGUAGES.length })}</span>
      </div>
    </div>
  )
}
