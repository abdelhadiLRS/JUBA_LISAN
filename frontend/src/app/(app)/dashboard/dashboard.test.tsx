import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen, waitFor } from '@testing-library/react'
import DashboardPage from './page'

const { api, auth, language, progress, labels }=vi.hoisted(()=>({
  api:vi.fn(),auth:{user:{id:1,displayName:'Learner',username:'learner',avatar:null,subscription_status:'none',freemium_trial_ends_at:null},accessToken:'test-token'},
  language:{activeLanguage:{code:'it-IT'},isSwitching:false},
  progress:{streak:0,xp:0,todayLessons:[] as Array<Record<string,unknown>>,completedToday:[] as number[],setProgress:vi.fn(),setTodayLessons:vi.fn()},
  labels:{'nav.friends':'Friends','progress.dailyGoal':'Daily goal','progress.weeklyGoal':'Weekly goal','dashboard.welcomeBack':'Welcome back','dashboard.refresh':'Refresh dashboard','dashboard.loadingProgress':'Loading progress','error.body':'Could not load dashboard','error.retry':'Retry'} as Record<string,string>,
}))
vi.mock('@/lib/api',()=>({apiFetch:api}))
vi.mock('next-intl',()=>({useLocale:()=> 'en',useTranslations:(namespace:string)=>Object.assign((key:string)=>labels[`${namespace}.${key}`]||key,{has:()=>true})}))
vi.mock('@/store/auth',()=>({useAuthStore:(selector:(s:typeof auth)=>unknown)=>selector(auth),isSubscribed:()=>false,needsPaymentRecovery:()=>false,isFreemiumTrialActive:()=>false}))
vi.mock('@/store/config',()=>({useConfigStore:(selector:(s:{stripeEnabled:boolean})=>unknown)=>selector({stripeEnabled:false})}))
vi.mock('@/store/language',()=>({useLanguageStore:(selector:(s:typeof language)=>unknown)=>selector(language)}))
vi.mock('@/store/progress',()=>({useProgressStore:()=>progress}))
vi.mock('@/lib/learning-progress',()=>({subscribeToLearningProgressUpdated:()=>()=>{}}))
vi.mock('@/components/tour/OnboardingTour',()=>({default:()=>null}))
vi.mock('@/components/whats-new/WhatsNew',()=>({default:()=>null}))
vi.mock('@/components/ui/page-loading',()=>({PageLoading:({label}:{label:string})=><p>{label}</p>}))
vi.mock('@/components/billing/SubscriptionPlanButtons',()=>({SubscriptionPlanButtons:()=>null}))
vi.mock('@/components/AuthAvatarImage',()=>({AuthAvatarImage:()=>null}))
const response=(data:unknown)=>({ok:true,status:200,json:async()=>data})
const summary={total_xp:40,current_streak:2,total_lessons:3,accuracy:.82,vocabulary_progress:.2,vocabulary_mastered:2,vocabulary_total:10}
const goal={daily_xp:15,daily_xp_target:30,daily_progress:.5,weekly_xp:75,weekly_xp_target:250,weekly_progress:.3}
const entry={user_id:1,username:'learner',display_name:'Learner',rank:7,xp:15,is_current_user:true}
function answers(url:string){
  if(url.startsWith('/api/progress/summary'))return response(summary)
  if(url.startsWith('/api/study-plan/today'))return response({cefr_level:'A1',progress_day:0,total_days:48,lessons:[]})
  if(url.startsWith('/api/progress/history'))return response({entries:[]})
  if(url.startsWith('/api/progress/goals'))return response(goal)
  if(url.startsWith('/api/leagues/current'))return response({joined:true,tier:'silver',ends_at:'2026-10-05T00:00:00Z',entries:[entry],current_user:entry,total:1})
  return response([])
}
beforeEach(()=>{
  api.mockReset();api.mockImplementation((url:string)=>Promise.resolve(answers(url)))
  language.activeLanguage={code:'it-IT'};language.isSwitching=false
  progress.setProgress.mockReset();progress.setTodayLessons.mockReset()
  progress.xp=0;progress.streak=0;progress.todayLessons=[]
  progress.setProgress.mockImplementation((p:{xp:number;streak:number})=>{progress.xp=p.xp;progress.streak=p.streak})
  progress.setTodayLessons.mockImplementation((lessons:Array<Record<string,unknown>>)=>{progress.todayLessons=lessons})
})
afterEach(cleanup)

