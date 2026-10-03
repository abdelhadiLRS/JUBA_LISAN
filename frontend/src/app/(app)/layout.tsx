'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { useAuthStore, isSubscribed } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { apiFetch } from '@/lib/api'
import { mapUser } from '@/lib/mappers'
import { useLogout } from '@/hooks/useLogout'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { ContactFormModal } from '@/components/ui/contact-form-modal'
import { LoadingBar } from '@/components/ui/loading-bar'
import { PageLoading } from '@/components/ui/page-loading'
import LanguageSwitcher from '@/components/LanguageSwitcher'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'
import { BookOpen, ChartNoAxesColumnIncreasing, Gamepad2, Headphones, Languages, MessageCircle, Settings, Users, Library, ClipboardCheck, UserRound, Search, Trophy, Sparkles, Menu, X, ChevronDown } from 'lucide-react'
import './reference-dashboard.css'
import './app-layout-fix.css'
import './nunito-local.css'

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const locale = useLocale()
  const dir = locale === 'ar' ? 'rtl' : 'ltr'
  const tNav = useTranslations('nav')
  const tCommon = useTranslations('common')
  const tBilling = useTranslations('billing')
  const pathname = usePathname()
  const router = useRouter()
  const user = useAuthStore(s => s.user)
  const accessToken = useAuthStore(s => s.accessToken)
  const setTokens = useAuthStore(s => s.setTokens)
  const setUser = useAuthStore(s => s.setUser)
  const logout = useAuthStore(s => s.logout)
  const handleLogout = useLogout()
  const loadConfig = useConfigStore(s => s.load)
  const stripeEnabled = useConfigStore(s => s.stripeEnabled)
  const [initializing, setInitializing] = useState(true)
  const [logoutConfirm, setLogoutConfirm] = useState(false)
  const mobileMenuTriggerRef = useRef<HTMLButtonElement>(null)
  const mobileMenuPanelRef = useRef<HTMLElement>(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [resourcesOpen, setResourcesOpen] = useState(false)
  const [contactOpen, setContactOpen] = useState(false)
  const [resendSent, setResendSent] = useState(false)
  const [feedbackUnreadCount, setFeedbackUnreadCount] = useState(0)
  const [trialDaysLeft, setTrialDaysLeft] = useState(0)
  const mainNavItems = [
    { href: '/progress', label: tNav('progress'), icon: ChartNoAxesColumnIncreasing }, { href: '/games', label: tNav('games'), icon: Gamepad2 }, { href: '/flashcards', label: tNav('flashcards'), icon: Library }, { href: '/friends', label: tNav('friends'), icon: Users }, { href: '/chat', label: tNav('tutor'), icon: MessageCircle }, { href: '/listening', label: tNav('listening'), icon: Headphones }, { href: '/reading', label: tNav('reading'), icon: BookOpen }, { href: '/conversation', label: tNav('conversation'), icon: Languages }, { href: '/assessment', label: tNav('assessment'), icon: ClipboardCheck }, { href: '/coach', label: tNav('coach'), icon: Sparkles }, { href: '/review', label: tNav('review'), icon: Trophy }, { href: '/translator', label: tNav('translator'), icon: Search },
  ]
  const resourceNavItems = [{ href: '/grammar', label: tNav('grammar'), icon: BookOpen }, { href: '/vocabulary', label: tNav('vocabulary'), icon: Languages }, { href: '/phrasebook', label: tNav('phrasebook'), icon: Library }]
  const bottomNavItems = [{ href: '/settings', label: tNav('settings'), icon: Settings }, { href: '/faq', label: tNav('faq'), icon: MessageCircle }, { href: '/feedback', label: tNav('feedback'), icon: MessageCircle }]
  const topNavItems = [{ href: '/dashboard', label: tNav('home') }, { href: '/plan', label: tNav('myPlan') }, { href: '/courses', label: tNav('courses') }]
  const PREMIUM_HREFS = new Set(['/chat', '/listening', '/reading', '/conversation'])
  const showPremiumBadge = stripeEnabled && !isSubscribed(user, stripeEnabled)
  const active = (href: string) => pathname === href || pathname.startsWith(href + '/')
  const closeMobileMenu = () => { setMobileMenuOpen(false); setResourcesOpen(false); mobileMenuTriggerRef.current?.focus() }
  async function handleResendVerification() { const res = await apiFetch('/api/auth/resend-verification', { method: 'POST' }); if (res.ok) setResendSent(true) }
  useEffect(() => { async function init() { loadConfig(); try { if (!accessToken) { const res = await fetch('/api/auth/refresh', { method: 'POST', credentials: 'include' }); if (!res.ok) { logout(); router.push('/login'); return } const { access_token } = await res.json(); setTokens(access_token) } const meRes = await apiFetch('/api/auth/me'); if (!meRes.ok) { logout(); router.push('/login'); return } const me = await meRes.json(); setUser(mapUser(me)); if (me.learning_goals === null) router.replace('/onboarding') } catch { logout(); router.push('/login') } finally { setInitializing(false) } } init() }, [])
  useEffect(() => { if (user?.subscription_status === 'trialing' && user?.subscription_ends_at && stripeEnabled) { setTrialDaysLeft(Math.max(1, Math.ceil((new Date(user.subscription_ends_at).getTime() - Date.now()) / 86400000))); return } if (user?.freemium_trial_ends_at && stripeEnabled && user?.subscription_status !== 'active' && user?.subscription_status !== 'trialing') { const end = new Date(user.freemium_trial_ends_at); if (end > new Date()) { setTrialDaysLeft(Math.max(1, Math.ceil((end.getTime() - Date.now()) / 86400000))); return } } setTrialDaysLeft(0) }, [user?.subscription_status, user?.subscription_ends_at, user?.freemium_trial_ends_at, stripeEnabled])
  useEffect(() => { setMobileMenuOpen(false); setResourcesOpen(resourceNavItems.some(item => active(item.href))) }, [pathname])
  useEffect(() => { if (!mobileMenuOpen) return; const panel = mobileMenuPanelRef.current; const getFocusableElements = () => Array.from(panel?.querySelectorAll<HTMLElement>('a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])') ?? []).filter(element => !element.closest('[hidden]') && element.getAttribute('aria-hidden') !== 'true'); getFocusableElements()[0]?.focus(); const handleKeyDown = (event: KeyboardEvent) => { if (event.key === 'Escape') { setMobileMenuOpen(false); setResourcesOpen(false); mobileMenuTriggerRef.current?.focus(); return } if (event.key !== 'Tab') return; const elements = getFocusableElements(); if (!elements.length) { event.preventDefault(); return } const first = elements[0]; const last = elements[elements.length - 1]; if (event.shiftKey && (document.activeElement === first || !panel?.contains(document.activeElement))) { event.preventDefault(); last.focus() } else if (!event.shiftKey && (document.activeElement === last || !panel?.contains(document.activeElement))) { event.preventDefault(); first.focus() } }; const previousOverflow = document.body.style.overflow; document.body.style.overflow = 'hidden'; document.addEventListener('keydown', handleKeyDown); return () => { document.body.style.overflow = previousOverflow; document.removeEventListener('keydown', handleKeyDown) } }, [mobileMenuOpen])
  useEffect(() => { if (initializing) return; async function loadFeedbackUnreadCount() { try { const res = await apiFetch('/api/feedback/unread-summary'); if (!res.ok) return; const data = await res.json(); setFeedbackUnreadCount(data.unread_count ?? 0) } catch { setFeedbackUnreadCount(0) } } loadFeedbackUnreadCount(); window.addEventListener('juba:feedback-read', loadFeedbackUnreadCount); return () => window.removeEventListener('juba:feedback-read', loadFeedbackUnreadCount) }, [initializing])
  const feedbackBadgeText = feedbackUnreadCount > 99 ? '99+' : feedbackUnreadCount > 0 ? String(feedbackUnreadCount) : ''
  const displayName = user?.displayName || user?.username || ''
  const renderAvatar = (size: number) => user?.avatar ? <AuthAvatarImage avatar={user.avatar} alt="" width={size} height={size} className="h-full w-full object-cover" /> : <UserRound size={Math.round(size / 2)} aria-hidden="true" />
  const renderNavLink = (item: typeof mainNavItems[number], mobile = false) => <Link key={item.href} href={item.href} onClick={mobile ? closeMobileMenu : undefined} className={`juba-duo-nav-link ${active(item.href) ? 'is-active' : ''}`} aria-current={active(item.href) ? 'page' : undefined}><item.icon size={18} aria-hidden="true"/><span className="truncate">{item.label}</span>{showPremiumBadge && PREMIUM_HREFS.has(item.href) && <span className="reference-nav-premium" aria-hidden="true">★</span>}{item.href === '/feedback' && feedbackBadgeText && <span className="reference-feedback-badge">{feedbackBadgeText}</span>}</Link>
  const renderUtilityLinks = (mobile = false) => <div className="juba-duo-nav-divider">{bottomNavItems.map(item => renderNavLink(item, mobile))}{user?.role === 'admin' && renderNavLink({ href: '/admin', label: tNav('admin'), icon: Settings }, mobile)}</div>
  const renderResources = (mobile = false) => <div className="reference-resource-group"><button onClick={() => setResourcesOpen(value => !value)} className="juba-duo-resource-toggle" aria-expanded={resourcesOpen} aria-controls={mobile ? 'mobile-resources-menu' : 'desktop-resources-menu'}><span>{tNav('resources')}</span><ChevronDown size={14} className={resourcesOpen ? 'reference-chevron-open' : ''} aria-hidden="true"/></button><div id={mobile ? 'mobile-resources-menu' : 'desktop-resources-menu'} hidden={!resourcesOpen}>{resourceNavItems.map(item => renderNavLink(item, mobile))}</div></div>
  const renderUser = (mobile = false) => <div className="juba-duo-user"><div className="reference-account"><span className="reference-account-avatar">{renderAvatar(32)}</span><div className="reference-account-copy"><p>{displayName}</p><p>@{user?.username?.toLowerCase()}</p></div></div>{trialDaysLeft > 0 && <p className="reference-trial">★ {tBilling('trialDays', { days: trialDaysLeft })}</p>}<p className="juba-duo-version">v1.9.16</p><button onClick={() => { if (mobile) closeMobileMenu(); setContactOpen(true) }} className="juba-duo-user-action">{tNav('contact')}</button><button onClick={() => { if (mobile) closeMobileMenu(); setLogoutConfirm(true) }} className="juba-duo-user-action">{tCommon('logout')}</button></div>
  if (initializing) return <div className="juba-app-shell" dir={dir}><PageLoading label={tCommon('initializing')} minHeight="min-h-[100dvh]" className="bg-[var(--juba-bg)]"/></div>
  return <div className="juba-app-shell" dir={dir}><a className="juba-duo-skip-link" href="#main-content">{locale === 'ar' ? 'تجاوز إلى المحتوى الرئيسي' : 'Skip to main content'}</a><aside className="juba-duo-sidebar" aria-label={tNav('primaryNavigation')}><div className="reference-brand"><span className="juba-duo-logo-mark" aria-hidden="true">JL</span><span>JUBA LISAN</span></div><nav className="juba-duo-nav" aria-label={tNav('primaryNavigation')}>{mainNavItems.map((item, index) => <div key={item.href}>{(index === 0 || index === 1 || index === 5) && <div className="juba-duo-nav-section-label">{index === 0 ? (locale === 'ar' ? 'التعلّم' : 'LEARN') : index === 1 ? (locale === 'ar' ? 'الممارسة' : 'PRACTICE') : (locale === 'ar' ? 'اكتشاف' : 'DISCOVER')}</div>}{renderNavLink(item)}</div>)}{renderResources()}{renderUtilityLinks()}</nav>{renderUser()}</aside><div className="juba-duo-mobile-bar"><span className="juba-duo-mobile-brand">JUBA LISAN</span><button onClick={() => setMobileMenuOpen(value => !value)} ref={mobileMenuTriggerRef} className="juba-duo-mobile-trigger" aria-label={mobileMenuOpen ? (locale === 'ar' ? 'إغلاق القائمة' : 'Close menu') : (locale === 'ar' ? 'فتح القائمة' : 'Open menu')} aria-expanded={mobileMenuOpen} aria-controls="juba-duo-mobile-menu">{mobileMenuOpen ? <X size={20}/> : <Menu size={20}/>}</button></div><nav id="juba-duo-mobile-menu" ref={mobileMenuPanelRef} hidden={!mobileMenuOpen} aria-label={tNav('primaryNavigation')} className="juba-duo-mobile-menu"><LanguageSwitcher/><div className="reference-mobile-primary">{topNavItems.map(item => <Link key={item.href} href={item.href} onClick={closeMobileMenu} aria-current={active(item.href) ? 'page' : undefined}>{item.label}</Link>)}</div>{mainNavItems.map(item => renderNavLink(item, true))}{renderResources(true)}{renderUtilityLinks(true)}{renderUser(true)}</nav><main className="juba-duo-main" id="main-content" aria-label={locale === 'ar' ? 'المحتوى الرئيسي' : 'Main content'} tabIndex={-1}><header className="juba-app-topbar" aria-label={tNav('navigation')}><nav className="juba-app-topnav" aria-label={tNav('primaryNavigation')}>{topNavItems.map(item => <Link key={item.href} href={item.href} className={active(item.href) ? 'is-active' : ''} aria-current={active(item.href) ? 'page' : undefined}>{item.label}</Link>)}</nav><div className="reference-course-control"><LanguageSwitcher/></div><div className="juba-app-topbar-user"><span>{displayName}</span><span className="juba-app-topbar-user-avatar">{renderAvatar(30)}</span></div></header>{user && user.is_verified === false && <div className="reference-verification-banner"><span>{tCommon('verifyEmailBanner')}</span>{resendSent ? <span>{tCommon('verifyEmailSent')}</span> : <button onClick={handleResendVerification}>{tCommon('resendVerification')}</button>}</div>}<div className="juba-duo-page-frame juba-dashboard-workspace" tabIndex={-1} id="app-scroll-region">{children}</div></main><LoadingBar/><ContactFormModal open={contactOpen} onClose={() => setContactOpen(false)}/><ConfirmDialog open={logoutConfirm} title={tCommon('logoutConfirmTitle')} message={tCommon('logoutConfirmMessage')} confirmLabel={tCommon('logout')} onConfirm={handleLogout} onCancel={() => setLogoutConfirm(false)}/></div>
}
