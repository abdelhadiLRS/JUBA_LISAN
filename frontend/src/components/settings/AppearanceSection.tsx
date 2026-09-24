'use client'

import { useTranslations } from 'next-intl'
import { useThemeStore } from '@/store/theme'

export function AppearanceSection({ title }: { title?: string } = {}) {
  const t = useTranslations('settings')
  const theme = useThemeStore((s) => s.theme)
  const setTheme = useThemeStore((s) => s.setTheme)

  return (
    <div className="border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] border p-6">
      <div className="border-[var(--juba-app-line)] mb-5 flex items-center gap-2 border-b pb-4">
        <span className="text-[var(--juba-app-muted)]">●</span>
        <span className="text-[var(--juba-app-muted)] font-mono tracking-widest uppercase">
          {title ?? t('sectionAppearance')}
        </span>
      </div>
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-[var(--juba-app-ink)] font-mono text-xs tracking-wide">
            {t('theme')}
          </p>
          <p className="text-[var(--juba-app-muted)] mt-0.5 font-mono">
            {theme === 'dark'
              ? t('darkActive')
              : theme === 'light'
                ? t('lightActive')
                : t('systemActive')}
          </p>
        </div>
        <div className="flex gap-1">
          {(['system', 'dark', 'light'] as const).map((opt) => (
            <button
              key={opt}
              onClick={() => setTheme(opt)}
              className={`text-[var(--juba-app-ink)] border px-3 py-2 font-mono tracking-widest uppercase transition-colors ${
                theme === opt
                  ? 'border-[var(--juba-app-line)]-2 text-[var(--juba-app-ink)] bg-[var(--juba-app-surface)]-2'
                  : 'border-[var(--juba-app-line)] text-[var(--juba-app-muted)] hover:border-[var(--juba-app-line)]-2 hover:text-[var(--juba-app-ink)]'
              }`}
            >
              {opt === 'system'
                ? t('themeSystem')
                : opt === 'dark'
                  ? t('themeDark')
                  : t('themeLight')}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
