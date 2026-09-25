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
      <style dangerouslySetInnerHTML={{ __html: `.juba-reference-page{--bg:#F3F2F3;--blue:#373FB8;--blue2:#5862E2;--lav:#9A9FF3;--ink:#070709;--orange:#F95D22;--mauve:#9F89BD;--plum:#442E3B;background:var(--bg);color:var(--ink);font-family:var(--font-geist-sans),Arial,sans-serif}.juba-reference-page .juba-site-nav{background:rgba(243,242,243,.92)!important;border-bottom:1px solid rgba(7,7,9,.08)!important;backdrop-filter:blur(18px)}.juba-reference-page .juba-ff-nav-inner{height:76px!important;max-width:1320px!important}.juba-reference-page .juba-ff-brand-mark{width:42px!important;height:42px!important;border-radius:13px!important;background:#373FB8!important;color:#fff!important;box-shadow:4px 4px 0 #070709!important}.juba-reference-page .juba-brand-spark{color:#F95D22!important}.juba-reference-page .juba-ff-brand-name{color:#070709!important}.juba-reference-page .juba-brand-accent{color:#373FB8!important}.juba-reference-page .juba-ff-brand-copy small{display:block!important;margin-top:1px!important;color:#77747a!important;font-size:9px!important;font-weight:700!important}.juba-reference-page .juba-ff-nav-link{color:#070709!important;font-size:11px!important;font-weight:700!important}.juba-reference-page .juba-ff-nav-link:hover{color:#373FB8!important}.juba-reference-page .juba-nav-region{border-color:#d9d7da!important;background:#fff!important}.juba-reference-page .juba-ff-nav-signin{color:#070709!important;font-size:11px!important}.juba-reference-page .juba-ff-nav-cta{background:#373FB8!important;color:#fff!important;border-radius:12px!important;box-shadow:4px 4px 0 #070709!important;font-size:11px!important}.juba-reference-page .juba-landing-illustration{background:#DFF5FA!important;min-height:620px!important;position:relative!important;overflow:hidden!important;border-radius:34px!important;color:#070709!important}
.juba-reference-page .juba-landing-illustration .landing-sun{position:absolute;width:190px;height:190px;border-radius:50%;right:9%;top:7%;background:#FFE27A;box-shadow:7px 7px 0 #070709}
.juba-reference-page .juba-landing-illustration .landing-cloud{position:absolute;width:170px;height:54px;border-radius:999px;background:#fff;box-shadow:5px 5px 0 rgba(7,7,9,.12)}
.juba-reference-page .juba-landing-illustration .landing-cloud:before,.juba-reference-page .juba-landing-illustration .landing-cloud:after{content:"";position:absolute;border-radius:50%;background:#fff}
.juba-reference-page .juba-landing-illustration .landing-cloud:before{width:72px;height:72px;left:28px;top:-34px}
.juba-reference-page .juba-landing-illustration .landing-cloud:after{width:58px;height:58px;left:84px;top:-22px}
.juba-reference-page .juba-landing-illustration .landing-cloud-one{left:9%;top:14%;transform:scale(.82)}
.juba-reference-page .juba-landing-illustration .landing-cloud-two{right:8%;top:39%;transform:scale(.58)}
.juba-reference-page .juba-landing-illustration .landing-ground{position:absolute;left:4%;right:4%;bottom:4%;height:48%;border-radius:48% 48% 0 0;background:#E5F4D8;border-top:4px solid #070709}
.juba-reference-page .juba-landing-illustration .landing-book{position:absolute;left:8%;bottom:10%;z-index:3;width:230px;min-height:120px;padding:18px;border:3px solid #070709;border-radius:22px;background:#F95D22;color:#fff;box-shadow:9px 10px 0 #070709;display:flex;align-items:flex-end;gap:12px;font-weight:900;font-size:14px;transform:rotate(-5deg)}
.juba-reference-page .juba-landing-illustration .landing-book svg{width:42px;height:42px}
.juba-reference-page .juba-landing-illustration .landing-bubble{position:absolute;z-index:6;padding:12px 16px;border:3px solid #070709;border-radius:16px;background:#fff;box-shadow:6px 7px 0 #070709;font-size:12px;font-weight:900}
.juba-reference-page .juba-landing-illustration .landing-bubble-one{left:10%;top:30%;transform:rotate(-4deg)}
.juba-reference-page .juba-landing-illustration .landing-bubble-two{right:7%;top:55%;background:#FFE27A;transform:rotate(4deg)}
.juba-reference-page .juba-landing-illustration .landing-language-cluster{position:absolute;z-index:4;right:7%;bottom:10%;display:flex;gap:8px;flex-wrap:wrap;max-width:190px;justify-content:flex-end}
.juba-reference-page .juba-landing-illustration .landing-language-cluster span{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:#fff;border:3px solid #070709;box-shadow:4px 5px 0 #070709;font-size:10px;font-weight:950;transform:rotate(var(--r,0deg))}
.juba-reference-page .juba-landing-illustration .landing-language-cluster span:nth-child(2){background:#9A9FF3;transform:translateY(-8px) rotate(-5deg)}
.juba-reference-page .juba-landing-illustration .landing-language-cluster span:nth-child(3){background:#FFE27A;transform:rotate(5deg)}
.juba-reference-page .juba-landing-illustration .landing-language-cluster span:nth-child(4){background:#F95D22;transform:translateY(8px) rotate(-4deg)}
.juba-reference-page .juba-landing-illustration .landing-language-cluster span:nth-child(5){background:#E5F4D8;transform:rotate(6deg)}
.juba-reference-page .juba-landing-illustration .landing-character{position:absolute;z-index:5}
.juba-reference-page .juba-landing-illustration .landing-character-main{left:42%;bottom:9%;width:250px;height:300px}
.juba-reference-page .juba-landing-illustration .character-body{position:absolute;left:50%;bottom:0;transform:translateX(-50%);width:220px;height:230px;border-radius:52% 48% 43% 57%;background:#3D7B27;border:4px solid #070709;box-shadow:12px 13px 0 #070709}
.juba-reference-page .juba-landing-illustration .character-face{position:absolute;z-index:2;left:50%;top:8%;transform:translateX(-50%);width:172px;height:150px;border-radius:48% 52% 46% 54%;background:#9A9FF3;border:4px solid #070709;box-shadow:8px 9px 0 #070709}
.juba-reference-page .juba-landing-illustration .eye{position:absolute;top:54px;width:18px;height:25px;border-radius:50%;background:#070709}
.juba-reference-page .juba-landing-illustration .eye-left{left:48px}.juba-reference-page .juba-landing-illustration .eye-right{right:48px}
.juba-reference-page .juba-landing-illustration .mouth{position:absolute;left:50%;bottom:30px;width:42px;height:20px;border-bottom:4px solid #070709;border-radius:50%;transform:translateX(-50%)}
.juba-reference-page .juba-landing-illustration .landing-character-small{width:72px;height:72px;border-radius:50%;display:grid;place-items:center;border:3px solid #070709;box-shadow:6px 7px 0 #070709;font-size:14px;font-weight:950}
.juba-reference-page .juba-landing-illustration .character-small-one{left:29%;bottom:15%;background:#F95D22;transform:rotate(-8deg)}
.juba-reference-page .juba-landing-illustration .character-small-two{right:22%;bottom:12%;background:#9F89BD;transform:rotate(8deg)}
.juba-reference-page .juba-landing-illustration .character-small-three{right:8%;bottom:25%;background:#fff;transform:rotate(-7deg)}
@media(max-width:900px){.juba-reference-page .juba-landing-illustration{min-height:520px!important}.juba-reference-page .juba-landing-illustration .landing-character-main{left:37%;transform:scale(.86);transform-origin:bottom center}.juba-reference-page .juba-landing-illustration .landing-book{width:190px}}
@media(max-width:560px){.juba-reference-page .juba-landing-illustration .landing-language-cluster{right:4%;bottom:8%;max-width:130px;gap:5px}.juba-reference-page .juba-landing-illustration .landing-language-cluster span{width:31px;height:31px;font-size:8px;border-width:2px;box-shadow:3px 3px 0 #070709}.juba-reference-page .juba-landing-illustration{min-height:470px!important}.juba-reference-page .juba-landing-illustration .landing-character-main{left:31%;transform:scale(.67);transform-origin:bottom center}.juba-reference-page .juba-landing-illustration .landing-book{width:150px;min-height:90px;padding:12px;font-size:10px}.juba-reference-page .juba-landing-illustration .landing-book svg{width:28px;height:28px}.juba-reference-page .juba-landing-illustration .landing-bubble{font-size:9px;padding:8px 10px}.juba-reference-page .juba-landing-illustration .landing-character-small{width:52px;height:52px;font-size:10px}}

.juba-reference-page .juba-ref-hero{position:relative;background:#9A9FF3!important;padding:34px 28px 88px!important}.juba-reference-page .juba-ref-hero:before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.22;background:repeating-linear-gradient(125deg,transparent 0 105px,#fff 105px 180px,transparent 180px 285px)}.juba-reference-page .juba-ref-hero-inner{position:relative;z-index:1;display:flex!important;flex-direction:column;gap:18px;padding-top:0!important}.juba-reference-page .juba-ref-hero-copy{min-height:0!important;padding:34px 42px!important;border-radius:26px!important;display:grid!important;grid-template-columns:1.4fr .8fr;align-items:end;gap:30px;box-shadow:none!important}.juba-reference-page .juba-ref-hero-copy h1{font-size:clamp(3rem,5vw,5.6rem)!important;max-width:820px!important;margin:14px 0!important}.juba-reference-page .juba-ref-hero-copy p{max-width:620px!important}.juba-reference-page .juba-ref-hero-actions{justify-content:flex-end;margin-top:0!important}.juba-reference-page .juba-ref-hero-art{min-height:620px!important;width:100%;border-radius:28px!important;box-shadow:0 18px 45px rgba(7,7,9,.16)}.juba-reference-page .juba-ref-hero-shape{z-index:0}.juba-reference-page .shape-yellow{display:none}.juba-reference-page .shape-green{width:440px;height:440px;left:auto;right:-180px;bottom:-250px;background:#5862E2;opacity:.55}.juba-reference-page .juba-ref-section{padding:78px 0!important}.juba-reference-page .juba-ref-pillars{background:#F3F2F3!important}.juba-reference-page .juba-ref-pillar-grid{grid-template-columns:1.25fr .85fr .85fr!important;align-items:stretch}.juba-reference-page .juba-ref-pillar{min-height:360px!important}.juba-reference-page .juba-ref-pillar:first-child{min-height:440px!important;background:#5862E2!important}.juba-reference-page .juba-ref-pillar:nth-child(2){background:#F95D22!important}.juba-reference-page .juba-ref-pillar:nth-child(3){background:#9A9FF3!important}.juba-reference-page .juba-ref-language-section{padding-top:10px!important}.juba-reference-page .juba-ref-language-art{background:#fff!important}.juba-reference-page .juba-ref-ai-section{padding-top:10px!important}.juba-reference-page .juba-ref-ai-art{background:#442E3B!important}@media(max-width:900px){.juba-reference-page .juba-ref-hero-copy{grid-template-columns:1fr!important}.juba-reference-page .juba-ref-hero-actions{justify-content:flex-start;margin-top:12px!important}.juba-reference-page .juba-ref-pillar-grid{grid-template-columns:1fr!important}}@media(max-width:560px){.juba-reference-page .juba-ref-hero{padding:18px 14px 55px!important}.juba-reference-page .juba-ref-hero-copy{padding:26px 22px!important}.juba-reference-page .juba-ref-hero-art{min-height:480px!important}.juba-reference-page .juba-ref-hero-copy h1{font-size:3.2rem!important}}.juba-reference-page .juba-ff-menu{background:#fff!important;border:1px solid #d9d7da!important}.juba-reference-page *{box-sizing:border-box}.juba-reference-page a{text-decoration:none}.juba-ref-hero{padding:0 28px 74px;background:var(--bg);overflow:hidden}.juba-ref-hero-inner{width:min(1320px,100%);margin:auto;display:grid;grid-template-columns:1.03fr 1.45fr;gap:28px;align-items:stretch;padding-top:32px}.juba-ref-hero-copy{min-height:590px;padding:58px 54px;border-radius:34px;background:#fff;display:flex;flex-direction:column;justify-content:center;box-shadow:0 2px 0 #07070908}.juba-ref-kicker{display:inline-flex;width:max-content;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;background:#F3F2F3;color:var(--blue);font-size:11px;font-weight:800}.juba-ref-hero-copy h1{margin:20px 0 18px;max-width:620px;font-size:clamp(3.3rem,6vw,6.8rem);line-height:.88;letter-spacing:-.075em;font-weight:850}.juba-ref-hero-copy p{max-width:520px;margin:0;color:#69676c;font-size:15px;line-height:1.75}.juba-ref-hero-actions{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:30px}.juba-ref-button{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:14px 20px;border-radius:14px;background:var(--ink);color:#fff;font-size:12px;font-weight:800}.juba-ref-text-link{padding:13px 17px;border-radius:14px;background:#F3F2F3;color:var(--ink);font-size:12px;font-weight:800}.juba-ref-hero-art{min-height:590px;position:relative;border-radius:34px;background:#E9E8EA;overflow:hidden}.juba-ref-hero-shape{position:absolute}.shape-yellow{width:210px;height:210px;right:7%;top:7%;border-radius:50%;background:var(--lav);opacity:.65}.shape-green{width:300px;height:300px;left:-100px;bottom:-150px;border-radius:50%;background:var(--mauve);opacity:.55}.juba-ref-cloud,.juba-ref-sun{display:none}.juba-ref-ground{position:absolute;left:28px;right:28px;bottom:28px;height:270px;border-radius:28px;background:#fff;transform:none}.juba-ref-character{position:absolute;display:grid;place-items:center;border:0;box-shadow:none;background:transparent;color:var(--ink);font-weight:850}.character-main{width:220px;height:220px;right:33%;bottom:74px;border-radius:50%;background:var(--blue2);box-shadow:14px 16px 0 var(--ink);transform:rotate(-5deg)}.character-main>span{font-size:80px;color:#fff}.character-face{display:none}.character-small{width:auto;height:auto;padding:12px 16px;border-radius:14px;border:2px solid var(--ink);background:#fff;box-shadow:5px 5px 0 var(--ink);font-size:12px}.character-one{left:9%;bottom:210px;background:#D9DBFA;transform:rotate(-7deg)}.character-two{left:20%;bottom:92px;background:#F8C3B1;transform:rotate(6deg)}.character-three{right:8%;bottom:235px;background:#D7CBE3;transform:rotate(7deg)}.juba-ref-speech{position:absolute;padding:12px 15px;border-radius:13px;background:#fff;border:2px solid var(--ink);box-shadow:5px 5px 0 var(--ink);font-size:12px;font-weight:800}.speech-one{left:10%;top:19%}.speech-two{right:9%;top:30%;background:#FFE0D5}.juba-ref-book{position:absolute;left:7%;bottom:54px;min-width:220px;padding:16px;border-radius:18px;background:var(--orange);color:#fff;border:2px solid var(--ink);box-shadow:6px 7px 0 var(--ink);display:grid;grid-template-columns:auto 1fr;gap:10px}.juba-ref-book strong{font-size:13px}.juba-ref-book small{font-size:10px;opacity:.9}.juba-ref-hero-bottom{display:none}.juba-ref-section{width:min(1320px,calc(100% - 56px));margin:auto;padding:86px 0}.juba-ref-section-heading{text-align:left;max-width:700px;margin:0 0 34px}.juba-ref-section-heading h2{margin:14px 0;font-size:clamp(2.5rem,5vw,5rem);line-height:.92;letter-spacing:-.065em;font-weight:850}.juba-ref-section-heading p{color:#69676c;font-size:14px;line-height:1.75}.juba-ref-pillars{background:var(--bg)}.juba-ref-pillar-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.juba-ref-pillar{min-height:330px;padding:24px;border-radius:26px;border:0;box-shadow:none;display:flex;flex-direction:column;justify-content:flex-end;transition:transform .2s}.juba-ref-pillar:hover{transform:translateY(-4px)}.pillar-mint{background:var(--blue2);color:#fff}.pillar-blue{background:var(--orange);color:#fff}.pillar-yellow{background:var(--lav);color:var(--ink)}.juba-ref-pillar .pillar-icon{width:48px;height:48px;display:grid;place-items:center;border-radius:14px;background:#fff;color:var(--ink);margin-bottom:auto}.juba-ref-pillar h3{margin:9px 0;font-size:25px;line-height:1;font-weight:850}.juba-ref-pillar p{max-width:290px;margin:0;font-size:12px;line-height:1.65;opacity:.82}.juba-ref-pillar>svg{margin-top:20px}.juba-ref-language-section{width:min(1320px,calc(100% - 56px));margin:auto;padding:86px 0;display:grid;grid-template-columns:.72fr 1.28fr;gap:18px}.juba-ref-language-copy{padding:42px;border-radius:28px;background:#fff}.juba-ref-language-copy h2,.juba-ref-ai-copy h2,.juba-ref-cta h2{margin:16px 0;font-size:clamp(2.7rem,5vw,5rem);line-height:.9;letter-spacing:-.07em;font-weight:850}.juba-ref-language-copy p,.juba-ref-ai-copy>p,.juba-ref-cta p{color:#69676c;font-size:14px;line-height:1.75}.juba-ref-language-art{min-height:420px;padding:30px;border-radius:28px;background:#D9DBFA;display:grid;place-items:center;overflow:hidden}.juba-ref-ai-section{width:min(1320px,calc(100% - 56px));margin:auto;padding:0 0 86px;display:grid;grid-template-columns:1.28fr .72fr;gap:18px;background:transparent}.juba-ref-ai-art{min-height:430px;position:relative;border-radius:28px;background:var(--plum);overflow:hidden}.ai-avatar{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:150px;height:150px;border-radius:50%;background:var(--lav);display:grid;place-items:center;color:var(--ink);box-shadow:12px 13px 0 var(--ink)}.ai-bubble{position:absolute;padding:12px 15px;border-radius:14px;border:2px solid var(--ink);background:#fff;box-shadow:5px 5px 0 var(--ink);font-size:11px;font-weight:800}.bubble-user{left:8%;top:16%;background:#F8C3B1}.bubble-ai{right:8%;bottom:17%;background:#D9DBFA}.ai-wave{display:none}.juba-ref-ai-copy{padding:42px;border-radius:28px;background:#fff}.juba-ref-ai-points{display:grid;gap:10px;margin:22px 0}.juba-ref-ai-points span{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:800}.juba-ref-reviews{width:min(1320px,calc(100% - 56px));margin:auto;padding:0 0 86px;background:transparent}.juba-ref-review-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.juba-ref-review-card{padding:24px;border:0;border-radius:24px;background:#fff;box-shadow:none}.juba-ref-review-card p{font-size:13px;line-height:1.7}.juba-ref-review-card strong{font-size:12px}.juba-ref-pricing{width:min(1320px,calc(100% - 56px));margin:auto;padding:86px 0;background:transparent}.juba-ref-cta{width:min(1320px,calc(100% - 56px));margin:0 auto 86px;padding:55px;border-radius:30px;background:var(--blue);color:#fff}.juba-ref-cta-inner{display:grid;grid-template-columns:1fr 360px;align-items:center;gap:50px}.juba-ref-cta p{color:#E4E5FF}.juba-ref-cta .juba-ref-kicker{background:#fff;color:var(--blue)}.juba-ref-cta-device{height:300px;border-radius:30px;background:var(--lav);border:0;box-shadow:12px 13px 0 var(--ink);display:grid;place-items:center;color:var(--ink);transform:rotate(4deg);font-weight:850}.juba-ref-faq{width:min(1320px,calc(100% - 56px));margin:auto;padding:0 0 100px;background:transparent}@media(max-width:900px){.juba-ref-hero-inner,.juba-ref-language-section,.juba-ref-ai-section,.juba-ref-cta-inner{grid-template-columns:1fr}.juba-ref-hero-copy{padding:42px 30px}.juba-ref-pillar-grid,.juba-ref-review-grid{grid-template-columns:1fr}.juba-ref-hero-art{min-height:500px}.juba-ref-cta-device{height:230px}}@media(max-width:560px){.juba-ref-hero{padding:0 14px 45px}.juba-ref-section,.juba-ref-language-section,.juba-ref-ai-section,.juba-ref-reviews,.juba-ref-pricing,.juba-ref-cta,.juba-ref-faq{width:calc(100% - 28px)}.juba-ref-hero-copy h1{font-size:3.4rem}.juba-ref-hero-art{min-height:430px}.character-main{width:150px;height:150px;right:28%;bottom:78px}.character-main>span{font-size:58px}.juba-ref-book{left:5%;bottom:34px;min-width:185px}.juba-ref-ground{left:16px;right:16px;bottom:16px;height:210px}}` }} />

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
