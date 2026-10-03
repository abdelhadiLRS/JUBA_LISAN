import type {ReactNode} from 'react'
import CompetitionStandings from '@/components/games/CompetitionStandings'
import LeagueMovement from '@/components/games/LeagueMovement'
import LeagueRiskAlert from '@/components/games/LeagueRiskAlert'

export default function GamesLayout({children}:{children:ReactNode}){
  return <><LeagueRiskAlert/>{children}<LeagueMovement/><CompetitionStandings/></>
}
