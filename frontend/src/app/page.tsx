import Link from 'next/link'
import Image from 'next/image'
import { cookies } from 'next/headers'
import { getLocale, getTranslations } from 'next-intl/server'
import type { Metadata } from 'next'
import PricingSection from '@/components/billing/PricingSection'
import { LandingFAQ } from '@/components/ui/landing-faq'
import { LandingNav } from '@/components/ui/landing-nav'
import { ScrollReveal } from '@/components/ui/scroll-reveal'
import { ContactButton } from '@/components/ui/contact-button'
import { LanguageBubbles, SUPPORTED_LANGUAGE_COUNT } from '@/components/LanguageBubbles'
import { LandingReviewsCarousel } from '@/components/reviews/LandingReviewsCarousel'
import type { ReviewPublic } from '@/types/api'
import { normalizeLocale } from '@/lib/locales'

export const metadata: Metadata = {
  title: 'JUBA LISAN — Learn languages naturally with AI',
  description:
    'Learn languages naturally with AI through speaking, listening, reading, vocabulary, grammar, and personalized practice.',
  robots: { index: true, follow: true },
  openGraph: {
    title: 'JUBA LISAN — AI-powered language learning',
    description:
      'Learn languages naturally with AI through speaking, listening, reading, vocabulary, grammar, and personalized practice.',
    url: 'https://jubalisan.com',
    type: 'website',
    images: [
      {
        url: '/og-image-v2.png',
        width: 1200,
        height: 630,
        alt: 'JUBA LISAN — AI-powered language learning',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'JUBA LISAN — AI-powered language learning',
    description:
      'Learn languages with an AI tutor, real-time voice conversations, spaced-repetition flashcards, and structured grammar lessons.',
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
    'JUBA LISAN is an AI-powered language learning platform with conversation, vocabulary, grammar, listening, reading, and personalized learning.',
  
  offers: {
    '@type': 'Offer',
    price: '0',
    priceCurrency: 'USD',
  },
}

export default async function Home() {
  const cookieStore = await cookies()
  const hasSession = cookieStore.has('refresh_token')
  const locale = normalizeLocale(await getLocale())
  const dir = locale === 'ar' ? 'rtl' : 'ltr'
  const t = await getTranslations('landing')
  const tCommon = await getTranslations('common')
  const tBilling = await getTranslations('billing')

  let allowRegistration = false
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
      // Landing CTAs can lag registration changes by the existing one-hour cache.
      // The backend still enforces ALLOW_REGISTRATION on every signup request.
      fetch(`${backendUrl}/api/config`, { next: { revalidate: 3600 } }),
      fetch(`${backendUrl}/api/reviews/public?limit=100`, {
        next: { revalidate: 300 },
      }).catch(() => null),
    ])
    if (configRes.ok) {
      const cfg = await configRes.json()
      allowRegistration = cfg.allow_registration === true
      stripeEnabled = cfg.stripe_enabled ?? false
      trialDays = cfg.stripe_trial_days ?? 7
      priceMonthly = cfg.price_monthly ?? 0.0
      priceYearly = cfg.price_yearly ?? 0.0
      totalPriceMonthly = cfg.total_price_monthly ?? 0.0
      totalPriceYearly = cfg.total_price_yearly ?? 0.0
    }
    if (reviewsRes?.ok) {
      reviews = await reviewsRes.json()
    }
  } catch {
    /* non-fatal */
  }

  return (
    <div className="juba-busuu-page flex min-h-screen flex-col">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Nav */}
      <LandingNav
        hasSession={hasSession}
        allowRegistration={allowRegistration}
        dir={dir}
        navFeatures={t('navFeatures')}
        primaryNavigation={tCommon('menu')}
        navLanguages={t('navLanguages')}
        interfaceLanguages={t('interfaceLanguages')}
        navReviews={t('navReviews')}
        showReviews={reviews.length > 0}
        signIn={t('signIn')}
        dashboard={t('dashboard')}
        getStarted={t('ctaStart')}
        homeLabel={t('homeLabel')}
        openMenuLabel={t('openMenuLabel')}
        closeMenuLabel={t('closeMenuLabel')}
        locale={locale}
      />

      {/* Busuu reference hero: centered blue composition with the visual anchored below the CTA */}
      <section className="juba-busuu-reference-hero">
        <div className="juba-busuu-reference-hero-inner">
          <div className="juba-busuu-reference-hero-copy">
            <span className="juba-busuu-reference-kicker">{tCommon('tagline')}</span>
            <h1>{t('heroTitle')}</h1>
            <p>{t('heroSub')}</p>
            <div className="juba-busuu-reference-actions">
              <Link
                href={
                  hasSession
                    ? '/dashboard'
                    : allowRegistration
                      ? '/register'
                      : '/login'
                }
                className="juba-busuu-reference-primary"
              >
                {hasSession
                  ? t('dashboard')
                  : allowRegistration
                    ? tCommon('start')
                    : t('signIn')}
              </Link>
            </div>
          </div>

          <div className="juba-busuu-reference-hero-art">
            <img
              src="https://raw.githubusercontent.com/abdelhadiLRS/JUBA_LISAN/main/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/en-paid-landing.avif"
              alt=""
              aria-hidden="true"
            />
          </div>
        </div>
      </section>

      {/* Busuu reference language chooser */}
      <section id="languages" className="juba-busuu-reference-languages scroll-mt-24">
        <div className="juba-busuu-reference-languages-inner">
          <h2>{t('navLanguages')}</h2>
          <LanguageBubbles dir={dir} />
        </div>
      </section>

      <section className="juba-busuu-proof-strip" aria-label={t('navFeatures')}>
        <div className="juba-busuu-proof-inner">
          <div className="juba-busuu-proof-stat">
            <strong>{SUPPORTED_LANGUAGE_COUNT}+</strong>
            <span>{t('navLanguages')}</span>
          </div>
          <div className="juba-busuu-proof-divider" aria-hidden="true" />
          <div className="juba-busuu-proof-item">
            <span className="juba-busuu-proof-check" aria-hidden="true">✓</span>
            <span>{t('feature1Title')}</span>
          </div>
          <div className="juba-busuu-proof-divider" aria-hidden="true" />
          <div className="juba-busuu-proof-item">
            <span className="juba-busuu-proof-check" aria-hidden="true">✓</span>
            <span>{t('feature2Title')}</span>
          </div>
          <div className="juba-busuu-proof-divider" aria-hidden="true" />
          <div className="juba-busuu-proof-item">
            <span className="juba-busuu-proof-check" aria-hidden="true">✓</span>
            <span>{t('feature3Title')}</span>
          </div>
        </div>
      </section>

      {/* Busuu-style differentiation section */}
      <ScrollReveal>
        <section id="features" className="juba-busuu-different scroll-mt-16">
          <div className="juba-busuu-different-inner">
            <div className="juba-busuu-different-heading">
              <span className="juba-busuu-eyebrow">{tCommon('tagline')}</span>
              <h2>{t('navFeatures')}</h2>
            </div>

            <div className="juba-busuu-different-grid">
              {[
                {
                  title: t('feature1Title'),
                  desc: t('feature1Desc'),
                  image:
                    'https://raw.githubusercontent.com/abdelhadiLRS/JUBA_LISAN/main/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/what-makes-busuu-different-1-real_people__1_.png',
                },
                {
                  title: t('feature2Title'),
                  desc: t('feature2Desc'),
                  image:
                    'https://raw.githubusercontent.com/abdelhadiLRS/JUBA_LISAN/main/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/what-makes-busuu-different-2-supportive-community.png',
                },
                {
                  title: t('feature3Title'),
                  desc: t('feature3Desc'),
                  image:
                    'https://raw.githubusercontent.com/abdelhadiLRS/JUBA_LISAN/main/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/what-makes-busuu-different-3-express-yourself__1_.png',
                },
              ].map(({ title, desc, image }) => (
                <article key={title} className="juba-busuu-different-card">
                  <div className="juba-busuu-different-media">
                    <img src={image} alt="" aria-hidden="true" loading="lazy" />
                  </div>
                  <div className="juba-busuu-different-copy">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
      </ScrollReveal>

      {/* Reviews */}
      <ScrollReveal>
        <section id="reviews" className="juba-busuu-testimonials scroll-mt-16">
          <div className="juba-busuu-testimonials-inner">
            <LandingReviewsCarousel reviews={reviews} />
          </div>
        </section>
      </ScrollReveal>

      {/* Pricing */}
      <ScrollReveal>
        <div id="pricing" className="juba-busuu-pricing scroll-mt-16">
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

      {/* Open Source */}
      <ScrollReveal>
        <section className="juba-busuu-open-source-section">
          <div className="juba-busuu-open-source flex flex-col items-center justify-between gap-5 sm:flex-row">
            <div className="flex items-center gap-4">
              <Image
                src="/github.svg"
                alt="GitHub"
                width={20}
                height={20}
                className="block opacity-80"
              />
              <div className="text-start">
                <p className="juba-busuu-open-source-title font-sans text-sm font-bold tracking-tight">
                  {tBilling('openSourceTitle')}
                </p>
                <p className="juba-busuu-open-source-description mt-1 text-xs font-semibold tracking-wide">
                  {tBilling('openSourceDesc')}
                </p>
              </div>
            </div>
            <a
              href="https://github.com/abdelhadiLRS/JUBA_LISAN"
              target="_blank"
              rel="noopener noreferrer"
              className="juba-busuu-open-source-cta border px-6 py-3 text-xs font-bold tracking-wide whitespace-nowrap transition-colors"
            >
              {tBilling('openSourceCta')}
            </a>
          </div>
        </section>
      </ScrollReveal>

      {/* FAQ */}
      <ScrollReveal>
        <section id="faq" className="juba-busuu-faq-section scroll-mt-16">
          <h2 className="juba-busuu-faq-title mb-8 text-center font-sans text-sm font-bold tracking-wide">
            {t('faqTitle')}
          </h2>
          <LandingFAQ dir={dir} />
        </section>
      </ScrollReveal>

      {/* Footer */}
      <footer className="juba-busuu-footer border-t px-6 py-10">
        <div className="mx-auto grid max-w-4xl grid-cols-2 gap-8 md:grid-cols-4">
          <div>
            <span className="juba-busuu-footer-brand block text-xs font-bold tracking-widest uppercase">
              JUBA LISAN
            </span>
            <span className="juba-busuu-footer-copyright mt-2 block text-xs leading-relaxed">
              © {new Date().getFullYear()}
            </span>
          </div>
          <div>
            <h4 className="juba-busuu-footer-heading mb-3 font-sans text-sm font-bold tracking-tight">
              {t('footerProduct')}
            </h4>
            <div className="flex flex-col gap-2">
              <a
                href="https://github.com/abdelhadiLRS/JUBA_LISAN"
                target="_blank"
                rel="noopener noreferrer"
                className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors"
              >
                {t('github')}
              </a>
            </div>
          </div>
          <div>
            <h4 className="juba-busuu-footer-heading mb-3 font-sans text-sm font-bold tracking-tight">
              {t('footerLegal')}
            </h4>
            <div className="flex flex-col gap-2">
              <Link
                href="/privacy?from=landing"
                className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors"
              >
                {t('privacy')}
              </Link>
              <Link
                href="/terms?from=landing"
                className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors"
              >
                {t('terms')}
              </Link>
            </div>
          </div>
          <div>
            <h4 className="juba-busuu-footer-heading mb-3 font-sans text-sm font-bold tracking-tight">
              {t('contact')}
            </h4>
            <div className="flex flex-col gap-2">
              <a
                href="https://www.arturocarreterocalvo.com"
                target="_blank"
                rel="noopener noreferrer"
                className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors"
              >
                {t('aboutMe')}
              </a>
              <ContactButton />
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
