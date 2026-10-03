import type { ReactNode } from 'react'
import ReferenceFeatures from './ReferenceFeatures'
import CompetitionStandings from '@/components/games/CompetitionStandings'
import LeagueMovement from '@/components/games/LeagueMovement'
import LeagueRiskAlert from '@/components/games/LeagueRiskAlert'

export default function DashboardLayout({children}:{children:ReactNode}){
  return <div className="reference-dashboard-route"><LeagueRiskAlert/>{children}<LeagueMovement/><CompetitionStandings/><ReferenceFeatures/></div>
}
