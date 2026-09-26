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
      <style dangerouslySetInnerHTML={{ __html: `

/* Funfluent-inspired public landing visual pass */
.juba-reference-page{
  font-family:Arial Rounded MT Bold, Nunito, Trebuchet MS, var(--font-geist-sans), Arial, sans-serif;
}
.juba-reference-page .juba-site-nav{
  background:transparent!important;
  border:0!important;
  backdrop-filter:none!important;
  padding:12px 14px 0;
}
.juba-reference-page .juba-ff-nav-inner{
  width:min(1180px,100%)!important;
  height:68px!important;
  padding:8px 10px 8px 16px!important;
  border:2px solid #183022;
  border-radius:999px;
  background:rgba(255,255,255,.94)!important;
  box-shadow:5px 5px 0 #183022;
}
.juba-reference-page .juba-ff-brand{gap:10px!important}
.juba-reference-page .juba-ff-brand-mark{
  width:42px!important;height:42px!important;border-radius:15px!important;
  box-shadow:3px 3px 0 #183022!important;transform:rotate(-4deg);
}
.juba-reference-page .juba-ff-brand-copy small{
  display:block;margin-top:1px;color:#68766d;font-size:8px;line-height:1;font-weight:800;letter-spacing:.03em;
}
.juba-reference-page .juba-ff-nav-link{font-size:11px!important;font-weight:850!important}
.juba-reference-page .juba-ff-nav-cta{
  border:2px solid #183022!important;border-radius:999px!important;
  padding:10px 15px!important;box-shadow:3px 3px 0 #183022!important;
}
.juba-reference-page .juba-nav-region{border:2px solid #183022!important;box-shadow:2px 2px 0 rgba(24,48,34,.12)}
.juba-reference-page .juba-landing-image-art{
  position:relative;display:flex;align-items:center;justify-content:center;
  min-height:520px;background:transparent!important;overflow:visible;
}
.juba-reference-page .juba-new-hero-photo{max-width:760px;border-radius:34px;border:2px solid #183022;box-shadow:10px 11px 0 #183022;object-fit:cover}
.juba-reference-page .juba-new-cta-photo{border-radius:30px;border:2px solid #183022;object-fit:cover}
.juba-reference-page .juba-landing-real-image{
  display:block;width:100%;height:auto;max-width:900px;
  filter:drop-shadow(0 18px 0 rgba(24,48,34,.08));
  animation:juba-landing-float 6s ease-in-out infinite;
}
.juba-reference-page .juba-ref-language-art{position:relative}
.juba-reference-page .juba-ref-language-art>.juba-landing-real-image{
  position:absolute;inset:0;width:100%;height:100%;object-fit:contain;z-index:0;
  animation:juba-landing-float 7s ease-in-out infinite;
}
.juba-reference-page .juba-ref-language-overlay{position:relative;z-index:2;width:100%;height:100%}
@keyframes juba-landing-float{0%,100%{transform:translateY(0) rotate(-.5deg)}50%{transform:translateY(-8px) rotate(.5deg)}}
@media(prefers-reduced-motion:reduce){.juba-reference-page .juba-landing-real-image{animation:none}}
.juba-reference-page .juba-ref-hero{
  margin-top:-80px;padding-top:78px;
  background:
    radial-gradient(circle at 8% 18%,rgba(255,226,122,.68),transparent 210px),
    radial-gradient(circle at 92% 34%,rgba(223,245,250,.9),transparent 260px),
    linear-gradient(180deg,#fffdf7 0%,#f6faed 100%);
}
.juba-reference-page .juba-ref-hero-copy h1{
  font-family:Arial Rounded MT Bold,Nunito,Trebuchet MS,var(--font-geist-sans),sans-serif;
  font-weight:950;letter-spacing:-.09em;
}
.juba-reference-page .juba-ref-hero-copy h1::after{
  content:"";display:block;width:110px;height:10px;margin-top:22px;border-radius:999px;
  background:#ffe27a;transform:rotate(-3deg);box-shadow:16px 3px 0 #3d7b27;
}
.juba-reference-page .juba-ref-hero-art{filter:saturate(1.04)}
.juba-reference-page .juba-ref-hero-art::before,.juba-reference-page .juba-ref-hero-art::after{
  content:"";position:absolute;z-index:6;pointer-events:none;
}
.juba-reference-page .juba-ref-hero-art::before{
  width:52px;height:52px;left:1%;top:10%;border:3px solid #183022;border-radius:50%;
  background:#ffd9d0;transform:rotate(-14deg);
}
.juba-reference-page .juba-ref-hero-art::after{
  width:34px;height:34px;right:1%;bottom:25%;border:3px solid #183022;border-radius:11px;
  background:#eee7ff;transform:rotate(17deg);
}
.juba-reference-page .juba-ref-book{border-radius:22px;transform:rotate(-2deg)}
.juba-reference-page .juba-ref-speech{border-radius:999px}
.juba-reference-page .juba-pillar-image{display:block;width:min(210px,72%);height:auto;margin:0 auto 10px;transition:transform .22s ease;filter:drop-shadow(0 7px 0 rgba(24,48,34,.08))}
.juba-reference-page .juba-pillar-image{will-change:transform}
.juba-reference-page .juba-ref-pillar:nth-child(2) .juba-pillar-image{animation:juba-landing-float 6.5s ease-in-out -1.5s infinite}
.juba-reference-page .juba-ref-pillar:nth-child(3) .juba-pillar-image{animation:juba-landing-float 7s ease-in-out -3s infinite}
.juba-reference-page .juba-cta-real-image{will-change:transform}
.juba-reference-page .juba-ref-pillar:hover .juba-pillar-image{transform:translateY(-5px) rotate(-2deg) scale(1.03)}
.juba-reference-page .juba-ref-pillar{border-radius:30px}
.juba-reference-page .juba-ref-pillar:nth-child(1){transform:rotate(-1.1deg)}
.juba-reference-page .juba-ref-pillar:nth-child(2){transform:translateY(9px) rotate(.7deg)}
.juba-reference-page .juba-ref-pillar:nth-child(3){transform:rotate(-.7deg)}
.juba-reference-page .juba-ref-pillar:hover{transform:translateY(-7px) rotate(0deg)}
.juba-reference-page .juba-ref-language-art{border-radius:34px 55px 42px 58px;transform:rotate(1deg)}
.juba-reference-page .juba-ref-ai-art{border-radius:36px 58px 45px 55px}
.juba-reference-page .juba-cta-real-image{max-width:520px;filter:drop-shadow(0 14px 0 rgba(24,48,34,.09))}
@media(max-width:560px){.juba-reference-page .juba-cta-real-image{max-width:100%;height:auto}}
.juba-reference-page .juba-ref-cta{position:relative}
.juba-reference-page .juba-ref-cta::before,.juba-reference-page .juba-ref-cta::after{
  content:"";position:absolute;border:3px solid #183022;pointer-events:none;
}
.juba-reference-page .juba-ref-cta::before{
  width:74px;height:74px;left:5%;top:15%;border-radius:50%;background:rgba(255,255,255,.24);transform:rotate(12deg);
}
.juba-reference-page .juba-ref-cta::after{
  width:42px;height:42px;right:7%;bottom:12%;border-radius:12px;background:#ffe27a;transform:rotate(-15deg);
}
@media(max-width:900px){
  .juba-reference-page .juba-site-nav{padding-top:8px}
  .juba-reference-page .juba-ff-nav-inner{width:calc(100% - 4px)!important}
  .juba-reference-page .juba-ref-hero{margin-top:-68px;padding-top:68px}
}
@media(max-width:560px){
  .juba-reference-page .juba-site-nav{padding-inline:7px}
  .juba-reference-page .juba-ff-nav-inner{height:60px!important;padding:6px 8px 6px 11px!important;border-radius:20px}
  .juba-reference-page .juba-ff-brand-mark{width:36px!important;height:36px!important}
  .juba-reference-page .juba-ff-brand-name{font-size:14px!important}
  .juba-reference-page .juba-ff-brand-copy small{display:none}
  .juba-reference-page .juba-ref-hero{margin-top:-60px;padding-top:65px}
  .juba-reference-page .juba-ref-hero-art::before{width:36px;height:36px}
  .juba-reference-page .juba-ref-hero-art::after{width:26px;height:26px}
  .juba-reference-page .juba-ref-pillar:nth-child(2){transform:none}
}
.juba-reference-page{--ink:#183022;--green:#3d7b27;--green-dark:#275d19;--mint:#e5f4d8;--blue:#dff5fa;--yellow:#ffe27a;--orange:#f6a23a;background:#fffdf7;color:var(--ink);font-family:var(--font-geist-sans),Arial,sans-serif}
.juba-reference-page .juba-site-nav{background:rgba(255,253,247,.94)!important;border-bottom:1px solid #d9e5d7!important;backdrop-filter:blur(18px)}
.juba-reference-page .juba-ff-nav-inner{height:76px!important;max-width:1240px!important}
.juba-reference-page .juba-ff-brand-mark{background:var(--green)!important;color:#fff!important;box-shadow:4px 4px 0 var(--ink)!important}
.juba-reference-page .juba-brand-spark,.juba-reference-page .juba-brand-accent{color:var(--green)!important}
.juba-reference-page .juba-ff-brand-name,.juba-reference-page .juba-ff-nav-link,.juba-reference-page .juba-ff-nav-signin{color:var(--ink)!important}
.juba-reference-page .juba-ff-nav-link:hover{color:var(--green)!important}
.juba-reference-page .juba-nav-region{border-color:#d9e5d7!important;background:#fff!important}
.juba-reference-page .juba-ff-nav-cta{background:var(--green)!important;color:#fff!important;border-radius:14px!important;box-shadow:4px 4px 0 var(--ink)!important}
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
.juba-reference-page .juba-ref-pricing{display:block!important;visibility:visible!important;min-height:620px;padding:110px 22px;background:#fffdf7;scroll-margin-top:90px}.juba-reference-page .juba-ref-pricing>div{max-width:1160px;margin:0 auto}
.juba-reference-page .juba-ref-cta-inner{position:relative}
.juba-reference-page .juba-ref-cta-inner:before{content:"✦";position:absolute;left:45%;top:-45px;font-size:70px;color:#ffe27a;text-shadow:3px 3px 0 var(--ink);transform:rotate(12deg);opacity:.95}
.juba-reference-page .juba-ref-cta-device{position:relative;transform:rotate(4deg)}
.juba-reference-page .juba-ref-faq .juba-ref-section-heading{position:relative}
.juba-reference-page .juba-ref-faq .juba-ref-section-heading:after{content:"";display:block;width:74px;height:6px;margin:24px auto 0;border-radius:99px;background:var(--green);box-shadow:12px 0 0 var(--yellow),24px 0 0 #dff5fa}
@media(max-width:900px){.juba-reference-page .juba-ref-cta-inner:before{left:auto;right:8%;top:-35px}.juba-reference-page .juba-ref-language-art{min-height:360px}}
@media(max-width:560px){.juba-reference-page .juba-ref-cta-inner:before{font-size:48px;top:-20px}.juba-reference-page .juba-ref-language-art{min-height:300px}.juba-reference-page .juba-ff-nav-inner{height:68px!important}.juba-reference-page .juba-ref-hero-actions{flex-direction:column;align-items:stretch}.juba-reference-page .juba-ref-hero-actions .juba-ref-button,.juba-reference-page .juba-ref-hero-actions .juba-ref-text-link{width:100%;justify-content:center;text-align:center}.juba-reference-page .juba-ref-pillar-grid{grid-template-columns:1fr}.juba-reference-page .juba-ref-ai-art{transform:none;box-shadow:7px 8px 0 var(--ink)}.juba-reference-page .juba-ref-cta-inner{gap:34px}.juba-reference-page .juba-ref-cta-device{max-width:86%;margin-inline:auto}.juba-reference-page .juba-ref-section-heading h2,.juba-reference-page .juba-ref-language-copy h2,.juba-reference-page .juba-ref-ai-copy h2,.juba-reference-page .juba-ref-cta h2{font-size:clamp(2rem,9vw,3rem);line-height:1.05}}
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
.juba-reference-page .juba-games-showcase{padding:110px 22px;background:#fffdf7}
.juba-reference-page .juba-games-heading{width:min(760px,100%);margin:0 auto 44px;text-align:center}
.juba-reference-page .juba-games-heading h2{margin:17px 0 13px;font-size:clamp(2.4rem,5vw,4.8rem);line-height:.9;letter-spacing:-.075em;font-weight:950;color:#183022}
.juba-reference-page .juba-games-heading p{margin:0;color:#68766d;font-size:14px;line-height:1.8}
.juba-reference-page .juba-games-grid{width:min(1120px,100%);margin:0 auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.juba-reference-page .juba-games-tabs{width:min(1120px,100%);margin:0 auto 18px;display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
.juba-reference-page .juba-games-tab{border:2px solid #183022;border-radius:999px;background:#fff;padding:9px 14px;color:#68766d;font-size:10px;font-weight:900;transition:transform .16s,background .16s,color .16s,box-shadow .16s}
.juba-reference-page .juba-games-tab:hover{transform:translateY(-2px);color:#183022}
.juba-reference-page .juba-games-tab.is-active{background:#3d7b27;color:#fff;box-shadow:3px 3px 0 #183022}
.juba-reference-page .juba-game-stage{width:min(1120px,100%);margin:0 auto;display:grid;grid-template-columns:1.25fr .75fr;align-items:center;gap:28px;padding:18px;border:2px solid #183022;border-radius:30px;background:#eef7e4;box-shadow:6px 7px 0 #183022}
.juba-reference-page .juba-game-stage-image{padding:10px;border:2px solid #183022;border-radius:24px;background:#fff;overflow:hidden}
.juba-reference-page .juba-game-stage-image img{display:block;width:100%;height:auto;border-radius:16px}
.juba-reference-page .juba-game-stage-copy{padding:24px}
.juba-reference-page .juba-game-stage-index{display:inline-flex;border:1px solid #d9e5d7;border-radius:999px;background:#fff;padding:7px 10px;color:#39751d;font-size:9px;font-weight:900}
.juba-reference-page .juba-game-stage-copy h3{margin:18px 0 8px;color:#183022;font-size:clamp(1.8rem,3vw,3rem);font-weight:950;letter-spacing:-.06em}
.juba-reference-page .juba-game-stage-copy p{margin:0 0 22px;color:#68766d;font-size:13px;line-height:1.7}
.juba-reference-page .juba-game-stage-copy .juba-ref-button{display:inline-flex}
@media(max-width:900px){.juba-reference-page .juba-game-stage{grid-template-columns:1fr}.juba-reference-page .juba-game-stage-copy{padding:14px 8px 8px}}
.juba-reference-page .juba-game-card{min-width:0;border:2px solid #183022;border-radius:26px;background:#fff;overflow:hidden;box-shadow:5px 6px 0 #183022;transition:transform .18s ease,box-shadow .18s ease}
.juba-reference-page .juba-game-card:hover{transform:translateY(-5px) rotate(-.4deg);box-shadow:8px 9px 0 #183022}
.juba-reference-page .juba-game-image-wrap{padding:10px;background:#f3f7ee}
.juba-reference-page .juba-game-image-wrap img{display:block;width:100%;height:auto;border-radius:18px}
.juba-reference-page .juba-game-card-copy{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:15px 16px}
.juba-reference-page .juba-game-card-copy strong{font-size:12px;color:#183022}
.juba-reference-page .juba-game-card-copy span{display:inline-flex;align-items:center;gap:4px;color:#39751d;font-size:10px;font-weight:900}
.juba-reference-page .juba-game-card-copy svg{width:13px;height:13px}
.juba-reference-page .juba-ai-showcase{padding:120px max(22px,calc((100% - 1160px)/2));display:grid;grid-template-columns:1.15fr .85fr;align-items:center;gap:75px;background:#f2edff}
.juba-reference-page .juba-ai-showcase-art{position:relative;min-height:470px;border:2px solid #183022;border-radius:36px 58px 45px 55px;background:#fff;box-shadow:12px 13px 0 #183022;overflow:hidden}
.juba-reference-page .juba-ai-showcase-image{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;padding:36px;filter:drop-shadow(0 14px 0 rgba(24,48,34,.09));animation:juba-landing-float 7s ease-in-out infinite}
.juba-reference-page .juba-ai-chat-bubble{position:absolute;z-index:4;max-width:42%;padding:11px 14px;border:2px solid #183022;border-radius:16px;background:#fff;font-size:11px;line-height:1.45;font-weight:800;box-shadow:4px 4px 0 #183022}
.juba-reference-page .juba-ai-chat-user{left:6%;top:14%;background:#fff0b7}
.juba-reference-page .juba-ai-chat-tutor{right:6%;bottom:18%;background:#dff5fa}
.juba-reference-page .juba-ai-wave{position:absolute;left:50%;bottom:28px;z-index:5;display:flex;align-items:center;gap:5px;transform:translateX(-50%)}
.juba-reference-page .juba-ai-wave i{display:block;width:5px;height:15px;border-radius:999px;background:#3d7b27;transform-origin:center;animation:none}
.juba-reference-page .juba-ai-wave i.is-playing{animation:juba-ai-wave 720ms ease-in-out infinite alternate;animation-delay:var(--wave-delay)}
@keyframes juba-ai-wave{from{transform:scaleY(.45)}to{transform:scaleY(1.6)}}
.juba-reference-page .juba-ai-play{position:absolute;right:22px;bottom:20px;z-index:6;width:42px;height:42px;display:grid;place-items:center;border:2px solid #183022;border-radius:50%;background:#3d7b27;color:#fff;box-shadow:3px 3px 0 #183022}
.juba-reference-page .juba-ai-play svg{width:16px;height:16px}
.juba-reference-page .juba-ai-live-pill{position:absolute;left:22px;bottom:20px;z-index:6;display:inline-flex;align-items:center;gap:6px;padding:8px 10px;border:1px solid #d9e5d7;border-radius:999px;background:rgba(255,255,255,.94);font-size:9px;font-weight:900;color:#275d19}
.juba-reference-page .juba-ai-live-pill svg{width:13px;height:13px}
.juba-reference-page .juba-ai-showcase-copy h2{margin:17px 0 14px;font-size:clamp(2.7rem,5.5vw,5.2rem);line-height:.9;letter-spacing:-.08em;font-weight:950;color:#183022}
.juba-reference-page .juba-ai-showcase-copy p{max-width:510px;margin-bottom:26px;color:#68766d;font-size:14px;line-height:1.8}
.juba-reference-page .juba-ai-showcase-copy .juba-ref-button{display:inline-flex}
@media(max-width:900px){.juba-reference-page .juba-games-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.juba-reference-page .juba-ai-showcase{grid-template-columns:1fr;gap:40px;padding-top:85px;padding-bottom:85px}}
@media(max-width:560px){.juba-reference-page .juba-games-showcase{padding:76px 14px}.juba-reference-page .juba-games-grid{grid-template-columns:1fr}.juba-reference-page .juba-ai-showcase{padding:75px 16px}.juba-reference-page .juba-ai-showcase-art{min-height:350px}.juba-reference-page .juba-ai-showcase-image{padding:24px}.juba-reference-page .juba-ai-chat-bubble{max-width:48%;font-size:9px}.juba-reference-page .juba-ai-showcase-copy h2{font-size:clamp(2rem,9vw,3rem);line-height:1.05}}
` }} />


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
          <Image
            src="/landing/juba-language-atlas.svg"
            alt={t('languagesHeadline')}
            width={760}
            height={560}
            className="juba-landing-real-image"
          />
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
