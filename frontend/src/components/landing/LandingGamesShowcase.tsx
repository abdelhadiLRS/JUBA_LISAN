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
    <section dir={dir} id="games" className="juba-games-showcase juba-jl-games">
      <style>{".juba-jl-games{background:#f7fff3;color:#242424;font-family:'Nunito Sans','Noto Sans Arabic',system-ui,sans-serif;padding-top:84px}.juba-jl-games .juba-games-heading{text-align:center;max-width:760px;margin:0 auto 28px}.juba-jl-games .juba-ref-kicker{color:#46a302;font-weight:900}.juba-jl-games .juba-games-heading h2{color:#242424;font-weight:950;letter-spacing:-.06em;font-size:clamp(2.2rem,5vw,4.3rem);line-height:.98}.juba-jl-games .juba-games-heading p{color:#777;line-height:1.7}.juba-jl-games .juba-games-tabs{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-bottom:18px}.juba-jl-games .juba-games-tab{min-height:42px;padding:8px 14px;border:2px solid #e5e5e5;border-radius:12px;background:#fff;color:#777;font-weight:900;box-shadow:0 2px 0 rgba(0,0,0,.04)}.juba-jl-games .juba-games-tab:hover{border-color:#58cc02;background:#efffe6;color:#46a302}.juba-jl-games .juba-games-tab.is-active{border-color:#46a302;background:#58cc02;color:#fff;box-shadow:0 3px 0 #46a302}.juba-jl-games .juba-game-stage{max-width:980px;margin:0 auto;border:2px solid #e5e5e5;border-radius:24px;background:#fff;box-shadow:0 5px 0 rgba(0,0,0,.07);display:grid;grid-template-columns:1.15fr .85fr;gap:24px;padding:24px;align-items:center}.juba-jl-games .juba-game-stage-image{min-height:280px;display:grid;place-items:center;border-radius:18px;background:#efffe6;border:2px solid #d9f7c5;padding:18px}.juba-jl-games .juba-game-stage-image img{max-width:100%;height:auto}.juba-jl-games .juba-game-stage-copy{padding:8px}.juba-jl-games .juba-game-stage-index{color:#46a302;font-weight:900;font-size:12px}.juba-jl-games .juba-game-stage-copy h3{margin:10px 0 8px;color:#242424;font-size:clamp(1.8rem,4vw,3rem);font-weight:950;letter-spacing:-.05em}.juba-jl-games .juba-game-stage-copy p{color:#777;line-height:1.6;margin-bottom:18px}.juba-jl-games .juba-ref-button{display:inline-flex;align-items:center;gap:7px;min-height:46px;padding:10px 16px;border:2px solid #46a302;border-radius:14px;background:#58cc02;color:#fff;font-weight:900;box-shadow:0 4px 0 #46a302;text-decoration:none}.juba-jl-games .juba-practical-language-section{margin-top:70px;padding-top:70px;border-top:2px solid #dcebd5}.juba-jl-games .juba-practical-language-copy{text-align:center;max-width:760px;margin:0 auto 34px}.juba-jl-games .juba-practical-language-copy h2{color:#242424;font-weight:950;letter-spacing:-.055em}.juba-jl-games .juba-practical-language-copy p{color:#777;line-height:1.7}.juba-jl-games .juba-practical-language-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.juba-jl-games .juba-practical-language-card{border:2px solid #e5e5e5!important;border-radius:16px!important;background:#fff!important;box-shadow:0 3px 0 rgba(0,0,0,.05)!important}.juba-jl-games .juba-practical-language-card:hover{border-color:#58cc02!important;background:#efffe6!important}@media(max-width:900px){.juba-jl-games .juba-game-stage{grid-template-columns:1fr}.juba-jl-games .juba-practical-language-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.juba-jl-games{padding-top:58px}.juba-jl-games .juba-game-stage{padding:14px;border-radius:18px}.juba-jl-games .juba-game-stage-image{min-height:210px}.juba-jl-games .juba-practical-language-grid{grid-template-columns:1fr}}"}</style>
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