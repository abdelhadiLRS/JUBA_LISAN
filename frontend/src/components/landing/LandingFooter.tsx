import Image from 'next/image'
import Link from 'next/link'
import { ContactButton } from '@/components/ui/contact-button'
import type { Locale } from '@/lib/locales'

interface LandingFooterProps {
  t: (key: string) => string
  hasSession: boolean
  dir?: 'ltr' | 'rtl'
  locale?: Locale
  showReviews?: boolean
}

export function LandingFooter({ t, hasSession, dir = 'ltr', locale = 'en', showReviews = false }: LandingFooterProps) {
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
            <Link href={locale === 'en' ? '/' : `/${locale}`} className="juba-busuu-footer-logo" aria-label="JUBA LISAN">
              <Image src="/logo.png" alt="JUBA LISAN" width={168} height={58} />
            </Link>
            <p>{t('footerTagline')}</p>
          </div>
          <div className="juba-busuu-footer-intro-links">
            <Link href="#languages">{t('navLanguages')}</Link>
            <Link href="#pricing">{t('navPricing')}</Link>
            <Link href={hasSession ? '/dashboard' : '/register'}>{hasSession ? t('dashboard') : t('ctaStart')}</Link>
          </div>
        </div>

        <div className="juba-busuu-footer-grid">
          <div className="juba-busuu-footer-column">
            <h3>{t('footerLearning')}</h3>
            <Link href="#features">{t('howItWorks')}</Link>
            <Link href="#languages">{t('navLanguages')}</Link>
            <Link href="#benefits">{t('builtForLearners')}</Link>
            {showReviews && <Link href="#reviews">{t('navReviews')}</Link>}
          </div>

          <div className="juba-busuu-footer-column">
            <h3>{t('aboutMe')}</h3>
            <Link href="#features">{t('navFeatures')}</Link>
            <Link href="#pricing">{t('navPricing')}</Link>
            <a href="https://github.com/abdelhadiLRS/JUBA_LISAN" target="_blank" rel="noopener noreferrer">{t('github')}</a>
          </div>

          <div className="juba-busuu-footer-column">
            <h3>{t('footerProduct')}</h3>
            <Link href={hasSession ? '/dashboard' : '/register'}>{hasSession ? t('dashboard') : t('ctaStart')}</Link>
            <Link href="#languages">{t('availableInApp')}</Link>
            <Link href="#faq">{t('navFAQ')}</Link>
          </div>

          <div className="juba-busuu-footer-column">
            <h3>{t('footerResources')}</h3>
            <span className="juba-busuu-footer-contact"><ContactButton /></span>
            <Link href="/privacy?from=landing">{t('privacy')}</Link>
            <Link href="/terms?from=landing">{t('terms')}</Link>
          </div>
        </div>

        <div className="juba-busuu-footer-language">
          <div id="juba-busuu-footer-language-heading" className="juba-busuu-footer-language-heading">
            <strong>{t('navLanguages')}</strong>
          </div>
          <nav className="juba-busuu-footer-language-list" aria-labelledby="juba-busuu-footer-language-heading">
            {footerLanguages.map(([label, code]) => (
              <Link
                key={code}
                href={code === 'en' ? '/' : `/${code}`}
                lang={code}
                dir="auto"
                aria-current={code === locale ? 'page' : undefined}
              >
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
