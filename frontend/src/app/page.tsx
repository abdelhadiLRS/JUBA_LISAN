import Link from 'next/link'
import {cookies} from 'next/headers'
import {getLocale,getTranslations} from 'next-intl/server'
import type {Metadata} from 'next'
import PricingSection from '@/components/billing/PricingSection'
import {LandingFAQ} from '@/components/ui/landing-faq'
import {LandingNav} from '@/components/ui/landing-nav'
import {ContactButton} from '@/components/ui/contact-button'
import {LanguageBubbles} from '@/components/LanguageBubbles'
import {LandingReviewsCarousel} from '@/components/reviews/LandingReviewsCarousel'
import type {ReviewPublic} from '@/types/api'
import {normalizeLocale} from '@/lib/locales'
import './landing-refresh.css'

export const metadata:Metadata={
  title:'JUBA LISAN | Learn languages naturally with AI',
  description:'Learn languages naturally with AI through speaking, listening, reading, vocabulary, grammar, and personalized practice.',
  robots:{index:true,follow:true},
  openGraph:{title:'JUBA LISAN | AI-powered language learning',description:'Speaking, listening, reading and personalized language practice.',url:'https://jubalisan.com',type:'website',images:[{url:'/og-image-v2.png',width:1200,height:630,alt:'JUBA LISAN | AI-powered language learning'}]},
  twitter:{card:'summary_large_image',title:'JUBA LISAN | AI-powered language learning',description:'Learn with an AI tutor, voice conversations, flashcards, and structured grammar lessons.',images:['/og-image-v2.png']},
}

/** Original decorative artwork, not a screenshot or fabricated account data. */
function LearningArtwork({variant=0}:{variant?:number}){
  return <svg viewBox="0 0 640 480" fill="none" aria-hidden="true" className={`jl-art jl-art-${variant}`}>
    <ellipse cx="330" cy="426" rx="214" ry="20" fill="var(--jl-line)"/>
    <rect x="208" y="40" width="232" height="380" rx="30" fill="var(--jl-surface)" stroke="var(--jl-ink)" strokeWidth="3"/>
    <rect x="284" y="54" width="80" height="8" rx="4" fill="var(--jl-line)"/>
    <rect x="230" y="84" width="188" height="136" rx="16" fill="var(--jl-soft)"/>
    <circle cx="324" cy="133" r="26" fill="var(--jl-green)"/>
    <path d="m311 133 9 9 18-20" stroke="var(--jl-surface)" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round"/>
    <rect x="258" y="179" width="132" height="8" rx="4" fill="var(--jl-green)"/>
    <rect x="270" y="197" width="108" height="5" rx="2.5" fill="var(--jl-line)"/>
    {[250,287,324].map((y,index)=><g key={y}><circle cx="248" cy={y} r="9" fill={index===variant%3?'var(--jl-amber)':'var(--jl-soft)'}/><rect x="270" y={y-5} width={110-index*17} height="10" rx="5" fill="var(--jl-line)"/></g>)}
    <rect x="230" y="356" width="188" height="40" rx="20" fill="var(--jl-green)"/>
    <path d="M97 108h142a16 16 0 0 1 16 16v44a16 16 0 0 1-16 16h-75l-28 24v-24H97a16 16 0 0 1-16-16v-44a16 16 0 0 1 16-16Z" fill="var(--jl-amber)"/>
    <path d="M109 137h98m-98 17h65" stroke="var(--jl-ink)" strokeWidth="6" strokeLinecap="round"/>
    <path d="M431 233h110a16 16 0 0 1 16 16v45a16 16 0 0 1-16 16h-31v22l-27-22h-52a16 16 0 0 1-16-16v-45a16 16 0 0 1 16-16Z" fill="var(--jl-soft)" stroke="var(--jl-green)" strokeWidth="2"/>
    <path d="M440 273v-8m12 20v-32m12 39v-46m12 38v-30m12 20v-10m12 15v-20m12 26v-34m12 23v-12" stroke="var(--jl-green)" strokeWidth="4" strokeLinecap="round"/>
    <path d="m493 84 8 18 19 2-14 13 4 19-17-10-17 10 4-19-14-13 19-2Z" fill="var(--jl-amber)"/>
    <circle cx="118" cy="308" r="32" fill="var(--jl-green)"/>
    <path d="m105 307 10 10 18-21" stroke="var(--jl-surface)" strokeWidth="5" strokeLinecap="round"/>
  </svg>
}

