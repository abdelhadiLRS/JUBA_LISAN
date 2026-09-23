# JUBA LISAN

![JUBA LISAN](https://img.shields.io/badge/JUBA%20LISAN-AI%20Language%20Learning-b1bde8?style=flat-square)
![License](https://img.shields.io/badge/license-AGPL%20v3-blue?style=flat-square)
![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square)
![Redis](https://img.shields.io/badge/Redis-7-dc382d?style=flat-square)
![Windows](https://img.shields.io/badge/Windows-desktop-0078D4?style=flat-square)

## Overview

**JUBA LISAN** is a multilingual, AI-assisted language-learning platform built around structured CEFR learning, personalized study plans, interactive lessons, vocabulary, grammar, reading, listening, writing, spaced repetition, AI conversation, speech, assessment, progress tracking, learner memory, and multilingual support.

The project is designed as a self-hostable platform and can use local AI services such as Ollama as well as configurable external AI and speech providers. The backend is the integration boundary for AI, speech, database, cache, authentication, quotas, and business logic.

> **Status:** actively developed. The repository already contains the core learning platform, multi-language learning architecture, study-plan engine, AI tutor, voice pipeline, generated reading/listening exercises, learner memory, feedback, reviews, subscriptions, administration, CI/CD, and Windows desktop packaging.

## Vision

JUBA LISAN is intended to be a complete language-learning environment rather than a simple vocabulary application.

Its architecture combines:

- CEFR-oriented progression from A1 to C2.
- Placement and level assessment.
- Personalized study plans.
- Grammar, vocabulary and phrasebook foundations.
- Reading, listening, writing and conversation.
- AI-generated exercises and learning material.
- AI tutoring through the persona **Lingu**.
- Text and real-time voice conversation.
- Spaced repetition and flashcards.
- XP, streaks, competencies, skill scores and progress.
- Multiple simultaneously learned target languages.
- Native-language explanations and translations.
- Persistent learner memory.
- Multilingual UI.
- Optional subscriptions and quotas.
- Self-hosted/server deployment.
- Windows desktop deployment.

## Learning model

The platform separates the user account from individual learning tracks.

A learner can study multiple target languages simultaneously. Each target language has its own study plan, curriculum progression, lessons, competencies and progress.

User-level information remains global, including:

- profile and account;
- native language;
- UI locale;
- avatar/profile information;
- subscription and quota state;
- AI memories.

The current default target language is **en-GB**. **en-US** is also supported but is not used as the fallback default.

Lesson progression is designed around explicit lifecycle states. The plan can contain current, pending, skipped and completed lessons. A completed lesson can be reviewed without awarding progress again, while skipped pending lessons can be resumed.

## Language architecture

Current fully integrated target-language support includes:

- en-GB — English (United Kingdom)
- en-US — English (United States)
- es-ES — Spanish
- it-IT — Italian
- pt-PT — Portuguese
- de-DE — German
- fr-FR — French
- ja-JP — Japanese
- ko-KR — Korean
- zh-CN — Mainland Chinese

The repository also contains an expanding language-data foundation for additional languages and native-language/resource coverage, including Arabic, Danish, Dutch, Finnish, Greek, Hindi, Indonesian, Malay, Norwegian, Persian, Polish, Russian, Swedish, Turkish and others.

The project distinguishes three concepts:

1. **Target language:** a language with complete learning-track/application integration.
2. **Native/resource language:** a language available for translations, explanations, static resources, onboarding, UI or future curriculum expansion.
3. **Future world-language catalogue:** the architecture is designed to expand substantially beyond the currently integrated target-language set without rewriting the learning engine.

New target languages should follow the canonical process documented in specs/add-target-language.instructions.md.

## AI tutor — Lingu

The built-in AI tutor is named **Lingu**.

Lingu is integrated with the learning engine and can:

- conduct text conversations;
- conduct voice conversations;
- adapt responses to the learner's target language and level;
- explain grammar and vocabulary;
- provide corrections and feedback;
- use native-language support;
- work with lesson/study context;
- retain selected learner memories;
- operate through configurable LLM providers.

Supported provider options include:

- Ollama for local/self-hosted inference;
- OpenAI;
- Anthropic;
- DeepSeek.

The frontend never needs direct access to provider credentials. AI requests are handled by the backend.

## Voice and conversation

Voice is a first-class learning capability.

The real-time conversation pipeline supports:

- WebSocket communication;
- speech-to-text;
- LLM response generation;
- text-to-speech;
- streamed audio;
- voice activity detection;
- interruption/barge-in handling;
- conversation duration/inactivity controls;
- persistent text transcripts.

### TTS

Supported modes include:

- local Kokoro-FastAPI;
- OpenAI TTS.

### STT

Supported modes include:

- local faster-whisper;
- OpenAI Whisper.

Local speech services can use GPU acceleration where available. External providers can be selected when local hardware is insufficient.

## Personalized study plans

The study-plan engine organizes learning into a progression instead of isolated exercises.

It manages:

- target language;
- CEFR level;
- lesson sequence;
- progress day;
- current lesson;
- pending lessons;
- skipped lessons;
- completed lessons;
- resumed lessons;
- competency progression.

Important integrity rules include atomic completion/progress updates and protection against duplicate progress from ordinary lesson review.

The authoritative study-plan behavior is documented in specs/study-plan.instructions.md.

## Learning resources

### Grammar

Structured grammar resources provide explanations, examples and level-oriented learning. Native-language help is supported where available.

### Vocabulary

Vocabulary resources provide structured lexical learning and connect to lesson and review workflows.

### Phrasebook

The phrasebook focuses on practical expressions and real-world situations.

### Skills and tests

The platform tracks competencies and skills and includes level-oriented completion tests and assessments.

## Reading and listening

### Reading

AI-generated reading exercises can combine:

1. target language and learner level;
2. generated reading content;
3. comprehension questions;
4. persisted exercise state;
5. API delivery;
6. attempt/result tracking.

Reading history is available with shared pagination.

### Listening

The listening pipeline combines AI generation and speech synthesis:

1. generate level-appropriate content;
2. generate questions;
3. synthesize audio;
4. store/reuse generated resources;
5. deliver the exercise;
6. record attempts and results.

Listening history is also paginated.

Active reading and listening exercises use the shared vocabulary/flashcard lookup flow so learners can save useful words for later review.

## Vocabulary and spaced repetition

JUBA LISAN includes an SM-2-style spaced-repetition workflow.

Flashcards can be created from learning surfaces and reviewed later using learner performance and review intervals. Vocabulary remains connected to the curriculum instead of being isolated from the rest of the learning experience.

## Assessment and progress

The platform tracks multiple dimensions of progress:

- XP;
- streaks;
- skill scores;
- competencies;
- lesson completion;
- study-plan progress;
- assessment results;
- reading attempts;
- listening attempts;
- flashcard/review activity;
- conversation activity.

Assessment supports placement and level progression rather than acting only as a generic quiz.

## Learner memory

JUBA LISAN includes an AI memory system for authenticated learners.

Memory is **global per user**, not separated by target language. Lingu can save useful learner context through a controlled memory tool, and users can manage their memories directly.

Supported operations include:

- best-effort automatic memory saving;
- manual creation;
- listing;
- deletion;
- clearing.

Memory behavior is deliberately conservative: confirmed saves are required before reporting success, memory failures should not break normal text/voice responses, and deleting a learning language preserves the learner's global memories.

## Accounts and authentication

The authentication system uses short-lived JWT access tokens and rotating opaque refresh tokens.

Current design:

- JWT HS256 access token;
- approximately 15-minute access-token lifetime;
- opaque UUID4 refresh token;
- approximately 30-day refresh lifetime;
- HTTP-only refresh cookie;
- server-side refresh-token storage;
- refresh rotation and replay protection;
- logout invalidation;
- frontend silent refresh on 401 responses.

Account features include registration, login/logout, email verification, password reset, profile management, avatar support, native-language selection, UI locale and learning-language management.

Public registration can be disabled, allowing controlled user/invitation management.

## Feedback, reviews and administration

### Feedback

Users can submit feature requests and bug reports, vote, comment and follow discussions. Administrators can moderate and respond.

The authenticated feedback UI includes unread-thread indicators and administrator badges.

### Reviews

The platform supports one verified review per user, administrator approval and display of approved positive reviews on the public landing page.

### Administration

Administration includes:

- maintenance mode;
- dashboard announcements;
- user/account management;
- feedback moderation;
- review approval;
- subscription-related controls.

Dashboard announcements can be authored, translated, edited, activated/deactivated and revised across supported UI languages. Dismissal is tracked per user and revision.

## Subscriptions and quotas

JUBA LISAN can run as a self-hosted application without commercial services, while hosted deployments can enable freemium and subscription controls.

The platform includes:

- Stripe integration;
- subscription state;
- token quotas;
- conversation/session limits;
- usage accounting;
- customer portal support when enabled.

Self-hosted deployments can disable Stripe.

A configurable one-time post-assessment voice trial is also supported for eligible unsubscribed hosted users.

## Architecture

~~~text
                    JUBA LISAN FRONTEND
               Next.js / React / TypeScript
                          │
                    REST / WebSocket
                          │
                          ▼
                 FASTAPI BACKEND
       Auth / Learning / AI / Speech / Progress
                 │                 │
        ┌────────┘                 └─────────┐
        ▼                                    ▼
   PostgreSQL 16                          Redis 7
 persistent data                       cache / locks
        │
        └───────────────┐
                        ▼
              AI / SPEECH PROVIDERS
       Ollama / OpenAI / Anthropic / DeepSeek
       Kokoro / faster-whisper / OpenAI speech
~~~

The backend is the integration boundary. Browser clients do not directly call Ollama, speech engines, or provider APIs.

## Repository structure

~~~text
JUBA_LISAN/
├── assets/                         # Product logos and static assets
├── automation/                     # Build, development and status scripts
├── backend/                        # FastAPI application
│   ├── alembic/                    # Database migrations
│   ├── app/                        # API, models, services, schemas and data
│   └── tests/                      # Backend tests
├── data/                           # Shared/runtime data where applicable
├── docs/                           # Documentation/content
├── frontend/                       # Next.js App Router application
├── messages/                       # next-intl translations
├── scripts/                        # Setup, formatting and maintenance
├── specs/                          # Authoritative technical specifications
├── .github/workflows/              # CI/CD workflows
├── AGENTS.md                       # Development/AI-agent rules
├── API_INTEGRATION_GUIDE.md        # API integration guide
├── API_SETUP_GUIDE.md              # API setup guide
├── CHANGELOG.md                    # Detailed version history
├── CONTRIBUTING.md                 # Contribution workflow
├── DEVELOPMENT.md                  # Development guide
├── DEVELOPMENT_ROADMAP.md          # Product roadmap
├── IMPLEMENTATION_PLAN.md          # Implementation planning
├── IMPLEMENTATION_COMPLETE.md      # Implementation status
├── docker-compose.yml              # Deployment compose stack
├── docker-compose.dev.yml          # Development compose stack
├── .env.example                    # Environment template
├── LICENSE                         # License
└── README.md                       # Project overview
~~~

## Technology stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js 16, React, TypeScript |
| UI | shadcn/ui, Tailwind CSS |
| State | Zustand |
| i18n | next-intl |
| Backend | FastAPI, Python 3.14 |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy async |
| Migrations | Alembic |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Local LLM | Ollama |
| External LLM | OpenAI, Anthropic, DeepSeek |
| Local TTS | Kokoro-FastAPI |
| Local STT | faster-whisper |
| External speech | OpenAI TTS / Whisper |
| Desktop | Electron + Next.js standalone + packaged FastAPI |
| Deployment | Docker Compose |
| CI/CD | GitHub Actions |

## Backend data model

The backend uses SQLAlchemy with Alembic migrations.

The schema covers areas including:

- users and authentication;
- target languages;
- study plans;
- lessons and exercises;
- competencies and progress;
- conversations;
- reading;
- listening;
- flashcards/review;
- feedback;
- reviews;
- learner memories;
- AI usage;
- quotas;
- subscriptions;
- email verification/reset;
- profile and UI locale.

Database changes should be implemented through versioned Alembic migrations.

## API and real-time communication

The REST API covers authentication, users, learning languages, study plans, lessons, resources, flashcards, reading, listening, progress, feedback, reviews, memory, subscriptions, quotas and administration.

Real-time AI conversation uses:

~~~text
/ws/conversation
~~~

Production reverse proxies must preserve WebSocket upgrade/forwarding behavior.

The complete API inventory is maintained in specs/api-endpoints.instructions.md.

## Internationalization

JUBA LISAN has two complementary localization layers.

### Interface language

The frontend uses next-intl message files for UI localization.

### Learning/native language

The learner's native language can differ from the target language and is used for:

- vocabulary translations;
- flashcards;
- tutor feedback;
- lesson native explanations;
- exercise explanations;
- grammar help;
- phrasebook resources;
- vocabulary resources.

The architecture is intended to support RTL languages and non-Latin writing systems as the language catalogue grows.

## Windows desktop application

JUBA LISAN includes a Windows x64 desktop target.

The desktop package contains:

- Electron shell;
- Next.js standalone renderer;
- packaged FastAPI backend;
- SQLite persistence;
- application data stored outside the installation directory;
- persistent authentication state;
- optional Ollama integration;
- Redis disabled for the core desktop runtime.

Build from PowerShell:

~~~powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-desktop.ps1
~~~

Artifacts are written under:

~~~text
frontend\dist\
~~~

The repository also contains a dedicated Windows desktop GitHub Actions workflow.

## Development environment

**Docker is not required or expected on the local development machine.**

The project's development rules use a remote deployment model: the local machine is used for editing and validation, while the full Docker/Compose application runs remotely or in CI.

Local validation focuses on:

- backend unit tests;
- Ruff/Black;
- frontend lint;
- TypeScript type checking;
- frontend unit tests;
- formatting;
- pre-push validation.

Docker Compose remains relevant to deployment and CI/CD, not to the normal local development workflow.

## Local development without Docker

### Backend

Use Python 3.14 and a virtual environment.

~~~powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
~~~

### Frontend

~~~bash
cd frontend
npm install
npm run lint
npx tsc --noEmit
npm run test:run
~~~

The repository expects package-lock.json to remain compatible with npm 11.

### Formatting

From the repository root:

~~~bash
./scripts/format.sh
~~~

This is the canonical formatting entry point.

## Configuration

Start from .env.example.

Important configuration areas include:

- application URL and environment;
- SECRET_KEY;
- registration policy;
- PostgreSQL settings;
- Redis settings;
- LLM_PROVIDER;
- OLLAMA_BASE_URL and OLLAMA_MODEL;
- OpenAI/Anthropic/DeepSeek credentials when used;
- TTS_PROVIDER;
- STT_PROVIDER;
- speech models/voices;
- quotas and conversation limits;
- Stripe settings;
- assessment voice-trial settings.

Never commit real production secrets.

## Testing and quality

### Backend

- pytest;
- asynchronous API/service tests;
- authentication tests;
- database/model tests;
- service tests;
- coverage tracking;
- Ruff;
- Black.

### Frontend

- ESLint;
- TypeScript type checking;
- Vitest/unit tests;
- build verification.

### CI/CD

GitHub Actions cover:

- backend quality;
- frontend quality;
- pull-request/develop validation;
- Docker image publishing;
- release automation;
- mobile checks;
- Windows desktop packaging.

The development rules require failing tests to be reported instead of silently changing production code just to make a suite pass.

## Documentation

The project follows specification-driven documentation.

Important references include:

- specs/architecture.instructions.md — overall architecture and data flow.
- specs/architecture-backend.instructions.md — backend architecture.
- specs/architecture-frontend.instructions.md — frontend architecture.
- specs/database-models.instructions.md — database schema.
- specs/services.instructions.md — backend services.
- specs/prompts.instructions.md — AI prompt architecture.
- specs/api-endpoints.instructions.md — REST/WebSocket API.
- specs/study-plan.instructions.md — study-plan behavior.
- specs/add-target-language.instructions.md — language expansion checklist.
- specs/testing.instructions.md — testing strategy.
- specs/docker.instructions.md — deployment/Compose.
- specs/rate-limiting.instructions.md — API rate limits.
- specs/roadmap.instructions.md — roadmap.
- CHANGELOG.md — detailed implementation history.
- DEVELOPMENT_ROADMAP.md — high-level milestones.
- AGENTS.md — development and AI-agent operating rules.

Documentation is part of the implementation. Changes to behavior, models, endpoints, configuration, dependencies or major features should keep the affected specifications and changelog synchronized.

## Development principles

1. Preserve learning logic when changing the UI.
2. Keep the core engine language-neutral.
3. Support multiple simultaneous learning tracks.
4. Keep local AI a first-class option.
5. Keep LLM/TTS/STT providers replaceable.
6. Keep provider credentials and external API calls behind the backend.
7. Preserve progress integrity and atomic lesson completion.
8. Keep technical documentation synchronized with implementation.
9. Support both full server deployment and practical Windows desktop use.
10. Design internationalization for expansion rather than one fixed language.
11. Keep language data modular and independently expandable.
12. Keep learner memory manageable and non-essential to basic conversation.

## Roadmap direction

The long-term development direction includes:

- deeper A1–C2 curriculum coverage;
- expansion of the world-language catalogue;
- richer grammar/vocabulary foundations;
- broader native-language explanations;
- improved multilingual speech;
- stronger adaptive learning;
- richer assessment and competency models;
- improved AI tutoring and correction;
- improved conversation quality and memory;
- additional learning activities;
- stronger mobile/device support;
- continued Windows desktop refinement;
- self-hosting and operational hardening;
- richer learner analytics.

The language roadmap should continue through the modular language-data architecture rather than duplicating the learning engine for every language.

## Licensing and attribution

JUBA LISAN retains the repository's existing licensing, copyright, attribution, contribution and commercial-license documents.

Before redistributing or offering the project as a hosted service, review:

- LICENSE
- COMMERCIAL_LICENSE.md
- CONTRIBUTING.md
- CONTRIBUTOR_LICENSE_AGREEMENT.md

## Repository

**GitHub:** https://github.com/abdelhadiLRS/JUBA_LISAN

The README provides the project-level overview. The repository specifications and CHANGELOG remain the authoritative sources for detailed implementation behavior and version history.
