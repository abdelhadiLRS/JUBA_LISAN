'use client'

import { useEffect, useRef, useState } from 'react'
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
    { href: '/friends', label: tNav('friends'), icon: Users },
    { href: '/chat', label: tNav('tutor'), icon: MessageCircle },
    { href: '/listening', label: tNav('listening'), icon: Headphones },
    { href: '/reading', label: tNav('reading'), icon: BookOpen },
    { href: '/conversation', label: tNav('conversation'), icon: Languages },
    { href: '/assessment', label: tNav('assessment'), icon: ClipboardCheck },
    { href: '/coach', label: tNav('coach'), icon: Sparkles },
    { href: '/courses', label: tNav('courses'), icon: BookOpen },
    { href: '/review', label: tNav('review'), icon: Trophy },
    { href: '/translator', label: tNav('translator'), icon: Search },
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
  const mobileMenuTriggerRef = useRef<HTMLButtonElement>(null)
  const mobileMenuPanelRef = useRef<HTMLElement>(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [resourcesOpen, setResourcesOpen] = useState(false)
  const [contactOpen, setContactOpen] = useState(false)
  const [resendSent, setResendSent] = useState(false)
  const [feedbackUnreadCount, setFeedbackUnreadCount] = useState(0)

  const closeMobileMenu = () => {
    setMobileMenuOpen(false)
    setResourcesOpen(false)
    mobileMenuTriggerRef.current?.focus()
  }

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
    setResourcesOpen(
      resourceNavItems.some(
        (item) => pathname === item.href || pathname.startsWith(item.href + '/')
      )
    )
  }, [pathname])

  useEffect(() => {
    if (!mobileMenuOpen) return

    const panel = mobileMenuPanelRef.current
    const getFocusableElements = () =>
      Array.from(
        panel?.querySelectorAll<HTMLElement>(
          'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        ) ?? []
      ).filter((element) => !element.closest('[hidden]') && element.getAttribute('aria-hidden') !== 'true')

    getFocusableElements()[0]?.focus()

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setMobileMenuOpen(false)
        setResourcesOpen(false)
        mobileMenuTriggerRef.current?.focus()
        return
      }

      if (event.key !== 'Tab') return
      const focusableElements = getFocusableElements()
      if (focusableElements.length === 0) {
        event.preventDefault()
        return
      }

      const first = focusableElements[0]
      const last = focusableElements[focusableElements.length - 1]
      if (event.shiftKey && (document.activeElement === first || !panel?.contains(document.activeElement))) {
        event.preventDefault()
        last.focus()
      } else if (!event.shiftKey && (document.activeElement === last || !panel?.contains(document.activeElement))) {
        event.preventDefault()
        first.focus()
      }
    }

    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    document.addEventListener('keydown', handleKeyDown)

    return () => {
      document.body.style.overflow = previousOverflow
      document.removeEventListener('keydown', handleKeyDown)
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
        minHeight="min-h-[100dvh]"
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
    <>

      <style>{`
        /* JUBA LISAN app shell — strict reference chrome */
        .juba-reference-shell{background:#fff!important;color:#555!important}
        .juba-reference-shell .juba-duo-sidebar{width:220px!important;min-width:220px!important;background:#fff!important;border-right:1px solid #edf0ea!important;box-shadow:none!important;position:sticky!important;top:0!important;height:100dvh!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child{height:92px!important;padding:0 24px!important;border-bottom:0!important;display:flex!important;align-items:center!important;gap:10px!important}
        .juba-reference-shell .juba-duo-logo-mark{width:40px!important;height:40px!important;border:0!important;border-radius:50%!important;background:#58cc02!important;color:#fff!important;display:grid!important;place-items:center!important;font-weight:950!important;font-size:13px!important;box-shadow:0 3px 0 #46a302!important;flex:none!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child>span:last-child{color:#58a91b!important;font-size:15px!important;font-weight:900!important;letter-spacing:-.03em!important;text-transform:none!important}
        .juba-reference-shell .juba-duo-language{display:none!important}
        .juba-reference-shell .juba-duo-nav{padding:14px 12px!important}
        .juba-reference-shell .juba-duo-nav-link{min-height:43px!important;border:0!important;border-radius:10px!important;padding:8px 11px!important;margin:3px 0!important;color:#777!important;font-size:12px!important;font-weight:750!important;letter-spacing:0!important;text-transform:none!important;gap:12px!important}
        .juba-reference-shell .juba-duo-nav-link svg{width:20px!important;height:20px!important}
        .juba-reference-shell .juba-duo-nav-link:hover{background:#f6fbf3!important;color:#58a91b!important}
        .juba-reference-shell .juba-duo-nav-link.is-active{background:#eff9e8!important;color:#58a91b!important;box-shadow:none!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(1) svg{color:#58cc02!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(2) svg{color:#38a8e8!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(3) svg{color:#ffb900!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(4) svg{color:#2f9ee7!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(5) svg{color:#9b6be8!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(6) svg{color:#e55b5b!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(7) svg{color:#2aa6e0!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(8) svg{color:#5aa66b!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(9) svg{color:#36a86b!important}
        .juba-reference-shell .juba-duo-resource-toggle{min-height:38px!important;padding:8px 11px!important;color:#999!important;font-size:10px!important;font-weight:800!important}
        .juba-reference-shell .juba-duo-nav-divider{border-top:0!important;margin-top:5px!important;padding-top:0!important}
        .juba-reference-shell .juba-duo-user{border-top:1px solid #f0f0f0!important;background:#fff!important;padding:13px 15px!important}
        .juba-reference-shell .juba-duo-user-action{color:#999!important;font-size:10px!important}
        .juba-reference-shell .juba-duo-version{color:#c1c1c1!important;font-size:8px!important}
        .juba-reference-shell .juba-duo-main{background:#fff!important;min-width:0!important}
        .juba-reference-shell .juba-duo-page-frame{background:#fff!important}
        .juba-reference-shell .juba-duo-mobile-bar{display:none!important}
        @media (max-width:900px){
          .juba-reference-shell .juba-duo-sidebar{display:none!important}
          .juba-reference-shell .juba-duo-main{width:100%!important}
          .juba-reference-shell .juba-duo-mobile-bar{display:block!important;background:#fff!important;border-bottom:1px solid #edf0ea!important;box-shadow:none!important}
        }
        /* Reference fidelity pass — shared geometry only; landing page untouched */
        .juba-reference-shell .juba-duo-sidebar{width:224px!important;min-width:224px!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child{height:88px!important;padding:0 22px!important}
        .juba-reference-shell .juba-duo-nav{padding:16px 10px!important}
        .juba-reference-shell .juba-duo-nav-link{min-height:42px!important;margin:2px 0!important;padding:8px 12px!important;border-radius:9px!important;font-size:12px!important;line-height:1.2!important}
        .juba-reference-shell .juba-duo-nav-link svg{width:19px!important;height:19px!important}
        .juba-reference-shell .juba-duo-user{padding:12px 14px!important}
        @media (min-width:901px){.juba-reference-shell .juba-duo-page-frame{min-height:100dvh!important}}
        @media (max-width:900px){.juba-reference-shell .juba-duo-sidebar{width:100%!important;min-width:0!important}}

        /* Reference fidelity pass 2 — final shell proportions */
        .juba-reference-shell .juba-duo-sidebar{width:224px!important;min-width:224px!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child{height:86px!important}
        .juba-reference-shell .juba-duo-nav{padding:14px 10px!important}
        .juba-reference-shell .juba-duo-nav-link{min-height:41px!important;padding:8px 12px!important;margin:2px 0!important}
        .juba-reference-shell .juba-duo-nav-link.is-active{font-weight:850!important}
        .juba-reference-shell .juba-duo-user{padding:11px 14px!important}
        .juba-reference-shell .juba-duo-main{overflow-x:hidden!important}
        @media (max-width:900px){.juba-reference-shell .juba-duo-sidebar{width:100%!important;min-width:0!important}}

        /* Reference fidelity pass 3 — exact visual alignment */

        .juba-reference-shell .juba-duo-sidebar{width:228px!important;min-width:228px!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child{height:84px!important;padding:0 20px!important}
        .juba-reference-shell .juba-duo-logo-mark{width:38px!important;height:38px!important;font-size:12px!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child>span:last-child{font-size:14px!important;letter-spacing:-.025em!important}
        .juba-reference-shell .juba-duo-nav{padding:13px 9px!important}
        .juba-reference-shell .juba-duo-nav-link{min-height:40px!important;padding:8px 11px!important;border-radius:8px!important;gap:11px!important}
        .juba-reference-shell .juba-duo-nav-link svg{width:18px!important;height:18px!important}
        .juba-reference-shell .juba-duo-resource-toggle{min-height:36px!important;padding:7px 11px!important}
        .juba-reference-shell .juba-duo-nav-divider{margin-top:4px!important}
        .juba-reference-shell .juba-duo-user{padding:10px 13px!important}
        .juba-reference-shell .juba-duo-main{background:#fff!important}
        @media (max-width:1180px) and (min-width:901px){
          .juba-reference-shell .juba-duo-sidebar{width:196px!important;min-width:196px!important}
          .juba-reference-shell .juba-duo-nav-link{padding-inline:9px!important;gap:9px!important}
        }
        /* Reference fidelity pass 8 — final Busuu-style shell alignment */
        .juba-reference-shell .juba-duo-sidebar{width:220px!important;min-width:220px!important;flex-basis:220px!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child{height:80px!important;padding-inline:20px!important}
        .juba-reference-shell .juba-duo-logo-mark{width:36px!important;height:36px!important;box-shadow:0 2px 0 #46a302!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child>span:last-child{font-size:15px!important}
        .juba-reference-shell .juba-duo-nav{padding:12px 9px!important}
        .juba-reference-shell .juba-duo-nav-link{min-height:39px!important;margin:1px 0!important;padding:7px 11px!important;border-radius:9px!important;gap:10px!important}
        .juba-reference-shell .juba-duo-nav-link svg{width:18px!important;height:18px!important}
        .juba-reference-shell .juba-duo-user{padding:11px 13px!important}
        .juba-reference-shell .juba-duo-main{min-width:0!important}
        .juba-reference-shell .juba-duo-page-frame{scrollbar-width:thin!important;scrollbar-color:#dfe7da transparent!important}
        @media (max-width:1180px) and (min-width:901px){
          .juba-reference-shell .juba-duo-sidebar{width:204px!important;min-width:204px!important;flex-basis:204px!important}
          .juba-reference-shell .juba-duo-nav-link{font-size:11px!important;padding-inline:9px!important}
        }
        @media (max-width:900px){
          .juba-reference-shell .juba-duo-mobile-bar{height:56px!important;min-height:56px!important}
        }

        /* Reference fidelity pass 4 — shell finishing */
        .juba-reference-shell .juba-duo-sidebar{background:#fff!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child{border-bottom:1px solid #f3f4f1!important}
        .juba-reference-shell .juba-duo-nav-link{transition:background-color .16s ease,color .16s ease!important}
        .juba-reference-shell .juba-duo-nav-link.is-active{position:relative!important}
        .juba-reference-shell .juba-duo-nav-link.is-active:before{content:""!important;position:absolute!important;inset-inline-start:0!important;top:8px!important;bottom:8px!important;width:3px!important;border-radius:0 4px 4px 0!important;background:#58cc02!important}
        .juba-reference-shell .juba-duo-user{box-shadow:0 -1px 0 rgba(237,240,234,.55)!important}
        .juba-reference-shell .juba-duo-page-frame{scroll-behavior:smooth!important}
        .juba-reference-shell .juba-duo-main{font-synthesis:none!important;-webkit-font-smoothing:antialiased!important}
        @media (max-width:900px){
          .juba-reference-shell .juba-duo-mobile-bar{height:56px!important;min-height:56px!important;border-bottom:1px solid #edf0ea!important}
        }
        /* Reference fidelity pass 6 — final surface polish */
        .juba-reference-shell .juba-duo-sidebar{isolation:isolate!important}
        .juba-reference-shell .juba-duo-nav-link{font-family:inherit!important;letter-spacing:-.005em!important}
        .juba-reference-shell .juba-duo-nav-link.is-active:before{inset-inline-start:-1px!important}
        .juba-reference-shell .juba-duo-user{background:#fff!important}
        .juba-reference-shell .juba-duo-main{background:#fff!important}
        .juba-reference-shell .juba-duo-page-frame{background:#fff!important}
        .juba-reference-shell a:focus-visible,.juba-reference-shell button:focus-visible{outline:2px solid #58cc02!important;outline-offset:2px!important}
        @media (max-width:900px){.juba-reference-shell .juba-duo-mobile-bar{box-shadow:0 1px 8px rgba(30,50,20,.035)!important}}
              /* reference fidelity pass 7 — lock the screenshot geometry without changing behavior */
        .juba-reference-shell .juba-duo-sidebar{flex:0 0 220px!important}
        .juba-reference-shell .juba-duo-nav-link{position:relative!important;line-height:1.15!important}
        .juba-reference-shell .juba-duo-nav-link.is-active{background:#eaf8e5!important;color:#58a91b!important;font-weight:850!important}
        .juba-reference-shell .juba-duo-nav-link.is-active:before{width:3px!important;height:22px!important;border-radius:0 4px 4px 0!important;background:#58cc02!important}
        .juba-reference-shell .juba-duo-user{border-top:1px solid #edf0ea!important;padding:14px 12px 16px!important}
        .juba-reference-shell .juba-duo-main{min-height:100dvh!important}
        .juba-reference-shell .juba-duo-page-frame{scroll-behavior:smooth!important}
        .juba-reference-shell .juba-duo-page-frame::-webkit-scrollbar{width:8px!important}
        .juba-reference-shell .juba-duo-page-frame::-webkit-scrollbar-thumb{background:#dfe7da!important;border-radius:99px!important;border:2px solid #fff!important}
        @media (max-width:900px){.juba-reference-shell .juba-duo-sidebar{width:0!important;min-width:0!important;flex-basis:0!important}}

        /* Reference fidelity pass 9 — optical hierarchy and viewport stability */
        .juba-reference-shell .juba-duo-sidebar{overflow:hidden!important}
        .juba-reference-shell .juba-duo-nav{overflow-y:auto!important;overflow-x:hidden!important;scrollbar-width:none!important}
        .juba-reference-shell .juba-duo-nav::-webkit-scrollbar{display:none!important}
        .juba-reference-shell .juba-duo-nav-link{white-space:nowrap!important}
        .juba-reference-shell .juba-duo-nav-link svg{flex:none!important}
        .juba-reference-shell .juba-duo-user{flex:none!important}
        .juba-reference-shell .juba-duo-page-frame{overscroll-behavior-y:contain!important}
        @media (min-width:901px){
          .juba-reference-shell .juba-duo-sidebar{height:100dvh!important}
          .juba-reference-shell .juba-duo-main{height:100dvh!important;display:flex!important;flex-direction:column!important}
          .juba-reference-shell .juba-duo-page-frame{flex:1 1 auto!important;min-height:0!important}
        }
        @media (max-width:640px){
          .juba-reference-shell .juba-duo-main{width:100%!important}
        }
      `}        /* Reference fidelity pass 10 — screenshot-level shell geometry */
        .juba-reference-shell .juba-duo-sidebar{width:216px!important;min-width:216px!important;flex-basis:216px!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child{height:78px!important;padding-inline:18px!important}
        .juba-reference-shell .juba-duo-logo-mark{width:34px!important;height:34px!important;font-size:11px!important}
        .juba-reference-shell .juba-duo-nav{padding:11px 8px!important}
        .juba-reference-shell .juba-duo-nav-link{min-height:38px!important;padding:7px 10px!important;margin:1px 0!important;border-radius:8px!important;gap:10px!important;font-size:11.5px!important}
        .juba-reference-shell .juba-duo-nav-link svg{width:17px!important;height:17px!important;flex:none!important}
        .juba-reference-shell .juba-duo-resource-toggle{min-height:34px!important;padding:6px 10px!important;font-size:9px!important}
        .juba-reference-shell .juba-duo-user{padding:10px 12px!important}
        .juba-reference-shell .juba-duo-main{min-width:0!important;overflow:hidden!important}
        .juba-reference-shell .juba-duo-page-frame{min-width:0!important;background:#fff!important}
        .juba-reference-shell .juba-duo-nav-link.is-active:before{top:7px!important;bottom:7px!important;width:2px!important}
        @media (max-width:1180px) and (min-width:901px){
          .juba-reference-shell .juba-duo-sidebar{width:196px!important;min-width:196px!important;flex-basis:196px!important}
          .juba-reference-shell .juba-duo-nav-link{font-size:10.5px!important;padding-inline:8px!important;gap:8px!important}
          .juba-reference-shell .juba-duo-nav-link svg{width:16px!important;height:16px!important}
        }
        @media (max-width:900px){.juba-reference-shell .juba-duo-mobile-bar{height:54px!important;min-height:54px!important}}

        /* Reference fidelity pass 11 — final optical alignment */
        .juba-reference-shell .juba-duo-sidebar{width:216px!important;min-width:216px!important;flex-basis:216px!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child{height:78px!important;padding-inline:18px!important}
        .juba-reference-shell .juba-duo-logo-mark{width:34px!important;height:34px!important;font-size:11px!important}
        .juba-reference-shell .juba-duo-sidebar>div:first-child>span:last-child{font-size:14px!important}
        .juba-reference-shell .juba-duo-nav{padding:11px 8px!important}
        .juba-reference-shell .juba-duo-nav-link{min-height:38px!important;padding:7px 10px!important;border-radius:8px!important;gap:10px!important;font-size:11.5px!important}
        .juba-reference-shell .juba-duo-nav-link svg{width:17px!important;height:17px!important}
        .juba-reference-shell .juba-duo-resource-toggle{min-height:34px!important;padding:7px 10px!important}
        .juba-reference-shell .juba-duo-user{padding:10px 12px!important}
        .juba-reference-shell .juba-duo-user-action{transition:color .16s ease,background-color .16s ease!important;border-radius:6px!important;padding:2px 4px!important}
        .juba-reference-shell .juba-duo-user-action:hover{background:#f6fbf3!important;color:#58a91b!important}
        .juba-reference-shell .juba-duo-main{background:#fff!important}
        .juba-reference-shell .juba-duo-page-frame{background:#fff!important}
        @media (max-width:1180px) and (min-width:901px){
          .juba-reference-shell .juba-duo-sidebar{width:192px!important;min-width:192px!important;flex-basis:192px!important}
          .juba-reference-shell .juba-duo-nav-link{font-size:10.5px!important;padding-inline:8px!important;gap:8px!important}
        }
        @media (max-width:900px){
          .juba-reference-shell .juba-duo-mobile-bar{height:54px!important;min-height:54px!important}
        }


        /* Reference fidelity pass 12 — screenshot color rhythm and navigation detail */
        .juba-reference-shell .juba-duo-sidebar{background:#fff!important}
        .juba-reference-shell .juba-duo-nav-link{color:#70766f!important;font-weight:700!important}
        .juba-reference-shell .juba-duo-nav-link svg{stroke-width:2.15!important;transition:color .16s ease,transform .16s ease!important}
        .juba-reference-shell .juba-duo-nav-link:hover svg{transform:translateX(1px)!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(1) svg{color:#58cc02!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(2) svg{color:#ff9600!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(3) svg{color:#1cb0f6!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(4) svg{color:#ce82ff!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(5) svg{color:#ff4b4b!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(6) svg{color:#1cb0f6!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(7) svg{color:#58cc02!important}
        .juba-reference-shell .juba-duo-nav-link:nth-child(n+8) svg{color:#8b95a1!important}
        .juba-reference-shell .juba-duo-nav-link.is-active svg{color:#58cc02!important}
        .juba-reference-shell .juba-duo-nav-link.is-active{background:#eaf8e5!important}
        .juba-reference-shell .juba-duo-resource-toggle{color:#8a9088!important;font-weight:800!important;letter-spacing:.08em!important}
        .juba-reference-shell .juba-duo-user{background:#fff!important}
        @media (min-width:901px){
          .juba-reference-shell .juba-duo-page-frame{background:#f8faf7!important}
        }
        @media (max-width:900px){
          .juba-reference-shell .juba-duo-page-frame{background:#fff!important}
        }


        /* Reference fidelity pass 13 — shared visual language across every app page */
        .juba-reference-shell .juba-page-shell,
        .juba-reference-shell .juba-mobile-settings,
        .juba-reference-shell .juba-mobile-courses,
        .juba-reference-shell .juba-mobile-flashcards,
        .juba-reference-shell .juba-mobile-plan{
          color:var(--duo-ink);
        }
        .juba-reference-shell .juba-page-shell{max-width:1480px!important;margin-inline:auto!important}
        .juba-reference-shell .juba-page-hero{
          background:#fff!important;
          border:1px solid #edf1ea!important;
          border-radius:14px!important;
          box-shadow:0 1px 2px rgba(35,55,25,.035)!important;
        }
        .juba-reference-shell .juba-page-title{color:#30362f!important;letter-spacing:-.025em!important}
        .juba-reference-shell .juba-page-subtitle{color:#858c83!important}
        .juba-reference-shell .juba-eyebrow{color:#58a91b!important;letter-spacing:.09em!important}
        .juba-reference-shell .juba-panel,
        .juba-reference-shell .juba-card{
          background:#fff!important;
          border:1px solid #edf1ea!important;
          border-radius:13px!important;
          box-shadow:0 1px 2px rgba(35,55,25,.035)!important;
        }
        .juba-reference-shell .juba-panel:hover,
        .juba-reference-shell .juba-card:hover{
          border-color:#e4eadf!important;
          box-shadow:0 4px 14px rgba(35,55,25,.055)!important;
        }
        .juba-reference-shell .juba-input{
          background:#fff!important;
          border:1px solid #e5ebe1!important;
          border-radius:10px!important;
          color:#30362f!important;
          transition:border-color .16s ease,box-shadow .16s ease!important;
        }
        .juba-reference-shell .juba-input:focus{
          border-color:#9bd878!important;
          box-shadow:0 0 0 3px rgba(88,204,2,.12)!important;
          outline:none!important;
        }
        .juba-reference-shell button:not([data-reference-ignore]),
        .juba-reference-shell a.rounded-\[14px\],
        .juba-reference-shell a.rounded-\[20px\]{
          transition:transform .16s ease,box-shadow .16s ease,background-color .16s ease,border-color .16s ease!important;
        }
        .juba-reference-shell .juba-mobile-courses .juba-card,
        .juba-reference-shell .juba-mobile-plan .juba-card{
          overflow:hidden;
        }
        .juba-reference-shell .juba-mobile-courses,
        .juba-reference-shell .juba-mobile-settings,
        .juba-reference-shell .juba-mobile-flashcards,
        .juba-reference-shell .juba-mobile-plan{
          max-width:1480px!important;
        }
        .juba-reference-shell .juba-mobile-settings .juba-panel,
        .juba-reference-shell .juba-mobile-flashcards .juba-panel{
          border-radius:13px!important;
        }
        .juba-reference-shell .juba-assessment-page{
          background:#f8faf7!important;
        }
        .juba-reference-shell .juba-assessment-page>div{
          border-color:#edf1ea!important;
          border-radius:14px!important;
          box-shadow:0 1px 2px rgba(35,55,25,.035)!important;
        }
        .juba-reference-shell .juba-duo-shell{
          color:#30362f!important;
        }
        .juba-reference-shell .juba-duo-page-frame{
          border-color:#edf1ea!important;
          border-radius:13px!important;
          box-shadow:0 1px 2px rgba(35,55,25,.035)!important;
        }
        .juba-reference-shell .juba-duo-page-frame:hover{
          border-color:#e4eadf!important;
        }
        .juba-reference-shell .juba-games{
          background:#f8faf7!important;
          min-height:100%!important;
        }
        .juba-reference-shell .games-shell{
          max-width:1480px!important;
        }
        .juba-reference-shell .games-header,
        .juba-reference-shell .games-brand,
        .juba-reference-shell .stats-grid,
        .juba-reference-shell .game-grid,
        .juba-reference-shell .section-heading{
          border-color:#edf1ea!important;
        }
        @media (max-width:900px){
          .juba-reference-shell .juba-page-shell,
          .juba-reference-shell .juba-mobile-settings,
          .juba-reference-shell .juba-mobile-courses,
          .juba-reference-shell .juba-mobile-flashcards,
          .juba-reference-shell .juba-mobile-plan{
            max-width:none!important;
          }
          .juba-reference-shell .juba-assessment-page,
          .juba-reference-shell .juba-games{background:#fff!important}
        }

</style>
    <div className="juba-duo-shell juba-busuu-app juba-reference-shell" dir={dir}>
      <a className="juba-duo-skip-link" href="#main-content">
        {locale === 'ar' ? 'تجاوز إلى المحتوى الرئيسي' : 'Skip to main content'}
      </a>
      {/* Sidebar */}
      <aside className="juba-duo-sidebar" aria-label={tNav('primaryNavigation')}>
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
        <nav className="juba-duo-nav" aria-label={tNav('primaryNavigation')}>
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
            <div id="desktop-resources-menu" hidden={!resourcesOpen}>
              {resourceNavItems.map((item) => {
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
              })}
            </div>
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
      <div className="juba-duo-mobile-bar fixed inset-x-0 top-0 z-50 border-b-2 border-[var(--duo-line)] bg-[var(--duo-bg)] shadow-[0_2px_0_var(--duo-line)]">
        <div className="flex items-center justify-between px-4 py-3">
          <span className="juba-duo-mobile-brand">JUBA LISAN</span>
          <button
            onClick={() => setMobileMenuOpen((o) => !o)}
            ref={mobileMenuTriggerRef}
            className="juba-duo-mobile-trigger"
            aria-label={mobileMenuOpen ? (locale === 'ar' ? 'إغلاق القائمة' : 'Close menu') : (locale === 'ar' ? 'فتح القائمة' : 'Open menu')}
            aria-expanded={mobileMenuOpen}
            aria-controls="juba-duo-mobile-menu"
          >
            <span className="text-base leading-none" aria-hidden="true">
              {mobileMenuOpen ? '×' : '☰'}
            </span>
          </button>
        </div>

        {/* Dropdown */}
        <nav
          id="juba-duo-mobile-menu"
          ref={mobileMenuPanelRef}
          hidden={!mobileMenuOpen}
          aria-label={tNav('primaryNavigation')}
          className="juba-duo-mobile-menu max-h-[calc(100dvh-66px)] overflow-y-auto overscroll-contain"
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
                  onClick={closeMobileMenu}
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
                className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] flex min-h-11 w-full items-center justify-between border-s-2 border-transparent px-5 py-2 font-sans text-sm tracking-wide wrap-anywhere uppercase transition-colors"
                aria-expanded={resourcesOpen}
                aria-controls="mobile-resources-menu"
              >
                <span>{tNav('resources')}</span>
                <span className="text-[var(--duo-ink)]">
                  {resourcesOpen ? '▴' : '▾'}
                </span>
              </button>
              <div id="mobile-resources-menu" hidden={!resourcesOpen}>
                {resourceNavItems.map((item) => {
                  const active =
                    pathname === item.href ||
                    pathname.startsWith(item.href + '/')
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={closeMobileMenu}
                      aria-current={active ? 'page' : undefined}
                      className={`flex min-h-11 items-center gap-3 py-2.5 pe-5 ps-8 font-sans text-sm tracking-wide wrap-anywhere uppercase transition-colors ${
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
                })}
              </div>
            </div>

            {/* Bottom items (mobile) */}
            {bottomNavItems.map((item) => {
              const active =
                pathname === item.href || pathname.startsWith(item.href + '/')
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={closeMobileMenu}
                  className={`flex min-h-11 items-center gap-3 px-5 py-3 font-sans text-sm tracking-wide wrap-anywhere uppercase transition-colors ${
                    active
                      ? 'text-[var(--duo-ink)] bg-[var(--duo-line)] border-s-2 border-[var(--duo-green)]'
                      : 'text-[var(--duo-muted)] hover:text-[var(--duo-ink)] hover:bg-[var(--duo-card)] border-s-2 border-transparent'
                  }`}
                  aria-current={active ? 'page' : undefined}
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
                onClick={closeMobileMenu}
                aria-current={pathname.startsWith('/admin') ? 'page' : undefined}
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
                  closeMobileMenu()
                  setContactOpen(true)
                }}
                className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] mb-1 block font-sans text-xs tracking-widest uppercase transition-colors"
              >
                {tNav('contact')}
              </button>
              <button
                onClick={() => {
                  closeMobileMenu()
                  setLogoutConfirm(true)
                }}
                className="text-[var(--duo-muted)] hover:text-[var(--duo-ink)] font-sans text-xs tracking-widest uppercase transition-colors"
              >
                {tCommon('logout')}
              </button>
            </div>
        </nav>
      </div>

      {/* Main */}
      <main
        className="juba-duo-main min-w-0 overflow-x-hidden"
        id="main-content"
        aria-label={locale === 'ar' ? 'المحتوى الرئيسي' : 'Main content'}
        tabIndex={-1}
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
          className="juba-duo-page-frame juba-dashboard-workspace min-h-0 min-w-0 flex-1 overflow-x-hidden overflow-y-auto overscroll-contain [scrollbar-gutter:stable]"
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
    </>
  )
}
