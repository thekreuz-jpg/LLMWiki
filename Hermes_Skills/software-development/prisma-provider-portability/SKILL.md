---
name: prisma-provider-portability
description: "Verify Prisma apps before switching DB providers."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [prisma, postgres, sqlite, portability]
---

# Prisma Provider Portability

Do not promise a provider switch by changing `.env` alone. Inspect the stack first.

## Required inspection pass

Before switching providers, check ALL of these:

1. `prisma/schema.prisma` datasource `provider`
2. Raw SQL anywhere: `$1` placeholders, `ON CONFLICT`, `JSONB`, `@@index`
3. Auth adapters: NextAuth `@prisma-adapter` may assume Postgres behavior
4. Field types: `DateTime` vs `Int`/`String`, `cuid()`/`uuid()`, `Json` vs `String`

## Decision matrix

| Signal | Verdict |
|--------|---------|
| `provider = "postgresql"`, raw SQL, `ON CONFLICT`, `@@index` | Rewrite required. Not env-configurable. |
| `provider = "sqlite"` already, no raw SQL | Env change may work. |
| Mixed Prisma + `pg`/`mysql2` clients | Full driver port needed. |

## Prisma 6+ note

Prisma 6+ dropped SQLite provider support. Switching to SQLite requires schema, driver, and likely code changes — not just `.env`.

## Safe alternatives when Postgres is unavailable

- Cloud Postgres: Neon, Supabase, Vercel Postgres, Railway — single connection string.
- Manual local Postgres: EDB installer, `winget`/`choco` where available, or portable `initdb` + `pg_ctl`.

## Pitfalls

- `better-sqlite3` in `package.json` does not mean Prisma uses it; often an unrelated direct dependency.
- Windows Postgres installers frequently fail silently or need admin rights; verify installer access before assuming availability.
