import Image from 'next/image'
import Link from 'next/link'
import { ContactButton } from '@/components/ui/contact-button'

interface LandingFooterProps {
  t: (key: string) => string
  dir?: 'ltr' | 'rtl'
  showReviews?: boolean
}

export function LandingFooter({ t, dir = 'ltr', showReviews = false }: LandingFooterProps) {
  const footerLanguages = [
    ['English', 'en'], ['Français', 'fr'], ['Español', 'es'], ['Deutsch', 'de'],
    ['Italiano', 'it'], ['Português', 'pt'], ['العربية', 'ar'], ['Русский', 'ru'],
    ['Nederlands', 'nl'], ['Polski', 'pl'], ['Română', 'ro'],
  ]

  return (
    <footer dir={dir} className="juba-busuu-footer">
      <div className="juba-busuu-footer-shell">
        <div className="juba-busuu-footer-intro">
          <div className="juba-busuu-footer-brand">
            <Link href="/" className="juba-busuu-footer-logo" aria-label="JUBA LISAN">
              <Image src="/logo.png" alt="JUBA LISAN" width={168} height={58} />
            </Link>
            <p>{t('footerTagline')}</p>
          </div>
          <div className="juba-busuu-footer-intro-links">
            <Link href="#languages">{t('navLanguages')}</Link>
            <Link href="#pricing">{t('navPricing')}</Link>
            <Link href="/register">{t('ctaStart')}</Link>
          </div>
        </div>

        <div className="juba-busuu-footer-grid">
          <div className="juba-busuu-footer-column">
            <h3>{t('footerLearning')}</h3>
            <Link href="#features">{t('navFeatures')}</Link>
            <Link href="#languages">{t('supportedLanguages')}</Link>
            <Link href="#features">{t('howItWorks')}</Link>
            <Link href="/register">{t('ctaExplore')}</Link>
          </div>

          <div className="juba-busuu-footer-column">
            <h3>{t('footerProduct')}</h3>
            <Link href="#pricing">{t('navPricing')}</Link>
            {showReviews && <Link href="#reviews">{t('navReviews')}</Link>}
            <Link href="#faq">{t('navFAQ')}</Link>
          </div>

          <div className="juba-busuu-footer-column">
            <h3>{t('footerResources')}</h3>
            <a href="https://github.com/abdelhadiLRS/JUBA_LISAN" target="_blank" rel="noopener noreferrer">{t('github')}</a>
            <span className="juba-busuu-footer-contact"><ContactButton /></span>
          </div>

          <div className="juba-busuu-footer-column">
            <h3>{t('aboutMe')}</h3>
            <Link href="/privacy?from=landing">{t('privacy')}</Link>
            <Link href="/terms?from=landing">{t('terms')}</Link>
            <Link href="/register">{t('ctaStart')}</Link>
          </div>
        </div>

        <div className="juba-busuu-footer-language">
          <div id="juba-busuu-footer-language-heading" className="juba-busuu-footer-language-heading">
            <strong>{t('navLanguages')}</strong>
          </div>
          <nav className="juba-busuu-footer-language-list" aria-labelledby="juba-busuu-footer-language-heading">
            {footerLanguages.map(([label, code]) => (
              <Link key={code} href={code === 'en' ? '/' : `/${code}`} lang={code} dir="auto">
                {label}
              </Link>
            ))}
          </nav>
        </div>

        <div className="juba-busuu-footer-bottom">
          <span>© {new Date().getFullYear()} JUBA LISAN</span>
          <div>
            <Link href="/terms?from=landing">{t('terms')}</Link>
            <Link href="/privacy?from=landing">{t('privacy')}</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
