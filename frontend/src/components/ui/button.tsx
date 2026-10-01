import { Button as ButtonPrimitive } from '@base-ui/react/button'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva("group/button inline-flex shrink-0 items-center justify-center rounded-[10px] border border-transparent bg-clip-padding text-sm font-semibold whitespace-nowrap transition-[box-shadow,background-color,border-color] outline-none select-none focus-visible:ring-2 focus-visible:ring-[var(--duo-green)]/20 active:not-aria-[haspopup]:translate-y-px disabled:pointer-events-none disabled:opacity-50 aria-invalid:border-[var(--duo-red)] aria-invalid:ring-2 aria-invalid:ring-[var(--duo-red)]/20 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4", {
  variants: {
    variant: {
      default: 'border-[var(--duo-green)] bg-[var(--duo-green)] text-white shadow-sm hover:bg-[var(--duo-green-dark)]',
      outline: 'border-[var(--duo-line)] bg-[var(--duo-card)] text-[var(--duo-ink)] shadow-sm hover:bg-[var(--duo-bg)]',
      secondary: 'border-[var(--duo-line)] bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)] text-[var(--duo-green-dark)] shadow-none hover:bg-[color-mix(in_srgb,var(--duo-green)_14%,transparent)]',
      ghost: 'text-[var(--duo-muted)] hover:bg-[var(--duo-bg)] hover:text-[var(--duo-ink)]',
      destructive: 'border-[var(--duo-red)]/30 bg-[var(--duo-red)]/10 text-[var(--duo-red)] hover:bg-[var(--duo-red)]/20 focus-visible:ring-[var(--duo-red)]/20',
      link: 'text-[var(--duo-green-dark)] underline-offset-4 hover:underline',
    },
    size: {
      default: 'h-9 gap-1.5 px-3.5 has-data-[icon=inline-end]:pr-3 has-data-[icon=inline-start]:pl-3',
      xs: "h-6 gap-1 rounded-lg px-2 text-xs in-data-[slot=button-group]:rounded-lg has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 [&_svg:not([class*='size-'])]:size-3",
      sm: "h-8 gap-1 rounded-lg px-2.5 text-[0.8rem] in-data-[slot=button-group]:rounded-lg has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 [&_svg:not([class*='size-'])]:size-3.5",
      lg: 'h-10 gap-1.5 px-4.5 has-data-[icon=inline-end]:pr-3.5 has-data-[icon=inline-start]:pl-3.5',
      icon: 'size-9', 'icon-xs': "size-6 rounded-lg in-data-[slot=button-group]:rounded-lg [&_svg:not([class*='size-'])]:size-3", 'icon-sm': 'size-8 rounded-lg in-data-[slot=button-group]:rounded-lg', 'icon-lg': 'size-10',
    },
  }, defaultVariants: { variant: 'default', size: 'default' },
})
function Button({ className, variant = 'default', size = 'default', ...props }: ButtonPrimitive.Props & VariantProps<typeof buttonVariants>) { return <ButtonPrimitive data-slot="button" className={cn(buttonVariants({ variant, size, className }))} {...props} /> }
export { Button, buttonVariants }
