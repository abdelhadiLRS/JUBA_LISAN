'use client'

import Link from 'next/link'
import { ArrowRight, BookOpen, CheckCircle2, Headphones, LockKeyhole, MessageCircle, Sparkles } from 'lucide-react'

const levels = [
  { id: 'a1', title: 'A1 · Starter', desc: 'Build your first practical vocabulary and everyday phrases.', progress: 0, lessons: 24, unlocked: true },
  { id: 'a2', title: 'A2 · Elementary', desc: 'Understand common situations and speak with more confidence.', progress: 0, lessons: 30, unlocked: true },
  { id: 'b1', title: 'B1 · Intermediate', desc: 'Express ideas, follow conversations, and read with independence.', progress: 0, lessons: 36, unlocked: true },
  { id: 'b2', title: 'B2 · Upper Intermediate', desc: 'Handle richer conversations and more precise language.', progress: 0, lessons: 40, unlocked: false },
  { id: 'c1', title: 'C1 · Advanced', desc: 'Develop fluent, nuanced communication for demanding contexts.', progress: 0, lessons: 44, unlocked: false },
]

const skills = [
  { icon: BookOpen, title: 'Vocabulary', text: 'Learn useful words in context.' },
  { icon: MessageCircle, title: 'Speaking', text: 'Turn recognition into active recall.' },
  { icon: Headphones, title: 'Listening', text: 'Train your ear with short, focused practice.' },
]

export default function CoursesPage() {
  return (
    <main className="min-h-screen px-5 py-10 sm:px-8 lg:px-12">
      <div className="mx-auto max-w-6xl">
        <section className="overflow-hidden rounded-[36px] border-2 border-neutral-950 bg-[#d8f53f] p-7 shadow-[10px_10px_0_rgba(17,17,17,.9)] sm:p-10">
          <div className="max-w-3xl">
            <p className="text-xs font-black uppercase tracking-[.22em]">JUBA LISAN · COURSES</p>
            <h1 className="mt-3 text-4xl font-black tracking-tight sm:text-6xl">Choose your path. Learn a little every day.</h1>
            <p className="mt-5 max-w-2xl text-base font-semibold leading-7 sm:text-lg">A clear CEFR journey built around short lessons, active recall, listening and real communication.</p>
            <Link href="/learning-journey" className="mt-7 inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-white px-5 py-3 font-black shadow-[4px_4px_0_rgba(17,17,17,.9)]">Continue my journey <ArrowRight className="h-4 w-4" /></Link>
          </div>
        </section>

        <section className="mt-12 grid gap-5 md:grid-cols-3">
          {skills.map(({ icon: Icon, title, text }) => (
            <div key={title} className="rounded-[28px] border-2 border-neutral-950 bg-white p-6 shadow-[6px_6px_0_rgba(17,17,17,.85)] dark:bg-neutral-900">
              <Icon className="h-7 w-7" />
              <h2 className="mt-5 text-xl font-black">{title}</h2>
              <p className="mt-2 font-medium text-neutral-600 dark:text-neutral-300">{text}</p>
            </div>
          ))}
        </section>

        <section className="mt-14">
          <div className="mb-6 flex items-end justify-between gap-4"><div><p className="text-xs font-black uppercase tracking-[.2em] text-neutral-500">CEFR ROADMAP</p><h2 className="mt-2 text-3xl font-black">Your language levels</h2></div><span className="rounded-full border-2 border-neutral-950 px-4 py-2 text-sm font-black">{levels.length} levels</span></div>
          <div className="grid gap-5 lg:grid-cols-2">
            {levels.map((level, index) => (
              <article key={level.id} className={`rounded-[30px] border-2 border-neutral-950 p-6 shadow-[6px_6px_0_rgba(17,17,17,.85)] ${level.unlocked ? 'bg-white dark:bg-neutral-900' : 'bg-neutral-100 dark:bg-neutral-800'}`}>
                <div className="flex items-start justify-between gap-4"><div><span className="text-xs font-black uppercase tracking-[.16em] text-neutral-500">Level {index + 1}</span><h3 className="mt-2 text-2xl font-black">{level.title}</h3></div>{level.unlocked ? <CheckCircle2 className="h-6 w-6" /> : <LockKeyhole className="h-6 w-6" />}</div>
                <p className="mt-3 max-w-xl font-medium text-neutral-600 dark:text-neutral-300">{level.desc}</p>
                <div className="mt-6 flex items-center justify-between text-sm font-black"><span>{level.lessons} lessons</span><span>{level.progress}% complete</span></div>
                <div className="mt-2 h-3 overflow-hidden rounded-full border-2 border-neutral-950 bg-white"><div className="h-full rounded-full bg-[#d8f53f]" style={{ width: `${level.progress}%` }} /></div>
                {level.unlocked ? <Link href={`/lesson/${level.id}-01`} className="mt-6 inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-[#d8f53f] px-5 py-3 font-black">Start level <ArrowRight className="h-4 w-4" /></Link> : <span className="mt-6 inline-flex items-center gap-2 rounded-full border-2 border-neutral-300 px-5 py-3 font-black text-neutral-400"><LockKeyhole className="h-4 w-4" /> Unlock later</span>}
              </article>
            ))}
          </div>
        </section>

        <section className="mt-14 rounded-[30px] border-2 border-neutral-950 bg-white p-7 shadow-[6px_6px_0_rgba(17,17,17,.85)] dark:bg-neutral-900"><div className="flex items-center gap-3"><Sparkles className="h-6 w-6" /><h2 className="text-2xl font-black">Learn with a simple rhythm</h2></div><div className="mt-6 grid gap-4 sm:grid-cols-4">{['Learn', 'Practice', 'Recall', 'Review'].map((step, i) => <div key={step} className="rounded-2xl border-2 border-neutral-950 p-4"><span className="text-xs font-black text-neutral-500">0{i + 1}</span><p className="mt-2 font-black">{step}</p></div>)}</div></section>
      </div>
    </main>
  )
}
