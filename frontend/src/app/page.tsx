import Link from 'next/link'
import Image from 'next/image'
import { cookies } from 'next/headers'
import { getLocale, getTranslations } from 'next-intl/server'
import type { Metadata } from 'next'
import type { Locale } from '@/lib/locales'
import { ArrowRight, BookOpen, Headphones, MessageCircle, Sparkles } from 'lucide-react'
import PricingSection from '@/components/billing/PricingSection'
import { LandingFAQ } from '@/components/ui/landing-faq'
import { LandingNav } from '@/components/ui/landing-nav'
import { LanguageBubbles } from '@/components/LanguageBubbles'
import { LandingFooter } from '@/components/landing/LandingFooter'
import { LandingAiTutorShowcase } from '@/components/landing/LandingAiTutorShowcase'
import { LandingGamesShowcase } from '@/components/landing/LandingGamesShowcase'
import type { ReviewPublic } from '@/types/api'

export const metadata: Metadata = {
  title: 'JUBA LISAN: AI-Powered Language Learning Platform',
  description:
    'Learn languages naturally with your personal AI tutor. Master real-time voice conversations, structured CEFR lessons, interactive reading and listening, and smart flashcards.',
  robots: { index: true, follow: true },
  openGraph: {
    title: 'JUBA LISAN: AI-Powered Language Learning Platform',
    description:
      'Learn languages naturally with your personal AI tutor.',
    url: 'https://jubalisan.com',
    type: 'website',
    images: [{ url: '/og-image-v2.png', width: 1200, height: 630, alt: 'JUBA LISAN' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'JUBA LISAN: AI-Powered Language Learning Platform',
    description: 'Learn languages naturally with your personal AI tutor.',
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
    'AI-powered language learning platform with CEFR lessons, AI tutoring, voice conversation, reading, listening and flashcards.',
}

export default async function Home() {
  const cookieStore = await cookies()
  const hasSession = cookieStore.has('refresh_token')
  const locale = await getLocale()
  const t = await getTranslations('landing')
  const tBilling = await getTranslations('billing')

  let stripeEnabled = false
  let trialDays = 7
  let priceMonthly = 0
  let priceYearly = 0
  let totalPriceMonthly = 0
  let totalPriceYearly = 0
  let reviews: ReviewPublic[] = []

  try {
    const backendUrl = process.env.BACKEND_URL || 'http://backend:8000'
    const [configRes, reviewsRes] = await Promise.all([
      fetch(`${backendUrl}/api/config`, { next: { revalidate: 3600 } }),
      fetch(`${backendUrl}/api/reviews/public?limit=100`, { next: { revalidate: 300 } }),
    ])

    if (configRes.ok) {
      const cfg = await configRes.json()
      stripeEnabled = cfg.stripe_enabled ?? false
      trialDays = cfg.stripe_trial_days ?? 7
      priceMonthly = cfg.price_monthly ?? 0
      priceYearly = cfg.price_yearly ?? 0
      totalPriceMonthly = cfg.total_price_monthly ?? 0
      totalPriceYearly = cfg.total_price_yearly ?? 0
    }
    if (reviewsRes.ok) reviews = await reviewsRes.json()
  } catch {
    // Public landing data is non-fatal.
  }

  return (
    <main
      className="juba-reference-page min-h-screen overflow-x-hidden"
      dir={locale === 'ar' ? 'rtl' : 'ltr'}
      lang={locale}
    >
      <LandingNav
        hasSession={hasSession}
        dir={locale === 'ar' ? 'rtl' : 'ltr'}
        navFeatures={t('navFeatures')}
        navDemo={t('aiVoiceDemo')}
        navLanguages={t('supportedLanguages')}
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

      {/* HERO — the visitor-facing composition is deliberately rebuilt around the supplied reference:
          oversized playful type, pale paper background, organic illustration, floating cards and a single CTA. */}
      <section className="juba-ref-hero">
        <div className="juba-ref-hero-inner">
          <div className="juba-ref-hero-copy">
            <span className="juba-ref-kicker"><Sparkles className="h-4 w-4" /> {t('heroBadge')}</span>
            <h1>{t('heroTitle')}</h1>
            <p>{t('heroSub')}</p>
            <div className="juba-ref-hero-actions">
              <Link href={hasSession ? '/dashboard' : '/register'} className="juba-ref-button">
                {hasSession ? t('dashboard') : t('ctaStart')} <ArrowRight className="h-5 w-5" />
              </Link>
              <a href="#features" className="juba-ref-text-link">{t('ctaExplore')}</a>
            </div>
          </div>

          <div className="juba-ref-hero-art juba-landing-image-art">
            <Image
              src="/landing/juba-hero-characters.svg"
              alt={t('heroTitle')}
              width={900}
              height={700}
              className="juba-landing-real-image"
              priority
            />
          </div>
        </div>
        <div className="juba-ref-hero-bottom" aria-hidden="true" />
      </section>

      {/* PRODUCT PILLARS — real JUBA LISAN routes, presented as the reference's playful feature blocks. */}
      <section id="features" className="juba-ref-section juba-ref-pillars">
        <div className="juba-ref-section-heading">
          <span className="juba-ref-kicker">{t('flowEyebrow')}</span>
          <h2>{t('flowHeadline')}</h2>
          <p>{t('flowDescription')}</p>
        </div>
        <div className="juba-ref-pillar-grid">
          <Link href="/reading" className="juba-ref-pillar pillar-mint">
            <Image src="/landing/juba-reading.svg" alt="" width={210} height={150} className="juba-pillar-image" />
            <div className="pillar-icon"><BookOpen /></div>
            <span>{t('languagesEyebrow')}</span>
            <h3>{t('languagesHeadline')}</h3>
            <p>{t('languagesDescription')}</p>
            <ArrowRight />
          </Link>
          <Link href="/listening" className="juba-ref-pillar pillar-blue">
            <Image src="/landing/juba-listening.svg" alt="" width={210} height={150} className="juba-pillar-image" />
            <div className="pillar-icon"><Headphones /></div>
            <span>{t('flowVoiceLabel')}</span>
            <h3>{t('flowVoiceTitle')}</h3>
            <p>{t('flowVoiceDescription')}</p>
            <ArrowRight />
          </Link>
          <Link href="/chat" className="juba-ref-pillar pillar-yellow">
            <Image src="/landing/juba-chat.svg" alt="" width={210} height={150} className="juba-pillar-image" />
            <div className="pillar-icon"><MessageCircle /></div>
            <span>{t('flowAiLabel')}</span>
            <h3>{t('flowAiTitle')}</h3>
            <p>{t('flowAiDescription')}</p>
            <ArrowRight />
          </Link>
        </div>
      </section>

      <LandingGamesShowcase
        dir={locale === 'ar' ? 'rtl' : 'ltr'}
        eyebrow={t('featureSectionLabel')}
        title={t('bentoTitle')}
        description={t('bentoSubtitle')}
        matchingLabel={t('feature6Title')}
        memoryLabel={t('feature8Title')}
        orderingLabel={t('feature5Title')}
        sentenceBuilderLabel={t('feature2Title')}
        openLabel={t('openInJuba')}
      />

      {/* LANGUAGE SECTION — uses the real supported-language component. */}
      <section id="languages" className="juba-ref-language-section">
        <div className="juba-ref-language-copy">
          <span className="juba-ref-kicker">{t('languagesEyebrow')}</span>
          <h2>{t('languagesHeadline')}</h2>
          <p>{t('languagesDescription')}</p>
          <Link href="/register" className="juba-ref-button">{t('ctaStart')} <ArrowRight className="h-4 w-4" /></Link>
        </div>
        <div className="juba-ref-language-art">
          <div className="juba-ref-language-overlay">
            <LanguageBubbles dir={locale === 'ar' ? 'rtl' : 'ltr'} />
          </div>
        </div>
      </section>

      {/* AI / VOICE STORY — one visual block instead of the old dashboard-heavy landing. */}
      <LandingAiTutorShowcase
        dir={locale === 'ar' ? 'rtl' : 'ltr'}
        imageAlt={t('flowAiTitle')}
        userMessage={t('showcaseUserMsg')}
        aiMessage={t('showcaseAiMsg')}
        activeLabel={t('showcaseMicActive')}
        speakingLabel={t('showcaseSpeaking')}
        openLabel={t('openAiTutor')}
      />

      {/* REAL PUBLIC REVIEWS ONLY. */}
      {reviews.length > 0 && (
        <section id="reviews" className="juba-ref-reviews">
          <div className="juba-ref-section-heading">
            <span className="juba-ref-kicker">{t('navReviews')}</span>
            <h2>{t('flowHeadline')}</h2>
          </div>
          <div className="juba-ref-review-grid">
            {reviews.slice(0, 6).map((review) => (
              <article key={review.id} className="juba-ref-review-card">
                <p>“{review.comment ?? ''}”</p>
                <strong>{review.user_display_name || 'JUBA LISAN learner'}</strong>
              </article>
            ))}
          </div>
        </section>
      )}

      {/* REAL PRICING — existing billing/API data is untouched. */}
      <div id="pricing" className="juba-ref-pricing">
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

      <section className="juba-ref-cta">
        <div className="juba-ref-cta-inner">
          <div>
            <span className="juba-ref-kicker">{t('heroBadge')}</span>
            <h2>{t('ctaStart')}</h2>
            <p>{t('heroSub')}</p>
            <Link href={hasSession ? '/dashboard' : '/register'} className="juba-ref-button">
              {hasSession ? t('dashboard') : t('ctaStart')} <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="juba-ref-cta-device">
            <Image
              src="/landing/juba-learning-journey.svg"
              alt={t('ctaStart')}
              width={760}
              height={620}
              className="juba-landing-real-image juba-cta-real-image"
            />
          </div>
        </div>
      </section>

      <section id="faq" className="juba-ref-faq">
        <div className="juba-ref-section-heading">
          <span className="juba-ref-kicker">{t('navFAQ')}</span>
          <h2>{t('faqTitle')}</h2>
        </div>
        <LandingFAQ dir={locale === 'ar' ? 'rtl' : 'ltr'} />
      </section>

      <LandingFooter t={t} dir={locale === 'ar' ? 'rtl' : 'ltr'} />
    </main>
  )
}
