import * as React from 'react'
import { Input as InputPrimitive } from '@base-ui/react/input'

import { cn } from '@/lib/utils'

function Input({ className, type, ...props }: React.ComponentProps<'input'>) {
  return (
    <InputPrimitive
      type={type}
      data-slot="input"
      className={cn(
        'h-10 w-full min-w-0 rounded-xl border-2 border-[var(--duo-line)] bg-[var(--duo-card)] px-3 py-2 text-sm font-medium text-[var(--duo-ink)] shadow-[0_2px_0_var(--duo-line)] outline-none transition-[border-color,box-shadow,background-color,transform] placeholder:text-[var(--duo-muted)] file:inline-flex file:h-6 file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:border-[var(--duo-green-dark)] focus-visible:bg-[var(--duo-card)] focus-visible:ring-3 focus-visible:ring-[var(--duo-green)]/20 focus-visible:translate-y-[-1px] disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 aria-invalid:border-[var(--duo-red)] aria-invalid:ring-3 aria-invalid:ring-[var(--duo-red)]/15 md:text-sm',
        className
      )}
      {...props}
    />
  )
}

export { Input }
