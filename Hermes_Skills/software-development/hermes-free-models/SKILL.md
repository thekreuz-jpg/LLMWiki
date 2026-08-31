---
name: hermes-free-models
description: "Switch Hermes free model; verify the live portal list first."
version: 1.0.0
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [model, free, nous, openrouter, switching, provider]
    related_skills: [hermes-agent, hermes-desktop-theming]
---

# Hermes Free-Model Selection & Switching

How to pick a free (no-credit) model and switch the active Hermes model — the
durable, verified way. The curated free list in the repo is STALE; trust the
live portal endpoint and the interactive picker instead.

## When to Use
- User asks "what's the strongest free model" / "switch me to a better free model".
- User wants to change the active model (config `model.default` + `model.provider`).
- A `:free` slug the user picked returns HTTP 404 "requires available credits".

## Source of truth for what is FREE (critical)
The repo's curated free list (`hermes_cli/models.py`, the `_PROVIDER_MODELS["nous"]`
free-tier tuples, ~lines 95-101) is **stale and not authoritative**. It has listed
models that are no longer free (confirmed case: `inclusionai/ring-2.6-1t:free`
returned HTTP 404 "requires available credits" from the Nous backend).

**Verify against the LIVE portal endpoint instead:**
```
GET https://portal.nousresearch.com/api/nous/recommended-models
```
The `freeRecommendedModels` array is the current free roster (each entry has
`modelName`, `tokenPrice: "$0.00/1M"`). This is what the interactive picker
uses to filter free-tier options. Fetched 2026-08-11 the live free list was:
`upstage/solar-pro4:free`, `tencent/hy3:free`, `poolside/laguna-s-2.1:free`
(262K ctx), `stepfun/step-3.7-flash:free` (vision), `poolside/laguna-xs-2.1:free`.

Rule: if a model is NOT in `freeRecommendedModels`, assume it is NOT free — do
not recommend or set it, even if it appears in the curated list.

## Why the interactive picker hides some "free" models
For free-tier users, `partition_nous_models_by_tier` (`hermes_cli/models.py:~671`)
splits models by the live OpenRouter pricing map: only zero-cost (`prompt` and
`completion` == 0) models are selectable; others show grayed/unavailable. So a
model absent from the picker is absent for a real reason. Trust the picker's
filtering over the hardcoded curated list.

## How to switch the active model (verified working)
`HERMES_HOME` is the install home (Windows: `C:\Users\Kreuz\AppData\Local\hermes`,
NOT `~/.hermes`). Config: `<HERMES_HOME>/config.yaml`, under `model:`.

```bash
hermes config set model.default "upstage/solar-pro4:free"
hermes config set model.provider nous
```
- A direct config write bypasses the picker's free-tier filter (so it can set a
  model the picker hides) — but if that model isn't actually free server-side,
  the NEXT API call 404s. Only set slugs you've confirmed in `freeRecommendedModels`.
- **Restart required:** a `/new` does NOT reload config. The Hermes process must
  be relaunched for `model.default` to take effect. Confirm on the next turn that
  the active model line shows the new slug.

## Strongest free reasoning pick (as of 2026-08-11)
`upstage/solar-pro4:free` is the largest/general free model; the two Poolside
"Laguna" models are smaller coding-focused; `stepfun/step-3.7-flash:free` adds
vision. Re-verify via the live endpoint before asserting "strongest" — the roster
drifts. Do NOT rank by the curated list's parameter counts; that list is stale.

## Pitfalls
- Never recommend a `:free` slug from the curated list without checking the live
  endpoint — it will 404 and you'll have to revert.
- `hermes config set` writes to `HERMES_HOME/config.yaml`; on Windows that's
  `AppData\Local\hermes`, not `~/.hermes`.
- Telling the user "the picker is wrong, set it manually" is backwards — the
  picker filters by live pricing and is usually right; the curated list is wrong.
- **Third-provider credential errors look like "out of credits" but aren't.** A
  Gemini HTTP 401 ("rejected this API key's type") means the Standard key was
  deprecated — create an Auth key. A 404 ("no longer available") means the model
  slug is dead — pick a newer one. Don't confuse these with actual quota
  exhaustion (HTTP 429). See `references/gemini-key-migration.md`.

## References
- `references/live-free-list.md` — the endpoint, parsing, and the last fetched
  free roster snapshot (with date) for offline confirmation.
- `references/gemini-key-migration.md` — Google Gemini Standard→Auth key
  migration: timeline, symptoms, fix, and how to distinguish 401/404/429.

## Verification
After switching: relaunch Hermes, send one message, confirm the active-model
metadata in the session header matches `model.default` and no 404 occurs.
