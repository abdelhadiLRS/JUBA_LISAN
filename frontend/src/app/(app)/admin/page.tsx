'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { AlertTriangle, Bug, MessageSquareText, ShieldAlert, Star, Ticket, UserPlus, Users, ChevronRight } from 'lucide-react'
import { AdminNav } from '@/components/admin/AdminNav'
import { AdminBadge, AdminMetric, AdminPageHeader, AdminPanel } from '@/components/admin/AdminShell'
import { apiFetch } from '@/lib/api'
import { useConfigStore } from '@/store/config'

interface AdminOverviewStats{users_total:number;users_active:number;users_inactive:number;subscriptions_active:number;subscriptions_trialing:number;subscriptions_past_due:number;feedback_total:number;feedback_pending:number;feedback_bug_pending:number;reviews_pending:number}
const actions=[{href:'/admin/users',key:'manageUsers',descriptionKey:'manageUsersDesc',icon:Users},{href:'/admin/users?create=1',key:'createUser',descriptionKey:'createUserDesc',icon:UserPlus},{href:'/admin/feedback',key:'reviewFeedback',descriptionKey:'reviewFeedbackDesc',icon:MessageSquareText},{href:'/admin/reviews',key:'reviewReviews',descriptionKey:'reviewReviewsDesc',icon:Star}] as const
function ratio(value:number,total:number){return total>0?Math.max(0,Math.min(100,Math.round(value/total*100))):0}
export default function AdminOverviewPage(){
  const t=useTranslations('admin')
  const tCommon=useTranslations('common')
  const maintenanceMode=useConfigStore(s=>s.maintenanceMode)
  const [stats,setStats]=useState<AdminOverviewStats|null>(null)
  const [loadingStats,setLoadingStats]=useState(true)
  const [statsError,setStatsError]=useState('')
  const [reload,setReload]=useState(0)
  useEffect(()=>{
    let cancelled=false
    async function loadStats(){
      setLoadingStats(true);setStatsError('')
      try{const res=await apiFetch('/api/admin/stats');if(!res.ok)throw new Error();const data=await res.json();if(!cancelled)setStats(data)}catch{if(!cancelled)setStatsError(t('adminStatsError'))}finally{if(!cancelled)setLoadingStats(false)}
    }
    void loadStats();return ()=>{cancelled=true}
  },[t,reload])
  const activePct=ratio(stats?.users_active??0,stats?.users_total??0)
  const paidBase=(stats?.subscriptions_active??0)+(stats?.subscriptions_trialing??0)+(stats?.subscriptions_past_due??0)
  const paidPct=ratio((stats?.subscriptions_active??0)+(stats?.subscriptions_trialing??0),paidBase)
  return <div className="juba-page-shell reference-admin-overview">
    <style>{`
      .juba-app-shell .reference-admin-overview{display:flex;flex-direction:column;gap:24px;}
      .juba-app-shell .reference-admin-metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;}
      .juba-app-shell .reference-admin-overview-layout{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:24px;align-items:start;}
      .juba-app-shell .reference-admin-overview-primary{display:flex;flex-direction:column;gap:24px;min-width:0;}
      .juba-app-shell .reference-admin-ratios{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
      .juba-app-shell .reference-admin-ratio{padding:16px;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);}
      .juba-app-shell .reference-admin-ratio>div:first-child{display:flex;justify-content:space-between;gap:8px;font-size:12px;color:var(--juba-muted);margin-block-end:12px;}
      .juba-app-shell .reference-admin-track{height:8px;border-radius:3px;overflow:hidden;background:var(--juba-soft);}
      .juba-app-shell .reference-admin-track>span{display:block;height:100%;background:var(--juba-green);}
      .juba-app-shell .reference-admin-track[data-amber="true"]>span{background:var(--juba-yellow);}
      .juba-app-shell .reference-admin-error{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:12px 16px;border:1px solid var(--duo-red);border-radius:6px;font-size:13px;}
      .juba-app-shell .reference-admin-error button{padding-inline:12px;}
      .juba-app-shell .reference-admin-maintenance{display:flex;align-items:flex-start;gap:12px;padding:16px;border:1px solid var(--juba-border);border-radius:6px;flex-wrap:wrap;}
      .juba-app-shell .reference-admin-maintenance[data-active="true"]{background:oklch(97% .03 90);}
      .juba-app-shell .reference-admin-maintenance>svg{flex:none;color:var(--juba-muted);}
      .juba-app-shell .reference-admin-maintenance>div{flex:1;min-width:160px;}
      .juba-app-shell .reference-admin-maintenance h2{font-size:14px;font-weight:650;margin:0;}
      .juba-app-shell .reference-admin-maintenance p{font-size:13px;line-height:1.6;color:var(--juba-muted);margin:6px 0 0;}
      .juba-app-shell .reference-admin-maintenance a{padding-inline:12px;}
      .juba-app-shell .reference-admin-alert-row,.juba-app-shell .reference-admin-quick-row{display:flex;align-items:center;gap:12px;padding:16px;border-block-end:1px solid var(--juba-border);text-decoration:none;color:var(--juba-ink);}
      .juba-app-shell .reference-admin-alert-row:last-child,.juba-app-shell .reference-admin-quick-row:last-child{border:0;}
      .juba-app-shell .reference-admin-alert-row:hover,.juba-app-shell .reference-admin-quick-row:hover{background:var(--juba-green-soft);}
      .juba-app-shell .reference-admin-alert-row>svg,.juba-app-shell .reference-admin-quick-row>svg{flex:none;color:var(--juba-green-dark);}
      .juba-app-shell .reference-admin-alert-row>div,.juba-app-shell .reference-admin-quick-row>div{flex:1;min-width:0;}
      .juba-app-shell .reference-admin-alert-row strong,.juba-app-shell .reference-admin-quick-row strong{font-size:13px;font-weight:600;}
      .juba-app-shell .reference-admin-alert-row p,.juba-app-shell .reference-admin-quick-row p{font-size:12px;line-height:1.6;color:var(--juba-muted);margin:4px 0 0;}
      .juba-app-shell[dir="rtl"] .reference-admin-quick-row>svg:last-child{transform:scaleX(-1);}
      @media(max-width:1050px){.juba-app-shell .reference-admin-overview-layout{grid-template-columns:1fr;}}
      @media(max-width:640px){.juba-app-shell .reference-admin-overview,.juba-app-shell .reference-admin-overview-primary{gap:16px;}.juba-app-shell .reference-admin-metrics,.juba-app-shell .reference-admin-ratios{grid-template-columns:1fr;}.juba-app-shell .reference-admin-alert-row{flex-wrap:wrap;}}
    `}</style>
    <AdminPageHeader eyebrow={`${t('title')} / ${t('overview')}`} title={t('title')}/><AdminNav/>
    {statsError&&<div className="reference-admin-error" role="alert"><span>{statsError}</span><button className="juba-secondary-button" onClick={()=>setReload(value=>value+1)} disabled={loadingStats}>{tCommon('retry')}</button></div>}
    <div className="reference-admin-metrics" aria-busy={loadingStats}><AdminMetric label={t('users')} value={loadingStats?t('loading'):stats?.users_total??'…'} icon={Users}/><AdminMetric label={t('activeUsers')} value={loadingStats?t('loading'):stats?.users_active??'…'} icon={ShieldAlert}/><AdminMetric label={t('paidAccess')} value={loadingStats?t('loading'):stats?`${stats.subscriptions_active} / ${stats.subscriptions_trialing}`:'…'} icon={Ticket}/><AdminMetric label={t('pendingFeedback')} value={loadingStats?t('loading'):stats?.feedback_pending??'…'} icon={MessageSquareText}/><AdminMetric label={t('pendingReviews')} value={loadingStats?t('loading'):stats?.reviews_pending??'…'} icon={Star}/></div>
    <div className="reference-admin-overview-layout"><div className="reference-admin-overview-primary">
      {stats&&!loadingStats&&<section className="reference-admin-ratios"><div className="reference-admin-ratio"><div><span>{t('activeUsers')}</span><strong>{activePct}%</strong></div><div className="reference-admin-track" role="progressbar" aria-label={t('activeUsers')} aria-valuemin={0} aria-valuemax={100} aria-valuenow={activePct}><span style={{width:activePct+'%'}}/></div></div><div className="reference-admin-ratio"><div><span>{t('paidAccess')}</span><strong>{paidPct}%</strong></div><div className="reference-admin-track" data-amber="true" role="progressbar" aria-label={t('paidAccess')} aria-valuemin={0} aria-valuemax={100} aria-valuenow={paidPct}><span style={{width:paidPct+'%'}}/></div></div></section>}
      <section className="reference-admin-maintenance" data-active={maintenanceMode}><ShieldAlert size={20}/><div><h2>{t('maintenanceTitle')}</h2><p>{maintenanceMode?t('maintenanceOnDesc'):t('maintenanceOffDesc')}</p></div><Link className="juba-secondary-button" href="/admin/system">{t('openSystemControls')}</Link></section>
      <AdminPanel title={t('operationalAlerts')}><Link href="/admin/feedback?status=pending&type=bug" className="reference-admin-alert-row"><Bug size={20}/><div><strong>{t('pendingBugs')}</strong><p>{t('pendingBugsDesc')}</p></div><AdminBadge tone={stats?.feedback_bug_pending?'danger':'neutral'}>{loadingStats?t('loading'):stats?.feedback_bug_pending??'…'}</AdminBadge></Link><Link href="/admin/users?subscription=past_due" className="reference-admin-alert-row"><AlertTriangle size={20}/><div><strong>{t('pastDueSubscriptions')}</strong><p>{t('pastDueSubscriptionsDesc')}</p></div><AdminBadge tone={stats?.subscriptions_past_due?'warning':'neutral'}>{loadingStats?t('loading'):stats?.subscriptions_past_due??'…'}</AdminBadge></Link></AdminPanel>
    </div><aside><AdminPanel title={t('overview')}>{actions.map(({href,key,descriptionKey,icon:Icon})=><Link className="reference-admin-quick-row" href={href} key={href}><Icon size={20}/><div><strong>{t(key)}</strong><p>{t(descriptionKey)}</p></div><ChevronRight size={16} aria-hidden="true"/></Link>)}</AdminPanel></aside></div>
  </div>
}
