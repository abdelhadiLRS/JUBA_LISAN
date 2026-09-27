import Image from 'next/image'
import Link from 'next/link'
import { ContactButton } from '@/components/ui/contact-button'

interface LandingFooterProps {
  t: (key: string) => string
  dir?: 'ltr' | 'rtl'
}

export function LandingFooter({ t, dir = 'ltr' }: LandingFooterProps) {
  const footerLanguages = [
    ['English', 'en'],
    ['Français', 'fr'],
    ['Español', 'es'],
    ['Deutsch', 'de'],
    ['Italiano', 'it'],
    ['Português', 'pt'],
    ['日本語', 'ja'],
    ['한국어', 'ko'],
    ['العربية', 'ar'],
    ['中文', 'zh'],
    ['Русский', 'ru'],
    ['Türkçe', 'tr'],
    ['Nederlands', 'nl'],
    ['Polski', 'pl'],
  ]

  return (
    <footer dir={dir} className="juba-duo-footer">
      <div className="juba-busuu-footer-shell">
        <div className="juba-busuu-footer-top">
          <div className="juba-busuu-footer-brand">
            <Link href="/" className="juba-busuu-footer-logo" aria-label="JUBA LISAN">
              <Image src="/logo.png" alt="JUBA LISAN" width={180} height={62} />
            </Link>
            <p>{t('footerTagline')}</p>
          </div>

          <div className="juba-busuu-footer-social" aria-label="JUBA LISAN social links">
            <a href="https://github.com/abdelhadiLRS/JUBA_LISAN" target="_blank" rel="noopener noreferrer" aria-label="GitHub">GitHub</a>
          </div>
        </div>

        <div className="juba-busuu-footer-grid">
          <div className="juba-busuu-footer-column">
            <h3>{t('footerProduct')}</h3>
            <Link href="#features">{t('navFeatures')}</Link>
            <Link href="#features">{t('navFeatures')}</Link>
            <Link href="#languages">{t('navLanguages')}</Link>
            <Link href="#pricing">{t('navPricing')}</Link>
          </div>

          <div className="juba-busuu-footer-column">
            <h3>{t('aboutMe')}</h3>
            <Link href="#reviews">{t('navReviews')}</Link>
            <Link href="#faq">{t('navFAQ')}</Link>
            <Link href="/">{t('homeLabel')}</Link>
            <Link href="/register">{t('ctaStart')}</Link>
          </div>

          <div className="juba-busuu-footer-column">
            <h3>{t('footerLearning')}</h3>
            <Link href="#languages">{t('supportedLanguages')}</Link>
            <Link href="#features">{t('navFeatures')}</Link>
            <Link href="#features">{t('howItWorks')}</Link>
            <Link href="/register">{t('ctaExplore')}</Link>
          </div>

          <div className="juba-busuu-footer-column">
            <h3>{t('footerResources')}</h3>
            <Link href="#faq">{t('navFAQ')}</Link>
            <a href="https://github.com/abdelhadiLRS/JUBA_LISAN" target="_blank" rel="noopener noreferrer">{t('github')}</a>
            <span className="juba-busuu-footer-contact"><ContactButton /></span>
          </div>

          <div className="juba-busuu-footer-column">
            <h3>{t('footerLegal')}</h3>
            <Link href="/privacy?from=landing">{t('privacy')}</Link>
            <Link href="/terms?from=landing">{t('terms')}</Link>
          </div>
        </div>

        <div className="juba-busuu-footer-language">
          <span>{dir === 'rtl' ? 'لغة الواجهة' : 'Interface language'}</span>
          <div className="juba-busuu-footer-language-list">
            {footerLanguages.map(([label, code]) => (
              <Link key={code} href={code === 'en' ? '/' : `/?locale=${code}`}>
                {label}
              </Link>
            ))}
          </div>
        </div>

        <div className="juba-busuu-footer-bottom">
          <span>© {new Date().getFullYear()} JUBA LISAN. All rights reserved.</span>
          <div>
            <Link href="/terms?from=landing">{t('terms')}</Link>
            <Link href="/privacy?from=landing">{t('privacy')}</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
