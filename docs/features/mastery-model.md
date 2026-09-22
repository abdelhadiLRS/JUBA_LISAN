# Mastery Model

JUBA LISAN tracks mastery at the exercise/content level and aggregates those states into lesson-level progress.

## Mastery states

| State | Meaning | Current rule |
| --- | --- | --- |
| `unseen` | No valid adaptive attempt exists for the content identity. | Zero covered variants. |
| `struggling` | The learner is below the reinforcement threshold. | Mastery score < 0.50. |
| `learning` | The learner has evidence of learning but has not met mastery coverage. | 0.50 ≤ score < 0.80, or fewer than two covered variants. |
| `mastered` | The learner has reached the required score across multiple variants. | Score ≥ 0.80 and at least two distinct variants. |

The score is the average of the best score achieved for each distinct normalized variant belonging to the same `content_id`.

## Lesson mastery

The lesson aggregate exposes:

- attempted and unseen exercise counts;
- struggling, learning, and mastered counts;
- average mastery score;
- attempt and mastery coverage rates;
- the number of covered variants.

The next-target selector uses the same state model:

1. struggling;
2. unseen;
3. learning with the lowest mastery score;
4. deterministic exercise-id ordering for equal scores.

Mastered content is excluded from the next-target queue.

## Review-session lifecycle

The lesson review UI is a focused mastery loop rather than lesson completion:

1. capture the starting lesson mastery rate;
2. request a mastery candidate;
3. answer and refresh the candidate's mastery fields;
4. finish when the candidate becomes mastered or the aggregate rate improves;
5. stop explicitly when no non-mastered candidate remains.

A struggling answer remains available for retry/adaptive reinforcement rather than being discarded from the session.

## Skill-level extension

Skill mastery is designed to be an aggregation layer above the existing content identities. A future skill record can reference one or more exercise/content identities without changing the attempt model. The aggregation should reuse the same per-variant best-score calculation and state thresholds, then group the resulting content mastery by skill.

This keeps **lesson mastery** (coverage of a lesson's exercises) distinct from **skill mastery** (coverage of a reusable learning objective across lessons). Until skill mappings are persisted, the application should not present a fabricated skill percentage.

## Localization contract

User-facing mastery states and review lifecycle messages must be translated through the locale message catalog. API reason values remain stable machine-readable identifiers:

- `struggling`
- `unseen`
- `lowest_mastery`

This separation lets the UI localize wording without changing API behavior.


## Skill mastery

Lesson exercises may declare one or more learning skills through the exercise `skills` field. The mastery engine reuses the same adaptive variant history used for lesson mastery, but groups exercises by normalized skill label.

The lesson API exposes:

- `GET /api/lessons/{lesson_id}/mastery` for the lesson aggregate.
- `GET /api/lessons/{lesson_id}/mastery/skills` for per-skill mastery aggregates.
- `GET /api/lessons/{lesson_id}/mastery/next` for the next exercise requiring mastery work.

An exercise can contribute to multiple skills. Skill labels are trimmed, case-folded, and deduplicated per exercise before aggregation; blank or non-string labels are ignored. Returned skill aggregates are sorted deterministically by canonical skill name. This prevents formatting differences or repeated labels from inflating skill coverage while keeping lesson mastery and skill mastery on the same score, state, and variant-coverage semantics.
