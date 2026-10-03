import type {ReactNode} from 'react'
import CompetitionStandings from '@/components/games/CompetitionStandings'

export default function GamesLayout({children}:{children:ReactNode}){
  return <>{children}<CompetitionStandings/></>
}
