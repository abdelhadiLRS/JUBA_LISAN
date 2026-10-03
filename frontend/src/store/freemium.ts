import {create} from 'zustand'
import {apiFetch} from '@/lib/api'
import {useAuthStore} from '@/store/auth'
import {quotaAccountKey} from '@/lib/quota-client'

interface FreemiumStatus{
 trial_active:boolean
 trial_ends_at:string|null
 chat_remaining:number
 chat_limit:number
 lessons_remaining:number
 lessons_limit:number
 listening_remaining:number
 listening_limit:number
 reading_remaining:number
 reading_limit:number
 voice_remaining_seconds:number
 voice_limit_seconds:number
}
type NumericFreemiumKey='chat_remaining'|'lessons_remaining'|'listening_remaining'|'reading_remaining'
interface FreemiumStore{
 status:FreemiumStatus|null
 loaded:boolean
 lastFetch:number
 fetchStatus:(force?:boolean)=>Promise<void>
 decrement:(feature:NumericFreemiumKey)=>void
}
function account(){const auth=useAuthStore.getState();return quotaAccountKey(auth.accessToken,auth.user)}
let activeAccount:string|null=account(),generation=0
let pending:{account:string;generation:number;promise:Promise<void>}|null=null
function validStatus(data:unknown):data is FreemiumStatus{
 if(!data||typeof data!=='object')return false
 const value=data as Record<string,unknown>
 return typeof value.trial_active==='boolean'&&(value.trial_ends_at===null||typeof value.trial_ends_at==='string')&&
 ['chat_remaining','chat_limit','lessons_remaining','lessons_limit','listening_remaining','listening_limit','reading_remaining','reading_limit','voice_remaining_seconds','voice_limit_seconds'].every(key=>typeof value[key]==='number'&&Number.isInteger(value[key])&&(value[key] as number)>=0)
}
export const useFreemiumStore=create<FreemiumStore>((set,get)=>({
 status:null,loaded:false,lastFetch:0,
 fetchStatus:(force=false)=>{
  const key=account(),now=Date.now()
  if(!key){set({status:null,loaded:false,lastFetch:0});return Promise.resolve()}
  if(!force&&get().loaded&&now-get().lastFetch<60000)return Promise.resolve()
  if(pending?.account===key&&pending.generation===generation)return pending.promise
  const version=generation
  const promise=(async()=>{
   try{
    const response=await apiFetch('/api/freemium/status')
    if(!response.ok)throw new Error('Quota request failed')
    const data:unknown=await response.json()
    if(!validStatus(data))throw new Error('Invalid quota response')
    if(version===generation&&account()===key)set({status:data,loaded:true,lastFetch:Date.now()})
   }catch{if(version===generation&&account()===key)set({status:null,loaded:false,lastFetch:0})}
   finally{if(pending?.account===key&&pending.generation===version)pending=null}
  })()
  pending={account:key,generation:version,promise};return promise
 },
 decrement:(_feature)=>{
  // Attempts/completion/review do not necessarily consume generation quota.
  // Preserve the legacy method contract, but read actual usage instead of guessing.
  void get().fetchStatus(true)
 }
}))
useAuthStore.subscribe(()=>{
 const next=account()
 if(next===activeAccount)return
 activeAccount=next;generation++;pending=null
 useFreemiumStore.setState({status:null,loaded:false,lastFetch:0})
})
