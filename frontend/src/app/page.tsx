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
    <div dir={dir} className="juba-busuu-page flex min-h-screen flex-col">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <a className="juba-busuu-skip-link" href="#main-content">
        {t('skipToContent')}
      </a>

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
        navPricing={t('navPricing')}
        showReviews={reviews.length > 0}
        signIn={t('signIn')}
        dashboard={t('dashboard')}
        getStarted={t('ctaStart')}
        homeLabel={t('homeLabel')}
        openMenuLabel={t('openMenuLabel')}
        closeMenuLabel={t('closeMenuLabel')}
        locale={locale}
      />

      <main id="main-content">
      {/* Busuu reference hero: centered blue composition with the visual anchored below the CTA */}
      <section data-editorial-section="00" className="juba-busuu-reference-hero" aria-labelledby="landing-hero-title">
        <div className="juba-busuu-reference-hero-inner">
          <div className="juba-busuu-reference-hero-copy">
            <div className="juba-busuu-hero-meta" aria-hidden="true">
              <span>JUBA LISAN</span>
              <span>AI LANGUAGE LEARNING</span>
            </div>
            <span className="juba-busuu-reference-kicker">{tCommon('tagline')}</span>
            <h1 id="landing-hero-title">{t('heroTitle')}</h1>
            <p>{t('heroSub')}</p>
            <div className="juba-busuu-reference-actions">
              <img
                src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/left-wing.png"
                alt=""
                aria-hidden="true"
                className="juba-busuu-reference-wing juba-busuu-reference-wing-left"
              />
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
              <img
                src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/right-wing.png"
                alt=""
                aria-hidden="true"
                className="juba-busuu-reference-wing juba-busuu-reference-wing-right"
              />
            </div>
            <div className="juba-busuu-hero-benefits" aria-label={t('navFeatures')}>
              <span><b aria-hidden="true">✓</b>{t('feature1Title')}</span>
              <span><b aria-hidden="true">✓</b>{t('feature2Title')}</span>
              <span><b aria-hidden="true">✓</b>{t('feature3Title')}</span>
            </div>
          </div>

          <div className="juba-busuu-reference-hero-art">
            <div className="juba-busuu-hero-float juba-busuu-hero-float-left">
              <span>01</span>
              <strong>{t('feature1Title')}</strong>
            </div>
            <div className="juba-busuu-hero-float juba-busuu-hero-float-right">
              <span>02</span>
              <strong>{t('feature2Title')}</strong>
            </div>
            <div className="juba-busuu-hero-float juba-busuu-hero-float-bottom">
              <span>03</span>
              <strong>{t('feature3Title')}</strong>
            </div>
            <img
              src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/en-paid-landing.avif"
              alt=""
              aria-hidden="true"
              fetchPriority="high"
              decoding="async"
            />
          </div>
        </div>
      </section>

      {/* Strong editorial language destination */}
      <section id="languages" data-editorial-section="01" className="juba-busuu-reference-languages scroll-mt-24" aria-labelledby="landing-languages-title">
        <div className="juba-busuu-reference-languages-inner">
          <div className="juba-busuu-language-intro">
            <div>
              <span className="juba-busuu-eyebrow">{tCommon('tagline')}</span>
              <h2 id="landing-languages-title">{t('navLanguages')}</h2>
            </div>
            <p>{t('heroSub')}</p>
          </div>
          <div className="juba-busuu-language-stage">
            <LanguageBubbles dir={dir} />
          </div>
          <div className="juba-busuu-language-bottom">
            <span>{SUPPORTED_LANGUAGE_COUNT}+ languages</span>
            <Link
              href={hasSession ? '/dashboard' : allowRegistration ? '/register' : '/login'}
              className="juba-busuu-language-cta-link"
            >
              {hasSession ? t('dashboard') : allowRegistration ? t('ctaStart') : t('signIn')} <span aria-hidden="true">↗</span>
            </Link>
          </div>
        </div>
      </section>

      <section data-editorial-section="01A" className="juba-busuu-proof-strip" aria-labelledby="landing-proof-title">
        <div className="juba-busuu-proof-inner">
          <h2 id="landing-proof-title" className="sr-only">{t('navFeatures')}</h2>
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

      {/* Busuu-style real-world learning section */}
      <ScrollReveal>
        <section data-editorial-section="02" className="juba-busuu-real-world" aria-labelledby="landing-real-world-title">
          <div className="juba-busuu-real-world-inner">
            <div className="juba-busuu-real-world-heading">
              <span className="juba-busuu-eyebrow">{tCommon('tagline')}</span>
              <h2 id="landing-real-world-title">{t('heroTitle')}</h2>
              <p>{t('heroSub')}</p>
            </div>
            <div className="juba-busuu-real-world-grid">
              {[
                {
                  label: t('feature1Title'),
                  copy: t('feature1Desc'),
                  icon: '01',
                  tone: 'blue',
                },
                {
                  label: t('feature2Title'),
                  copy: t('feature2Desc'),
                  icon: '02',
                  tone: 'green',
                },
                {
                  label: t('feature3Title'),
                  copy: t('feature3Desc'),
                  icon: '03',
                  tone: 'cream',
                },
              ].map(({ label, copy, icon, tone }) => (
                <article
                  key={label}
                  className={`juba-busuu-real-world-card juba-busuu-real-world-card--${tone}`}
                >
                  <div className="juba-busuu-real-world-card-top">
                    <span className="juba-busuu-real-world-index">{icon}</span>
                    <span className="juba-busuu-real-world-mark" aria-hidden="true">↗</span>
                  </div>
                  <div className="juba-busuu-real-world-copy">
                    <h3>{label}</h3>
                    <p>{copy}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
      </ScrollReveal>

      {/* Busuu-style differentiation section */}
      <ScrollReveal>
        <section id="features" data-editorial-section="03" className="juba-busuu-different scroll-mt-16" aria-labelledby="landing-features-title">
          <div className="juba-busuu-different-inner">
            <div className="juba-busuu-different-heading">
              <span className="juba-busuu-eyebrow">{tCommon('tagline')}</span>
              <h2 id="landing-features-title">{t('navFeatures')}</h2>
            </div>

            <div className="juba-busuu-different-grid">
              {[
                {
                  title: t('feature1Title'),
                  desc: t('feature1Desc'),
                  image:
                    '/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/what-makes-busuu-different-1-real_people__1_.png',
                },
                {
                  title: t('feature2Title'),
                  desc: t('feature2Desc'),
                  image:
                    '/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/what-makes-busuu-different-2-supportive-community.png',
                },
                {
                  title: t('feature3Title'),
                  desc: t('feature3Desc'),
                  image:
                    '/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/what-makes-busuu-different-3-express-yourself__1_.png',
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
        <section id="reviews" data-editorial-section="04" className="juba-busuu-testimonials scroll-mt-16" aria-labelledby="landing-reviews-title">
          <div className="juba-busuu-testimonials-inner">
            <h2 id="landing-reviews-title" className="sr-only">{t('navReviews')}</h2>
            <LandingReviewsCarousel reviews={reviews} />
          </div>
        </section>
      </ScrollReveal>

      {/* Busuu-style "why learn" editorial section */}
      <ScrollReveal>
        <section data-editorial-section="05" className="juba-busuu-why-learn" aria-labelledby="landing-why-learn-title">
          <div className="juba-busuu-why-learn-inner">
            <div className="juba-busuu-why-learn-heading">
              <span className="juba-busuu-eyebrow">{tCommon('tagline')}</span>
              <h2 id="landing-why-learn-title">{t('navFeatures')}</h2>
              <p>{t('heroSub')}</p>
            </div>
            <div className="juba-busuu-why-learn-grid">
              {[
                { number: '01', title: t('feature1Title'), desc: t('feature1Desc') },
                { number: '02', title: t('feature2Title'), desc: t('feature2Desc') },
                { number: '03', title: t('feature3Title'), desc: t('feature3Desc') },
              ].map(({ number, title, desc }) => (
                <article key={title} className="juba-busuu-why-learn-card">
                  <span className="juba-busuu-why-learn-number" aria-hidden="true">{number}</span>
                  <h3>{title}</h3>
                  <p>{desc}</p>
                </article>
              ))}
            </div>
            <div className="juba-busuu-why-learn-cta">
              <Link
                href={hasSession ? '/dashboard' : allowRegistration ? '/register' : '/login'}
                className="juba-busuu-reference-primary"
              >
                {hasSession ? t('dashboard') : allowRegistration ? tCommon('start') : t('signIn')}
              </Link>
            </div>
          </div>
        </section>
      </ScrollReveal>

      {/* Pricing */}
      <ScrollReveal>
        <section id="pricing" data-editorial-section="06" className="juba-busuu-pricing scroll-mt-16" aria-labelledby="landing-pricing-title">
          <h2 id="landing-pricing-title" className="sr-only">{t('navPricing')}</h2>
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
      </ScrollReveal>

      {/* Busuu-style app download band */}
      <ScrollReveal>
        <section data-editorial-section="07" className="juba-busuu-app-section" aria-labelledby="app-download-title">
          <div className="juba-busuu-app-inner">
            <div className="juba-busuu-app-copy">
              <span className="juba-busuu-eyebrow">{tCommon('tagline')}</span>
              <h2 id="app-download-title">{t('heroTitle')}</h2>
              <p>{t('heroSub')}</p>
              <div className="juba-busuu-app-badges">
                <Link
                  href={hasSession ? '/dashboard' : allowRegistration ? '/register' : '/login'}
                  className="juba-busuu-app-cta"
                >
                  {hasSession ? t('dashboard') : allowRegistration ? tCommon('start') : t('signIn')}
                </Link>
              </div>
            </div>
            <div className="juba-busuu-app-art" aria-hidden="true">
              <img
                className="juba-busuu-app-branch-left"
                loading="lazy"
                decoding="async"
                src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/tree-branch-left.svg"
                alt=""
              />
              <img
                className="juba-busuu-app-convector"
                loading="lazy"
                decoding="async"
                src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/convector-green.svg"
                alt=""
              />
              <img
                className="juba-busuu-app-branch-right"
                loading="lazy"
                decoding="async"
                src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/tree-branch-right.svg"
                alt=""
              />
              <img
                className="juba-busuu-app-triangle-up"
                loading="lazy"
                decoding="async"
                src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/triangle-up.svg"
                alt=""
              />
              <img
                className="juba-busuu-app-triangle-down"
                loading="lazy"
                decoding="async"
                src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/triangle-down.svg"
                alt=""
              />
            </div>
          </div>
        </section>
      </ScrollReveal>

      {/* Busuu reference: New languages editorial banner */}
      <ScrollReveal>
        <section data-editorial-section="07A" className="juba-busuu-new-languages" aria-label={t('tickerNewLanguages')}>
          <div className="juba-busuu-new-languages-track">
            {[0, 1].map((group) => (
              <div
                className="juba-busuu-new-languages-group"
                aria-hidden={group === 1}
                key={group}
              >
                <span>{t('tickerNewLanguages')}</span>
                <img
                  src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/Speech.svg"
                  alt=""
                  aria-hidden="true"
                />
                <span>{t('tickerNewOpportunities')}</span>
                <img
                  src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/Speech.svg"
                  alt=""
                  aria-hidden="true"
                />
                <span>{t('tickerNewYou')}</span>
                <img
                  src="/theme/busuu/Learn%20Languages%20Online_%20Start%20for%20Free%20-%20Busuu_files/Speech.svg"
                  alt=""
                  aria-hidden="true"
                />
              </div>
            ))}
          </div>
        </section>
      </ScrollReveal>

      {/* Open Source */}
      <ScrollReveal>
        <section data-editorial-section="07B" className="juba-busuu-open-source-section" aria-labelledby="landing-open-source-title">
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
                <h2 id="landing-open-source-title" className="juba-busuu-open-source-title font-sans text-sm font-bold tracking-tight">
                  {tBilling('openSourceTitle')}
                </h2>
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
        <section id="faq" data-editorial-section="08" className="juba-busuu-faq-section scroll-mt-16" aria-labelledby="landing-faq-title">
          <h2 id="landing-faq-title" className="juba-busuu-faq-title mb-8 text-center font-sans text-sm font-bold tracking-wide">
            {t('faqTitle')}
          </h2>
          <LandingFAQ dir={dir} />
        </section>
      </ScrollReveal>

      </main>

      {/* Footer */}
      <footer data-editorial-section="09" className="juba-busuu-footer border-t px-6 py-10" aria-labelledby="landing-footer-title">
        <h2 id="landing-footer-title" className="sr-only">{t('footerProduct')}</h2>
        <div className="mx-auto grid max-w-6xl grid-cols-2 gap-x-10 gap-y-10 md:grid-cols-3 lg:grid-cols-6">
          <div>
            <span className="juba-busuu-footer-brand block text-xs font-bold tracking-widest uppercase">
              JUBA LISAN
            </span>
            <span className="juba-busuu-footer-copyright mt-2 block text-xs leading-relaxed">
              {t('footerTagline')}
            </span>
            <span className="juba-busuu-footer-copyright mt-3 block text-xs leading-relaxed">
              © {new Date().getFullYear()}
            </span>
          </div>
          <div>
            <h4 className="juba-busuu-footer-heading mb-3 font-sans text-sm font-bold tracking-tight">
              {t('footerProduct')}
            </h4>
            <div className="flex flex-col gap-2">
              <a href="#features" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('navFeatures')}
              </a>
              <a href="#languages" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('navLanguages')}
              </a>
              <a href="#reviews" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('navReviews')}
              </a>
              <a href="#faq" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('faqTitle')}
              </a>
              <a href="#pricing" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('navPricing')}
              </a>
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
              {t('footerLearning')}
            </h4>
            <div className="flex flex-col gap-2">
              <a href="#languages" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('navLanguages')}
              </a>
              <a href="#features" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('navFeatures')}
              </a>
              <a href="#reviews" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('navReviews')}
              </a>
            </div>
          </div>

          <div>
            <h4 className="juba-busuu-footer-heading mb-3 font-sans text-sm font-bold tracking-tight">
              {t('footerResources')}
            </h4>
            <div className="flex flex-col gap-2">
              <a href="#reviews" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('navReviews')}
              </a>
              <a href="#faq" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('navFAQ')}
              </a>
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
              <Link href="/privacy?from=landing" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
                {t('privacy')}
              </Link>
              <Link href="/terms?from=landing" className="juba-busuu-footer-link text-xs font-semibold tracking-wide transition-colors">
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
