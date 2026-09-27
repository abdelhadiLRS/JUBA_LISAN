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
 return <section className="juba-funfluent-dashboard juba-jl-dashboard-preview py-20 sm:py-24">
      <style>{".juba-jl-dashboard-preview{background:#f7fff3;color:#242424;font-family:'Nunito Sans','Noto Sans Arabic',system-ui,sans-serif}.juba-jl-dashboard-preview .juba-ff-section-head{text-align:center;max-width:760px;margin:0 auto 34px}.juba-jl-dashboard-preview .juba-ff-section-tag{color:#46a302;font-weight:900}.juba-jl-dashboard-preview .juba-ff-section-head h2{color:#242424;font-weight:950;letter-spacing:-.06em}.juba-jl-dashboard-preview .juba-ff-section-head p{color:#777}.juba-jl-dashboard-preview .juba-ff-dashboard-card{border:2px solid #e5e5e5!important;border-radius:24px!important;background:#fff!important;box-shadow:0 5px 0 rgba(0,0,0,.07)!important;padding:22px!important}.juba-jl-dashboard-preview .juba-ff-dashboard-real-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.juba-jl-dashboard-preview .juba-ff-real-panel{display:flex;gap:14px;padding:18px;border:2px solid #e5e5e5;border-radius:18px;background:#fff}.juba-jl-dashboard-preview .juba-ff-real-icon{width:44px;height:44px;display:grid;place-items:center;flex:none;border-radius:50%;background:#efffe6;color:#46a302}.juba-jl-dashboard-preview .juba-ff-real-panel strong{color:#242424;font-weight:900}.juba-jl-dashboard-preview .juba-ff-real-panel p{color:#777;margin-top:4px;line-height:1.5}.juba-jl-dashboard-preview .juba-ff-real-note{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-top:16px;padding-top:16px;border-top:2px solid #e5e5e5;color:#777}.juba-jl-dashboard-preview .juba-ff-feature-link{color:#46a302;font-weight:900}@media(max-width:640px){.juba-jl-dashboard-preview .juba-ff-dashboard-real-grid{grid-template-columns:1fr}.juba-jl-dashboard-preview .juba-ff-real-note{align-items:flex-start;flex-direction:column}}"}</style>
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

