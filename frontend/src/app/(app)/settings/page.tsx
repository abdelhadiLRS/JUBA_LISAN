'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'next/navigation'
import { Bot, CreditCard, Globe2, MessageSquareText, Palette, User, Volume2, LogOut, Trash2 } from 'lucide-react'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { useLogout } from '@/hooks/useLogout'
import { ProfileSection } from '@/components/settings/ProfileSection'
import { ConversationSection } from '@/components/settings/ConversationSection'
import { VoiceSection } from '@/components/settings/VoiceSection'
import { UsageLimitsSection } from '@/components/settings/UsageLimitsSection'
import { AppearanceSection } from '@/components/settings/AppearanceSection'
import { BillingSection } from '@/components/settings/BillingSection'
import { ReviewSection } from '@/components/settings/ReviewSection'
import { SettingsActionCard, SettingsNav, SettingsPageHeader, SettingsPanel } from '@/components/settings/SettingsShell'

export default function SettingsPage(){
  const t=useTranslations('settings')
  const tCommon=useTranslations('common')
  const user=useAuthStore(s=>s.user)
  const logout=useAuthStore(s=>s.logout)
  const router=useRouter()
  const handleLogout=useLogout()
  const [logoutConfirm,setLogoutConfirm]=useState(false)
  const [deleteConfirm,setDeleteConfirm]=useState(false)
  const [deleting,setDeleting]=useState(false)
  const [deleteError,setDeleteError]=useState(false)
  const navItems=[{href:'#account',label:t('sectionAccount'),icon:User},{href:'#preferences',label:t('sectionAppearance'),icon:Palette},{href:'#voice',label:t('sectionConversation'),icon:Volume2},{href:'#plan',label:t('sectionUsageLimits'),icon:CreditCard},{href:'#community',label:t('sectionReview'),icon:MessageSquareText},{href:'#legal',label:t('sectionLegal'),icon:Globe2}]
  async function handleDeleteAccount(){
    setDeleting(true);setDeleteError(false)
    try{await apiFetch('/api/auth/me',{method:'DELETE'});logout();router.push('/login')}catch{setDeleteError(true);setDeleting(false)}
  }
  return <div className="juba-page-shell reference-settings-page">
    <style>{`
      .juba-app-shell .reference-settings-page{display:flex;flex-direction:column;gap:16px;}
      .juba-app-shell .reference-settings-links{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-block-start:8px;}
      .juba-app-shell .reference-settings-session{padding:16px;border:1px solid var(--juba-border);border-radius:6px;background:var(--juba-card);}
      .juba-app-shell .reference-settings-session h3{margin:0 0 16px;font-size:14px;font-weight:650;}
      .juba-app-shell .reference-settings-session-actions{display:flex;flex-wrap:wrap;gap:12px;}
      .juba-app-shell .reference-settings-session-actions button{padding-inline:16px;}
      .juba-app-shell .reference-settings-delete{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:40px;padding:8px 16px;border:1px solid var(--duo-red);border-radius:6px;background:transparent;color:var(--duo-red);font-size:13px;}
      .juba-app-shell .reference-settings-error{padding:12px;border:1px solid var(--duo-red);border-radius:6px;color:var(--duo-red);font-size:13px;margin-block-end:12px;}
      .juba-app-shell .reference-settings-voice{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
      .juba-app-shell .reference-settings-legal{border:1px solid var(--juba-border);border-radius:6px;overflow:hidden;}
      .juba-app-shell .reference-settings-legal a{display:flex;align-items:center;min-height:48px;padding:12px 16px;border-block-end:1px solid var(--juba-border);color:var(--juba-muted);font-size:14px;text-decoration:none;}
      .juba-app-shell .reference-settings-legal a:last-child{border:0;}
      .juba-app-shell .reference-settings-legal a:hover{color:var(--juba-green-dark);background:var(--juba-green-soft);}
      @media(max-width:760px){.juba-app-shell .reference-settings-links,.juba-app-shell .reference-settings-voice{grid-template-columns:1fr;}.juba-app-shell .reference-settings-delete{min-height:44px;}}
    `}</style>
    <SettingsPageHeader eyebrow={`${t('sectionAccount')} / ${t('title')}`} title={t('title')}/>
    <SettingsNav items={navItems}/>
    <div className="reference-settings-links"><SettingsActionCard href="/settings/languages" label={t('languagesManage')} description={t('sectionLanguages')} icon={Globe2}/><SettingsActionCard href="/settings/memories" label={t('memoryManage')} description={t('sectionMemory')} icon={Bot}/></div>
    <SettingsPanel id="account" title={t('sectionAccount')}><ProfileSection title={t('cardProfileAccess')}/><section className="reference-settings-session"><h3>{t('cardSessionSecurity')}</h3>{deleteError&&<p className="reference-settings-error" role="alert">{tCommon('error')}</p>}<div className="reference-settings-session-actions"><button className="juba-secondary-button" onClick={()=>setLogoutConfirm(true)}><LogOut size={16} aria-hidden="true"/>{tCommon('logout')}</button>{user?.role!=='admin'&&<button className="reference-settings-delete" onClick={()=>setDeleteConfirm(true)} disabled={deleting}><Trash2 size={16} aria-hidden="true"/>{t('deleteAccount')}</button>}</div></section></SettingsPanel>
    <SettingsPanel id="preferences" title={t('sectionAppearance')}><AppearanceSection title={t('cardTheme')}/></SettingsPanel>
    <SettingsPanel id="voice" title={t('sectionConversation')}><div className="reference-settings-voice"><ConversationSection title={t('cardConversationTiming')}/><VoiceSection title={t('cardTutorVoice')}/></div></SettingsPanel>
    <SettingsPanel id="plan" title={t('sectionUsageLimits')}><BillingSection/><UsageLimitsSection title={t('cardCurrentUsage')}/></SettingsPanel>
    <SettingsPanel id="community" title={t('sectionReview')}><ReviewSection title={t('cardProductReview')}/></SettingsPanel>
    <SettingsPanel id="legal" title={t('sectionLegal')}><section className="reference-settings-legal" aria-label={t('cardLegalDocuments')}><a href="/terms?from=settings">{t('termsOfService')}</a><a href="/privacy?from=settings">{t('privacyPolicy')}</a></section></SettingsPanel>
    <ConfirmDialog open={logoutConfirm} title={tCommon('logoutConfirmTitle')} message={tCommon('logoutConfirmMessage')} confirmLabel={tCommon('logout')} onConfirm={handleLogout} onCancel={()=>setLogoutConfirm(false)}/>
    <ConfirmDialog open={deleteConfirm} title={t('deleteAccountTitle')} message={t('deleteAccountMessage')} confirmLabel={t('deleteAccountConfirm')} danger onConfirm={handleDeleteAccount} onCancel={()=>setDeleteConfirm(false)}/>
  </div>
}
