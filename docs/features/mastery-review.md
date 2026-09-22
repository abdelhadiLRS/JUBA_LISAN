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
