'use client'

import Link from 'next/link'
import { ArrowRight, BookOpen, CheckCircle2, Headphones, LockKeyhole, Mic2, Sparkles } from 'lucide-react'

const levels = [
  { id: 'a1', title: 'A1 · Starter', desc: 'Build your first practical vocabulary and everyday phrases.', progress: 0, lessons: 24, unlocked: true, current: true },
  { id: 'a2', title: 'A2 · Elementary', desc: 'Understand common situations and speak with more confidence.', progress: 0, lessons: 30, unlocked: true, current: false },
  { id: 'b1', title: 'B1 · Intermediate', desc: 'Express ideas, follow conversations, and read with independence.', progress: 0, lessons: 36, unlocked: true, current: false },
  { id: 'b2', title: 'B2 · Upper Intermediate', desc: 'Handle richer conversations and more precise language.', progress: 0, lessons: 40, unlocked: false, current: false },
  { id: 'c1', title: 'C1 · Advanced', desc: 'Develop fluent, nuanced communication for demanding contexts.', progress: 0, lessons: 44, unlocked: false, current: false },
]

const skills = [
  { icon: BookOpen, title: 'Learn', text: 'Build useful language in small, focused steps.' },
  { icon: Headphones, title: 'Listen', text: 'Train your ear with short real-world practice.' },
  { icon: Mic2, title: 'Speak', text: 'Turn recognition into confident active recall.' },
]

const places = [
  { icon: '☕', title: 'Café', text: 'Order, ask and respond.' },
  { icon: '🍽️', title: 'Restaurant', text: 'Food, requests and payment.' },
  { icon: '✈️', title: 'Travel', text: 'Tickets, directions and arrival.' },
  { icon: '💼', title: 'Work', text: 'Meetings and everyday tasks.' },
]

export default function CoursesPage() {
  return (
    <main className="min-h-screen px-4 py-8 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-6xl space-y-8">
        <section className="juba-card relative overflow-hidden p-7 sm:p-10">
          <div className="relative z-10 max-w-3xl">
            <div className="juba-eyebrow"><Sparkles className="h-4 w-4" /> Your learning world</div>
            <h1 className="mt-4 text-4xl font-black tracking-tight text-fl-fg sm:text-6xl">Learn language you can actually use.</h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-fl-muted-2 sm:text-lg">Move through practical situations, strengthen your memory, and unlock the next part of your journey one mission at a time.</p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Link href="/learning-journey" className="inline-flex items-center gap-2 rounded-xl bg-[var(--juba-text)] px-5 py-3 font-bold text-[var(--juba-surface)] transition hover:opacity-90">Continue journey <ArrowRight className="h-4 w-4" /></Link>
              <Link href="/assessment" className="inline-flex items-center gap-2 rounded-xl border border-fl-border bg-fl-surface px-5 py-3 font-bold text-fl-fg transition hover:bg-fl-surface-2">Find my level</Link>
            </div>
          </div>
          <div className="juba-hero-glow" aria-hidden="true" />
        </section>

        <section className="grid gap-4 md:grid-cols-3">
          {skills.map(({ icon: Icon, title, text }) => (
            <div key={title} className="juba-card p-5">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[var(--juba-primary-soft)] text-[var(--juba-primary-dark)]"><Icon className="h-5 w-5" /></div>
              <h2 className="mt-4 text-xl font-black text-fl-fg">{title}</h2>
              <p className="mt-2 text-sm leading-6 text-fl-muted-2">{text}</p>
            </div>
          ))}
        </section>

        <section>
          <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
            <div><p className="juba-eyebrow">Your roadmap</p><h2 className="mt-2 text-3xl font-black text-fl-fg sm:text-4xl">One path. Five levels.</h2></div>
            <span className="rounded-full border border-fl-border bg-fl-surface-2 px-4 py-2 text-sm font-bold text-fl-muted">CEFR · {levels.length} levels</span>
          </div>
          <div className="grid gap-5 lg:grid-cols-2">
            {levels.map((level, index) => (
              <article key={level.id} className={`juba-card relative p-6 ${level.current ? 'ring-2 ring-[var(--juba-primary)]' : ''}`}>
                {level.current && <span className="absolute -top-3 right-5 rounded-full bg-[var(--juba-warm)] px-3 py-1 text-[11px] font-black uppercase tracking-[.14em] text-[var(--juba-text)]">Start here</span>}
                <div className="flex items-start justify-between gap-4">
                  <div><span className="text-xs font-bold uppercase tracking-[.16em] text-fl-muted-2">Level {index + 1}</span><h3 className="mt-2 text-2xl font-black text-fl-fg">{level.title}</h3></div>
                  <div className={`flex h-10 w-10 items-center justify-center rounded-full ${level.unlocked ? 'bg-[var(--juba-warm-soft)] text-[var(--juba-primary-dark)]' : 'bg-fl-surface-2 text-fl-muted-2'}`}>{level.unlocked ? <CheckCircle2 className="h-5 w-5" /> : <LockKeyhole className="h-5 w-5" />}</div>
                </div>
                <p className="mt-3 max-w-xl text-sm leading-6 text-fl-muted-2">{level.desc}</p>
                <div className="mt-6 flex items-center justify-between text-sm font-bold text-fl-fg"><span>{level.lessons} lessons</span><span>{level.progress}%</span></div>
                <div className="mt-2 h-2.5 overflow-hidden rounded-full bg-fl-surface-2"><div className="h-full rounded-full bg-[var(--juba-warm)]" style={{ width: `${level.progress}%` }} /></div>
                {level.unlocked ? <Link href="/plan" className="mt-6 inline-flex items-center gap-2 rounded-xl bg-[var(--juba-primary-soft)] px-5 py-3 font-bold text-[var(--juba-primary-dark)] transition hover:bg-[var(--juba-primary)]">Open learning plan <ArrowRight className="h-4 w-4" /></Link> : <span className="mt-6 inline-flex items-center gap-2 rounded-xl bg-fl-surface-2 px-5 py-3 font-bold text-fl-muted-2"><LockKeyhole className="h-4 w-4" /> Unlock later</span>}
              </article>
            ))}
          </div>
        </section>

        <section className="juba-card p-6 sm:p-7">
          <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="juba-eyebrow">Real-world missions</p><h2 className="mt-2 text-2xl font-black text-fl-fg">Practice language where it matters.</h2></div><Link href="/learning-journey" className="font-bold text-[var(--juba-primary-dark)] underline underline-offset-4">See my journey</Link></div>
          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {places.map((place) => <div key={place.title} className="rounded-2xl border border-fl-border bg-fl-surface-2 p-4"><span className="text-2xl" aria-hidden="true">{place.icon}</span><p className="mt-3 font-black text-fl-fg">{place.title}</p><p className="mt-1 text-sm text-fl-muted-2">{place.text}</p></div>)}
          </div>
        </section>

        <section className="juba-card p-6 sm:p-7">
          <div className="flex items-center gap-3"><Sparkles className="h-6 w-6 text-[var(--juba-primary-dark)]" /><h2 className="text-2xl font-black text-fl-fg">The JUBA rhythm</h2></div>
          <div className="mt-6 grid gap-3 sm:grid-cols-4">{['Learn', 'Practice', 'Recall', 'Review'].map((step, i) => <div key={step} className="rounded-2xl border border-fl-border bg-fl-surface-2 p-4"><span className="text-xs font-bold text-fl-muted-2">0{i + 1}</span><p className="mt-2 font-black text-fl-fg">{step}</p></div>)}</div>
        </section>
      </div>
    </main>
  )
}
