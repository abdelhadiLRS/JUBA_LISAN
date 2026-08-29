'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import {
  BarChart3,
  BookMarked,
  BookOpen,
  ClipboardCheck,
  GraduationCap,
  Headphones,
  HelpCircle,
  Home,
  Layers,
  Map,
  Menu,
  MessageCircle,
  MessageSquare,
  MessageSquarePlus,
  Settings,
  Shield,
  X,
  type LucideIcon,
} from 'lucide-react'
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

const NAV_ICONS: Record<string, LucideIcon> = {
  '/dashboard': Home,
  '/plan': Map,
  '/progress': BarChart3,
  '/flashcards': Layers,
  '/chat': MessageCircle,
  '/listening': Headphones,
  '/reading': BookOpen,
  '/conversation': MessageCircle,
  '/assessment': ClipboardCheck,
  '/grammar': BookMarked,
  '/vocabulary': GraduationCap,
  '/phrasebook': MessageSquare,
  '/settings': Settings,
  '/faq': HelpCircle,
  '/feedback': MessageSquarePlus,
  '/admin': Shield,
}

// Primary destinations surfaced in the mobile bottom navigation.
const BOTTOM_NAV_HREFS = [
  '/dashboard',
  '/plan',
  '/flashcards',
  '/chat',
  '/progress',
]

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const tNav = useTranslations('nav')
  const tCommon = useTranslations('common')
  const tBilling = useTranslations('billing')
  const pathname = usePathname()

  const mainNavItems = [
    { href: '/dashboard', label: tNav('home') },
    { href: '/plan', label: tNav('myPlan') },
    { href: '/progress', label: tNav('progress') },
    { href: '/flashcards', label: tNav('flashcards') },
    { href: '/chat', label: tNav('tutor') },
    { href: '/listening', label: tNav('listening') },
    { href: '/reading', label: tNav('reading') },
    { href: '/conversation', label: tNav('conversation') },
    { href: '/assessment', label: tNav('assessment') },
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
  const user = useAuthStore((s) => s.user)
  const accessToken = useAuthStore((s) => s.accessToken)
  const setTokens = useAuthStore((s) => s.setTokens)
  const setUser = useAuthStore((s) => s.setUser)
  const logout = useAuthStore((s) => s.logout)
  const handleLogout = useLogout()
  const [initializing, setInitializing] = useState(true)
  const loadConfig = useConfigStore((s) => s.load)
  const [logoutConfirm, setLogoutConfirm] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [resourcesOpen, setResourcesOpen] = useState(false)
  const [contactOpen, setContactOpen] = useState(false)
  const [resendSent, setResendSent] = useState(false)
  const [feedbackUnreadCount, setFeedbackUnreadCount] = useState(0)

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

        if (me.learning_goals === null) {
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
    // Stripe trial countdown
    if (
      user?.subscription_status === 'trialing' &&
      user?.subscription_ends_at &&
      stripeEnabled
    ) {
      const days = Math.max(
        1,
        Math.ceil(
          (new Date(user.subscription_ends_at).getTime() - Date.now()) /
            (1000 * 60 * 60 * 24)
        )
      )
      setTrialDaysLeft(days)
      return
    }
    // Freemium trial countdown
    if (
      user?.freemium_trial_ends_at &&
      stripeEnabled &&
      user?.subscription_status !== 'active' &&
      user?.subscription_status !== 'trialing'
    ) {
      const end = new Date(user.freemium_trial_ends_at)
      if (end > new Date()) {
        const days = Math.max(
          1,
          Math.ceil((end.getTime() - Date.now()) / (1000 * 60 * 60 * 24))
        )
        setTrialDaysLeft(days)
        return
      }
    }
    setTrialDaysLeft(0)
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
    window.addEventListener('freelingo:feedback-read', loadFeedbackUnreadCount)
    return () => {
      window.removeEventListener(
        'freelingo:feedback-read',
        loadFeedbackUnreadCount
      )
    }
  }, [initializing])

  if (initializing) {
    return (
      <PageLoading
        label={tCommon('initializing')}
        minHeight="min-h-screen"
        className="bg-fl-bg"
      />
    )
  }

  const feedbackBadgeText =
    feedbackUnreadCount > 99
      ? '99+'
      : feedbackUnreadCount > 0
        ? String(feedbackUnreadCount)
        : ''

  const isActive = (href: string) =>
    pathname === href || pathname.startsWith(href + '/')

  const navLinkClass = (active: boolean, inset = false) =>
    `flex items-center gap-3 rounded-xl ${
      inset ? 'py-2.5 ps-8 pe-4' : 'px-3.5 py-2.5'
    } text-sm font-medium transition-colors ${
      active
        ? 'bg-[var(--juba-primary-soft)] text-[var(--juba-primary-dark)]'
        : 'text-[var(--juba-muted)] hover:bg-[var(--juba-surface-soft)] hover:text-[var(--juba-text)]'
    }`

  const renderNavIcon = (
    href: string,
    active: boolean,
    className = 'h-[18px] w-[18px]'
  ) => {
    const Icon = NAV_ICONS[href] ?? Layers
    return (
      <Icon
        className={`${className} ${active ? 'text-[var(--juba-primary)]' : 'text-[var(--juba-muted)]'}`}
        aria-hidden="true"
      />
    )
  }

  const bottomMobileItems = mainNavItems.filter((item) =>
    BOTTOM_NAV_HREFS.includes(item.href)
  )

  return (
    <div className="bg-fl-bg flex min-h-screen md:h-screen md:overflow-hidden">
      {/* Sidebar (desktop) */}
      <aside className="border-fl-border bg-fl-bg hidden w-60 shrink-0 flex-col border-e md:flex">
        {/* Logo area */}
        <div className="border-fl-border flex items-center gap-2.5 border-b px-5 py-5">
          <span
            className="flex h-7 w-7 items-center justify-center rounded-lg text-xs font-black text-white"
            style={{ background: 'var(--juba-primary)' }}
            aria-hidden="true"
          >
            JL
          </span>
          <span className="text-fl-fg text-sm font-bold tracking-wide">
            JUBA LISAN
          </span>
        </div>

        {/* Language switcher */}
        <div className="border-fl-border border-b">
          <LanguageSwitcher />
        </div>

        {/* Nav */}
        <nav
          className="flex-1 space-y-1 overflow-y-auto px-3 py-4"
          aria-label="Main"
        >
          {/* Main items */}
          {mainNavItems.map((item) => {
            const active = isActive(item.href)
            return (
              <Link
                key={item.href}
                href={item.href}
                className={navLinkClass(active)}
                aria-current={active ? 'page' : undefined}
              >
                {renderNavIcon(item.href, active)}
                <span className="truncate">{item.label}</span>
                {showPremiumBadge && PREMIUM_HREFS.has(item.href) && (
                  <span
                    className="ms-auto text-xs"
                    style={{ color: 'var(--juba-warm)' }}
                    title="Premium"
                  >
                    ★
                  </span>
                )}
              </Link>
            )
          })}

          {/* Resources group */}
          <div className="pt-2">
            <button
              onClick={() => setResourcesOpen((o) => !o)}
              className="text-fl-muted-3 hover:text-fl-fg flex w-full items-center justify-between rounded-xl px-3.5 py-2 text-xs font-semibold tracking-wide uppercase transition-colors"
              aria-expanded={resourcesOpen}
            >
              <span>{tNav('resources')}</span>
              <span aria-hidden="true">{resourcesOpen ? '▴' : '▾'}</span>
            </button>
            {resourcesOpen &&
              resourceNavItems.map((item) => {
                const active = isActive(item.href)
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={navLinkClass(active, true)}
                    aria-current={active ? 'page' : undefined}
                  >
                    {renderNavIcon(item.href, active, 'h-4 w-4')}
                    <span className="truncate">{item.label}</span>
                  </Link>
                )
              })}
          </div>

          {/* Bottom items */}
          <div className="border-fl-border mt-2 space-y-1 border-t pt-3">
            {bottomNavItems.map((item) => {
              const active = isActive(item.href)
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={navLinkClass(active)}
                  aria-current={active ? 'page' : undefined}
                >
                  {renderNavIcon(item.href, active)}
                  <span className="truncate">{item.label}</span>
                  {item.href === '/feedback' && feedbackBadgeText && (
                    <span className="ms-auto flex h-5 min-w-5 items-center justify-center rounded-full bg-red-600 px-1 text-[10px] leading-none font-bold text-white">
                      {feedbackBadgeText}
                    </span>
                  )}
                </Link>
              )
            })}

            {user?.role === 'admin' && (
              <Link
                href="/admin"
                className={navLinkClass(isActive('/admin'))}
                aria-current={isActive('/admin') ? 'page' : undefined}
              >
                {renderNavIcon('/admin', isActive('/admin'))}
                <span className="truncate">{tNav('admin')}</span>
              </Link>
            )}
          </div>
        </nav>

        {/* User + logout */}
        <div className="border-fl-border border-t px-5 py-4">
          <div className="mb-3 flex items-center gap-3">
            <div className="border-fl-border h-9 w-9 flex-shrink-0 overflow-hidden rounded-full border">
              {user?.avatar ? (
                <AuthAvatarImage
                  avatar={user.avatar}
                  alt=""
                  width={36}
                  height={36}
                  className="h-full w-full object-cover"
                  fallback={
                    <div className="bg-fl-surface-2 flex h-full w-full items-center justify-center">
                      <span className="text-fl-muted-1 text-xs font-semibold select-none">
                        {(user?.displayName ||
                          user?.username ||
                          '?')[0].toUpperCase()}
                      </span>
                    </div>
                  }
                />
              ) : (
                <div className="bg-fl-surface-2 flex h-full w-full items-center justify-center">
                  <span className="text-fl-muted-1 text-xs font-semibold select-none">
                    {(user?.displayName ||
                      user?.username ||
                      '?')[0].toUpperCase()}
                  </span>
                </div>
              )}
            </div>
            <div className="min-w-0">
              <p className="text-fl-fg truncate text-sm font-semibold">
                {user?.displayName || user?.username}
              </p>
              <p className="text-fl-muted-3 truncate text-xs">
                @{user?.username?.toLowerCase()}
              </p>
              {trialDaysLeft > 0 && (
                <p
                  className="truncate text-xs font-medium"
                  style={{ color: 'var(--juba-warm)' }}
                >
                  ★ {tBilling('trialDays', { days: trialDaysLeft })}
                </p>
              )}
            </div>
          </div>
          <p className="text-fl-muted-4 mb-2 text-[11px] tracking-wide">
            v1.8.41
          </p>
          <div className="flex items-center gap-4">
            <button
              onClick={() => setContactOpen(true)}
              className="text-fl-muted-2 hover:text-fl-fg text-xs font-medium transition-colors"
            >
              {tNav('contact')}
            </button>
            <button
              onClick={() => setLogoutConfirm(true)}
              className="text-fl-muted-2 hover:text-fl-fg text-xs font-medium transition-colors"
            >
              {tCommon('logout')}
            </button>
          </div>
        </div>
      </aside>

      {/* Mobile top bar */}
      <div className="border-fl-border bg-fl-bg fixed top-0 right-0 left-0 z-50 border-b md:hidden">
        <div className="flex items-center justify-between px-4 py-3">
          <span className="text-fl-fg flex items-center gap-2 text-sm font-bold tracking-wide">
            <span
              className="flex h-6 w-6 items-center justify-center rounded-md text-[10px] font-black text-white"
              style={{ background: 'var(--juba-primary)' }}
              aria-hidden="true"
            >
              JL
            </span>
            JUBA LISAN
          </span>
          <button
            onClick={() => setMobileMenuOpen((o) => !o)}
            className="text-fl-muted-2 hover:text-fl-fg p-1 transition-colors"
            aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={mobileMenuOpen}
          >
            {mobileMenuOpen ? (
              <X className="h-5 w-5" aria-hidden="true" />
            ) : (
              <Menu className="h-5 w-5" aria-hidden="true" />
            )}
          </button>
        </div>

        {/* Dropdown */}
        {mobileMenuOpen && (
          <nav className="border-fl-border bg-fl-bg max-h-[calc(100svh-3.5rem)] space-y-1 overflow-y-auto overscroll-contain border-t px-3 pb-4">
            <div className="border-fl-border -mx-3 mb-2 border-b">
              <LanguageSwitcher />
            </div>
            {mainNavItems.map((item) => {
              const active = isActive(item.href)
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={navLinkClass(active)}
                  aria-current={active ? 'page' : undefined}
                >
                  {renderNavIcon(item.href, active)}
                  <span className="truncate">{item.label}</span>
                  {showPremiumBadge && PREMIUM_HREFS.has(item.href) && (
                    <span
                      className="ms-auto text-xs"
                      style={{ color: 'var(--juba-warm)' }}
                    >
                      ★
                    </span>
                  )}
                </Link>
              )
            })}

            {/* Resources group (mobile) */}
            <div>
              <button
                onClick={() => setResourcesOpen((o) => !o)}
                className="text-fl-muted-3 hover:text-fl-muted-2 flex w-full items-center justify-between rounded-xl px-3.5 py-2 text-xs font-semibold tracking-wide uppercase transition-colors"
                aria-expanded={resourcesOpen}
              >
                <span>{tNav('resources')}</span>
                <span aria-hidden="true">{resourcesOpen ? '▴' : '▾'}</span>
              </button>
              {resourcesOpen &&
                resourceNavItems.map((item) => {
                  const active = isActive(item.href)
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={navLinkClass(active, true)}
                      aria-current={active ? 'page' : undefined}
                    >
                      {renderNavIcon(item.href, active, 'h-4 w-4')}
                      <span className="truncate">{item.label}</span>
                    </Link>
                  )
                })}
            </div>

            {/* Bottom items (mobile) */}
            <div className="border-fl-border space-y-1 border-t pt-2">
              {bottomNavItems.map((item) => {
                const active = isActive(item.href)
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className={navLinkClass(active)}
                    aria-current={active ? 'page' : undefined}
                  >
                    {renderNavIcon(item.href, active)}
                    <span className="truncate">{item.label}</span>
                    {item.href === '/feedback' && feedbackBadgeText && (
                      <span className="ms-auto flex h-5 min-w-5 items-center justify-center rounded-full bg-red-600 px-1 text-[10px] leading-none font-bold text-white">
                        {feedbackBadgeText}
                      </span>
                    )}
                  </Link>
                )
              })}

              {user?.role === 'admin' && (
                <Link
                  href="/admin"
                  onClick={() => setMobileMenuOpen(false)}
                  className={navLinkClass(isActive('/admin'))}
                  aria-current={isActive('/admin') ? 'page' : undefined}
                >
                  {renderNavIcon('/admin', isActive('/admin'))}
                  <span className="truncate">{tNav('admin')}</span>
                </Link>
              )}
            </div>

            <div className="border-fl-border mt-2 border-t pt-3">
              <div className="mb-2 flex items-center gap-3">
                <div className="border-fl-border h-8 w-8 flex-shrink-0 overflow-hidden rounded-full border">
                  {user?.avatar ? (
                    <AuthAvatarImage
                      avatar={user.avatar}
                      alt=""
                      width={32}
                      height={32}
                      className="h-full w-full object-cover"
                      fallback={
                        <div className="bg-fl-surface-2 flex h-full w-full items-center justify-center">
                          <span className="text-fl-muted-1 text-xs font-semibold select-none">
                            {(user?.displayName ||
                              user?.username ||
                              '?')[0].toUpperCase()}
                          </span>
                        </div>
                      }
                    />
                  ) : (
                    <div className="bg-fl-surface-2 flex h-full w-full items-center justify-center">
                      <span className="text-fl-muted-1 text-xs font-semibold select-none">
                        {(user?.displayName ||
                          user?.username ||
                          '?')[0].toUpperCase()}
                      </span>
                    </div>
                  )}
                </div>
                <div className="min-w-0">
                  <p className="text-fl-fg truncate text-sm font-semibold">
                    {user?.displayName || user?.username}
                  </p>
                  <p className="text-fl-muted-3 truncate text-xs">
                    @{user?.username?.toLowerCase()}
                  </p>
                </div>
              </div>
              {trialDaysLeft > 0 && (
                <p
                  className="mb-2 text-xs font-medium"
                  style={{ color: 'var(--juba-warm)' }}
                >
                  ★ {tBilling('trialDays', { days: trialDaysLeft })}
                </p>
              )}
              <p className="text-fl-muted-4 mb-2 text-[11px] tracking-wide">
                v1.8.41
              </p>
              <div className="flex items-center gap-4">
                <button
                  onClick={() => {
                    setMobileMenuOpen(false)
                    setContactOpen(true)
                  }}
                  className="text-fl-muted-2 hover:text-fl-fg text-xs font-medium transition-colors"
                >
                  {tNav('contact')}
                </button>
                <button
                  onClick={() => {
                    setMobileMenuOpen(false)
                    setLogoutConfirm(true)
                  }}
                  className="text-fl-muted-2 hover:text-fl-fg text-xs font-medium transition-colors"
                >
                  {tCommon('logout')}
                </button>
              </div>
            </div>
          </nav>
        )}
      </div>

      {/* Main */}
      <main className="flex min-h-[100dvh] flex-1 flex-col overflow-hidden pt-14 md:min-h-screen md:pt-0">
        {/* Email verification banner */}
        {user && user.is_verified === false && (
          <div className="border-fl-border bg-fl-surface flex flex-wrap items-center gap-x-4 gap-y-1 border-b px-4 py-2">
            <span className="text-fl-muted-1 text-xs">
              ● {tCommon('verifyEmailBanner')}
            </span>
            {resendSent ? (
              <span className="text-fl-muted-2 text-xs">
                {tCommon('verifyEmailSent')}
              </span>
            ) : (
              <button
                onClick={handleResendVerification}
                className="text-fl-accent text-xs font-medium underline transition-all hover:no-underline"
              >
                {tCommon('resendVerification')}
              </button>
            )}
          </div>
        )}
        <div className="min-h-0 flex-1 overflow-y-auto pb-20 md:pb-0">
          {children}
        </div>
      </main>

      {/* Mobile bottom navigation */}
      <nav
        className="border-fl-border bg-fl-surface fixed right-0 bottom-0 left-0 z-50 border-t md:hidden"
        aria-label="Primary"
      >
        <div
          className="mx-auto grid max-w-lg grid-cols-5"
          style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}
        >
          {bottomMobileItems.map((item) => {
            const active = isActive(item.href)
            const Icon = NAV_ICONS[item.href] ?? Layers
            return (
              <Link
                key={item.href}
                href={item.href}
                className="flex flex-col items-center gap-0.5 py-2.5 transition-colors"
                aria-current={active ? 'page' : undefined}
              >
                <Icon
                  className={`h-5 w-5 ${active ? 'text-[var(--juba-primary)]' : 'text-[var(--juba-muted)]'}`}
                  aria-hidden="true"
                />
                <span
                  className={`max-w-full truncate text-[10px] leading-tight ${
                    active
                      ? 'font-semibold text-[var(--juba-primary-dark)]'
                      : 'text-[var(--juba-muted)]'
                  }`}
                >
                  {item.label}
                </span>
              </Link>
            )
          })}
        </div>
      </nav>

      <LoadingBar />

      <ContactFormModal
        open={contactOpen}
        onClose={() => setContactOpen(false)}
      />

      <ConfirmDialog
        open={logoutConfirm}
        title={tCommon('logoutConfirmTitle')}
        message={tCommon('logoutConfirmMessage')}
        confirmLabel={tCommon('logout')}
        onConfirm={handleLogout}
        onCancel={() => setLogoutConfirm(false)}
      />
    </div>
  )
}
