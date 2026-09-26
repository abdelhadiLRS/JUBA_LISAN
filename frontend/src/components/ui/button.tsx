import { Button as ButtonPrimitive } from '@base-ui/react/button'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva("group/button inline-flex shrink-0 items-center justify-center rounded-[14px] border border-transparent bg-clip-padding text-sm font-semibold whitespace-nowrap transition-[transform,box-shadow,background-color,border-color] outline-none select-none focus-visible:ring-3 focus-visible:ring-[#5862e2]/20 active:not-aria-[haspopup]:translate-y-px disabled:pointer-events-none disabled:opacity-50 aria-invalid:border-[#b33a32] aria-invalid:ring-3 aria-invalid:ring-[#b33a32]/20 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4", {
  variants: {
    variant: {
      default: 'border-[#5862e2] bg-[#5862e2] text-white shadow-[0_5px_0_#373fb8] hover:-translate-y-px hover:shadow-[0_6px_0_#373fb8]',
      outline: 'border-[rgba(7,7,9,.09)] bg-white text-[#202127] shadow-[0_4px_0_rgba(7,7,9,.08)] hover:bg-[#f4f4f2] hover:-translate-y-px',
      secondary: 'border-[rgba(7,7,9,.08)] bg-[#ededff] text-[#373fb8] shadow-none hover:bg-[#e4e5ff] hover:-translate-y-px',
      ghost: 'text-[rgba(32,33,39,.52)] hover:bg-[#f4f4f2] hover:text-[#202127]',
      destructive: 'border-[#b33a32]/30 bg-[#b33a32]/10 text-[#b33a32] hover:bg-[#b33a32]/20 focus-visible:ring-[#b33a32]/20',
      link: 'text-[#373fb8] underline-offset-4 hover:underline',
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
