---
name: windows-local-app-setup
description: "Setup Windows services/apps when standard installers fail."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [Windows, Postgres, NSSM, Services]
---

# Windows Local App Setup

Use when the user needs a local Windows app/service installed and connected to startup/background operation, especially when:
- winget/choco/scoop are blocked, missing, or misconfigured
- admin/elevation is required
- the app must auto-start as a Windows service
- the target is a Node-based Hermes bridge or similar background worker

Related: `github-repo-management` for cloning repos, `hermes-agent` for Hermes install/config.

## 1. Local PostgreSQL on Windows

When `winget install PostgreSQL.*` returns "No package found" or choco is blocked by permissions:

1. Try direct installer download: `curl -L -o C:/Users/<user>/Downloads/postgresql-installer.exe https://get.enterprisedb.com/postgresql/postgresql-installer-latest-x64.exe`
2. If the downloaded file is not a real installer (small size, HTML error page), manually download from https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
3. Run installer manually or via elevated PowerShell: `Start-Process 'C:/path/installer.exe' -Verb runAs`
4. After install, the service name pattern is `postgresql-x64-<major>` or `postgresql-<major>`.
5. Create databases with the absolute `psql.exe` path: `"C:/Program Files/PostgreSQL/<ver>/bin/psql.exe" -U postgres -c "CREATE DATABASE <name>;"`.
6. Local Postgres almost always needs `sslmode=disable` in the connection string.

Pitfall: `psql` is usually not on PATH. On MSYS bash, always use the absolute path and quote it.

## 2. NSSM Service Wrapper

Use when `sc create` is insufficient, the service account needs explicit env vars, or the command is not a true Windows service.

Installation:
- If winget works: `winget install --id NSSM.NSSM`
- Else: download zip from `https://nssm.cc/release/nssm-2.24.zip`, extract `win64/nssm.exe`.

Elevated install/start:
- The NSSM CLI installer requires admin. If it returns "Administrator access is needed", launch the GUI via elevated PowerShell instead:
  `powershell -NoProfile -Command "Start-Process 'C:/path/nssm.exe' -ArgumentList 'install','<ServiceName>','<app>','<args>' -Verb runAs"`

Configuration:
- Set **AppDirectory** to the script's working directory.
- Set env vars on the **Environment** tab in the GUI, or via `nssm set <svc> AppEnvironmentExtra "<KEY>=<value>"`.
- Set startup type to auto: `nssm set <svc> Start SERVICE_AUTO_START`.

Pitfall: do not rely on shell PATH inside the service. Set `AppEnvironmentExtra` for anything the wrapped script needs.

Pitfall: when NSSM `set` returns “Administrator access is needed,” the CLI cannot modify an existing service. Either elevate PowerShell for NSSM, use a fresh admin shell, or fall back to Task Scheduler.

## 3. Auto-start fallback: Task Scheduler
If NSSM/service creation is blocked by permissions, use Task Scheduler with a batch file wrapper.

Wrapper template (`run-<app>.bat`):
```bat
@echo off
set KEY=value
cd /d C:\path\to\app\working\dir
node script.mjs
```

Create task (elevated PowerShell):
```powershell
schtasks /create /tn "TaskName" /tr "'C:\path\to
un-app.bat'" /sc onlogon /ru "USERNAME" /f
```

Verify:
```powershell
schtasks /query /tn "TaskName"
```

Notes:
- `onlogon` triggers at interactive logon.
- If `sc.exe delete <svc>` returns `FAILED 1060`, the service entry was never created; ignore.

## 4. Verification

- After installing the service, verify it starts: `nssm start <ServiceName>`.
- For Hermes bridge specifically: `curl -s 'http://localhost:3000/api/hermes/activity?take=20'` and confirm a `Bridge connected` event appears.
- For Postgres specifically: query the DB with the absolute `psql.exe` path to avoid PATH issues.

## 5. Local Postgres gotchas on Windows

- Service name pattern: `postgresql-x64-<major>`.
- Default superuser: `postgres`.
- Local connections usually require `sslmode=disable` in the URL even if other docs say `require`/`prefer`. Default `postgresql://` without explicit sslmode can fail with SSL negotiation errors on Windows-local Postgres.
- Create DBs with the absolute client path:
  `"C:/Program Files/PostgreSQL/<ver>/bin/psql.exe" -U postgres -h localhost -c "CREATE DATABASE <name>;"`

## 6. NSSM path discovery on Windows

`winget install NSSM.NSSM` can report success but leave `nssm.exe` outside the shell PATH. If `where nssm` returns nothing, search:
- `C:/ProgramData/chocolatey/lib/nssm*/win64/nssm.exe`
- `C:/Users/<user>/Downloads/...`
Or re-extract from `https://nssm.cc/release/nssm-2.24.zip`.

## 7. Next.js dev server quirks

- `npm run dev` can fail with `Unable to acquire lock` if another dev server was killed uncleanly. Fix: remove `.next` and restart.
- If port 3000 is in use by an unknown process, identify it with `netstat -ano | grep ':3000 '` before assuming the port is free.
- After adding/modifying API routes, if responses don’t change, clear `.next` and restart dev server rather than relying on hot reload.

## 8. Hermes bridge on Windows

- The bridge uses Node’s `pg` client against Postgres; set `DATABASE_URL` with explicit `sslmode=disable` for local Postgres.
- The bridge does not need `hermes` on PATH if `HERMES_BIN` is set to the full CLI path, e.g. `C:/Users/Kreuz/AppData/Local/hermes/hermes-agent/venv/Scripts/hermes`.
- If `hermes` CLI calls time out inside the bridge, the Hermes subcommand syntax may differ from what the bridge expects; the bridge has fallback attempts, but some failures are expected and non-fatal.

## 9. Windows dev dependency warning

`better-sqlite3@12.x` may emit EBADENGINE warnings under Node 21.x. They are non-fatal; if native install breaks, retry under Node 20/22/24 instead.

## 10. Task Scheduler service fallback

- Preferred order: NSSM → Task Scheduler.
- Task Scheduler task command uses the batch wrapper format: `/tr "'C:\\path\\to\
un-app.bat'"`.
- Verify with: `schtasks /query /tn "TaskName"`.
- If `sc.exe delete <svc>` returns `FAILED 1060`, the service was never created; ignore.
