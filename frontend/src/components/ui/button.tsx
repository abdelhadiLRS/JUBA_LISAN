import { Button as ButtonPrimitive } from '@base-ui/react/button'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const buttonVariants = cva(
  "group/button inline-flex shrink-0 items-center justify-center rounded-xl border-2 border-transparent bg-clip-padding text-sm font-semibold whitespace-nowrap transition-all outline-none select-none focus-visible:border-[var(--juba-app-green-dark)] focus-visible:ring-3 focus-visible:ring-[var(--juba-app-green)]/30 active:not-aria-[haspopup]:translate-y-[2px] disabled:pointer-events-none disabled:opacity-50 aria-invalid:border-[#b33a32] aria-invalid:ring-3 aria-invalid:ring-[#b33a32]/20 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
  {
    variants: {
      variant: {
        default: 'border-[var(--juba-app-ink)] bg-[var(--juba-app-green)] text-white shadow-[0_4px_0_var(--juba-app-ink)] hover:brightness-105 hover:-translate-y-px',
        outline:
          'border-[var(--juba-app-line)] bg-[var(--juba-app-surface)] text-[var(--juba-app-ink)] shadow-[0_3px_0_var(--juba-app-line)] hover:bg-[var(--juba-app-bg)] hover:border-[#b8d1aa] hover:-translate-y-px aria-expanded:bg-[var(--juba-app-bg)]',
        secondary:
          'border-[var(--juba-app-line)] bg-[#f3f7ef] text-[var(--juba-app-ink)] shadow-[0_3px_0_var(--juba-app-line)] hover:bg-[var(--juba-app-green-soft)] aria-expanded:bg-[var(--juba-app-green-soft)]',
        ghost:
          'text-[var(--juba-app-muted)] hover:bg-[#f3f7ef] hover:text-[var(--juba-app-ink)]',
        destructive:
          'border-[#b33a32]/30 bg-[#b33a32]/10 text-[#b33a32] hover:bg-[#b33a32]/20 focus-visible:border-[#b33a32]/40 focus-visible:ring-[#b33a32]/20',
        link: 'text-[var(--juba-app-green-dark)] underline-offset-4 hover:underline',
      },
      size: {
        default:
          'h-9 gap-1.5 px-3 has-data-[icon=inline-end]:pr-2.5 has-data-[icon=inline-start]:pl-2.5',
        xs: "h-6 gap-1 rounded-lg px-2 text-xs in-data-[slot=button-group]:rounded-lg has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 [&_svg:not([class*='size-'])]:size-3",
        sm: "h-8 gap-1 rounded-lg px-2.5 text-[0.8rem] in-data-[slot=button-group]:rounded-lg has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 [&_svg:not([class*='size-'])]:size-3.5",
        lg: 'h-10 gap-1.5 px-4 has-data-[icon=inline-end]:pr-3 has-data-[icon=inline-start]:pl-3',
        icon: 'size-9',
        'icon-xs': "size-6 rounded-lg in-data-[slot=button-group]:rounded-lg [&_svg:not([class*='size-'])]:size-3",
        'icon-sm': 'size-8 rounded-lg in-data-[slot=button-group]:rounded-lg',
        'icon-lg': 'size-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

function Button({
  className,
  variant = 'default',
  size = 'default',
  ...props
}: ButtonPrimitive.Props & VariantProps<typeof buttonVariants>) {
  return (
    <ButtonPrimitive
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
