# Skill Mastery

JUBA LISAN derives skill mastery from the same adaptive exercise mastery engine used by lesson review.

## Contract

Skill labels are read from each lesson exercise's `skills` metadata. Before aggregation or targeting, labels are:

1. trimmed;
2. case-folded;
3. discarded when empty or non-string;
4. deduplicated per exercise.

An exercise may contribute to more than one skill.

## Mastery model

Each skill reuses the exercise-level mastery state:

| State | Rule |
| --- | --- |
| `unseen` | No valid adaptive variant attempt exists. |
| `struggling` | Mastery score is below `0.50`. |
| `learning` | Mastery score is at least `0.50` but the mastery requirement is not met. |
| `mastered` | Average best score is at least `0.80` and at least two distinct variants are covered for every exercise in the skill. |

Repeated attempts on the same normalized variant improve its best score but do not add variant coverage.

## API

- `GET /api/lessons/{lesson_id}/mastery` — lesson snapshot, including the skill collection.
- `GET /api/lessons/{lesson_id}/mastery/skills` — skill-only snapshot.
- `GET /api/lessons/{lesson_id}/mastery/skills/next` — highest-priority non-mastered skill.
- `GET /api/lessons/{lesson_id}/mastery/skills/{skill}/next` — next mastery exercise for one requested skill.

The skill-specific target endpoint treats surrounding whitespace and case differences as the same skill. An empty skill is rejected with HTTP 400; an unknown skill is rejected with HTTP 404; a skill with no remaining mastery target is also rejected with HTTP 404.

## Selection order

The next skill follows one deterministic priority:

`struggling → unseen → learning → mastered`

Mastered skills are excluded. Within the same state, lower mastery rate is selected first, followed by lower average mastery score and then the canonical skill name.

Skill-focused exercise selection uses the same lesson mastery selector, so the state priority and score ordering remain consistent between lesson-wide and skill-scoped practice.

## UI behavior

The lesson screen exposes:

- an explicit completion state when every tracked skill is mastered;
- a lesson-level mastery snapshot;
- a prioritized skill coverage section;
- a direct practice action on every non-mastered skill;
- a focused mastery session that remains scoped to the selected skill;
- an explicit exhausted state when no target remains.

A focused session captures the selected skill's mastery rate at start. Progress in unrelated skills does not terminate that session. Completion occurs when the selected skill becomes mastered or its skill-scoped target endpoint is exhausted.

## Data consistency

The API is the source of truth. After a review answer, the client refreshes lesson mastery and its embedded skill collection together. Exercise responses also expose normalized skill labels so exercise metadata and aggregate skill identity use the same canonical representation.
