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
      {/* emergency inline landing visual */}
      <style dangerouslySetInnerHTML={{ __html: ".juba-reference-page{--i:#183022;--m:#68766d;--p:#fffdf7;--g:#3d7b27;background:var(--p);color:var(--i);min-height:100vh;font-family:var(--font-geist-sans),system-ui,sans-serif}.juba-reference-page *{box-sizing:border-box}.juba-reference-page a{text-decoration:none}.juba-ref-hero{position:relative;min-height:760px;overflow:hidden;background:radial-gradient(circle at 15% 16%,rgba(255,226,122,.65),transparent 220px),linear-gradient(180deg,#fffdf7,#f8fbe9)}.juba-ref-hero-inner{width:calc(100% - 44px);max-width:1240px;min-height:690px;margin:auto;display:grid;grid-template-columns:.88fr 1.12fr;align-items:center;gap:30px;position:relative;z-index:3}.juba-ref-hero-copy{padding:76px 0 90px;position:relative;z-index:5}.juba-ref-kicker{display:inline-flex;align-items:center;gap:7px;padding:8px 13px;border:1.5px solid #c8ddc1;border-radius:999px;background:#fff;color:#275d19;font-size:11px;font-weight:900;letter-spacing:.07em;text-transform:uppercase}.juba-ref-hero-copy h1{max-width:720px;margin:21px 0 20px;font-size:clamp(3.5rem,7.2vw,7.7rem);line-height:.86;letter-spacing:-.085em;font-weight:950}.juba-ref-hero-copy p{max-width:570px;margin:0;color:var(--m);font-size:1.15rem;line-height:1.72}.juba-ref-hero-actions{display:flex;align-items:center;gap:20px;flex-wrap:wrap;margin-top:32px}.juba-ref-button{display:inline-flex;align-items:center;gap:9px;padding:14px 21px;border:2px solid var(--i);border-radius:16px;background:var(--g);color:#fff;font-size:13px;font-weight:900;box-shadow:5px 5px 0 var(--i)}.juba-ref-text-link{font-weight:850;color:var(--i);text-decoration:underline!important}.juba-ref-hero-art{position:relative;min-height:620px}.juba-ref-hero-shape{position:absolute;z-index:1}.shape-yellow{width:240px;height:240px;right:12%;top:10%;border-radius:50%;background:#ffe27a;opacity:.5}.shape-green{width:420px;height:230px;right:-100px;bottom:40px;border-radius:50%;background:#dcefcf;transform:rotate(-9deg)}.juba-ref-cloud{position:absolute;z-index:2;border-radius:999px;background:#fff;box-shadow:0 8px 30px #18302212}.cloud-a{width:135px;height:42px;left:8%;top:18%}.cloud-b{width:180px;height:54px;right:0;top:30%}.juba-ref-sun{position:absolute;z-index:2;width:155px;height:155px;right:18%;top:12%;border-radius:50%;background:#ffd85e}.juba-ref-ground{position:absolute;z-index:2;left:4%;right:0;bottom:50px;height:230px;border-radius:50% 50% 0 0;background:#b9d99d;transform:rotate(-4deg)}.juba-ref-character{position:absolute;z-index:7;display:grid;place-items:center;border:4px solid var(--i);background:#fff;box-shadow:9px 10px 0 var(--i);color:var(--g);font-weight:950}.character-main{width:210px;height:250px;right:31%;bottom:112px;border-radius:46% 54% 38% 62%;background:#f7fff1;transform:rotate(-5deg)}.character-main>span{font-size:58px;position:absolute;bottom:23px;right:31px;color:#ffd85e;text-shadow:3px 3px var(--i)}.character-face{position:absolute;left:50%;top:31%;transform:translate(-50%,-50%);display:flex;gap:29px}.character-face i{width:13px;height:19px;border-radius:50%;background:var(--i)}.character-small{width:82px;height:88px;border-width:3px;box-shadow:5px 6px 0 var(--i);border-radius:42% 58% 55% 45%;font-size:14px}.character-one{left:9%;bottom:125px;background:#e7f4dc;transform:rotate(-10deg)}.character-two{left:30%;bottom:245px;background:#e5f5fa;transform:rotate(7deg)}.character-three{right:5%;bottom:142px;background:#eee7ff;transform:rotate(10deg)}.juba-ref-speech{position:absolute;z-index:8;padding:10px 14px;border:2px solid var(--i);border-radius:14px;background:#fff;font-size:12px;font-weight:900;box-shadow:4px 4px 0 var(--i)}.speech-one{left:12%;top:31%}.speech-two{right:6%;top:18%;background:#fff0b8}.juba-ref-book{position:absolute;z-index:9;left:28%;bottom:22px;min-width:250px;padding:13px 17px;display:grid;grid-template-columns:auto 1fr;align-items:center;gap:10px;border:2px solid var(--i);border-radius:16px;background:#fff;box-shadow:6px 6px 0 var(--i)}.juba-ref-book strong{font-size:12px}.juba-ref-book small{font-size:10px;color:var(--m)}.juba-ref-hero-bottom{position:absolute;z-index:4;left:-5%;bottom:-80px;width:110%;height:180px;border-radius:50% 50% 0 0;background:var(--p)}.juba-ref-section{padding:105px 22px}.juba-ref-section-heading{text-align:center;max-width:760px;margin:0 auto 48px}.juba-ref-section-heading h2{margin:17px 0 13px;font-size:clamp(2.4rem,5vw,4.8rem);line-height:.9;font-weight:950}.juba-ref-section-heading p{color:var(--m);line-height:1.8}.juba-ref-pillars{background:#eef7e4}.juba-ref-pillar-grid{max-width:1100px;margin:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.juba-ref-pillar{min-height:360px;padding:25px;border:2px solid var(--i);border-radius:28px;box-shadow:7px 8px 0 var(--i);display:flex;flex-direction:column}.pillar-mint{background:#dff1d1}.pillar-blue{background:#dff4f8}.pillar-yellow{background:#fff0b7}.juba-ref-pillar .pillar-icon{width:58px;height:58px;display:grid;place-items:center;border:2px solid var(--i);border-radius:18px;background:#fff;margin-bottom:auto}.juba-ref-pillar h3{margin:9px 0;font-size:25px;font-weight:950}.juba-ref-pillar p{color:#526057;font-size:12px;line-height:1.7}.juba-ref-language-section{max-width:1160px;margin:auto;padding:120px 0;display:grid;grid-template-columns:.8fr 1.2fr;align-items:center;gap:70px}.juba-ref-language-copy h2,.juba-ref-ai-copy h2,.juba-ref-cta h2{font-size:clamp(2.7rem,5.5vw,5.2rem);line-height:.9;font-weight:950}.juba-ref-language-copy p,.juba-ref-ai-copy>p,.juba-ref-cta p{max-width:510px;color:var(--m);line-height:1.8}.juba-ref-language-art{min-height:390px;padding:34px;border:2px solid var(--i);border-radius:45%;background:#e8f3d9;box-shadow:9px 10px 0 #18302224;display:grid;place-items:center}.juba-ref-ai-section{padding:120px 22px;display:grid;grid-template-columns:1.15fr .85fr;align-items:center;gap:75px;background:#f2edff}.juba-ref-ai-art{min-height:440px;border:2px solid var(--i);border-radius:45%;background:#fff;box-shadow:10px 11px 0 var(--i);display:grid;place-items:center;position:relative}.ai-avatar{width:115px;height:115px;border:4px solid var(--i);border-radius:36px;background:#dff1d1;display:grid;place-items:center;box-shadow:7px 8px 0 var(--g)}.ai-bubble{position:absolute;padding:11px 14px;border:2px solid var(--i);border-radius:15px;background:#fff;font-size:11px;font-weight:850;box-shadow:4px 4px 0 var(--i)}.bubble-user{left:9%;top:19%;background:#fff0b7}.bubble-ai{right:8%;bottom:20%;background:#dff4f8}.juba-ref-reviews{padding:110px 22px;background:#eef7e4}.juba-ref-review-grid{max-width:1080px;margin:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.juba-ref-review-card{padding:24px;border:2px solid var(--i);border-radius:23px;background:#fff;box-shadow:5px 6px 0 var(--i)}.juba-ref-pricing{padding:100px 22px;background:#fffdf7}.juba-ref-cta{padding:110px 22px;background:#68c7e4}.juba-ref-cta-inner{max-width:1100px;margin:auto;display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:50px}.juba-ref-cta-device{width:260px;height:430px;margin:auto;border:8px solid var(--i);border-radius:38px;background:#fff;box-shadow:14px 15px 0 var(--g);display:flex;align-items:center;justify-content:center}.juba-ref-faq{padding:105px 22px 120px;background:#f4f7ef}@media(max-width:900px){.juba-ref-hero-inner,.juba-ref-language-section,.juba-ref-ai-section,.juba-ref-cta-inner{grid-template-columns:1fr}.juba-ref-hero-inner{min-height:0;padding-top:45px}.juba-ref-hero-art{min-height:540px}.juba-ref-pillar-grid,.juba-ref-review-grid{grid-template-columns:1fr}}@media(max-width:560px){.juba-ref-hero-inner{width:calc(100% - 28px)}.juba-ref-hero-art{min-height:420px;transform:scale(.9);transform-origin:center top}.character-main{width:160px;height:195px;right:27%;bottom:75px}.character-small{width:62px;height:68px;font-size:10px}.juba-ref-book{left:17%;min-width:220px}.juba-ref-language-section{padding:80px 14px}.juba-ref-ai-section{padding:80px 16px}.juba-ref-cta{padding:80px 16px}}" }} />

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
