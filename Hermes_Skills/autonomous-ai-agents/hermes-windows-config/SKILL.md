---
name: hermes-windows-config
description: "Windows-specific Hermes configuration: workspace path gotchas, Docker backend setup, and remote gateway access for the desktop app."
version: 1.0.0
author: Hermes Agent + Kreuz
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [windows, config, docker, gateway, remote]
---

# Hermes Windows Config

Windows-specific Hermes setup behaviors that are not obvious from the docs.

## Workspace path resolution

When `terminal.cwd` is set to `/workspace` in `config.yaml`, on Windows under the bundled git-bash/MSYS environment this path does **not** resolve to `C:\Users\<user>\workspace`. Instead, it often resolves relative to the Hermes git checkout:

```
C:\Users\Kreuz\AppData\Local\hermes\git\workspace
```

### Verify the real path
```bash
pwd
cygpath -w /workspace
```

### Fix
Either create the directory in the resolved location, or set `terminal.cwd` to an explicit Windows-style path such as `C:/Users/Kreuz/workspace`.

## Docker backend

### Prerequisites
- Docker Desktop for Windows with WSL 2 backend.

### Config change
```yaml
terminal:
  backend: docker
  cwd: /workspace     # must exist inside container or be mounted
  docker_mount_cwd_to_workspace: false
```

### Run example
```bash
docker build -t hermes-agent .
docker run -it --rm \
  -v "C:\Users\Kreuz\AppData\Local\hermes:C:\Users\Kreuz\AppData\Local\hermes" \
  -v "C:\Users\Kreuz\workspace:/workspace" \
  -e HERMES_HOME=C:\Users\Kreuz\AppData\Local\hermes \
  hermes-agent
```

## Python PATH ambiguity on Windows (local terminal backend)

When `terminal.backend` is `local`, `python` may resolve to Hermes's bundled venv interpreter before any system Python. If a tool requires a newer Python version, the version-gate failure will still reference an older system interpreter even after installing a newer one.

### Why it happens
- `where python` returns Hermes's venv first.
- A fresh `terminal()` shell does not inherit env files by default.
- Writing `LAST30DAYS_PYTHON=...` to `~/.config/last30days/.env` does not automatically populate the next shell's environment.

### Fix
Use the explicit Windows interpreter path instead of relying on PATH or env files:

```powershell
# Verify what python resolves to
where python

# Locate installed versions
py -0

# Explicit invocation for tools requiring Python 3.12+
& 'C:\Users\Kreuz\AppData\Local\Programs\Python\Python312\python.exe' script.py
```

Make it the default invocation path for any skill or tool that hard-fails its Python version gate despite a newer install being present.

## last30days Windows setup

This skill's Windows quirks are significant enough to call out explicitly:

### First-run gate requires `SETUP_COMPLETE=true`
The `last30days` first-run check is a literal grep for `SETUP_COMPLETE=true` in `~/.config/last30days/.env`:
```bash
grep -q "SETUP_COMPLETE=true" ~/.config/last30days/.env 2>/dev/null && echo "1" || echo "FIRST_RUN_DETECTED"
```
Without that exact line, setup treats every run as a first run and forces the full browser-cookie wizard.

### `.env` must be `KEY=VALUE`, not cookie JSON
If you paste the raw cookie JSON array exported from the browser, the skill will not parse it. Use this shape:
```env
SETUP_COMPLETE=true
AUTH_TOKEN=***
CT0=***
```

### Python 3.12+ interpreter
The engine requires Python 3.12+. On Windows, the default `python` may resolve to an older venv, so explicitly invoke:
```bash
/c/Users/Kreuz/AppData/Local/Programs/Python/Python312/python.exe
```
and export `LAST30DAYS_PYTHON` to that path for the invocation.

### Save-dir path behavior under git-bash/MSYS
Saved artifacts may appear under a `/c/Users/Kreuz/.config/last30days/...` style path rather than a clean Windows path. This does not break execution, but be aware that the on-disk path shown in output may start with `/c/`.

## Remote gateway / desktop app

The Hermes desktop app can drive a remote Hermes instance via per-profile remote-gateway login.

### Requirements
1. Gateway service running on the host: `hermes gateway run` or `hermes gateway install && hermes gateway start`
2. The gateway must be exposed on the LAN. Check config for bind address/port or forward with your tunnel/firewall rule.
3. Strong auth set on the profile.
4. On the remote PC, install the Hermes desktop app and use its remote-gateway login flow to point it at the host gateway.

## Web dashboard LAN binding (hermes dashboard)

`hermes dashboard` is the web admin UI. By default it binds to `127.0.0.1` (loopback) only, so no other machine can reach it. For the exact launch command, credential setup, firewall rule, and verification probe, see `references/dashboard-lan.md`.

