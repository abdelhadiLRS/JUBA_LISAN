import Link from 'next/link'
import Script from 'next/script'
import { cookies } from 'next/headers'
import { getLocale, getTranslations } from 'next-intl/server'
import type { Metadata } from 'next'
import type { Locale } from '@/lib/locales'
import { ArrowRight, BookOpen, Headphones, MessageCircle, Sparkles, Volume2 } from 'lucide-react'
import PricingSection from '@/components/billing/PricingSection'
import { LandingFAQ } from '@/components/ui/landing-faq'
import { LandingNav } from '@/components/ui/landing-nav'
import { LanguageBubbles } from '@/components/LanguageBubbles'
import { LandingFooter } from '@/components/landing/LandingFooter'
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
    <main className="juba-reference-page min-h-screen overflow-x-hidden">
      <Script
        id="juba-lisan-structured-data"
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

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

      {/* HERO — the visitor-facing composition is deliberately rebuilt around the supplied reference:
          oversized playful type, pale paper background, organic illustration, floating cards and a single CTA. */}
      <section className="juba-ref-hero">
        <div className="juba-ref-hero-shape shape-yellow" aria-hidden="true" />
        <div className="juba-ref-hero-shape shape-green" aria-hidden="true" />
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

          <div className="juba-ref-hero-art" aria-hidden="true">
            <div className="juba-ref-cloud cloud-a" />
            <div className="juba-ref-cloud cloud-b" />
            <div className="juba-ref-sun" />
            <div className="juba-ref-ground" />
            <div className="juba-ref-character character-main">
              <div className="character-face"><i /><i /><b /></div>
              <span>J</span>
            </div>
            <div className="juba-ref-character character-small character-one"><span>EN</span></div>
            <div className="juba-ref-character character-small character-two"><span>FR</span></div>
            <div className="juba-ref-character character-small character-three"><span>ES</span></div>
            <div className="juba-ref-speech speech-one">Hello!</div>
            <div className="juba-ref-speech speech-two">Bonjour!</div>
            <div className="juba-ref-book"><BookOpen className="h-7 w-7" /><strong>JUBA LISAN</strong><small>Learn · Practice · Progress</small></div>
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
            <div className="pillar-icon"><BookOpen /></div>
            <span>{t('languagesEyebrow')}</span>
            <h3>{t('languagesHeadline')}</h3>
            <p>{t('languagesDescription')}</p>
            <ArrowRight />
          </Link>
          <Link href="/listening" className="juba-ref-pillar pillar-blue">
            <div className="pillar-icon"><Headphones /></div>
            <span>{t('flowVoiceLabel')}</span>
            <h3>{t('flowVoiceTitle')}</h3>
            <p>{t('flowVoiceDescription')}</p>
            <ArrowRight />
          </Link>
          <Link href="/chat" className="juba-ref-pillar pillar-yellow">
            <div className="pillar-icon"><MessageCircle /></div>
            <span>{t('flowAiLabel')}</span>
            <h3>{t('flowAiTitle')}</h3>
            <p>{t('flowAiDescription')}</p>
            <ArrowRight />
          </Link>
        </div>
      </section>

      {/* LANGUAGE SECTION — uses the real supported-language component. */}
      <section id="languages" className="juba-ref-language-section">
        <div className="juba-ref-language-copy">
          <span className="juba-ref-kicker">{t('languagesEyebrow')}</span>
          <h2>{t('languagesHeadline')}</h2>
          <p>{t('languagesDescription')}</p>
          <Link href="/register" className="juba-ref-button">{t('ctaStart')} <ArrowRight className="h-4 w-4" /></Link>
        </div>
        <div className="juba-ref-language-art">
          <LanguageBubbles />
        </div>
      </section>

      {/* AI / VOICE STORY — one visual block instead of the old dashboard-heavy landing. */}
      <section id="demo" className="juba-ref-ai-section">
        <div className="juba-ref-ai-art" aria-hidden="true">
          <div className="ai-orbit orbit-one" />
          <div className="ai-orbit orbit-two" />
          <div className="ai-avatar"><Sparkles /></div>
          <div className="ai-bubble bubble-user">Can we practice today?</div>
          <div className="ai-bubble bubble-ai">Of course — let's speak naturally.</div>
          <div className="ai-wave"><i /><i /><i /><i /><i /><i /><i /></div>
        </div>
        <div className="juba-ref-ai-copy">
          <span className="juba-ref-kicker">{t('flowAiLabel')}</span>
          <h2>{t('flowAiTitle')}</h2>
          <p>{t('flowAiDescription')}</p>
          <div className="juba-ref-ai-points">
            <span><Volume2 /> {t('proofVoice')}</span>
            <span><Sparkles /> {t('proofTutor')}</span>
          </div>
          <Link href="/conversation" className="juba-ref-button">{t('ctaStart')} <ArrowRight className="h-4 w-4" /></Link>
        </div>
      </section>

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
      <section id="pricing" className="juba-ref-pricing">
        <PricingSection
          stripeEnabled={stripeEnabled}
          trialDays={trialDays}
          hasSession={hasSession}
          priceMonthly={priceMonthly}
          priceYearly={priceYearly}
          totalPriceMonthly={totalPriceMonthly}
          totalPriceYearly={totalPriceYearly}
        />
      </section>

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
          <div className="juba-ref-cta-device" aria-hidden="true">
            <div className="device-top">JUBA LISAN</div>
            <div className="device-star">✦</div>
            <div className="device-lines"><i /><i /><i /></div>
          </div>
        </div>
      </section>

      <section id="faq" className="juba-ref-faq">
        <div className="juba-ref-section-heading">
          <span className="juba-ref-kicker">{t('navFAQ')}</span>
          <h2>{t('faqTitle')}</h2>
        </div>
        <LandingFAQ />
      </section>

      <LandingFooter t={t} />
    </main>
  )
}
