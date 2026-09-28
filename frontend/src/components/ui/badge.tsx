import { mergeProps } from '@base-ui/react/merge-props'
import { useRender } from '@base-ui/react/use-render'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'group/badge inline-flex h-7 w-fit shrink-0 items-center justify-center gap-1 overflow-hidden rounded-full border-2 border-[var(--duo-line)] px-2.5 py-0.5 text-xs font-bold whitespace-nowrap transition-all focus-visible:border-[var(--duo-green-dark)] focus-visible:ring-2 focus-visible:ring-[var(--duo-green)]/25 has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 aria-invalid:border-[var(--duo-red)] aria-invalid:ring-[var(--duo-red)]/20 [&>svg]:pointer-events-none [&>svg]:size-3!',
  {
    variants: {
      variant: {
        default: 'bg-[var(--duo-yellow)] text-[var(--duo-ink)] [a]:hover:opacity-80',
        secondary:
          'bg-[color-mix(in_srgb,var(--duo-green)_8%,transparent)] text-[var(--duo-ink)] [a]:hover:bg-[color-mix(in_srgb,var(--duo-green)_10%,transparent)]',
        destructive:
          'border-[var(--duo-red)]/30 bg-[var(--duo-red)]/10 text-[var(--duo-red)] [a]:hover:bg-[var(--duo-red)]/20',
        outline:
          'bg-[var(--duo-card)] text-[var(--duo-ink)] [a]:hover:bg-[color-mix(in_srgb,var(--duo-green)_8%,transparent)]',
        ghost:
          'border-transparent text-[var(--duo-muted)] hover:bg-[color-mix(in_srgb,var(--duo-green)_8%,transparent)] hover:text-[var(--duo-ink)]',
        link: 'border-transparent text-[var(--duo-green-dark)] underline-offset-4 hover:underline',
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
