'use client'

import { useEffect, useMemo, useState, type ReactNode } from 'react'
import { useTranslations } from 'next-intl'
import Link from 'next/link'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { subscribeToLearningProgressUpdated } from '@/lib/learning-progress'
interface ProgressSummary {
  current_streak?: number
  total_xp?: number
  accuracy?: number
  vocabulary_mastered?: number
  vocabulary_total?: number
  vocabulary_progress?: number
  skills?: Record<string, number>
  mastery?: {
    tracked_items: number
    average_score: number
    counts: Record<string, number>
    skills: Record<string, { items: number; average_score: number; counts: Record<string, number> }>
  }
}

interface SmartReview {
  due_count?: number
  recommended_game?: string | null
  recommended_skill?: string | null
  cefr_level?: string | null
  average_mastery?: number
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
  const t = useTranslations('coach')
  const user = useAuthStore((s) => s.user)
  const language = useLanguageStore((s) => s.activeLanguage)
  const [progress, setProgress] = useState<ProgressSummary>({})
  const [plan, setPlan] = useState<TodayPlan>({})
  const [smartReview, setSmartReview] = useState<SmartReview>({})
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  async function load() {
    try {
      const [progressRes, planRes, reviewRes] = await Promise.all([
        apiFetch('/api/progress/summary'),
        apiFetch('/api/study-plan/today'),
        apiFetch('/api/progress/smart-review'),
      ])
      if (progressRes.ok) setProgress(await progressRes.json())
      if (planRes.ok) setPlan(await planRes.json())
      if (reviewRes.ok) setSmartReview(await reviewRes.json())
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  useEffect(() => {
    load()
  }, [language?.code])

  useEffect(() => {
    return subscribeToLearningProgressUpdated(() => {
      void load()
    })
  }, [])

  const weakestSkill = useMemo(() => {
    const entries = Object.entries(progress.skills ?? {})
    if (!entries.length) return 'speaking'
    return entries.sort((a, b) => Number(a[1]) - Number(b[1]))[0][0]
  }, [progress.skills])

  const completed = (plan.lessons ?? []).filter((l) => l.is_completed).length
  const total = plan.lessons?.length ?? 0
  const vocabProgress = Math.round((progress.vocabulary_progress ?? 0) * 100)
  const masterySkills = Object.entries(progress.mastery?.skills ?? {})
  const weakestMastery = masterySkills.length
    ? [...masterySkills].sort((a, b) => a[1].average_score - b[1].average_score)[0]
    : null
  const masteryCounts = progress.mastery?.counts ?? {}
  const masteryFocusLabel = weakestMastery
    ? weakestMastery[0].replaceAll('_', ' ')
    : weakestSkill.replaceAll('_', ' ')

  const reviewCopy = language?.code === 'ar'
    ? { eyebrow: 'مراجعة ذكية', title: 'لديك مراجعة مستحقة الآن', action: 'ابدأ المراجعة', skill: 'المهارة المقترحة' }
    : language?.code === 'fr'
      ? { eyebrow: 'Révision intelligente', title: 'Vous avez des révisions dues', action: 'Commencer la révision', skill: 'Compétence proposée' }
      : language?.code === 'es'
        ? { eyebrow: 'Repaso inteligente', title: 'Tienes repasos pendientes', action: 'Iniciar repaso', skill: 'Habilidad propuesta' }
        : language?.code === 'de'
          ? { eyebrow: 'Intelligente Wiederholung', title: 'Wiederholungen sind fällig', action: 'Wiederholung starten', skill: 'Empfohlene Fähigkeit' }
          : language?.code === 'it'
            ? { eyebrow: 'Ripasso intelligente', title: 'Hai ripassi da fare', action: 'Inizia il ripasso', skill: 'Abilità consigliata' }
            : language?.code === 'pt'
              ? { eyebrow: 'Revisão inteligente', title: 'Há revisões pendentes', action: 'Iniciar revisão', skill: 'Competência sugerida' }
              : language?.code === 'pl'
                ? { eyebrow: 'Inteligentna powtórka', title: 'Masz oczekujące powtórki', action: 'Rozpocznij powtórkę', skill: 'Sugerowana umiejętność' }
                : language?.code === 'nl'
                  ? { eyebrow: 'Slim herhalen', title: 'Je hebt herhalingen klaarstaan', action: 'Start herhaling', skill: 'Aanbevolen vaardigheid' }
                  : language?.code === 'ro'
                    ? { eyebrow: 'Recapitulare inteligentă', title: 'Ai elemente de revizuit', action: 'Începe revizuirea', skill: 'Competență recomandată' }
                    : language?.code === 'ru'
                      ? { eyebrow: 'Умное повторение', title: 'Есть задания для повторения', action: 'Начать повторение', skill: 'Рекомендуемый навык' }
                      : { eyebrow: 'Smart review', title: 'You have due reviews', action: 'Start review', skill: 'Recommended skill' }

  return (
    <main className="container-xl page-body py-4">
      <div className="mx-auto max-w-7xl space-y-8">
        <header className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="page-pretitle mb-3 inline-flex items-center gap-2 rounded-full border border bg-[#ededff] px-3 py-1.5 text-[#373fb8]">
              <BrainCircuit className="h-4 w-4" />
              {t('eyebrow')}
            </div>
            <h1 className="text-3xl font-black tracking-tight text-[#202127] sm:text-4xl">
              {user?.displayName || user?.username || 'Learner'}, {t('headlineSuffix')}
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-[rgba(32,33,39,.52)] sm:text-base">
              {t('description')}
            </p>
          </div>
          <button
            type="button"
            onClick={() => { setRefreshing(true); load() }}
            disabled={refreshing}
            className="inline-flex items-center justify-center gap-2 rounded border border bg-white px-4 py-2.5 text-sm font-bold text-[#202127] transition hover:border-[#5862e2] disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
            {t('refresh')}
          </button>
        </header>

        <section className="grid gap-5 lg:grid-cols-[1.5fr_1fr]">
          <div className="card overflow-hidden p-6 sm:p-8">
            <div className="flex flex-col gap-6 sm:flex-row sm:items-center">
              <div className="relative flex h-24 w-24 shrink-0 items-center justify-center rounded-3xl bg-[#5862e2] text-[#202127] ">
                <i className="ti ti-sparkles icon" aria-hidden="true" />
                <span className="absolute -right-1 -top-1 h-4 w-4 rounded-full border border-[#fff] bg-[#fff3d1]" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-xs font-extrabold uppercase tracking-[.18em] text-[#373fb8]">{t('insight')}</p>
                <h2 className="mt-2 text-2xl font-black text-[#202127]">{t('focusOn')} {weakestSkill.replaceAll('_', ' ')} {t('today')}</h2>
                <p className="mt-2 max-w-xl text-sm leading-6 text-[rgba(32,33,39,.52)]">
                  {t('insightDescription')}
                </p>
                <div className="mt-5 flex flex-wrap gap-3">
                  <Link href="/conversation" className="inline-flex items-center gap-2 rounded bg-[#5862e2] px-5 py-3 text-sm font-bold text-white  transition hover:opacity-90">
                    {t('startPractice')} <ArrowRight className="h-4 w-4" />
                  </Link>
                  <Link href="/plan" className="inline-flex items-center gap-2 rounded border border px-5 py-3 text-sm font-bold text-[#202127] transition hover:bg-[#ededff]">
                    {t('viewPlan')}
                  </Link>
                </div>
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[.16em] text-[rgba(32,33,39,.52)]">{t('momentum')}</p>
                <p className="mt-1 text-xl font-black text-[#202127]">{t('keepStreak')}</p>
              </div>
              <Flame className="h-6 w-6 text-[#373fb8]" />
            </div>
            <div className="grid grid-cols-3 gap-3">
              <Metric icon={<Flame />} value={`${progress.current_streak ?? 0}`} label={t('dayStreak')} />
              <Metric icon={<Zap />} value={`${progress.total_xp ?? 0}`} label={t('totalXp')} />
              <Metric icon={<Target />} value={`${progress.accuracy ? Math.round(progress.accuracy * 100) : 0}%`} label={t('accuracy')} />
            </div>
          </div>
        </section>

        {Number(smartReview.due_count ?? 0) > 0 && (
          <section className="card overflow-hidden border border-[#5862e2] p-6 sm:p-8">
            <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[.16em] text-[#373fb8]">{reviewCopy.eyebrow}</p>
                <h2 className="mt-1 text-2xl font-black text-[#202127]">{reviewCopy.title}</h2>
                <p className="mt-2 text-sm leading-6 text-[rgba(32,33,39,.52)]">
                  {smartReview.due_count} · {reviewCopy.skill}: {(smartReview.recommended_skill ?? weakestSkill).replaceAll('_', ' ')}
                  {smartReview.cefr_level ? ' · CEFR ' + smartReview.cefr_level : ''}
                </p>
              </div>
              <Link href="/games?review=1" className="inline-flex items-center justify-center gap-2 rounded bg-[#5862e2] px-5 py-3 text-sm font-bold text-white  transition hover:opacity-90">
                {reviewCopy.action} <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </section>
        )}

        {progress.mastery && progress.mastery.tracked_items > 0 && (
          <section className="card p-6 sm:p-8">
            <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[.16em] text-[#373fb8]">{t('review')}</p>
                <h2 className="mt-1 text-2xl font-black text-[#202127]">
                  {t('focusOn')} {masteryFocusLabel} {t('today')}
                </h2>
                <p className="mt-2 text-sm leading-6 text-[rgba(32,33,39,.52)]">
                  {Math.round((progress.mastery.average_score ?? 0) * 100)}% {t('accuracy')} · {progress.mastery.tracked_items} {t('wordsMastered')}
                </p>
              </div>
              <div className="grid grid-cols-2 gap-2 sm:grid-cols-5">
                {(['new', 'learning', 'reviewing', 'weak', 'mastered'] as const).map((state) => (
                  <div key={state} className="min-w-[68px] rounded border border bg-[#ededff] px-3 py-2 text-center">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-[rgba(32,33,39,.52)]">
                      {state === 'mastered' ? t('mastered') : state === 'new' ? t('notStarted') : t('inProgress')}
                    </p>
                    <p className="mt-1 text-sm font-black text-[#202127]">{masteryCounts[state] ?? 0}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

        <section className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          <CoachCard icon={<Mic />} title={t('speak')} value={t('conversation')} detail={t('speakDetail')} href="/conversation" />
          <CoachCard icon={<Volume2 />} title={t('listen')} value={t('practice')} detail={t('listenDetail')} href="/listening" />
          <CoachCard icon={<RefreshCw />} title={t('review')} value={t('flashcards')} detail={t('reviewDetail')} href="/flashcards" />
          <CoachCard icon={<TrendingUp />} title={t('progress')} value={`${vocabProgress}%`} detail={`${progress.vocabulary_mastered ?? 0} {t('wordsMastered')}`} href="/progress" />
        </section>

        <section className="grid gap-5 lg:grid-cols-[1.35fr_1fr]">
          <div className="card p-6 sm:p-8">
            <div className="mb-6 flex items-end justify-between gap-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-[.16em] text-[#373fb8]">{t('adaptiveQueue')}</p>
                <h2 className="mt-1 text-2xl font-black text-[#202127]">{t('bestWork')}</h2>
              </div>
              <span className="rounded-full bg-[#ededff] px-3 py-1 text-xs font-bold text-[rgba(32,33,39,.52)]">{completed}/{total} {t('complete')}</span>
            </div>
            <div className="space-y-3">
              {(plan.lessons ?? []).slice(0, 4).map((lesson, index) => (
                <Link key={`${lesson.id}-${index}`} href={lesson.id ? `/lesson/${lesson.id}` : '/plan'} className="group flex items-center gap-4 rounded-[28px] border border bg-white p-4 transition hover:-translate-y-0.5 hover:border-[#5862e2]">
                  <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded ${lesson.is_completed ? 'bg-[#fff3d1] text-[#373fb8]' : 'bg-[#ededff] text-[#373fb8]'}`}>
                    {lesson.is_completed ? <CheckCircle2 className="h-5 w-5" /> : <span className="text-sm font-black">{index + 1}</span>}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-bold text-[#202127]">{lesson.title}</p>
                    <p className="mt-1 text-xs text-[rgba(32,33,39,.52)]">{lesson.lesson_type.replaceAll('_', ' ')} · {lesson.estimated_minutes || 25} min</p>
                  </div>
                  <ArrowRight className="h-4 w-4 text-[rgba(32,33,39,.52)] transition group-hover:translate-x-1" />
                </Link>
              ))}
              {!plan.lessons?.length && !loading && <p className="rounded-[28px] border border-dashed border p-6 text-center text-sm text-[rgba(32,33,39,.52)]">{t('assessmentPrompt')}</p>}
            </div>
          </div>

          <div className="card p-6 sm:p-8">
            <p className="text-xs font-bold uppercase tracking-[.16em] text-[#373fb8]">{t('contextEyebrow')}</p>
            <h2 className="mt-1 text-2xl font-black text-[#202127]">{t('rooms')}</h2>
            <p className="mt-2 text-sm leading-6 text-[rgba(32,33,39,.52)]">{t('roomsDescription')}</p>
            <div className="mt-5 grid grid-cols-2 gap-3">
              {scenarios.map((scenario) => (
                <Link key={scenario.title} href={scenario.href} className="rounded-[28px] border border p-4 transition hover:-translate-y-0.5 hover:border-[#5862e2] hover:bg-[#ededff]">
                  <span className="text-2xl">{scenario.icon}</span>
                  <p className="mt-3 text-sm font-black text-[#202127]">{scenario.title}</p>
                  <p className="mt-1 text-xs leading-5 text-[rgba(32,33,39,.52)]">{scenario.desc}</p>
                </Link>
              ))}
            </div>
          </div>
        </section>

        <footer className="flex flex-col gap-2 border-t border pt-6 text-xs text-[rgba(32,33,39,.52)] sm:flex-row sm:items-center sm:justify-between">
          <span>Learning {language?.name ? `· ${language.name}` : `· ${t('personalized')}`}</span>
          <span>CEFR {plan.cefr_level || t('adaptive')} · JUBA LISAN Coach</span>
        </footer>
      </div>
    </main>
  )
}

function Metric({ icon, value, label }: { icon: ReactNode; value: string; label: string }) {
  return (
    <div className="rounded-[28px] bg-[#ededff] p-3">
      <div className="mb-2 h-4 w-4 text-[#373fb8]">{icon}</div>
      <p className="text-lg font-black text-[#202127]">{value}</p>
      <p className="text-[10px] font-bold uppercase tracking-wider text-[rgba(32,33,39,.52)]">{label}</p>
    </div>
  )
}

function CoachCard({ icon, title, value, detail, href }: { icon: React.ReactNode; title: string; value: string; detail: string; href: string }) {
  return (
    <Link href={href} className="card group p-5">
      <div className="flex items-center justify-between">
        <span className="flex h-10 w-10 items-center justify-center rounded bg-[#ededff] text-[#373fb8]">{icon}</span>
        <ArrowRight className="h-4 w-4 text-[rgba(32,33,39,.52)] transition group-hover:translate-x-1" />
      </div>
      <p className="mt-5 text-xs font-bold uppercase tracking-[.14em] text-[rgba(32,33,39,.52)]">{title}</p>
      <p className="mt-1 text-2xl font-black text-[#202127]">{value}</p>
      <p className="mt-2 text-xs leading-5 text-[rgba(32,33,39,.52)]">{detail}</p>
    </Link>
  )
}
