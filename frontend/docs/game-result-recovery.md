# Recovering saved game results

A game completion POST can commit its XP/event and still lose its HTTP response. Retrying used to return `409` without showing the saved result. The client now performs a read-only confirmation through `GET /api/progress/game-session/{session_id}/result` after network failures, server errors, 409 conflicts or unreadable successful JSON responses.

The recovery request never awards XP, completes a session or creates a progress event. It requires the existing learner token and checks that the requester owns the session. Unknown/other-user sessions return 404; unfinished sessions or unavailable saved records return 409. Completed sessions remain recoverable after expiry or plan archival.

The response reads this session's recorded round XP, score and accuracy from GameProgressEvent. Cumulative stats, skills and total XP are current values for the original session's study plan, not a reconstructed historical snapshot. Skill deltas and newly-earned achievement details were not persisted in the old event schema, so recovery returns empty `skill_results` and `new_achievements` rather than inventing them. Earned achievements remain available in aggregate `achievements`.

Successful recovery uses the same existing UI completion flow: the real result is displayed and the learning-progress update event refreshes Leaderboard/Leagues without a second award. Validation, permission, expiration and rate-limit errors are not turned into success. An inconclusive recovery preserves the original failure; the learner may retry. No automatic second POST occurs inside the recovery helper.

Added tests: eight frontend recovery cases and six backend read-only/security cases. Full Vitest, pytest, build, migration and browser checks were not run because project dependencies are unavailable in the writing sandbox and it has no internet access. Deployment requires the new registered result route in addition to the existing game and competition APIs. This change needs no database migration.
