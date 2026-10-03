# Free, Go and Plus

Product tier is independent of monthly/yearly billing interval. Prices are EUR:
Free0, Go7.99/month or79.99/year, Plus14.99/month or149.99/year.
A one-use seven-day Go trial requires no card and uses server-owned trial dates.
Registration's existing trial resolves to Go, never unlimited. Explicit trial start
is `POST /api/subscriptions/trial`.

## Deployment requirements

Configure four EUR recurring prices in the deployment environment:

```
STRIPE_PRICE_GO_MONTHLY=price_...
STRIPE_PRICE_GO_YEARLY=price_...
STRIPE_PRICE_PLUS_MONTHLY=price_...
STRIPE_PRICE_PLUS_YEARLY=price_...
```

`ProductSettings` reads the same environment/.env as core settings. Stripe product
IDs, prices, keys and portal configuration were NOT changed on a live account.
Keep legacy STRIPE_PRICE_MONTHLY and STRIPE_PRICE_YEARLY references so existing
subscriber prices continue to be recognized as Plus after new prices are configured.
Configure the Stripe portal to allow only the intended tier/interval products.
Checkout validates active status, EUR amount and recurring interval. It never adds
an additional card-based trial. Application trial remains independent of checkout.

Run Alembic through `0068_billing_intents` before traffic. Migration0066 preserves
legacy paid accounts as Plus. Effective `/me.tier` comes from payment status or
server-issued trial; `billing_product_tier` describes the stored billing product.
Canceled/past-due/unpaid users resolve to Free; cancel-at-period-end keeps paid
access while Stripe remains active. Self-hosted STRIPE_ENABLED=false stays unmetered.

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
| Standalone pronunciation TTS |300|1800|5400|month / seconds|

Voice session caps are300/900/1800 seconds. UTC day, Monday-based week and calendar
month resets, no rollover, one shared account allowance across all learning languages.
Input caps: chat2000 characters, translation/correction1000, AI cards20/request.
Manual card import/creation and review of existing content are not AI generation.
XP and competition scoring are unchanged.

## Implemented endpoints and UI

- Public `GET /api/subscriptions/catalog` and `/api/config.subscription_catalog`.
- Authenticated `GET /api/subscriptions/me`: tier and used/reserved/remaining/resets.
- `GET /api/freemium/status`: compatibility scalars plus the feature map.
- `POST /api/subscriptions/correct`: standalone correction shares translation quota.
- Durable reservations in translation, both tutor chat paths, new lesson persistence,
  flashcard generation/from-word, reading/listening generation, voice and standalone TTS.
- Reading/listening replay, attempts, cached audio and history do not consume generation quota.
- Settings `/settings/subscription` shows real usage and plan actions. Pricing uses three
  tiers and a separate billing interval selector. Paid/trial banners no longer hide usage
  or promise unlimited access. Arabic/English wording is implemented; full locale rollout
  remains outstanding.

Voice bills server session elapsed time only after a delivered user turn with nonempty
assistant text, audio and completion. Failed-only, empty-answer, text-only and greeting-only
sessions release reservations. Idle time after a successful turn is included in session time.
TTS measures WAV/MP3 duration and rounds up seconds. Oversized output isn't delivered or
charged. Backend now requires mutagen. Cached voice previews remain free.

## Concurrency and recovery

Conditional SQL updates enforce allowance caps; terminal state/counters settle atomically.
Two-hour worker reservations are reclaimed on the next same-bucket reserve. Usage status
excludes expired holds so they cannot indefinitely block preflight voice/TTS checks.
Reading/listening's optional Redis generation lock has a five-minute lease. Without Redis,
duplicate generation remains possible, though numeric quotas remain capped.

Checkout intents persist BEFORE Stripe session creation, with Stripe customer/session
idempotency keys. Same account/product/interval retries reuse a session, while another
pending product/interval returns409 until the intent expires. Checkout expires after31minutes.
A provider timeout near expiry still requires recovery testing; no distributed exactly-once
claim is made.

Content saving and quota settlement remain separate transactions. A crash or database
failure between them requires reconciliation. SQLite locking with independently opened
quota sessions needs integration verification, especially persistence-failure cleanup.
Legacy auth/legal/translation wording and other billing CTA consumers require a final audit.

## Verification

Tests were added/migrated for tier catalog, payment contracts, intent reuse, legacy price
mapping, quota boundary/failure release/idempotency, voice delivery and measured WAV duration.
Build, pytest, Vitest, migrations, Stripe webhooks and browser/device testing have NOT run
in the current environment. Static reviews and source changes are not passing runtime tests.
