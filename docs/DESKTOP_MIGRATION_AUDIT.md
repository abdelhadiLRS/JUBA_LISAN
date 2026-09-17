# JUBA LISAN Desktop Migration Audit

## Executive Summary

This document provides a comprehensive audit of the JUBA LISAN codebase for migration to a standalone Windows Desktop application. The goal is to transform the existing web-based platform into a professional desktop application that works offline, without Docker, PostgreSQL, or Redis dependencies.

---

## 1. Current Architecture Overview

### 1.1 Project Structure

```
JUBA_LISAN/
├── backend/                 # FastAPI backend (Python)
│   ├── app/
│   │   ├── core/           # Config, database, security, limiter
│   │   ├── data/           # Local curriculum, vocabulary, grammar
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── routers/        # API endpoints
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic, AI, TTS, STT
│   │   └── main.py         # FastAPI application entry point
│   ├── alembic/            # Database migrations
│   └── requirements.txt    # Python dependencies
├── frontend/                # Next.js frontend (TypeScript/React)
│   ├── src/
│   ├── public/
│   └── package.json        # Node.js dependencies
├── docker-compose.yml      # Production deployment
├── docker-compose.dev.yml  # Development deployment
└── docs/                   # Documentation
```

### 1.2 Current Technology Stack

| Layer | Technology | Desktop Migration Status |
|-------|------------|-------------------------|
| Frontend | Next.js 16, React 19 | ✅ Can be embedded in Tauri/Electron |
| Backend | FastAPI, Python 3.14 | ✅ Can run as local service |
| Database | PostgreSQL 16 | ⚠️ Must replace with SQLite for Desktop |
| Cache | Redis 7 | ⚠️ Must remove or replace with in-memory/SQLite |
| LLM | Ollama, OpenAI, Anthropic, DeepSeek | ✅ Already supports multiple providers |
| TTS | Kokoro (local), OpenAI | ⚠️ Kokoro requires Docker; need Windows TTS fallback |
| STT | faster-whisper (local), OpenAI | ⚠️ Whisper requires Docker; need Windows STT fallback |
| Auth | JWT, custom users table | ✅ Can work locally |
| Deployment | Docker Compose | ❌ Must be replaced with native installer |

---

## 2. Docker Dependencies Analysis

### 2.1 Services Requiring Docker

| Service | Image | Purpose | Desktop Alternative |
|---------|-------|---------|---------------------|
| postgres | postgres:16-alpine | Primary database | **SQLite** (embedded) |
| redis | redis:7-alpine | Caching, rate limiting, sessions | **In-memory cache + SQLite** |
| backend | Custom FastAPI | API server | **Embedded Python runtime** |
| frontend | Custom Next.js | Web UI | **Tauri/Electron WebView** |
| kokoro | ghcr.io/remsky/kokoro-fastapi-gpu | TTS (GPU) | **Windows SAPI + Cloud TTS fallback** |
| whisper | onerahmet/openai-whisper-asr-webservice | STT (GPU) | **Windows Speech Recognition + Cloud STT fallback** |

### 2.2 GPU-Only Services

The `kokoro` and `whisper` services are marked with `profiles: ["gpu"]` and require NVIDIA CUDA. These are **optional** in the current setup and should remain optional in Desktop mode.

**Desktop Strategy:**
- Use Windows built-in TTS/STT APIs when available
- Fall back to cloud providers (OpenAI) if configured
- Gracefully degrade if no TTS/STT is available

---

## 3. PostgreSQL Migration to SQLite

### 3.1 Current Database Configuration

File: `backend/app/core/database.py`

```python
engine = create_async_engine(
    settings.DATABASE_URL,  # postgresql+asyncpg://...
    echo=False,
    connect_args={"timeout": 10, "command_timeout": 10},
)
```

### 3.2 Required Changes

1. **Database URL Abstraction**
   - Desktop mode: `sqlite+aiosqlite:///path/to/juba_lisan.db`
   - Server mode: `postgresql+asyncpg://...`

2. **SQLAlchemy Compatibility**
   - ✅ Already using SQLAlchemy ORM
   - ✅ Models use standard declarative base
   - ⚠️ Need to verify PostgreSQL-specific features (JSONB, arrays, etc.)

