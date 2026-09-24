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

        <div className="juba-ff-steps grid grid-cols-1 gap-3 md:grid-cols-5 md:gap-0">
          {steps.map(([Icon, title, desc, art, href], i) => (
            <Link
              href={href}
              key={title}
              className="group relative flex min-h-[230px] flex-col border-b border-[#dce7dc] px-5 py-6 transition-colors md:min-h-[250px] md:border-b-0 md:border-r md:last:border-r-0 md:px-6"
            >
              <div className="mb-7 flex items-center justify-between">
                <span className="text-[11px] font-black tracking-[0.18em] text-[#39751d]">
                  {String(i + 1).padStart(2, '0')}
                </span>
                <Icon className="h-5 w-5 text-[#39751d] transition-transform duration-200 group-hover:translate-x-1" aria-hidden="true" />
              </div>
              <div className="mb-5 text-[10px] font-black tracking-[0.2em] text-[#718078]">{art}</div>
              <h3 className="max-w-[180px] text-[20px] font-black leading-[1.05] tracking-[-0.035em] text-[#183022]">
                {t(title)}
              </h3>
              <p className="mt-3 max-w-[190px] text-[12px] leading-5 text-[#617068]">{t(desc)}</p>
              <span className="mt-auto inline-flex items-center gap-1 pt-5 text-[10px] font-black uppercase tracking-[0.16em] text-[#39751d]">
                Explore <ArrowRight className="h-3 w-3 transition-transform duration-200 group-hover:translate-x-1" />
              </span>
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
            <div className="juba-ff-real-progress-list">
              {[
                ['CEFR level', 'Your current level is shown from your account.'],
                ['Streak & XP', 'Daily activity and XP are calculated from your learning history.'],
                ['Lessons completed', 'Completed lessons are reflected in your study progress.'],
                ['Vocabulary progress', 'Vocabulary practice and review contribute to your progress.'],
              ].map(([label, desc]) => (
                <div className="juba-ff-real-progress-item" key={label}>
                  <span className="juba-ff-real-progress-dot" aria-hidden="true" />
                  <span><strong>{label}</strong><small>{desc}</small></span>
                </div>
              ))}
            </div>
            <p className="mt-3 text-xs leading-5 opacity-75">
              No sample progress values are shown here. Open the dashboard to view the values calculated for your account.
            </p>
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
