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
      <style dangerouslySetInnerHTML={{ __html: ".juba-reference-page{--bg:#F3F2F3;--blue:#373FB8;--blue2:#5862E2;--lav:#9A9FF3;--ink:#070709;--orange:#F95D22;--mauve:#9F89BD;--plum:#442E3B;background:var(--bg);color:var(--ink);font-family:var(--font-geist-sans),Arial,sans-serif}.juba-reference-page *{box-sizing:border-box}.juba-reference-page a{text-decoration:none}.juba-ref-hero{padding:0 28px 74px;background:var(--bg);overflow:hidden}.juba-ref-hero-inner{width:min(1320px,100%);margin:auto;display:grid;grid-template-columns:1.03fr 1.45fr;gap:28px;align-items:stretch;padding-top:32px}.juba-ref-hero-copy{min-height:590px;padding:58px 54px;border-radius:34px;background:#fff;display:flex;flex-direction:column;justify-content:center;box-shadow:0 2px 0 #07070908}.juba-ref-kicker{display:inline-flex;width:max-content;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;background:#F3F2F3;color:var(--blue);font-size:11px;font-weight:800}.juba-ref-hero-copy h1{margin:20px 0 18px;max-width:620px;font-size:clamp(3.3rem,6vw,6.8rem);line-height:.88;letter-spacing:-.075em;font-weight:850}.juba-ref-hero-copy p{max-width:520px;margin:0;color:#69676c;font-size:15px;line-height:1.75}.juba-ref-hero-actions{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:30px}.juba-ref-button{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:14px 20px;border-radius:14px;background:var(--ink);color:#fff;font-size:12px;font-weight:800}.juba-ref-text-link{padding:13px 17px;border-radius:14px;background:#F3F2F3;color:var(--ink);font-size:12px;font-weight:800}.juba-ref-hero-art{min-height:590px;position:relative;border-radius:34px;background:#E9E8EA;overflow:hidden}.juba-ref-hero-shape{position:absolute}.shape-yellow{width:210px;height:210px;right:7%;top:7%;border-radius:50%;background:var(--lav);opacity:.65}.shape-green{width:300px;height:300px;left:-100px;bottom:-150px;border-radius:50%;background:var(--mauve);opacity:.55}.juba-ref-cloud,.juba-ref-sun{display:none}.juba-ref-ground{position:absolute;left:28px;right:28px;bottom:28px;height:270px;border-radius:28px;background:#fff;transform:none}.juba-ref-character{position:absolute;display:grid;place-items:center;border:0;box-shadow:none;background:transparent;color:var(--ink);font-weight:850}.character-main{width:220px;height:220px;right:33%;bottom:74px;border-radius:50%;background:var(--blue2);box-shadow:14px 16px 0 var(--ink);transform:rotate(-5deg)}.character-main>span{font-size:80px;color:#fff}.character-face{display:none}.character-small{width:auto;height:auto;padding:12px 16px;border-radius:14px;border:2px solid var(--ink);background:#fff;box-shadow:5px 5px 0 var(--ink);font-size:12px}.character-one{left:9%;bottom:210px;background:#D9DBFA;transform:rotate(-7deg)}.character-two{left:20%;bottom:92px;background:#F8C3B1;transform:rotate(6deg)}.character-three{right:8%;bottom:235px;background:#D7CBE3;transform:rotate(7deg)}.juba-ref-speech{position:absolute;padding:12px 15px;border-radius:13px;background:#fff;border:2px solid var(--ink);box-shadow:5px 5px 0 var(--ink);font-size:12px;font-weight:800}.speech-one{left:10%;top:19%}.speech-two{right:9%;top:30%;background:#FFE0D5}.juba-ref-book{position:absolute;left:7%;bottom:54px;min-width:220px;padding:16px;border-radius:18px;background:var(--orange);color:#fff;border:2px solid var(--ink);box-shadow:6px 7px 0 var(--ink);display:grid;grid-template-columns:auto 1fr;gap:10px}.juba-ref-book strong{font-size:13px}.juba-ref-book small{font-size:10px;opacity:.9}.juba-ref-hero-bottom{display:none}.juba-ref-section{width:min(1320px,calc(100% - 56px));margin:auto;padding:86px 0}.juba-ref-section-heading{text-align:left;max-width:700px;margin:0 0 34px}.juba-ref-section-heading h2{margin:14px 0;font-size:clamp(2.5rem,5vw,5rem);line-height:.92;letter-spacing:-.065em;font-weight:850}.juba-ref-section-heading p{color:#69676c;font-size:14px;line-height:1.75}.juba-ref-pillars{background:var(--bg)}.juba-ref-pillar-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.juba-ref-pillar{min-height:330px;padding:24px;border-radius:26px;border:0;box-shadow:none;display:flex;flex-direction:column;justify-content:flex-end;transition:transform .2s}.juba-ref-pillar:hover{transform:translateY(-4px)}.pillar-mint{background:var(--blue2);color:#fff}.pillar-blue{background:var(--orange);color:#fff}.pillar-yellow{background:var(--lav);color:var(--ink)}.juba-ref-pillar .pillar-icon{width:48px;height:48px;display:grid;place-items:center;border-radius:14px;background:#fff;color:var(--ink);margin-bottom:auto}.juba-ref-pillar h3{margin:9px 0;font-size:25px;line-height:1;font-weight:850}.juba-ref-pillar p{max-width:290px;margin:0;font-size:12px;line-height:1.65;opacity:.82}.juba-ref-pillar>svg{margin-top:20px}.juba-ref-language-section{width:min(1320px,calc(100% - 56px));margin:auto;padding:86px 0;display:grid;grid-template-columns:.72fr 1.28fr;gap:18px}.juba-ref-language-copy{padding:42px;border-radius:28px;background:#fff}.juba-ref-language-copy h2,.juba-ref-ai-copy h2,.juba-ref-cta h2{margin:16px 0;font-size:clamp(2.7rem,5vw,5rem);line-height:.9;letter-spacing:-.07em;font-weight:850}.juba-ref-language-copy p,.juba-ref-ai-copy>p,.juba-ref-cta p{color:#69676c;font-size:14px;line-height:1.75}.juba-ref-language-art{min-height:420px;padding:30px;border-radius:28px;background:#D9DBFA;display:grid;place-items:center;overflow:hidden}.juba-ref-ai-section{width:min(1320px,calc(100% - 56px));margin:auto;padding:0 0 86px;display:grid;grid-template-columns:1.28fr .72fr;gap:18px;background:transparent}.juba-ref-ai-art{min-height:430px;position:relative;border-radius:28px;background:var(--plum);overflow:hidden}.ai-avatar{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:150px;height:150px;border-radius:50%;background:var(--lav);display:grid;place-items:center;color:var(--ink);box-shadow:12px 13px 0 var(--ink)}.ai-bubble{position:absolute;padding:12px 15px;border-radius:14px;border:2px solid var(--ink);background:#fff;box-shadow:5px 5px 0 var(--ink);font-size:11px;font-weight:800}.bubble-user{left:8%;top:16%;background:#F8C3B1}.bubble-ai{right:8%;bottom:17%;background:#D9DBFA}.ai-wave{display:none}.juba-ref-ai-copy{padding:42px;border-radius:28px;background:#fff}.juba-ref-ai-points{display:grid;gap:10px;margin:22px 0}.juba-ref-ai-points span{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:800}.juba-ref-reviews{width:min(1320px,calc(100% - 56px));margin:auto;padding:0 0 86px;background:transparent}.juba-ref-review-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.juba-ref-review-card{padding:24px;border:0;border-radius:24px;background:#fff;box-shadow:none}.juba-ref-review-card p{font-size:13px;line-height:1.7}.juba-ref-review-card strong{font-size:12px}.juba-ref-pricing{width:min(1320px,calc(100% - 56px));margin:auto;padding:86px 0;background:transparent}.juba-ref-cta{width:min(1320px,calc(100% - 56px));margin:0 auto 86px;padding:55px;border-radius:30px;background:var(--blue);color:#fff}.juba-ref-cta-inner{display:grid;grid-template-columns:1fr 360px;align-items:center;gap:50px}.juba-ref-cta p{color:#E4E5FF}.juba-ref-cta .juba-ref-kicker{background:#fff;color:var(--blue)}.juba-ref-cta-device{height:300px;border-radius:30px;background:var(--lav);border:0;box-shadow:12px 13px 0 var(--ink);display:grid;place-items:center;color:var(--ink);transform:rotate(4deg);font-weight:850}.juba-ref-faq{width:min(1320px,calc(100% - 56px));margin:auto;padding:0 0 100px;background:transparent}@media(max-width:900px){.juba-ref-hero-inner,.juba-ref-language-section,.juba-ref-ai-section,.juba-ref-cta-inner{grid-template-columns:1fr}.juba-ref-hero-copy{padding:42px 30px}.juba-ref-pillar-grid,.juba-ref-review-grid{grid-template-columns:1fr}.juba-ref-hero-art{min-height:500px}.juba-ref-cta-device{height:230px}}@media(max-width:560px){.juba-ref-hero{padding:0 14px 45px}.juba-ref-section,.juba-ref-language-section,.juba-ref-ai-section,.juba-ref-reviews,.juba-ref-pricing,.juba-ref-cta,.juba-ref-faq{width:calc(100% - 28px)}.juba-ref-hero-copy h1{font-size:3.4rem}.juba-ref-hero-art{min-height:430px}.character-main{width:150px;height:150px;right:28%;bottom:78px}.character-main>span{font-size:58px}.juba-ref-book{left:5%;bottom:34px;min-width:185px}.juba-ref-ground{left:16px;right:16px;bottom:16px;height:210px}}" }} />

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
