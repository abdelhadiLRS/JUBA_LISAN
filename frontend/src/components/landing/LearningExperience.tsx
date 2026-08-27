'use client'

import {
  Globe,
  Target,
  Compass,
  MessageSquare,
  TrendingUp,
  ArrowRight,
  Sparkles,
  BrainCircuit,
  BriefcaseBusiness,
  Plane,
  Trophy,
  FileText,
  Mic,
  RotateCcw,
  BarChart3,
} from 'lucide-react'

interface LearningExperienceProps {
  t: (key: string) => string
}

export function LearningExperience({ t }: LearningExperienceProps) {
  const steps = [
    { num: '01', title: t('step1Title'), desc: t('step1Desc'), icon: Globe },
    { num: '02', title: t('step2Title'), desc: t('step2Desc'), icon: Target },
    { num: '03', title: t('step3Title'), desc: t('step3Desc'), icon: Compass },
    { num: '04', title: t('step4Title'), desc: t('step4Desc'), icon: MessageSquare },
    { num: '05', title: t('step5Title'), desc: t('step5Desc'), icon: TrendingUp },
  ]

  const scenarios = [
    { icon: Plane, label: 'Travel', desc: 'Airport, hotel & real-world conversations' },
    { icon: BriefcaseBusiness, label: 'Business', desc: 'Meetings, interviews & workplace English' },
    { icon: MessageSquare, label: 'Daily Life', desc: 'Natural conversations for everyday life' },
    { icon: Trophy, label: 'Exams', desc: 'Focused practice for CEFR & language exams' },
  ]

  const intelligence = [
    { icon: BrainCircuit, title: 'Adaptive AI Coach', desc: 'Your next activity changes with your progress, mistakes and goals.' },
    { icon: FileText, title: 'Learn From Anything', desc: 'Turn text, notes or imported content into lessons, vocabulary and quizzes.' },
    { icon: RotateCcw, title: 'Smart Review', desc: 'Bring back words and concepts at the right moment with spaced repetition.' },
    { icon: Trophy, title: 'Weekly Missions', desc: 'Small challenges create momentum without turning learning into a chore.' },
  ]

  const voiceScores = [
    { label: 'Pronunciation', value: 91 },
    { label: 'Grammar', value: 84 },
    { label: 'Vocabulary', value: 88 },
    { label: 'Fluency', value: 79 },
  ]

  return (
    <section className="relative overflow-hidden border-y border-neutral-200/60 bg-neutral-50/50 py-20 dark:border-neutral-800/60 dark:bg-neutral-900/40 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto mb-14 max-w-3xl text-center">
          <span className="mb-2 block text-xs font-bold uppercase tracking-widest text-amber-600 dark:text-amber-400">THE METHODOLOGY</span>
          <h2 className="text-3xl font-extrabold tracking-tight text-neutral-900 dark:text-white sm:text-4xl">{t('experienceTitle')}</h2>
          <p className="mt-4 text-base text-neutral-600 dark:text-neutral-400 sm:text-lg">{t('experienceSubtitle')}</p>
        </div>

        <div className="relative grid grid-cols-1 gap-6 md:grid-cols-5">
          {steps.map((step, idx) => {
            const Icon = step.icon
            return (
              <div key={step.num} className="juba-card group relative flex flex-col justify-between p-6">
                <div>
                  <div className="mb-6 flex items-center justify-between">
                    <span className="text-2xl font-extrabold text-amber-500/40 transition-colors group-hover:text-amber-500 dark:text-amber-400/30">{step.num}</span>
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400"><Icon className="h-5 w-5" /></div>
                  </div>
                  <h3 className="mb-2 text-base font-bold text-neutral-900 dark:text-white">{step.title}</h3>
                  <p className="text-xs leading-relaxed text-neutral-600 dark:text-neutral-400">{step.desc}</p>
                </div>
                {idx < steps.length - 1 && <div className="absolute -right-3 top-1/2 z-10 hidden -translate-y-1/2 text-neutral-300 dark:text-neutral-700 md:block"><ArrowRight className="h-5 w-5" /></div>}
              </div>
            )
          })}
        </div>

        <div className="mt-16 grid grid-cols-1 gap-6 lg:grid-cols-12">
          <div className="juba-card relative overflow-hidden bg-white p-7 dark:bg-neutral-950 sm:p-9 lg:col-span-7">
            <div className="absolute -right-20 -top-20 h-56 w-56 rounded-full bg-amber-400/10 blur-3xl" />
            <div className="relative">
              <div className="mb-4 flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-amber-600 dark:text-amber-400"><Sparkles className="h-4 w-4" />Real-world practice</div>
              <h3 className="text-2xl font-extrabold tracking-tight text-neutral-900 dark:text-white sm:text-3xl">Practice the language you actually need.</h3>
              <p className="mt-3 max-w-2xl text-sm leading-relaxed text-neutral-600 dark:text-neutral-400">Choose a situation, speak naturally with JUBA AI, receive instant feedback and repeat the scenario until it feels effortless.</p>

              <div className="mt-7 grid grid-cols-2 gap-3">
                {scenarios.map(({ icon: Icon, label, desc }) => (
                  <div key={label} className="rounded-2xl border border-neutral-200 bg-neutral-50/80 p-4 transition-transform hover:-translate-y-0.5 dark:border-neutral-800 dark:bg-neutral-900/70">
                    <Icon className="mb-3 h-5 w-5 text-amber-500" />
                    <p className="text-sm font-bold text-neutral-900 dark:text-white">{label}</p>
                    <p className="mt-1 text-[11px] leading-relaxed text-neutral-500 dark:text-neutral-400">{desc}</p>
                  </div>
                ))}
              </div>

              <div className="mt-5 rounded-2xl border border-neutral-200 bg-neutral-50 p-4 dark:border-neutral-800 dark:bg-neutral-900">
                <div className="mb-4 flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500 text-neutral-950"><Mic className="h-5 w-5" /></div><div><p className="text-sm font-extrabold text-neutral-900 dark:text-white">Instant speaking feedback</p><p className="text-[11px] text-neutral-500">Analyze → correct → try again</p></div></div>
                  <span className="rounded-full bg-emerald-500/10 px-2.5 py-1 text-[10px] font-bold text-emerald-600">82% overall</span>
                </div>
                <div className="grid grid-cols-2 gap-x-5 gap-y-3 sm:grid-cols-4">
                  {voiceScores.map(({ label, value }) => (
                    <div key={label}>
                      <div className="mb-1 flex justify-between text-[10px] font-semibold text-neutral-500"><span>{label}</span><span>{value}</span></div>
                      <div className="h-1.5 overflow-hidden rounded-full bg-neutral-200 dark:bg-neutral-800"><div className="h-full rounded-full bg-amber-500" style={{ width: `${value}%` }} /></div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-3 lg:col-span-5">
            {intelligence.map(({ icon: Icon, title, desc }) => (
              <div key={title} className="juba-card group flex items-start gap-4 bg-white p-5 dark:bg-neutral-950">
                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-neutral-100 text-amber-500 transition-colors group-hover:bg-amber-500 group-hover:text-neutral-950 dark:bg-neutral-900"><Icon className="h-5 w-5" /></div>
                <div><h3 className="text-sm font-bold text-neutral-900 dark:text-white">{title}</h3><p className="mt-1 text-xs leading-relaxed text-neutral-500 dark:text-neutral-400">{desc}</p></div>
              </div>
            ))}
            <div className="rounded-2xl bg-neutral-900 p-5 text-white dark:bg-white dark:text-neutral-950">
              <div className="flex items-center gap-3"><BarChart3 className="h-5 w-5 text-amber-400 dark:text-amber-600" /><div><p className="text-sm font-extrabold">Your learning, not a generic course.</p><p className="mt-1 text-[11px] opacity-60">Personalized from day one and refined every session.</p></div></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
