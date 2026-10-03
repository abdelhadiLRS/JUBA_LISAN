import type { ReactNode } from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import FlashcardsPage from './page'
const {apiFetch,markUpdated}=vi.hoisted(()=>({apiFetch:vi.fn(),markUpdated:vi.fn()}))
vi.mock('@/lib/api',()=>({apiFetch}))
vi.mock('@/lib/learning-progress',()=>({markLearningProgressUpdated:markUpdated}))
vi.mock('next-intl',()=>({useTranslations:()=> (key:string)=>key}))
vi.mock('next/link',()=>({default:({children,href,...props}:{children:ReactNode;href:string})=><a href={href} {...props}>{children}</a>}))
vi.mock('@/store/language',()=>({useLanguageStore:(selector:(state:{activeLanguage:{code:string}})=>unknown)=>selector({activeLanguage:{code:'en-GB'}})}))
vi.mock('@/components/ui/AudioPlayer',()=>({AudioPlayer:()=> <span>audio</span>}))
vi.mock('@/components/ui/VoiceRecorder',()=>({VoiceRecorder:()=> <span>recorder</span>}))
vi.mock('@/components/ui/page-loading',()=>({PageLoading:()=> <div role="status">loading</div>}))
vi.mock('@/components/TargetLanguageText',()=>({TargetLanguageText:({children,as:Tag='span',className,dir}:{children:ReactNode;as?:'p'|'span';className?:string;dir?:string})=><Tag className={className} dir={dir}>{children}</Tag>}))
const cards=[{id:1,word:'apple',definition:'A fruit.',example_sentence:'An apple.',translation:'pomme',ease_factor:2.5,interval:1,repetitions:0},{id:2,word:'pear',definition:'Another fruit.',example_sentence:'A pear.',translation:'poire',ease_factor:2.5,interval:1,repetitions:0}]
beforeEach(()=>{apiFetch.mockReset();markUpdated.mockReset()})
afterEach(cleanup)
async function reveal(){await screen.findByText('apple');fireEvent.click(screen.getByRole('button',{name:'tapToReveal'}))}
describe('Flashcard review persistence',()=>{
  it('keeps the current card when the server rejects its rating',async()=>{
    apiFetch.mockImplementation((url:string)=>Promise.resolve(url==='/api/flashcards/due'?{ok:true,json:async()=>({due:cards,total:2})}:{ok:false}))
    render(<FlashcardsPage/>)
    await reveal()
    fireEvent.click(screen.getByRole('button',{name:'good'}))
    await screen.findByRole('alert')
    expect(screen.getByText('apple')).toBeTruthy()
    expect(screen.queryByText('pear')).toBeNull()
    expect(markUpdated).not.toHaveBeenCalled()
  })
  it('sends one rating and advances once while a request is pending',async()=>{
    let resolveReview!:(value:{ok:boolean})=>void
    const pending=new Promise<{ok:boolean}>(resolve=>{resolveReview=resolve})
    apiFetch.mockImplementation((url:string)=>url==='/api/flashcards/due'?Promise.resolve({ok:true,json:async()=>({due:cards,total:2})}):pending)
    render(<FlashcardsPage/>)
    await reveal()
    const button=screen.getByRole('button',{name:'good'})
    fireEvent.click(button);fireEvent.click(button)
    expect(apiFetch.mock.calls.filter(([url])=>String(url).endsWith('/review'))).toHaveLength(1)
    resolveReview({ok:true})
    await screen.findByText('pear')
    expect(markUpdated).toHaveBeenCalledTimes(1)
  })
  it('shows a load failure instead of claiming all cards are reviewed',async()=>{
    apiFetch.mockResolvedValue({ok:false})
    render(<FlashcardsPage/>)
    await screen.findByRole('alert')
    expect(screen.queryByText('noDue')).toBeNull()
    expect(screen.getByRole('button',{name:'retry'})).toBeTruthy()
  })
  it('shows zero completed progress before the first successful save',async()=>{
    apiFetch.mockResolvedValue({ok:true,json:async()=>({due:cards,total:2})})
    render(<FlashcardsPage/>)
    await screen.findByText('apple')
    await waitFor(()=>expect(screen.getByRole('progressbar').getAttribute('aria-valuenow')).toBe('0'))
  })
})
