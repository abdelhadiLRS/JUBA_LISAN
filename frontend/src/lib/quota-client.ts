import type {User} from '@/store/auth'
export type QuotaSnapshot={remaining:number;limit:number;resets_at:string;period:string;unit:string}
export type AccountQuota={tier:string;metered:boolean;features:Record<string,QuotaSnapshot>}

/** A freshness hint only. The server remains the sole authentication authority. */
export function quotaAccountKey(token:string|null,user:Pick<User,'id'>|null):string|null{
 if(!token)return null
 try{
  const segment=token.split('.')[1]
  if(segment){const padded=segment.replace(/-/g,'+').replace(/_/g,'/').padEnd(Math.ceil(segment.length/4)*4,'=')
   const payload=JSON.parse(atob(padded)) as {sub?:unknown}
   if(typeof payload.sub==='string'||typeof payload.sub==='number')return `account:${payload.sub}`
  }
 }catch{}
 return user?`account:${user.id}`:`token:${token}`
}
export function parseQuotaResponse(value:unknown):AccountQuota{
 if(!value||typeof value!=='object')throw new Error('Invalid quota response')
 const data=value as Record<string,unknown>
 if(!['free','go','plus'].includes(String(data.tier))||typeof data.metered!=='boolean'||!data.features||typeof data.features!=='object'||Array.isArray(data.features))throw new Error('Invalid quota response')
 for(const item of Object.values(data.features)){
  if(!item||typeof item!=='object')throw new Error('Invalid feature quota')
  const q=item as Record<string,unknown>
  for(const field of ['limit','remaining'])if(typeof q[field]!=='number'||!Number.isFinite(q[field])||!Number.isInteger(q[field])||(q[field] as number)<0)throw new Error('Invalid quota count')
  if(typeof q.resets_at!=='string'||!Number.isFinite(Date.parse(q.resets_at))||!['day','week','month'].includes(String(q.period))||!['requests','cards','seconds'].includes(String(q.unit)))throw new Error('Invalid quota period')
 }
 return data as unknown as AccountQuota
}
