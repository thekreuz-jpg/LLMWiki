---
name: hermes-desktop-theming
description: "Want a desktop app theme? Use the built-in marketplace."
version: 1.0.0
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [desktop, theme, appearance, marketplace, skin, teal, settings]
    related_skills: [hermes-themes]
---

# Hermes Desktop Theming

How the Hermes **desktop app** (Electron renderer) gets its look, and the
fastest way to give a user a specific appearance.

## When to Use
- User wants a specific look on the desktop app ("a teal theme like the web
  one", "dark blue vibes", "match brand colors").
- User asks about desktop Appearance / Settings themes.
- You are about to hand-write a skin YAML or edit `presets.ts` for a desktop
  appearance request — STOP and read "Surface-first" below first.

## Surface-first — the marketplace is the easy path
When a user wants a *specific named look* on the desktop app, lead with the
**built-in theme marketplace**, NOT hand-written skins and NOT editing source.

- **Where:** Settings → Appearance → "Install theme…", OR open **Cmd-K /
  Ctrl-K** and pick "Install theme…".
- **What it is:** live search over the **VS Code Marketplace** (empty query =
  most-installed; typing filters). Pick a result → it downloads → converts →
  installs → activates in one click.
- **Why it beats a skin:** see "Skin vs DesktopTheme" below. No YAML, no source
  edit, no build.
- **Gotcha that bit a past session:** an agent told the user to hand-write a
  skin or edit `presets.ts` to get "teal" on desktop. Wrong — the marketplace
  had teal themes one search away, and a skin wouldn't have recolored the chat
  pane anyway. Inspect the real Settings surface before answering.

## Built-in desktop themes (no marketplace install needed)
Defined in `apps/desktop/src/themes/presets.ts` (`BUILTIN_THEMES`):
`nous` (glass neutrals + Nous blue — the desktop default), `midnight` (deep
blue-violet, matches web's midnight), `ember` (warm), `mono` (grayscale),
`cyberpunk`, `slate` (cool blue-gray). **There is no built-in teal** — the web
dashboard's "Hermes Teal" (`default` in `web/src/themes/presets.ts`) was never
ported to the desktop.

## Skin vs DesktopTheme (critical distinction)
- **Skin engine** (`~/.hermes/skins/*.yaml`, keyed via `display.skin`) themes
  the **CLI, TUI, and desktop chrome** — it does NOT recolor the desktop's
  React **chat pane**. So a teal skin makes the chrome teal but leaves the chat
  surface on its `DesktopTheme`.
- **DesktopTheme** (`apps/desktop/src/themes/*`) is what actually paints the
  desktop chat UI. The marketplace installs these; `presets.ts` defines the
  built-ins. Appearance grid / Cmd-K / `/skin` all read the merged registry
  (built-ins + user/marketplace themes).
- Implication: to truly match the web's "Hermes Teal" chat look on desktop, you
  need either a marketplace teal theme OR a new `teal` entry in `presets.ts` —
  a skin alone won't do it.

## When to hand-write a skin anyway
- Coordinated cross-surface palette (CLI+TUI+desktop chrome together).
- A single-color tweak to the active look: `hermes skin set <key> <hex>`
  (edits the active skin in place; never fork `default` or hand-edit
  `config.yaml` to activate — use `hermes config set display.skin <name>`).

## Pitfalls
- Don't lead desktop appearance requests with the hard code path (YAML /
  `presets.ts`). Use the marketplace unless the user explicitly wants a
  coordinated cross-surface skin.
- Skin ≠ desktop chat theme. Verify which surface the user means.
- Built-in desktop themes are a fixed small set; anything else comes from the
  marketplace or a `presets.ts` edit (requires a build).

## References
- `references/desktop-marketplace.md` — full source map of the marketplace
  pipeline (files, functions, storage key) and the built-in theme list.

## Verification
- Confirm a marketplace-installed theme shows in Settings → Appearance and
  applies live. For a skin, `hermes config get display.skin` reports the name
  and the gateway repaints within ~a second.
