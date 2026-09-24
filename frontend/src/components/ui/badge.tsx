import { mergeProps } from '@base-ui/react/merge-props'
import { useRender } from '@base-ui/react/use-render'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'group/badge inline-flex h-7 w-fit shrink-0 items-center justify-center gap-1 overflow-hidden rounded-full border-2 border-[var(--juba-app-line)] px-2.5 py-0.5 text-xs font-bold whitespace-nowrap transition-all focus-visible:border-[var(--juba-app-green-dark)] focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)]/25 has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 aria-invalid:border-[#b33a32] aria-invalid:ring-[#b33a32]/20 [&>svg]:pointer-events-none [&>svg]:size-3!',
  {
    variants: {
      variant: {
        default: 'bg-[var(--juba-app-yellow)] text-[var(--juba-app-ink)] [a]:hover:opacity-80',
        secondary:
          'bg-[#f3f7ef] text-[var(--juba-app-ink)] [a]:hover:bg-[var(--juba-app-green-soft)]',
        destructive:
          'border-[#b33a32]/30 bg-[#b33a32]/10 text-[#b33a32] [a]:hover:bg-[#b33a32]/20',
        outline:
          'bg-[var(--juba-app-surface)] text-[var(--juba-app-ink)] [a]:hover:bg-[#f3f7ef]',
        ghost:
          'border-transparent text-[var(--juba-app-muted)] hover:bg-[#f3f7ef] hover:text-[var(--juba-app-ink)]',
        link: 'border-transparent text-[var(--juba-app-green-dark)] underline-offset-4 hover:underline',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

function Badge({
  className,
  variant = 'default',
  render,
  ...props
}: useRender.ComponentProps<'span'> & VariantProps<typeof badgeVariants>) {
  return useRender({
    defaultTagName: 'span',
    props: mergeProps<'span'>(
      {
        className: cn(badgeVariants({ variant }), className),
      },
      props
    ),
    render,
    state: {
      slot: 'badge',
      variant,
    },
  })
}

export { Badge, badgeVariants }
