# Automatic league demotion warnings

In-app banners now appear on `/leagues`, `/games` (including nested game routes) and `/dashboard`. The component reads the existing authenticated league endpoint; it never writes XP, changes membership or performs promotion/demotion.

## Automatic checks

The visible active page checks on mount, every sixty seconds, after saved learning-progress events and when returning from a hidden tab. Hidden tabs do not poll. Requests are aborted on replacement/unmount and have a fifteen-second timeout. Generation guards reject stale responses after account/language changes. A failed check removes the prior banner rather than presenting old risk as current. No background worker, email, push permission, operating-system notification or ClickUp message is created. The app must be open on one of these pages for alerts to appear.

## Risk rules

Warnings require an enrolled learner with a valid personal rank, an unfinalized and unexpired season, at least five eligible division participants, and a tier above Bronze. Unknown/invalid data produces no warning. Diamond learners can still be at demotion risk.

`danger` means the existing server-aligned projection classifies the rank as demotion. `near` means rank is at least the last safe rank minus one, without already being in a promotion position. For ten participants the last safe shared rank is eight: ranks seven/eight receive proximity warnings and ranks greater than eight receive danger warnings. Equal ranks are not split. The banner explains the cutoff and makes no promise about the final outcome.

A deadline note appears with forty-eight hours or less remaining. Dismissal is kept in component memory for the same season/severity/deadline class; minor rank fluctuations do not reopen it. A higher severity, entering the closing window or a new season can show a new warning. Reloading/remounting resets dismissal; this initial implementation intentionally does not persist alert preferences or notification history.

## Presentation

Arabic/English copy, textual near/danger indicators, differentiated neutral-amber/red surfaces, personal rank and cutoff, links to real practice and the league page, and a keyboard-accessible dismiss button. The wrapper uses a polite live region instead of audio alarms. Alerts are provisional; settlement still happens through the existing first-next-week-enrollment lifecycle.

## Verification

Eight Vitest cases cover cutoffs, ties, Bronze/small-group exemptions, expiry/finalization, escalation signatures, safe ranks and invalid data. Tests are added, not executed in the project environment. Full build, API integration and browser checks remain pending because dependencies are unavailable and the writing sandbox has no internet access.
