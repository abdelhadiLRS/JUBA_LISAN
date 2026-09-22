# Lesson Mastery Review

JUBA LISAN exposes lesson-level mastery targeting through:

- `GET /api/lessons/{lesson_id}/mastery` for aggregate mastery coverage.
- `GET /api/lessons/{lesson_id}/mastery/next` for the next exercise that needs mastery work.

## Selection policy

1. Struggling exercises are selected before unseen exercises.
2. Unseen exercises are selected before learning exercises.
3. Within the same state, the lowest mastery score is selected first.
4. Mastered exercises are excluded.
5. Response reasons are stable: `struggling`, `unseen`, or `lowest_mastery`.

The selection logic is isolated in `backend/app/services/lesson_mastery.py` so API and future UI review flows can reuse the same policy.
The lesson-wide and skill-wide selectors share one canonical state-priority table in `lesson_mastery.py`, so `struggling → unseen → learning → mastered` cannot drift between review surfaces.


## Review session

The lesson UI now turns the next-target endpoint into a focused review session:

- Starting review captures the current lesson mastery rate.
- Each completed review exercise advances to a fresh mastery candidate.
- The session does not complete the lesson itself.
- If the lesson mastery rate increases during the session, the review session ends and reports the improvement.
- The learner can also finish the review session manually at any time.
- If no non-mastered candidate remains, the session ends automatically.


### Session progress feedback

The review session records the mastery rate at session start. When a completed review raises the lesson mastery rate, the session ends and the UI keeps the final rate so it can show the exact positive delta (for example, `Δ +8%`). The active session card also exposes the current candidate reason and uses an ARIA live region so progress changes are announced to assistive technology.


### Struggling-answer retention

When a review answer scores below the struggling threshold, the session keeps the answered exercise in place instead of immediately replacing it with another candidate. Existing retry and adaptive-variant actions remain available, allowing the learner to reinforce the same weak item before the session moves on.


### Candidate mastery completion

A review session now ends when the exercise just reviewed reaches the `mastered` state in the refreshed attempt summary. The lesson mastery aggregate is refreshed before the completion state is displayed, so the final mastery rate and delta reflect the post-answer state. If the candidate is not yet mastered, the existing session selection and struggling-answer retention rules continue to apply.


### Immediate candidate state hydration

After each review answer, the client reconciles the answered exercise with the refreshed attempt summary before deciding whether to continue the session. The candidate's `mastery_score`, `mastery_state`, and `mastery_variants` are written into the local exercise model immediately, preventing the mastery card from displaying the pre-answer state while the aggregate mastery request is completing.

### Exhausted review state

When a skill-focused review is exhausted, the UI keeps the selected skill in context and uses skill-specific completion copy rather than claiming that the whole lesson is mastered. The lesson-wide review keeps the generic exhausted message.


When the mastery-next endpoint reports that every lesson exercise is mastered, the lesson UI now exits the active review loop into an explicit exhausted state. The state is localized, announces completion through the live status region, and provides the existing Finish action instead of silently clearing the candidate.


## Skill mastery contract

Lesson mastery is the exercise-level aggregate for one lesson. Skill mastery reuses the same adaptive mastery states but groups exercises by the normalized `skills` metadata attached to lesson content. A single exercise may contribute to multiple skills, while duplicate skill labels on the same exercise are counted once.

The skill endpoint is `GET /api/lessons/{lesson_id}/mastery/skills`. Each skill reports total, attempted, mastered, learning, struggling, and unseen exercises, average mastery score, mastery rate, attempt rate, and covered adaptive variants. This keeps the lesson UI able to explain both **how much of the lesson is mastered** and **which learning skills still need coverage**.

## Skill mastery presentation

The lesson screen presents skills in action priority rather than alphabetical order: struggling skills first, then unseen, learning, and mastered. Within the same state, lower mastery coverage appears first and skill names provide a deterministic tie-break. This makes the existing snapshot immediately actionable without changing the API's canonical skill ordering.

Exercise payloads also expose skill labels through the same canonical normalization (trimmed, case-folded, and deduplicated), so exercise-level metadata and aggregate skill buckets use one identity.

