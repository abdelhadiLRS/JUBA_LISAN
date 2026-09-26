'use client'

import Image from 'next/image'

type Language = { code: string; name: string; country: string; alt: string }

const LANGUAGES: Language[] = [
  { code: 'en', name: 'English', country: 'gb', alt: 'United Kingdom' },
  { code: 'fr', name: 'Français', country: 'fr', alt: 'France' },
  { code: 'es', name: 'Español', country: 'es', alt: 'Spain' },
  { code: 'de', name: 'Deutsch', country: 'de', alt: 'Germany' },
  { code: 'it', name: 'Italiano', country: 'it', alt: 'Italy' },
  { code: 'pt', name: 'Português', country: 'pt', alt: 'Portugal' },
  { code: 'nl', name: 'Nederlands', country: 'nl', alt: 'Netherlands' },
  { code: 'ru', name: 'Русский', country: 'ru', alt: 'Russia' },
  { code: 'tr', name: 'Türkçe', country: 'tr', alt: 'Türkiye' },
  { code: 'el', name: 'Ελληνικά', country: 'gr', alt: 'Greece' },
  { code: 'ro', name: 'Română', country: 'ro', alt: 'Romania' },
  { code: 'hu', name: 'Magyar', country: 'hu', alt: 'Hungary' },
  { code: 'uk', name: 'Українська', country: 'ua', alt: 'Ukraine' },
  { code: 'fi', name: 'Suomi', country: 'fi', alt: 'Finland' },
  { code: 'sv', name: 'Svenska', country: 'se', alt: 'Sweden' },
  { code: 'ar', name: 'العربية', country: 'dz', alt: 'Algeria' },
  { code: 'he', name: 'עברית', country: 'il', alt: 'Israel' },
  { code: 'yo', name: 'Yorùbá', country: 'ng', alt: 'Nigeria' },
  { code: 'xh', name: 'isiXhosa', country: 'za', alt: 'South Africa' },
  { code: 'mg', name: 'Malagasy', country: 'mg', alt: 'Madagascar' },
  { code: 'ny', name: 'Chichewa', country: 'mw', alt: 'Malawi' },
  { code: 'vi', name: 'Tiếng Việt', country: 'vn', alt: 'Vietnam' },
  { code: 'ja', name: '日本語', country: 'jp', alt: 'Japan' },
  { code: 'ko', name: '한국어', country: 'kr', alt: 'South Korea' },
  { code: 'zh', name: '中文', country: 'cn', alt: 'China' },
  { code: 'mi', name: 'Māori', country: 'nz', alt: 'New Zealand' },
  { code: 'sm', name: 'Gagana Sāmoa', country: 'ws', alt: 'Samoa' },
  { code: 'to', name: 'Lea faka-Tonga', country: 'to', alt: 'Tonga' },
  { code: 'sq', name: 'Shqip', country: 'al', alt: 'Albania' },
  { code: 'eu', name: 'Euskara', country: 'es', alt: 'Basque Country · Spain' },
  { code: 'gl', name: 'Galego', country: 'es', alt: 'Galicia · Spain' },
  { code: 'no', name: 'Norsk', country: 'no', alt: 'Norway' },
  { code: 'da', name: 'Dansk', country: 'dk', alt: 'Denmark' },
  { code: 'pl', name: 'Polski', country: 'pl', alt: 'Poland' },
  { code: 'cs', name: 'Čeština', country: 'cz', alt: 'Czechia' },
  { code: 'sk', name: 'Slovenčina', country: 'sk', alt: 'Slovakia' },
  { code: 'fa', name: 'فارسی', country: 'ir', alt: 'Iran' },
  { code: 'hi', name: 'हिन्दी', country: 'in', alt: 'India' },
  { code: 'bn', name: 'বাংলা', country: 'bd', alt: 'Bangladesh' },
  { code: 'id', name: 'Bahasa Indonesia', country: 'id', alt: 'Indonesia' },
  { code: 'ms', name: 'Bahasa Melayu', country: 'my', alt: 'Malaysia' },
  { code: 'th', name: 'ไทย', country: 'th', alt: 'Thailand' },
]

export function LanguageBubbles({ dir = 'ltr' }: { dir?: 'ltr' | 'rtl' }) {
  return (
    <section dir={dir} aria-label="Languages available in JUBA LISAN" className="w-full rounded-[28px] border border-[#e7e8ef] bg-white/95 p-4 shadow-[0_16px_38px_rgba(32,33,58,.09)] sm:p-6">
      <div className="mb-5 flex flex-wrap items-end justify-between gap-3">
        <div className={dir === 'rtl' ? 'text-right' : 'text-left'}>
          <p className="text-[10px] font-black uppercase tracking-[.18em] text-[#635bff]">Explore languages</p>
          <h3 className="mt-1 text-xl font-black tracking-tight text-[#202127] sm:text-2xl">Search the world. {LANGUAGES.length} languages.</h3>
        </div>
        <span className="rounded-full bg-[#eeedff] px-3 py-1.5 text-[10px] font-extrabold text-[#635bff]">{LANGUAGES.length} languages</span>
      </div>
      <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2 sm:gap-3 lg:grid-cols-3">
        {LANGUAGES.map((language) => (
          <div
            key={language.code}
            className={`group flex min-w-0 items-center gap-3 rounded-2xl border border-[#e9eaf2] bg-white px-3 py-3 transition-all duration-200 hover:-translate-y-0.5 hover:border-[#c9c7ff] hover:bg-[#f8f7ff] hover:shadow-[0_8px_20px_rgba(32,33,58,.07)] ${dir === 'rtl' ? 'flex-row-reverse text-right' : 'flex-row text-left'}`}
          >
            <div className="relative h-11 w-[62px] shrink-0 overflow-hidden rounded-lg border border-black/5 bg-[#f3f4f8] shadow-sm">
              <Image
                src={`https://flagcdn.com/w160/${language.country}.png`}
                alt={`${language.alt} flag`}
                width={160}
                height={120}
                unoptimized
                className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
            </div>
            <span lang={language.code} dir="auto" className="min-w-0 flex-1 break-words text-sm font-extrabold text-[#202127]">
              {language.name}
            </span>
          </div>
        ))}
      </div>
    </section>
  )
}
