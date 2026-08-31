---
name: windows-local-services
description: "Windows service setup, autostart, and dev-server recovery."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [Windows, services, autostart, Node.js, Postgres, Task Scheduler, NSSM]
    related_skills: [github-repo-management, hermes-remote-access]
---

# Windows Local Services

How to run and persist local services on Windows without fighting the shell.

## When to use

- You need a local Postgres instance for a self-hosted app.
- You need a Node.js bridge/worker to auto-start at logon.
- `npm run dev` or another dev server gets stuck and won't restart.

## 1. Local Postgres on Windows

### Install

If `winget`/`choco` are blocked, download the Windows installer directly:

- https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

### Connection string quirk

Local Postgres on Windows **must use `sslmode=disable`**. Without it, Node `pg` throws:

```
Error: The server does not support SSL connections
```

Use:

```
postgres://postgres:<password>@localhost:5432/<db>?sslmode=disable
```

### Create a database

From an elevated shell:

```powershell
& 'C:\Program Files\PostgreSQL\<ver>\bin\psql.exe' -U postgres -c "CREATE DATABASE <name>;"
```

## 2. Auto-start a Node.js process at logon

### Preferred: Task Scheduler (no admin required)

1. Create a batch file, e.g. `run-bridge.bat`:

```bat
@echo off
set DATABASE_URL=postgres://postgres:<pwd>@localhost:5432/<db>?sslmode=disable
set HERMES_BOARD=default
cd /d C:\path\to\bridge
node bridge.mjs
```

2. Register the task from an **elevated** PowerShell once:

```powershell
schtasks /create /tn "MyBridge" /tr "'C:\path\to\run-bridge.bat'" /sc onlogon /ru "USERNAME" /f
```

3. Verify:

```powershell
schtasks /query /tn "MyBridge"
```

### Alternative: NSSM (requires elevation to install/edit)

NSSM wraps any executable as a Windows service. Download from https://nssm.cc.

```powershell
# From elevated PowerShell
nssm install MyService "C:\Program Files\nodejs\node.exe" "C:\path\to\script.js"
nssm set MyService AppDirectory "C:\path\to\workdir"
nssm set MyService AppEnvironmentExtra "DATABASE_URL=postgres://...?sslmode=disable"
nssm start MyService
```

**Pitfall:** NSSM cannot edit an existing service without elevation. If you get `OpenService() failed: Access is denied`, rerun from an elevated shell.

## 3. Next.js dev-server lockfile recovery

On Windows, after killing `npm run dev`, the next start can fail with:

```
Unable to acquire lock at C:\...\.next\dev\lock, is another instance of next dev running?
```

Fix:

```powershell
taskkill /F /FI "TCP:3000"
Remove-Item -Force .next\dev\lock
npm run dev
```

Or from bash:

```bash
taskkill /F /PID <pid>
rm -f .next/dev/lock
npm run dev
```

## 4. Quick checks

- Postgres running: `sc query postgresql-x64-18`
- Port in use: `netstat -ano | findstr :3000`
- Kill by port PID: `taskkill /F /PID <pid>`

## References

- `references/windows-postgres-setup.md` — local Postgres install and DB creation recipes
- `references/task-scheduler-setup.md` — exact schtasks syntax and batch-file template
- `references/nextjs-lockfile.md` — lockfile recovery and stale-process cleanup
