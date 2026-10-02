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
        /* JUBA LISAN — single reference design system for authenticated app chrome */
        .juba-app-shell{--juba-bg:#f8faf7;--juba-border:#e8eee4;--juba-ink:#30362f;--juba-muted:#7d857c;--juba-green:#58cc02;background:var(--juba-bg)!important;color:var(--juba-ink)!important;min-height:100dvh;width:100%;display:flex;flex-direction:row;direction:inherit;overflow:hidden}
        /* Shared dashboard canvas: every authenticated page uses the same visual grammar. */
        .juba-app-shell .juba-dashboard-workspace > *{
          width:100%!important;max-width:1480px!important;margin-inline:auto!important;
          box-sizing:border-box!important;
        }
        .juba-app-shell .juba-reference-page > *,
        .juba-app-shell .juba-reference-page-inner > *{
          max-width:none!important;
        }
        .juba-app-shell .juba-reference-hero,
        .juba-app-shell .juba-page-hero{
          background:#fff!important;border:1px solid var(--juba-border)!important;
          border-radius:14px!important;box-shadow:0 1px 2px rgba(36,48,32,.025)!important;
        }
        .juba-app-shell .juba-reference-section,
        .juba-app-shell .juba-reference-list-section{
          border-radius:12px!important;
        }
        .juba-app-shell .juba-card,
        .juba-app-shell .juba-panel,
        .juba-app-shell .juba-reference-list-card{
          background:#fff!important;border-color:var(--juba-border)!important;
          box-shadow:0 1px 2px rgba(36,48,32,.025)!important;
        }
        .juba-app-shell .juba-section-title,
        .juba-app-shell h1,
        .juba-app-shell h2,
        .juba-app-shell h3{
          letter-spacing:-.018em;
        }
        .juba-app-shell .juba-eyebrow,
        .juba-app-shell .juba-section-title{
          color:#7d857c!important;
        }
        .juba-app-shell .juba-primary-button{
          background:#58cc02!important;color:#fff!important;border-color:#58cc02!important;
          border-radius:9px!important;box-shadow:0 2px 0 #46a302!important;
        }
        .juba-app-shell .juba-primary-button:hover{background:#52bd00!important}
        .juba-app-shell .juba-secondary-button{
          background:#fff!important;border:1px solid #dfe7da!important;color:#586158!important;
          border-radius:9px!important;
        }
        .juba-app-shell .juba-input{
          min-height:40px!important;border:1px solid #dfe7da!important;border-radius:9px!important;
          background:#fff!important;color:#30362f!important;
        }
        .juba-app-shell .juba-badge{
          border:1px solid #dfe7da!important;background:#f5f9f2!important;color:#62805a!important;
          border-radius:999px!important;
        }
        .juba-app-shell table{
          border-color:var(--juba-border)!important;background:#fff!important;
        }
        .juba-app-shell thead{
          background:#f7faf5!important;
        }
        .juba-app-shell th{
          color:#7d857c!important;font-size:9px!important;font-weight:850!important;
          letter-spacing:.06em!important;text-transform:uppercase!important;
        }
        .juba-app-shell td{color:#4e564d!important;border-color:#edf1ea!important}
        .juba-app-shell [role="progressbar"]{border-radius:999px!important}
        .juba-app-shell svg{flex-shrink:0}
        .juba-app-shell[dir="rtl"] .juba-reference-page,
        .juba-app-shell[dir="rtl"] .juba-reference-page-inner{text-align:right}
        .juba-app-shell[dir="ltr"] .juba-reference-page,
        .juba-app-shell[dir="ltr"] .juba-reference-page-inner{text-align:left}
        @media (max-width:850px){
          .juba-app-shell .juba-dashboard-workspace > *{
            width:100%!important;max-width:100%!important;
            box-sizing:border-box!important;
          }
        }
        .juba-app-shell .juba-duo-sidebar{width:224px!important;min-width:224px!important;flex:0 0 224px!important;height:100dvh!important;position:sticky!important;top:0!important;overflow:hidden!important;background:#fff!important;border-inline-end:1px solid var(--juba-border)!important;box-shadow:none!important}
        .juba-app-shell .juba-duo-sidebar>div:first-child{height:72px!important;padding:0 18px!important;display:flex!important;align-items:center!important;gap:10px!important;border-bottom:1px solid #f0f3ed!important;background:#fff!important}
        .juba-app-shell .juba-duo-logo-mark{width:34px!important;height:34px!important;flex:none!important;display:grid!important;place-items:center!important;border:0!important;border-radius:50%!important;background:#58cc02!important;color:#fff!important;font-size:11px!important;font-weight:900!important;box-shadow:0 2px 0 #46a302!important}
        .juba-app-shell .juba-duo-sidebar>div:first-child>span:last-child{color:#58a91b!important;font-size:14px!important;font-weight:900!important;letter-spacing:-.025em!important;text-transform:none!important}
        .juba-app-shell .juba-duo-language{display:none!important}
        .juba-app-shell .juba-duo-nav{flex:1 1 auto!important;min-height:0!important;overflow-y:auto!important;overflow-x:hidden!important;padding:14px 10px 12px!important;scrollbar-width:none!important}
        .juba-app-shell .juba-duo-nav::-webkit-scrollbar{display:none!important}
        .juba-app-shell .juba-duo-nav-link{position:relative!important;display:flex!important;align-items:center!important;min-height:40px!important;margin:2px 0!important;padding:8px 11px!important;gap:10px!important;border:0!important;border-radius:9px!important;color:#70766f!important;background:transparent!important;font-size:11.5px!important;font-weight:700!important;line-height:1.15!important;letter-spacing:0!important;text-transform:none!important;white-space:nowrap!important;transition:background-color .16s ease,color .16s ease!important}
        .juba-app-shell .juba-duo-nav-link svg{width:17px!important;height:17px!important;flex:none!important;stroke-width:2.15!important}\n        .juba-app-shell .juba-duo-nav-section-label{margin:13px 10px 5px!important;color:#a0a79f!important;font-size:8px!important;font-weight:850!important;line-height:1!important;letter-spacing:.12em!important;text-transform:uppercase!important}

        .juba-app-shell .juba-duo-nav-link:hover{background:#f5faef!important;color:#4f9718!important;transform:none!important}
        .juba-app-shell .juba-duo-nav-link.is-active{background:#eaf8e5!important;color:#4f9718!important;font-weight:850!important;box-shadow:none!important}
        .juba-app-shell .juba-duo-nav-link.is-active:before{content:""!important;position:absolute!important;inset-inline-start:0!important;top:7px!important;bottom:7px!important;width:2px!important;border-radius:0 4px 4px 0!important;background:#58cc02!important}
        .juba-app-shell .juba-duo-nav-link.is-active svg{color:#58cc02!important}
        .juba-app-shell .juba-duo-resource-toggle{width:100%!important;min-height:34px!important;display:flex!important;align-items:center!important;justify-content:space-between!important;padding:7px 10px!important;border:0!important;border-radius:8px!important;background:transparent!important;color:#8a9088!important;font-size:9px!important;font-weight:800!important;letter-spacing:.08em!important;text-transform:uppercase!important}
        .juba-app-shell .juba-duo-resource-toggle:hover{background:#f7faf5!important;color:#5a9e28!important}
        .juba-app-shell .juba-duo-nav-divider{margin-top:4px!important;padding-top:0!important;border-top:0!important}
        .juba-app-shell .juba-duo-user{flex:none!important;padding:10px 12px!important;background:#fff!important;border-top:1px solid #eef1ec!important;box-shadow:none!important}
        .juba-app-shell .juba-duo-user-action{color:#8a9088!important;font-size:10px!important;border-radius:6px!important;padding:2px 4px!important;background:transparent!important;transition:color .16s ease,background-color .16s ease!important}
        .juba-app-shell .juba-duo-user-action:hover{color:#58a91b!important;background:#f6fbf3!important}
        .juba-app-shell .juba-duo-version{color:#c1c8bf!important;font-size:8px!important}
        .juba-app-shell .juba-duo-main{min-width:0!important;min-height:100dvh!important;background:var(--juba-bg)!important;display:flex!important;flex-direction:column!important;overflow:hidden!important;font-synthesis:none!important;-webkit-font-smoothing:antialiased!important}
        .juba-app-shell .juba-duo-page-frame{min-width:0!important;min-height:0!important;flex:1 1 auto!important;background:var(--juba-bg)!important;overscroll-behavior-y:contain!important;scrollbar-width:thin!important;scrollbar-color:#dfe7da transparent!important}
        .juba-app-shell .juba-duo-page-frame::-webkit-scrollbar{width:8px!important}
        .juba-app-shell .juba-duo-page-frame::-webkit-scrollbar-thumb{background:#dfe7da!important;border-radius:99px!important;border:2px solid var(--juba-bg)!important}
        .juba-app-shell .juba-app-topbar{height:64px!important;flex:0 0 64px!important;display:flex!important;align-items:center!important;gap:28px!important;padding:0 28px!important;background:#fff!important;border-bottom:1px solid #e8eee4!important;position:sticky!important;top:0!important;z-index:30!important;direction:inherit!important}
        .juba-app-shell .juba-app-topbar-brand{display:none!important}
        .juba-app-shell .juba-app-topnav{display:flex!important;align-items:stretch!important;gap:2px!important;height:100%!important;flex:1!important;min-width:0!important}
        .juba-app-shell .juba-app-topnav a{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:100%!important;padding:0 14px!important;border:0!important;border-bottom:2px solid transparent!important;color:#8a9188!important;background:transparent!important;text-decoration:none!important;font-size:10px!important;font-weight:800!important;white-space:nowrap!important;transition:color .16s ease,border-color .16s ease,background-color .16s ease!important}
        .juba-app-shell .juba-app-topnav a:hover{color:#58a51e!important;background:#f8fbf6!important}
        .juba-app-shell .juba-app-topnav a.is-active{color:#4f9718!important;border-bottom-color:#58cc02!important}
        .juba-app-shell .juba-app-topbar-user{display:flex!important;align-items:center!important;gap:8px!important;flex:none!important;color:#747c73!important;font-size:9px!important;font-weight:750!important}
        .juba-app-shell .juba-app-topbar-user-avatar{width:30px!important;height:30px!important;border-radius:50%!important;overflow:hidden!important;background:#edf3e9!important;border:1px solid #e4ebe0!important;display:grid!important;place-items:center!important}
        .juba-app-shell .juba-app-topbar-user-avatar img{width:100%!important;height:100%!important;object-fit:cover!important}
        .juba-app-shell .juba-duo-page-frame{direction:inherit!important;flex:1 1 auto;min-width:0}
        .juba-app-shell[dir="rtl"] .juba-app-topnav{flex-direction:row!important}
        .juba-app-shell[dir="rtl"] .juba-app-topbar-user{margin-inline-start:0!important}
        .juba-app-shell[dir="ltr"] .juba-app-topnav{flex-direction:row!important}
        .juba-app-shell [dir="rtl"] input,.juba-app-shell [dir="rtl"] textarea{direction:rtl!important;text-align:right!important}
        .juba-app-shell [dir="ltr"] input,.juba-app-shell [dir="ltr"] textarea{direction:ltr!important;text-align:left!important}
        .juba-app-shell [dir="rtl"] .dash2-chart,.juba-app-shell [dir="rtl"] .dash2-lessons{direction:rtl!important}
        .juba-app-shell [dir="ltr"] .dash2-chart,.juba-app-shell [dir="ltr"] .dash2-lessons{direction:ltr!important}
        .juba-app-shell .juba-ltr-data{direction:ltr!important;unicode-bidi:isolate!important}
        .juba-app-shell .juba-bidi-isolate{unicode-bidi:isolate!important}
        @media (max-width:850px){.juba-app-shell .juba-app-topbar{height:58px!important;flex-basis:58px!important;padding:0 14px!important;gap:10px!important}.juba-app-shell .juba-app-topnav{overflow-x:auto!important;scrollbar-width:none!important}.juba-app-shell .juba-app-topnav::-webkit-scrollbar{display:none!important}.juba-app-shell .juba-app-topnav a{font-size:9px!important;padding:0 10px!important}.juba-app-shell .juba-app-topbar-user span{display:none!important}}
        .juba-app-shell .juba-duo-mobile-bar{display:none!important}
        .juba-app-shell .juba-duo-mobile-brand{color:#58a91b!important;font-weight:900!important;letter-spacing:-.03em!important}
        .juba-app-shell .juba-duo-mobile-trigger{border:1px solid #e6ebe2!important;background:#fff!important;border-radius:9px!important;color:#5f6960!important;box-shadow:0 1px 2px rgba(40,60,30,.04)!important}
        .juba-app-shell .juba-duo-mobile-menu{background:#fff!important;border-top:0!important}
        .juba-app-shell .juba-duo-mobile-menu .juba-duo-nav-link{min-height:46px!important;margin:0!important;padding:10px 16px!important;border-bottom:1px solid #f2f4f0!important;border-radius:0!important}
        .juba-app-shell .juba-duo-mobile-menu .juba-duo-nav-link.is-active{background:#eff8e9!important}
        .juba-app-shell .juba-page-shell,.juba-app-shell .juba-mobile-courses,.juba-app-shell .juba-mobile-grammar,.juba-app-shell .juba-mobile-vocabulary,.juba-app-shell .juba-mobile-translator,.juba-app-shell .juba-mobile-listening,.juba-app-shell .juba-mobile-reading,.juba-app-shell .juba-mobile-settings,.juba-app-shell .juba-mobile-friends,.juba-app-shell .juba-admin-shell,.juba-app-shell .juba-admin-reviews-shell,.juba-app-shell .juba-admin-system-shell,.juba-app-shell .juba-admin-users-shell{width:100%!important;max-width:1480px!important;margin-inline:auto!important;box-sizing:border-box!important}
        .juba-app-shell .juba-reference-translator-grid{max-width:1180px!important;margin-inline:auto!important;width:100%!important}
        .juba-app-shell .juba-reference-translator-panel{border-radius:12px!important}
        .juba-app-shell .juba-reference-assessment-card{width:min(100%,720px)!important;border-radius:12px!important}
        .juba-app-shell .juba-reference-assessment-panel{border-radius:10px!important}
        .juba-app-shell .juba-reference-card-header{min-height:52px!important}
        .juba-app-shell .juba-reference-card-body{min-height:220px!important}
        .juba-app-shell .juba-reference-action{min-height:42px!important}
        .juba-app-shell .juba-reference-page{color:#242b25!important}
        .juba-app-shell .juba-reference-page-inner{display:flex!important;flex-direction:column!important}
        .juba-app-shell .juba-reference-hero{min-height:132px!important;display:flex!important;align-items:center!important}
        .juba-app-shell .juba-reference-hero h1{font-size:30px!important;line-height:1.12!important;letter-spacing:-.035em!important}
        .juba-app-shell .juba-reference-actions{gap:8px!important}
        .juba-app-shell .juba-reference-section-head h2{font-size:24px!important;line-height:1.15!important}
        .juba-app-shell .juba-reference-filter-panel{overflow:hidden!important}
        .juba-app-shell .juba-reference-filter-panel>div:first-child{min-height:52px!important;align-items:center!important}
        .juba-app-shell .juba-reference-filter-panel input{height:42px!important;max-width:460px!important}
        .juba-app-shell .juba-reference-tabs{padding-top:2px!important}
        .juba-app-shell .juba-reference-list-section>div:first-child{min-height:30px!important}
        .juba-app-shell .juba-reference-list-card{min-height:104px!important}
        .juba-app-shell .juba-reference-list-card:hover{border-color:#dce8d5!important;box-shadow:0 2px 10px rgba(42,64,34,.035)!important}
        .juba-app-shell .juba-reference-section{box-shadow:0 2px 10px rgba(42,64,34,.035)!important}
        .juba-app-shell .juba-page-shell{padding:24px 28px 36px!important}
        .juba-app-shell .juba-page-hero{background:#fff!important;border:1px solid #e8eee4!important;border-radius:12px!important;box-shadow:0 2px 10px rgba(42,64,34,.035)!important}
        .juba-app-shell .juba-page-title{color:#242b25!important;letter-spacing:-.035em!important}
        .juba-app-shell .juba-page-subtitle{color:#7b827c!important}
        .juba-app-shell .juba-eyebrow{color:#58a91b!important;font-weight:850!important;letter-spacing:.12em!important}
        .juba-app-shell .juba-card,.juba-app-shell .juba-panel{background:#fff!important;border:1px solid #e8eee4!important;border-radius:12px!important;box-shadow:0 2px 10px rgba(42,64,34,.035)!important}
        .juba-app-shell .juba-card:hover,.juba-app-shell .juba-panel:hover{border-color:#dfe8d9!important;box-shadow:0 2px 10px rgba(42,64,34,.035)!important}
        .juba-app-shell .juba-input{min-height:42px!important;background:#fff!important;border:1px solid #e1e7de!important;border-radius:10px!important;color:#303730!important;box-shadow:none!important}
        .juba-app-shell .juba-input:focus{border-color:#58cc02!important;box-shadow:0 0 0 3px rgba(88,204,2,.10)!important;outline:none!important}
        .juba-app-shell .juba-primary-button,.juba-app-shell .juba-secondary-button{border-radius:10px!important}
        .juba-app-shell .juba-badge{border-radius:999px!important}.juba-app-shell .juba-muted{color:#7d857c!important}
        .juba-app-shell .juba-assessment-page,.juba-app-shell .juba-games,.juba-app-shell .juba-dashboard-workspace{background:var(--juba-bg)!important}
        .juba-app-shell .games-shell{max-width:1480px!important}
        .juba-app-shell [class*="juba-mobile-"] input:not([type="checkbox"]):not([type="radio"]),.juba-app-shell [class*="juba-mobile-"] textarea,.juba-app-shell [class*="juba-mobile-"] select{border:1px solid #e3e9df!important;border-radius:10px!important;background:#fff!important;box-shadow:none!important}
        .juba-app-shell [class*="juba-mobile-"] input:focus,.juba-app-shell [class*="juba-mobile-"] textarea:focus,.juba-app-shell [class*="juba-mobile-"] select:focus{border-color:#58cc02!important;box-shadow:0 0 0 3px rgba(88,204,2,.10)!important;outline:none!important}
        .juba-app-shell a:focus-visible,.juba-app-shell button:focus-visible{outline:2px solid #58cc02!important;outline-offset:2px!important}
        @media (max-width:1180px) and (min-width:901px){.juba-app-shell .juba-duo-sidebar{width:192px!important;min-width:192px!important;flex-basis:192px!important}.juba-app-shell .juba-duo-nav-link{font-size:10.5px!important;padding-inline:8px!important;gap:8px!important}.juba-app-shell .juba-duo-nav-link svg{width:16px!important;height:16px!important}}
        @media (max-width:900px){.juba-app-shell{display:block!important}.juba-app-shell .juba-app-topbar{display:none!important}.juba-app-shell{background:#fff!important}.juba-app-shell .juba-duo-sidebar{display:none!important;width:0!important;min-width:0!important;flex-basis:0!important}.juba-app-shell .juba-duo-main{width:100%!important;min-height:100dvh!important;background:#fff!important}.juba-app-shell .juba-duo-page-frame{background:#fff!important;padding-top:54px!important}.juba-app-shell .juba-dashboard-workspace > *{width:100%!important;max-width:100%!important;box-sizing:border-box!important}.juba-app-shell .juba-duo-mobile-bar{display:block!important;height:54px!important;min-height:54px!important;background:#fff!important;border-bottom:1px solid #e8eee4!important;box-shadow:0 2px 10px rgba(40,60,30,.04)!important}.juba-app-shell [class*="juba-mobile-"]{background:#fff!important;padding-inline:14px!important;padding-top:18px!important;padding-bottom:24px!important}.juba-app-shell [class*="juba-mobile-"] h1{font-size:32px!important}.juba-app-shell [class*="juba-mobile-"] .juba-card,.juba-app-shell [class*="juba-mobile-"] .juba-panel{border-radius:12px!important}}
      `}</style>
    <div className="juba-duo-shell juba-busuu-app juba-app-shell" dir={dir}>
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
          {mainNavItems.map((item, index) => {
            const active =
              pathname === item.href || pathname.startsWith(item.href + '/')
            const group =
              index === 0
                ? (locale === 'ar' ? 'التعلّم' : 'LEARN')
                : index === 1
                  ? (locale === 'ar' ? 'الممارسة' : 'PRACTICE')
                  : index === 5
                    ? (locale === 'ar' ? 'اكتشاف' : 'DISCOVER')
                    : null
            return (
              <div key={item.href}>
                {group && <div className="juba-duo-nav-section-label">{group}</div>}
                <Link
                  href={item.href}
                  className={`juba-duo-nav-link ${active ? 'is-active' : ''}`}
                  aria-current={active ? 'page' : undefined}
                >
                  <item.icon className={`h-[18px] w-[18px] shrink-0 ${active ? 'text-[var(--duo-green)]' : 'text-[var(--duo-muted)]'}`} />
                  <span className="truncate">{item.label}</span>
                  {showPremiumBadge && PREMIUM_HREFS.has(item.href) && (
                    <span className="text-[var(--duo-green)] ms-auto shrink-0 text-xs">★</span>
                  )}
                </Link>
              </div>
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
      <div className="juba-duo-mobile-bar fixed inset-x-0 top-0 z-50 border-b border-[var(--duo-line)] bg-[var(--duo-card)] shadow-sm">
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
            <div className="mx-5 mt-2 border-t border-[var(--duo-line)] pt-3">
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
        <header className="juba-app-topbar" aria-label={tNav('navigation')}>
          <div className="juba-app-topbar-brand" aria-hidden="true">JUBA LISAN</div>
          <nav className="juba-app-topnav">
            {[
              { href: '/dashboard', label: tNav('home') },
              { href: '/plan', label: tNav('myPlan') },
              { href: '/courses', label: tNav('courses') },
            ].map((item) => {
              const active = pathname === item.href || pathname.startsWith(item.href + '/')
              return <Link key={item.href} href={item.href} className={active ? 'is-active' : ''} aria-current={active ? 'page' : undefined}>{item.label}</Link>
            })}
          </nav>
          <div className="juba-app-topbar-user">
            <span className="truncate max-w-[150px]">{user?.displayName || user?.username || ''}</span>
            <div className="juba-app-topbar-user-avatar">
              {user?.avatar ? <AuthAvatarImage avatar={user.avatar} alt="" width={30} height={30} className="h-full w-full object-cover" /> : <UserRound size={15} />}
            </div>
          </div>
        </header>
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
                className="text-[var(--duo-green)] font-sans text-xs underline transition-colors hover:no-underline"
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
