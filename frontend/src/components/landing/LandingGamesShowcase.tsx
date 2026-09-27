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
  practicalEyebrow: string
  practicalTitle: string
  practicalDescription: string
  practicalCta: string
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
  practicalEyebrow,
  practicalTitle,
  practicalDescription,
  practicalCta,
}: LandingGamesShowcaseProps) {
  const [active, setActive] = useState<(typeof GAMES)[number]['key']>('matching')

  const labels = {
    matching: matchingLabel,
    memory: memoryLabel,
    ordering: orderingLabel,
    'sentence-builder': sentenceBuilderLabel,
  }

  const activeGame = GAMES.find((game) => game.key === active) ?? GAMES[0]

  const moveGame = (direction: 1 | -1) => {
    const currentIndex = GAMES.findIndex((game) => game.key === active)
    const nextIndex = (currentIndex + direction + GAMES.length) % GAMES.length
    setActive(GAMES[nextIndex].key)
    requestAnimationFrame(() => {
      document.getElementById('juba-game-tab-' + GAMES[nextIndex].key)?.focus()
    })
  }

  return (
    <section dir={dir} id="games" className="juba-games-showcase">
      <div className="juba-games-heading">
        <span className="juba-ref-kicker"><Gamepad2 className="h-4 w-4" /> {eyebrow}</span>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
      <div className="juba-games-tabs" role="tablist" aria-orientation="horizontal" aria-label={title}>
        {GAMES.map((game) => (
          <button
            key={game.key}
            id={`juba-game-tab-${game.key}`}
            type="button"
            role="tab"
            aria-selected={active === game.key}
            aria-controls="juba-game-panel"
            tabIndex={active === game.key ? 0 : -1}
            onClick={() => setActive(game.key)}
            onKeyDown={(event) => {
              if (event.key === (dir === 'rtl' ? 'ArrowLeft' : 'ArrowRight')) {
                event.preventDefault()
                moveGame(1)
              } else if (event.key === (dir === 'rtl' ? 'ArrowRight' : 'ArrowLeft')) {
                event.preventDefault()
                moveGame(-1)
              } else if (event.key === 'Home') {
                event.preventDefault()
                setActive(GAMES[0].key)
                document.getElementById('juba-game-tab-' + GAMES[0].key)?.focus()
              } else if (event.key === 'End') {
                event.preventDefault()
                setActive(GAMES[GAMES.length - 1].key)
                document.getElementById('juba-game-tab-' + GAMES[GAMES.length - 1].key)?.focus()
              }
            }}
            className={active === game.key ? 'juba-games-tab is-active' : 'juba-games-tab'}
          >
            {labels[game.key]}
          </button>
        ))}
      </div>
      <div
        id="juba-game-panel"
        className="juba-game-stage"
        role="tabpanel"
        tabIndex={0}
        aria-live="polite"
        aria-labelledby={`juba-game-tab-${activeGame.key}`}
      >
        <div className="juba-game-stage-image">
          <Image src={activeGame.src} alt={labels[activeGame.key]} width={420} height={260} priority={active === 'matching'} />
        </div>
        <div className="juba-game-stage-copy">
          <span className="juba-game-stage-index">{GAMES.findIndex((game) => game.key === activeGame.key) + 1} / {GAMES.length}</span>
          <h3>{labels[activeGame.key]}</h3>
          <p>{openLabel}</p>
          <Link href={activeGame.href} className="juba-ref-button">
            {openLabel} <ArrowUpRight className={dir === 'rtl' ? 'rotate-180' : undefined} aria-hidden="true" />
          </Link>
        </div>
      </div>

      <section className="juba-practical-language-section" aria-labelledby="juba-practical-title">
        <div className="juba-practical-language-copy">
          <span className="juba-ref-kicker">{practicalEyebrow}</span>
          <h2 id="juba-practical-title">{practicalTitle}</h2>
          <p>{practicalDescription}</p>
          <Link href="/register" className="juba-ref-button">{practicalCta}</Link>
        </div>
        <div className="juba-practical-language-grid" role="group" aria-label={practicalTitle}>
          {[
            ['🇬🇧','English','الإنجليزية'],['🇪🇸','Español','الإسبانية'],['🇫🇷','Français','الفرنسية'],['🇩🇪','Deutsch','الألمانية'],
            ['🇮🇹','Italiano','الإيطالية'],['🇵🇹','Português','البرتغالية'],['🇯🇵','日本語','اليابانية'],['🇰🇷','한국어','الكورية'],
            ['🇩🇿','العربية','العربية'],['🇷🇺','Русский','الروسية'],['🇹🇷','Türkçe','التركية'],['🇨🇳','中文','الصينية'],
            ['🇳🇱','Nederlands','الهولندية'],['🇵🇱','Polski','البولندية'],
          ].map(([flag,name,arName]) => (
            <Link key={name} href="/register" aria-label={`${practicalCta}: ${dir === 'rtl' ? arName : name}`} className="juba-practical-language-card">
              <span className="juba-practical-language-flag" aria-hidden="true">{flag}</span>
              <span><strong>{dir === 'rtl' ? arName : name}</strong><small>{dir === 'rtl' ? name : 'JUBA LISAN'}</small></span>
            </Link>
          ))}
        </div>
      </section>
    </section>
  )
}