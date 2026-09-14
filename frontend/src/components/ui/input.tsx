import * as React from 'react'
import { Input as InputPrimitive } from '@base-ui/react/input'

import { cn } from '@/lib/utils'

function Input({ className, type, ...props }: React.ComponentProps<'input'>) {
  return (
    <InputPrimitive
      type={type}
      data-slot="input"
      className={cn(
        'h-9 w-full min-w-0 rounded-xl border border-[var(--juba-border)] bg-[var(--juba-surface-soft)] px-3 py-1.5 text-sm text-[var(--juba-text)] shadow-none outline-none transition-[border-color,box-shadow,background-color] placeholder:text-[var(--juba-muted)] file:inline-flex file:h-6 file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:border-[var(--juba-primary-dark)] focus-visible:bg-[var(--juba-surface)] focus-visible:ring-3 focus-visible:ring-[var(--juba-primary)]/30 disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 aria-invalid:border-[var(--juba-danger)] aria-invalid:ring-3 aria-invalid:ring-[var(--juba-danger)]/15 md:text-sm',
        className
      )}
      {...props}
    />
  )
}

export { Input }
