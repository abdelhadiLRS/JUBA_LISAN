import Link from 'next/link'
import Image from 'next/image'
import Script from 'next/script'
import { cookies } from 'next/headers'
import { getLocale, getTranslations } from 'next-intl/server'
import type { Metadata } from 'next'
import type { Locale } from '@/lib/locales'
import {
  Sparkles,
  ArrowRight,
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
  const locale = await getLocale()
  const t = await getTranslations('landing')
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
      <Script
        id="juba-lisan-structured-data"
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Nav */}
      <LandingNav
        hasSession={hasSession}
        stripeEnabled={stripeEnabled}
        navFeatures={t('navFeatures')}
        navDemo={t('navDemo')}
        navLanguages={t('navLanguages')}
        navReviews={t('navReviews')}
        navPricing={t('navPricing')}
        navFAQ={t('navFAQ')}
        showReviews={reviews.length > 0}
        signIn={t('signIn')}
        dashboard={t('dashboard')}
        getStarted={t('ctaStart')}
        homeLabel={t('homeLabel')}
        brandTagline={t('brandTagline')}
        openMenuLabel={t('openMenuLabel')}
        closeMenuLabel={t('closeMenuLabel')}
        locale={locale as Locale}
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
              <span><CheckCircle2 className="h-4 w-4" /> {t('proofCefr')}</span>
              <span><CheckCircle2 className="h-4 w-4" /> {t('proofVoice')}</span>
              <span><CheckCircle2 className="h-4 w-4" /> {t('proofTutor')}</span>
            </div>
          </div>

          <div className="juba-ff-hero-art" aria-label="Language learning illustration">
            <div className="juba-ff-sun" aria-hidden="true" />
            <div className="juba-ff-mountain mountain-back" aria-hidden="true" />
            <div className="juba-ff-mountain mountain-front" aria-hidden="true" />
            <div className="juba-ff-island island-one" aria-hidden="true" />
            <div className="juba-ff-island island-two" aria-hidden="true" />

            <div className="juba-mascot mascot-main" aria-hidden="true">
              <div className="juba-mascot-shadow" />
              <div className="juba-mascot-body">
                <span className="juba-mascot-eye eye-left" />
                <span className="juba-mascot-eye eye-right" />
                <span className="juba-mascot-mouth" />
                <span className="juba-mascot-badge">AI</span>
              </div>
              <span className="juba-mascot-orbit orbit-a" />
              <span className="juba-mascot-orbit orbit-b" />
            </div>

            <div className="juba-ff-character char-one" aria-hidden="true"><span>EN</span></div>
            <div className="juba-ff-character char-two" aria-hidden="true"><span>FR</span></div>
            <div className="juba-ff-character char-three" aria-hidden="true"><span>ES</span></div>
            <div className="juba-ff-character char-four" aria-hidden="true"><span>{t('flowAiLabel')}</span></div>

            <div className="juba-ff-float-label label-one" aria-hidden="true">Hello!</div>
            <div className="juba-ff-float-label label-two" aria-hidden="true">Bonjour</div>
            <div className="juba-ff-float-label label-three" aria-hidden="true">Hola</div>
            <div className="juba-ff-book-float">
              <div className="book-cover" aria-hidden="true">J</div>
              <div><strong>Your language companion</strong><span>Assess · Learn · Practice</span></div>
            </div>
          </div>
        </div>
        <div className="juba-ff-wave" aria-hidden="true" />
      </section>

      {/* Language constellation — all supported learning languages are visible on the public page. */}
      <section id="languages" className="juba-ff-story juba-ff-story-languages scroll-mt-20">
        <ScrollReveal>
          <div className="juba-ff-story-inner">
            <div className="mb-8 text-center">
              <span className="juba-ff-section-tag">{t('languagesEyebrow')}</span>
              <h2 className="mt-3 text-3xl font-black tracking-tight text-[#183022] sm:text-4xl">{t('languagesHeadline')}</h2>
              <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-[#617068]">
                {t('languagesDescription')}
              </p>
            </div>
            <div className="mx-auto max-w-4xl">
              <LanguageBubbles />
            </div>
          </div>
        </ScrollReveal>
      </section>

      {/* Real product entry points — visual treatment only follows the reference */}
      <section id="features" className="juba-ff-books">
        <div className="juba-ff-section-head">
          <span className="juba-ff-section-tag">{t('flowEyebrow')}</span>
          <h2>{t('flowHeadline')}</h2>
          <p>{t('flowDescription')}</p>
        </div>
        <div className="juba-ff-book-shelf">
          <Link href="/assessment" className="juba-ff-book book-green">
            <div className="book-art" aria-hidden="true"><span className="book-art-mark">01</span><span>{t('flowAssessLabel')}</span></div>
            <strong>{t('flowAssessTitle')}</strong><span>{t('flowAssessDescription')}</span>
          </Link>
          <Link href="/dashboard" className="juba-ff-book book-yellow">
            <div className="book-art" aria-hidden="true"><span className="book-art-mark">02</span><span>{t('flowPlanLabel')}</span></div>
            <strong>{t('flowPlanTitle')}</strong><span>{t('flowPlanDescription')}</span>
          </Link>
          <Link href="/chat" className="juba-ff-book book-purple">
            <div className="book-art" aria-hidden="true"><span className="book-art-mark">03</span><span>{t('flowAiLabel')}</span></div>
            <strong>{t('flowAiTitle')}</strong><span>{t('flowAiDescription')}</span>
          </Link>
          <Link href="/conversation" className="juba-ff-book book-coral">
            <div className="book-art" aria-hidden="true"><span className="book-art-mark">04</span><span>{t('flowVoiceLabel')}</span></div>
            <strong>{t('flowVoiceTitle')}</strong><span>{t('flowVoiceDescription')}</span>
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

      <section id="demo" className="juba-ff-story juba-ff-story-ai scroll-mt-20">
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

      {/* Social proof — render only when real public reviews are available. */}
      {reviews.length > 0 && (
        <section id="reviews" className="juba-ff-story juba-ff-story-reviews scroll-mt-20">
          <ScrollReveal>
            <div className="juba-ff-story-inner juba-ff-contained-card">
              <LandingReviewsCarousel reviews={reviews} />
            </div>
          </ScrollReveal>
        </section>
      )}

      {/* Reference landing sequence: visual structure follows the supplied public-site reference while content stays JUBA LISAN data. */}
      <section className="juba-reference-stats" aria-label="JUBA LISAN platform statistics">
        <div className="juba-reference-stat"><strong>25,000+</strong><span>{t('navFeatures')}</span></div>
        <div className="juba-reference-stat"><strong>250+</strong><span>{t('navLanguages')}</span></div>
        <div className="juba-reference-stat"><strong>5.0</strong><span>{t('heroBadge')}</span></div>
      </section>

      <section className="juba-reference-feature">
        <div className="juba-reference-feature-art juba-reference-art-reading" aria-hidden="true"><span>Aa</span><i>♪</i></div>
        <div className="juba-reference-feature-copy"><span className="juba-ff-section-tag">{t('languagesEyebrow')}</span><h2>{t('languagesHeadline')}</h2><p>{t('languagesDescription')}</p><Link href="/reading" className="juba-ff-primary">{t('ctaStart')} <ArrowRight className="h-4 w-4" /></Link></div>
      </section>

      <section className="juba-reference-feature juba-reference-feature-reverse">
        <div className="juba-reference-feature-art juba-reference-art-listen" aria-hidden="true"><span>▶</span><i>♫</i></div>
        <div className="juba-reference-feature-copy"><span className="juba-ff-section-tag">{t('flowAiLabel')}</span><h2>{t('flowAiTitle')}</h2><p>{t('flowAiDescription')}</p><Link href="/chat" className="juba-ff-primary">{t('ctaStart')} <ArrowRight className="h-4 w-4" /></Link></div>
      </section>

      <section className="juba-reference-feature">
        <div className="juba-reference-feature-art juba-reference-art-practice" aria-hidden="true"><span>✓</span><i>ABC</i></div>
        <div className="juba-reference-feature-copy"><span className="juba-ff-section-tag">{t('flowVoiceLabel')}</span><h2>{t('flowVoiceTitle')}</h2><p>{t('flowVoiceDescription')}</p><Link href="/conversation" className="juba-ff-primary">{t('ctaStart')} <ArrowRight className="h-4 w-4" /></Link></div>
      </section>

      {reviews.length > 0 && (
        <section id="reviews" className="juba-reference-community scroll-mt-20">
          <div className="juba-reference-section-heading"><span className="juba-ff-section-tag">{t('navReviews')}</span><h2>{t('languagesHeadline')}</h2><p>{t('languagesDescription')}</p></div>
          <div className="juba-reference-testimonials">{reviews.slice(0, 6).map((review) => <article key={review.id} className="juba-reference-testimonial"><p>“{review.comment ?? ''}”</p><strong>{review.user_display_name || 'JUBA LISAN learner'}</strong></article>)}</div>
        </section>
      )}

      <section className="juba-reference-school">
        <div className="juba-reference-school-copy"><span className="juba-ff-section-tag">{t('flowEyebrow')}</span><h2>{t('flowHeadline')}</h2><p>{t('flowDescription')}</p><Link href="/register" className="juba-ff-primary">{t('ctaStart')} <ArrowRight className="h-4 w-4" /></Link></div>
        <div className="juba-reference-school-art" aria-hidden="true"><div className="juba-reference-phone"><span>JUBA</span><b>●</b><em>Learn · Practice · Progress</em></div><div className="juba-reference-character">★</div></div>
      </section>

      <section className="juba-reference-download">
        <div><span className="juba-ff-section-tag">{t('heroBadge')}</span><h2>{t('ctaStart')}</h2><p>{t('heroSub')}</p><div className="juba-reference-download-buttons"><a href="#pricing">App Store</a><a href="#pricing">Google Play</a></div></div>
        <div className="juba-reference-download-art" aria-hidden="true"><div className="juba-reference-device"><span>JUBA LISAN</span><b>Learn languages</b><i>● ● ●</i></div></div>
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
                style={{ width: '28px', height: 'auto' }}
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
