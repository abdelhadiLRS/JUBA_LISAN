import CompetitionStandings from '@/components/games/CompetitionStandings'
import LeagueMovement from '@/components/games/LeagueMovement'
import LeagueHistoryCharts from '@/components/games/LeagueHistoryCharts'
import LeagueRiskAlert from '@/components/games/LeagueRiskAlert'

export default function LeaguesPage(){
  return <main><LeagueRiskAlert/><LeagueMovement/><LeagueHistoryCharts/><CompetitionStandings/></main>
}
