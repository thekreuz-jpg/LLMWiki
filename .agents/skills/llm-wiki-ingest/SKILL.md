# LLM Wiki Ingest Skill

Use this skill to ingest new Raw sources into the Wiki.

## Trigger

When the user adds a new source to `Raw/Sources/` or asks to process unprocessed sources.

## Workflow

1. **Identify unprocessed sources** — Run `python3 scripts/wiki_tool.py source-delta` to find Raw sources not yet in the manifest.
2. **Search the catalog** — For each source, run `python3 scripts/wiki_tool.py search-catalog --query "<source topic>"` to find related Wiki notes.
3. **Open relevant Wiki notes** — Only the most relevant compiled notes.
4. **Create or update Wiki notes** — Write focused notes in `Wiki/` with:
   - Proper frontmatter (see `Schema/frontmatter-schema.md`)
   - `sources` linking back to the Raw source
   - `source_count` matching the number of sources
5. **Update the source manifest** — Run `python3 scripts/wiki_tool.py source-scan --update --accept-covered`.
6. **Run the maintenance gate**:
   ```bash
   python3 scripts/wiki_tool.py build
   python3 scripts/wiki_tool.py lint
   python3 scripts/wiki_tool.py source-lint
   python3 scripts/audit_public.py
   ```
7. **Log the change** — If the ingest meaningfully changed the Wiki, run:
   ```bash
   python3 scripts/wiki_tool.py log --title "Ingest: <source>" --details "<summary>"
   ```

## Rules

- Never write compiled notes directly into `Raw/Sources/`.
- Every claim in a Wiki note must be traceable to a source.
- Keep `source_count` accurate.
- Do not invent citations.
