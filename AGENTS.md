# LLM Wiki Agent Rules

This file governs how AI agents interact with this LLM Wiki vault.  This repository is a starter LLM Wiki for humans and agents.

## Vault Structure

- **`Raw/Sources/`** — Source material only. Never treat these as compiled notes. They are the raw input that gets processed into Wiki notes.
- **`Wiki/`** — Compiled, reusable knowledge. Only finalized, traceable notes live here.
- **`Schema/`** — Rules, conventions, and reference docs for the Wiki system.
- **`_templates/`** — Note templates for creating new sources and compiled notes.
- **`.agents/skills/`** — Agent skills for ingesting, querying, linting, and maintaining the Wiki.
- **`scripts/`** — Deterministic tooling (`wiki_tool.py`, hooks, audit).

Default workflow:
	1. Add source material to raw/sources/
	2. compile short reusable notes in Wiki/
	3. Rebuild indexes and wiki/catalog.jsonl
	4. run lint and source checks
	5. append wiki/log.md

Use scripts/wiki_tool.py as the canonical repo-local maintenance tool for build, lint, source scan, source delta, source coverage, catalog search, and log commands.

Default write locations:
- Topic hubs: wiki/Topics/
- Concepts: Wiki/Concepts/
- Entities: Wiki/Entities
- Projects: Wiki/Projects/
- Logs: Wiki/Logs/
	
## Agent Obligations

1. **Treat `Raw/Sources/` as source material, not as compiled notes.** Raw sources are inputs to be processed, not final knowledge, source-faithful.
2. **Write reusable knowledge only under `Wiki/`**. Never write compiled notes directly into `Raw/`.
3. Do not overwrite Raw source content during compilation.
4. **Keep every compiled note linked to one or more Raw sources.** Every claim in a Wiki note must be traceable back to a source in `Raw/Sources/`.
5. **Search `Wiki/catalog.jsonl` before opening broad Raw context.** The catalog is the entry point — use it to find relevant compiled notes first.
6. **Run `build`, `lint`, and source checks before commits.** The maintenance gate must pass before any meaningful commit.
7. **Do not invent citations or create unsupported claims.** If a claim can't be traced to a source, don't make it.
8. Use plain tags only
9. Use topics and sources frontmatter on compiled Wiki notes.
10. Treat source_count as derived
11. Keep compiled notes short, single-purpose, and source-traceable.
12. Query from Wiki/index.md and Wiki/catalog.jsonl before opening broad context

## Maintenance Gate

Before every meaningful commit, run:

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

After source ingestion, also run:

```bash
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
```

## Ingest Workflow

1. Put cleaned Markdown in `Raw/Sources/`.
2. Run `search-catalog` for likely related topics.
3. Open only the most relevant compiled Wiki notes.
4. Create or update focused notes in `Wiki/`.
5. Add Raw source links to `sources`.
6. Keep `source_count` accurate.
7. Run the maintenance gate.
8. Add a log entry if the ingest meaningfully changed the Wiki.

## Query Workflow

1. Start with `Wiki/index.md`.
2. Search the catalog: `python3 scripts/wiki_tool.py search-catalog --query "user topic"`
3. Open the most relevant Wiki notes.
4. Open Raw sources only when the compiled note is insufficient or the user asks for source-level verification.
5. Cite the compiled note and Raw source when the answer depends on source material.
