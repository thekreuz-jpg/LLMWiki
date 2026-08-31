---
name: hermes-mission-control
description: "Deploy Hermes mission-control dashboards and bridge bus."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Hermes, Dashboard, Postgres, Windows, Bridge]
---

# Hermes Mission Control

Deploy a self-hosted dashboard that talks to your local Hermes agent over a shared Postgres message bus.

## When to use

- Setting up Hermy HQ or similar Hermes mission-control dashboard
- Wiring `hermes-bridge` to Postgres
- Installing the bridge as a Windows service/auto-start task
- Debugging empty kanban or failed dashboard mutations

## Prerequisites

- Node.js 20+ and npm
- PostgreSQL reachable from both web app and bridge machine
- `hermes` CLI on PATH for the bridge machine
- Google OAuth app for login

## Setup flow

### 1. Clone and install

```bash
git clone <repo-url> hermy-hq && cd hermy-hq
npm install
cp .env.example .env
```

### 2. Database

Use real Postgres. SQLite is not supported by this repo’s Prisma schema or `hermes-bridge/bridge.mjs`.

**Local Postgres on Windows:**
- If installer download fails, use an existing local install or a free cloud Postgres (Neon/Supabase).
- Create the database manually if `prisma db push` fails on create:
  ```bash
  "C:\Program Files\PostgreSQL\<ver>\bin\psql.exe" -U postgres -c "CREATE DATABASE <name>;"
  ```
- Use `sslmode=disable` for local connections.

**.env required core:**
```bash
DATABASE_URL="postgres://user:pass@localhost:5432/db?sslmode=disable"
POSTGRES_URL="postgres://user:pass@localhost:5432/db?sslmode=disable"
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="$(openssl rand -base64 32)"
GOOGLE_CLIENT_ID="..."
GOOGLE_CLIENT_SECRET="..."
ALLOWED_EMAILS="you@example.com"
NEXT_PUBLIC_OWNER_NAME="Your Name"
NEXT_PUBLIC_BASE_URL="http://localhost:3000"
HERMES_BOARD="default"
HERMES_BIN="hermes"
HERMES_WIKI="C:/path/to/wiki"
BRIEF_HOUR="7"
INTERNAL_API_SECRET="$(openssl rand -hex 32)"
CRON_SECRET="$(openssl rand -hex 32)"
```

### 3. Push schema

```bash
npx prisma db push
```

If it errors on creating the DB, create it manually with `psql` first.

### 4. Run dev server

```bash
npm run dev
```

Verify at `http://localhost:3000`. If you get a stale lock error:
```bash
# kill old node process, then remove lockfile
rm -f .next/dev/lock
```

### 5. Connect the bridge

```bash
cd hermes-bridge && npm install
DATABASE_URL='postgres://...' HERMES_BOARD=default node bridge.mjs
```

You should see `hermes-bridge up …` and a **Bridge connected** event in the dashboard activity feed.

### 6. Auto-start on Windows

NSSM often fails from non-admin shells. Use Task Scheduler instead:

```powershell
# Create hermes-bridge/run-bridge.bat first
schtasks /create /tn "HermesBridge" /tr "'C:\Users\<user>\hermy-hq\hermes-bridge\run-bridge.bat'" /sc onlogon /ru "<user>" /f
```

## Critical integration points

### Do not rely on kanban mirror from delegated contexts

`hermes kanban list --json` fails inside delegated/subagent contexts:
```
kanban: could not initialize database: delegate_task child contexts cannot mutate Kanban tasks or boards
```

**Workaround:** use `AgentRequest` as the source of truth for the dashboard. Create requests via `/api/hermes/dispatch` or `/api/tasks` (if wired), and build the UI from `AgentRequest.status`.

### The `/tasks` page may be a mock

In some forks, `/tasks` is a Notion-backed mock. Replace `src/app/api/tasks/route.ts` with real Prisma queries against `HermesTask` and `AgentRequest` if you need task creation to feed the bus.

### Real request lifecycle

1. Dashboard creates `AgentRequest` with status `queued` or `awaiting_approval`
2. Bridge polls `AgentRequest WHERE status IN ('queued','approved')`
3. Bridge runs `hermes` CLI and updates request to `done`/`failed`
4. Dashboard polls `/api/hermes/requests` for live state

## Verification

- `http://localhost:3000/api/hermes/activity` should show `Bridge connected`
- `http://localhost:3000/api/hermes/requests` should show queued work
- Bridge logs: `hermes-bridge up · board=default · poll=5000ms · mirror=30000ms`
