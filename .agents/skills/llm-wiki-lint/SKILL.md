# LLM Wiki Lint Skill

Use this skill to validate the Wiki's integrity.

## Trigger

When the user asks to check, lint, or validate the Wiki.

## Workflow

1. **Run the full maintenance gate**:
   ```bash
   python3 scripts/wiki_tool.py doctor
   python3 scripts/wiki_tool.py build
   python3 scripts/wiki_tool.py lint
   python3 scripts/wiki_tool.py source-lint
   python3 scripts/audit_public.py
   ```
2. **Report findings** — Summarize any failures or warnings.
3. **Fix issues** — Correct frontmatter errors, broken source links, or missing catalog entries.
4. **Re-run** — Verify all checks pass after fixes.

## Checks

- Compiled Wiki notes use allowed tags
- `source_count` matches `len(sources)`
- Source links point to existing files
- Raw source notes have required frontmatter
- Catalog and manifest are up to date
- No secrets or private paths in commits
