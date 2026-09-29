'use client'

import Image from 'next/image'

type Language = { code: string; name: string; country: string }

export const LANGUAGES: Language[] = [
  { code: 'en', name: 'English', country: 'gb' },
  { code: 'es', name: 'Español', country: 'es' },
  { code: 'fr', name: 'Français', country: 'fr' },
  { code: 'ja', name: '日本語', country: 'jp' },
  { code: 'de', name: 'Deutsch', country: 'de' },
  { code: 'it', name: 'Italiano', country: 'it' },
  { code: 'ko', name: '한국어', country: 'kr' },
  { code: 'ar', name: 'العربية', country: 'dz' },
  { code: 'ru', name: 'Русский', country: 'ru' },
  { code: 'tr', name: 'Türkçe', country: 'tr' },
  { code: 'zh', name: '中文', country: 'cn' },
  { code: 'pt', name: 'Português', country: 'pt' },
  { code: 'nl', name: 'Nederlands', country: 'nl' },
  { code: 'pl', name: 'Polski', country: 'pl' },
  { code: 'fi', name: 'Suomi', country: 'fi' },
  { code: 'sv', name: 'Svenska', country: 'se' },
  { code: 'he', name: 'עברית', country: 'il' },
  { code: 'yo', name: 'Yorùbá', country: 'ng' },
  { code: 'xh', name: 'isiXhosa', country: 'za' },
  { code: 'mg', name: 'Malagasy', country: 'mg' },
  { code: 'ny', name: 'Chichewa', country: 'mw' },
  { code: 'vi', name: 'Tiếng Việt', country: 'vn' },
  { code: 'mi', name: 'Māori', country: 'nz' },
  { code: 'sm', name: 'Gagana Sāmoa', country: 'ws' },
  { code: 'to', name: 'Lea faka-Tonga', country: 'to' },
  { code: 'sq', name: 'Shqip', country: 'al' },
  { code: 'eu', name: 'Euskara', country: 'es' },
  { code: 'gl', name: 'Galego', country: 'es' },
  { code: 'no', name: 'Norsk', country: 'no' },
  { code: 'da', name: 'Dansk', country: 'dk' },
  { code: 'cs', name: 'Čeština', country: 'cz' },
  { code: 'sk', name: 'Slovenčina', country: 'sk' },
  { code: 'fa', name: 'فارسی', country: 'ir' },
  { code: 'hi', name: 'हिन्दी', country: 'in' },
  { code: 'bn', name: 'বাংলা', country: 'bd' },
  { code: 'id', name: 'Bahasa Indonesia', country: 'id' },
  { code: 'ms', name: 'Bahasa Melayu', country: 'my' },
  { code: 'th', name: 'ไทย', country: 'th' },
]

export const FEATURED_LANGUAGES: Language[] = [
  { code: 'en', name: 'English', country: 'gb' },
  { code: 'es', name: 'Español', country: 'es' },
  { code: 'fr', name: 'Français', country: 'fr' },
  { code: 'ja', name: '日本語', country: 'jp' },
  { code: 'de', name: 'Deutsch', country: 'de' },
  { code: 'it', name: 'Italiano', country: 'it' },
  { code: 'ko', name: '한국어', country: 'kr' },
  { code: 'ar', name: 'العربية', country: 'dz' },
  { code: 'ru', name: 'Русский', country: 'ru' },
  { code: 'tr', name: 'Türkçe', country: 'tr' },
  { code: 'zh', name: '中文', country: 'cn' },
  { code: 'pt', name: 'Português', country: 'pt' },
  { code: 'nl', name: 'Nederlands', country: 'nl' },
  { code: 'pl', name: 'Polski', country: 'pl' },
]

export const SUPPORTED_LANGUAGE_COUNT = LANGUAGES.length

export function LanguageBubbles({ dir = 'ltr' }: { dir?: 'ltr' | 'rtl' }) {
  const featuredLanguages = FEATURED_LANGUAGES

  return (
    <ul
      dir={dir}
      className="juba-busuu-language-list"
      aria-labelledby="language-title"
      tabIndex={0}
    >
      {featuredLanguages.map((language) => (
        <li key={language.code} className="juba-busuu-language-item">
          <Image
            src={`https://flagcdn.com/w80/${language.country}.png`}
            alt=""
            aria-hidden="true"
            width={80}
            height={60}
            unoptimized
            style={{ height: 'auto' }}
          />
          <span lang={language.code} dir="auto">{language.name}</span>
        </li>
      ))}
    </ul>
  )
}
