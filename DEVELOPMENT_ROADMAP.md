# JUBA LISAN — Development Roadmap

This file tracks the product-rebuild roadmap defined by the master development
prompt, mapped against the actual state of the repository. The reference version
is `specs/version.md` and `CHANGELOG.md` (currently v1.8.40).

Status legend: ✅ Complete · 🟡 Partially complete (started, needs work) · ❌ Not started

## Phase status

### Phase 1 — Audit ✅
- Monorepo audited: `backend/` (FastAPI, 22 models, 20 services, 23 routers), `frontend/` (Next.js 16 App Router, 6 stores, i18n via next-intl with 10 message files), Docker Compose deployment, GitHub Actions CI/CD.
- Existing strengths: full curriculum/study-plan engine, SM-2 flashcards, TTS/STT voice pipeline, Lingu tutor (chat + voice), listening/reading exercises, feedback board, memories, Stripe subscriptions, multi-language learning, onboarding, i18n including RTL-capable locales.
- Last commits established the JUBA LISAN brand direction (`docs/JUBA_LISAN_BRAND.md`), retention learning loop (`docs/LEARNING_RETENTION_SYSTEM.md`), token layer (`frontend/src/app/juba-modern.css`), and refreshed login/register pages.

### Phase 2 — Design System 🟡
- ✅ Color tokens (light/dark) in `juba-modern.css`.
- ✅ App-shell typography migrated to Geist Sans sentence case with token-based states (v1.8.41); remaining legacy screens still use the mono treatment.
- ❌ Centralized component layer on top of the tokens (many legacy mono-styled components remain).
- 🟡 RTL: app shell now uses logical utilities; systematic audit of remaining screens pending.
- ✅ Build determinism: CJK web fonts removed in favor of platform font stacks — production build is fully offline (v1.8.41).

### Phase 3 — App Shell ✅
- ✅ Sidebar + mobile dropdown rebuilt with the JUBA LISAN identity (v1.8.41).
- ✅ Mobile bottom navigation for primary destinations with safe-area support.
- ✅ Real lucide icons across sidebar, dropdown, and bottom navigation.
- ✅ Logical utilities (`border-e`, `ps/pe`, `ms-auto`) for correct RTL mirroring.
- 🔜 Remaining: collapse/toggle behavior for desktop sidebar, deep-shell polish (breadcrumbs, page headers).

### Phase 4 — Onboarding ✅
- ✅ Rebuilt with the JUBA LISAN identity (v1.8.42): JL monogram header, animated step-progress dots, rounded goal chips, modernized trial/subscription cards. Logic, endpoints, and edge cases unchanged.
### Phase 5 — Dashboard 🟡
- ✅ Dashboard rebuilt with the JUBA LISAN identity (v1.8.41): hero next-step card, icon stat tiles (streak/XP/lessons/accuracy), rounded progress bars, skill performance grid with warm accent for weak skills, modernized premium banner and quick actions. All data contracts and behaviors preserved.
- ❌ Retention-loop surfaces on home (items due for review, daily goal ring, smart motivation messages) — pending Smart Review backend surfaces (Phase 9).
### Phase 6 — Timeline A1–C2 🟡
- ✅ Plan page rebuilt (v1.8.42): status-badge unit journey (check/play/lock/ribbon), warm active ring, pill progress bars, highlighted pending-lessons card, modernized unit drawer.
- 🔜 Remaining: multi-level overview (A1→C2 progression map beyond the user's current plan level), unit content previews (vocabulary/grammar/listening counts as visual chips).
### Phase 7 — Courses ❌
### Phase 8 — First Lesson ❌ (lesson player exists, not rebuilt)
### Phase 9 — Smart Review ❌ (SM-2 flashcards exist, needs dedicated review experience)
### Phase 10 — Grammar Review ❌
### Phase 11 — Vocabulary ❌ (vocabulary hub + flashcards exist, needs mastery loop surfacing)
### Phase 12 — Speaking / Lingu ❌ (exists, not rebuilt)
### Phase 13 — Progress ❌ (exists, not rebuilt)
### Phase 14 — Mastery ❌ (competencies exist, not surfaced as mastery center)
### Phase 15 — Streak / Goals / XP ❌ (goals exist at onboarding, no streak/XP system)
### Phase 16 — Discover / Social ❌
### Phase 17 — Profile ❌ (settings/profile exist, not rebuilt)
### Phase 18 — Backend integration 🟡 (rich backend; new surfaces will need small additive endpoints)
### Phase 19 — Performance ❌
### Phase 20 — Accessibility ❌
### Phase 21 — Full QA ❌
### Phase 22 — Production readiness ❌

## Automation

- `automation/` scripts (develop/test/build/status/one-click dev) — ❌ not started.

## Test state

- Frontend: 446/446 passing (fully green as of v1.8.42; two long-standing `apiFetch` test failures repaired).

## Working rules

- Work directly on `main`, no force push, no breaking of existing features.
- Every completed phase: lint + typecheck + tests, commit, push, then update this file.
- Backend/spec documentation updates follow the confirmation rules in `AGENTS.md`.
