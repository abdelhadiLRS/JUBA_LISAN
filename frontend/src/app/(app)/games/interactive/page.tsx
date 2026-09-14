'use client'

import Link from 'next/link'
import { useState } from 'react'
import '../games.css'
import '../../../../components/games/interactive-games.css'

type Lang = 'ar' | 'fr' | 'en'

const copy = {
  ar: {
    title: 'الألعاب التفاعلية',
    subtitle: 'تدريبات عملية للذاكرة والمطابقة والترتيب.',
    memory: 'لعبة الذاكرة', memoryDesc: 'طابق البطاقات وأكمل جميع الأزواج.',
    matching: 'لعبة المطابقة', matchingDesc: 'اربط كل كلمة بترجمتها الصحيحة.',
    ordering: 'لعبة الترتيب', orderingDesc: 'رتّب العناصر في التسلسل الصحيح.',
    start: 'ابدأ', back: 'العودة إلى مركز الألعاب', language: 'اللغة',
  },
  fr: {
    title: 'Jeux interactifs',
    subtitle: 'Des activités pratiques de mémoire, association et classement.',
    memory: 'Jeu de mémoire', memoryDesc: 'Associe les cartes et complète toutes les paires.',
    matching: 'Jeu d’association', matchingDesc: 'Relie chaque mot à sa bonne traduction.',
    ordering: 'Jeu de classement', orderingDesc: 'Place les éléments dans le bon ordre.',
    start: 'Commencer', back: 'Retour aux jeux', language: 'Langue',
  },
  en: {
    title: 'Interactive games',
    subtitle: 'Hands-on practice for memory, matching, and ordering.',
    memory: 'Memory game', memoryDesc: 'Match the cards and complete every pair.',
    matching: 'Matching game', matchingDesc: 'Connect each word to its correct translation.',
    ordering: 'Ordering game', orderingDesc: 'Place the items in the correct sequence.',
    start: 'Start', back: 'Back to games', language: 'Language',
  },
} as const

export default function InteractiveGamesPage() {
  const [lang, setLang] = useState<Lang>('ar')
  const t = copy[lang]
  const cards = [
    { href: '/games/memory', title: t.memory, desc: t.memoryDesc, icon: '🧠' },
    { href: '/games/matching', title: t.matching, desc: t.matchingDesc, icon: '🔗' },
    { href: '/games/ordering', title: t.ordering, desc: t.orderingDesc, icon: '🔢' },
  ]

  return (
    <main className="juba-games" dir={lang === 'ar' ? 'rtl' : 'ltr'}>
      <section className="games-shell">
        <header className="games-header">
          <div>
            <div className="games-brand">JUBA EDU</div>
            <h1>{t.title}</h1>
            <p>{t.subtitle}</p>
          </div>
          <div className="language-control">
            <span>{t.language}</span>
            {(['ar', 'fr', 'en'] as Lang[]).map((value) => (
              <button key={value} className={lang === value ? 'active' : ''} onClick={() => setLang(value)}>
                {value.toUpperCase()}
              </button>
            ))}
          </div>
        </header>

        <section className="game-grid" aria-label={t.title}>
          {cards.map((card) => (
            <Link key={card.href} href={`${card.href}?lang=${lang}`} className="game-card">
              <span className="game-icon">{card.icon}</span>
              <span className="game-title">{card.title}</span>
              <span className="game-desc">{card.desc}</span>
              <span className="start">{t.start} →</span>
            </Link>
          ))}
        </section>

        <Link className="interactive-secondary" href="/games">← {t.back}</Link>
      </section>
    </main>
  )
}
