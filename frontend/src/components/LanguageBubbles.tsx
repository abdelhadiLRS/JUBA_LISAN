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
        <div>
          <p className="text-[10px] font-black uppercase tracking-[.18em] text-[#635bff]">Explore languages</p>
          <h3 className="mt-1 text-xl font-black tracking-tight text-[#202127] sm:text-2xl">One world. {LANGUAGES.length} languages.</h3>
        </div>
        <span className="rounded-full bg-[#eeedff] px-3 py-1.5 text-[10px] font-extrabold text-[#635bff]">{LANGUAGES.length} languages</span>
      </div>
      <div className="grid grid-cols-2 gap-x-3 gap-y-5 sm:grid-cols-3 sm:gap-x-5 sm:gap-y-6 lg:grid-cols-4">
        {LANGUAGES.map((language, index) => (
          <div key={language.code} className="group flex min-w-0 flex-col items-center gap-2 text-center">
            <div className="juba-waving-flag relative flex h-[66px] w-[92px] items-center justify-center sm:h-[76px] sm:w-[108px]" style={{ animationDelay: `${(index % 7) * -0.22}s` }}>
              <Image
                src={`https://flagcdn.com/w160/${language.country}.png`}
                alt={`${language.alt} flag`}
                width={160}
                height={120}
                unoptimized
                className="h-[54px] w-[82px] rounded-[5px] object-cover shadow-[0_8px_16px_rgba(25,35,65,.18)] transition-transform duration-300 group-hover:scale-110 sm:h-[62px] sm:w-[96px]"
              />
            </div>
            <span className="max-w-full break-words text-xs font-extrabold text-[#202127] sm:text-sm">{language.name}</span>
          </div>
        ))}
      </div>
      <style jsx>{`
        .juba-waving-flag {
          transform-origin: 50% 45%;
          animation: juba-flag-wave 4.2s ease-in-out infinite;
        }
        .juba-waving-flag::after {
          content: "";
          position: absolute;
          inset: 7px 2px 1px;
          z-index: -1;
          border-radius: 8px;
          background: rgba(32, 33, 58, .12);
          filter: blur(9px);
          transform: translateY(7px) scaleX(.88);
        }
        @keyframes juba-flag-wave {
          0%, 100% { transform: perspective(500px) rotate(-2deg) skewY(-1deg); }
          50% { transform: perspective(500px) rotate(2deg) skewY(1.5deg) translateY(-3px); }
        }
        @media (prefers-reduced-motion: reduce) {
          .juba-waving-flag { animation: none; }
        }
      `}</style>
    </section>
  )
}
