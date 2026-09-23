import { Globe, Target, Compass, MessageSquare, TrendingUp, Sparkles, BrainCircuit, BriefcaseBusiness, Plane, Trophy, FileText, Mic, RotateCcw } from 'lucide-react'

interface LearningExperienceProps { t: (key: string) => string }

export function LearningExperience({ t }: LearningExperienceProps) {
  const steps = [
    [Globe, 'step1Title', 'step1Desc', '🌍'], [Target, 'step2Title', 'step2Desc', '🎯'],
    [Compass, 'step3Title', 'step3Desc', '🧭'], [MessageSquare, 'step4Title', 'step4Desc', '🗣️'],
    [TrendingUp, 'step5Title', 'step5Desc', '🏆'],
  ] as const
  const scenarios = [
    [Plane, 'Travel', 'Airport, hotel & real-world conversations'], [BriefcaseBusiness, 'Business', 'Meetings, interviews & workplace English'],
    [MessageSquare, 'Daily Life', 'Natural conversations for everyday life'], [Trophy, 'Exams', 'Focused CEFR & exam practice'],
  ] as const
  const intelligence = [
    [BrainCircuit, 'Adaptive AI Coach', 'Your next activity changes with your progress and goals.'],
    [FileText, 'Learn From Anything', 'Turn text and notes into lessons, vocabulary and quizzes.'],
    [RotateCcw, 'Smart Review', 'Bring words and concepts back at the right moment.'],
  ] as const

  return (
    <section className="juba-funfluent-experience py-20 sm:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="juba-ff-section-head">
          <span className="juba-ff-section-tag"><Sparkles className="mr-1 inline h-3.5 w-3.5" />The learning journey</span>
          <h2>{t('experienceTitle')}</h2>
          <p>{t('experienceSubtitle')}</p>
        </div>
        <div className="juba-ff-steps">
          {steps.map(([Icon,title,desc,art],i) => (
            <article key={title} className={`juba-ff-step step-${i}`}>
              <div className="juba-ff-step-number">{String(i+1).padStart(2,'0')}</div>
              <div className="juba-ff-step-art">{art}</div>
              <Icon className="juba-ff-step-icon" />
              <h3>{t(title)}</h3><p>{t(desc)}</p>
            </article>
          ))}
        </div>
        <div className="juba-ff-practice">
          <div className="juba-ff-practice-copy">
            <span className="juba-ff-section-tag">Practice for real life</span>
            <h3>Use your language where it matters.</h3>
            <p>Choose a situation, speak with JUBA AI, get instant feedback, then try again until it feels natural.</p>
            <div className="juba-ff-scenario-grid">
              {scenarios.map(([Icon,label,desc]) => <div key={label}><Icon /><strong>{label}</strong><span>{desc}</span></div>)}
            </div>
          </div>
          <div className="juba-ff-coach-card">
            <div className="juba-ff-coach-head"><div><Mic /><strong>Speaking feedback</strong></div><span>82% overall</span></div>
            {['Pronunciation','Grammar','Vocabulary','Fluency'].map((label,i) => <div className="juba-ff-score" key={label}><span>{label}</span><b>{[91,84,88,79][i]}%</b><i><em style={{width:`${[91,84,88,79][i]}%`}} /></i></div>)}
            <div className="juba-ff-intelligence">
              {intelligence.map(([Icon,title,desc]) => <div key={title}><Icon /><span><strong>{title}</strong>{desc}</span></div>)}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
