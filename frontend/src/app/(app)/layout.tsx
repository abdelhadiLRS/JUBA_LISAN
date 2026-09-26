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
  }, [stripeEnabled, user?.subscription_status, user?.subscription_ends_at, user?.freemium_trial_ends_at])

  const pageLabel = (() => {
    const labels: Record<string, string> = {
      '/dashboard': tNav('home'),
      '/plan': tNav('myPlan'),
      '/progress': tNav('progress'),
      '/games': tNav('games'),
      '/flashcards': tNav('flashcards'),
      '/friends': tNav('friends'),
      '/chat': tNav('tutor'),
      '/listening': tNav('listening'),
      '/reading': tNav('reading'),
      '/conversation': tNav('conversation'),
      '/assessment': tNav('assessment'),
      '/coach': tNav('coach'),
      '/courses': tNav('courses'),
      '/review': tNav('review'),
      '/translator': tNav('translator'),
      '/grammar': tNav('grammar'),
      '/vocabulary': tNav('vocabulary'),
      '/phrasebook': tNav('phrasebook'),
      '/settings': tNav('settings'),
      '/faq': tNav('faq'),
      '/feedback': tNav('feedback'),
    }
    return labels[pathname] ?? 'JUBA LISAN'
  })()

  const renderNavItems = (items: Array<{ href: string; label: string }>) =>
    items.map((item) => {
      const active = pathname === item.href || pathname.startsWith(item.href + '/')
      const premium = PREMIUM_HREFS.has(item.href) && showPremiumBadge
      return (
        <Link
          key={item.href}
          href={item.href}
          onClick={() => setSidebarOpen(false)}
          title={sidebarCollapsed ? item.label : undefined}
          className={'nav-link mb-1 d-flex align-items-center ' + (sidebarCollapsed ? 'justify-content-center ' : '') + (active ? 'active bg-primary-lt text-primary fw-semibold' : 'text-secondary')}
        >
          <NavIcon href={item.href} />
          {!sidebarCollapsed && <span className="ms-2 flex-grow-1">{item.label}</span>}
          {!sidebarCollapsed && premium && <span className="badge bg-yellow-lt text-yellow ms-auto">PRO</span>}
        </Link>
      )
    })

  return (
    <div className="page juba-tabler-app min-h-screen bg-[#f5f7fb]">
      {sidebarOpen && <button type="button" aria-label="Close menu" onClick={() => setSidebarOpen(false)} className="fixed inset-0 z-[60] bg-black/40 lg:hidden" />}
      <aside className={`navbar navbar-vertical navbar-expand-lg fixed inset-y-0 start-0 z-[70] flex-col border-end bg-white transition-[width,transform] duration-200 lg:sticky lg:top-0 lg:h-screen ${sidebarCollapsed ? 'w-[76px]' : 'w-[260px]'} ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
        <div className={`navbar-brand min-h-[64px] border-bottom px-3 ${sidebarCollapsed ? 'justify-center' : ''}`}>
          <Link href="/dashboard" onClick={() => setSidebarOpen(false)} className="d-flex align-items-center gap-2 text-decoration-none text-dark">
            <span className="avatar avatar-sm rounded-2 bg-primary text-white fw-bold">JL</span>
            {!sidebarCollapsed && <span className="fw-bold text-dark">JUBA LISAN</span>}
          </Link>
        </div>
        <div className="navbar-collapse w-100 overflow-hidden">
          <nav aria-label="Primary navigation" className={`navbar-nav pt-3 w-100 ${sidebarCollapsed ? 'px-2' : 'px-3'}`}>
            {!sidebarCollapsed && <div className="mb-2 px-2 text-uppercase text-secondary small fw-bold">Main</div>}
            {renderNavItems(mainNavItems)}
            <div className="my-3 border-top" />
            {!sidebarCollapsed && <div className="mb-2 px-2 text-uppercase text-secondary small fw-bold">{tNav('resources')}</div>}
            {renderNavItems(resourceNavItems)}
            <div className="my-3 border-top" />
            {renderNavItems(bottomNavItems)}
          </nav>
        </div>
        <div className={`mt-auto w-100 border-top p-3 ${sidebarCollapsed ? 'px-2' : ''}`}>
          <div className={`d-flex align-items-center ${sidebarCollapsed ? 'justify-content-center' : 'gap-2'} mb-3`}>
            <span className="avatar avatar-sm rounded-circle bg-azure-lt text-azure fw-bold">
              {user?.avatar ? <AuthAvatarImage avatar={user.avatar} alt="" width={36} height={36} className="h-full w-full object-cover rounded-circle" fallback={<span>{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>} /> : <span>{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>}
            </span>
            {!sidebarCollapsed && <div className="min-w-0"><div className="text-dark small fw-semibold text-truncate">{user?.displayName || user?.username || 'Learner'}</div><div className="text-secondary small text-truncate">{user?.email || ''}</div></div>}
          </div>
          <div className={`d-flex align-items-center ${sidebarCollapsed ? 'flex-column gap-2' : 'justify-content-between gap-2'}`}>
            {!sidebarCollapsed && <LanguageSwitcher />}
            <button type="button" onClick={() => setLogoutConfirm(true)} title={tCommon('logout')} aria-label={tCommon('logout')} className="btn btn-ghost-secondary btn-sm"><LogOut className="icon" />{!sidebarCollapsed && <span className="ms-2">{tCommon('logout')}</span>}</button>
          </div>
        </div>
      </aside>
      <div className="page-wrapper min-w-0">
        <header className="navbar navbar-expand-md navbar-light bg-white border-bottom sticky-top z-50">
          <div className="container-fluid">
            <button type="button" onClick={() => setSidebarOpen(true)} aria-label="MENU" className="btn btn-ghost-secondary d-lg-none me-2"><Menu className="icon" /></button>
            <div className="navbar-nav flex-row order-md-last align-items-center gap-2">
              <button type="button" className="btn btn-ghost-secondary position-relative" aria-label="Notifications" title="Notifications"><Bell className="icon" /></button>
              <Link href="/settings" title={tNav('settings')} aria-label={tNav('settings')} className="nav-link p-0">
                <span className="avatar avatar-sm rounded-circle bg-azure-lt text-azure fw-bold">
                  {user?.avatar ? <AuthAvatarImage avatar={user.avatar} alt="" width={36} height={36} className="h-full w-full object-cover rounded-circle" fallback={<span>{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>} /> : <span>{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>}
                </span>
              </Link>
            </div>
            <div className="navbar-nav me-auto">
              <div className="d-flex flex-column">
                <span className="text-uppercase text-secondary small fw-bold">JUBA LISAN</span>
                <span className="navbar-brand p-0 m-0 fs-3 fw-bold text-dark">{pageLabel}</span>
              </div>
            </div>
            <button type="button" onClick={() => setSidebarCollapsed((value) => !value)} className="btn btn-ghost-secondary d-none d-lg-inline-flex me-2" aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'} title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}>{sidebarCollapsed ? <PanelLeft className="icon" /> : <PanelLeftClose className="icon" />}</button>
          </div>
        </header>
        <main className="page-body bg-[#f5f7fb]">
          {user && user.is_verified === false && (
            <div className="alert alert-warning rounded-0 border-0 border-bottom mb-0 d-flex flex-wrap align-items-center gap-3">
              <span className="fw-semibold">{tCommon('verifyEmailBanner')}</span>
              {resendSent ? <span>{tCommon('verifyEmailSent')}</span> : <button onClick={handleResendVerification} className="btn btn-link p-0">{tCommon('resendVerification')}</button>}
            </div>
          )}
          <div className="container-fluid py-4"><div className="juba-app-page">{children}</div></div>
        </main>
      </div>
      <LoadingBar />
      <ContactFormModal open={contactOpen} onClose={() => setContactOpen(false)} />
      <ConfirmDialog open={logoutConfirm} title={tCommon('logoutConfirmTitle')} message={tCommon('logoutConfirmMessage')} confirmLabel={tCommon('logout')} onConfirm={handleLogout} onCancel={() => setLogoutConfirm(false)} />
    </div>
  )
}