### Quick gotchas (all hit in practice)
- **Non-loopback bind engages the auth gate.** As of the June 2026 hardening, `--insecure` is a NO-OP (no longer disables auth). A LAN bind always requires basic auth or OAuth; `GET /` returns `302 /login?next=%2F`.
- **Wrong `.env` path on Windows.** The dashboard reads `$HERMES_HOME/.env` (`C:\Users\Kreuz\AppData\Local\hermes\.env`), NOT `~/.hermes/.env`. Appending creds to the wrong file silently writes nothing.
- **Windows Firewall blocks inbound 9119 from other PCs.** A local `curl` to the LAN IP works (same-host traffic), but a different machine is dropped unless you add an inbound allow rule on the **Private** profile. `New-NetFirewallRule` must run in **Administrator PowerShell** — Hermes' terminal is non-elevated and returns `Access is denied` (exit 5).
- **`netstat` in MSYS bash is unreliable** for Windows listeners; confirm the socket with `powershell.exe -Command "Get-NetTCPConnection -LocalPort 9119"`.
- **Port is 9119**, not 9199 (easy read-back typo).

## Browser-based login limits (X/Twitter)

Cookies exported from the browser cannot fully restore authenticated sessions inside Hermes's browser tool.

### Why direct cookie import fails
- `auth_token` is `httpOnly`
- `__cf_bm` is `httpOnly`
These are set by the server and cannot be written from JavaScript via `document.cookie`, so pasted cookie JSON will not make a browser session authenticated.

### Confirmed behavior
- Loading `x.com` in the Hermes browser shows the login form
- Non-`httpOnly` cookies can be set via JS, but the critical session cookies cannot
- An API probe from the browser session without proper cookies will not authenticate

### Practical workaround on Windows
Do not attempt browser automation login. Instead:
- Export `auth_token` and `ct0` from your logged-in browser
- Provide them to CLI-capable tools via `.env` files or environment variables
- For `last30days` specifically, write them to `C:\Users\Kreuz\.config\last30days\.env` as `AUTH_TOKEN=...` and `CT0=...`
- For X automation, use a tool/library that accepts raw cookies directly rather than relying on browser cookie stores

## Native Windows binaries from git-bash/MSYS

When invoking Windows-native executables from the Hermes bash terminal, MSYS path translation can break them. Use Windows-style paths for those invocations:

```bash
# Correct: explicit Windows-style path to a native binary
'C:/Program Files/PostgreSQL/18/bin/psql.exe' -U postgres -h localhost -c "SELECT 1;"

# Correct: explicit Windows-style path to the Hermes venv interpreter
'C:/Users/Kreuz/AppData/Local/hermes/hermes-agent/venv/Scripts/hermes' status
```

MSYS-style paths like `/c/Program Files/...` or `/c/Users/...` will cause Windows-native binaries to fail with "file not found" or "cannot change to" errors.

## Local Postgres + Hermy HQ / hermes-bridge on Windows

### Verified working stack
- Postgres installed via EDB/installer
- Service name: `postgresql-x64-18`
- Local DB URL shape: `postgres://postgres:<password>@localhost:5432/<dbname>`
- Prisma push: `npx prisma db push` in the repo root
- Bridge: `cd hermes-bridge && npm install && DATABASE_URL='postgres://...' HERMES_BOARD=default node bridge.mjs`

### Windows pitfalls
- If `winget`/`choco` installer access is blocked, use the EDB installer directly; the resulting service still listens on `5432` by default.
- If `psql` is not on PATH from bash, use the absolute Windows path above. Do not rely on `service` or `systemctl` on Windows; use `sc query <service>`.
- The bridge hard-requires a direct `postgres://` URL. `prisma://` or `postgresql://` over Prisma Accelerate is rejected by `bridge.mjs`.
- If the Hermes CLI call inside the bridge times out, it's often the parent Hermes runtime blocking `hermes kanban ...` rather than bridge config. That does not stop other mirror loops (`mirrorCrons`, `mirrorHealth`, `mirrorWiki`, `mirrorCost`).

### Persisting the bridge on Windows
- The repo ships a macOS `launchd` plist only.
- On Windows, run the bridge via Task Scheduler or NSSM as a logon-triggered process with:
  - Working directory: `<repo>/hermes-bridge`
  - Env: `DATABASE_URL=<same as website>` and `HERMES_BOARD=default`
  - Command: `node bridge.mjs`
- Verify from the dashboard `/hermes` activity feed: a "Bridge connected" event confirms the bus loop is live.

## Git Bash vs PowerShell vs cmd for Hermes commands

- Use **bash/MSYS** syntax for shell work (`ls`, `find`, `grep`, `&&`, `|`, single quotes).
- Use **Windows-native paths** when calling native Windows executables from bash (`C:/Users/...`, `C:/Program Files/...`).
- Do **not** use PowerShell builtins (`Get-ChildItem`, `$env:FOO`, `Select-String`) in bash terminal calls — they will fail.
- `cd` is a bash builtin and path translation works; native-tool args do not.
