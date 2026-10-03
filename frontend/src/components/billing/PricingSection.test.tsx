import type {ReactNode} from 'react'
import {afterEach,beforeEach,describe,expect,it,vi} from 'vitest'
import {cleanup,render,screen,waitFor} from '@testing-library/react'
import PricingSection from './PricingSection'
const {apiFetch,subscription,translate}=vi.hoisted(()=>({apiFetch:vi.fn(),subscription:vi.fn(),translate:(key:string)=>key}))
vi.mock('@/lib/api',()=>({apiFetch}))
vi.mock('@/lib/landing-subscription',()=>({getLandingSubscriptionState:subscription}))
vi.mock('@/store/auth',()=>({useAuthStore:(selector:(s:{accessToken:string})=>unknown)=>selector({accessToken:'token'})}))
vi.mock('next-intl',()=>({useTranslations:()=>translate}))
vi.mock('next/link',()=>({default:({href,children,...props}:{href:string;children:ReactNode})=><a href={href} {...props}>{children}</a>}))
const props={stripeEnabled:true,trialDays:7,hasSession:false,priceMonthly:10,priceYearly:100,totalPriceMonthly:10,totalPriceYearly:120}
const config=(values:Record<string,unknown>={})=>({ok:true,json:async()=>({stripe_enabled:true,allow_registration:true,stripe_trial_days:7,price_monthly:10,price_yearly:100,total_price_monthly:10,total_price_yearly:120,...values})})
beforeEach(()=>{apiFetch.mockReset();subscription.mockReset();subscription.mockResolvedValue({subscribed:false,trialUsed:false})})
afterEach(cleanup)
describe('Pricing action integration',()=>{
 it('uses login links when registration is closed',async()=>{
  apiFetch.mockResolvedValue(config({allow_registration:false}))
  render(<PricingSection {...props}/>)
  await screen.findAllByRole('link',{name:'signIn'})
  expect(screen.getAllByRole('link').every(link=>link.getAttribute('href')==='/login')).toBe(true)
 })
 it('does not expose checkout buttons when Stripe is disabled',async()=>{
  apiFetch.mockResolvedValue(config({stripe_enabled:false}))
  render(<PricingSection {...props} hasSession/>)
  await screen.findByRole('link',{name:'dashboard'})
  expect(screen.queryByRole('button',{name:'ctaRegister'})).toBeNull()
  expect(screen.queryByText('planMonthlyName')).toBeNull()
 })
 it('does not offer a second subscription to an active subscriber',async()=>{
  subscription.mockResolvedValue({subscribed:true,trialUsed:true})
  apiFetch.mockResolvedValue(config())
  render(<PricingSection {...props} hasSession/>)
  await waitFor(()=>expect(screen.getAllByRole('link',{name:'dashboard'})).toHaveLength(4))
  expect(screen.queryByRole('button',{name:'ctaRegisterTrialUsed'})).toBeNull()
 })
 it('blocks checkout when subscription verification fails',async()=>{
  subscription.mockRejectedValue(new Error('unverified'))
  apiFetch.mockResolvedValue(config())
  render(<PricingSection {...props} hasSession/>)
  await screen.findByRole('alert')
  expect(screen.queryByRole('button',{name:'ctaRegister'})).toBeNull()
 })
})
