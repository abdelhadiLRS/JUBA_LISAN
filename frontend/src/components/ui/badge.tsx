import { mergeProps } from '@base-ui/react/merge-props'
import { useRender } from '@base-ui/react/use-render'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'group/badge inline-flex h-7 w-fit shrink-0 items-center justify-center gap-1 overflow-hidden rounded-full border-2 border-[var(--juba-border)] px-2.5 py-0.5 text-xs font-bold whitespace-nowrap transition-all focus-visible:border-[var(--juba-primary-dark)] focus-visible:ring-2 focus-visible:ring-[var(--juba-primary)]/25 has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 aria-invalid:border-[var(--juba-danger)] aria-invalid:ring-[var(--juba-danger)]/20 [&>svg]:pointer-events-none [&>svg]:size-3!',
  {
    variants: {
      variant: {
        default: 'bg-[var(--juba-primary)] text-[var(--juba-text)] [a]:hover:opacity-80',
        secondary:
          'bg-[var(--juba-surface-soft)] text-[var(--juba-text)] [a]:hover:bg-[var(--juba-border)]',
        destructive:
          'border-[color-mix(in_srgb,var(--juba-danger)_24%,var(--juba-border))] bg-[color-mix(in_srgb,var(--juba-danger)_10%,var(--juba-surface))] text-[var(--juba-danger)] [a]:hover:bg-[color-mix(in_srgb,var(--juba-danger)_16%,var(--juba-surface))]',
        outline:
          'bg-[var(--juba-surface)] text-[var(--juba-text)] [a]:hover:bg-[var(--juba-surface-soft)]',
        ghost:
          'border-transparent text-[var(--juba-muted)] hover:bg-[var(--juba-surface-soft)] hover:text-[var(--juba-text)]',
        link: 'border-transparent text-[var(--juba-primary-dark)] underline-offset-4 hover:underline',
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
