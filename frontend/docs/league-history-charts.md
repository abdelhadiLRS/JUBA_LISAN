# Interactive league history charts

`/leagues` now mounts `LeagueHistoryCharts`, backed by the authenticated `/api/leagues/history` endpoint. It uses the active learning language and fetches twelve previous enrolled seasons per page. `Load older seasons` fetches another page and re-reads the loaded window rather than appending potentially stale responses. A full last page only indicates that another page may exist, not an asserted historical total.

## Interactions

Three metric buttons switch between XP, personal rank and participated league tier. SVG points can be clicked or focused with Tab and activated with Enter/Space. Selecting a point changes an accessible season selector and a live detail panel with actual XP/rank/tier, week dates, reported participants, settlement state and persisted outcome. An expandable table provides the same raw data without requiring chart interaction.

The default filter includes settled seasons only. Users can include pending seasons; pending points use a distinct marker and dashed connecting segments, and their detail panel explicitly says values are not final. Final outcomes are shown only when the server reports finalized state and a recognized next tier. Switching language or refreshing uses generation guards so old requests cannot overwrite current data. Saved-progress events and returning to a visible tab refresh loaded history.

## Data semantics

XP and personal rank come from the history response's `current_user`, using persisted final results for finalized seasons and current server calculations for unfinalized seasons. Missing values are omitted from the chart and labelled unavailable, never coerced to zero. Legitimate zero earned XP stays zero. Tier is the division participated in, not a projected or resulting next tier. Rank one is best and appears higher on the plot.

Horizontal positions use actual UTC week-start dates, so missed enrollment weeks retain their time gaps. The connecting line summarizes the available enrolled seasons only: it does not imply a stored rank for intervening days or unplayed weeks. Single-point, empty, all-zero and unavailable-value series are handled explicitly. The reported participant total can reflect account eligibility/deletion filters in the existing API; it is not an immutable historical population snapshot.

The backend does not persist daily rank snapshots within each season. These charts therefore show weekly participation history, not invented intra-week trends. Expired seasons remain pending until the existing first-next-week-enrollment rollover runs. No background finalization or write is performed by viewing a chart.

## Verification

Eight Vitest cases cover chronological ordering/deduplication, pending filtering, missing versus zero values, participated tiers, actual time spacing, rank-axis direction, single/all-zero series and unavailable data. Full Vitest, build, browser and API integration checks were not run because project dependencies are unavailable in the code-writing environment, whose sandbox has no internet access.

The stylesheet is imported by the internal league component only; Landing Page files are unchanged. Arabic and English copy are included; full translation catalog coverage remains pending. Desktop/mobile SVG scrolling, keyboard points and the data table are implemented but still need real-browser verification. The chart shows the loaded history window and supports loading older pages; it makes no claim to have exhaustively fetched every season on first render.