describe('Reference Dashboard v4',()=>{
  it('shows real goals and league standings without automatically enrolling',async()=>{
    render(<DashboardPage/>)
    await screen.findByRole('heading',{name:'Silver League'})
    expect(screen.getByText('50% of your daily goal!')).toBeTruthy()
    expect(screen.getByText('15/30')).toBeTruthy()
    expect(screen.getByText('15 XP')).toBeTruthy()
    expect(screen.getByText('82%')).toBeTruthy()
    expect(screen.getByRole('heading',{name:'Friends'})).toBeTruthy()
    expect(screen.queryByText('dashboard.friends')).toBeNull()
    expect(api.mock.calls.every(([,options])=>options===undefined)).toBe(true)
    expect(api.mock.calls.some(([url])=>url.includes('target_language=it-IT'))).toBe(true)
  })
  it('retains chart structure and a truthful no-activity state',async()=>{
    const {container}=render(<DashboardPage/>)
    await screen.findByText('No recorded activity for this period.')
    expect(container.querySelector('.reference-dashboard-chart-axis')).toBeTruthy()
    expect(container.querySelectorAll('.reference-dashboard-bar')).toHaveLength(0)
    expect(container.querySelector('.reference-dashboard-league')).toBeTruthy()
    expect(container.querySelector('.reference-dashboard-rail')).toBeTruthy()
  })
  it('distinguishes history/friend failures from successful empty reads',async()=>{
    api.mockImplementation((url:string)=>Promise.resolve(url.includes('/history')||url.includes('/social/friends')?{ok:false,status:503}:answers(url)))
    render(<DashboardPage/>)
    await screen.findByText('Could not load activity.')
    expect(screen.getByText('Could not load friends.')).toBeTruthy()
    expect(screen.queryByText('No recorded activity for this period.')).toBeNull()
  })
  it('offers a league link without inventing participants when not enrolled',async()=>{
    api.mockImplementation((url:string)=>Promise.resolve(url.includes('/leagues/current')?response({joined:false,tier:'bronze',entries:[],current_user:null,total:0}):answers(url)))
    render(<DashboardPage/>)
    const link=await screen.findByRole('link',{name:'Explore league'})
    expect(link.getAttribute('href')).toBe('/leagues')
    expect(screen.queryByText('15 XP')).toBeNull()
  })
  it('discards old-language responses after switching context',async()=>{
    const pending:Array<{url:string;resolve:(value:unknown)=>void}>=[]
    api.mockImplementation((url:string)=>new Promise(resolve=>pending.push({url,resolve})))
    const {rerender}=render(<DashboardPage/>)
    await waitFor(()=>expect(pending).toHaveLength(6))
    language.activeLanguage={code:'fr-FR'}
    rerender(<DashboardPage/>)
    await waitFor(()=>expect(pending).toHaveLength(12))
    pending.slice(6).forEach(({url,resolve})=>resolve(url.includes('/leagues/current')?response({joined:true,tier:'gold',ends_at:'2026-10-05T00:00:00Z',entries:[],current_user:null,total:0}):answers(url)))
    await screen.findByRole('heading',{name:'Gold League'})
    pending.slice(0,6).forEach(({url,resolve})=>resolve(answers(url)))
    await Promise.resolve();await Promise.resolve()
    expect(screen.queryByRole('heading',{name:'Silver League'})).toBeNull()
  })
})
