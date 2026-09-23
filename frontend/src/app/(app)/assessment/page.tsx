'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useLanguageStore } from '@/store/language'
import { isSubscribed, useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import BeginnerGate from '@/components/assessment/BeginnerGate'
import AdaptiveQuizCard from '@/components/assessment/AdaptiveQuizCard'
import DurationSelector, {
  DURATION_OPTIONS,
  type DurationOption,
} from '@/components/assessment/DurationSelector'
import { type AssessmentQuestion, type CEFRLevel } from '@/data/types'
import { CEFR_LEVELS } from '@/data/curriculum'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'

interface AnswerRecord {
  question_id: string
  skill: string
  difficulty: string
  correct: boolean
}

interface AssessmentResult {
  cefr_level: string
  score: number
  skill_profile: Record<string, number>
  strengths: string[]
  weaknesses: string[]
}

interface ExistingPlan {
  cefr_level: string
  created_at: string
}

interface VoiceTrialOffer {
  available: boolean
  token?: string
  duration_seconds?: number
}

interface AssessmentCompleteResponse {
  plan_id: number
  cefr_level: string
  voice_trial?: VoiceTrialOffer
}

type FlowStep =
  | 'checking'
  | 'existing'
  | 'beginner-gate'
  | 'quiz'
  | 'result'
  | 'duration'
  | 'voice-trial-offer'

const MAX_QUESTIONS = 15
const CORRECT_STREAK_TO_UP = 2
const WRONG_STREAK_TO_DOWN = 2
const START_LEVEL: CEFRLevel = 'A2'

function pickNextQuestion(
  bank: AssessmentQuestion[],
  usedIds: Set<string>,
  currentLevel: CEFRLevel
): AssessmentQuestion | null {
  const available = bank.filter(
    (q) => !usedIds.has(q.id) && q.difficulty === currentLevel
  )
  if (available.length === 0) return null
  return available[Math.floor(Math.random() * available.length)]
}

function adjustLevel(current: CEFRLevel, direction: 'up' | 'down'): CEFRLevel {
  const idx = CEFR_LEVELS.indexOf(current)
  if (direction === 'up' && idx < CEFR_LEVELS.length - 1)
    return CEFR_LEVELS[idx + 1]
  if (direction === 'down' && idx > 0) return CEFR_LEVELS[idx - 1]
  return current
}

export default function AssessmentPage() {
  const t = useTranslations('assessment')
  const tCommon = useTranslations('common')
  const router = useRouter()
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const user = useAuthStore((s) => s.user)
  const stripeEnabled = useConfigStore((s) => s.stripeEnabled)
  const configLoaded = useConfigStore((s) => s.loaded)
  const loadConfig = useConfigStore((s) => s.load)

  const [step, setStep] = useState<FlowStep>('checking')
  const [existingPlan, setExistingPlan] = useState<ExistingPlan | null>(null)
  const [error, setError] = useState('')
  const [bank, setBank] = useState<AssessmentQuestion[]>([])
  const [currentQuestion, setCurrentQuestion] = useState<AssessmentQuestion | null>(null)
  const [questionNumber, setQuestionNumber] = useState(0)
  const [answers, setAnswers] = useState<AnswerRecord[]>([])
  const [usedIds] = useState<Set<string>>(() => new Set())
  const [currentLevel, setCurrentLevel] = useState<CEFRLevel>(START_LEVEL)
  const [correctStreak, setCorrectStreak] = useState(0)
  const [wrongStreak, setWrongStreak] = useState(0)
  const [result, setResult] = useState<AssessmentResult | null>(null)
  const [selectedLevel, setSelectedLevel] = useState<CEFRLevel>('A1')
  const [evaluating, setEvaluating] = useState(false)
  const [durationOption, setDurationOption] = useState<DurationOption>(DURATION_OPTIONS[2])
  const [selectedGoals, setSelectedGoals] = useState<string[]>(['grammar', 'vocabulary'])
  const [submitting, setSubmitting] = useState(false)
  const [trialLoading, setTrialLoading] = useState(false)
  const [createdPlanId, setCreatedPlanId] = useState<number | null>(null)
  const [voiceTrial, setVoiceTrial] = useState<VoiceTrialOffer | null>(null)
  const [showStartWarning, setShowStartWarning] = useState(false)

  useEffect(() => { void loadConfig() }, [loadConfig])

  useEffect(() => {
    async function check() {
      try {
        const lang = activeLanguage?.code ?? 'en-GB'
        const [planRes, bankRes] = await Promise.all([
          apiFetch('/api/study-plan/current'),
          apiFetch(`/api/assessment/bank?language=${lang}`),
        ])
        if (bankRes.ok) {
          const bankData = (await bankRes.json()) as { questions: AssessmentQuestion[] }
          setBank(bankData.questions)
        }
        if (planRes.ok) {
          const plan = await planRes.json()
          if (plan?.cefr_level) {
            setExistingPlan(plan as ExistingPlan)
            setStep('existing')
            return
          }
        }
      } catch {
        /* no plan */
      }
      setStep('beginner-gate')
    }
    void check()
  }, [activeLanguage?.code])

  const canOfferVoiceTrial =
    configLoaded && stripeEnabled && user !== null &&
    !isSubscribed(user, stripeEnabled) && !user.assessment_voice_trial_used

  function loadNextQuestion(level: CEFRLevel, usedSet: Set<string>) {
    const q = pickNextQuestion(bank, usedSet, level)
    if (q) {
      usedSet.add(q.id)
      setCurrentQuestion(q)
    } else {
      void evaluateQuiz([...answers])
    }
  }

  function startQuiz() {
    if (bank.length === 0) {
      setError(tCommon('errorMessage'))
      return
    }
    usedIds.clear()
    setAnswers([])
    setCurrentLevel(START_LEVEL)
    setCorrectStreak(0)
    setWrongStreak(0)
    const q = pickNextQuestion(bank, usedIds, START_LEVEL)
    if (q) {
      usedIds.add(q.id)
      setCurrentQuestion(q)
      setQuestionNumber(1)
      setStep('quiz')
    }
  }

  function handleAnswer(chosen: string) {
    if (!currentQuestion) return
    const isCorrect = chosen === currentQuestion.correct
    const record: AnswerRecord = {
      question_id: currentQuestion.id,
      skill: currentQuestion.skill,
      difficulty: currentQuestion.difficulty,
      correct: isCorrect,
    }
    const newAnswers = [...answers, record]
    setAnswers(newAnswers)
    let newCorrect = correctStreak
    let newWrong = wrongStreak
    let newLevel = currentLevel
    if (isCorrect) {
      newCorrect += 1
      newWrong = 0
      if (newCorrect >= CORRECT_STREAK_TO_UP) {
        newLevel = adjustLevel(currentLevel, 'up')
        newCorrect = 0
      }
    } else {
      newWrong += 1
      newCorrect = 0
      if (newWrong >= WRONG_STREAK_TO_DOWN) {
        newLevel = adjustLevel(currentLevel, 'down')
        newWrong = 0
      }
    }
    setCorrectStreak(newCorrect)
    setWrongStreak(newWrong)
    if (newAnswers.length >= MAX_QUESTIONS) {
      void evaluateQuiz(newAnswers)
      return
    }
    setCurrentLevel(newLevel)
    setQuestionNumber((n) => n + 1)
    setTimeout(() => loadNextQuestion(newLevel, usedIds), 150)
  }

  async function evaluateQuiz(answersToSend: AnswerRecord[]) {
    setEvaluating(true)
    setCurrentQuestion(null)
    try {
      const res = await apiFetch('/api/assessment/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: answersToSend }),
      })
      if (!res.ok) {
        const d = await res.json().catch(() => ({}))
        throw new Error((d as { detail?: string }).detail ?? `Error ${res.status}`)
      }
      const data = (await res.json()) as AssessmentResult
      setResult(data)
      setSelectedLevel(data.cefr_level as CEFRLevel)
      setStep('result')
    } catch (err) {
      const msg = err instanceof Error ? err.message : ''
      setError(msg === 'ai_service_error' || msg === 'ai_service_unavailable' ? tCommon('errorMessage') : msg || 'Evaluation failed')
    } finally {
      setEvaluating(false)
    }
  }

  async function handleComplete() {
    if (!result) return
    setSubmitting(true)
    setError('')
    try {
      const res = await apiFetch('/api/assessment/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cefr_level: selectedLevel,
          skill_profile: result.skill_profile,
          strengths: result.strengths,
          weaknesses: result.weaknesses,
          duration_weeks: durationOption.weeks,
          days_per_week: durationOption.daysPerWeek,
          goals: selectedGoals,
          target_language: activeLanguage?.code ?? undefined,
        }),
      })
      if (!res.ok) {
        const d = await res.json().catch(() => ({}))
        throw new Error((d as { detail?: string }).detail ?? `Error ${res.status}`)
      }
      const data = (await res.json()) as AssessmentCompleteResponse
      setCreatedPlanId(data.plan_id)
      if (data.voice_trial?.available && data.voice_trial.token) {
        setVoiceTrial(data.voice_trial)
        setStep('voice-trial-offer')
        setSubmitting(false)
        return
      }
      router.push('/plan')
    } catch (err) {
      const msg = err instanceof Error ? err.message : ''
      setError(msg === 'ai_service_error' || msg === 'ai_service_unavailable' ? tCommon('errorMessage') : msg || 'Failed to create plan')
      setSubmitting(false)
    }
  }

  function startVoiceTrial() {
    if (!voiceTrial?.token) return
    sessionStorage.setItem('assessment_voice_trial', JSON.stringify({
      token: voiceTrial.token,
      durationSeconds: voiceTrial.duration_seconds ?? 300,
      cefrLevel: selectedLevel,
      planId: createdPlanId,
      targetLanguage: activeLanguage?.code,
    }))
    router.push('/conversation')
  }

  async function requestVoiceTrial() {
    if (!existingPlan) return
    setTrialLoading(true)
    setError('')
    try {
      const res = await apiFetch('/api/assessment/voice-trial', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_language: activeLanguage?.code }),
      })
      if (!res.ok) {
        const d = await res.json().catch(() => ({}))
        throw new Error((d as { detail?: string }).detail ?? `Error ${res.status}`)
      }
      const data = (await res.json()) as AssessmentCompleteResponse
      if (data.voice_trial?.available && data.voice_trial.token) {
        setCreatedPlanId(data.plan_id)
        setSelectedLevel(data.cefr_level as CEFRLevel)
        setVoiceTrial(data.voice_trial)
        setStep('voice-trial-offer')
        return
      }
      setError(tCommon('errorMessage'))
    } catch (err) {
      const msg = err instanceof Error ? err.message : ''
      setError(msg || tCommon('errorMessage'))
    } finally {
      setTrialLoading(false)
    }
  }

  const cardClass = 'w-full max-w-2xl overflow-hidden rounded-[30px] border-2 border-[var(--juba-lilac)] bg-white shadow-[0_22px_55px_rgba(61,42,130,0.12)]'
  const panelClass = 'rounded-[22px] border-2 border-[var(--juba-lilac)] bg-[var(--juba-lilac)]/45 p-4'
  const actionClass = 'w-full rounded-[18px] bg-[var(--juba-violet-dark)] px-4 py-3 font-bold text-white shadow-[0_6px_0_var(--juba-violet-dark)] transition hover:-translate-y-0.5 hover:bg-[var(--juba-violet-dark)]'

  if (step === 'checking' || (step === 'quiz' && (evaluating || !currentQuestion))) {
    return <PageLoading label={evaluating ? t('evaluating') : tCommon('loading')} />
  }

  if (step === 'existing' && existingPlan) {
    const assessedDate = new Date(existingPlan.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })
    return (
      <div className="flex min-h-[60vh] items-center justify-center bg-gradient-to-br from-[var(--juba-lilac)]/30 via-white to-[var(--juba-sky)]/20 p-4 sm:p-6">
        <div className={cardClass}>
          <div className="flex items-center gap-3 border-b border-[var(--juba-border)] px-5 py-4">
            <span className="flex h-8 w-8 items-center justify-center rounded-[18px] bg-[var(--juba-lilac)] text-sm font-bold text-[var(--juba-violet-dark)]">A</span>
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('title')}</p>
              <p className="text-xs text-[var(--juba-muted)]">{t('currentLevel')}</p>
            </div>
          </div>
          <div className="space-y-6 p-6 sm:p-8 text-center">
            <div>
              <p className="mb-2 text-xs font-semibold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('currentLevel')}</p>
              <p className="text-6xl font-extrabold tracking-tight text-[var(--juba-text)]">{existingPlan.cefr_level}</p>
            </div>
            <div className={panelClass}>
              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('assessedOn')}</p>
              <p className="mt-1 text-sm text-[var(--juba-text)]">{assessedDate}</p>
            </div>
            <p className="text-sm leading-relaxed text-[var(--juba-muted)]">{t('alreadyHasPlan')}</p>
            {canOfferVoiceTrial && (
              <div className={panelClass + ' space-y-3'}>
                <p className="font-semibold text-[var(--juba-text)]">{t('voiceTrialTitle')}</p>
                <p className="text-xs leading-relaxed text-[var(--juba-muted)]">{t('voiceTrialDesc', { minutes: 5 })}</p>
                <button onClick={requestVoiceTrial} disabled={trialLoading} className={actionClass + ' disabled:opacity-50'}>
                  {trialLoading ? '...' : `${t('voiceTrialStart')} →`}
                </button>
              </div>
            )}
            {error && <div className="rounded-[18px] border border-[var(--juba-danger)]/30 bg-[var(--juba-danger)]/10 px-4 py-3 text-xs text-[var(--juba-danger)]">✕ {error}</div>}
            <div className="flex gap-2">
              <button onClick={() => router.push('/dashboard')} className="flex-1 rounded-[18px] border border-[var(--juba-border)] px-3 py-3 text-xs font-semibold text-[var(--juba-muted)] transition hover:bg-[var(--juba-surface-soft)]">← {tCommon('backToDashboard')}</button>
              <button onClick={() => setStep('beginner-gate')} className={actionClass + ' flex-[1.75]'}>{t('retake')}</button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (step === 'beginner-gate') {
    return (
      <>
        <BeginnerGate
          languageCode={activeLanguage?.iso639 ?? ''}
          onBeginner={() => {
            setResult({ cefr_level: 'A1', score: 0, skill_profile: {}, strengths: [], weaknesses: [] })
            setSelectedLevel('A1')
            setAnswers([])
            setStep('duration')
          }}
          onHasExperience={() => setShowStartWarning(true)}
        />
        <ConfirmDialog
          open={showStartWarning}
          title={t('startWarningTitle')}
          message={t('startWarningMessage')}
          confirmLabel={t('startWarningConfirm')}
          onConfirm={() => { setShowStartWarning(false); startQuiz() }}
          onCancel={() => setShowStartWarning(false)}
        />
      </>
    )
  }

  if (step === 'quiz' && currentQuestion) {
    return (
      <div className="juba-mobile-assessment mx-auto w-full max-w-4xl px-4 py-6 sm:py-10">
        <div className="mb-5 flex items-center justify-between rounded-[22px] border-2 border-[var(--juba-lilac)] bg-white px-5 py-4 shadow-sm">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('title')}</p>
            <p className="mt-1 text-sm font-semibold text-[var(--juba-text)]">{currentLevel}</p>
          </div>
          <div className="rounded-[18px] bg-[var(--juba-lilac)] px-3 py-1.5 text-xs font-bold text-[var(--juba-violet-dark)]">{questionNumber}/{MAX_QUESTIONS}</div>
        </div>
        <AdaptiveQuizCard question={currentQuestion} questionNumber={questionNumber} totalQuestions={MAX_QUESTIONS} onAnswer={handleAnswer} languageCode={activeLanguage?.code} />
      </div>
    )
  }

  if (step === 'result' && result) {
    const score = Math.round(result.score * 100)
    const aiLevel = result.cefr_level
    const levelChanged = selectedLevel !== aiLevel
    return (
      <div className="flex min-h-[60vh] items-center justify-center p-4 sm:p-6">
        <div className={cardClass}>
          <div className="flex items-center gap-3 border-b border-[var(--juba-border)] px-5 py-4">
            <span className="flex h-8 w-8 items-center justify-center rounded-[18px] bg-[var(--juba-yellow)] text-sm font-bold text-[var(--juba-violet-dark)]">✓</span>
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('resultStep')}</p>
              <p className="text-xs text-[var(--juba-muted)]">{t('cefrLevel')}</p>
            </div>
          </div>
          <div className="space-y-6 p-6 sm:p-8 text-center">
            <div>
              <p className="mb-2 text-xs font-semibold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('cefrLevel')}</p>
              <p className="text-6xl font-extrabold tracking-tight text-[var(--juba-text)]">{aiLevel}</p>
            </div>
            <div className={panelClass}>
              <p className="text-xs font-semibold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{tCommon('score')}</p>
              <p className="mt-1 text-3xl font-extrabold text-[var(--juba-text)]">{score}%</p>
            </div>
            <div>
              <p className="mb-3 text-xs font-semibold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('overrideLevel')}</p>
              <div className="flex flex-wrap justify-center gap-2">
                {CEFR_LEVELS.map((lvl) => (
                  <button key={lvl} onClick={() => setSelectedLevel(lvl)} className={`rounded-[18px] border px-4 py-2 text-xs font-bold transition ${selectedLevel === lvl ? 'border-[var(--juba-violet-dark)] bg-[var(--juba-lilac)] text-[var(--juba-violet-dark)]' : 'border-[var(--juba-border)] text-[var(--juba-muted)] hover:bg-[var(--juba-surface-soft)]'}`}>
                    {lvl}
                  </button>
                ))}
              </div>
              {levelChanged && <p className="mt-2 text-xs text-[var(--juba-muted)]">{t('suggestedLevel', { aiLevel, selectedLevel })}</p>}
            </div>
            {result.strengths.length > 0 && (
              <div>
                <p className="mb-2 text-xs font-semibold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('strengths')}</p>
                <div className="flex flex-wrap justify-center gap-2">{result.strengths.map((s) => <span key={s} className="rounded-[18px] border border-[var(--juba-border)] bg-[var(--juba-yellow)] px-3 py-1.5 text-xs font-medium text-[var(--juba-violet-dark)]">{s}</span>)}</div>
              </div>
            )}
            {result.weaknesses.length > 0 && (
              <div>
                <p className="mb-2 text-xs font-semibold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('needsWork')}</p>
                <div className="flex flex-wrap justify-center gap-2">{result.weaknesses.map((w) => <span key={w} className="rounded-[18px] border border-[var(--juba-danger)]/25 bg-[var(--juba-danger)]/10 px-3 py-1.5 text-xs font-medium text-[var(--juba-danger)]">{w}</span>)}</div>
              </div>
            )}
            {error && <div className="rounded-[18px] border border-[var(--juba-danger)]/30 bg-[var(--juba-danger)]/10 px-4 py-3 text-xs text-[var(--juba-danger)]">✕ {error}</div>}
            <button onClick={() => setStep('duration')} className={actionClass}>{t('createPlan')} →</button>
          </div>
        </div>
      </div>
    )
  }

  if (step === 'duration') {
    return (
      <DurationSelector
        selectedWeeks={durationOption.weeks}
        selectedGoals={selectedGoals}
        onSelectDuration={setDurationOption}
        onToggleGoal={(goal) => setSelectedGoals((prev) => prev.includes(goal) ? prev.filter((g) => g !== goal) : [...prev, goal])}
        onConfirm={handleComplete}
        onBack={() => {
          const isBeginner = result?.score === 0 && result?.cefr_level === 'A1' && answers.length === 0
          setStep(isBeginner ? 'beginner-gate' : 'result')
        }}
        cefr_level={selectedLevel}
        loading={submitting}
      />
    )
  }

  if (step === 'voice-trial-offer') {
    const minutes = Math.round((voiceTrial?.duration_seconds ?? 300) / 60)
    return (
      <div className="flex min-h-[60vh] items-center justify-center p-4 sm:p-6">
        <div className={cardClass}>
          <div className="flex items-center gap-3 border-b border-[var(--juba-border)] px-5 py-4">
            <span className="flex h-8 w-8 items-center justify-center rounded-[18px] bg-[var(--juba-lilac)] text-sm font-bold text-[var(--juba-violet-dark)]">◉</span>
            <p className="text-xs font-bold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('voiceTrialLabel')}</p>
          </div>
          <div className="space-y-6 p-6 sm:p-8 text-center">
            <div>
              <p className="mb-2 text-xs font-semibold uppercase tracking-[0.12em] text-[var(--juba-muted)]">{t('cefrLevel')}</p>
              <p className="text-6xl font-extrabold tracking-tight text-[var(--juba-text)]">{selectedLevel}</p>
            </div>
            <div className={panelClass}>
              <p className="mb-2 font-semibold text-[var(--juba-text)]">{t('voiceTrialTitle')}</p>
              <p className="text-xs leading-relaxed text-[var(--juba-muted)]">{t('voiceTrialDesc', { minutes })}</p>
            </div>
            <button onClick={startVoiceTrial} className={actionClass}>{t('voiceTrialStart')} →</button>
            <button onClick={() => router.push('/plan')} className="w-full py-2 text-xs font-semibold uppercase tracking-[0.1em] text-[var(--juba-muted)] transition hover:text-[var(--juba-text)]">{t('voiceTrialSkip')}</button>
          </div>
        </div>
      </div>
    )
  }

  return null
}
