'use client'

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
  const labels = {
    matching: matchingLabel,
    memory: memoryLabel,
    ordering: orderingLabel,
    'sentence-builder': sentenceBuilderLabel,
  }

  return (
    <section dir={dir} id="games" className="juba-games-showcase">
      <div className="juba-games-heading">
        <span className="juba-ref-kicker"><Gamepad2 className="h-4 w-4" /> {eyebrow}</span>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
      <div className="juba-games-grid">
        {GAMES.map((game) => (
          <Link key={game.key} href={game.href} className="juba-game-card">
            <div className="juba-game-image-wrap">
              <Image src={game.src} alt={labels[game.key]} width={420} height={260} />
            </div>
            <div className="juba-game-card-copy">
              <strong>{labels[game.key]}</strong>
              <span>{openLabel}<ArrowUpRight aria-hidden="true" /></span>
            </div>
          </Link>
        ))}
      </div>
    </section>
  )
}
