import Link from 'next/link'
import Image from 'next/image'
import { cookies } from 'next/headers'
import { getTranslations } from 'next-intl/server'
import type { Metadata } from 'next'
import {
  Sparkles,
  ArrowRight,
  Bot,
  Mic,
  Volume2,
  ShieldCheck,
  CheckCircle2,
} from 'lucide-react'
import PricingSection from '@/components/billing/PricingSection'
import { LandingFAQ } from '@/components/ui/landing-faq'
import { LandingNav } from '@/components/ui/landing-nav'
import { ScrollReveal } from '@/components/ui/scroll-reveal'
import { LanguageBubbles } from '@/components/LanguageBubbles'
import { LandingReviewsCarousel } from '@/components/reviews/LandingReviewsCarousel'
import { BentoFeatures } from '@/components/landing/BentoFeatures'
import { AiConversationShowcase } from '@/components/landing/AiConversationShowcase'
import { DashboardPreview } from '@/components/landing/DashboardPreview'
import { LanguageShowcase } from '@/components/landing/LanguageShowcase'
import { LearningExperience } from '@/components/landing/LearningExperience'
import { LandingFooter } from '@/components/landing/LandingFooter'
import type { ReviewPublic } from '@/types/api'

export const metadata: Metadata = {
  title: 'JUBA LISAN: AI-Powered Language Learning Platform',
  description:
    'Learn languages naturally with your personal AI tutor. Master real-time voice conversations, structured CEFR lessons, interactive reading & listening, and smart flashcards.',
  robots: { index: true, follow: true },
  openGraph: {
    title: 'JUBA LISAN: AI-Powered Language Learning Platform',
    description:
      'Learn languages naturally with your personal AI tutor. Master real-time voice conversations, structured CEFR lessons, interactive reading & listening, and smart flashcards.',
    url: 'https://jubalisan.com',
    type: 'website',
    images: [
      {
        url: '/og-image-v2.png',
        width: 1200,
        height: 630,
        alt: 'JUBA LISAN: AI-Powered Language Learning Platform',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'JUBA LISAN: AI-Powered Language Learning Platform',
    description:
      'Learn languages naturally with your personal AI tutor. Master real-time voice conversations, structured CEFR lessons, interactive reading & listening, and smart flashcards.',
    images: ['/og-image-v2.png'],
  },
}

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'SoftwareApplication',
  name: 'JUBA LISAN',
  applicationCategory: 'EducationApplication',
  operatingSystem: 'Web',
  url: 'https://jubalisan.com',
  description:
    'AI-powered language learning platform with real-time voice conversation, spaced-repetition flashcards, structured CEFR lessons, and interactive AI tutor.',
  offers: {
    '@type': 'Offer',
    price: '0',
    priceCurrency: 'USD',
  },
}

export default async function Home() {
  const cookieStore = await cookies()
  const hasSession = cookieStore.has('refresh_token')
  const t = await getTranslations('landing')
  const tCommon = await getTranslations('common')
  const tBilling = await getTranslations('billing')

  let stripeEnabled = false
  let trialDays = 7
  let priceMonthly = 0.0
  let priceYearly = 0.0
  let totalPriceMonthly = 0.0
  let totalPriceYearly = 0.0
  let reviews: ReviewPublic[] = []
  try {
    const backendUrl = process.env.BACKEND_URL || 'http://backend:8000'
    const [configRes, reviewsRes] = await Promise.all([
      fetch(`${backendUrl}/api/config`, { next: { revalidate: 3600 } }),
      fetch(`${backendUrl}/api/reviews/public?limit=100`, {
        next: { revalidate: 300 },
      }),
    ])
    if (configRes.ok) {
      const cfg = await configRes.json()
      stripeEnabled = cfg.stripe_enabled ?? false
      trialDays = cfg.stripe_trial_days ?? 7
      priceMonthly = cfg.price_monthly ?? 0.0
      priceYearly = cfg.price_yearly ?? 0.0
      totalPriceMonthly = cfg.total_price_monthly ?? 0.0
      totalPriceYearly = cfg.total_price_yearly ?? 0.0
    }
    if (reviewsRes.ok) {
      reviews = await reviewsRes.json()
    }
  } catch {
    /* non-fatal */
  }

  return (
    <div className="juba-funfluent-page min-h-screen flex flex-col font-sans selection:bg-[var(--juba-yellow)]/25 overflow-x-hidden">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Nav */}
      <LandingNav
        hasSession={hasSession}
        stripeEnabled={stripeEnabled}
        navFeatures={t('navFeatures')}
        navReviews={t('navReviews')}
        navPricing={t('navPricing')}
        navFAQ={t('navFAQ')}
        showReviews={reviews.length > 0}
        signIn={t('signIn')}
        dashboard={t('dashboard')}
      />

      {/* Hero Section */}
      <section className="juba-funfluent-hero">
        <div className="juba-funfluent-hero-inner">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">

            {/* Left Column: Hero Text & Actions */}
            <div className="juba-funfluent-copy">

              {/* Floating Language Pills Header */}
              <div className="mb-4">
                <LanguageBubbles />
              </div>

              {/* Badge */}
              <div className="inline-flex items-center gap-2 rounded-[18px] bg-[var(--juba-lilac)] border-2 border-[var(--juba-border)] px-3.5 py-1.5 text-xs font-bold text-[var(--juba-violet)] uppercase tracking-wider mb-6">
                <Sparkles className="h-4 w-4" />
                {t('heroBadge')}
              </div>

              {/* Main Headline */}
              <h1>
                {t('heroTitle')}
              </h1>

              {/* Subtitle */}
              <p>
                {t('heroSub')}
              </p>

              {/* CTAs */}
              <div className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto">
                <Link
                  href={hasSession ? '/dashboard' : '/register'}
                  className="juba-ff-primary w-full sm:w-auto gap-2"
                >
                  {hasSession ? t('dashboard') : t('ctaStart')}
                  <ArrowRight className="w-5 h-5" />
                </Link>
                <a
                  href="#features"
                  className="juba-ff-secondary w-full sm:w-auto gap-2"
                >
                  {t('ctaExplore')}
                </a>
              </div>

              {/* Key Trust Highlights */}
              <div className="mt-10 pt-8 border-t border-[var(--juba-border)] flex flex-wrap items-center justify-center lg:justify-start gap-6 text-xs font-semibold text-[var(--juba-muted)]">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-500" /> Free 7-Day Access
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" /> Real-time Voice VAD
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" /> CEFR Structured Curriculum
                </div>
              </div>
            </div>

            {/* Right Column: AI Tutor Card Showcase */}
            <div className="juba-ff-art"><div className="ff-orbit" aria-hidden="true" /><div className="ff-card"><span className="ff-emoji">🦜</span>Speak & learn</div><div className="ff-card"><span className="ff-emoji">📚</span>Read stories</div><div className="ff-card"><span className="ff-emoji">🎧</span>Listen naturally</div>
              <div className="relative z-10 mx-auto w-full max-w-md rounded-[30px] border-[6px] border-white bg-white/90 p-6 shadow-[0_18px_0_rgba(57,117,29,.10),0_30px_55px_rgba(57,117,29,.16)] backdrop-blur-xl">
                <div className="flex items-center justify-between pb-4 border-b border-[var(--juba-border)] mb-6">
                  <div className="flex items-center gap-3">
                    <div className="relative flex h-12 w-12 items-center justify-center rounded-[28px] bg-gradient-to-tr from-[var(--juba-violet)] to-[var(--juba-coral)] text-white font-extrabold text-xl shadow-md">
                      <Bot className="w-6 h-6" />
                      <span className="absolute -bottom-0.5 -right-0.5 flex h-3.5 w-3.5">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-[18px] bg-emerald-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-[18px] h-3.5 w-3.5 bg-emerald-500"></span>
                      </span>
                    </div>
                    <div>
                      <h3 className="font-extrabold text-base text-[var(--juba-text)]">JUBA AI Tutor</h3>
                      <p className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">Active & Ready to speak</p>
                    </div>
                  </div>
                  <span className="text-xs px-2.5 py-1 rounded-[18px] bg-[var(--juba-yellow)]/25 text-[var(--juba-violet)] font-bold border border-[var(--juba-border)]">
                    B2 Upper Intermediate
                  </span>
                </div>

                {/* Simulated Conversation Preview */}
                <div className="space-y-4 mb-6">
                  <div className="bg-[var(--juba-surface-soft)] p-4 rounded-[28px] border border-[var(--juba-border)]">
                    <p className="text-xs text-[var(--juba-muted)] font-semibold mb-1">JUBA Tutor says:</p>
                    <p className="text-sm text-[var(--juba-text)] font-medium leading-relaxed">
                      "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
                    </p>
                  </div>

                  {/* Audio Waveform Widget */}
                  <div className="flex items-center justify-between bg-[var(--juba-yellow)]/35 p-4 rounded-[28px] border border-[var(--juba-border)]">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-[18px] bg-[var(--juba-violet)] text-[var(--juba-ink)] flex items-center justify-center shrink-0 shadow-md">
                        <Mic className="w-5 h-5 animate-pulse" />
                      </div>
                      <div>
                        <p className="text-xs font-bold text-[var(--juba-text)]">Voice Input Ready</p>
                        <p className="text-[11px] text-[var(--juba-violet)]">Speech detection active</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-1 h-5">
                      <span className="w-1 bg-[var(--juba-violet)] h-3 rounded-[18px] animate-pulse"></span>
                      <span className="w-1 bg-[var(--juba-violet)] h-5 rounded-[18px] animate-pulse delay-75"></span>
                      <span className="w-1 bg-[var(--juba-violet)] h-2 rounded-[18px] animate-pulse delay-150"></span>
                    </div>
                  </div>
                </div>

                <div className="pt-2">
                  <Link
                    href={hasSession ? '/dashboard' : '/register'}
                    className="w-full flex items-center justify-center gap-2 py-3 rounded-[18px] bg-[var(--juba-violet)] hover:bg-[var(--juba-violet-dark)] text-white font-bold text-xs transition-all"
                  >
                    Try Conversation Mode <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* Bento Features Section */}
      <ScrollReveal>
        <BentoFeatures t={t} />
      </ScrollReveal>

      {/* AI Conversation Showcase Section */}
      <ScrollReveal>
        <AiConversationShowcase t={t} />
      </ScrollReveal>

      {/* Dashboard Preview Mockup Section */}
      <ScrollReveal>
        <DashboardPreview t={t} />
      </ScrollReveal>

      {/* Supported Languages Showcase Section */}
      <ScrollReveal>
        <LanguageShowcase t={t} />
      </ScrollReveal>

      {/* Learning Experience Timeline Section */}
      <ScrollReveal>
        <LearningExperience t={t} />
      </ScrollReveal>

      {/* Reviews Section */}
      <ScrollReveal>
        <div id="reviews" className="scroll-mt-20">
          <LandingReviewsCarousel reviews={reviews} />
        </div>
      </ScrollReveal>

      {/* Pricing Section */}
      <ScrollReveal>
        <div id="pricing" className="scroll-mt-20">
          <PricingSection
            stripeEnabled={stripeEnabled}
            trialDays={trialDays}
            hasSession={hasSession}
            priceMonthly={priceMonthly}
            priceYearly={priceYearly}
            totalPriceMonthly={totalPriceMonthly}
            totalPriceYearly={totalPriceYearly}
          />
        </div>
      </ScrollReveal>

      {/* Open Source Banner */}
      <ScrollReveal>
        <section className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8 pb-16 pt-8">
          <div className="juba-card p-8 flex flex-col items-center justify-between gap-6 sm:flex-row bg-gradient-to-r from-[var(--juba-violet-dark)] to-[var(--juba-violet)] text-white">
            <div className="flex items-center gap-4">
              <Image
                src="/github_white.svg"
                alt="GitHub"
                width={28}
                height={28}
                className="opacity-90"
              />
              <div className="text-left">
                <p className="font-bold text-base tracking-tight text-white">
                  {tBilling('openSourceTitle')}
                </p>
                <p className="text-xs text-white/70 mt-1">
                  {tBilling('openSourceDesc')}
                </p>
              </div>
            </div>
            <a
              href="https://github.com/abdelhadiLRS/JUBA_LISAN"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-[18px] border border-white/20 bg-white/10 hover:bg-white/20 text-white px-6 py-2.5 text-xs font-bold tracking-wider uppercase transition-colors whitespace-nowrap"
            >
              {tBilling('openSourceCta')}
            </a>
          </div>
        </section>
      </ScrollReveal>

      {/* FAQ Section */}
      <ScrollReveal>
        <section
          id="faq"
          className="mx-auto w-full max-w-5xl scroll-mt-20 px-4 sm:px-6 pb-20"
        >
          <div className="text-center mb-12">
            <h2 className="text-3xl font-extrabold tracking-tight text-[var(--juba-text)]">
              {t('faqTitle')}
            </h2>
          </div>
          <LandingFAQ />
        </section>
      </ScrollReveal>

      {/* Redesigned Footer */}
      <LandingFooter t={t} />
    </div>
  )
}
