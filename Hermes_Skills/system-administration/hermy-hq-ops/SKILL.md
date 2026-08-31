---
name: hermy-hq-ops
description: Health-check and recover the Hermes/Hermy HQ Windows stack.
---

# Hermy HQ Ops (Windows)

Recurring health-check + recovery runbook for the local Hermes/Hermy HQ deployment.
Stable environment facts (paths, service names, ports) also live in memory; this skill owns the
*procedure and pitfalls*. Re-verify facts against memory before acting — paths can change.

## Stack & ports
- **Hermes desktop app** — `Hermes.exe` (Electron). Healthy if procs present and `hermes status` shows Nous Portal logged in.
- **Postgres 18** — service `postgresql-x64-18`, DB `hermyhq` on `:5432`, `sslmode=disable`. psql at `C:\Program Files\PostgreSQL\18\bin\psql.exe` (NOT on PATH).
- **LAN dashboard** — `hermes dashboard --host 192.168.1.69 --port 9119 --skip-build`. Auto-start Task `Hermes_Dashboard_LAN` → `start-dashboard.bat`.
- **Hermy HQ web app** — Next.js at `C:\Users\Kreuz\hermy-hq`, serves `:3000`. No auto-start task; launched manually.
- **Hermes bridge** — `C:\Users\Kreuz\hermy-hq\hermes-bridge\bridge.mjs`. Auto-start Task `HermesBridge` → `run-bridge.bat`. Needs Postgres + correct `DATABASE_URL`.

## Diagnostic runbook (in this order)
1. `hermes status` — agent env, API keys, auth providers. Confirms desktop app + Nous Portal.
2. `sc.exe query postgresql-x64-18` — expect `STATE : 4 RUNNING`.
3. Scheduled tasks (see Pitfalls re: "Ready"):
   `schtasks.exe /query /tn HermesBridge /v /fo LIST`
   `schtasks.exe /query /tn Hermes_Dashboard_LAN /v /fo LIST`
   Read **Last Result** + **Last Run Time**; `0` = clean, `0xC0000142` (-1073741510) = init failure.
4. Listening ports (use `netstat -ano | grep`, NOT PowerShell `$_` — see Pitfalls):
   `netstat -ano | grep LISTENING | grep -E ':3000|:9119|:5432'`
5. HTTP probes: `curl -s -m4 -o /dev/null -w '%{http_code}\n' http://localhost:3000` and `...:9119`.

## Recovery (validated 2026-08-18)
- **LAN dashboard down** → relaunch detached (this is what `start-dashboard.bat` does):
  `powershell.exe -NoProfile -Command "Start-Process -FilePath 'C:\Users\Kreuz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe' -ArgumentList '-m','hermes_cli.main','dashboard','--no-open','--host','192.168.1.69','--port','9119','--skip-build' -WindowStyle Hidden -WorkingDirectory 'C:\Users\Kreuz\AppData\Local\hermes\hermes-agent'"`
  Then probe `:9119` → expect `302` (redirect to login). Foreground smoke test prints `HERMES_DASHBOARD_READY port=9119`.
- **Bridge / Hermy HQ down with `28P01`** → Postgres password in `DATABASE_URL` is wrong/placeholder.
  Fix the password in BOTH `C:\Users\Kreuz\hermy-hq\.env` and `C:\Users\Kreuz\hermy-hq\hermes-bridge\run-bridge.bat`, then relaunch via `run-bridge.bat` (sets DATABASE_URL/HERMES_BOARD/HERMES_BIN/HERMES_WIKI/BRIEF_HOUR then `node bridge.mjs`). The app reads `DATABASE_URL` from `.env`.
  ⚠️ Do NOT guess or reset the Postgres password without the user's explicit go-ahead.

## Pitfalls
- **MSYS bash mangles PowerShell `$_`** — a pipeline like `Get-NetTCPConnection | Where-Object {$_...}` passed through git-bash expands `$_` as a shell variable → `...State` becomes a bogus path (`/c/Users/Kreuz.State`) and the command fails. Use `netstat -ano | grep LISTENING | grep ':PORT'` in bash instead.
- **psql not on PATH** — call `C:\Program Files\PostgreSQL\18\bin\psql.exe` by full path.
- **Task Scheduler "Ready" ≠ running** — `schtasks` shows `Status: Ready` for an idle/At-logon task that is NOT currently executing. A live task shows `Status: Running`. Judge health by ports + Last Result, not "Ready".
- **Bridge task `-1073741510`** = `0xC0000142` = process init failure at logon (env not set / crashed on connect). The *code* runs fine when launched with correct env.
- **`28P01`** = `password authentication failed for user "postgres"`. The `DATABASE_URL` password is wrong. The literal `***` placeholder in `.env`/`run-bridge.bat` is the usual cause.
- **`hermes dashboard` in desktop context** throws "Desktop IPC bridge is unavailable" (#52945). Must run the venv `python -m hermes_cli.main dashboard` with `HERMES_DESKTOP`/`HERMES_WEB_DIST`/`HERMES_SERVE_HEADLESS` stripped (exactly what `start-dashboard.bat` does) — do NOT run it from inside the Electron app shell.
- **Use `hermes dashboard`, never `hermes serve`** for the LAN web UI (per memory).

## References
- `references/healthcheck-runbook.md` — full validated command transcripts, error codes, exact restart invocations.
- `scripts/check-hermyhq.sh` — one-shot bash probe that prints a status line per component.
