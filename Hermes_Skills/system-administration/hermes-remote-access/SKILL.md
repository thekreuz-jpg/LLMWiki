---
name: hermes-remote-access
description: Reach Hermes dashboard from another machine safely.
version: 2.2.0
author: Hermes (autonomous curator)
license: MIT
---

# Hermes Remote Access (web dashboard)

## Key facts (verified live, Aug 2026 — desktop-app install on Windows 10)

- Default bind is **loopback only**: `--host 127.0.0.1`, default port **9119**.
- As of the **June 2026 hardening**, `--insecure` is a **DEPRECATED / NO-OP** — a
  non-loopback bind ALWAYS requires an auth provider (basic auth or OAuth). Don't
  suggest `--insecure` opens it up; it does not.
- **The Hermes DESKTOP APP runs `hermes serve` (headless), which DISABLES the web UI**
  ("Headless backend (hermes serve): web UI disabled — use `hermes dashboard` for the
  browser UI."). So the browser dashboard is a **SEPARATE `hermes dashboard` process**,
  NOT auto-bound by the desktop app after reboot. After a reboot you MUST launch it.
- The Hermes terminal shell (when spawned by the desktop app) **inherits
  `HERMES_DESKTOP=1` + `HERMES_WEB_DIST=...app.asar...` + `HERMES_SERVE_HEADLESS`**.
  A `hermes dashboard` launched in that shell WITHOUT stripping those vars serves the
  Electron *renderer* in the browser → "Desktop IPC bridge is unavailable" (issue #52945).
  **You MUST strip those three vars before launching** (see mandated command).

## Mandated launch command (LAN, desktop-app install)

```
cd "C:\Users\Kreuz\AppData\Local\hermes\hermes-agent"
env -u HERMES_DESKTOP -u HERMES_WEB_DIST -u HERMES_SERVE_HEADLESS \
  "./venv/Scripts/python.exe" -m hermes_cli.main dashboard \
  --no-open --host 192.168.1.69 --port 9119 --skip-build
```

**Launch it DETACHED** so it survives Hermes terminal/session resets. A tracked
`terminal background=true` job is parented to the Hermes shell and gets **reaped when
this session's context resets** — that is exactly what silently dropped the live
connection mid-session. Use `Start-Process` from a standalone PowerShell so the
process is parented to the OS, not to the Hermes shell:

```powershell
# launch-dashboard.ps1  (run: Start-Process powershell -File <this-file>)
Remove-Item Env:HERMES_DESKTOP        -ErrorAction SilentlyContinue
Remove-Item Env:HERMES_WEB_DIST       -ErrorAction SilentlyContinue
Remove-Item Env:HERMES_SERVE_HEADLESS -ErrorAction SilentlyContinue
& "C:\Users\Kreuz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" `
  -m hermes_cli.main dashboard --no-open --host 192.168.1.69 --port 9119 --skip-build
```

Expect `HTTP 302` (auth redirect) on a bare GET — that means it's up. The dashboard may
spawn a child worker (uv python); that's normal. Do NOT launch a second instance.
For a reboot-proof setup see `references/windows-auto-start.md`.

Auth: put creds in `C:\Users\Kreuz\AppData\Local\hermes\.env` (install home is
`AppData\Local\hermes`, NOT `~/.hermes`):
```
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=admin
HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=<strong password>
HERMES_DASHBOARD_BASIC_AUTH_SECRET=<openssl rand -base64 32>
```

## Options

### Option A — SSH tunnel (most secure, no auth provider needed)
Keep the dashboard on loopback (`--host 127.0.0.1`); tunnel from the other machine.
Still launch the (sanitized) dashboard process first — the desktop app will not do it.
Requires OpenSSH Server on the Windows host
(`Settings → Apps → Optional features → OpenSSH Server`).

### Option B — bind to LAN IP with auth gate (trusted LAN only)
Use the **mandated launch command** above (it already binds `192.168.1.69`). Reach it
at `http://192.168.1.69:9119`. Optionally layer Caddy + IP allowlist. Never expose to
the open internet without the proxy.

## Verification
- From the host or other PC: `curl -s -o /dev/null -w "%{http_code}" http://192.168.1.69:9119`
  → expect `302` (auth redirect) then login behind creds. Blank refusal = not up.
- `hermes dashboard --status` lists running dashboard processes.

## Pitfalls (learned the hard way)
- **NEVER rely on `terminal background=true` to keep a server alive.** It is tracked by
  the Hermes session and is reaped when the session/terminal context resets (interruption,
  app restart, "out of band" mid-turn). The user will see the service vanish with no
  explicit kill. Always launch long-lived servers DETACHED via `Start-Process` (see
  Mandated launch command). Verify with `netstat`/`curl` afterwards, not by trusting the
  background handle.
- **MUST launch `hermes dashboard` as a separate process.** The desktop app does NOT
  auto-bind the browser dashboard after reboot (its `serve` backend disables web UI).
  The earlier "DO NOT launch standalone — let the app own it" guidance was WRONG for
  this setup and caused a long dead-end loop.
- **ALWAYS `env -u HERMES_DESKTOP -u HERMES_WEB_DIST -u HERMES_SERVE_HEADLESS`** when
  launching. Skipping this → Electron renderer served in browser → "Desktop IPC bridge
  is unavailable". This is the #1 cause of the dashboard failing.
- Don't trust "it connected once" — that was a sanitized launch. Unsanitized launches
  collide on 9119 and break the bridge.
- Kill stale dashboards before relaunching: kill BOTH the parent (venv python) and the
  child worker (uv python) PIDs, then start one clean sanitized instance.
- Install home is `C:\Users\Kreuz\AppData\Local\hermes` (NOT `~/.hermes`).
- Windows terminal backend is MSYS bash (POSIX). Use POSIX paths/syntax, not PowerShell.
- With the `Hermes_Dashboard_LAN` AtLogOn task in place (and auto-login if you want it
  pre-login), the dashboard+agent server COMES BACK after reboot — you do NOT need to
  relaunch manually. Verify post-reboot with `netstat -ano | findstr 9119` + the curl 302
  probe below.
- VERIFY the actual architecture with a process tree before assuming a client/server split.
  `Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -like '*hermes_cli*'}` showed
  ONLY `dashboard` running (no `hermes serve`) while chat worked — proving the dashboard IS
  the server. Don't add a redundant `hermes serve` task on 9119.

## Desktop app remote mode (correction to earlier advice)
The desktop app is **NOT local-only**. Its `AGENTS.md` documents a `local ↔ remote ↔
cloud` connection mode ("connection/mode apply" is a soft re-home, not a cold start),
and `hermes pairing` (`list|approve|revoke|clear-pending`) mints/approves access codes
for another machine to connect to the agent backend. So a desktop app installed on the
*other* PC can operate the agent PC in **remote mode** — it is a valid alternative to the
web UI, not a dead end. Earlier "the desktop app is local-only, use the web UI" guidance
was WRONG. Both clients (desktop remote mode + web dashboard) talk to the same backend and
can coexist. Pick based on preference: browser tab (web UI) vs native app (desktop remote
mode). Neither removes the need for a running backend on the agent PC.
- **Feature-parity claims from other LLMs are unverified — verify before repeating.** E.g.
  a summary claiming "Web UI has voice input, desktop app doesn't" is oversimplified: voice
  is a BACKEND capability (`config_defaults.py` ships faster-whisper STT + edge/elevenlabs/
  openai/mistral/gemini TTS providers) which either client can route to. Treat feature lists
  from chat models as hypotheses; confirm in source (`apps/desktop/`, `hermes_cli/`) before
  asserting them.

## Auto-start (survives reboot)
- **`hermes dashboard` IS the agent server.** Verified live (Aug 2026): with the desktop
  app closed, a process tree showed ONLY `hermes_cli.main dashboard --host 192.168.1.69
  --port 9119` running — NO `hermes serve` process — yet chat worked end-to-end. The
  dashboard command runs the agent inline; it is NOT a thin client to a separate backend.
  Launching the dashboard (singular) is sufficient. Do NOT also run a separate
  `hermes serve` on 9119 — it would spawn a second agent and fight the session store.
- A `Hermes_Dashboard_LAN` scheduled task (AtLogOn, user Kreuz) already exists and runs
  `launch-dashboard.ps1` (env-sanitized, detached). It brings the dashboard+agent server
  back after logon+reboot, and chat works with NO separate backend needed.
- **Pre-login (boot screen, before any manual login):** the AtLogOn task only fires after
  a user logs in. To get the dashboard up at the boot screen, enable Windows auto-login for
  `Kreuz` (writes password to Winlogon registry; see `scripts/set-autologon.ps1`). Do NOT
  try to run the dashboard as SYSTEM "whether logged on or not" — at boot there's no user
  profile/network fully up and the launch tends to fail the same way the IPC-bridge bug
  did. Auto-login is the low-risk path. See `references/windows-auto-start.md`.
- A separate `Hermes_Gateway` scheduled task handles the messaging gateway independently
  of the desktop app — leave it alone.
- Exact scripts + task-creation command: see `references/windows-auto-start.md`.

## Reference files
- `references/windows-auto-start.md` — detached-launch `.ps1`, `Start-Process` incantation,
  `Hermes_Dashboard_LAN` scheduled-task recipe, firewall note, and the (corrected) no-gap
  backend architecture.
- `scripts/set-autologon.ps1` — enable Windows auto-login (local secure-prompt; password
  never leaves the machine) so the AtLogOn task fires at the boot screen. Run on the agent PC.
Overlaps with bundled `hermes-agent` skill (stale on `--insecure` and on the desktop
dashboard-binding behavior). Trust THIS skill for remote-access behavior.
