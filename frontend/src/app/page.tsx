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
    <div className="juba-funfluent-page juba-ff-reference min-h-screen flex flex-col font-sans selection:bg-[#ffd45c]/30 overflow-x-hidden">
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

      {/* Funfluent reference hero */}
      <section className="juba-ff-hero">
        <div className="juba-ff-hero-cloud cloud-one" aria-hidden="true" />
        <div className="juba-ff-hero-cloud cloud-two" aria-hidden="true" />
        <div className="juba-ff-hero-inner">
          <div className="juba-ff-hero-copy">
            <div className="juba-ff-pill"><Sparkles className="h-4 w-4" /> {t('heroBadge')}</div>
            <h1>{t('heroTitle')}</h1>
            <p>{t('heroSub')}</p>
            <div className="juba-ff-hero-actions">
              <Link href={hasSession ? '/dashboard' : '/register'} className="juba-ff-primary">
                {hasSession ? t('dashboard') : t('ctaStart')} <ArrowRight className="w-5 h-5" />
              </Link>
              <a href="#features" className="juba-ff-hero-link">{t('ctaExplore')}</a>
            </div>
            <div className="juba-ff-mini-proof">
              <span><CheckCircle2 className="h-4 w-4" /> CEFR-aligned learning</span>
              <span><CheckCircle2 className="h-4 w-4" /> Voice practice</span>
              <span><CheckCircle2 className="h-4 w-4" /> AI tutor</span>
            </div>
          </div>

          <div className="juba-ff-hero-art" aria-label="JUBA LISAN learning illustration">
            <div className="juba-ff-sun" aria-hidden="true" />
            <div className="juba-ff-mountain mountain-back" aria-hidden="true" />
            <div className="juba-ff-mountain mountain-front" aria-hidden="true" />
            <div className="juba-ff-island island-one" aria-hidden="true" />
            <div className="juba-ff-island island-two" aria-hidden="true" />
            <div className="juba-ff-character char-one">🧑🏽‍🎓</div>
            <div className="juba-ff-character char-two">🧙🏽‍♀️</div>
            <div className="juba-ff-character char-three">🧑🏻‍🚀</div>
            <div className="juba-ff-character char-four">🧑🏽‍🏴‍☠️</div>
            <div className="juba-ff-orbit orbit-one" aria-hidden="true" />
            <div className="juba-ff-orbit orbit-two" aria-hidden="true" />
            <div className="juba-ff-spark spark-one" aria-hidden="true">✦</div>
            <div className="juba-ff-spark spark-two" aria-hidden="true">✦</div>
            <div className="juba-ff-float-label label-one">Hello!</div>
            <div className="juba-ff-float-label label-two">Bonjour</div>
            <div className="juba-ff-float-label label-three">Hola</div>
            <div className="juba-ff-book-float">
              <div className="book-cover">🧭</div>
              <div><strong>Choose your next step</strong><span>Assess · Plan · Practice</span></div>
            </div>
          </div>
        </div>
        <div className="juba-ff-wave" aria-hidden="true" />
      </section>

      {/* Real product entry points — visual treatment only follows the reference */}
      <section id="features" className="juba-ff-books">
        <div className="juba-ff-section-head">
          <span className="juba-ff-section-tag">JUBA LISAN learning flow</span>
          <h2>Start with your real learning path</h2>
          <p>Each entry below opens an actual JUBA LISAN workflow rather than a decorative demo.</p>
        </div>
        <div className="juba-ff-book-shelf">
          <Link href="/assessment" className="juba-ff-book book-green">
            <div className="book-art">🧭<br /><span>ASSESS</span></div>
            <strong>Level Assessment</strong><span>Find your CEFR starting point</span>
          </Link>
          <Link href="/dashboard" className="juba-ff-book book-yellow">
            <div className="book-art">📅<br /><span>PLAN</span></div>
            <strong>Study Plan</strong><span>Follow today’s lessons and objectives</span>
          </Link>
          <Link href="/chat" className="juba-ff-book book-purple">
            <div className="book-art">💬<br /><span>AI</span></div>
            <strong>AI Tutor</strong><span>Practice through real conversations</span>
          </Link>
          <Link href="/conversation" className="juba-ff-book book-coral">
            <div className="book-art">🎙️<br /><span>VOICE</span></div>
            <strong>Voice Conversation</strong><span>Continue practice by speaking</span>
          </Link>
        </div>
      </section>

      {/* Funfluent-style product story: every JUBA LISAN capability stays real,
          but the presentation follows the reference from top to bottom. */}
      <section className="juba-ff-story juba-ff-story-features">
        <ScrollReveal>
          <div className="juba-ff-story-inner">
            <BentoFeatures t={t} />
          </div>
        </ScrollReveal>
      </section>

      <section className="juba-ff-story juba-ff-story-ai">
        <ScrollReveal>
          <div className="juba-ff-story-inner">
            <AiConversationShowcase t={t} />
          </div>
        </ScrollReveal>
      </section>

      <section className="juba-ff-story juba-ff-story-dashboard">
        <ScrollReveal>
          <div className="juba-ff-story-inner">
            <DashboardPreview t={t} />
          </div>
        </ScrollReveal>
      </section>

      <section className="juba-ff-story juba-ff-story-languages">
        <ScrollReveal>
          <div className="juba-ff-story-inner">
            <LanguageShowcase t={t} />
          </div>
        </ScrollReveal>
      </section>

      <section className="juba-ff-story juba-ff-story-learning">
        <ScrollReveal>
          <div className="juba-ff-story-inner">
            <LearningExperience t={t} />
          </div>
        </ScrollReveal>
      </section>

      {/* Social proof */}
      <section id="reviews" className="juba-ff-story juba-ff-story-reviews scroll-mt-20">
        <ScrollReveal>
          <div className="juba-ff-story-inner juba-ff-contained-card">
            <LandingReviewsCarousel reviews={reviews} />
          </div>
        </ScrollReveal>
      </section>

      {/* Pricing */}
      <section id="pricing" className="juba-ff-story juba-ff-story-pricing scroll-mt-20">
        <ScrollReveal>
          <div className="juba-ff-story-inner">
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
      </section>

      {/* Open Source Banner */}
      <ScrollReveal>
        <section className="juba-ff-open-source mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8 pb-16 pt-8">
          <div className="juba-ff-open-source-card flex flex-col items-center justify-between gap-6 sm:flex-row">
            <div className="flex items-center gap-4">
              <Image
                src="/github_white.svg"
                alt="GitHub"
                width={28}
                height={28}
                className="juba-ff-open-source-icon opacity-90"
              />
              <div className="text-left">
                <p className="juba-ff-open-source-title font-bold text-base tracking-tight">
                  {tBilling('openSourceTitle')}
                </p>
                <p className="juba-ff-open-source-desc text-xs mt-1">
                  {tBilling('openSourceDesc')}
                </p>
              </div>
            </div>
            <a
              href="https://github.com/abdelhadiLRS/JUBA_LISAN"
              target="_blank"
              rel="noopener noreferrer"
              className="juba-ff-open-source-cta rounded-[18px] px-6 py-2.5 text-xs font-bold tracking-wider uppercase transition-colors whitespace-nowrap"
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
            <h2 className="text-3xl font-extrabold tracking-tight text-[#183022]">
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
