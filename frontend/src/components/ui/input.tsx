import * as React from 'react'
import { Input as InputPrimitive } from '@base-ui/react/input'

import { cn } from '@/lib/utils'

function Input({ className, type, ...props }: React.ComponentProps<'input'>) {
  return (
    <InputPrimitive
      type={type}
      data-slot="input"
      className={cn(
        'h-10 w-full min-w-0 rounded-xl border-2 border-[var(--juba-border)] bg-[var(--juba-surface)] px-3 py-2 text-sm font-medium text-[var(--juba-text)] shadow-[0_2px_0_var(--juba-border)] outline-none transition-[border-color,box-shadow,background-color,transform] placeholder:text-[var(--juba-muted)] file:inline-flex file:h-6 file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:border-[var(--juba-primary-dark)] focus-visible:bg-[var(--juba-surface)] focus-visible:ring-3 focus-visible:ring-[var(--juba-primary)]/20 focus-visible:translate-y-[-1px] disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 aria-invalid:border-[var(--juba-danger)] aria-invalid:ring-3 aria-invalid:ring-[var(--juba-danger)]/15 md:text-sm',
        className
      )}
      {...props}
    />
  )
}

export { Input }
