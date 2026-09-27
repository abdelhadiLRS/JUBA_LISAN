'use client'

import { Tabs as TabsPrimitive } from '@base-ui/react/tabs'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

function Tabs({ className, orientation = 'horizontal', ...props }: TabsPrimitive.Root.Props) {
  return (
    <TabsPrimitive.Root
      data-slot="tabs"
      data-orientation={orientation}
      className={cn('group/tabs flex gap-2 data-horizontal:flex-col', className)}
      {...props}
    />
  )
}

const tabsListVariants = cva(
  'group/tabs-list inline-flex w-fit items-center justify-center rounded-full border-2 border-[var(--juba-app-line)] p-1 text-[var(--juba-app-muted)] shadow-[2px_2px_0_var(--juba-app-line)] group-data-horizontal/tabs:h-11 group-data-vertical/tabs:h-fit group-data-vertical/tabs:flex-col data-[variant=line]:rounded-none data-[variant=line]:border-0 data-[variant=line]:shadow-none',
  {
    variants: {
      variant: {
        default: 'bg-[var(--juba-app-surface)]',
        line: 'gap-1 bg-transparent',
      },
    },
    defaultVariants: { variant: 'default' },
  }
)

function TabsList({
  className,
  variant = 'default',
  ...props
}: TabsPrimitive.List.Props & VariantProps<typeof tabsListVariants>) {
  return (
    <TabsPrimitive.List
      data-slot="tabs-list"
      data-variant={variant}
      className={cn(tabsListVariants({ variant }), className)}
      {...props}
    />
  )
}

function TabsTrigger({ className, ...props }: TabsPrimitive.Tab.Props) {
  return (
    <TabsPrimitive.Tab
      data-slot="tabs-trigger"
      className={cn(
        'relative inline-flex h-[calc(100%-1px)] flex-1 items-center justify-center gap-1.5 rounded-full border-2 border-transparent px-3.5 py-2 text-sm font-bold whitespace-nowrap text-[var(--juba-app-muted)] transition-[color,background-color,box-shadow,transform] hover:-translate-y-px hover:text-[var(--juba-app-green-dark)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--juba-app-green)]/40 focus-visible:ring-offset-1 disabled:pointer-events-none disabled:opacity-50 aria-disabled:pointer-events-none aria-disabled:opacity-50 group-data-vertical/tabs:w-full group-data-vertical/tabs:justify-start data-active:border-[var(--juba-app-green-dark)] data-active:bg-[var(--juba-app-green-soft)] data-active:text-[var(--juba-app-green-dark)] data-active:shadow-[2px_2px_0_var(--juba-app-line)] [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*="size-"])]:size-4',
        'group-data-[variant=line]/tabs-list:bg-transparent group-data-[variant=line]/tabs-list:data-active:bg-transparent group-data-[variant=line]/tabs-list:data-active:border-transparent group-data-[variant=line]/tabs-list:data-active:shadow-none',
        'after:absolute after:opacity-0 after:transition-opacity group-data-horizontal/tabs:after:inset-x-2 group-data-horizontal/tabs:after:bottom-[-5px] group-data-horizontal/tabs:after:h-0.5 group-data-vertical/tabs:after:inset-y-0 group-data-vertical/tabs:after:-right-1 group-data-vertical/tabs:after:w-0.5 group-data-[variant=line]/tabs-list:data-active:after:opacity-100 group-data-[variant=line]/tabs-list:after:bg-[var(--juba-app-green)]',
        className
      )}
      {...props}
    />
  )
}

function TabsContent({ className, ...props }: TabsPrimitive.Panel.Props) {
  return <TabsPrimitive.Panel data-slot="tabs-content" className={cn('flex-1 text-sm outline-none', className)} {...props} />
}

export { Tabs, TabsList, TabsTrigger, TabsContent, tabsListVariants }
