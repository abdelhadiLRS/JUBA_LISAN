'use client'

import Image from 'next/image'

type Language = { code: string; name: string; country: string; learners: string }

export const LANGUAGES: Language[] = [
  { code: 'en', name: 'English', country: 'gb', learners: '26M' },
  { code: 'es', name: 'Español', country: 'es', learners: '2M' },
  { code: 'fr', name: 'Français', country: 'fr', learners: '5M' },
  { code: 'ja', name: '日本語', country: 'jp', learners: '4M' },
  { code: 'de', name: 'Deutsch', country: 'de', learners: '4M' },
  { code: 'it', name: 'Italiano', country: 'it', learners: '2M' },
  { code: 'ko', name: '한국어', country: 'kr', learners: '100K' },
  { code: 'ar', name: 'العربية', country: 'dz', learners: '1M' },
  { code: 'ru', name: 'Русский', country: 'ru', learners: '1M' },
  { code: 'tr', name: 'Türkçe', country: 'tr', learners: '2M' },
  { code: 'zh', name: '中文', country: 'cn', learners: '2M' },
  { code: 'pt', name: 'Português', country: 'pt', learners: '2M' },
  { code: 'nl', name: 'Nederlands', country: 'nl', learners: '16K' },
  { code: 'pl', name: 'Polski', country: 'pl', learners: '2M' },
  { code: 'fi', name: 'Suomi', country: 'fi', learners: '—' },
  { code: 'sv', name: 'Svenska', country: 'se', learners: '—' },
  { code: 'he', name: 'עברית', country: 'il', learners: '—' },
  { code: 'yo', name: 'Yorùbá', country: 'ng', learners: '—' },
  { code: 'xh', name: 'isiXhosa', country: 'za', learners: '—' },
  { code: 'mg', name: 'Malagasy', country: 'mg', learners: '—' },
  { code: 'ny', name: 'Chichewa', country: 'mw', learners: '—' },
  { code: 'vi', name: 'Tiếng Việt', country: 'vn', learners: '—' },
  { code: 'mi', name: 'Māori', country: 'nz', learners: '—' },
  { code: 'sm', name: 'Gagana Sāmoa', country: 'ws', learners: '—' },
  { code: 'to', name: 'Lea faka-Tonga', country: 'to', learners: '—' },
  { code: 'sq', name: 'Shqip', country: 'al', learners: '—' },
  { code: 'eu', name: 'Euskara', country: 'es', learners: '—' },
  { code: 'gl', name: 'Galego', country: 'es', learners: '—' },
  { code: 'no', name: 'Norsk', country: 'no', learners: '—' },
  { code: 'da', name: 'Dansk', country: 'dk', learners: '—' },
  { code: 'cs', name: 'Čeština', country: 'cz', learners: '—' },
  { code: 'sk', name: 'Slovenčina', country: 'sk', learners: '—' },
  { code: 'fa', name: 'فارسی', country: 'ir', learners: '—' },
  { code: 'hi', name: 'हिन्दी', country: 'in', learners: '—' },
  { code: 'bn', name: 'বাংলা', country: 'bd', learners: '—' },
  { code: 'id', name: 'Bahasa Indonesia', country: 'id', learners: '—' },
  { code: 'ms', name: 'Bahasa Melayu', country: 'my', learners: '—' },
  { code: 'th', name: 'ไทย', country: 'th', learners: '—' },
]

export const FEATURED_LANGUAGES = LANGUAGES.slice(0, 14)
export const SUPPORTED_LANGUAGE_COUNT = LANGUAGES.length

export function LanguageBubbles({ dir = 'ltr' }: { dir?: 'ltr' | 'rtl' }) {
  return (
    <ul dir={dir} className="juba-busuu-language-list" aria-labelledby="language-title">
      {FEATURED_LANGUAGES.map((language) => (
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
          <small>{language.learners}</small>
        </li>
      ))}
    </ul>
  )
}
