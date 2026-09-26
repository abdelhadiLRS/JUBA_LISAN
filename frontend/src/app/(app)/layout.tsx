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
import { Bell, BookOpen, BrainCircuit, ChevronDown, ClipboardCheck, Gamepad2, GraduationCap, Headphones, Languages, MessageCircle, MessagesSquare, Settings2, Sparkles, Trophy, UserRound, Users, Volume2, X } from 'lucide-react'

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

  const visibleMainNavItems = isAdmin ? [] : mainNavItems
  const visibleResourceNavItems = isAdmin ? [] : resourceNavItems
  const visibleBottomNavItems = isAdmin ? [] : bottomNavItems

  const feedbackBadgeText =
    feedbackUnreadCount > 99
      ? '99+'
      : feedbackUnreadCount > 0
        ? String(feedbackUnreadCount)
        : ''

  return (
    <div className="min-h-screen bg-[#dfe3ff] p-0 md:p-3 lg:p-4">
      <div className="mx-auto flex min-h-screen max-w-[1600px] flex-col overflow-hidden bg-[#f6f6f4] shadow-[0_35px_100px_-35px_rgba(24,28,46,.55)] md:min-h-[calc(100vh-24px)] md:rounded-[34px]">
        <header className="relative z-50 flex min-h-[76px] items-center gap-3 bg-[#24272b] px-4 text-white sm:px-6 lg:px-8">
          <Link href="/dashboard" className="flex shrink-0 items-center gap-3">
            <span className="grid size-11 place-items-center rounded-full bg-[#7776df] shadow-inner shadow-white/20">
              <span className="text-lg font-black">JL</span>
            </span>
            <span className="hidden text-lg font-black tracking-[-.04em] sm:inline">JUBA LISAN</span>
          </Link>

          <nav className="mx-auto hidden items-center gap-1 rounded-full bg-[#17191c] p-1 sm:flex">
            {[
              { href: '/dashboard', label: tNav('home') },
              { href: '/plan', label: tNav('myPlan') },
              { href: '/progress', label: tNav('progress') },
              { href: '/games', label: tNav('games') },
              { href: '/courses', label: tNav('courses') },
            ].map((item) => {
              const active = pathname === item.href || pathname.startsWith(item.href + '/')
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`rounded-full px-4 py-2 text-xs font-bold transition ${
                    active ? 'bg-white text-[#24272b]' : 'text-white/60 hover:bg-white/10 hover:text-white'
                  }`}
                >
                  {item.label}
                </Link>
              )
            })}
          </nav>

          <div className="ml-auto flex items-center gap-2">
            <LanguageSwitcher />
            <button type="button" className="relative hidden size-10 place-items-center rounded-full border border-white/10 text-white/75 hover:bg-white/10 sm:grid" aria-label="Notifications">
              <Bell className="size-4" />
              <span className="absolute right-2 top-2 size-1.5 rounded-full bg-[#f26b69]" />
            </button>
            <Link href="/settings" className="hidden items-center gap-2 rounded-full bg-white/10 px-3 py-2 sm:flex">
              <div className="grid size-8 place-items-center overflow-hidden rounded-full bg-[#d8c9a9] text-[#25272b]">
                {user?.avatar ? (
                  <AuthAvatarImage avatar={user.avatar} alt="" width={32} height={32} className="h-full w-full object-cover" fallback={<span className="text-xs font-black">{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>} />
                ) : (
                  <span className="text-xs font-black">{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>
                )}
              </div>
              <span className="max-w-28 truncate text-xs font-black">{user?.displayName || user?.username}</span>
              <ChevronDown className="size-3 text-white/50" />
            </Link>
            <button
              type="button"
              onClick={() => setMobileMenuOpen((o) => !o)}
              className="grid size-10 place-items-center rounded-full bg-white/10 sm:hidden"
              aria-label={mobileMenuOpen ? tCommon('close') : tCommon('openMenu')}
            >
              {mobileMenuOpen ? <X className="size-5" /> : <Menu className="size-5" />}
            </button>
          </div>
        </header>

        {mobileMenuOpen && (
          <nav className="border-b border-black/10 bg-[#24272b] px-4 py-3 text-white sm:hidden">
            <div className="grid grid-cols-2 gap-2">
              {[...visibleMainNavItems, ...visibleResourceNavItems, ...visibleBottomNavItems].map((item) => {
                const active = pathname === item.href || pathname.startsWith(item.href + '/')
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`rounded-2xl px-3 py-3 text-xs font-bold ${
                      active ? 'bg-white text-[#24272b]' : 'bg-white/5 text-white/70'
                    }`}
                  >
                    {item.label}
                  </Link>
                )
              })}
            </div>
          </nav>
        )}

        <div className="flex min-h-0 flex-1">
          <aside className="hidden w-60 shrink-0 flex-col bg-[#292c30] text-white lg:flex">
            <div className="border-b border-white/10 px-5 py-5">
              <p className="text-[10px] font-bold uppercase tracking-[.18em] text-white/40">{tNav('home')}</p>
              <p className="mt-1 truncate text-sm font-black">{user?.displayName || user?.username}</p>
            </div>
            <nav className="flex-1 overflow-y-auto px-3 py-4">
              {visibleMainNavItems.map((item) => {
                const active = pathname === item.href || pathname.startsWith(item.href + '/')
                return (
                  <Link key={item.href} href={item.href} className={`mb-1 flex items-center justify-between rounded-2xl px-4 py-3 text-sm font-bold transition ${
                    active ? 'bg-[#7776df] text-white shadow-lg' : 'text-white/55 hover:bg-white/10 hover:text-white'
                  }`}>
                    <span className="flex min-w-0 items-center gap-3"><NavIcon href={item.href} className="size-4 shrink-0 opacity-80" /><span className="truncate">{item.label}</span></span>
                    {showPremiumBadge && PREMIUM_HREFS.has(item.href) && <Sparkles className="size-3.5 shrink-0 text-[#ffcf67]" />}
                  </Link>
                )
              })}
              <div className="my-4 border-t border-white/10" />
              <p className="px-4 pb-2 text-[9px] font-bold uppercase tracking-[.16em] text-white/30">{tNav('resources')}</p>
              {visibleResourceNavItems.map((item) => {
                const active = pathname === item.href || pathname.startsWith(item.href + '/')
                return <Link key={item.href} href={item.href} className={`mb-1 block rounded-2xl px-4 py-2.5 text-xs font-bold transition ${active ? 'bg-white/10 text-white' : 'text-white/50 hover:text-white'}`}>{item.label}</Link>
              })}
            </nav>
            <div className="border-t border-white/10 p-4">
              <div className="mb-3 flex items-center gap-3">
                <div className="grid size-10 shrink-0 place-items-center overflow-hidden rounded-full bg-[#d8c9a9] text-[#25272b]">
                  {user?.avatar ? <AuthAvatarImage avatar={user.avatar} alt="" width={40} height={40} className="h-full w-full object-cover" fallback={<span className="font-black">{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>} /> : <span className="font-black">{(user?.displayName || user?.username || '?')[0].toUpperCase()}</span>}
                </div>
                <div className="min-w-0">
                  <p className="truncate text-xs font-black">{user?.displayName || user?.username}</p>
                  <p className="truncate text-[10px] text-white/40">@{user?.username?.toLowerCase()}</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <Link href="/settings" className="rounded-xl bg-white/10 px-3 py-2 text-center text-[10px] font-bold">{tNav('settings')}</Link>
                <button onClick={() => setLogoutConfirm(true)} className="rounded-xl bg-white/10 px-3 py-2 text-[10px] font-bold">{tCommon('logout')}</button>
              </div>
            </div>
          </aside>

          <main className="min-h-0 flex-1 overflow-y-auto bg-[#f6f6f4]">
            {user && user.is_verified === false && (
              <div className="flex flex-wrap items-center gap-x-4 gap-y-1 border-b border-black/5 bg-[#fff8e8] px-4 py-2">
                <span className="text-xs font-bold text-black/55">● {tCommon('verifyEmailBanner')}</span>
                {resendSent ? <span className="text-xs text-black/45">{tCommon('verifyEmailSent')}</span> : <button onClick={handleResendVerification} className="text-xs font-bold text-[#5f5ec5] underline">{tCommon('resendVerification')}</button>}
              </div>
            )}
            <div className="min-h-full">{children}</div>
          </main>
        </div>
      </div>

      <LoadingBar />
      <ContactFormModal open={contactOpen} onClose={() => setContactOpen(false)} />
      <ConfirmDialog open={logoutConfirm} title={tCommon('logoutConfirmTitle')} message={tCommon('logoutConfirmMessage')} confirmLabel={tCommon('logout')} onConfirm={handleLogout} onCancel={() => setLogoutConfirm(false)} />
    </div>
  )
}
