import { Flame, Award, BookOpen, Target, CheckCircle2, ArrowRight, Sparkles } from 'lucide-react'
interface DashboardPreviewProps { t:(key:string)=>string }
export function DashboardPreview({t}:DashboardPreviewProps){
 const metrics=[[Flame,'14 Days','Streak'],[Award,'2,450 XP','XP earned'],[BookOpen,'420','Words learned'],[Target,'B2','Current level']] as const
 const skills=[['Speaking',82],['Listening',90],['Grammar',76],['Vocabulary',88]]
 return <section className="juba-funfluent-dashboard py-20 sm:py-24">
  <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
   <div className="juba-ff-section-head"><span className="juba-ff-section-tag"><Sparkles className="mr-1 inline h-3.5 w-3.5"/>Your learning world</span><h2>{t('dashboardPreviewTitle')}</h2><p>{t('dashboardPreviewSubtitle')}</p></div>
   <div className="juba-ff-dashboard-card">
    <div className="juba-ff-metric-row">{metrics.map(([Icon,value,label])=><div className="juba-ff-metric" key={label}><Icon/><span><b>{value}</b><small>{label}</small></span></div>)}</div>
    <div className="juba-ff-dashboard-grid">
     <div className="juba-ff-today"><div className="juba-ff-panel-title"><strong>Today’s adventure</strong><span>2 / 3 complete</span></div>
      {[['Business vocabulary','15 expressions'],['Conditional sentences','Grammar quiz'],['Voice conversation','10 min with JUBA AI']].map(([a,b],i)=><div className={`juba-ff-task task-${i}`} key={a}><div className="juba-ff-task-icon">{i<2?'✓':'▶'}</div><span><strong>{a}</strong><small>{b}</small></span><b>{i<2?'+50 XP':'Start'}</b></div>)}
     </div>
     <div className="juba-ff-skill-panel"><strong>Skills growing</strong>{skills.map(([label,value])=><div className="juba-ff-dashboard-score" key={label}><span>{label}</span><b>{value}%</b><i><em style={{width:`${value}%`}}/></i></div>)}<div className="juba-ff-level-badge">CEFR · Upper Intermediate <b>B2</b></div></div>
    </div>
   </div>
  </div>
 </section>
}