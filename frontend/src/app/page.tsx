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
    <main
      className="juba-reference-page min-h-screen overflow-x-hidden"
      dir={locale === 'ar' ? 'rtl' : 'ltr'}
      lang={locale}
    >
      <style dangerouslySetInnerHTML={{ __html: `
.juba-reference-page{--ink:#183022;--green:#3d7b27;--green-dark:#275d19;--mint:#e5f4d8;--blue:#dff5fa;--yellow:#ffe27a;--orange:#f6a23a;background:#fffdf7;color:var(--ink);font-family:var(--font-geist-sans),Arial,sans-serif}
.juba-reference-page .juba-site-nav{background:rgba(255,253,247,.94)!important;border-bottom:1px solid #d9e5d7!important;backdrop-filter:blur(18px)}
.juba-reference-page .juba-ff-nav-inner{height:76px!important;max-width:1240px!important}
.juba-reference-page .juba-ff-brand-mark{background:var(--green)!important;color:#fff!important;box-shadow:4px 4px 0 var(--ink)!important}
.juba-reference-page .juba-brand-spark,.juba-reference-page .juba-brand-accent{color:var(--green)!important}
.juba-reference-page .juba-ff-brand-name,.juba-reference-page .juba-ff-nav-link,.juba-reference-page .juba-ff-nav-signin{color:var(--ink)!important}
.juba-reference-page .juba-ff-nav-link:hover{color:var(--green)!important}
.juba-reference-page .juba-nav-region{border-color:#d9e5d7!important;background:#fff!important}
.juba-reference-page .juba-ff-nav-cta{background:var(--green)!important;color:#fff!important;border-radius:14px!important;box-shadow:4px 4px 0 var(--ink)!important}
.juba-reference-page .juba-landing-illustration{background:linear-gradient(180deg,#dff5fa 0%,#f8fbe9 100%)!important}
.juba-reference-page .juba-landing-illustration .landing-sun{background:var(--yellow);box-shadow:none}
.juba-reference-page .juba-landing-illustration .landing-cloud{box-shadow:0 8px 30px rgba(24,48,34,.07)}
.juba-reference-page .juba-landing-illustration .landing-ground{background:#b9d99d;border-top:4px solid var(--ink)}
.juba-reference-page .juba-landing-illustration .landing-book{background:#fff;color:var(--ink);border-color:var(--ink);box-shadow:6px 6px 0 var(--ink)}
.juba-reference-page .juba-landing-illustration .landing-book svg{color:var(--green)}
.juba-reference-page .juba-landing-illustration .landing-bubble{border-color:var(--ink);box-shadow:4px 4px 0 var(--ink)}
.juba-reference-page .juba-landing-illustration .landing-bubble-two{background:#fff0b7}
.juba-reference-page .juba-landing-illustration .landing-character-main{filter:none}
.juba-reference-page .juba-landing-illustration .character-body{background:var(--green);border-color:var(--ink);box-shadow:9px 10px 0 var(--ink)}
.juba-reference-page .juba-landing-illustration .character-face{background:#f7fff1;border-color:var(--ink);box-shadow:6px 7px 0 var(--ink)}
.juba-reference-page .juba-landing-illustration .eye{background:var(--ink)}
.juba-reference-page .juba-landing-illustration .mouth{border-color:var(--ink)}
.juba-reference-page .juba-landing-illustration .landing-character-small{border-color:var(--ink);box-shadow:5px 6px 0 var(--ink)}
.juba-reference-page .juba-landing-illustration .character-small-one{background:#e7f4dc}
.juba-reference-page .juba-landing-illustration .character-small-two{background:#e5f5fa}
.juba-reference-page .juba-landing-illustration .character-small-three{background:#eee7ff}
.juba-reference-page .juba-landing-illustration .landing-language-cluster span{border-color:var(--ink);box-shadow:4px 5px 0 var(--ink)}
.juba-reference-page .juba-ref-section-heading h2,.juba-reference-page .juba-ref-language-copy h2,.juba-reference-page .juba-ref-ai-copy h2,.juba-reference-page .juba-ref-cta h2{font-family:var(--font-geist-sans),Arial,sans-serif;text-wrap:balance}
.juba-reference-page .juba-ref-pillar{overflow:hidden;isolation:isolate}
.juba-reference-page .juba-ref-pillar:before{content:"";position:absolute;right:-34px;top:-34px;width:120px;height:120px;border-radius:50%;background:rgba(255,255,255,.38);z-index:-1}
.juba-reference-page .juba-ref-pillar .pillar-icon{box-shadow:3px 3px 0 rgba(24,48,34,.18)}
.juba-reference-page .juba-ref-pillar>svg{padding:3px;border-radius:50%;background:rgba(255,255,255,.65)}
.juba-reference-page .juba-ref-language-art{position:relative;overflow:hidden}
.juba-reference-page .juba-ref-language-art:before,.juba-reference-page .juba-ref-language-art:after{content:"";position:absolute;border-radius:50%;pointer-events:none}
.juba-reference-page .juba-ref-language-art:before{width:120px;height:120px;right:8%;top:8%;background:#ffe27a;opacity:.55}
.juba-reference-page .juba-ref-language-art:after{width:80px;height:80px;left:8%;bottom:8%;background:#dff5fa;opacity:.9}
.juba-reference-page .juba-ref-language-art>*{position:relative;z-index:2}
.juba-reference-page .juba-ref-ai-section{position:relative;overflow:hidden}
.juba-reference-page .juba-ref-ai-section:before{content:"";position:absolute;width:260px;height:260px;left:-100px;top:-90px;border-radius:50%;background:#e5f4d8;opacity:.75}
.juba-reference-page .juba-ref-ai-section>*{position:relative;z-index:1}
.juba-reference-page .juba-ref-ai-art{box-shadow:12px 13px 0 var(--ink);transform:rotate(-1.2deg)}
.juba-reference-page .juba-ref-ai-art:after{content:"";position:absolute;inset:14px;border:1px dashed #d8e4d3;border-radius:inherit;pointer-events:none}
.juba-reference-page .juba-ref-review-card{transition:transform .18s,box-shadow .18s}
.juba-reference-page .juba-ref-review-card:hover{transform:translateY(-4px) rotate(-.5deg);box-shadow:7px 8px 0 var(--ink)}
.juba-reference-page .juba-ref-pricing>div{max-width:1160px;margin:0 auto}
.juba-reference-page .juba-ref-cta-inner{position:relative}
.juba-reference-page .juba-ref-cta-inner:before{content:"✦";position:absolute;left:45%;top:-45px;font-size:70px;color:#ffe27a;text-shadow:3px 3px 0 var(--ink);transform:rotate(12deg);opacity:.95}
.juba-reference-page .juba-ref-cta-device{position:relative;transform:rotate(4deg)}
.juba-reference-page .juba-ref-faq .juba-ref-section-heading{position:relative}
.juba-reference-page .juba-ref-faq .juba-ref-section-heading:after{content:"";display:block;width:74px;height:6px;margin:24px auto 0;border-radius:99px;background:var(--green);box-shadow:12px 0 0 var(--yellow),24px 0 0 #dff5fa}
@media(max-width:900px){.juba-reference-page .juba-ref-cta-inner:before{left:auto;right:8%;top:-35px}.juba-reference-page .juba-ref-language-art{min-height:360px}}
@media(max-width:560px){.juba-reference-page .juba-ref-cta-inner:before{font-size:48px;top:-20px}.juba-reference-page .juba-ref-language-art{min-height:300px}}
.juba-reference-page :is(a,button,[role="button"]):focus-visible{outline:3px solid #f6a23a!important;outline-offset:4px!important;border-radius:8px}
.juba-reference-page .juba-ref-section-heading{padding-inline:8px}
.juba-reference-page .juba-ref-pillar h3,.juba-reference-page .juba-ref-pillar p{overflow-wrap:anywhere}
.juba-reference-page .juba-ref-language-copy,.juba-reference-page .juba-ref-ai-copy{min-width:0}
.juba-reference-page .juba-ref-language-art .animate-float{will-change:transform}
.juba-reference-page .juba-ref-cta{background:linear-gradient(125deg,#dff5fa 0%,#68c7e4 72%,#9cdef0 100%)}
.juba-reference-page .juba-ref-cta .juba-ref-button{background:#fff;color:var(--ink)}
.juba-reference-page .juba-ref-faq{scroll-margin-top:90px}
.juba-reference-page [id]{scroll-margin-top:88px}
@media(max-width:900px){.juba-reference-page .juba-ref-section{padding:78px 18px}.juba-reference-page .juba-ref-review-grid{gap:18px}.juba-reference-page .juba-ref-ai-section{padding-top:85px;padding-bottom:85px}}
@media(max-width:560px){.juba-reference-page .juba-ref-section{padding:64px 14px}.juba-reference-page .juba-ref-section-heading{margin-bottom:30px}.juba-reference-page .juba-ref-pillar{padding:21px;min-height:260px}.juba-reference-page .juba-ref-review-card{padding:19px}.juba-reference-page .juba-ref-cta-device{max-width:78%;height:310px}.juba-reference-page .juba-ref-hero-actions{gap:14px}.juba-reference-page .juba-ref-button{max-width:100%;white-space:normal}}
@media(prefers-reduced-motion:reduce){.juba-reference-page *, .juba-reference-page *:before,.juba-reference-page *:after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}
` }} />

      <Script
        id="juba-lisan-structured-data"
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <LandingNav
        hasSession={hasSession}
        stripeEnabled={stripeEnabled}
        dir={locale === 'ar' ? 'rtl' : 'ltr'}
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

          <div className="juba-ref-hero-art juba-landing-illustration" aria-label="JUBA LISAN visitor landing illustration">
            <div className="landing-sun" aria-hidden="true" />
            <div className="landing-cloud landing-cloud-one" aria-hidden="true" />
            <div className="landing-cloud landing-cloud-two" aria-hidden="true" />
            <div className="landing-ground" aria-hidden="true" />
            <div className="landing-book" aria-hidden="true">
              <BookOpen />
              <span>{t('languagesHeadline')}</span>
            </div>
            <div className="landing-bubble landing-bubble-one">{t('heroBadge')}</div>
            <div className="landing-bubble landing-bubble-two">{t('flowAiLabel')}</div>
            <div className="landing-language-cluster" aria-hidden="true">
              <span>EN</span><span>AR</span><span>FR</span><span>ES</span><span>DE</span>
            </div>
            <div className="landing-character landing-character-main" aria-hidden="true">
              <div className="character-face">
                <span className="eye eye-left" />
                <span className="eye eye-right" />
                <span className="mouth" />
              </div>
              <div className="character-body" />
            </div>
            <div className="landing-character landing-character-small character-small-one" aria-hidden="true"><span>EN</span></div>
            <div className="landing-character landing-character-small character-small-two" aria-hidden="true"><span>AR</span></div>
            <div className="landing-character landing-character-small character-small-three" aria-hidden="true"><span>FR</span></div>
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
          <div className="ai-bubble bubble-user">{t('flowAiTitle')}</div>
          <div className="ai-bubble bubble-ai">{t('flowAiDescription')}</div>
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
