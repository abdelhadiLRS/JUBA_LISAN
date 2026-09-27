'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
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
import { BarChart3, BookOpen, Bot, Brain, ChevronDown, ClipboardCheck, Gamepad2, Globe2, GraduationCap, Headphones, Home, Languages, MessageCircle, MessagesSquare, Settings, Sparkles, Trophy, Users, Wrench } from 'lucide-react'

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const tNav = useTranslations('nav')
  const tCommon = useTranslations('common')
  const tBilling = useTranslations('billing')
  const pathname = usePathname()

  const mainNavItems = [
    { href: '/dashboard', label: tNav('home') },
    { href: '/plan', label: tNav('myPlan') },
    { href: '/progress', label: tNav('progress') },
    { href: '/games', label: tNav('games') },
    { href: '/flashcards', label: tNav('flashcards') },
    { href: '/friends', label: 'Friends' },
    { href: '/chat', label: tNav('tutor') },
    { href: '/listening', label: tNav('listening') },
    { href: '/reading', label: tNav('reading') },
    { href: '/conversation', label: tNav('conversation') },
    { href: '/assessment', label: tNav('assessment') },
    { href: '/coach', label: 'Coach' },
    { href: '/courses', label: 'Courses' },
    { href: '/review', label: 'Review' },
    { href: '/translator', label: 'Translator' },
  ]

  const resourceNavItems = [
    { href: '/grammar', label: tNav('grammar') },
    { href: '/vocabulary', label: tNav('vocabulary') },
    { href: '/phrasebook', label: tNav('phrasebook') },
  ]

  const navIcons: Record<string, typeof Home> = {
    '/dashboard': Home, '/plan': GraduationCap, '/progress': BarChart3, '/games': Gamepad2, '/flashcards': Brain,
    '/friends': Users, '/chat': MessageCircle, '/listening': Headphones, '/reading': BookOpen, '/conversation': MessagesSquare,
    '/assessment': ClipboardCheck, '/coach': Bot, '/courses': Languages, '/review': Trophy, '/translator': Globe2,
    '/grammar': Sparkles, '/vocabulary': Brain, '/phrasebook': BookOpen, '/settings': Settings, '/faq': Wrench, '/feedback': MessageCircle,
  }

  const bottomNavItems = [
    { href: '/settings', label: tNav('settings') },
    { href: '/faq', label: tNav('faq') },
    { href: '/feedback', label: tNav('feedback') },
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
        className="bg-[var(--juba-learning-bg)]"
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
    <div className="juba-learning-shell bg-[var(--juba-learning-bg)] flex min-h-screen md:h-screen md:overflow-hidden">
      {/* Sidebar */}
      <aside className="juba-learning-sidebar border-[var(--juba-learning-border)] bg-white hidden w-[260px] shrink-0 flex-col border-r px-0 py-0 md:flex">
        {/* Logo area */}
        <div className="border-[var(--juba-learning-border)] flex items-center gap-2 border-b px-5 py-5">
          <span className="text-[var(--juba-learning-muted)]">●</span>
          <span className="text-[var(--juba-learning-ink)] font-sans text-sm font-extrabold tracking-widest uppercase">
            JUBA LISAN
          </span>
        </div>

        {/* Language switcher */}
        <div className="border-[var(--juba-learning-border)] border-b">
          <LanguageSwitcher />
        </div>

        {/* Nav */}
        <nav className="juba-learning-nav flex-1 overflow-y-auto py-4">
          {/* Main items */}
          {mainNavItems.map((item) => {
            const active =
              pathname === item.href || pathname.startsWith(item.href + '/')
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-5 py-3 font-sans text-sm font-semibold wrap-anywhere transition-colors ${
                  active
                    ? 'text-[var(--juba-learning-ink)] bg-[var(--juba-learning-green-soft)] border-[var(--juba-learning-green)] border-l-2'
                    : 'text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] hover:bg-[var(--juba-learning-surface-soft)] border-l-2 border-transparent'
                }`}
              >
                {(() => { const Icon = navIcons[item.href] ?? Sparkles; return <Icon className={`h-5 w-5 shrink-0 ${active ? 'text-[var(--juba-learning-green-dark)]' : 'text-[var(--juba-learning-muted)]'}`} aria-hidden="true" /> })()}
                {item.label}
                {showPremiumBadge && PREMIUM_HREFS.has(item.href) && (
                  <span className="text-[var(--juba-learning-green-dark)] ml-auto text-xs">★</span>
                )}
              </Link>
            )
          })}

          {/* Resources group */}
          <div className="mt-2">
            <button
              onClick={() => setResourcesOpen((o) => !o)}
              className="text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-muted)] flex w-full items-center justify-between border-l-2 border-transparent px-5 py-2 font-sans text-sm font-semibold wrap-anywhere uppercase transition-colors"
            >
              <span>{tNav('resources')}</span>
              <ChevronDown className={`h-4 w-4 transition-transform ${resourcesOpen ? 'rotate-180' : ''}`} aria-hidden="true" />
            </button>
            {resourcesOpen &&
              resourceNavItems.map((item) => {
                const active =
                  pathname === item.href || pathname.startsWith(item.href + '/')
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center gap-3 py-2.5 pr-5 pl-8 font-sans text-sm font-semibold wrap-anywhere transition-colors ${
                      active
                        ? 'text-[var(--juba-learning-ink)] bg-[var(--juba-learning-green-soft)] border-[var(--juba-learning-green)] border-l-2'
                        : 'text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] hover:bg-[var(--juba-learning-surface-soft)] border-l-2 border-transparent'
                    }`}
                  >
                    {(() => { const Icon = navIcons[item.href] ?? Sparkles; return <Icon className={`h-4 w-4 shrink-0 ${active ? 'text-[var(--juba-learning-green-dark)]' : 'text-[var(--juba-learning-muted)]'}`} aria-hidden="true" /> })()}
                    {item.label}
                  </Link>
                )
              })}
          </div>

          {/* Bottom items */}
          <div className="border-[var(--juba-learning-border)] mt-2 border-t pt-2">
            {bottomNavItems.map((item) => {
              const active =
                pathname === item.href || pathname.startsWith(item.href + '/')
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-3 px-5 py-3 font-sans text-sm font-semibold wrap-anywhere transition-colors ${
                    active
                      ? 'text-[var(--juba-learning-ink)] bg-[var(--juba-learning-green-soft)] border-[var(--juba-learning-green)] border-l-2'
                      : 'text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] hover:bg-[var(--juba-learning-surface-soft)] border-l-2 border-transparent'
                  }`}
                >
                  {(() => { const Icon = navIcons[item.href] ?? Sparkles; return <Icon className={`h-5 w-5 shrink-0 ${active ? 'text-[var(--juba-learning-green-dark)]' : 'text-[var(--juba-learning-muted)]'}`} aria-hidden="true" /> })()}
                  {item.label}
                  {item.href === '/feedback' && feedbackBadgeText && (
                    <span className="text-white ml-auto flex h-6 w-6 shrink-0 -translate-y-0.5 items-center justify-center rounded-full bg-red-600 leading-none font-bold tracking-normal">
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
              className={`flex items-center gap-3 px-5 py-3 font-sans text-sm font-semibold wrap-anywhere transition-colors ${
                pathname.startsWith('/admin')
                  ? 'text-[var(--juba-learning-ink)] bg-[var(--juba-learning-green-soft)] border-[var(--juba-learning-green)] border-l-2'
                  : 'text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] hover:bg-[var(--juba-learning-surface-soft)] border-l-2 border-transparent'
              }`}
            >
              <Sparkles className="h-5 w-5 text-[var(--juba-learning-muted)]" aria-hidden="true" />
              {tNav('admin')}
            </Link>
          )}
        </nav>

        {/* User + logout */}
        <div className="border-[var(--juba-learning-border)] border-t px-5 py-4">
          <div className="mb-3 flex items-center gap-3">
            <div className="border-[var(--juba-learning-border)] h-8 w-8 flex-shrink-0 overflow-hidden rounded-full border">
              {user?.avatar ? (
                <AuthAvatarImage
                  avatar={user.avatar}
                  alt=""
                  width={32}
                  height={32}
                  className="h-full w-full object-cover"
                  fallback={
                    <div className="bg-[var(--juba-learning-green-soft)] flex h-full w-full items-center justify-center">
                      <span className="text-[var(--juba-learning-muted)] font-sans text-xs select-none">
                        {(user?.displayName ||
                          user?.username ||
                          '?')[0].toUpperCase()}
                      </span>
                    </div>
                  }
                />
              ) : (
                <div className="bg-[var(--juba-learning-green-soft)] flex h-full w-full items-center justify-center">
                  <span className="text-[var(--juba-learning-muted)] font-sans text-xs select-none">
                    {(user?.displayName ||
                      user?.username ||
                      '?')[0].toUpperCase()}
                  </span>
                </div>
              )}
            </div>
            <div className="min-w-0">
              <p className="text-fl-caption text-[var(--juba-learning-muted)] truncate font-mono tracking-widest uppercase">
                {user?.displayName || user?.username}
              </p>
              <p className="text-[var(--juba-learning-ink)] text-[var(--juba-learning-muted)] truncate font-mono">
                @{user?.username?.toLowerCase()}
              </p>
              {trialDaysLeft > 0 && (
                <p className="text-[var(--juba-learning-ink)] text-[var(--juba-learning-green-dark)] truncate font-sans text-xs">
                  ★ {tBilling('trialDays', { days: trialDaysLeft })}
                </p>
              )}
            </div>
          </div>
          <p className="text-[var(--juba-learning-ink)] text-[var(--juba-learning-muted)] font-code mb-2 tracking-wider">
            v1.9.15
          </p>
          <button
            onClick={() => setContactOpen(true)}
            className="text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] mb-1 w-full text-left font-sans text-xs font-semibold tracking-widest uppercase transition-colors"
          >
            {tNav('contact')}
          </button>
          <button
            onClick={() => setLogoutConfirm(true)}
            className="text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] w-full text-left font-sans text-xs font-semibold tracking-widest uppercase transition-colors"
          >
            {tCommon('logout')}
          </button>
        </div>
      </aside>

      {/* Mobile top bar */}
      <div className="border-[var(--juba-learning-border)] bg-[var(--juba-learning-bg)] fixed top-0 right-0 left-0 z-50 border-b md:hidden">
        <div className="flex items-center justify-between px-4 py-3">
          <span className="text-[var(--juba-learning-ink)] font-code text-xs font-bold tracking-widest uppercase">
            JUBA LISAN
          </span>
          <button
            onClick={() => setMobileMenuOpen((o) => !o)}
            className="text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] p-1 font-mono transition-colors"
            aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
          >
            <span className="text-base leading-none">
              {mobileMenuOpen ? '✕' : '☰'}
            </span>
          </button>
        </div>

        {/* Dropdown */}
        {mobileMenuOpen && (
          <nav className="border-[var(--juba-learning-border)] bg-[var(--juba-learning-bg)] max-h-[calc(100svh-3.5rem)] overflow-y-auto overscroll-contain border-t pb-2">
            <div className="border-[var(--juba-learning-border)] border-b">
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
                  className={`flex items-center gap-3 px-5 py-3 font-sans text-sm font-semibold wrap-anywhere uppercase transition-colors ${
                    active
                      ? 'text-[var(--juba-learning-ink)] bg-[var(--juba-learning-green-soft)] border-[var(--juba-learning-green)] border-l-2'
                      : 'text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] hover:bg-[var(--juba-learning-surface-soft)] border-l-2 border-transparent'
                  }`}
                >
                  {(() => { const Icon = navIcons[item.href] ?? Sparkles; return <Icon className={`h-5 w-5 shrink-0 ${active ? 'text-[var(--juba-learning-green-dark)]' : 'text-[var(--juba-learning-muted)]'}`} aria-hidden="true" /> })()}
                  {item.label}
                  {showPremiumBadge && PREMIUM_HREFS.has(item.href) && (
                    <span className="text-[var(--juba-learning-green-dark)] ml-auto text-xs">★</span>
                  )}
                </Link>
              )
            })}

            {/* Resources group (mobile) */}
            <div>
              <button
                onClick={() => setResourcesOpen((o) => !o)}
                className="text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-muted)] flex w-full items-center justify-between border-l-2 border-transparent px-5 py-2 font-sans text-sm font-semibold wrap-anywhere uppercase transition-colors"
              >
                <span>{tNav('resources')}</span>
                <span className="text-[var(--juba-learning-ink)]">
                  {resourcesOpen ? '▴' : '▾'}
                </span>
              </button>
              {resourcesOpen &&
                resourceNavItems.map((item) => {
                  const active =
                    pathname === item.href ||
                    pathname.startsWith(item.href + '/')
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`flex items-center gap-3 py-2.5 pr-5 pl-8 font-sans text-sm font-semibold wrap-anywhere uppercase transition-colors ${
                        active
                          ? 'text-[var(--juba-learning-ink)] bg-[var(--juba-learning-green-soft)] border-[var(--juba-learning-green)] border-l-2'
                          : 'text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] hover:bg-[var(--juba-learning-surface-soft)] border-l-2 border-transparent'
                      }`}
                    >
                      <span
                        className={`text-[var(--juba-learning-ink)] ${active ? 'text-[var(--juba-learning-ink)]' : 'text-[var(--juba-learning-muted)]'}`}
                      >
                        ·
                      </span>
                      {item.label}
                    </Link>
                  )
                })}
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
                  className={`flex items-center gap-3 px-5 py-3 font-sans text-sm font-semibold wrap-anywhere uppercase transition-colors ${
                    active
                      ? 'text-[var(--juba-learning-ink)] bg-[var(--juba-learning-green-soft)] border-[var(--juba-learning-green)] border-l-2'
                      : 'text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] hover:bg-[var(--juba-learning-surface-soft)] border-l-2 border-transparent'
                  }`}
                >
                  <span
                    className={`text-[var(--juba-learning-ink)] ${active ? 'text-[var(--juba-learning-ink)]' : 'text-[var(--juba-learning-muted)]'}`}
                  >
                    ●
                  </span>
                  {item.label}
                  {item.href === '/feedback' && feedbackBadgeText && (
                    <span className="text-[var(--juba-learning-ink)] ml-auto flex h-6 w-6 shrink-0 -translate-y-0.5 items-center justify-center rounded-full bg-red-600 leading-none font-bold tracking-normal text-white">
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
                className={`flex items-center gap-3 px-5 py-3 font-sans text-sm font-semibold wrap-anywhere uppercase transition-colors ${
                  pathname.startsWith('/admin')
                    ? 'text-[var(--juba-learning-ink)] bg-[var(--juba-learning-green-soft)] border-[var(--juba-learning-green)] border-l-2'
                    : 'text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] hover:bg-[var(--juba-learning-surface-soft)] border-l-2 border-transparent'
                }`}
              >
                <span className="text-[var(--juba-learning-ink)] text-[var(--juba-learning-muted)]">●</span>
                {tNav('admin')}
              </Link>
            )}
            <div className="border-[var(--juba-learning-border)] mx-5 mt-2 border-t pt-3">
              <div className="mb-2 flex items-center gap-3">
                <div className="border-[var(--juba-learning-border)] h-7 w-7 flex-shrink-0 overflow-hidden rounded-full border">
                  {user?.avatar ? (
                    <AuthAvatarImage
                      avatar={user.avatar}
                      alt=""
                      width={28}
                      height={28}
                      className="h-full w-full object-cover"
                      fallback={
                        <div className="bg-[var(--juba-learning-green-soft)] flex h-full w-full items-center justify-center">
                          <span className="text-fl-hint text-[var(--juba-learning-muted)] font-mono select-none">
                            {(user?.displayName ||
                              user?.username ||
                              '?')[0].toUpperCase()}
                          </span>
                        </div>
                      }
                    />
                  ) : (
                    <div className="bg-[var(--juba-learning-green-soft)] flex h-full w-full items-center justify-center">
                      <span className="text-fl-hint text-[var(--juba-learning-muted)] font-mono select-none">
                        {(user?.displayName ||
                          user?.username ||
                          '?')[0].toUpperCase()}
                      </span>
                    </div>
                  )}
                </div>
                <div className="min-w-0">
                  <p className="text-fl-caption text-[var(--juba-learning-muted)] truncate font-mono tracking-widest uppercase">
                    {user?.displayName || user?.username}
                  </p>
                  <p className="text-[var(--juba-learning-ink)] text-[var(--juba-learning-muted)] truncate font-mono">
                    @{user?.username?.toLowerCase()}
                  </p>
                </div>
              </div>
              {trialDaysLeft > 0 && (
                <p className="text-[var(--juba-learning-ink)] text-[var(--juba-learning-green-dark)] mb-2 font-sans text-xs">
                  ★ {tBilling('trialDays', { days: trialDaysLeft })}
                </p>
              )}
              <p className="text-[var(--juba-learning-ink)] text-[var(--juba-learning-muted)] font-code mb-2 tracking-wider">
                v1.9.15
              </p>
              <button
                onClick={() => {
                  setMobileMenuOpen(false)
                  setContactOpen(true)
                }}
                className="text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] mb-1 block font-sans text-xs font-semibold tracking-widest uppercase transition-colors"
              >
                {tNav('contact')}
              </button>
              <button
                onClick={() => {
                  setMobileMenuOpen(false)
                  setLogoutConfirm(true)
                }}
                className="text-[var(--juba-learning-muted)] hover:text-[var(--juba-learning-ink)] font-sans text-xs font-semibold tracking-widest uppercase transition-colors"
              >
                {tCommon('logout')}
              </button>
            </div>
          </nav>
        )}
      </div>

      {/* Main */}
      <main className="juba-learning-main flex min-h-[100dvh] flex-1 flex-col overflow-hidden pt-14 md:min-h-screen md:pt-0">
        {/* Email verification banner */}
        {user && user.is_verified === false && (
          <div className="border-[var(--juba-learning-border)] bg-[var(--juba-learning-surface-soft)] flex flex-wrap items-center gap-x-4 gap-y-1 border-b px-4 py-2">
            <span className="text-[var(--juba-learning-muted)] font-sans text-xs tracking-wide">
              ● {tCommon('verifyEmailBanner')}
            </span>
            {resendSent ? (
              <span className="text-[var(--juba-learning-muted)] font-sans text-xs">
                {tCommon('verifyEmailSent')}
              </span>
            ) : (
              <button
                onClick={handleResendVerification}
                className="text-[var(--juba-learning-green-dark)] font-sans text-xs underline transition-all hover:no-underline"
              >
                {tCommon('resendVerification')}
              </button>
            )}
          </div>
        )}
        <div className="min-h-0 flex-1 overflow-y-auto">{children}</div>
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
