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
