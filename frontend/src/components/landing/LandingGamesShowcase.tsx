'use client'

import { useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { ArrowUpRight, Gamepad2 } from 'lucide-react'

interface LandingGamesShowcaseProps {
  dir?: 'ltr' | 'rtl'
  eyebrow: string
  title: string
  description: string
  matchingLabel: string
  memoryLabel: string
  orderingLabel: string
  sentenceBuilderLabel: string
  openLabel: string
}

const GAMES = [
  { key: 'matching', href: '/games/matching', src: '/landing/juba-game-matching.svg' },
  { key: 'memory', href: '/games/memory', src: '/landing/juba-game-memory.svg' },
  { key: 'ordering', href: '/games/ordering', src: '/landing/juba-game-ordering.svg' },
  { key: 'sentence-builder', href: '/games/sentence-builder', src: '/landing/juba-game-sentence-builder.svg' },
] as const

export function LandingGamesShowcase({
  dir = 'ltr',
  eyebrow,
  title,
  description,
  matchingLabel,
  memoryLabel,
  orderingLabel,
  sentenceBuilderLabel,
  openLabel,
}: LandingGamesShowcaseProps) {
  const [active, setActive] = useState<(typeof GAMES)[number]['key']>('matching')

  const labels = {
    matching: matchingLabel,
    memory: memoryLabel,
    ordering: orderingLabel,
    'sentence-builder': sentenceBuilderLabel,
  }

  const activeGame = GAMES.find((game) => game.key === active) ?? GAMES[0]

  return (
    <section dir={dir} id="games" className="juba-games-showcase">
      <div className="juba-games-heading">
        <span className="juba-ref-kicker"><Gamepad2 className="h-4 w-4" /> {eyebrow}</span>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
      <div className="juba-games-tabs" role="tablist" aria-label={title}>
        {GAMES.map((game) => (
          <button
            key={game.key}
            type="button"
            role="tab"
            aria-selected={active === game.key}
            onClick={() => setActive(game.key)}
            className={active === game.key ? 'juba-games-tab is-active' : 'juba-games-tab'}
          >
            {labels[game.key]}
          </button>
        ))}
      </div>
      <div className="juba-game-stage">
        <div className="juba-game-stage-image">
          <Image src={activeGame.src} alt={labels[activeGame.key]} width={420} height={260} priority={active === 'matching'} />
        </div>
        <div className="juba-game-stage-copy">
          <span className="juba-game-stage-index">{GAMES.findIndex((game) => game.key === activeGame.key) + 1} / {GAMES.length}</span>
          <h3>{labels[activeGame.key]}</h3>
          <p>{openLabel}</p>
          <Link href={activeGame.href} className="juba-ref-button">
            {openLabel} <ArrowUpRight aria-hidden="true" />
          </Link>
        </div>
      </div>

      <section className="juba-practical-language-section" aria-labelledby="juba-practical-title">
        <div className="juba-practical-language-copy">
          <span className="juba-ref-kicker">{dir === 'rtl' ? 'تعلّم للاستخدام الحقيقي' : 'Learn for real life'}</span>
          <h2 id="juba-practical-title">{dir === 'rtl' ? 'تعلّم اللغات للحياة والعمل' : 'Learn languages for life and work'}</h2>
          <p>{dir === 'rtl' ? 'دروس قصيرة ومحادثات واقعية ونطق واستماع ومفردات تساعدك على استخدام اللغة بثقة في الحياة اليومية والعمل.' : 'Short lessons, real conversations, pronunciation, listening and vocabulary built around situations you actually face.'}</p>
          <Link href="/register" className="juba-ref-button">{dir === 'rtl' ? 'تعلّم مجانًا' : 'Start learning for free'}</Link>
        </div>
        <div className="juba-practical-language-grid">
          {[
            ['🇬🇧','English','الإنجليزية'],['🇪🇸','Español','الإسبانية'],['🇫🇷','Français','الفرنسية'],['🇩🇪','Deutsch','الألمانية'],
            ['🇮🇹','Italiano','الإيطالية'],['🇵🇹','Português','البرتغالية'],['🇯🇵','日本語','اليابانية'],['🇰🇷','한국어','الكورية'],
            ['🇩🇿','العربية','العربية'],['🇷🇺','Русский','الروسية'],['🇹🇷','Türkçe','التركية'],['🇨🇳','中文','الصينية'],
            ['🇳🇱','Nederlands','الهولندية'],['🇵🇱','Polski','البولندية'],
          ].map(([flag,name,arName]) => (
            <Link key={name} href="/register" className="juba-practical-language-card">
              <span className="juba-practical-language-flag" aria-hidden="true">{flag}</span>
              <span><strong>{dir === 'rtl' ? arName : name}</strong><small>{dir === 'rtl' ? name : 'JUBA LISAN'}</small></span>
            </Link>
          ))}
        </div>
      </section>
    </section>
  )
}