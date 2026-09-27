import Image from 'next/image'
import Link from 'next/link'
import { ContactButton } from '@/components/ui/contact-button'

interface LandingFooterProps {
  t: (key: string) => string
  dir?: 'ltr' | 'rtl'
}

export function LandingFooter({ t, dir = 'ltr' }: LandingFooterProps) {
  return (
    <footer dir={dir} className="juba-duo-footer pt-16 pb-10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-10 mb-12">
          {/* Brand Info */}
          <div className="md:col-span-2">
            <Link href="/" className="mb-4 inline-flex items-center gap-3 group" aria-label="JUBA LISAN">
              <Image
                src="/logo.png"
                alt="JUBA LISAN"
                width={180}
                height={62}
                className="h-14 w-auto max-w-[180px] object-contain"
              />
            </Link>
            <p className="juba-footer-copy text-sm max-w-sm leading-relaxed mb-6">
              {t('footerTagline')}
            </p>
            <p className="juba-footer-meta text-xs font-semibold">
              © {new Date().getFullYear()} JUBA LISAN. All rights reserved.
            </p>
          </div>

          {/* Product Links */}
          <div>
            <h4 className="juba-footer-title font-black text-xs uppercase tracking-wider mb-4">
              {t('footerProduct')}
            </h4>
            <ul className="space-y-3 text-sm font-bold">
              <li><a href="#features" className="juba-footer-link transition-colors">{t('navFeatures')}</a></li>
              <li><a href="#games" className="juba-footer-link transition-colors">{t('navDemo')}</a></li>
              <li><a href="#languages" className="juba-footer-link transition-colors">{t('supportedLanguages')}</a></li>
              <li><a href="#pricing" className="juba-footer-link transition-colors">{t('navPricing')}</a></li>
            </ul>
          </div>

          {/* Resources Links */}
          <div>
            <h4 className="font-black text-xs text-[var(--juba-app-yellow)] uppercase tracking-wider mb-4">
              {t('footerResources')}
            </h4>
            <ul className="space-y-3 text-sm font-bold">
              <li><a href="#faq" className="juba-footer-link transition-colors">{t('navFAQ')}</a></li>
              <li><a href="https://github.com/abdelhadiLRS/JUBA_LISAN" target="_blank" rel="noopener noreferrer" className="juba-footer-link transition-colors">{t('github')}</a></li>
              <li className="pt-1"><ContactButton /></li>
            </ul>
          </div>

          {/* Legal Links */}
          <div>
            <h4 className="font-black text-xs text-[var(--juba-app-yellow)] uppercase tracking-wider mb-4">
              {t('footerLegal')}
            </h4>
            <ul className="space-y-3 text-sm font-bold">
              <li><Link href="/privacy?from=landing" className="juba-footer-link transition-colors">{t('privacy')}</Link></li>
              <li><Link href="/terms?from=landing" className="juba-footer-link transition-colors">{t('terms')}</Link></li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="juba-footer-bottom pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-bold">
          <span>{t('builtForLearners')}</span>
          <span>{t('footerPositioning')}</span>
        </div>
      </div>
    </footer>
  )
}
