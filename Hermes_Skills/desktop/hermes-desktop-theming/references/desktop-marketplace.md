# Desktop app — theme marketplace mechanics

The Hermes desktop app (Electron) has a built-in theme marketplace that pulls
from the **VS Code Marketplace**. This is the easiest way for a user to get a
specific look (e.g. "teal") on the desktop — no YAML, no source edits, no build.

## Entry points
- **Settings → Appearance → "Install theme…"**
- **Cmd-K / Ctrl-K → "Install theme…"** (command palette)

## Source map (verified in repo)
- `apps/desktop/src/app/command-palette/marketplace-theme-page.tsx`
  — the Cmd-K page. Debounced live search via
  `window.hermesDesktop?.themes?.searchMarketplace(q)`. Empty query →
  most-installed; typing filters. Selecting a row installs + activates and
  stays open so the user can grab several.
- `apps/desktop/src/themes/install.ts`
  — `installVscodeThemeFromMarketplace(id)` → `api.fetchMarketplace(id)` →
  `buildThemeFromMarketplace()` → `convertVscodeColorTheme()` (in `vscode.ts`)
  → `installUserTheme()`.
- `apps/desktop/src/themes/user-themes.ts`
  — stores installed themes in localStorage (`hermes-desktop-user-themes-v1`);
  merged with `BUILTIN_THEMES` from `presets.ts` for every lookup
  (Appearance grid, Cmd-K, `/skin`).
- `apps/desktop/src/themes/presets.ts`
  — built-in desktop themes: `nous` (blue, default), `midnight`, `ember`,
    `mono`, `cyberpunk`, `slate`. **No teal** — the web dashboard's
    "Hermes Teal" (`default` in `web/src/themes/presets.ts`) was never ported
    to the desktop.

## Result
Installed marketplace themes appear in the Appearance grid, Cmd-K, and `/skin`
like native built-ins. They are VS Code themes converted to `DesktopTheme`.

## When NOT to use the marketplace
- Coordinated cross-surface palette (CLI/TUI + desktop chrome) → skin engine
  (`display.skin`, `hermes skin set <key> <hex>`).
- The desktop's React chat surface is themed by `DesktopTheme`, not by the
  skin YAML — a skin alone won't recolor the chat pane the way web's Hermes
  Teal does. For a true desktop teal, either the marketplace or adding a
  `teal` entry to `presets.ts` is needed.
