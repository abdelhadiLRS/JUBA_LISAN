'use client'

import { useTranslations } from 'next-intl'
import { useThemeStore } from '@/store/theme'

export function AppearanceSection({ title }: { title?: string } = {}) {
  const t = useTranslations('settings')
  const theme = useThemeStore((s) => s.theme)
  const setTheme = useThemeStore((s) => s.setTheme)

  return (
    <div className="border-[var(--duo-line)] bg-[var(--duo-card)] border p-6">
      <div className="border-[var(--duo-line)] mb-5 flex items-center gap-2 border-b pb-4">
        <span className="text-[var(--duo-muted)]">●</span>
        <span className="text-[var(--duo-muted)] font-mono tracking-widest uppercase">
          {title ?? t('sectionAppearance')}
        </span>
      </div>
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-[var(--duo-ink)] font-mono text-xs tracking-wide">
            {t('theme')}
          </p>
          <p className="text-[var(--duo-muted)] mt-0.5 font-mono">
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
              className={`text-[var(--duo-ink)] border px-3 py-2 font-mono tracking-widest uppercase transition-colors ${
                theme === opt
                  ? 'border-[var(--duo-line)]-2 text-[var(--duo-ink)] bg-[var(--duo-card)]-2'
                  : 'border-[var(--duo-line)] text-[var(--duo-muted)] hover:border-[var(--duo-line)]-2 hover:text-[var(--duo-ink)]'
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