The lesson screen presents each normalized skill as a compact coverage card. The card shows the mastery percentage, mastered/learning/review-needed exercise counts, attempt rate, average mastery score, and covered adaptive variants. The API remains the source of truth; the UI refreshes skill mastery after review answers so the skill breakdown stays aligned with the lesson-level aggregate. Each non-mastered skill card also exposes a direct practice action, so learners can start a focused review for that exact skill without first selecting it from the global next-skill recommendation.


## Skill-level mastery snapshot

The lesson mastery response now includes a skills collection derived from the same exercise-level mastery engine. Each skill aggregates every lesson exercise mapped to that skill, including:

- mastery state (unseen, struggling, learning, mastered)
- attempted and mastered exercise counts
- average mastery score
- attempt and mastery rates
- covered adaptive variants

The dedicated GET /api/lessons/{lesson_id}/mastery/skills endpoint remains available for clients that only need skill coverage. `GET /api/lessons/{lesson_id}/mastery/skills/next` now returns the highest-priority non-mastered skill using the same struggling → unseen → learning policy, with lower mastery coverage as the tie-break. The lesson-level GET /api/lessons/{lesson_id}/mastery response is the preferred lesson-screen snapshot: it carries both lesson and skill progress, so the lesson UI hydrates both views from one request and refreshes them together after an answer.


## Mastery state model

Mastery is derived from the best score for each distinct adaptive variant of a content identity. The thresholds are centralized in the adaptive mastery service:

| State | Rule |
| --- | --- |
| `unseen` | No valid adaptive variant attempt exists for the content identity. |
| `struggling` | Mastery score is below `0.50`. |
| `learning` | Mastery score is at least `0.50` but the mastery requirement is not yet met. |
| `mastered` | Average best score is at least `0.80` **and** at least two distinct variants are covered. |

Repeated attempts on the same normalized variant improve its best score but do not increase variant coverage. This prevents repeated retries of one prompt from being treated as equivalent to demonstrated mastery across multiple variants.

## Skill aggregation semantics

Skills are a reporting layer over lesson exercises, not a second scoring engine. Each exercise can contribute to more than one skill. Skill aggregates reuse the exact exercise-level mastery state, so lesson and skill percentages cannot silently diverge because of separate threshold logic.

Skill labels are trimmed, case-normalized, and deduplicated per exercise. Empty and non-string labels are ignored. Skills are returned in deterministic order, while the skills/next selector applies the action order `struggling → unseen → learning → mastered`; within a state it uses mastery coverage, then average mastery score, then the skill name as deterministic tie-breakers.


## Skill-focused mastery practice

The lesson UI can start a mastery review for the highest-priority skill without losing the lesson-level mastery model. The endpoint:

`GET /api/lessons/{lesson_id}/mastery/skills/{skill}/next`

filters the lesson's exercises by the requested skill, applies the same struggling → unseen → learning priority and excludes mastered exercises. Skill matching is case-insensitive and ignores surrounding whitespace. A missing skill or a skill with no remaining mastery target returns a documented 4xx response.

When a skill-focused review is active, subsequent mastery targets remain scoped to that skill until the review is finished or the target is exhausted. This keeps the user's practice intent stable instead of silently switching back to another skill.


## Skill label normalization contract

Skill labels are canonicalized in one shared backend helper before aggregation or skill-focused targeting. A label is trimmed, case-folded, and ignored when it is empty or non-string; duplicate labels on the same exercise are collapsed. The same normalization is used by the aggregate service and by `/{lesson_id}/mastery/skills/{skill}/next`, so a skill such as `Grammar`, ` grammar `, or `GRAMMAR` addresses the same mastery bucket.

The skill-focused endpoint also uses the same stable `mastery_reason()` mapping as lesson-level targeting. This keeps recommendation reasons consistent across lesson-wide and skill-scoped review clients.


### Skill-focused completion semantics

A skill-focused review captures that skill's mastery rate at session start rather than the lesson-wide rate. After each answer, the refreshed skill aggregate is the completion source of truth: the review ends when the selected skill becomes mastered, or when its skill-scoped next-target endpoint is exhausted. A change in the selected skill's mastery rate is reported as the session delta; progress in unrelated skills does not prematurely end the focused review.