export default async function Home(){
  const cookieStore=await cookies()
  const hasSession=cookieStore.has('refresh_token')
  const locale=normalizeLocale(await getLocale())
  const dir=locale==='ar'?'rtl':'ltr'
  const t=await getTranslations('landing')
  const common=await getTranslations('common')
  const billing=await getTranslations('billing')
  let allowRegistration=false,stripeEnabled=false,trialDays=7
  let priceMonthly=0,priceYearly=0,totalPriceMonthly=0,totalPriceYearly=0
  let reviews:ReviewPublic[]=[]
  const backendUrl=process.env.BACKEND_URL||'http://backend:8000'
  // Independent failures must not discard legitimate reviews or billing config.
  const [configResponse,reviewsResponse]=await Promise.allSettled([
    fetch(`${backendUrl}/api/config`,{next:{revalidate:3600}}),
    fetch(`${backendUrl}/api/reviews/public?limit=100`,{next:{revalidate:300}}),
  ])
  if(configResponse.status==='fulfilled'&&configResponse.value.ok){
    try{const cfg=await configResponse.value.json();allowRegistration=cfg.allow_registration===true;stripeEnabled=cfg.stripe_enabled===true;trialDays=cfg.stripe_trial_days??7;priceMonthly=cfg.price_monthly??0;priceYearly=cfg.price_yearly??0;totalPriceMonthly=cfg.total_price_monthly??0;totalPriceYearly=cfg.total_price_yearly??0}catch{/* Keep conservative defaults. */}
  }
  if(reviewsResponse.status==='fulfilled'&&reviewsResponse.value.ok){
    try{const data=await reviewsResponse.value.json();reviews=Array.isArray(data)?data:[]}catch{/* No invented testimonials. */}
  }
  const href=hasSession?'/dashboard':allowRegistration?'/register':'/login'
  const cta=hasSession?t('dashboard'):allowRegistration?t('ctaStart'):t('signIn')
  const features=[{title:t('feature1Title'),desc:t('feature1Desc')},{title:t('feature2Title'),desc:t('feature2Desc')},{title:t('feature3Title'),desc:t('feature3Desc')}]
  const jsonLd={'@context':'https://schema.org','@type':'SoftwareApplication',name:'JUBA LISAN',applicationCategory:'EducationApplication',operatingSystem:'Web',url:'https://jubalisan.com',description:'AI-powered language learning with conversation, vocabulary, grammar, listening and reading.'}
  return <div className="juba-landing-refresh" dir={dir}>
    <script type="application/ld+json" dangerouslySetInnerHTML={{__html:JSON.stringify(jsonLd)}}/>
    <a className="jl-skip" href="#main-content">{t('skipToContent')}</a>
    <LandingNav hasSession={hasSession} allowRegistration={allowRegistration} dir={dir} navFeatures={t('navFeatures')} primaryNavigation={common('menu')} navLanguages={t('navLanguages')} interfaceLanguages={t('interfaceLanguages')} navReviews={t('navReviews')} showReviews={reviews.length>0} signIn={t('signIn')} dashboard={t('dashboard')} getStarted={t('ctaStart')} homeLabel={t('homeLabel')} openMenuLabel={t('openMenuLabel')} closeMenuLabel={t('closeMenuLabel')} locale={locale}/>
    <main id="main-content">
      <section className="jl-hero" aria-labelledby="landing-hero-title"><div className="jl-wrap jl-hero-inner"><div className="jl-hero-copy"><span className="jl-eyebrow">JUBA LISAN · {common('tagline')}</span><h1 id="landing-hero-title">{t('heroTitle')}</h1><p>{t('heroSub')}</p><Link className="jl-primary" href={href}>{cta}<span aria-hidden="true">{dir==='rtl'?'←':'→'}</span></Link><a className="jl-text-link" href="#languages">{t('navLanguages')}</a></div><div className="jl-hero-art"><LearningArtwork/><span className="jl-art-caption">{features[0].title} · {features[1].title}</span></div></div></section>
      <section id="languages" className="jl-languages" aria-labelledby="landing-languages-title"><div className="jl-wrap"><header className="jl-section-head"><h2 id="landing-languages-title">{t('navLanguages')}</h2><Link className="jl-text-link" href={href}>{cta} <span aria-hidden="true">↗</span></Link></header><LanguageBubbles dir={dir}/></div></section>
      <section id="features" className="jl-features" aria-labelledby="landing-features-title"><div className="jl-wrap"><header className="jl-feature-intro"><span className="jl-eyebrow">JUBA LISAN</span><h2 id="landing-features-title">{t('navFeatures')}</h2></header>{features.map((feature,index)=><article key={feature.title} className={`jl-feature-row jl-feature-row-${index}`}><div className="jl-feature-visual" aria-hidden="true"><LearningArtwork variant={index}/></div><div className="jl-feature-copy"><span className="jl-feature-number">0{index+1}</span><h3>{feature.title}</h3><p>{feature.desc}</p><Link className="jl-text-link" href={href}>{cta} <span aria-hidden="true">{dir==='rtl'?'←':'→'}</span></Link></div></article>)}</div></section>
      {reviews.length>0&&<section id="reviews" className="jl-reviews" aria-labelledby="landing-reviews-title"><div className="jl-wrap"><h2 id="landing-reviews-title">{t('navReviews')}</h2><LandingReviewsCarousel reviews={reviews}/></div></section>}
      <section id="pricing" className="jl-pricing" aria-labelledby="landing-pricing-title"><div className="jl-wrap"><h2 id="landing-pricing-title">{t('navPricing')}</h2><PricingSection stripeEnabled={stripeEnabled} trialDays={trialDays} hasSession={hasSession} priceMonthly={priceMonthly} priceYearly={priceYearly} totalPriceMonthly={totalPriceMonthly} totalPriceYearly={totalPriceYearly}/></div></section>
      <section className="jl-cta-band"><div className="jl-wrap"><span className="jl-eyebrow">JUBA LISAN</span><h2>{t('heroTitle')}</h2><p>{t('heroSub')}</p><Link href={href} className="jl-primary">{cta}</Link></div></section>
      <section className="jl-open-source"><div className="jl-wrap"><div><h2>{billing('openSourceTitle')}</h2><p>{billing('openSourceDesc')}</p></div><a href="https://github.com/abdelhadiLRS/JUBA_LISAN" target="_blank" rel="noopener noreferrer" className="jl-text-link">{billing('openSourceCta')} ↗</a></div></section>
      <section id="faq" className="jl-faq" aria-labelledby="landing-faq-title"><div className="jl-wrap"><h2 id="landing-faq-title">{t('faqTitle')}</h2><LandingFAQ dir={dir}/></div></section>
    </main>
    <footer className="jl-footer"><div className="jl-wrap jl-footer-grid"><div className="jl-footer-brand"><strong>JUBA LISAN</strong><p>{t('footerTagline')}</p><small>© {new Date().getFullYear()} JUBA LISAN</small></div><nav aria-label={t('footerProduct')}><h3>{t('footerProduct')}</h3><a href="#features">{t('navFeatures')}</a><a href="#languages">{t('navLanguages')}</a>{reviews.length>0&&<a href="#reviews">{t('navReviews')}</a>}<a href="#pricing">{t('navPricing')}</a></nav><nav aria-label={t('footerResources')}><h3>{t('footerResources')}</h3><a href="#faq">{t('navFAQ')}</a><a href="https://github.com/abdelhadiLRS/JUBA_LISAN" target="_blank" rel="noopener noreferrer">{t('github')}</a><ContactButton/></nav><nav aria-label={t('footerLegal')}><h3>{t('footerLegal')}</h3><Link href="/privacy?from=landing">{t('privacy')}</Link><Link href="/terms?from=landing">{t('terms')}</Link></nav></div></footer>
  </div>
}
