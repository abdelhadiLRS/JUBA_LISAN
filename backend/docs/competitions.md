# Leaderboard and Leagues API

All endpoints require the existing Bearer token and an active learner account. Administrators are rejected. OpenAPI response schemas are available in `/docs` after deployment.

## Endpoints

- `GET /api/leaderboard?period=week&limit=20&offset=0`: real XP ranking. `period` accepts `day`, `week`, `month`, `all`.
- `GET /api/leagues/current?limit=20&offset=0`: current weekly league, membership, standings, expiry and available tiers. Optional `tier=bronze|silver|gold|sapphire|ruby|diamond` selects a division.
- `POST /api/leagues/join` with `{}`: explicitly opt in to the active language's current weekly season. Idempotent. Optional body: `{"target_language":"fr-FR"}`. Extra fields, including XP, user ID and tier, are rejected.
- `GET /api/leagues/history?limit=12&offset=0`: the requesting learner's previous seasons, with final results once rolled over.

All GET endpoints accept optional `target_language`; it must be a language already owned by the requester. Omission uses their active language. Standings pagination accepts `limit=1..100`; history accepts `1..52`. Both accept `offset=0..100000`.

## Real-data and privacy contract

Only explicitly enrolled learners appear in competition standings. No fake profiles, filler opponents or randomized XP are created. GET requests never enroll a learner. The current league returns `joined=false`, empty standings and `season_id=null` when no season exists.

Scores are sums of nonnegative persisted `Progress.xp_earned`, including reward XP, joined through `StudyPlan.target_language`. Archived plans count, so regenerating a plan does not erase earned points. Languages remain separate, including locale variants. Future-dated progress is excluded. League scores cover the complete week, including points earned before joining that week. Dates use the server's date buckets, matching the existing progress API; deploy the server in UTC to match the advertised UTC midnight expiry.

Public entries expose only user ID, username, display name, avatar, XP and rank. No email, auth, subscription, learning goals or personal biography is returned. Inactive accounts and administrators are excluded. An enrolled learner remains opted in for that language's global leaderboard across periods; weekly participation requires joining each new season. This initial API does not include an opt-out endpoint.

Ranks use SQL `RANK()` on XP, so equal scores share a rank (1, 1, 3). User ID provides stable pagination only and never breaks a competition tie. `current_user` is returned independently of the requested page and is null when not enrolled in the selected ranking.

## Weekly progression

Seasons run Monday through Sunday. Each language has one season, with independent tier divisions, not fabricated 30-person groups. First enrollment starts in Bronze. Later enrollment uses the last finalized membership's resulting tier, even after missed weeks.

At the first POST join for a new week, all expired, unfinalized seasons in that language are finalized transactionally. Final XP/rank and resulting tier are persisted. These historical competition results then remain unchanged even if old progress changes. There is no background scheduler: an expired season is visibly `finalized=false` until rollover is triggered by a join.

With at least five eligible participants in a division, the top floor(N/5), at least one, rank positions promote one tier, provided XP is positive. Positions strictly greater than N-floor(N/5) demote one tier. Shared ranks are never split; ties can make promoted/demoted counts differ from 20%. Smaller divisions retain their tier. Bronze and Diamond are the lower and upper bounds. No XP, gem or subscription rewards are granted by this API.

Unique constraints enforce one season per language/week and one membership per learner/season. PostgreSQL uses season row locks for serialized rollover; SQLite uses an atomic write before rollover. Conflict-safe inserts make repeat enrollment idempotent. These concurrency paths still need integration verification on both deployment databases.

## Deployment and verification

Migration `0065_leagues` extends the current merged Alembic head. Existing application startup runs `alembic upgrade head`; manual deployments can run that command in `backend/` before serving the API. The migration adds only two competition tables and a progress-date index, without changing existing XP or accounts.

Regression suite: `pytest tests/test_leagues.py` from `backend/`. Covers auth/admin guards, real XP, archived plans, language isolation, ties, pagination, client-points rejection, membership idempotency, period rules and persisted rollover snapshots. Full API tests and migration execution require the repository dependencies and were not run in the code-writing environment. Frontend wiring is a separate follow-up; this change is the real backend API, not a claim that dashboard league UI is already connected.
