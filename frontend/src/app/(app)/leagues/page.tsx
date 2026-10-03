import CompetitionStandings from '@/components/games/CompetitionStandings'
import LeagueMovement from '@/components/games/LeagueMovement'
import LeagueHistoryCharts from '@/components/games/LeagueHistoryCharts'

export default function LeaguesPage(){
  return <main><LeagueMovement/><LeagueHistoryCharts/><CompetitionStandings/></main>
}
