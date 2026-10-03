# Stabilization batch 1

Approved fixes applied to landing billing policy and dashboard goal request lifecycle. No new games or competition mechanics were added.

## Billing

Pricing now reads current public config before exposing registration/payment actions. Closed registration routes visitors to login. Disabled Stripe does not show purchasable paid plans. Active/trialing subscribers route to Dashboard instead of duplicate checkout. Unknown subscription status remains blocked rather than interpreted as no subscription. Invalid/unavailable prices cannot start payment; the server config is checked again before the checkout POST. A ref lock prevents double checkout submissions.

Subscription reads use the centralized auth API, coalesce only current in-flight reads for the same token, and do not indefinitely cache failed or resolved results. Strict state reads reject invalid/unavailable account data. The legacy boolean helper remains a non-payment convenience read and catches failure as false.

The trial-duration subtitle/badge uses verified configured trial days. The existing free-feature descriptions/comparison rows still contain authored translation copy such as a seven-day freemium description; complete alignment with freemium and plan-entitlement config remains pending. This patch is not a full billing entitlement audit. Checkout destination is required to be an HTTPS URL returned by the backend; strict payment-host allowlisting and actual checkout/webhook tests remain pending.

## Dashboard goals

The new useReferenceFeatures hook invalidates old reads when a save begins. A pending GET can no longer overwrite the PUT result from the same request generation. Progress refreshes arriving during a write are coalesced and processed when the lock is released. Language changes invalidate old payloads and read the new context after any pending save settles. Successful server writes still emit progress refresh events; unsuccessful writes retain the displayed target and surface an error.

Goal editing, earned achievements, measurable next achievement, actual XP history and accessible activity values remain. Arabic direction checks now accept Arabic locale prefixes. This does not finish the larger Dashboard visual integration or translation-catalog migration.

## Added tests

Nine pricing-policy cases, four subscription-state cases, four pricing-component cases and six dashboard-hook cases. The tests cover registration/payment guards, unknown subscription state, retryable subscription reads, stale GET/PUT races, deferred progress refresh, duplicate writes, language changes, failed writes and invalid targets. These are source regression tests, not a claim that Vitest or the application build passed.

## Verification and remaining priorities

The coding sandbox lacks repository dependencies and internet access. Full TypeScript, Vitest, Next build, backend tests, migration execution and browser/device verification were not performed. GitHub CI workflow definitions exist, but current run results were not retrieved with the available connected tools. No claim is made about CI passing.

Still pending from the approved readiness plan: authoritative next-lesson precedence and plan stale-request handling, server-side game-move validation/XP anti-abuse policy, migrated game/session tests, database concurrency validation, end-to-end learner flow, visual Dashboard integration, complete i18n and league/privacy lifecycle improvements. This first batch fixes two bounded areas, not all launch blockers.
