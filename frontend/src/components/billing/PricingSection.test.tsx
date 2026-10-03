import type {ReactNode} from 'react'
import {afterEach,beforeEach,describe,expect,it,vi} from 'vitest'
import {cleanup,render,screen} from '@testing-library/react'
import PricingSection from './PricingSection'
const {apiFetch,auth}=vi.hoisted(()=>({apiFetch:vi.fn(),auth:{accessToken:''}}))
vi.mock('@/lib/api',()=>({apiFetch}))
vi.mock('@/store/auth',()=>({useAuthStore:(selector:(s:{accessToken:string})=>unknown)=>selector(auth)}))
vi.mock('next-intl',()=>({useLocale:()=> 'en-US'}))
vi.mock('next/link',()=>({default:({href,children,...props}:{href:string;children:ReactNode})=><a href={href} {...props}>{children}</a>}))
const props={stripeEnabled:true,trialDays:7,hasSession:false,priceMonthly:0,priceYearly:0,totalPriceMonthly:0,totalPriceYearly:0}
const catalog=(metered=true)=>({currency:'EUR',metered,trial:{tier:'go',days:7,card_required:false},plans:['free','go','plus'].map((tier,index)=>({tier,prices:{monthly:[0,799,1499][index],yearly:[0,7999,14999][index]},checkout_available:{monthly:metered&&index>0,yearly:metered&&index>0},voice_session_max_seconds:[300,900,1800][index],allowances:Object.fromEntries(['chat','lessons','reading','listening','flashcards','translation','voice','tts'].map(feature=>[feature,{limit:5,period:'day',unit:'requests'}]))}))})
const response=(data:unknown)=>({ok:true,json:async()=>data})
beforeEach(()=>{apiFetch.mockReset();auth.accessToken=''})
afterEach(cleanup)
describe('Tier pricing',()=>{
 it('uses login links when registration is closed',async()=>{
  apiFetch.mockResolvedValue(response({allow_registration:false,subscription_catalog:catalog()}))
  render(<PricingSection {...props}/>);const links=await screen.findAllByRole('link',{name:'Sign in'})
  expect(links).toHaveLength(3);expect(links.every(link=>link.getAttribute('href')==='/login')).toBe(true)
 })
 it('shows Free Go Plus rather than monthly and yearly products',async()=>{
  apiFetch.mockResolvedValue(response({allow_registration:true,subscription_catalog:catalog()}))
  render(<PricingSection {...props}/>);await screen.findByText('Go')
  expect(screen.getByText('Plus')).toBeTruthy();expect(screen.getByText('Free')).toBeTruthy()
  expect(screen.getByRole('button',{name:'Monthly'}).getAttribute('aria-pressed')).toBe('true')
 })
 it('uses portal actions instead of second checkout for paid users',async()=>{
  auth.accessToken='token';apiFetch.mockImplementation((url:string)=>Promise.resolve(response(url==='/api/config'?{allow_registration:true,subscription_catalog:catalog()}:{tier:'go',subscription_status:'active',trial_available:false,trial_ends_at:null})))
  render(<PricingSection {...props} hasSession/>);await screen.findByRole('button',{name:'Manage subscription'})
  expect(screen.getByRole('button',{name:'Change plan'})).toBeTruthy();expect(screen.queryByRole('button',{name:'Subscribe'})).toBeNull()
 })
 it('fails closed when account verification fails',async()=>{
  auth.accessToken='token';apiFetch.mockImplementation((url:string)=>Promise.resolve(url==='/api/config'?response({allow_registration:true,subscription_catalog:catalog()}):{ok:false}))
  render(<PricingSection {...props} hasSession/>);await screen.findByRole('alert')
  expect(screen.queryByRole('button',{name:'Subscribe'})).toBeNull()
 })
 it('does not expose paid checkout in self-hosted mode',async()=>{
  auth.accessToken='token';apiFetch.mockImplementation((url:string)=>Promise.resolve(response(url==='/api/config'?{subscription_catalog:catalog(false)}:{tier:'free',subscription_status:'none',trial_available:false,trial_ends_at:null})))
  render(<PricingSection {...props} hasSession/>);await screen.findAllByRole('link',{name:'Keep learning'})
  expect(screen.queryByRole('button',{name:'Subscribe'})).toBeNull()
 })
})