3. **Alembic Migrations**
   - ✅ Already using Alembic
   - ⚠️ May need dialect-specific adjustments
   - ✅ Can run migrations programmatically at startup

4. **Async Support**
   - ✅ Using `asyncpg` currently
   - ✅ `aiosqlite` available for SQLite async support
   - Requirements already include `aiosqlite>=0.20`

### 3.3 Potential Issues

| Feature | PostgreSQL | SQLite | Risk Level |
|---------|------------|--------|------------|
| Foreign Keys | ✅ Full support | ✅ Supported (must enable) | Low |
| JSON columns | ✅ JSONB | ✅ JSON (limited indexing) | Medium |
| Array types | ✅ Arrays | ❌ No native arrays | Medium |
| Upsert | ✅ ON CONFLICT | ✅ ON CONFLICT | Low |
| Date/Time | ✅ Full | ✅ Full | Low |
| Full-text search | ✅ TSVECTOR | ✅ FTS5 | Medium |

---

## 4. Redis Dependencies Analysis

### 4.1 Current Redis Usage

File: `backend/app/core/limiter.py`

```python
limiter = Limiter(
    key_func=_get_real_ip,
    default_limits=["60/minute"] if settings.RATE_LIMIT_ENABLED else [],
    enabled=settings.RATE_LIMIT_ENABLED,
    storage_uri=settings.REDIS_URL,  # redis://...
)
```

### 4.2 Redis Use Cases

| Use Case | Current Implementation | Desktop Alternative |
|----------|----------------------|---------------------|
| Rate Limiting | slowapi + Redis | **In-memory store** (single-user) |
| Caching | Not explicitly used | **SQLite + LRU cache** |
| Sessions | JWT-based (stateless) | **No change needed** |
| Task Queues | Not implemented | **Not needed for Desktop** |
| Pub/Sub | Not implemented | **Not needed for Desktop** |

### 4.3 Desktop Strategy

