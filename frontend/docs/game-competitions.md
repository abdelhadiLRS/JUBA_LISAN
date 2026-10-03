# Saved game results -> Leaderboard and Leagues

## Connection

There is one authoritative XP source: persisted `Progress.xp_earned`. Game completion already writes its validated XP to Progress. The competition API sums those rows by StudyPlan target language and date period. The frontend must not add the game result's XP to rankings locally or send another award request.

`EducationalGameSession` emits `markLearningProgressUpdated()` only after the server accepts completion. The new `CompetitionStandings` component subscribes to that event and reads `/api/leaderboard` and `/api/leagues/current`. It is mounted below the game content on all `/games` routes and on the Dashboard. Thus the saved round result and fresh rankings are visible on the same page. Events also propagate between open tabs through the existing BroadcastChannel/storage implementation. Returning to a visible tab refreshes standings. Refresh responses use generation guards so older requests cannot overwrite newer XP.

The panel uses the current active language, with daily/weekly/monthly/all-time leaderboard selection, ten-row pagination, an independently returned personal rank, the current league division and week dates. The personal league rank is shown even outside the top ten. Missing data remains empty, not padded with fictional participants. Fetch errors do not change the saved game result.

## Enrollment

Viewing standings or completing a game never enrolls someone automatically. `Join league` explicitly calls the existing `/api/leagues/join` endpoint with only `target_language`, after visible public-profile participation information. Repeat clicks are locked. XP already saved for this week and language counts on enrollment, including earlier games. A learner must join again for each new weekly season; their latest resulting tier carries forward.

League progression remains the backend's persisted rollover rule: the first enrollment in a new week finalizes expired seasons and assigns promotions/demotions. This connection adds no second XP ledger, automatic enrollment, scheduled rollover or fake rank animation. Leaderboard XP includes other learning activity and rewards as well as games; active-plan game totals can differ from language-wide competition totals because archived plans also count for competition.

## Tests and deployment

`backend/tests/test_game_competitions.py` exercises real memory session completion, Progress persistence, leaderboard/league agreement, replay rejection, unfinished and invalid games, pre-enrollment XP and language isolation. It reads server-owned test solutions without mutating answers or awarding points manually.

`frontend/src/components/games/CompetitionStandings.test.tsx` covers event-driven refresh, explicit enrollment, read errors, stale responses and period changes. These tests were added but not run in the writing environment, which lacks project dependencies and has no internet access. TypeScript build and browser verification remain pending.

Deploy with the previously added Alembic migration `0065_leagues` applied. The registered competition API and authenticated progress/game API must both be available. Existing LearningProgress events do not carry language or XP payloads; components intentionally re-read authoritative current-language data.

Remaining presentation limitations: Arabic/English panel copy only, no integrated season-history view, no countdown timer, no continuous polling for other players' scores, and no opt-out API. Refresh or return to the tab to retrieve other players' latest standings.
