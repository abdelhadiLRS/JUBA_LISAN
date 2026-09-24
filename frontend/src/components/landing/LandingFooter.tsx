import Link from 'next/link'
import { ContactButton } from '@/components/ui/contact-button'

interface LandingFooterProps {
  t: (key: string) => string
}

export function LandingFooter({ t }: LandingFooterProps) {
  return (
    <footer className="juba-ff-footer border-t pt-16 pb-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-10 mb-12">
          <div className="md:col-span-2">
            <Link href="/" className="flex items-center gap-3 mb-4">
              <div className="juba-footer-brand-mark flex h-9 w-9 items-center justify-center rounded-xl bg-[var(--juba-app-yellow)] text-[var(--juba-app-ink)] font-bold text-lg shadow-[0_4px_0_var(--juba-app-ink)] border-2 border-[var(--juba-app-ink)]">
                J
              </div>
              <span className="font-sans text-xl font-extrabold tracking-tight text-[var(--juba-app-ink)]">
                JUBA <span className="text-[var(--juba-app-green-dark)]">LISAN</span>
              </span>
            </Link>
            <p className="text-[var(--juba-app-muted)] text-sm max-w-sm leading-relaxed mb-6">
              {t('footerTagline')}
            </p>
            <p className="juba-footer-note text-xs">
              © {new Date().getFullYear()} JUBA LISAN. All rights reserved.
            </p>
          </div>

          <div>
            <h4 className="font-bold text-sm text-[var(--juba-app-ink)] uppercase tracking-wider mb-4">
              {t('footerProduct')}
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li><a href="#features" className="text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] transition-colors">{t('navFeatures')}</a></li>
              <li><a href="#demo" className="text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] transition-colors">{t('aiVoiceDemo')}</a></li>
              <li><a href="#languages" className="text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] transition-colors">{t('supportedLanguages')}</a></li>
              <li><a href="#pricing" className="text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] transition-colors">{t('navPricing')}</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-sm text-[var(--juba-app-ink)] uppercase tracking-wider mb-4">
              {t('footerResources')}
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li><a href="#faq" className="text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] transition-colors">{t('navFAQ')}</a></li>
              <li><a href="https://github.com/abdelhadiLRS/JUBA_LISAN" target="_blank" rel="noopener noreferrer" className="text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] transition-colors">{t('github')}</a></li>
              <li className="pt-1"><ContactButton /></li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-sm text-[var(--juba-app-ink)] uppercase tracking-wider mb-4">
              {t('footerLegal')}
            </h4>
            <ul className="space-y-2.5 text-sm">
              <li><Link href="/privacy?from=landing" className="text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] transition-colors">{t('privacy')}</Link></li>
              <li><Link href="/terms?from=landing" className="text-[var(--juba-app-muted)] hover:text-[var(--juba-app-ink)] transition-colors">{t('terms')}</Link></li>
            </ul>
          </div>
        </div>

        <div className="juba-footer-bottom border-t pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
          <span>{t('builtForLearners')}</span>
          <span>{t('footerPositioning')}</span>
        </div>
      </div>
    </footer>
  )
}
