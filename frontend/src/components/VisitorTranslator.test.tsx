import type {ReactNode} from 'react'
import {afterEach,beforeEach,describe,expect,it,vi} from 'vitest'
import {cleanup,fireEvent,render,screen,within} from '@testing-library/react'
import {VisitorTranslator} from './VisitorTranslator'
const {apiFetch,auth,translate}=vi.hoisted(()=>({apiFetch:vi.fn(),auth:{accessToken:''},translate:(key:string)=>key}))
vi.mock('@/lib/api',()=>({apiFetch,saveTranslatedWordLocally:vi.fn()}))
vi.mock('@/store/auth',()=>({useAuthStore:(selector:(value:{accessToken:string})=>unknown)=>selector(auth)}))
vi.mock('next-intl',()=>({useTranslations:()=>translate,useLocale:()=> 'en-US'}))
vi.mock('next/link',()=>({default:({href,children,...props}:{href:string;children:ReactNode})=><a href={href} {...props}>{children}</a>}))
vi.mock('@/lib/target-languages',()=>({TARGET_LANGUAGE_CATALOG:[{iso639:'en',name:'English'},{iso639:'ar',name:'Arabic'}]}))
beforeEach(()=>{apiFetch.mockReset();auth.accessToken=''})
afterEach(cleanup)
function open(){render(<VisitorTranslator/>);fireEvent.click(screen.getByRole('button',{name:'open'}));return within(screen.getByRole('dialog'))}
describe('Authenticated translator integration',()=>{
 it('requires sign-in for a guest instead of sending an unauthenticated API call',()=>{
  const dialog=open();expect(dialog.getByRole('link',{name:'Sign in'}).getAttribute('href')).toBe('/login');expect(dialog.queryByRole('textbox')).toBeNull();expect(apiFetch).not.toHaveBeenCalled()
 })
 it('uses the shared API client and server-compatible 1000 character limit',async()=>{
  auth.accessToken='token';apiFetch.mockResolvedValue({ok:true,status:200,json:async()=>({translation:'مرحبا',source:'en'})})
  const dialog=open(),input=dialog.getByRole('textbox',{name:'textToTranslate'})
  expect(input.getAttribute('maxlength')).toBe('1000')
  fireEvent.change(input,{target:{value:'Hello'}});fireEvent.click(dialog.getByRole('button',{name:'translate'}))
  await dialog.findByText('مرحبا');expect(apiFetch).toHaveBeenCalledWith('/api/translate',expect.objectContaining({method:'POST',body:JSON.stringify({text:'Hello',source:'auto',target:'ar'})}))
 })
 it('shows plan/reset navigation for structured quota exhaustion',async()=>{
  auth.accessToken='token';apiFetch.mockResolvedValue({ok:false,status:402,json:async()=>({detail:{reason:'quota_exhausted',feature:'translation'}})})
  const dialog=open();fireEvent.change(dialog.getByRole('textbox',{name:'textToTranslate'}),{target:{value:'Hello'}});fireEvent.click(dialog.getByRole('button',{name:'translate'}))
  const link=await dialog.findByRole('link',{name:'Plan and reset time'});expect(link.getAttribute('href')).toBe('/settings/subscription');expect(dialog.getByRole('alert').textContent).not.toContain('[object Object]')
 })
})
