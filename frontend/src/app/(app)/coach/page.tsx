'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import {
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  Flame,
  Mic,
  RefreshCw,
  Sparkles,
  Target,
  TrendingUp,
  Volume2,
  Zap,
} from 'lucide-react'

interface ProgressSummary {
  current_streak?: number
  total_xp?: number
  accuracy?: number
  vocabulary_mastered?: number
  vocabulary_total?: number
  vocabulary_progress?: number
  skills?: Record<string, number>
}

interface TodayPlan {
  cefr_level?: string | null
  lessons?: Array<{
    id: number | null
    title: string
    lesson_type: string
    estimated_minutes: number
    is_completed: boolean
  }>
  pending_count?: number
}

const scenarios = [
  { icon: '✈️', title: 'Airport', desc: 'Check in, ask for directions, handle delays.', href: '/conversation' },
  { icon: '💼', title: 'Job interview', desc: 'Practice answers, confidence and professional vocabulary.', href: '/conversation' },
  { icon: '🍽️', title: 'Restaurant', desc: 'Order naturally and handle a real conversation.', href: '/conversation' },
  { icon: '🏨', title: 'Hotel', desc: 'Book a room, solve problems and make requests.', href: '/conversation' },
]

export default function CoachPage() {
  const user = useAuthStore((s) => s.user)
  const language = useLanguageStore((s) => s.activeLanguage)
  const [progress, setProgress] = useState<ProgressSummary>({})
  const [plan, setPlan] = useState<TodayPlan>({})
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  async function load() {
    try {
      const [progressRes, planRes] = await Promise.all([
        apiFetch('/api/progress/summary'),
        apiFetch('/api/study-plan/today'),
      ])
      if (progressRes.ok) setProgress(await progressRes.json())
      if (planRes.ok) setPlan(await planRes.json())
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  useEffect(() => {
    load()
  }, [language?.code])

  const weakestSkill = useMemo(() => {
    const entries = Object.entries(progress.skills ?? {})
    if (!entries.length) return 'speaking'
    return entries.sort((a, b) => Number(a[1]) - Number(b[1]))[0][0]
  }, [progress.skills])

  const completed = (plan.lessons ?? []).filter((l) => l.is_completed).length
  const total = plan.lessons?.length ?? 0
  const vocabProgress = Math.round((progress.vocabulary_progress ?? 0) * 100)

  return (
    <main className="juba-mobile-coach min-h-screen bg-[#f8faf7] px-4 py-8 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-7xl space-y-8">
        <header className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="juba-eyebrow mb-3 inline-flex items-center gap-2 rounded-full border border-[#e1e5e2] bg-[#eaf5df] px-3 py-1.5 text-[#438600]">
              <BrainCircuit className="h-4 w-4" />
              Your AI Learning Coach
            </div>
            <h1 className="text-3xl font-black tracking-tight text-[#30343b] sm:text-4xl">
              {user?.displayName || user?.username || 'Learner'}, here is your next best move.
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-[#68736d] sm:text-base">
              JUBA LISAN turns your activity into a focused daily plan instead of asking you to decide what to study next.
            </p>
          </div>
          <button
            onClick={() => { setRefreshing(true); load() }}
            disabled={refreshing}
            className="inline-flex items-center justify-center gap-2 rounded-[20px] border-2 border-[#e1e5e2] bg-white px-4 py-2.5 text-sm font-bold text-[#30343b] transition hover:border-[var(--juba-primary)] disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh coaching
          </button>
        </header>

        <section className="grid gap-5 lg:grid-cols-[1.5fr_1fr]">
          <div className="juba-card overflow-hidden p-6 sm:p-8">
            <div className="flex flex-col gap-6 sm:flex-row sm:items-center">
              <div className="relative flex h-24 w-24 shrink-0 items-center justify-center rounded-3xl bg-[#58a700] text-[#30343b] shadow-[0_4px_0_#438600]">
                <Sparkles className="h-10 w-10" />
                <span className="absolute -right-1 -top-1 h-4 w-4 rounded-full border-2 border-white bg-[#ffb020]" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-xs font-extrabold uppercase tracking-[.18em] text-[#438600]">Coach insight</p>
                <h2 className="mt-2 text-2xl font-black text-[#30343b]">Focus on {weakestSkill.replaceAll('_', ' ')} today.</h2>
                <p className="mt-2 max-w-xl text-sm leading-6 text-[#68736d]">
                  Your recent activity suggests this is the highest-impact skill to practice next. A short session is better than skipping the day.
                </p>
                <div className="mt-5 flex flex-wrap gap-3">
                  <Link href="/conversation" className="inline-flex items-center gap-2 rounded-[20px] bg-[#58a700] px-5 py-3 text-sm font-bold text-[#30343b] transition hover:bg-[#438600]">
                    Start focused practice <ArrowRight className="h-4 w-4" />
                  </Link>
                  <Link href="/plan" className="inline-flex items-center gap-2 rounded-[20px] border-2 border-[#e1e5e2] px-5 py-3 text-sm font-bold text-[#30343b] transition hover:bg-[#eaf5df]">
                    View my plan
                  </Link>
                </div>
              </div>
            </div>
          </div>

          <div className="juba-card p-6">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[.16em] text-[#68736d]">Today's momentum</p>
                <p className="mt-1 text-xl font-black text-[#30343b]">Keep the streak alive</p>
              </div>
              <Flame className="h-6 w-6 text-[#438600]" />
            </div>
            <div className="grid grid-cols-3 gap-3">
              <Metric icon={<Flame />} value={`${progress.current_streak ?? 0}`} label="day streak" />
              <Metric icon={<Zap />} value={`${progress.total_xp ?? 0}`} label="total XP" />
              <Metric icon={<Target />} value={`${progress.accuracy ? Math.round(progress.accuracy * 100) : 0}%`} label="accuracy" />
            </div>
          </div>
        </section>

        <section className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          <CoachCard icon={<Mic />} title="Speak" value="10 min" detail="Build fluency with live correction." href="/conversation" />
          <CoachCard icon={<Volume2 />} title="Listen" value="8 min" detail="Train comprehension with targeted audio." href="/listening" />
          <CoachCard icon={<RefreshCw />} title="Review" value={`${Math.max(0, 15 - (plan.pending_count ?? 0))} cards`} detail="Refresh the words most likely to fade." href="/flashcards" />
          <CoachCard icon={<TrendingUp />} title="Progress" value={`${vocabProgress}%`} detail={`${progress.vocabulary_mastered ?? 0} words mastered so far.`} href="/progress" />
        </section>

        <section className="grid gap-5 lg:grid-cols-[1.35fr_1fr]">
          <div className="juba-card p-6 sm:p-8">
            <div className="mb-6 flex items-end justify-between gap-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-[.16em] text-[#438600]">Adaptive queue</p>
                <h2 className="mt-1 text-2xl font-black text-[#30343b]">Your best work for today</h2>
              </div>
              <span className="rounded-full bg-[#eaf5df] px-3 py-1 text-xs font-bold text-[#68736d]">{completed}/{total} complete</span>
            </div>
            <div className="space-y-3">
              {(plan.lessons ?? []).slice(0, 4).map((lesson, index) => (
                <Link key={`${lesson.id}-${index}`} href={lesson.id ? `/lesson/${lesson.id}` : '/plan'} className="group flex items-center gap-4 rounded-[20px] border-2 border-[#e1e5e2] bg-white p-4 transition hover:-translate-y-0.5 hover:border-[var(--juba-primary)]">
                  <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-[20px] ${lesson.is_completed ? 'bg-[#eaf5df] text-[#438600]' : 'bg-[#eaf5df] text-[#438600]'}`}>
                    {lesson.is_completed ? <CheckCircle2 className="h-5 w-5" /> : <span className="text-sm font-black">{index + 1}</span>}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-bold text-[#30343b]">{lesson.title}</p>
                    <p className="mt-1 text-xs text-[#68736d]">{lesson.lesson_type.replaceAll('_', ' ')} · {lesson.estimated_minutes || 25} min</p>
                  </div>
                  <ArrowRight className="h-4 w-4 text-[#68736d] transition group-hover:translate-x-1" />
                </Link>
              ))}
              {!plan.lessons?.length && !loading && <p className="rounded-[20px] border border-dashed border-[#e1e5e2] p-6 text-center text-sm text-[#68736d]">Complete your assessment to unlock an adaptive learning plan.</p>}
            </div>
          </div>

          <div className="juba-card p-6 sm:p-8">
            <p className="text-xs font-bold uppercase tracking-[.16em] text-[#438600]">Practice in context</p>
            <h2 className="mt-1 text-2xl font-black text-[#30343b]">Real-world rooms</h2>
            <p className="mt-2 text-sm leading-6 text-[#68736d]">Stop memorizing isolated sentences. Practice what you actually need to say.</p>
            <div className="mt-5 grid grid-cols-2 gap-3">
              {scenarios.map((scenario) => (
                <Link key={scenario.title} href={scenario.href} className="rounded-[20px] border-2 border-[#e1e5e2] p-4 transition hover:-translate-y-0.5 hover:border-[var(--juba-primary)] hover:bg-[#eaf5df]">
                  <span className="text-2xl">{scenario.icon}</span>
                  <p className="mt-3 text-sm font-black text-[#30343b]">{scenario.title}</p>
                  <p className="mt-1 text-xs leading-5 text-[#68736d]">{scenario.desc}</p>
                </Link>
              ))}
            </div>
          </div>
        </section>

        <footer className="flex flex-col gap-2 border-t border-[#e1e5e2] pt-6 text-xs text-[#68736d] sm:flex-row sm:items-center sm:justify-between">
          <span>Learning {language?.name ? `· ${language.name}` : '· personalized for you'}</span>
          <span>CEFR {plan.cefr_level || 'adaptive'} · JUBA LISAN Coach</span>
        </footer>
      </div>
    </main>
  )
}

function Metric({ icon, value, label }: { icon: React.ReactNode; value: string; label: string }) {
  return (
    <div className="rounded-[16px] bg-[#eaf5df] p-3">
      <div className="mb-2 h-4 w-4 text-[#438600]">{icon}</div>
      <p className="text-lg font-black text-[#30343b]">{value}</p>
      <p className="text-[10px] font-bold uppercase tracking-wider text-[#68736d]">{label}</p>
    </div>
  )
}

function CoachCard({ icon, title, value, detail, href }: { icon: React.ReactNode; title: string; value: string; detail: string; href: string }) {
  return (
    <Link href={href} className="juba-card group p-5">
      <div className="flex items-center justify-between">
        <span className="flex h-10 w-10 items-center justify-center rounded-[16px] bg-[#eaf5df] text-[#438600]">{icon}</span>
        <ArrowRight className="h-4 w-4 text-[#68736d] transition group-hover:translate-x-1" />
      </div>
      <p className="mt-5 text-xs font-bold uppercase tracking-[.14em] text-[#68736d]">{title}</p>
      <p className="mt-1 text-2xl font-black text-[#30343b]">{value}</p>
      <p className="mt-2 text-xs leading-5 text-[#68736d]">{detail}</p>
    </Link>
  )
}
