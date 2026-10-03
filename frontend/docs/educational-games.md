# Playable educational games

The main `/games` page now launches ten language-learning activities rather than the previous six-item generic quiz menu: word memory, meaning matching, sentence building, meaning recall, spelling, listening detective, grammar correction, gap fill, word unscrambling and mixed retrieval review.

## Actual gameplay

- Memory: hidden word/definition cards, two-card turns, mismatch delay, matched-pair tracking and a move trace.
- Matching: word/definition columns, selected word state, real pair checks, missed-attempt feedback and a move trace.
- Sentence building: selectable word tiles, independent constructed sentence, removal/repositioning, server scoring. The shuffled public item array is never used as the answer. The old arbitrary ordering route now launches sentence building because the previous random vocabulary order had no inferable educational rule.
- Adaptive question activities: every choice or typed answer goes to `/api/progress/game-session/next`. The UI renders the next server-issued question. A wrong answer reissues the same logical item for retrieval practice; a round finishes only when the server says it is finished.
- Listening: explicit audio button using a matching target-language browser voice. No voice produces a visible error, not a silently wrong-language reading. Voice availability depends on the browser/device; server TTS fallback is not included in this change.

## Persistence and integrity

The existing authenticated session API generates content from the active study plan and CEFR curriculum. The UI uses the active language store, not an unrelated AR/FR/EN UI selector. Difficulty stays within 1..3 and does not change CEFR.

Every round is completed through `/api/progress/game-session/complete`. XP, accuracy and progress use its response only. Results are displayed only after successful persistence. Failed saves preserve answers/trace and remain retryable. Immediate request locks prevent double answer/completion submissions. Component unmount invalidates pending callbacks and clears memory timers/audio. No local reset of real learning progress is exposed.

Legacy `/games/memory`, `/games/matching`, `/games/sentence-builder` and `/games/ordering` pages reuse the new engine. Landing Page files/styles are not changed; the new stylesheet is loaded through internal games routes.

## Verification

`src/components/games/EducationalGameSession.test.tsx` adds eight regression tests for server-issued next questions, same-ID retries, failed saves, duplicate-answer locks, matching traces, server-scored sentence order, startup failures and stale saves after unmount. Run with the project's existing Vitest setup.

These tests, TypeScript build and browser/device checks were not executed in the writing environment because the checkout/dependencies are unavailable and its sandbox has no internet access. This is source implementation, not a claim of deployment or runtime certification.

## Remaining limitations

Interface copy currently supports Arabic and English; full translation-catalog coverage remains pending. Sentence building records the submitted attempt and displays real server accuracy, but does not yet provide an authored correct-sentence explanation or retry within the same completed session. Interactive traces retain all moves and are subject to the server's 100-move limit; a guided recovery mechanism for unusually long rounds is still needed. Existing backend content quality varies by language/CEFR, and generation/fallback quality must be audited independently. The backend itself was not redesigned in this change.
