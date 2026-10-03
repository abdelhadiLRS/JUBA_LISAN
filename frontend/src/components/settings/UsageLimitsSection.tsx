'use client'
import Link from 'next/link'
import {useLocale,useTranslations} from 'next-intl'
import {useAccountQuota} from '@/hooks/useAccountQuota'

export function UsageLimitsSection({title}:{title?:string}={}){
 const locale=useLocale(),ar=locale.startsWith('ar'),t=useTranslations('settings')
 const {state,failed,refresh}=useAccountQuota('voice')
 const labels:Record<string,string>=ar?{chat:'رسائل المعلم',lessons:'دروس جديدة',reading:'تمارين قراءة جديدة',listening:'تمارين استماع جديدة',flashcards:'بطاقات مولّدة',translation:'الترجمة والتصحيح',voice:'المحادثة الصوتية',tts:'صوت النطق'}:{chat:'Tutor messages',lessons:'New lessons',reading:'New reading exercises',listening:'New listening exercises',flashcards:'Generated cards',translation:'Translation and correction',voice:'Voice conversation',tts:'Pronunciation audio'}
 const number=new Intl.NumberFormat(locale)
 return <section className="rounded-[10px] border border-[var(--duo-line)] bg-[var(--duo-card)] p-6" aria-labelledby="account-usage-title">
  <header className="mb-5 flex flex-wrap items-center justify-between gap-3 border-b border-[var(--duo-line)] pb-4"><h2 id="account-usage-title" className="text-lg font-semibold">{title??t('sectionUsageLimits')}</h2>{state&&<span>{state.tier==='go'?'Go':state.tier==='plus'?'Plus':'Free'}</span>}</header>
  {failed?<div role="alert"><p>{ar?'تعذّر تحديث الاستخدام. لا نعتمد البيانات القديمة لتحديد المتبقي.':'Could not update usage. Previous readings are not treated as current allowance.'}</p><button type="button" className="min-h-11 underline" onClick={()=>void refresh()}>{ar?'إعادة المحاولة':'Retry'}</button></div>:!state?<p role="status">{ar?'جارٍ تحميل حصص الحساب':'Loading account allowances'}</p>:!state.metered?<p>{ar?'الوضع المحلي بلا حصص اشتراك مدفوعة.':'Self-hosted mode has no paid subscription quota enforcement.'}</p>:<>
   <div className="overflow-x-auto"><table className="w-full min-w-[520px] text-sm tabular-nums"><caption className="sr-only">{ar?'الحصص المشتركة بين لغات الحساب':'Allowances shared across account languages'}</caption><thead><tr><th scope="col" className="py-3 text-start">{ar?'الميزة':'Feature'}</th><th scope="col" className="px-3 text-start">{ar?'المتبقي / الحد':'Remaining / limit'}</th><th scope="col" className="py-3 text-start">{ar?'التجديد':'Reset'}</th></tr></thead><tbody>{Object.entries(state.features).map(([feature,q])=><tr key={feature} className="border-t border-[var(--duo-line)]"><th scope="row" className="py-3 text-start font-normal">{labels[feature]||feature}{q.unit==='seconds'&&<span className="block text-xs">{ar?'بالثواني':'in seconds'}</span>}</th><td className="px-3 py-3">{number.format(q.remaining)} / {number.format(q.limit)}</td><td className="py-3">{new Date(q.resets_at).toLocaleString(locale)}</td></tr>)}</tbody></table></div>
   <p className="mt-4 max-w-[70ch] text-sm">{ar?'الحصص مشتركة بين لغات الحساب. الطلبات الجارية تحجز جزءًا من المتبقي مؤقتًا؛ المراجعة لا تستهلك حصة توليد جديدة.':'Allowances are shared across account languages. In-flight requests temporarily reserve availability; review does not consume new generation quota.'}</p>
  </>}
  <Link href="/settings/subscription" className="mt-4 inline-flex min-h-11 items-center underline">{ar?'تفاصيل الباقة والاستخدام':'Plan and usage details'}</Link>
 </section>
}
