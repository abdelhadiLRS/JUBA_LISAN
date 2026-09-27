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

export const SUPPORTED_LANGUAGE_COUNT = LANGUAGES.length

export function LanguageBubbles({ dir = 'ltr' }: { dir?: 'ltr' | 'rtl' }) {
  return (
    <ul dir={dir} className="juba-busuu-language-list">
      {LANGUAGES.map((language) => (
        <li key={language.code} className="juba-busuu-language-item">
          <Image
            src={`https://flagcdn.com/w80/${language.country}.png`}
            alt=""
            aria-hidden="true"
            width={80}
            height={60}
            unoptimized
          />
          <span lang={language.code} dir="auto">{language.name}</span>
        </li>
      ))}
    </ul>
  )
}
