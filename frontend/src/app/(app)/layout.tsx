'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { useAuthStore, isSubscribed } from '@/store/auth'
import { useProgressStore } from '@/store/progress'
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
import { Bell, BookOpen, BrainCircuit, ClipboardCheck, Gamepad2, GraduationCap, Headphones, Languages, LogOut, Menu, MessageCircle, MessagesSquare, Settings2, Sparkles, Trophy, UserRound, Users, Volume2, X, PanelLeftClose, PanelLeft } from 'lucide-react'

const NAV_ICONS: Record<string, React.ComponentType<{ className?: string }>> = { '/dashboard': GraduationCap, '/plan': ClipboardCheck, '/progress': Trophy, '/games': Gamepad2, '/flashcards': BookOpen, '/friends': Users, '/chat': MessageCircle, '/listening': Headphones, '/reading': BookOpen, '/conversation': MessagesSquare, '/assessment': BrainCircuit, '/coach': Sparkles, '/courses': GraduationCap, '/review': Volume2, '/translator': Languages, '/grammar': BrainCircuit, '/vocabulary': BookOpen, '/phrasebook': MessagesSquare, '/settings': Settings2, '/faq': UserRound, '/feedback': MessageCircle }
function NavIcon({ href, className = 'size-4' }: { href: string; className?: string }) { const Icon = NAV_ICONS[href] ?? Sparkles; return <Icon className={className} aria-hidden="true" /> }

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const tNav = useTranslations('nav')
  const tCommon = useTranslations('common')
  const tBilling = useTranslations('billing')
  const pathname = usePathname()
  const user = useAuthStore((s) => s.user)
  const isAdmin = user?.role === 'admin'
  const isAdminRoute = pathname === '/admin' || pathname.startsWith('/admin/')

  const mainNavItems = [
    { href: '/dashboard', label: tNav('home') },
    { href: '/plan', label: tNav('myPlan') },
    { href: '/progress', label: tNav('progress') },
    { href: '/games', label: tNav('games') },
    { href: '/flashcards', label: tNav('flashcards') },
    { href: '/friends', label: tNav('friends') },
    { href: '/chat', label: tNav('tutor') },
    { href: '/listening', label: tNav('listening') },
    { href: '/reading', label: tNav('reading') },
    { href: '/conversation', label: tNav('conversation') },
    { href: '/assessment', label: tNav('assessment') },
    { href: '/coach', label: tNav('coach') },
    { href: '/courses', label: tNav('courses') },
    { href: '/review', label: tNav('review') },
    { href: '/translator', label: tNav('translator') },
  ]

  const resourceNavItems = [
    { href: '/grammar', label: tNav('grammar') },
    { href: '/vocabulary', label: tNav('vocabulary') },
    { href: '/phrasebook', label: tNav('phrasebook') },
  ]

  const bottomNavItems = [
    { href: '/settings', label: tNav('settings') },
    { href: '/faq', label: tNav('faq') },
    { href: '/feedback', label: tNav('feedback') },
  ]

  const router = useRouter()
  const xp = useProgressStore((s) => s.xp)
  const accessToken = useAuthStore((s) => s.accessToken)
  const setTokens = useAuthStore((s) => s.setTokens)
  const setUser = useAuthStore((s) => s.setUser)
  const logout = useAuthStore((s) => s.logout)
  const handleLogout = useLogout()
  const [initializing, setInitializing] = useState(true)
  const loadConfig = useConfigStore((s) => s.load)
  const [logoutConfirm, setLogoutConfirm] = useState(false)
  const [contactOpen, setContactOpen] = useState(false)
  const [resendSent, setResendSent] = useState(false)
  const [feedbackUnreadCount, setFeedbackUnreadCount] = useState(0)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  const PREMIUM_HREFS = new Set([
    '/chat',
    '/listening',
    '/reading',
    '/conversation',
  ])
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const showPremiumBadge = stripeEnabled && !isSubscribed(user, stripeEnabled)
  const [trialDaysLeft, setTrialDaysLeft] = useState(0)

  async function handleResendVerification() {
    const res = await apiFetch('/api/auth/resend-verification', {
      method: 'POST',
    })
    if (res.ok) setResendSent(true)
  }

  // On every page load, Zustand is empty. Use the httpOnly refresh cookie
  // to silently get a new access token, then fetch /me to populate the user.
  useEffect(() => {
    async function init() {
      // Load Stripe config once (non-blocking)
      loadConfig()
      try {
        if (!accessToken) {
          const res = await fetch('/api/auth/refresh', {
            method: 'POST',
            credentials: 'include',
          })
          if (!res.ok) {
            logout()
            router.push('/login')
            return
          }
          const { access_token } = await res.json()
          setTokens(access_token)
        }
        // Fetch user info if not already loaded
        const meRes = await apiFetch('/api/auth/me')
        if (!meRes.ok) {
          logout()
          router.push('/login')
          return
        }
        const me = await meRes.json()
        setUser(mapUser(me))

        if (me.learning_goals === null && me.role !== 'admin') {
          router.replace('/onboarding')
          return
        }
      } catch {
        logout()
        router.push('/login')
      } finally {
        setInitializing(false)
      }
    }
    init()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    if (initializing || !isAdmin || isAdminRoute) return
    router.replace('/admin')
  }, [initializing, isAdmin, isAdminRoute, router])

  useEffect(() => {
    const endsAt =
      user?.subscription_status === 'trialing'
        ? user.subscription_ends_at
        : user?.freemium_trial_ends_at

    const shouldCountDown =
      stripeEnabled &&
      Boolean(endsAt) &&
      user?.subscription_status !== 'active'

    if (!shouldCountDown || !endsAt) {
      setTrialDaysLeft(0)
      return
    }

    const update = () => {
      const remainingMs = new Date(endsAt).getTime() - Date.now()
      setTrialDaysLeft(
        remainingMs > 0
          ? Math.max(1, Math.ceil(remainingMs / (1000 * 60 * 60 * 24)))
          : 0
      )
    }

    update()
    const interval = window.setInterval(update, 60 * 1000)
    return () => window.clearInterval(interval)
  }, [
    user?.subscription_status,
    user?.subscription_ends_at,
    user?.freemium_trial_ends_at,
    stripeEnabled,
  ])

  useEffect(() => {
    if (initializing) return

    async function loadFeedbackUnreadCount() {
      try {
        const res = await apiFetch('/api/feedback/unread-summary')
        if (!res.ok) return
        const data = await res.json()
        setFeedbackUnreadCount(data.unread_count ?? 0)
      } catch {
        setFeedbackUnreadCount(0)
      }
    }

    loadFeedbackUnreadCount()
    window.addEventListener('juba:feedback-read', loadFeedbackUnreadCount)
    return () => {
      window.removeEventListener(
        'juba:feedback-read',
        loadFeedbackUnreadCount
      )
    }
  }, [initializing])

  if (initializing || (isAdmin && !isAdminRoute)) {
    return (
      <PageLoading
        label={tCommon('initializing')}
        minHeight="min-h-screen"
        className="bg-fl-bg"
      />
    )
  }

  const pageLabel = [...mainNavItems, ...resourceNavItems, ...bottomNavItems].find((item) => pathname === item.href || pathname.startsWith(item.href + '/'))?.label ?? tNav('home')
  const feedbackBadgeText = feedbackUnreadCount > 0
    ? feedbackUnreadCount > 99
      ? '99+'
      : String(feedbackUnreadCount)
    : ''
  const renderNavItems = (items: typeof mainNavItems) => items.map((item) => {
    const active = pathname === item.href || pathname.startsWith(item.href + '/')
    const premium = showPremiumBadge && PREMIUM_HREFS.has(item.href)
    const isFeedback = item.href === '/feedback'
    return (
      <Link key={item.href} href={item.href} onClick={() => setSidebarOpen(false)} aria-current={active ? 'page' : undefined}
        title={sidebarCollapsed ? item.label : undefined} className={`group flex min-h-11 items-center ${sidebarCollapsed ? 'justify-center px-0' : 'gap-3 px-3'} rounded-xl py-2.5 text-[13px] font-semibold transition ${active ? 'bg-[#7776df] text-white shadow-sm' : 'text-white/65 hover:bg-white/[0.07] hover:text-white'}`}>
        <span className="relative grid size-5 shrink-0 place-items-center"><NavIcon href={item.href} className="size-[18px]" />
          {premium && <Sparkles className="absolute -right-1 -top-1 size-2.5 text-[#ffcf67]" />}
        </span>
        {!sidebarCollapsed && <span className="min-w-0 flex-1 truncate">{item.label}</span>}
        {isFeedback && feedbackBadgeText && <span className="rounded-full bg-[#f26b69] px-2 py-0.5 text-[9px] font-black text-white">{feedbackBadgeText}</span>}
      </Link>
    )
  })

  return (
    <div className="juba-member-shell min-h-screen bg-[#f1f1f5] p-0">
      {sidebarOpen && <button type="button" aria-label={'Close menu'} onClick={() => setSidebarOpen(false)} className="fixed inset-0 z-[60] bg-black/45 backdrop-blur-[2px] lg:hidden" />}
      <div className="flex min-h-screen">
        <aside className={`fixed inset-y-0 left-0 z-[70] flex ${sidebarCollapsed ? 'w-[84px]' : 'w-[276px]'} shrink-0 flex-col bg-[#24272b] text-white shadow-2xl transition-[width,transform] duration-300 ease-out lg:sticky lg:top-0 lg:h-screen lg:translate-x-0 lg:shadow-none ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
          <div className={`flex h-[82px] shrink-0 items-center ${sidebarCollapsed ? 'justify-center px-2' : 'justify-between px-5'} border-b border-white/[0.08]`}>
            <Link href="/dashboard" onClick={() => setSidebarOpen(false)} className="flex items-center gap-3">
              <span className="grid size-11 place-items-center rounded-2xl bg-[#7776df] shadow-inner shadow-white/20"><span className="text-lg font-black">JL</span></span>
              {!sidebarCollapsed && <span className="text-[17px] font-black tracking-[-.04em]">JUBA LISAN</span>}
            </Link>
            <button type="button" onClick={() => setSidebarOpen(false)} className="grid size-9 place-items-center rounded-xl text-white/55 hover:bg-white/10 hover:text-white lg:hidden" aria-label={'Close menu'}><X className="size-4" /></button>
            <button type="button" onClick={() => setSidebarCollapsed((value) => !value)} className="hidden size-9 shrink-0 place-items-center rounded-xl text-white/55 transition hover:bg-white/10 hover:text-white lg:grid" aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'} title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}>{sidebarCollapsed ? <PanelLeft className="size-4" /> : <PanelLeftClose className="size-4" />}</button>
          </div>
          <nav aria-label="Main navigation" className={`min-h-0 flex-1 overflow-y-auto ${sidebarCollapsed ? 'px-2' : 'px-3'} py-5`}>
            {!sidebarCollapsed && <p className="mb-3 px-3 text-[9px] font-black uppercase tracking-[.2em] text-white/30">{'MENU'}</p>}
            <div className="space-y-1">{renderNavItems(mainNavItems)}</div>
            <div className="my-5 border-t border-white/[0.09]" />
            {!sidebarCollapsed && <p className="mb-3 px-3 text-[9px] font-black uppercase tracking-[.2em] text-white/30">{tNav('resources')}</p>}
            <div className="space-y-1">{renderNavItems(resourceNavItems)}</div>
            <div className="my-5 border-t border-white/[0.09]" />
            <div className="space-y-1">{renderNavItems(bottomNavItems)}</div>
          </nav>
          <div className={`shrink-0 border-t border-white/[0.09] ${sidebarCollapsed ? 'p-2' : 'p-4'}`}>
            <div className={`mb-3 flex items-center ${sidebarCollapsed ? 'justify-center' : 'justify-between gap-2'} rounded-xl bg-white/[0.06] p-2`}>
              <div className="flex min-w-0 items-center gap-2">
                <div className="grid size-9 shrink-0 place-items-center overflow-hidden rounded-full bg-[#d8c9a9] text-[#25272b]">
                  {user?.avatar ? <AuthAvatarImage avatar={user.avatar} alt="" width={36} height={36} className="h-full w-full object-cover" fallback={<span className="text-xs font-black">{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>} /> : <span className="text-xs font-black">{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>}
                </div>
                {!sidebarCollapsed && <div className="min-w-0"><p className="truncate text-xs font-bold text-white">{user?.displayName || user?.username || 'Learner'}</p><p className="truncate text-[10px] text-white/40">{user?.email || ''}</p></div>}
              </div>
              {!sidebarCollapsed && <Link href="/settings" onClick={() => setSidebarOpen(false)} aria-label={tNav('settings')} className="grid size-8 shrink-0 place-items-center rounded-lg text-white/55 hover:bg-white/10 hover:text-white"><Settings2 className="size-4" /></Link>}
            </div>
            <div className={`flex items-center ${sidebarCollapsed ? 'flex-col gap-2' : 'justify-between gap-2'}`}>
              {!sidebarCollapsed && <LanguageSwitcher />}
              <button type="button" onClick={() => setLogoutConfirm(true)} title={tCommon('logout')} aria-label={tCommon('logout')} className={`flex h-9 items-center ${sidebarCollapsed ? 'w-full justify-center px-0' : 'gap-2 px-3'} rounded-xl text-[11px] font-bold text-white/55 transition hover:bg-white/10 hover:text-white`}><LogOut className="size-4" />{!sidebarCollapsed && <span>{tCommon('logout')}</span>}</button>
            </div>
          </div>
        </aside>
        <div className="min-w-0 flex-1">
          <header className="flex h-[70px] items-center justify-between gap-3 border-b border-black/[0.06] bg-[#f6f6f4] px-4 sm:px-7">
            <div className="flex min-w-0 items-center gap-3">
              <button type="button" onClick={() => setSidebarOpen(true)} aria-label={'MENU'} className="grid size-10 shrink-0 place-items-center rounded-xl border border-black/[0.08] bg-white text-[#24272b] shadow-sm transition hover:bg-[#f0efff] lg:hidden"><Menu className="size-5" /></button>
              <div className="min-w-0"><p className="text-[9px] font-black uppercase tracking-[.16em] text-[#7776df]">JUBA LISAN</p><h1 className="truncate text-base font-extrabold text-[#24272b] sm:text-lg">{pageLabel}</h1></div>
            </div>
            <div className="flex shrink-0 items-center gap-2">
              <button type="button" className="relative grid size-10 place-items-center rounded-full border border-black/[0.07] bg-white text-[#777986] transition hover:bg-[#f0efff]" aria-label="Notifications" title="Notifications"><Bell className="size-4" /><span className="absolute right-2 top-2 size-1.5 rounded-full bg-[#f26b69]" /></button>
              <Link href="/settings" title={tNav('settings')} aria-label={tNav('settings')} className="grid size-10 place-items-center overflow-hidden rounded-full border border-black/[0.08] bg-white">
                <div className="grid size-9 place-items-center overflow-hidden rounded-full bg-[#d8c9a9] text-[#25272b]">
                  {user?.avatar ? <AuthAvatarImage avatar={user.avatar} alt="" width={36} height={36} className="h-full w-full object-cover" fallback={<span className="text-xs font-black">{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>} /> : <span className="text-xs font-black">{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>}
                </div>
              </Link>
            </div>
          </header>
          <main className="juba-app-content min-h-0 bg-[#f6f6f4]">
            {user && user.is_verified === false && (
              <div className="flex flex-wrap items-center gap-x-4 gap-y-1 border-b border-black/5 bg-[#fff8e8] px-4 py-2">
                <span className="text-xs font-bold text-black/55">● {tCommon('verifyEmailBanner')}</span>
                {resendSent ? <span className="text-xs text-black/45">{tCommon('verifyEmailSent')}</span> : <button onClick={handleResendVerification} className="text-xs font-bold text-[#5f5ec5] underline">{tCommon('resendVerification')}</button>}
              </div>
            )}
            <div className="juba-app-page">{children}</div>
          </main>
        </div>
      </div>
      <LoadingBar />
      <ContactFormModal open={contactOpen} onClose={() => setContactOpen(false)} />
      <ConfirmDialog open={logoutConfirm} title={tCommon('logoutConfirmTitle')} message={tCommon('logoutConfirmMessage')} confirmLabel={tCommon('logout')} onConfirm={handleLogout} onCancel={() => setLogoutConfirm(false)} />
    </div>
  )
}
