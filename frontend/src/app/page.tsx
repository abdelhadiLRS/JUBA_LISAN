import Link from 'next/link'
import Image from 'next/image'
import { cookies } from 'next/headers'
import { getLocale, getTranslations } from 'next-intl/server'
import type { Metadata } from 'next'
import type { Locale } from '@/lib/locales'
import { ArrowRight, ArrowUpRight, BookOpen, Headphones, Languages, MessageCircle } from 'lucide-react'
import PricingSection from '@/components/billing/PricingSection'
import { LandingFAQ } from '@/components/ui/landing-faq'
import { LandingNav } from '@/components/ui/landing-nav'
import { LanguageBubbles, SUPPORTED_LANGUAGE_COUNT } from '@/components/LanguageBubbles'
import { LandingFooter } from '@/components/landing/LandingFooter'
import type { ReviewPublic } from '@/types/api'

export const metadata: Metadata = {
  title: 'JUBA LISAN: AI-Powered Language Learning Platform',
  description:
    'Learn languages naturally with your personal AI tutor. Master real-time voice conversations, structured CEFR lessons, interactive reading and listening, and smart flashcards.',
  robots: { index: true, follow: true },
  openGraph: {
    title: 'JUBA LISAN: AI-Powered Language Learning Platform',
    description: 'Learn languages naturally with your personal AI tutor.',
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
  const reviewT = await getTranslations('landingReviews')

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
    if (reviewsRes.ok) reviews = (await reviewsRes.json()).filter((review: ReviewPublic) => review.comment?.trim())
  } catch {
    // Landing data is non-fatal.
  }

  const rtl = locale === 'ar'

  return (
    <main className="juba-busuu-landing min-h-screen overflow-x-hidden" dir={rtl ? 'rtl' : 'ltr'} lang={locale}>
      <LandingNav
        hasSession={hasSession}
        dir={rtl ? 'rtl' : 'ltr'}
        navFeatures={t('navFeatures')}
        navLanguages={t('navLanguages')}
        navReviews={t('navReviews')}
        navPricing={t('navPricing')}
        navFAQ={t('navFAQ')}
        showReviews={reviews.length > 0}
        signIn={t('signIn')}
        dashboard={t('dashboard')}
        getStarted={t('ctaStart')}
        homeLabel={t('homeLabel')}
        openMenuLabel={t('openMenuLabel')}
        closeMenuLabel={t('closeMenuLabel')}
        locale={locale as Locale}
      />

      <section className="juba-busuu-hero" aria-labelledby="landing-hero-title">
        <div className="juba-busuu-container juba-busuu-hero-grid">
          <div className="juba-busuu-hero-copy">
            <span className="juba-busuu-eyebrow">{t('heroBadge')}</span>
            <h1 id="landing-hero-title">{t('heroTitle')}</h1>
            <p>{t('heroSub')}</p>
            <div className="juba-busuu-actions">
              <Link href={hasSession ? '/dashboard' : '/register'} className="juba-busuu-primary">
                {hasSession ? t('dashboard') : t('ctaStart')}
                <ArrowRight className={rtl ? 'rotate-180' : ''} aria-hidden="true" />
              </Link>
              <a href="#languages" className="juba-busuu-secondary">{t('ctaExplore')}</a>
            </div>
            <div className="juba-busuu-hero-proof" aria-label={t('featureSectionLabel')}>
              <span><strong>CEFR</strong>{t('proofCefr')}</span>
              <span><strong>AI</strong>{t('proofTutor')}</span>
              <span><strong>VOICE</strong>{t('proofVoice')}</span>
            </div>
          </div>
          <div className="juba-busuu-hero-visual">
            <div className="juba-busuu-hero-disc" aria-hidden="true" />
            <Image src="/landing/juba-hero-characters.svg" alt={t('heroTitle')} width={900} height={700} priority />
          </div>
        </div>
      </section>

      <section id="languages" className="juba-busuu-language-discovery" aria-labelledby="language-title">
        <div className="juba-busuu-container">
          <div className="juba-busuu-heading">
            <span className="juba-busuu-eyebrow">{t('languagesEyebrow')}</span>
            <h2 id="language-title">{t('languagesHeadline')}</h2>
            <p>{t('languagesDescription')}</p>
          </div>
          <div className="juba-busuu-language-panel">
            <div className="juba-busuu-language-prompt">
              <span>{t('languagesEyebrow')}</span>
              <strong>{t('languagesHeadline')}</strong>
            </div>
            <LanguageBubbles dir={rtl ? 'rtl' : 'ltr'} />
          </div>
        </div>
      </section>

      <section className="juba-busuu-stats" aria-label={t('featureSectionLabel')}>
        <div className="juba-busuu-container juba-busuu-stats-grid">
          <article><strong>{SUPPORTED_LANGUAGE_COUNT}</strong><span>{t('supportedLanguages')}</span></article>
          <article><strong>A1–C2</strong><span>{t('proofCefr')}</span></article>
          <article><strong>AI</strong><span>{t('proofTutor')}</span></article>
          <article><strong>VOICE</strong><span>{t('proofVoice')}</span></article>
        </div>
      </section>

      <section id="features" className="juba-busuu-difference" aria-labelledby="difference-title">
        <div className="juba-busuu-container">
          <div className="juba-busuu-heading juba-busuu-heading-split">
            <div>
              <span className="juba-busuu-eyebrow">{t('featureSectionLabel')}</span>
              <h2 id="difference-title">{t('bentoTitle')}</h2>
            </div>
            <p>{t('bentoSubtitle')}</p>
          </div>
          <div className="juba-busuu-feature-grid">
            <Link href="/reading" className="juba-busuu-feature">
              <Image src="/landing/juba-reading.svg" alt="" width={360} height={250} />
              <div className="juba-busuu-feature-body">
                <span>{t('featureSectionLabel')}</span>
                <h3>{t('feature5Title')}</h3>
                <p>{t('feature5Desc')}</p>
                <ArrowUpRight className="juba-busuu-feature-arrow" aria-hidden="true" />
              </div>
            </Link>
            <Link href="/chat" className="juba-busuu-feature">
              <Image src="/landing/juba-chat.svg" alt="" width={360} height={250} />
              <div className="juba-busuu-feature-body">
                <span>{t('flowAiLabel')}</span>
                <h3>{t('feature2Title')}</h3>
                <p>{t('feature2Desc')}</p>
                <ArrowUpRight className="juba-busuu-feature-arrow" aria-hidden="true" />
              </div>
            </Link>
            <Link href="/listening" className="juba-busuu-feature">
              <Image src="/landing/juba-listening.svg" alt="" width={360} height={250} />
              <div className="juba-busuu-feature-body">
                <span>{t('flowVoiceLabel')}</span>
                <h3>{t('feature3Title')}</h3>
                <p>{t('feature3Desc')}</p>
                <ArrowUpRight className="juba-busuu-feature-arrow" aria-hidden="true" />
              </div>
            </Link>
          </div>
        </div>
      </section>

      {reviews.length > 0 && (
        <section id="reviews" className="juba-busuu-testimonials" aria-labelledby="reviews-title">
          <div className="juba-busuu-container">
            <div className="juba-busuu-heading">
              <span className="juba-busuu-eyebrow">{reviewT('eyebrow')}</span>
              <h2 id="reviews-title">{reviewT('title')}</h2>
              <p>{reviewT('subtitle')}</p>
            </div>
            <div className="juba-busuu-testimonial-grid">
              {reviews.slice(0, 6).map((review) => (
                <article key={review.id} className="juba-busuu-testimonial">
                  <div className="juba-busuu-testimonial-meta">
                    <span aria-label={reviewT('starsLabel', { rating: review.rating })}>
                      {'★'.repeat(Math.max(0, Math.min(5, review.rating)))}
                    </span>
                    <span>{reviewT('learningLanguage', { language: review.target_language })}</span>
                  </div>
                  <p>“{review.comment ?? ''}”</p>
                  <strong>{review.user_display_name || 'JUBA LISAN learner'}</strong>
                </article>
              ))}
            </div>
          </div>
        </section>
      )}

      <section className="juba-busuu-slogan" aria-hidden="true">
        <div className="juba-busuu-slogan-track">
          <span>{t('languagesHeadline')}</span><b>•</b><span>{t('flowVoiceTitle')}</span><b>•</b><span>{t('flowAiTitle')}</span><b>•</b>
          <span>{t('languagesHeadline')}</span><b>•</b><span>{t('flowVoiceTitle')}</span><b>•</b><span>{t('flowAiTitle')}</span>
        </div>
      </section>

      <section className="juba-busuu-practical" aria-labelledby="practical-title">
        <div className="juba-busuu-container juba-busuu-practical-grid">
          <div className="juba-busuu-practical-copy">
            <span className="juba-busuu-eyebrow">{t('flowEyebrow')}</span>
            <h2 id="practical-title">{t('flowHeadline')}</h2>
            <p>{t('flowDescription')}</p>
            <Link href={hasSession ? '/dashboard' : '/register'} className="juba-busuu-primary">
              {hasSession ? t('dashboard') : t('ctaStart')}
              <ArrowRight className={rtl ? 'rotate-180' : ''} aria-hidden="true" />
            </Link>
          </div>
          <div className="juba-busuu-practical-media">
            <Image src="/landing/juba-learning-journey.svg" alt="" width={760} height={620} />
          </div>
        </div>
      </section>

      <section id="benefits" className="juba-busuu-benefits" aria-labelledby="benefits-title">
        <div className="juba-busuu-container">
          <div className="juba-busuu-heading">
            <span className="juba-busuu-eyebrow">{t('featureSectionLabel')}</span>
            <h2 id="benefits-title">{t('builtForLearners')}</h2>
          </div>
          <div className="juba-busuu-benefit-list">
            <article><BookOpen aria-hidden="true" /><div><h3>{t('feature1Title')}</h3><p>{t('feature1Desc')}</p></div></article>
            <article><MessageCircle aria-hidden="true" /><div><h3>{t('feature6Title')}</h3><p>{t('feature6Desc')}</p></div></article>
            <article><Headphones aria-hidden="true" /><div><h3>{t('feature8Title')}</h3><p>{t('feature8Desc')}</p></div></article>
            <article><Languages aria-hidden="true" /><div><h3>{t('feature7Title')}</h3><p>{t('feature7Desc')}</p></div></article>
          </div>
        </div>
      </section>

      <section id="pricing" className="juba-busuu-pricing">
        <div className="juba-busuu-container">
          <div className="juba-busuu-heading">
            <span className="juba-busuu-eyebrow">{t('navPricing')}</span>
            <h2>{t('navPricing')}</h2>
          </div>
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
      </section>

      <section id="faq" className="juba-busuu-faq">
        <div className="juba-busuu-container">
          <div className="juba-busuu-heading">
            <span className="juba-busuu-eyebrow">{t('navFAQ')}</span>
            <h2>{t('faqTitle')}</h2>
          </div>
          <LandingFAQ dir={rtl ? 'rtl' : 'ltr'} />
        </div>
      </section>

      <section className="juba-busuu-final-cta">
        <div className="juba-busuu-container juba-busuu-final-cta-inner">
          <div>
            <span className="juba-busuu-eyebrow">{t('featureSectionLabel')}</span>
            <h2>{t('builtForLearners')}</h2>
            <p>{t('flowDescription')}</p>
            <Link href={hasSession ? '/dashboard' : '/register'} className="juba-busuu-primary">
              {hasSession ? t('dashboard') : t('ctaStart')}
              <ArrowRight className={rtl ? 'rotate-180' : ''} aria-hidden="true" />
            </Link>
          </div>
          <Image src="/landing/juba-hero-characters.svg" alt="" width={700} height={520} />
        </div>
      </section>

      <LandingFooter t={t} dir={rtl ? 'rtl' : 'ltr'} showReviews={reviews.length > 0} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
    </main>
  )
}
