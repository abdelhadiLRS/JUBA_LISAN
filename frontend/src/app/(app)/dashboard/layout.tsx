import type { ReactNode } from 'react'
import ReferenceFeatures from './ReferenceFeatures'
import CompetitionStandings from '@/components/games/CompetitionStandings'

export default function DashboardLayout({children}:{children:ReactNode}){
  return <div className="reference-dashboard-route">{children}<CompetitionStandings/><ReferenceFeatures/></div>
}
