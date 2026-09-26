'use client'

import { useEffect, useRef, useState } from 'react'
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
const NAV_ICONS: Record<string, string> = {
  '/dashboard': 'ti-home', '/plan': 'ti-clipboard-check', '/progress': 'ti-chart-bar',
  '/games': 'ti-device-gamepad-2', '/flashcards': 'ti-cards', '/friends': 'ti-users',
  '/chat': 'ti-message', '/listening': 'ti-headphones', '/reading': 'ti-book',
  '/conversation': 'ti-messages', '/assessment': 'ti-brain', '/coach': 'ti-sparkles',
  '/courses': 'ti-school', '/review': 'ti-refresh', '/translator': 'ti-language',
  '/grammar': 'ti-book-2', '/vocabulary': 'ti-books', '/phrasebook': 'ti-notes',
  '/settings': 'ti-settings', '/faq': 'ti-help', '/feedback': 'ti-message-report',
}
function NavIcon({ href, className = 'icon' }: { href: string; className?: string }) {
  return <i className={'ti ' + (NAV_ICONS[href] ?? 'ti-circle') + ' ' + className} aria-hidden="true" />
}

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const tNav = useTranslations('nav')
  const tCommon = useTranslations('common')
  const tBilling = useTranslations('billing')
  const pathname = usePathname()
  const user = useAuthStore((s) => s.user)
  const isAdmin = user?.role === 'admin'
  const isAdminRoute = pathname === '/admin' || pathname.startsWith('/admin/')

  type NavItem = { href: string; label: string; icon?: string; premium?: boolean }
  type NavGroup = { key: string; label: string; icon: string; items: NavItem[] }

  const mainNavItems: NavItem[] = [
    { href: '/dashboard', label: tNav('home') },
    { href: '/games', label: tNav('games') },
    { href: '/friends', label: tNav('friends') },
  ]

  const navGroups: NavGroup[] = [
    {
      key: 'learning',
      label: 'Learning',
      icon: 'ti-school',
      items: [
        { href: '/plan', label: tNav('myPlan') },
        { href: '/progress', label: tNav('progress') },
        { href: '/courses', label: tNav('courses') },
        { href: '/review', label: tNav('review') },
      ],
    },
    {
      key: 'practice',
      label: 'Practice',
      icon: 'ti-microphone-2',
      items: [
        { href: '/listening', label: tNav('listening'), premium: true },
        { href: '/reading', label: tNav('reading'), premium: true },
        { href: '/conversation', label: tNav('conversation'), premium: true },
        { href: '/assessment', label: tNav('assessment') },
        { href: '/coach', label: tNav('coach') },
        { href: '/chat', label: tNav('tutor'), premium: true },
      ],
    },
    {
      key: 'study-tools',
      label: 'Study tools',
      icon: 'ti-tool',
      items: [
        { href: '/flashcards', label: tNav('flashcards') },
        { href: '/grammar', label: tNav('grammar') },
        { href: '/vocabulary', label: tNav('vocabulary') },
        { href: '/phrasebook', label: tNav('phrasebook') },
        { href: '/translator', label: tNav('translator') },
      ],
    },
  ]

  const bottomNavItems: NavItem[] = [
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
  const [openTopMenu, setOpenTopMenu] = useState<string | null>(null)
  const topMenuRef = useRef<HTMLElement | null>(null)

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

  const isItemActive = (href: string) => pathname === href || pathname.startsWith(href + '/')

  const renderTopItem = (item: NavItem) => {
    const active = isItemActive(item.href)
    const premium = item.premium && showPremiumBadge
    return (
      <Link
        key={item.href}
        href={item.href}
        onClick={() => setOpenTopMenu(null)}
        className={'nav-link d-flex align-items-center gap-2 px-3 py-2 ' + (active ? 'active bg-primary-lt text-primary fw-semibold' : 'text-secondary')}
      >
        <i className={'ti ' + (NAV_ICONS[item.href] ?? 'ti-circle') + ' icon icon-sm'} aria-hidden="true" />
        <span>{item.label}</span>
        {premium && <span className="badge bg-yellow-lt text-yellow ms-1">PRO</span>}
      </Link>
    )
  }

  useEffect(() => {
    const handlePointerDown = (event: PointerEvent) => {
      if (topMenuRef.current && !topMenuRef.current.contains(event.target as Node)) setOpenTopMenu(null)
    }
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpenTopMenu(null)
    }
    document.addEventListener('pointerdown', handlePointerDown)
    document.addEventListener('keydown', handleKeyDown)
    return () => {
      document.removeEventListener('pointerdown', handlePointerDown)
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [])

  const renderTopGroup = (group: NavGroup) => {
    const active = group.items.some((item) => isItemActive(item.href))
    const open = openTopMenu === group.key
    return (
      <div key={group.key} className="nav-item dropdown position-relative">
        <button
          type="button"
          className={'nav-link dropdown-toggle d-flex align-items-center gap-2 border-0 px-3 py-2 ' + (active ? 'text-primary fw-semibold' : 'text-secondary')}
          aria-expanded={open}
          onClick={() => setOpenTopMenu(open ? null : group.key)}
        >
          <i className={'ti ' + group.icon + ' icon icon-sm'} aria-hidden="true" />
          <span>{group.label}</span>
        </button>
        {open && (
          <div className="dropdown-menu show position-absolute start-0 mt-1 p-2" style={{ minWidth: 240 }}>
            {group.items.map(renderTopItem)}
          </div>
        )}
      </div>
    )
  }

  const renderTopNavigation = () => (
    <nav ref={topMenuRef} aria-label="Primary navigation" className="navbar-nav flex-row flex-wrap align-items-center gap-1">
      {mainNavItems.map(renderTopItem)}
      {navGroups.map(renderTopGroup)}
      <div className="vr mx-1 d-none d-xl-block" />
      {bottomNavItems.map(renderTopItem)}
    </nav>
  )

  const activePageLabel = (() => {
    const allItems = [...mainNavItems, ...navGroups.flatMap((group) => group.items), ...bottomNavItems]
    return allItems.find((item) => isItemActive(item.href))?.label ?? 'JUBA LISAN'
  })()

  return (
    <div className="page juba-tabler-app min-h-screen bg-[#f5f7fb]">
      <div className="page-wrapper min-w-0 w-100">
        <header className="navbar navbar-expand-md navbar-light bg-white border-bottom sticky-top">
          <div className="container-fluid flex-nowrap gap-3">
            <Link href="/dashboard" className="navbar-brand d-flex align-items-center gap-2 me-2" onClick={() => setOpenTopMenu(null)}>
              <span className="avatar avatar-sm rounded-2 bg-primary text-white fw-bold">JL</span>
              <span className="fw-bold text-dark">JUBA LISAN</span>
            </Link>
            <div className="flex-fill overflow-visible min-w-0">
              {renderTopNavigation()}
            </div>
            <div className="navbar-nav flex-row align-items-center gap-2 ms-auto">
              <button type="button" className="btn btn-ghost-secondary position-relative" aria-label="Notifications" title="Notifications"><i className="ti ti-bell icon" aria-hidden="true" /></button>
              <LanguageSwitcher />
              <Link href="/settings" title={tNav('settings')} aria-label={tNav('settings')} className="nav-link p-0">
                <span className="avatar avatar-sm rounded-circle bg-azure-lt text-azure fw-bold">
                  {user?.avatar ? <AuthAvatarImage avatar={user.avatar} alt="" width={36} height={36} className="h-full w-full object-cover rounded-circle" fallback={<span>{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>} /> : <span>{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>}
                </span>
              </Link>
              <button type="button" onClick={() => setLogoutConfirm(true)} title={tCommon('logout')} aria-label={tCommon('logout')} className="btn btn-ghost-secondary btn-sm">
                <i className="ti ti-logout icon" aria-hidden="true" />
              </button>
            </div>
          </div>
        </header>
        <div className="bg-white border-bottom">
          <div className="container-fluid py-2 d-flex align-items-center justify-content-between">
            <div>
              <div className="text-uppercase text-secondary small fw-bold">JUBA LISAN</div>
              <div className="fs-3 fw-bold text-dark">{activePageLabel}</div>
            </div>
          </div>
        </div>
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
