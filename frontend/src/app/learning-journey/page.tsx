import Link from 'next/link'
import { ArrowRight, BookOpen, Brain, Check, Flame, Headphones, Mic, Sparkles, Trophy, Zap } from 'lucide-react'

const steps = [
  { n: '01', title: 'Choose your goal', text: 'Start with a clear reason to learn and a level that matches you.', icon: Trophy },
  { n: '02', title: 'Learn in small steps', text: 'Build vocabulary, grammar, listening and speaking through focused lessons.', icon: BookOpen },
  { n: '03', title: 'Practice actively', text: 'Speak, listen and use new words instead of only reading them.', icon: Mic },
  { n: '04', title: 'Review before you forget', text: 'Smart Review brings difficult words back at the right moment.', icon: Brain },
]

const habits = [
  ['10 min', 'Daily minimum'],
  ['5', 'Words to review'],
  ['1', 'Speaking practice'],
]

export default function LearningJourneyPage() {
  return (
    <main className="min-h-screen overflow-hidden bg-[#f7f3ea] text-neutral-950">
      <section className="relative border-b-2 border-neutral-950 bg-[#d8f53f]">
        <div className="mx-auto max-w-6xl px-5 pb-16 pt-8 sm:px-8 lg:pb-24 lg:pt-12">
          <nav className="mb-16 flex items-center justify-between">
            <Link href="/" className="text-xl font-black tracking-tight">JUBA LISAN</Link>
            <Link href="/dashboard" className="rounded-full border-2 border-neutral-950 bg-white px-5 py-2.5 text-sm font-black shadow-[3px_3px_0_#111]">My learning</Link>
          </nav>
          <div className="max-w-4xl">
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-white px-4 py-2 text-xs font-black uppercase tracking-[.16em] shadow-[3px_3px_0_#111]">
              <Sparkles className="h-4 w-4" /> Your learning journey
            </div>
            <h1 className="text-5xl font-black leading-[.95] tracking-[-.05em] sm:text-7xl lg:text-8xl">Learn a little.<br />Remember a lot.</h1>
            <p className="mt-7 max-w-2xl text-lg font-semibold leading-relaxed sm:text-xl">JUBA LISAN turns daily practice into a simple loop: learn, use, review, remember. Your progress grows one useful step at a time.</p>
            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Link href="/courses" className="inline-flex items-center justify-center gap-2 rounded-full border-2 border-neutral-950 bg-neutral-950 px-7 py-4 font-black text-white shadow-[5px_5px_0_#fff]">Start a lesson <ArrowRight className="h-5 w-5" /></Link>
              <Link href="/review" className="inline-flex items-center justify-center gap-2 rounded-full border-2 border-neutral-950 bg-white px-7 py-4 font-black shadow-[4px_4px_0_#111]">Review vocabulary <Brain className="h-5 w-5" /></Link>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-5 py-16 sm:px-8 lg:py-24">
        <div className="mb-10 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div><p className="text-xs font-black uppercase tracking-[.2em] text-neutral-500">The loop</p><h2 className="mt-2 text-4xl font-black tracking-tight sm:text-5xl">Four steps. One habit.</h2></div>
          <div className="flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-white px-4 py-2 text-sm font-black"><Flame className="h-4 w-4" /> Consistency beats intensity</div>
        </div>
        <div className="grid gap-5 md:grid-cols-2">
          {steps.map(({ n, title, text, icon: Icon }) => (
            <article key={n} className="rounded-[28px] border-2 border-neutral-950 bg-white p-7 shadow-[6px_6px_0_#111] transition-transform hover:-translate-y-1">
              <div className="flex items-start justify-between"><span className="text-sm font-black text-neutral-400">{n}</span><div className="rounded-2xl border-2 border-neutral-950 bg-[#d8f53f] p-3"><Icon className="h-5 w-5" /></div></div>
              <h3 className="mt-10 text-2xl font-black">{title}</h3><p className="mt-2 max-w-md font-semibold leading-relaxed text-neutral-600">{text}</p>
              <div className="mt-6 flex items-center gap-2 text-xs font-black uppercase tracking-wider text-neutral-500"><Check className="h-4 w-4" /> Progress saved</div>
            </article>
          ))}
        </div>
      </section>

      <section className="border-y-2 border-neutral-950 bg-white">
        <div className="mx-auto max-w-6xl px-5 py-16 sm:px-8 lg:py-20">
          <div className="grid gap-10 lg:grid-cols-[1fr_1.1fr] lg:items-center">
            <div><p className="text-xs font-black uppercase tracking-[.2em] text-neutral-500">Today</p><h2 className="mt-3 text-4xl font-black tracking-tight sm:text-5xl">Make today count.</h2><p className="mt-4 max-w-lg font-semibold leading-relaxed text-neutral-600">A small, repeatable routine is easier to keep and powerful enough to compound into real fluency.</p></div>
            <div className="grid gap-3 sm:grid-cols-3">
              {habits.map(([value, label]) => <div key={label} className="rounded-3xl border-2 border-neutral-950 bg-[#f7f3ea] p-5"><Zap className="h-5 w-5" /><p className="mt-8 text-3xl font-black">{value}</p><p className="mt-1 text-xs font-black uppercase tracking-wider text-neutral-500">{label}</p></div>)}
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-5 py-16 sm:px-8 lg:py-24">
        <div className="rounded-[32px] border-2 border-neutral-950 bg-[#d8f53f] p-7 shadow-[8px_8px_0_#111] sm:p-10">
          <div className="flex flex-col gap-7 md:flex-row md:items-center md:justify-between"><div><p className="text-xs font-black uppercase tracking-[.2em]">Keep going</p><h2 className="mt-2 text-3xl font-black sm:text-4xl">Your next session is one click away.</h2></div><Link href="/dashboard" className="inline-flex shrink-0 items-center justify-center gap-2 rounded-full border-2 border-neutral-950 bg-white px-7 py-4 font-black shadow-[4px_4px_0_#111]">Continue learning <ArrowRight className="h-5 w-5" /></Link></div>
          <div className="mt-8 flex flex-wrap gap-3 text-sm font-black"><span className="inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-white px-4 py-2"><Headphones className="h-4 w-4" /> Listening</span><span className="inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-white px-4 py-2"><Mic className="h-4 w-4" /> Speaking</span><span className="inline-flex items-center gap-2 rounded-full border-2 border-neutral-950 bg-white px-4 py-2"><Brain className="h-4 w-4" /> Review</span></div>
        </div>
      </section>
    </main>
  )
}
