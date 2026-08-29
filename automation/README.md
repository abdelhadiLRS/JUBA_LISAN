# automation/README.md

Lightweight development automation for JUBA LISAN. No LLM/Ollama dependency —
the scripts only orchestrate what the repository already provides and never
assume a tool exists: each one detects the package manager, scripts, and
local environments before running anything.

## Scripts

- `status.ps1` — branch, sync state, working tree, roadmap phase summary, and
  the canonical version at a glance.
- `test.ps1` — frontend lint, typecheck, and unit tests when `node_modules`
  exists; backend `pytest` only when a local Python venv is detected
  (otherwise skipped — CI runs backend tests).
- `build.ps1` — frontend production build when the `build` script exists.
- `develop.ps1` — the one-click cycle: pull `main` (fast-forward only),
  confirm unexpected local changes, run `test.ps1` and `build.ps1`, then
  interactively commit and push — but never commits or pushes after a failed
  check, and never force-pushes.

## Usage (Windows PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File automation\status.ps1
powershell -File automation\test.ps1
powershell -File automation\build.ps1
powershell -File automation\develop.ps1
```

## Safety rules encoded in the scripts

- Pulls use `--ff-only` so local history is never rewritten.
- Build or test failure blocks commit and push.
- Nothing is deleted, reset, or overwritten automatically.
- Pushing is an explicit confirmation step, never an automatic side effect.
