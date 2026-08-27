'use client'

import {
  BrainCircuit,
  CalendarCheck2,
  FileUp,
  Flame,
  Gauge,
  Lightbulb,
  RefreshCw,
  Sparkles,
  Target,
} from 'lucide-react'

const features = [
  {
    icon: BrainCircuit,
    title: 'Adaptive AI Coach',
    text: 'JUBA learns from your level, goals, mistakes and recent activity to shape what you should practice next.',
  },
  {
    icon: RefreshCw,
    title: 'Smart Review',
    text: 'Words and concepts return when they are most useful, powered by spaced repetition instead of random revision.',
  },
  {
    icon: FileUp,
    title: 'Learn From Anything',
    text: 'Turn notes, articles, images or imported content into a focused learning path with vocabulary, practice and quizzes.',
  },
  {
    icon: CalendarCheck2,
    title: 'Daily Missions',
    text: 'A small, personalized mission keeps momentum high without overwhelming the learner.',
  },
]

export function IntelligentLearningEngine() {
  return (
    <section className="relative overflow-hidden border-y border-neutral-200/70 bg-white py-20 dark:border-neutral-800/70 dark:bg-neutral-950 sm:py-24">
      <div className="absolute left-1/2 top-0 h-72 w-[44rem] -translate-x-1/2 rounded-full bg-amber-400/10 blur-3xl" />
      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid items-center gap-12 lg:grid-cols-12 lg:gap-16">
          <div className="lg:col-span-5">
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-amber-500/20 bg-amber-500/10 px-3.5 py-1.5 text-xs font-bold uppercase tracking-wider text-amber-700 dark:text-amber-300">
              <Sparkles className="h-3.5 w-3.5" />
              Your learning engine
            </div>
            <h2 className="text-3xl font-black tracking-tight text-neutral-950 dark:text-white sm:text-5xl">
              One learner. One evolving path.
            </h2>
            <p className="mt-5 max-w-xl text-base leading-8 text-neutral-600 dark:text-neutral-400 sm:text-lg">
              JUBA LISAN continuously turns your activity into the next best learning action. The platform adapts instead of forcing everyone through the same course.
            </p>

            <div className="mt-8 grid grid-cols-2 gap-3">
              <div className="rounded-2xl border border-neutral-200 bg-neutral-50 p-4 dark:border-neutral-800 dark:bg-neutral-900">
                <Gauge className="mb-3 h-5 w-5 text-amber-500" />
                <p className="text-xl font-black text-neutral-950 dark:text-white">B1 → B2</p>
                <p className="mt-1 text-xs text-neutral-500">Target progression</p>
              </div>
              <div className="rounded-2xl border border-neutral-200 bg-neutral-50 p-4 dark:border-neutral-800 dark:bg-neutral-900">
                <Flame className="mb-3 h-5 w-5 text-orange-500" />
                <p className="text-xl font-black text-neutral-950 dark:text-white">14 days</p>
                <p className="mt-1 text-xs text-neutral-500">Current streak</p>
              </div>
            </div>
          </div>

          <div className="lg:col-span-7">
            <div className="rounded-[28px] border border-neutral-200 bg-neutral-50/80 p-3 shadow-2xl shadow-neutral-900/5 dark:border-neutral-800 dark:bg-neutral-900/70">
              <div className="rounded-[22px] border border-neutral-200 bg-white p-5 dark:border-neutral-800 dark:bg-neutral-950 sm:p-7">
                <div className="flex items-center justify-between gap-4 border-b border-neutral-100 pb-5 dark:border-neutral-800">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-neutral-400">JUBA AI Coach</p>
                    <h3 className="mt-1 text-lg font-black text-neutral-950 dark:text-white">Your next best actions</h3>
                  </div>
                  <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-amber-500/10 text-amber-600 dark:text-amber-300">
                    <BrainCircuit className="h-5 w-5" />
                  </div>
                </div>

                <div className="mt-5 space-y-3">
                  {features.map(({ icon: Icon, title, text }, index) => (
                    <div key={title} className="group flex gap-4 rounded-2xl border border-neutral-200 bg-neutral-50 p-4 transition-all hover:-translate-y-0.5 hover:bg-white hover:shadow-lg dark:border-neutral-800 dark:bg-neutral-900 dark:hover:bg-neutral-800">
                      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-amber-600 shadow-sm dark:bg-neutral-950 dark:text-amber-300">
                        <Icon className="h-5 w-5" />
                      </div>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2">
                          <h4 className="text-sm font-extrabold text-neutral-950 dark:text-white">{title}</h4>
                          {index === 0 && <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-bold text-emerald-600">Recommended</span>}
                        </div>
                        <p className="mt-1 text-xs leading-6 text-neutral-500 dark:text-neutral-400">{text}</p>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-5 flex items-center gap-3 rounded-2xl bg-neutral-950 p-4 text-white dark:bg-white dark:text-neutral-950">
                  <Target className="h-5 w-5 shrink-0 text-amber-400 dark:text-amber-600" />
                  <div>
                    <p className="text-sm font-bold">Today: 12-minute listening + 10 smart reviews</p>
                    <p className="mt-1 text-[11px] opacity-60">Selected from your recent performance.</p>
                  </div>
                  <Lightbulb className="ml-auto h-5 w-5 shrink-0 text-amber-400 dark:text-amber-600" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
