# Nine approved subscription integration repairs

Applied to main after the source review of fcd49e2c621475348b9f329e63da6e6a84d9aaec.
No live Stripe prices, products, keys, subscriptions or customer records were changed.

## Repair mapping

1. VisitorTranslator uses apiFetch and requires account sign-in. Input counter and
   validation are1000 characters. Guests see a login action rather than a failing API call.
2. register reads validated tier/interval (including legacy plan links), passes them
   to onboarding, and retains a same-tab selection. Onboarding saves language/goals,
   then routes paid selections to the common catalog for explicit confirmation.
   No signup action silently starts payment or grants paid access.
3. SubscriptionPlanButtons and PaywallBanner no longer initiate interval-only Plus
   checkout or display independent legacy prices. They link to the unified catalog.
   Catalog restores requested tier/interval and uses server prices for final Checkout.
4. Chat reads real account quota, including paid and Go-trial users. Structured402
   shows reset/plan actions without hiding saved history. Input max2000 matches the
   server. A failed turn restores its input and removes provisional chat bubbles.
5. Reservation.commit(db) flushes content, updates reservation/usage on the same
   connection, then commits once. Chat saves both messages only on successful completion;
   lessons/exercises, generated cards and legacy tutor counters use this path.
   Card actual count is selected before charging, not after commit. Existing reading/
   listening services are adapted with session-scoped commit callbacks so their saved
   exercise and charge share one transaction. Post-commit response/refresh errors do
   not refund saved content. Filesystem audio writes are not a distributed DB/filesystem
   transaction; an orphaned MP3 from a rolled-back exercise remains a housekeeping issue.
6. FastAPI binds an injectable session factory for request/task scope. Short quota
   sessions and owned streaming/background sessions use it. Tests override BOTH get_db
   and the shared factory; background work captures its factory explicitly before
   request dependencies close. No request session is reused after its lifetime.
7. Reading/listening finally blocks release generation locks even when reservation
   cleanup fails; cleanup failures are logged and pending holds retain their expiry.
8. BillingIntent, FeatureUsage and FeatureReservation are imported by app.models,
   allowing clean-process Alembic metadata discovery. No new schema migration is
   needed for these registration changes.
9. Delayed Checkout retries first retain the exact persisted request/key so an accepted
   but uncertain Stripe reply can be recovered. ONLY Stripe's explicit expires_at
   validation rejection permits serialized intent renewal and a new key/fresh31minute
   creation window. Ambiguous timeouts and unrelated validation errors do not rotate.

## Verification performed here

- 22 selection/legacy-link/session-storage assertions passed against an exact copied
  TypeScript helper with only type annotations removed for Node execution.
- 17 modified Python source files passed compile() syntax checks without importing
  project dependencies.
- Exact-source Reservation.commit and background cleanup functions passed isolated
  stub checks for same-session settlement ordering, rollback after failed settlement,
  and lock release after cleanup failure. These are not database integration tests.
- Read-only static review of the changed quota/persistence and UI/API contracts found
  no additional high-confidence critical defect in the reviewed scope.

## Tests committed, NOT executed in this environment

- Metered translation HTTP route reaches the same injected usage database; exhaustion,
  failed generation, authentication and character boundaries.
- Successful content/usage atomic commits, settlement rollback and no post-commit refund.
- Legacy-service commit callback atomicity, background cleanup failure and fresh-process
  Alembic metadata registration.
- Checkout delayed-expiry rejection recovery and uncertain reply key preservation.
- Product-selection validation and translator authentication/402/input behavior.

The sandbox has no internet access and lacks project dependencies, pytest, npm and
TypeScript compiler. Full build, pytest, Vitest, PostgreSQL/SQLite/Redis integration,
Alembic execution, live Stripe and browser/device validation remain required before
claiming production readiness. GitHub Actions results were not retrieved.

## Remaining work outside these nine fixes

The original numeric tier limits/prices and self-hosted unmetered mode are unchanged.
Seven-day trial issuance still has legacy auth settings/copy outside this repair batch;
full locale/legal audit remains. Multi-worker webhook-vs-Checkout activation races and
voice binary turn association require integration stress tests. Optional Redis
coordination can permit duplicate generation when absent, while DB numeric quota caps
remain enforced. Do not describe this commit batch as a fully tested deployment.
