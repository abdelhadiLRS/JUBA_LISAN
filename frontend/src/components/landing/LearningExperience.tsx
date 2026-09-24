import Link from 'next/link'
import { Globe, Target, Compass, MessageSquare, TrendingUp, Sparkles, BrainCircuit, FileText, Mic, RotateCcw, ArrowRight, BookOpen, Headphones, Layers } from 'lucide-react'

interface LearningExperienceProps { t: (key: string) => string }

export function LearningExperience({ t }: LearningExperienceProps) {
  const steps = [
    [Globe, 'step1Title', 'step1Desc', 'LANGUAGE', '/dashboard'],
    [Target, 'step2Title', 'step2Desc', 'ASSESS', '/assessment'],
    [Compass, 'step3Title', 'step3Desc', 'PLAN', '/dashboard'],
    [MessageSquare, 'step4Title', 'step4Desc', 'PRACTICE', '/chat'],
    [TrendingUp, 'step5Title', 'step5Desc', 'PROGRESS', '/dashboard'],
  ] as const

  const tools = [
    [MessageSquare, 'AI Tutor', 'Practice conversations with the JUBA AI tutor.', '/chat'],
    [Mic, 'Voice Conversation', 'Speak and continue your language practice by voice.', '/conversation'],
    [BookOpen, 'Lessons', 'Work through structured CEFR-aligned lessons and exercises.', '/dashboard'],
    [Headphones, 'Listening', 'Build listening practice through the learning experience.', '/dashboard'],
    [Layers, 'Vocabulary & Review', 'Review vocabulary and reinforce learning over time.', '/dashboard'],
  ] as const

  const intelligence = [
    [BrainCircuit, 'Adaptive progress', 'Learning recommendations can respond to your assessment and progress.'],
    [FileText, 'Learning resources', 'Use the platform lessons, exercises and vocabulary practice as one workflow.'],
    [RotateCcw, 'Review loop', 'Return to vocabulary and skills as you continue through your learning path.'],
  ] as const

  return (
    <section className="juba-funfluent-experience py-20 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="juba-ff-section-head">
          <span className="juba-ff-section-tag"><Sparkles className="mr-1 inline h-3.5 w-3.5" />The JUBA LISAN learning journey</span>
          <h2>{t('experienceTitle')}</h2>
          <p>{t('experienceSubtitle')}</p>
        </div>

        <div className="juba-ff-steps">
          {steps.map(([Icon, title, desc, art, href], i) => (
            <Link href={href} key={title} className={`juba-ff-step step-${i}`}>
              <div className="juba-ff-step-number">{String(i + 1).padStart(2, '0')}</div>
              <div className="juba-ff-step-art">{art}</div>
              <Icon className="juba-ff-step-icon" />
              <h3>{t(title)}</h3>
              <p>{t(desc)}</p>
              <span className="mt-3 inline-flex items-center gap-1 text-xs font-bold uppercase tracking-wider">Open <ArrowRight className="h-3.5 w-3.5" /></span>
            </Link>
          ))}
        </div>

        <div className="juba-ff-practice">
          <div className="juba-ff-practice-copy">
            <span className="juba-ff-section-tag">Real JUBA LISAN tools</span>
            <h3>Move from explanation to practice.</h3>
            <p>These are real product areas, not simulated lessons. Open an area to continue inside JUBA LISAN.</p>
            <div className="juba-ff-scenario-grid">
              {tools.map(([Icon, label, desc, href]) => (
                <Link href={href} key={label}>
                  <Icon />
                  <strong>{label}</strong>
                  <span>{desc}</span>
                  <ArrowRight />
                </Link>
              ))}
            </div>
          </div>

          <div className="juba-ff-coach-card">
            <div className="juba-ff-coach-head"><div><TrendingUp /><strong>What JUBA LISAN tracks</strong></div><span>Real progress</span></div>
            {['CEFR level', 'Streak & XP', 'Lessons completed', 'Vocabulary progress'].map((label) => (
              <div className="juba-ff-score" key={label}>
                <span>{label}</span>
                <i><em style={{ width: '100%' }} /></i>
              </div>
            ))}
            <div className="juba-ff-intelligence">
              {intelligence.map(([Icon, title, desc]) => (
                <div key={title}><Icon /><span><strong>{title}</strong>{desc}</span></div>
              ))}
            </div>
            <Link href="/dashboard" className="mt-5 inline-flex items-center gap-2 text-sm font-bold">Open your dashboard <ArrowRight className="h-4 w-4" /></Link>
          </div>
        </div>
      </div>
    </section>
  )
}
