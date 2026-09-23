'use client'

import { useTranslations } from 'next-intl'
import { useThemeStore } from '@/store/theme'

export function AppearanceSection({ title }: { title?: string } = {}) {
  const t = useTranslations('settings')
  const theme = useThemeStore((s) => s.theme)
  const setTheme = useThemeStore((s) => s.setTheme)

  return (
    <div className="border-[var(--juba-border)] bg-[var(--juba-surface)] border p-6">
      <div className="border-[var(--juba-border)] mb-5 flex items-center gap-2 border-b pb-4">
        <span className="text-[var(--juba-text)] text-[var(--juba-muted)]">●</span>
        <span className="text-[var(--juba-text)] text-[var(--juba-muted)] font-mono tracking-widest uppercase">
          {title ?? t('sectionAppearance')}
        </span>
      </div>
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-[var(--juba-text)] font-mono text-xs tracking-wide">
            {t('theme')}
          </p>
          <p className="text-[var(--juba-text)] text-[var(--juba-muted)] mt-0.5 font-mono">
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
              className={`text-[var(--juba-text)] border px-3 py-2 font-mono tracking-widest uppercase transition-colors ${
                theme === opt
                  ? 'border-[var(--juba-border)]-2 text-[var(--juba-text)] bg-[var(--juba-surface)]-2'
                  : 'border-[var(--juba-border)] text-[var(--juba-muted)] hover:border-[var(--juba-border)]-2 hover:text-[var(--juba-text)]'
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
