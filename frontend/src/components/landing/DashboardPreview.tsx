import Link from 'next/link'
import { BookOpen, Target, CheckCircle2, ArrowRight, Sparkles, TrendingUp } from 'lucide-react'
interface DashboardPreviewProps { t:(key:string)=>string }

const dashboardAreas = [
  ['dashboardCurrentLanguage','dashboardCurrentLanguageDesc'],
  ['dashboardStudyPlan','dashboardStudyPlanDesc'],
  ['dashboardLearningProgress','dashboardLearningProgressDesc'],
  ['dashboardAdaptiveSteps','dashboardAdaptiveStepsDesc'],
] as const

export function DashboardPreview({t}:DashboardPreviewProps){
 return <section className="juba-funfluent-dashboard py-20 sm:py-24">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
   <div className="juba-ff-section-head">
    <span className="juba-ff-section-tag"><Sparkles className="mr-1 inline h-3.5 w-3.5"/>{t('dashboardSectionLabel')}</span>
    <h2>{t('dashboardPreviewTitle')}</h2>
    <p>{t('dashboardPreviewSubtitle')}</p>
   </div>
   <div className="juba-ff-dashboard-card" aria-label={t('dashboardOverviewLabel')}>
    <div className="juba-ff-dashboard-real-grid">
      {dashboardAreas.map(([title,desc],i)=>{
        const Icon=[Target,BookOpen,TrendingUp,CheckCircle2][i]
        return <article className="juba-ff-real-panel" key={title}>
          <div className="juba-ff-real-icon"><Icon /></div>
          <div><strong>{t(title)}</strong><p>{t(desc)}</p></div>
        </article>
      })}
    </div>
    <div className="juba-ff-real-note" role="note">
      <span>{t('dashboardDataNote')}</span>
      <Link href="/dashboard" className="juba-ff-feature-link">{t('openDashboard')} <ArrowRight /></Link>
    </div>
   </div>
  </div>
 </section>
}

