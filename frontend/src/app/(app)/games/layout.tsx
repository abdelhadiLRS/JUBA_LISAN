import type {ReactNode} from 'react'
import CompetitionStandings from '@/components/games/CompetitionStandings'
import LeagueMovement from '@/components/games/LeagueMovement'

export default function GamesLayout({children}:{children:ReactNode}){
  return <>{children}<LeagueMovement/><CompetitionStandings/></>
}
