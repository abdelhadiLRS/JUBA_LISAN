# Visible league movement

The new `/leagues` page combines a movement visualization with real enrollment and standings. The same movement panel appears below game content and on the Dashboard, with an explicit link to the league page.

## Current-week projections

The six-tier ladder marks the current division. The learner's panel shows their rank, XP, eligible participant total and projected destination tier, always labelled provisional. Standings rows have textual up/down/stay indicators plus green or warm-red surfaces; movement is not communicated by color alone. A visible legend explains top/bottom cutoffs. League pagination and a `View bottom ranks` control expose the demotion area beyond the initial top ten.

Projection rules mirror the existing server `next_tier` helper: five eligible participants minimum, floor(N/5) rank slots, positive XP for promotion, no movement beyond Bronze/Diamond. SQL ranks are shared at equal XP, so tied learners are never split using display order or IDs. Zone labels are effective movement labels: a Diamond leader and Bronze bottom learner are marked Stay because they cannot move beyond the tier bounds.

## Confirmed outcomes

Previous seasons are read from the existing history API. A season is shown as promoted, demoted or retained only if `finalized=true` and a recognized persisted `next_tier` exists. Unsettled seasons show `Awaiting settlement`, never a predicted decision disguised as confirmed. The original/current tier and persisted resulting tier are shown together.

The backend still finalizes expired seasons at the first new-week enrollment, not through a scheduler. The page states this explicitly. No XP, membership, promotion or demotion is written by viewing projections/history.

Saved learning-progress events refresh the projections and history. Returning to a visible tab also refreshes. Requests use generation guards against stale responses. UI copy covers Arabic and English, with RTL layouts and keyboard focus indicators.

## Verification and limitations

Eight Vitest rule cases cover minimum division size, positive XP, cutoff boundaries, ties, tier bounds and persisted outcomes. Full build, Vitest, browser/device and API integration checks were not run: dependencies are unavailable in the writing sandbox, which has no internet access. Isolated JavaScript parity checks may validate the projection helper independently, but are not an integration run.

The current projection is derived client-side from authoritative ranks/XP/totals using the documented server rule. Any future backend rule change must update this helper and its tests. History shows the latest eight seasons, without a dedicated history pager. This change adds no scheduled rollover or continuous opponent polling.
