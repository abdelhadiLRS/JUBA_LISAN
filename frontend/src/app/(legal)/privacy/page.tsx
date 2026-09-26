'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { useSearchParams } from 'next/navigation'

export default function PrivacyPage() {
  const t = useTranslations('legal.privacy')
  const tCommon = useTranslations('common')
  const searchParams = useSearchParams()
  const from = searchParams.get('from')
  const isFromSettings = from === 'settings'
  const isFromRegister = from === 'register'
  const isFromLanding = from === 'landing'
  const backHref = isFromSettings
    ? '/settings'
    : isFromRegister
      ? '/register'
      : isFromLanding
        ? '/'
        : '/'
  const backLabel = isFromSettings
    ? t('linkBackSettings')
    : isFromRegister
      ? t('linkBack')
      : tCommon('back')
  const termsHref = isFromSettings
    ? '/terms?from=settings'
    : isFromRegister
      ? '/terms?from=register'
      : isFromLanding
        ? '/terms?from=landing'
        : '/terms'
  const s2Items = [
    t('s2i1'),
    t('s2i2'),
    t('s2i3'),
    t('s2i4'),
    t('s2i5'),
    t('s2i6'),
    t('s2i7'),
    t('s2i8'),
    t('s2i9'),
    t('s2i10'),
  ]
  const s3Items = [
    t('s3i1'),
    t('s3i2'),
    t('s3i3'),
    t('s3i4'),
    t('s3i5'),
    t('s3i6'),
  ]

  return (
    <div>
      <div className="mb-10 flex flex-col items-center">
        <Link href="/">
          <Image
            src="/logo.png"
            alt="JUBA LISAN"
            width={48}
            height={48}
            className="mb-3"
          />
        </Link>
        <h1 className="text-[#202127] font-sans text-xl font-bold tracking-wide">JUBA LISAN</h1>
        <p className="text-black/50 text-black/50 mt-1 font-semibold tracking-wide">
          {tCommon('tagline')}
        </p>
      </div>

      <div className="space-y-8 rounded-[26px] border border-black/[0.08] bg-white p-6 shadow-[0_12px_30px_rgba(43,45,90,.055)] sm:p-8">
        <div className="border-black/[0.08] flex items-center gap-2 border-b border-black/[0.08] pb-4">
          <span className="text-[#202127] text-black/50"><span className="h-2 w-2 rounded-full bg-[#5862e2]" /></span>/span>
          <span className="text-black/50 font-sans text-xs tracking-wide">
            {t('pageTitle')}
          </span>
        </div>

        <p className="text-black/50 text-black/50 font-sans tracking-wide">
          {t('updated')}
        </p>

        <section className="space-y-3">
          <h2 className="text-[#202127] font-sans text-sm font-bold tracking-wide">
            {t('s1Title')}
          </h2>
          <p className="text-[#202127] font-sans text-sm leading-relaxed">
            {t('s1Body')}
          </p>
        </section>

        <section className="space-y-3">
          <h2 className="text-[#202127] font-sans text-sm font-bold tracking-wide">
            {t('s2Title')}
          </h2>
          <p className="text-[#202127] font-sans text-sm leading-relaxed">
            {t('s2Intro')}
          </p>
          <ul className="space-y-1 pl-4">
            {s2Items.map((item) => (
              <li
                key={item}
                className="text-[#202127] flex gap-2 font-sans text-sm leading-relaxed"
              >
                <span className="text-black/50 flex-shrink-0">—</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </section>

        <section className="space-y-3">
          <h2 className="text-[#202127] font-sans text-sm font-bold tracking-wide">
            {t('s3Title')}
          </h2>
          <p className="text-[#202127] font-sans text-sm leading-relaxed">
            {t('s3Intro')}
          </p>
          <ul className="space-y-1 pl-4">
            {s3Items.map((item) => (
              <li
                key={item}
                className="text-[#202127] flex gap-2 font-sans text-sm leading-relaxed"
              >
                <span className="text-black/50 flex-shrink-0">—</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
          <p className="text-[#202127] font-sans text-sm leading-relaxed">
            {t('s3Footer')}
          </p>
        </section>

        {[
          { title: t('s4Title'), body: t('s4Body') },
          { title: t('s5Title'), body: t('s5Body') },
          { title: t('s6Title'), body: t('s6Body') },
          { title: t('s7Title'), body: t('s7Body') },
          { title: t('s8Title'), body: t('s8Body') },
          { title: t('s9Title'), body: t('s9Body') },
        ].map((section) => (
          <section key={section.title} className="space-y-3">
            <h2 className="text-[#202127] font-sans text-sm font-bold tracking-wide">
              {section.title}
            </h2>
            <p className="text-[#202127] font-sans text-sm leading-relaxed">
              {section.body}
            </p>
          </section>
        ))}

        <div className="border-black/[0.08] flex gap-6 border-t border-black/[0.08] pt-4">
          <Link
            href={termsHref}
            className="text-black/50 hover:text-[#202127] font-sans text-xs tracking-wide transition-colors"
          >
            {t('linkTerms')}
          </Link>
          <Link
            href={backHref}
            className="text-black/50 hover:text-[#202127] font-sans text-xs tracking-wide transition-colors"
          >
            {backLabel}
          </Link>
        </div>
      </div>
    </div>
  )
}
