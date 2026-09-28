'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useLocale, useTranslations } from 'next-intl'
import { useAuthStore, isSubscribed } from '@/store/auth'
import { useProgressStore } from '@/store/progress'
import { LearningProgressBridge } from '@/components/LearningProgressBridge'
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
import { BookOpen, ChartNoAxesColumnIncreasing, Gamepad2, GraduationCap, Headphones, Languages, MessageCircle, Settings, Users, Library, ClipboardCheck, UserRound, Search, Trophy, Flame, Sparkles } from 'lucide-react'

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const locale = useLocale()
  const dir = locale === 'ar' ? 'rtl' : 'ltr'
  const tNav = useTranslations('nav')
  const tCommon = useTranslations('common')
  const tBilling = useTranslations('billing')
  const pathname = usePathname()

  const mainNavItems = [
    { href: '/dashboard', label: tNav('home'), icon: GraduationCap },
    { href: '/plan', label: tNav('myPlan'), icon: BookOpen },
    { href: '/progress', label: tNav('progress'), icon: ChartNoAxesColumnIncreasing },
    { href: '/games', label: tNav('games'), icon: Gamepad2 },
    { href: '/flashcards', label: tNav('flashcards'), icon: Library },
    { href: '/friends', label: 'Friends', icon: Users },
    { href: '/chat', label: tNav('tutor'), icon: MessageCircle },
    { href: '/listening', label: tNav('listening'), icon: Headphones },
    { href: '/reading', label: tNav('reading'), icon: BookOpen },
    { href: '/conversation', label: tNav('conversation'), icon: Languages },
    { href: '/assessment', label: tNav('assessment'), icon: ClipboardCheck },
    { href: '/coach', label: 'Coach', icon: Sparkles },
    { href: '/courses', label: 'Courses', icon: BookOpen },
    { href: '/review', label: 'Review', icon: Trophy },
    { href: '/translator', label: 'Translator', icon: Search },
  ]

  const resourceNavItems = [
    { href: '/grammar', label: tNav('grammar'), icon: BookOpen },
    { href: '/vocabulary', label: tNav('vocabulary'), icon: Languages },
    { href: '/phrasebook', label: tNav('phrasebook'), icon: Library },
  ]

  const bottomNavItems = [
    { href: '/settings', label: tNav('settings'), icon: Settings },
    { href: '/faq', label: tNav('faq'), icon: MessageCircle },
    { href: '/feedback', label: tNav('feedback'), icon: MessageCircle },
  ]

  const router = useRouter()
  const user = useAuthStore((s) => s.user)
  const xp = useProgressStore((s) => s.xp)
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
    setMobileMenuOpen(false)
    setResourcesOpen(false)
  }, [pathname])

  useEffect(() => {
    if (!mobileMenuOpen) return

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setMobileMenuOpen(false)
        setResourcesOpen(false)
      }
    }

    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    document.addEventListener('keydown', handleEscape)

    return () => {
      document.body.style.overflow = previousOverflow
      document.removeEventListener('keydown', handleEscape)
    }
  }, [mobileMenuOpen])

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

  if (initializing) {
    return (
      <PageLoading
        label={tCommon('initializing')}
        minHeight="min-h-screen"
        className="bg-[var(--duo-bg)]"
      />
    )
  }

  const feedbackBadgeText =
    feedbackUnreadCount > 99
      ? '99+'
      : feedbackUnreadCount > 0
        ? String(feedbackUnreadCount)
        : ''

  return (
    <div className="juba-duo-shell" dir={dir}>
      {/* Sidebar */}
      <aside className="juba-duo-sidebar" aria-label={tNav('navigation')}>
        {/* Logo area */}
        <div className="border-[var(--duo-line)] flex items-center gap-2 border-b px-5 py-5">
          <span className="juba-duo-logo-mark" aria-hidden="true">JL</span>
          <span className="text-[var(--duo-ink)] font-sans text-sm font-bold tracking-widest uppercase">
            JUBA LISAN
          </span>
        </div>

        {/* Language switcher */}
        <div className="juba-duo-language"><LanguageSwitcher /></div>

        {/* Nav */}
        <nav className="juba-duo-nav">
          {/* Main items */}
          {mainNavItems.map((item) => {
            const active =
              pathname === item.href || pathname.startsWith(item.href + '/')
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`juba-duo-nav-link ${active ? 'is-active' : ''}`}
                aria-current={active ? 'page' : undefined}
              >
                <item.icon className={`h-[18px] w-[18px] shrink-0 ${active ? 'text-[var(--duo-green)]' : 'text-[var(--duo-muted)]'}`} />
                {item.label}
                {showPremiumBadge && PREMIUM_HREFS.has(item.href) && (
                  <span className="text-[var(--duo-green)] ms-auto text-xs">★</span>
                )}
              </Link>
            )
          })}

          {/* Resources group */}
          <div className="mt-2">
            <button
              onClick={() => setResourcesOpen((o) => !o)}
              className="juba-duo-resource-toggle"
              aria-expanded={resourcesOpen}
              aria-controls="desktop-resources-menu"
            >
              <span>{tNav('resources')}</span>
              <span className="text-[var(--duo-ink)]">{resourcesOpen ? '▴' : '▾'}</span>
            </button>
            {resourcesOpen &&
              <div id="desktop-resources-menu">{resourceNavItems.map((item) => {
                const active =
                  pathname === item.href || pathname.startsWith(item.href + '/')
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`juba-duo-nav-link juba-duo-nav-link-sub ${active ? 'is-active' : ''}`}
                    aria-current={active ? 'page' : undefined}
                  >
                    <item.icon className="h-[17px] w-[17px] shrink-0" />
                    {item.label}
                  </Link>
                )
              })}</div>}
          </div>

          {/* Bottom items */}
          <div className="juba-duo-nav-divider">
            {bottomNavItems.map((item) => {
              const active =
                pathname === item.href || pathname.startsWith(item.href + '/')
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`juba-duo-nav-link ${active ? 'is-active' : ''}`}
                  aria-current={active ? 'page' : undefined}
                >
                  <item.icon className="h-[17px] w-[17px] shrink-0" />
                  {item.label}
                  {item.href === '/feedback' && feedbackBadgeText && (
                    <span className="ms-auto flex h-6 w-6 shrink-0 -translate-y-0.5 items-center justify-center rounded-full bg-[var(--duo-red)] leading-none font-bold tracking-normal text-white">
                      {feedbackBadgeText}
                    </span>
                  )}
                </Link>
              )
            })}
          </div>

          {user?.role === 'admin' && (
            <Link
              href="/admin"
              className={`juba-duo-nav-link ${pathname.startsWith('/admin') ? 'is-active' : ''}`}
              aria-current={pathname.startsWith('/admin') ? 'page' : undefined}
            >
              <Settings className="h-[17px] w-[17px] shrink-0" />
              {tNav('admin')}
            </Link>
          )}
        </nav>

        {/* User + logout */}
        <div className="juba-duo-user">
          <div className="mb-3 flex items-center gap-3">
            <div className="border-[var(--duo-line)] h-8 w-8 flex-shrink-0 overflow-hidden rounded-full border">
              {user?.avatar ? (
                <AuthAvatarImage
                  avatar={user.avatar}
                  alt=""
                  width={32}
                  height={32}
                  className="h-full w-full object-cover"
                  fallback={
                    <div className="bg-[var(--duo-line)] flex h-full w-full items-center justify-center">
                      <span className="text-[var(--duo-muted)] font-sans text-xs select-none">
                        {(user?.displayName ||
                          user?.username ||
                          '?')[0].toUpperCase()}
                      </span>
                    </div>
                  }
                />
              ) : (
                <div className="bg-[var(--duo-line)] flex h-full w-full items-center justify-center">
                  <span className="text-[var(--duo-muted)] font-sans text-xs select-none">
                    {(user?.displayName ||
                      user?.username ||
                      '?')[0].toUpperCase()}
                  </span>
                </div>
              )}
            </div>
            <div className="min-w-0">
              <p className="text-[var(--duo-muted)] truncate font-sans tracking-widest uppercase">
                {user?.displayName || user?.username}
              </p>
              <p className="text-[var(--duo-muted)] truncate font-sans">
                @{user?.username?.toLowerCase()}
              </p>
              {trialDaysLeft > 0 && (
                <p className="text-[var(--duo-green-dark)] truncate font-sans text-xs">
                  ★ {tBilling('trialDays', { days: trialDaysLeft })}
                </p>
              )}
            </div>
          </div>
          <p className="juba-duo-version">
            v1.9.16
          </p>
          <button
            onClick={() => setContactOpen(true)}
            className="juba-duo-user-action"
          >
            {tNav('contact')}
          </button>
          <button
            onClick={() => setLogoutConfirm(true)}
            className="juba-duo-user-action"
          >
            {tCommon('logout')}
          </button>
        </div>
      </aside>

      {/* Mobile top bar */}
      <div className="juba-duo-mobile-bar border-[var(--duo-line)] bg-[var(--duo-bg)] fixed inset-x-0 top-0 z-50 border-b shadow-[0_2px_0_var(--duo-line)]">
        <div className="flex items-center justify-between px-4 py-3">
          <span className="juba-duo-mobile-brand">JUBA LISAN</span>
          <button
            onClick={() => setMobileMenuOpen((o) => !o)}
            className="juba-duo-mobile-trigger"
            aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={mobileMenuOpen}
            aria-controls="juba-duo-mobile-menu"
          >
            <span className="text-base leading-none" aria-hidden="true">
              {mobileMenuOpen ? '×' : '☰'}
            </span>
          </button>
        </div>

        {/* Dropdown */}
        {mobileMenuOpen && (
          <nav
            id="juba-duo-mobile-menu"
            className="juba-duo-mobile-menu max-h-[calc(100vh-66px)] overflow-y-auto overscroll-contain"
          >
            <div className="border-[var(--duo-line)] border-b">
              <LanguageSwitcher />
            </div>
            {mainNavItems.map((item) => {
              const active =
                pathname === item.href || pathname.startsWith(item.href + '/')
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`juba-duo-nav-link ${active ? 'is-active' : ''}`}
                  aria-current={active ? 'page' : undefined}
                >
                  <item.icon className="h-[17px] w-[17px] shrink-0" />
                  {item.label}
                  {showPremiumBadge && PREMIUM_HREFS.has(item.href) && (
                    <span className="text-[var(--duo-green)] ms-auto text-xs">★</span>
                  )}
                </Link>
              )
            })}

            {/* Resources group (mobile) */}
            <div>
              <button
                onClick={() => setResourcesOpen((o) => !o)}
                className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] flex w-full items-center justify-between border-s-2 border-transparent px-5 py-2 font-sans text-sm tracking-wide wrap-anywhere uppercase transition-colors"
                aria-expanded={resourcesOpen}
                aria-controls="mobile-resources-menu"
              >
                <span>{tNav('resources')}</span>
                <span className="text-[var(--duo-ink)]">
                  {resourcesOpen ? '▴' : '▾'}
                </span>
              </button>
              {resourcesOpen &&
                <div id="mobile-resources-menu">{resourceNavItems.map((item) => {
                  const active =
                    pathname === item.href ||
                    pathname.startsWith(item.href + '/')
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`flex items-center gap-3 py-2.5 pe-5 ps-8 font-sans text-sm tracking-wide wrap-anywhere uppercase transition-colors ${
                        active
                          ? 'text-[var(--duo-ink)] bg-[var(--duo-line)] border-s-2 border-[var(--duo-green)]'
                          : 'text-[var(--duo-muted)] hover:text-[var(--duo-ink)] hover:bg-[var(--duo-card)] border-s-2 border-transparent'
                      }`}
                    >
                      <span
                        className={`text-[var(--duo-ink)] ${active ? 'text-[var(--duo-ink)]' : 'text-[var(--duo-muted)]'}`}
                      >
                        ·
                      </span>
                      {item.label}
                    </Link>
                  )
                })}</div>}
            </div>

            {/* Bottom items (mobile) */}
            {bottomNavItems.map((item) => {
              const active =
                pathname === item.href || pathname.startsWith(item.href + '/')
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center gap-3 px-5 py-3 font-sans text-sm tracking-wide wrap-anywhere uppercase transition-colors ${
                    active
                      ? 'text-[var(--duo-ink)] bg-[var(--duo-line)] border-s-2 border-[var(--duo-green)]'
                      : 'text-[var(--duo-muted)] hover:text-[var(--duo-ink)] hover:bg-[var(--duo-card)] border-s-2 border-transparent'
                  }`}
                >
                  <span
                    className={`text-[var(--duo-ink)] ${active ? 'text-[var(--duo-ink)]' : 'text-[var(--duo-muted)]'}`}
                  >
                    ●
                  </span>
                  {item.label}
                  {item.href === '/feedback' && feedbackBadgeText && (
                    <span className="text-[var(--duo-ink)] ms-auto flex h-6 w-6 shrink-0 -translate-y-0.5 items-center justify-center rounded-full bg-[var(--duo-red)] leading-none font-bold tracking-normal text-white">
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
                className={`flex items-center gap-3 px-5 py-3 font-sans text-sm tracking-wide wrap-anywhere uppercase transition-colors ${
                  pathname.startsWith('/admin')
                    ? 'text-[var(--duo-ink)] bg-[var(--duo-line)] border-s-2 border-[var(--duo-green)]'
                    : 'text-[var(--duo-muted)] hover:text-[var(--duo-ink)] hover:bg-[var(--duo-card)] border-s-2 border-transparent'
                }`}
              >
                <span className="text-[var(--duo-muted)]">●</span>
                {tNav('admin')}
              </Link>
            )}
            <div className="mx-5 mt-2 border-t-2 border-[var(--duo-line)] pt-3">
              <div className="mb-2 flex items-center gap-3">
                <div className="border-[var(--duo-line)] h-7 w-7 flex-shrink-0 overflow-hidden rounded-full border">
                  {user?.avatar ? (
                    <AuthAvatarImage
                      avatar={user.avatar}
                      alt=""
                      width={28}
                      height={28}
                      className="h-full w-full object-cover"
                      fallback={
                        <div className="bg-[var(--duo-line)] flex h-full w-full items-center justify-center">
                          <span className="text-[var(--duo-muted)] font-sans select-none">
                            {(user?.displayName ||
                              user?.username ||
                              '?')[0].toUpperCase()}
                          </span>
                        </div>
                      }
                    />
                  ) : (
                    <div className="bg-[var(--duo-line)] flex h-full w-full items-center justify-center">
                      <span className="text-[var(--duo-muted)] font-sans select-none">
                        {(user?.displayName ||
                          user?.username ||
                          '?')[0].toUpperCase()}
                      </span>
                    </div>
                  )}
                </div>
                <div className="min-w-0">
                  <p className="text-[var(--duo-muted)] truncate font-sans tracking-widest uppercase">
                    {user?.displayName || user?.username}
                  </p>
                  <p className="text-[var(--duo-muted)] truncate font-sans">
                    @{user?.username?.toLowerCase()}
                  </p>
                </div>
              </div>
              {trialDaysLeft > 0 && (
                <p className="text-[var(--duo-green-dark)] mb-2 font-sans text-xs">
                  ★ {tBilling('trialDays', { days: trialDaysLeft })}
                </p>
              )}
              <p className="mb-2 font-sans tracking-wider text-[var(--duo-muted)]">
                v1.9.16
              </p>
              <button
                onClick={() => {
                  setMobileMenuOpen(false)
                  setContactOpen(true)
                }}
                className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] mb-1 block font-sans text-xs tracking-widest uppercase transition-colors"
              >
                {tNav('contact')}
              </button>
              <button
                onClick={() => {
                  setMobileMenuOpen(false)
                  setLogoutConfirm(true)
                }}
                className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] font-sans text-xs tracking-widest uppercase transition-colors"
              >
                {tCommon('logout')}
              </button>
            </div>
          </nav>
        )}
      </div>

      {/* Main */}
      <main
        className="juba-duo-main min-w-0"
        id="main-content"
        aria-label={tNav('navigation')}
      >
        {/* Email verification banner */}
        {user && user.is_verified === false && (
          <div className="border-[var(--duo-line)] bg-[var(--duo-card)] flex flex-wrap items-center gap-x-4 gap-y-1 border-b px-4 py-2">
            <span className="text-[var(--duo-muted)] font-sans text-xs tracking-wide">
              ● {tCommon('verifyEmailBanner')}
            </span>
            {resendSent ? (
              <span className="text-[var(--duo-muted)] font-sans text-xs">
                {tCommon('verifyEmailSent')}
              </span>
            ) : (
              <button
                onClick={handleResendVerification}
                className="text-[var(--duo-green)] font-sans text-xs underline transition-all hover:no-underline"
              >
                {tCommon('resendVerification')}
              </button>
            )}
          </div>
        )}
        <div
          className="juba-duo-page-frame min-h-0 flex-1 overflow-y-auto overscroll-contain"
          tabIndex={-1}
          id="app-scroll-region"
        >
          {children}
        </div>
      </main>

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