1. **Rate Limiting**: Disable or use in-memory storage (single user doesn't need strict limits)
2. **Caching**: Use `functools.lru_cache` or simple SQLite tables
3. **Sessions**: Keep JWT approach (works without Redis)

---

## 5. Backend Entry Point Analysis

### 5.1 Current Startup Flow

File: `backend/app/main.py`

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Validate SECRET_KEY
    # 2. Run Alembic migrations
    # 3. Create directories (avatars, tts_previews)
    # 4. Initialize TTS service
    # 5. Initialize STT service
    yield
```

### 5.2 Desktop Modifications Needed

1. **Remove automatic migrations** → Run once at first launch only
2. **Make TTS/STT optional** → Don't fail if services unavailable
3. **Add graceful error handling** → Show user-friendly messages
4. **Add health check endpoint** → For desktop runtime to verify readiness

---

## 6. Frontend Analysis

### 6.1 Current Setup

- Next.js 16 with App Router
- Static export not configured (requires server)
- API calls to `BACKEND_URL` environment variable
- WebSocket support for conversation (`/ws/conversation`)

### 6.2 Desktop Integration Options

#### Option A: Tauri (Preferred)
- ✅ Small bundle size (~10MB vs ~150MB Electron)
- ✅ Better performance
- ✅ Native Windows integration
- ⚠️ Requires Rust toolchain
- ⚠️ Need to configure Next.js for Tauri

#### Option B: Electron
- ✅ Mature ecosystem
- ✅ Large community
- ✅ Easy Next.js integration
- ❌ Large bundle size
- ❌ Higher memory usage

### 6.3 Recommended Approach: **Tauri v2**

Tauri v2 supports running a dev server or bundling the frontend. We can:
1. Build Next.js as a static-ish app
2. Run FastAPI as a sidecar process
3. Use Tauri's IPC for native features

---

## 7. External Resources & Offline Support

### 7.1 Current External Resources

File: `backend/app/services/external_resources_service.py`

- Tatoeba (sentences)
- Common Voice (audio)
- CEFR resources
- MERLIN corpus
- Other licensed sources

### 7.2 Offline Strategy

| Resource Type | Online | Offline |
|--------------|--------|---------|
| Curriculum Data | ✅ Local files | ✅ Local files |
| Vocabulary | ✅ Local + external | ✅ Local only |
| Grammar | ✅ Local files | ✅ Local files |
| Listening Exercises | ✅ AI-generated | ✅ Pre-generated cache |
| Reading Exercises | ✅ AI-generated | ✅ Pre-generated cache |
| AI Conversations | ✅ Cloud AI | ⚠️ Local Ollama (optional) |
| TTS | ✅ Local Kokoro / Cloud | ⚠️ Windows TTS / Cache |
| STT | ✅ Local Whisper / Cloud | ⚠️ Windows STT / Cache |

### 7.3 Local Data Directory

Already exists: `backend/app/data/`
- Contains curriculum, vocabulary, grammar for multiple languages
- Can be extended for offline use

---

## 8. AI Provider Architecture

### 8.1 Current Providers

File: `backend/app/services/llm_adapter.py`

- ✅ Ollama (local)
- ✅ OpenAI (cloud)
- ✅ Anthropic (cloud)
- ✅ DeepSeek (cloud)

### 8.2 Desktop Configuration

```env
# Desktop defaults
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=juba-coder

# Cloud fallback (optional)
OPENAI_API_KEY=user_provided
ANTHROPIC_API_KEY=user_provided
```

### 8.3 Ollama Detection

Desktop app should:
1. Check if Ollama is installed
2. Check if Ollama service is running
3. List available models
4. Allow user to select model
5. Gracefully degrade if Ollama unavailable

---

## 9. Authentication & User Management

### 9.1 Current System

- JWT access/refresh tokens
- Users stored in PostgreSQL `users` table
- First user can be admin (`FIRST_USER_IS_ADMIN`)
- Email verification optional

### 9.2 Desktop Mode

**Option A: Single Local User**
- Skip login screen
- Auto-create local admin account
- Store credentials in Windows Credential Manager

**Option B: Multi-Profile Support**
- Allow multiple local learners
- Switch between profiles
- Each profile has separate progress

**Recommended:** Start with Option A, add Option B later

---

## 10. File System & Data Storage

### 10.1 Current Paths (Docker)

```yaml
volumes:
  - ${DATA_PATH}/postgres:/var/lib/postgresql/data
  - ${DATA_PATH}/redis:/data
  - ${DATA_PATH}/avatars:/app/avatars
  - ${DATA_PATH}/audio:/data/audio
  - ${DATA_PATH}/tts_previews:/app/tts_previews
```

### 10.2 Desktop Paths (Windows)

```
%APPDATA%\JUBA_LISAN\
├── database\
│   └── juba_lisan.db
├── audio\
├── avatars\
├── tts_previews\
├── logs\
│   ├── app.log
│   ├── backend.log
│   └── errors.log
├── backups\
├── cache\
└── config.json
```

---

## 11. Installer Requirements

### 11.1 Installation Package

```
JUBA-LISAN-Setup.exe
├── Embedded Python Runtime (3.14)
├── Backend Code + Dependencies
├── Frontend Build (Next.js)
├── Tauri Shell
├── Default Content (curriculum, vocabulary)
└── Configuration Templates
```

### 11.2 Installation Steps

1. Install to `Program Files\JUBA LISAN\`
2. Create Start Menu shortcut
3. Create Desktop shortcut (optional)
4. Register uninstaller
5. Set file associations (`.juba-backup`)

### 11.3 First Launch

1. Create user data directory
2. Initialize SQLite database
3. Run migrations
4. Create default admin user
5. Show welcome wizard (language selection, level, goals)

---

## 12. Risk Assessment

### 12.1 High Risk Items

| Item | Risk | Mitigation |
|------|------|------------|
| PostgreSQL → SQLite migration | Medium-High | Test all queries, use abstraction layer |
| Redis removal | Medium | Replace with in-memory for single-user |
| TTS/STT without Docker | Medium | Use Windows APIs + cloud fallback |
| Next.js in Tauri | Medium | Follow Tauri v2 Next.js guide |

### 12.2 Medium Risk Items

| Item | Risk | Mitigation |
|------|------|------------|
| Ollama detection | Low-Medium | Make optional, provide clear UX |
| Offline AI features | Medium | Cache responses, allow queueing |
| WebSocket in desktop | Low | Tauri supports WebSocket |

### 12.3 Low Risk Items

| Item | Risk | Mitigation |
|------|------|------------|
| JWT authentication | Low | Works same in desktop |
| Local content files | Low | Already file-based |
| Alembic migrations | Low | Can run programmatically |

---

## 13. Recommended Desktop Architecture

```
┌─────────────────────────────────────────────────────┐
│                  JUBA LISAN Desktop                  │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │              Tauri Shell                     │   │
│  │  ┌─────────────────────────────────────┐    │   │
│  │  │         Next.js Frontend             │    │   │
│  │  │    (built, served via localhost)     │    │   │
│  │  └─────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────┘   │
│                      ↓ IPC / HTTP                   │
│  ┌─────────────────────────────────────────────┐   │
│  │         FastAPI Backend (sidecar)            │   │
│  │  ┌─────────────────────────────────────┐    │   │
│  │  │         SQLite Database              │    │   │
│  │  │         (aiosqlite)                  │    │   │
│  │  └─────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────┘   │
│                      ↓                              │
│  ┌──────────────┐  ┌──────────────┐                │
│  │   Ollama     │  │  Windows     │                │
│  │ (optional)   │  │  TTS/STT     │                │
│  └──────────────┘  └──────────────┘                │
└─────────────────────────────────────────────────────┘
```

---

## 14. Implementation Phases

### Phase 1: Foundation (Current)
- [x] Repository audit
- [ ] Create desktop architecture documentation
- [ ] Set up database abstraction layer
- [ ] Create SQLite configuration

### Phase 2: Database Migration
- [ ] Add SQLite support to database.py
- [ ] Test migrations with SQLite
- [ ] Verify all models work with SQLite

### Phase 3: Remove Redis Dependency
- [ ] Make Redis optional
- [ ] Implement in-memory rate limiter
- [ ] Test without Redis

### Phase 4: Desktop Runtime
- [ ] Set up Tauri v2 project
- [ ] Configure Next.js for Tauri
- [ ] Create backend launcher

### Phase 5: Offline Features
- [ ] Implement Ollama detection
- [ ] Add Windows TTS/STT fallback
- [ ] Cache external resources

### Phase 6: Polish & Installer
- [ ] Create Windows installer
- [ ] Add auto-update mechanism
- [ ] Final testing

---

## 15. Files Requiring Modification

### Critical Files

| File | Change Type | Priority |
|------|-------------|----------|
| `backend/app/core/config.py` | Add DESKTOP_MODE flag | High |
| `backend/app/core/database.py` | Add SQLite support | High |
| `backend/app/core/limiter.py` | Make Redis optional | High |
| `backend/app/main.py` | Add graceful degradation | High |
| `backend/alembic/env.py` | Support SQLite | Medium |
| `frontend/next.config.ts` | Configure for Tauri | High |
| New: `desktop/` | Tauri app structure | High |

### Supporting Files

| File | Change Type | Priority |
|------|-------------|----------|
| `docker-compose.yml` | No change (keep for server) | Low |
| `requirements.txt` | Add aiosqlite (already present) | Done |
| `package.json` | Add desktop scripts | Medium |
| New: `docs/DESKTOP_*.md` | Documentation | Medium |

---

## 16. Testing Strategy

### 16.1 Unit Tests
- Database connection (SQLite vs PostgreSQL)
- Model queries
- Service initialization

### 16.2 Integration Tests
- Backend startup without Docker
- Migration execution
- API health checks

### 16.3 Desktop-Specific Tests
- First launch flow
- Database initialization
- Backend health monitoring
- Shutdown cleanup
- Offline mode
- Ollama detection
- TTS/STT fallback

---

## 17. Success Criteria

✅ **Desktop application builds successfully**
✅ **Runs without Docker**
✅ **Runs without PostgreSQL**
✅ **Runs without Redis**
✅ **Works offline (core features)**
✅ **Ollama optional (not required)**
✅ **TTS/STT graceful degradation**
✅ **Clean Windows installer**
✅ **User data preserved across updates**
✅ **Proper uninstall support**

---

## 18. Next Steps

1. **Create database abstraction layer** (immediate)
2. **Test SQLite compatibility** (immediate)
3. **Make Redis optional** (immediate)
4. **Set up Tauri project structure** (phase 2)
5. **Implement backend launcher** (phase 2)
6. **Build installer prototype** (phase 3)

---

*Generated: Desktop Migration Audit v1.0*
*Project: JUBA LISAN*
*Date: 2025*
