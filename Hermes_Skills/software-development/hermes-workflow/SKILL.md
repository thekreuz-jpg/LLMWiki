---
name: hermes-workflow
description: >
  Dispatch patterns for governing class-of-task workflows inside Hermes:
  when to use native tool APIs vs. user CLI, how to verify capabilities,
  and how to avoid misrepresenting what the agent can execute directly.
version: "0.1.0"
author: hermes-agent
license: MIT
metadata:
  hermes:
    tags: [hermes, workflow, tool-selection, dispatch]
---

# Hermes Workflow

Use this skill whenever the task involves **Hermes-native operation**:
skills, sessions, config/cron/kanban, MCP, tooling, slash commands,
profiles, memory, gateway, etc.

## Core rule: prefer native Hermes tools first

For Hermes-native tasks, order of execution should be:

1. **Native tool API** — if a first-class tool exists, use it directly.
   Examples: `skills_list`, `skill_view`, `skill_manage`, `terminal`,
   `read_file`, `session_search`, `memory`, `cronjob`, etc.
2. **Skill / reference guidance** — if an installed skill documents an
   established procedure for this class of task, follow it.
3. **Terminal / user CLI** — only when no native tool or skill path
   exists or when the action must run on the user’s local machine
   (e.g. installing Hermes itself, running local dev servers).
4. **Manual user workaround** — only when 1–3 are unavailable and the
   user is explicitly blocked. Always explain why.

## Why this matters

Auto-escalating to `terminal(..., command="hermes ...")` without checking
available tools first:
- wastes turns on failed `command not found` calls
- offloads trivial work to the user
- creates false impressions about what the agent can/cannot do
- burns context on retry loops instead of direct dispatch

## Capability probe pattern

If unsure whether a tool exists, do **not** guess from documentation or
from another agent’s toolset. Use the Hermes tool inventory or list-style
queries. Avoid blindly running CLI commands in a random environment
(Docker backend, SSH host, etc.) to discover Windows Hermes behavior;
those paths return generic failures like `command not found` rather than
informative errors.

## Windows / multi-environment nuance

- This session may run inside Docker/WSL while the user runs Hermes on
  Windows. Do **not** assume toolset parity between the session backend
  and the user’s install.
- For Windows-local Hermes commands (Windows Terminal, PowerShell, or
  Hermes desktop embedded terminal), ask the user to run them directly
  **only** after confirming that no native Hermes tool path exists for
  the same intent.
- When asking the user to run a command, state explicitly that it must
  run on their **Windows machine**, not inside the Hermes session
  backend, and why.

## Skill/catalog tasks

For skill listing, inspection, and management:

- **Installed skills** → `skills_list`
- **Inspect skill** → `skill_view(name)` then linked `file_path`
- **Manage** → `skill_manage(...)`: create/edit/patch/delete
- **User CLI fallback** → only when the user wants to install from the
  upstream catalog and no native install/write path is available.
  In that case, guide them with the exact `hermes skills install ...`
  command and note it must run on their Windows Hermes.

## Anti-patterns

- Do not say “I can’t run `hermes skills list` from here” when a native
  tool like `skills_list` already exists.
- Do not loop on failed `terminal(command="hermes ...")` calls in
  non-Hermes environments.
- Do not conflate Docker/WSL `/workspace` with the user’s real Hermes
  profile directory (`C:\Users\<user>\AppData\Local\hermes\`).

## Related

- `hermes-agent` — setup, config, providers, troubleshooting
- `hermes-desktop-plugins` — UI/plugin extensions
- `hermes-windows-config` — Windows-specific path/gateway quirks
