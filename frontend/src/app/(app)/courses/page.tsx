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
    <main className="min-h-screen px-5 py-8 sm:px-8 lg:px-12">
      <div className="mx-auto max-w-6xl">
        <section className="relative overflow-hidden rounded-[38px] border-2 border-neutral-950 bg-[#d8f53f] p-7 shadow-[10px_10px_0_rgba(17,17,17,.9)] sm:p-10">
          <div className="relative z-10 max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-white px-3 py-1.5 text-xs font-black uppercase tracking-[.16em]"><Sparkles className="h-4 w-4" /> Your learning world</div>
            <h1 className="mt-5 text-4xl font-black tracking-tight sm:text-6xl">Learn language you can actually use.</h1>
            <p className="mt-5 max-w-2xl text-base font-semibold leading-7 sm:text-lg">Move through practical situations, strengthen your memory, and unlock the next part of your journey one mission at a time.</p>
            <div className="mt-7 flex flex-wrap gap-3"><Link href="/learning-journey" className="inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-white px-5 py-3 font-black shadow-[4px_4px_0_rgba(17,17,17,.9)]">Continue journey <ArrowRight className="h-4 w-4" /></Link><Link href="/assessment" className="inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 px-5 py-3 font-black">Find my level</Link></div>
          </div>
          <div className="pointer-events-none absolute -bottom-16 -right-8 h-48 w-48 rounded-full border-2 border-neutral-950 bg-white/40" />
          <div className="pointer-events-none absolute -right-20 top-8 h-40 w-40 rounded-full border-2 border-neutral-950 bg-[#f29b54]/70" />
        </section>

        <section className="mt-8 grid gap-4 md:grid-cols-3">
          {skills.map(({ icon: Icon, title, text }) => <div key={title} className="rounded-[26px] border-2 border-neutral-950 bg-white p-5 shadow-[5px_5px_0_rgba(17,17,17,.8)] dark:bg-neutral-900"><div className="flex h-11 w-11 items-center justify-center rounded-2xl border-2 border-neutral-950 bg-[#d8f53f]"><Icon className="h-5 w-5" /></div><h2 className="mt-4 text-xl font-black">{title}</h2><p className="mt-2 font-medium text-neutral-600 dark:text-neutral-300">{text}</p></div>)}
        </section>

        <section className="mt-12">
          <div className="mb-7 flex flex-wrap items-end justify-between gap-4"><div><p className="text-xs font-black uppercase tracking-[.2em] text-neutral-500">Your roadmap</p><h2 className="mt-2 text-3xl font-black sm:text-4xl">One path. Five levels.</h2></div><span className="rounded-full border-2 border-neutral-950 bg-white px-4 py-2 text-sm font-black">CEFR · {levels.length} levels</span></div>
          <div className="relative grid gap-5 lg:grid-cols-2">
            <div className="pointer-events-none absolute bottom-10 left-1/2 top-10 hidden w-1 -translate-x-1/2 bg-neutral-950/15 lg:block" />
            {levels.map((level, index) => <article key={level.id} className={`relative rounded-[30px] border-2 border-neutral-950 p-6 shadow-[6px_6px_0_rgba(17,17,17,.85)] ${level.current ? 'bg-[#edf6bd]' : level.unlocked ? 'bg-white dark:bg-neutral-900' : 'bg-neutral-100 dark:bg-neutral-800'}`}>
              {level.current && <span className="absolute -top-3 right-5 rounded-full border-2 border-neutral-950 bg-[#d8f53f] px-3 py-1 text-[11px] font-black uppercase tracking-[.14em]">Start here</span>}
              <div className="flex items-start justify-between gap-4"><div><span className="text-xs font-black uppercase tracking-[.16em] text-neutral-500">Level {index + 1}</span><h3 className="mt-2 text-2xl font-black">{level.title}</h3></div><div className="flex h-10 w-10 items-center justify-center rounded-full border-2 border-neutral-950 bg-white">{level.unlocked ? <CheckCircle2 className="h-5 w-5" /> : <LockKeyhole className="h-5 w-5" />}</div></div>
              <p className="mt-3 max-w-xl font-medium text-neutral-600 dark:text-neutral-300">{level.desc}</p>
              <div className="mt-6 flex items-center justify-between text-sm font-black"><span>{level.lessons} lessons</span><span>{level.progress}%</span></div>
              <div className="mt-2 h-3 overflow-hidden rounded-full border-2 border-neutral-950 bg-white"><div className="h-full rounded-full bg-[#d8f53f]" style={{ width: `${level.progress}%` }} /></div>
              {level.unlocked ? <Link href="/plan" className="mt-6 inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-[#d8f53f] px-5 py-3 font-black">Open learning plan <ArrowRight className="h-4 w-4" /></Link> : <span className="mt-6 inline-flex items-center gap-2 rounded-full border-2 border-neutral-300 px-5 py-3 font-black text-neutral-400"><LockKeyhole className="h-4 w-4" /> Unlock later</span>}
            </article>)}
          </div>
        </section>

        <section className="mt-12 rounded-[30px] border-2 border-neutral-950 bg-white p-6 shadow-[6px_6px_0_rgba(17,17,17,.85)] dark:bg-neutral-900 sm:p-7"><div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-xs font-black uppercase tracking-[.2em] text-neutral-500">Real-world missions</p><h2 className="mt-2 text-2xl font-black">Practice language where it matters.</h2></div><Link href="/learning-journey" className="font-black underline underline-offset-4">See my journey</Link></div><div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">{places.map((place) => <div key={place.title} className="rounded-2xl border-2 border-neutral-950 bg-[#f7f4ea] p-4 dark:bg-neutral-800"><span className="text-2xl" aria-hidden="true">{place.icon}</span><p className="mt-3 font-black">{place.title}</p><p className="mt-1 text-sm font-medium text-neutral-600 dark:text-neutral-300">{place.text}</p></div>)}</div></section>

        <section className="mt-10 rounded-[30px] border-2 border-neutral-950 bg-white p-6 shadow-[6px_6px_0_rgba(17,17,17,.85)] dark:bg-neutral-900 sm:p-7"><div className="flex items-center gap-3"><Sparkles className="h-6 w-6" /><h2 className="text-2xl font-black">The JUBA rhythm</h2></div><div className="mt-6 grid gap-3 sm:grid-cols-4">{['Learn', 'Practice', 'Recall', 'Review'].map((step, i) => <div key={step} className="rounded-2xl border-2 border-neutral-950 p-4"><span className="text-xs font-black text-neutral-500">0{i + 1}</span><p className="mt-2 font-black">{step}</p></div>)}</div></section>
      </div>
    </main>
  )
}
