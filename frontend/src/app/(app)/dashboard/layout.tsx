import type { ReactNode } from 'react'
import ReferenceFeatures from './ReferenceFeatures'
import CompetitionStandings from '@/components/games/CompetitionStandings'
import LeagueMovement from '@/components/games/LeagueMovement'

export default function DashboardLayout({children}:{children:ReactNode}){
  return <div className="reference-dashboard-route">{children}<LeagueMovement/><CompetitionStandings/><ReferenceFeatures/></div>
}
