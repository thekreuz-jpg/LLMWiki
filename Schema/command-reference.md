# Command Reference

## wiki_tool.py Commands

### `doctor` — Health Check

Non-mutating check for vault structure and basic counts.

```bash
python3 scripts/wiki_tool.py doctor
```

### `build` — Generate Catalog and Indexes

Regenerates `Wiki/catalog.jsonl`, `Wiki/index.md`, and per-folder indexes.

```bash
python3 scripts/wiki_tool.py build
```

### `lint` — Validate Wiki Notes

Validates compiled Wiki note frontmatter, allowed tags, source links, and `source_count`.

```bash
python3 scripts/wiki_tool.py lint
```

### `source-scan` — List Raw Sources

Lists all Raw sources and their processing state.

```bash
python3 scripts/wiki_tool.py source-scan
python3 scripts/wiki_tool.py source-scan --update --accept-covered
```

### `source-lint` — Validate Sources

Validates source frontmatter and checks that processed sources have Wiki coverage.

```bash
python3 scripts/wiki_tool.py source-lint
```

### `source-delta` — Unprocessed Sources

Shows Raw sources not represented in the manifest.

```bash
python3 scripts/wiki_tool.py source-delta
```

### `source-coverage` — Coverage Report

Shows which Raw sources are covered by compiled Wiki notes.

```bash
python3 scripts/wiki_tool.py source-coverage
```

### `search-catalog` — Search Wiki Notes

Searches compiled Wiki notes through the catalog.

```bash
python3 scripts/wiki_tool.py search-catalog --query "llm wiki"
```

### `log` — Append Log Entry

Appends a short entry to `Wiki/Logs/log.md`.

```bash
python3 scripts/wiki_tool.py log --title "Title" --details "Details"
```

## audit_public.py — Pre-commit Audit

Fails on obvious secrets, machine-local paths, private keys, and plugin/cache state.

```bash
python3 scripts/audit_public.py
```

## install_hooks.sh — Install Git Hooks

Installs the pre-commit hook that runs the maintenance gate.

```bash
bash scripts/install_hooks.sh
```
