import type { ElementType, HTMLAttributes, ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { getTargetLanguageTextClass } from '@/lib/target-languages'

interface TargetLanguageTextProps extends HTMLAttributes<HTMLElement> {
  languageCode?: string | null
  children: ReactNode
  as?: ElementType
  reading?: string | null
  translation?: string | null
}

export function TargetLanguageText({
  languageCode,
  children,
  as: Component = 'span',
  className,
  reading,
  translation,
  ...props
}: TargetLanguageTextProps) {
  const code = languageCode ?? ''
  const accessibleReading = reading?.trim()
  const accessibleTranslation = translation?.trim()

  return (
    <Component
      className={cn(getTargetLanguageTextClass(code), className)}
      lang={code || undefined}
      {...props}
    >
      {children}
      {(accessibleReading || accessibleTranslation) && (
        <span className="mt-1 block font-sans text-xs leading-relaxed tracking-normal normal-case text-[var(--juba-app-muted)] opacity-90">
          {[accessibleReading, accessibleTranslation].filter(Boolean).join(' · ')}
        </span>
      )}
    </Component>
  )
}
