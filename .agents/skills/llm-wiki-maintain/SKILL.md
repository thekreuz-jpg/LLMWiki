# LLM Wiki Maintain Skill

Use this skill to maintain the Wiki over time.

## Trigger

When the user asks to maintain, clean up, or audit the Wiki.

## Workflow

1. **Run the maintenance gate**:
   ```bash
   python3 scripts/wiki_tool.py doctor
   python3 scripts/wiki_tool.py build
   python3 scripts/wiki_tool.py lint
   python3 scripts/wiki_tool.py source-lint
   python3 scripts/audit_public.py
   ```
2. **Check source coverage** — Run `python3 scripts/wiki_tool.py source-coverage` to see which Raw sources are covered.
3. **Identify gaps** — Run `python3 scripts/wiki_tool.py source-delta` to find unprocessed sources.
4. **Update indexes** — Run `python3 scripts/wiki_tool.py build` to regenerate catalogs and indexes.
5. **Log maintenance** — Run `python3 scripts/wiki_tool.py log --title "Maintenance" --details "<summary>"`.

## Rules

- Run the maintenance gate before every meaningful commit.
- Keep the catalog and manifest in sync with actual notes.
- Archive stale notes rather than deleting them.
