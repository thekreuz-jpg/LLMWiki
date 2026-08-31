# Session Notes: Hermes Mission Control Setup

## Local Postgres on Windows

- PostgreSQL 18 installed at `C:\Program Files\PostgreSQL\18`
- Service name: `postgresql-x64-18`
- `psql.exe` path: `C:\Program Files\PostgreSQL\18\bin\psql.exe`
- Default superuser: `postgres`
- Local connections require `sslmode=disable` in the connection string
- If installer download fails, use existing local install or cloud Postgres (Neon/Supabase)
- If `prisma db push` fails on DB creation, create DB manually first with `psql`

## Bridge Auto-Start on Windows

- NSSM installation via `winget` often fails or requires elevation unavailable from non-admin shells
- Workaround: use Windows Task Scheduler with a batch file
- Batch file location: `hermes-bridge/run-bridge.bat`
- Scheduled task name: `HermesBridge`
- Trigger: at logon
- Task Scheduler command:
  ```powershell
  schtasks /create /tn "HermesBridge" /tr "'C:\Users\<user>\hermy-hq\hermes-bridge\run-bridge.bat'" /sc onlogon /ru "<user>" /f
  ```

## Kanban Mirror Limitation

- `hermes kanban list --json` fails in delegated/subagent contexts with:
  ```
  kanban: could not initialize database: delegate_task child contexts cannot mutate Kanban tasks or boards
  ```
- This means bridge kanban mirror will not populate `HermesTask` when run from certain contexts
- Workaround: use `AgentRequest` as source of truth; wire `/api/tasks` to create both `HermesTask` and `AgentRequest` rows

## Next.js Dev Server Issues

- Stale lockfile: `.next/dev/lock`
- If server won't start after kill, remove lockfile: `rm -f .next/dev/lock`
- Port reuse: if port 3000 is in use, Next.js may use 3001 instead

## Dashboard Task Page

- Default `/tasks` page in some forks is a Notion-backed mock
- Replace with real Prisma queries to make task creation feed the `AgentRequest` bus
- Delete should only appear on tasks in "Done" column
