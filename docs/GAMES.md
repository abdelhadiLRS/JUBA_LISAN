# JUBA LISAN Games

## Purpose

Games are a learning surface, not a visual-only feature. Every supported game produces a persisted game session and contributes measurable practice evidence to learner progress.

## Game modes

### New learning modes

- **Word Scramble** — reconstruct a vocabulary item from shuffled letters; text answers are validated by the server and mapped to vocabulary mastery.
- **Fill the Blank** — contextual grammar retrieval using sentence completion; choices are generated and scored server-side.

These modes extend the existing Memory, Matching, Sentence Builder, Quick Choice, Listen & Choose, and Spelling games.

- **Word Match** — vocabulary matching with persisted scoring.
- **Quick Choice** — timed multiple choice; timeout is persisted as incorrect.
- **Sentence Builder** — grammar-focused word ordering through the interactive game engine.
- **Listen & Choose** — target-language audio interaction mapped to listening skill.
- **Spelling Challenge** — text input with authoritative backend validation.
- **Memory Cards** — interactive vocabulary pair matching.

## Persistence

The frontend starts and completes sessions through the game persistence layer. The backend stores game progress/events and derives XP, score, accuracy, streaks, daily completion, achievements, and statistics.

The client does not grant XP or determine the authoritative reward.

## Mastery integration

Completed game events are mapped to skills: matching → vocabulary, quick_choice → vocabulary, sentence_builder → grammar, listen_choose → listening, spelling → writing, memory → memory.

Game evidence is incorporated into the Mastery Center while the lesson-based next-skill recommendation remains based on lesson mastery data.

## Daily Challenge

The daily game identifier is deterministic and synchronized between client display and backend validation. The backend remains authoritative for eligibility and reward calculation.

## Localization

The Games Hub provides dedicated Arabic, French, and English copy, with RTL layout for Arabic.

## Non-negotiable rules

1. No mock game completion.
2. No client-only XP grants.
3. No client-authoritative scoring.
4. Text-answer games must be validated by the backend.
5. Game results remain associated with the authenticated learner.
6. Game results are usable as learning evidence.