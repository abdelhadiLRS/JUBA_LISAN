# JUBA LISAN

![JUBA LISAN](https://img.shields.io/badge/JUBA%20LISAN-AI%20Language%20Learning-b1bde8?style=flat-square)
![License](https://img.shields.io/badge/license-AGPL%20v3-blue?style=flat-square)
![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square)
![Self-hosted](https://img.shields.io/badge/self--hosted-yes-c3ec6c?style=flat-square)

JUBA LISAN is a self-hosted AI language-learning platform for structured CEFR learning, adaptive lessons, vocabulary, grammar, reading, listening, writing, conversation, flashcards, progress tracking, and optional voice features.

The project is being developed under the **JUBA LISAN** identity while retaining the repository's existing open-source licensing and attribution files. The application is designed to run locally or on a private server, with the backend acting as the integration layer for AI, speech, database, and cache services.

## What it provides

- CEFR-aligned learning from A1 to C2.
- Placement assessment and personalized study plans.
- Grammar, vocabulary, reading, writing, listening, and review lessons.
- AI-generated reading and listening exercises.
- Real-time AI conversation with optional voice input/output.
- SM-2 spaced-repetition flashcards.
- Progress, XP, streaks, skill scores, competencies, and level tests.
- Multi-language learning with native-language support.
- User memory and learning-language management.
- Optional subscriptions and freemium controls for deployments that enable them.
- Local-first AI support through Ollama, with OpenAI, Anthropic, and DeepSeek provider options.

## Architecture

JUBA LISAN is a monorepo composed of:

```text
JUBA_LISAN/
├── assets/                  # Logos and static assets
├── backend/                 # FastAPI backend
├── data/                    # Shared application data
├── docs/                    # Documentation / landing content
├── frontend/                # Next.js App Router frontend
├── messages/                # next-intl translation files
├── scripts/                 # Local setup and maintenance scripts
├── specs/                   # Project specifications
├── AGENTS.md                # AI assistant instructions
├── CHANGELOG.md             # Version history
├── CODE_OF_CONDUCT.md       # Community guidelines
├── COMMERCIAL_LICENSE.md    # Commercial licensing terms, if applicable
├── CONTRIBUTING.md          # Contribution guide
├── DEVELOPMENT.md           # Development guide
├── docker-compose.yml       # Main Docker deployment
├── docker-compose.dev.yml   # Development deployment
├── LICENSE                  # Repository license
└── README.md                # This file
```

### Core stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js 16, React, shadcn/ui, Tailwind CSS, Zustand, next-intl |
| Backend | FastAPI, SQLAlchemy async, Alembic, Pydantic v2 |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| LLM | Ollama (local) · OpenAI · Anthropic · DeepSeek |
| TTS | Kokoro-FastAPI (local) · OpenAI TTS |
| STT | faster-whisper (local) · OpenAI Whisper |
| Authentication | JWT access/refresh tokens, users and roles |
| Deployment | Docker Compose |
| Windows Desktop | Electron + Next.js standalone + packaged FastAPI + SQLite |

## Windows Desktop (.exe)

JUBA LISAN includes a Windows desktop target designed to run without Docker, PostgreSQL, or Redis. The desktop package contains:

- Electron desktop shell.
- Next.js standalone renderer.
- Packaged FastAPI backend executable.
- SQLite database stored under the Windows application-data directory.
- Persistent refresh-token records in SQLite so login sessions survive backend/application restarts.
- Optional local AI providers such as Ollama running on the Windows host.
- Redis disabled by default in Desktop mode.

The desktop application is intended for Windows x64.

### Build the Windows installer

From PowerShell at the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-desktop.ps1
```

The script:

1. Builds the packaged FastAPI backend with PyInstaller.
2. Installs frontend dependencies.
3. Builds Next.js in standalone mode.
4. Copies the standalone server, static assets, and public assets into the Electron package staging directory.
5. Builds both an NSIS installer and a portable Windows executable.

Artifacts are written to:

```text
frontend\dist\
```

### Desktop data location

Desktop application data is kept outside the installation directory so uninstall/reinstall does not implicitly remove user data. The application creates a data directory containing the SQLite database, generated secret key, audio files, and other local state.

The desktop backend is bound to localhost only. No Docker, PostgreSQL, or Redis service is required for the core desktop runtime.

### Desktop verification

The Windows CI workflow validates:

- SQLite model compatibility.
- Alembic migrations against SQLite.
- Desktop registration, login, logout, refresh, and `/me`.
- Refresh-token persistence after restarting the packaged backend against the same SQLite database.
- Startup and HTTP serving of the packaged Next.js standalone renderer.
- Windows NSIS and portable artifacts.

A local Windows build should still be performed before distributing an installer to end users.

## Quick start on Windows

The recommended Windows path for the server/self-hosted deployment is Docker Desktop with WSL2, plus Ollama running on the Windows host when using a local LLM.

### 1. Clone

```powershell
git clone https://github.com/abdelhadiLRS/JUBA_LISAN.git
cd JUBA_LISAN
```

### 2. Generate the local environment

The repository includes a Windows bootstrap script that creates `.env` from `.env.example` and generates local PostgreSQL, Redis, and JWT secrets.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-local.ps1
```

To generate the environment and start the stack in one step:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-local.ps1 -Start
```

### 3. Start the application manually

```powershell
docker compose up -d --build
```

Check service state:

```powershell
docker compose ps
```

Open:

```text
http://localhost:3000
```

Database migrations are executed by the backend during startup.

### 4. Local Ollama model

For the current JUBA LISAN local setup, the default model is:

```text
juba-coder
```

If Ollama is installed on the Windows host:

```powershell
ollama pull juba-coder
```

The default Docker configuration reaches host Ollama through:

```text
http://host.docker.internal:11434
```

You can change `LLM_PROVIDER`, `OLLAMA_BASE_URL`, and `OLLAMA_MODEL` in `.env`.

> **Important:** `juba-coder` is the current local development default. For production language tutoring, use a model that is appropriate for the desired language quality and hardware capacity.

## CPU-only Windows systems

The core JUBA LISAN stack does not require an NVIDIA GPU. GPU speech services are optional and are exposed through the `gpu` Docker Compose profile.

Start the core stack without GPU services:

```powershell
docker compose up -d --build
```

Enable the GPU speech profile only on a compatible NVIDIA/CUDA host:

```powershell
docker compose --profile gpu up -d --build
```

For CPU-only TTS/STT, configure the appropriate CPU speech images or use the OpenAI providers. The core web application, database, Redis, authentication, learning engine, and local LLM integration do not depend on NVIDIA hardware.

## Environment configuration

Start from `.env.example`. At minimum, a self-hosted deployment needs secure values for:

- `SECRET_KEY`
- `POSTGRES_PASSWORD`
- `REDIS_PASSWORD`
- `APP_BASE_URL`
- `LLM_PROVIDER`
- `OLLAMA_BASE_URL` and `OLLAMA_MODEL` when using Ollama

Never commit a real `.env` file or production secrets to Git.

## Production notes

### Reverse proxy and WebSocket

Real-time conversation uses `/ws/conversation`. A production deployment should place a reverse proxy in front of the application and forward WebSocket traffic to the backend container on port `8000`.

Microphone access requires a secure browser context: HTTPS in production or `localhost` during local development.

### Redis

Linux hosts should enable Redis memory overcommit:

```bash
sudo sysctl vm.overcommit_memory=1
echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf
```

### Speech services

TTS and STT are independently configurable:

```env
TTS_PROVIDER=local
STT_PROVIDER=local
```

or, when using OpenAI APIs:

```env
TTS_PROVIDER=openai
STT_PROVIDER=openai
OPENAI_API_KEY=...
```

Local Kokoro speech is primarily suited to English. For multilingual speech requirements, configure a suitable multilingual provider.

## Development

Frontend commands:

```bash
cd frontend
npm install
npm run dev
npm run lint
npm run test:run
npm run build
```

Backend development uses FastAPI, SQLAlchemy, Alembic, PostgreSQL, and Redis. See `DEVELOPMENT.md` for the repository's development workflow.

## Project principles

1. **Preserve core learning logic.** UI modernization must not silently change learning, scoring, authentication, quota, or API behavior.
2. **Local-first development.** The platform should remain usable with local services wherever practical.
3. **Modular providers.** LLM, TTS, and STT providers are configurable rather than hard-wired to one vendor.
4. **Responsive SaaS-style UI.** The JUBA LISAN interface uses a restrained off-white, lavender, lime, muted-purple, and ink visual system.
5. **Main branch development.** The active product implementation is maintained on `main`.

## Licensing and attribution

JUBA LISAN retains the repository's existing license, copyright notices, attribution, contribution, and commercial-license files. Consult `LICENSE`, `CONTRIBUTING.md`, `COMMERCIAL_LICENSE.md`, and related repository documentation before redistributing or offering a modified hosted service.

## Repository

**GitHub:** https://github.com/abdelhadiLRS/JUBA_LISAN

For issues and development work, use the GitHub repository's issue tracker and keep production changes on `main` unless a separate contribution workflow is explicitly required.
