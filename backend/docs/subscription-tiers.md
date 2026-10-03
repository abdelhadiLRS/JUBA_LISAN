# Free, Go and Plus rollout

Product tier is independent of `monthly` / `yearly` billing interval.
Prices are EUR: Free 0, Go 7.99/month or 79.99/year, Plus 14.99/month or 149.99/year.
A server-issued, one-use seven-day Go trial needs no payment card. Registration
continues to use the existing freemium trial fields; effective trial access is Go,
not unlimited. Explicit trial start is `POST /api/subscriptions/trial`.

## Deployment setup required

Set these four public product references in deployment configuration (not client code):

```
STRIPE_PRICE_GO_MONTHLY=price_...
STRIPE_PRICE_GO_YEARLY=price_...
STRIPE_PRICE_PLUS_MONTHLY=price_...
STRIPE_PRICE_PLUS_YEARLY=price_...
```

They are loaded by `ProductSettings` from the same environment/.env as core settings.
No Stripe products, prices or keys were created or changed by this implementation.
Create EUR recurring prices for the exact amounts above and configure the billing
portal to allow only these products. Keep legacy `STRIPE_PRICE_MONTHLY` and
`STRIPE_PRICE_YEARLY` references for existing subscriber webhook recognition.
Checkout validates active status, amount, currency and recurring interval before
returning a payment URL. Checkout never adds another card-based trial.

Run Alembic through `0067_feature_usage` before serving traffic. Migration0066
preserves legacy paid subscribers as Plus. Inactive payment states resolve to Free;
cancel-at-period-end retains paid access while Stripe remains active. The stored
billing product is historical; `/me.tier` is the effective entitlement.

## Account-wide allowances

| Feature | Free | Go | Plus | Period / unit |
|---|---:|---:|---:|---|
| Tutor messages |5|40|120|day / requests|
| New lessons |1|5|15|day / lessons|
| New reading exercises |2|15|40|week / requests|
| New listening exercises |2|10|25|week / requests|
| AI-generated flashcards |20|150|400|week / cards|
| Translation + standalone correction |5|30|100|day / requests|
| Voice |300|3600|10800|month / seconds|
| Standalone TTS |300|1800|5400|month / seconds|

Voice session maxima: 300 / 900 / 1800 seconds. UTC day, Monday-based week and
calendar month boundaries, with no rollover. All learning languages share counters.
Chat input max2000 characters, translation/correction max1000, generated cards max20.
Manual card creation/import and cached content review are not AI generation.
XP and competition rules are unchanged.

## APIs and integration

- `GET /api/subscriptions/catalog`: public prices, request caps and product limits.
- `GET /api/subscriptions/me`: effective tier, used/reserved/remaining/reset values.
- `GET /api/freemium/status`: legacy scalar fields plus the new feature map.
- `POST /api/subscriptions/correct`: independent text correction, sharing translation quota.
- `/api/translate`, both tutor chat routes, new lesson persistence, card generation/from-word,
  reading/listening generation, voice WebSocket and `/api/tts` use durable reservations.
- Reading/listening attempts/replay and saved history/audio do not consume generation quota.
- Voice charges server session elapsed seconds only when at least one delivered user
  turn has nonempty assistant text, audio and completion. Greeting-only, empty-answer,
  failed-only and text-only sessions release the reservation. Idle time in an otherwise
  successful session counts as session time. Per-session duration caps bound charges.
- TTS measures WAV/MP3 duration, rounded up to seconds. If it exceeds remaining quota,
  no audio is delivered and quota is released. `mutagen` is now a backend dependency.
- Settings usage page: `/settings/subscription`; banners include paid tiers and trial.

`STRIPE_ENABLED=false` intentionally preserves unmetered self-hosted use. Public
catalog says `metered=false`; numeric hosted allowances are not local restrictions.

## Concurrency / recovery limitations to validate

Database conditional updates reserve capacity before expensive work. Pending
reservations have a two-hour lease; terminal state and counters settle transactionally.
A crashed worker's hold is reclaimed on the next reservation for the same bucket.
The generation coordination lock is optional Redis with a five-minute lease; without
Redis duplicate generation can occur but numeric quota caps remain enforced.
Content persistence and usage settlement are separate transactions. An operational
failure between them requires reconciliation; no distributed exactly-once claim is made.
Billing initiation still needs end-to-end concurrency verification against Stripe.

## Verification status

New and migrated tests are committed, but build, pytest, Vitest, Alembic execution,
Stripe delivery and browser/device validation have not run in the current environment.
Static source review is not a passing test suite. Existing auth/legal/translation copy
and billing CTA consumers outside PricingSection need a final full integration audit.
