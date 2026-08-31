# Workflow Examples

## Ingesting a New Source

1. User adds `Raw/Sources/article.md` with proper frontmatter.
2. Agent runs `python3 scripts/wiki_tool.py search-catalog --query "article topic"`.
3. Agent opens relevant compiled Wiki notes.
4. Agent creates or updates `Wiki/Concepts/article-concept.md` with:
   - `sources: [Raw/Sources/article.md]`
   - `source_count: 1`
5. Agent runs the maintenance gate.
6. Agent commits with message describing the ingest.

## Querying the Wiki

1. User asks: "What do we know about X?"
2. Agent runs `python3 scripts/wiki_tool.py search-catalog --query "X"`.
3. Agent opens the most relevant Wiki notes.
4. Agent answers, citing both the Wiki note and the Raw source.

## Maintenance Run

1. Agent runs `python3 scripts/wiki_tool.py doctor`.
2. Agent runs `python3 scripts/wiki_tool.py build`.
3. Agent runs `python3 scripts/wiki_tool.py lint`.
4. Agent runs `python3 scripts/wiki_tool.py source-lint`.
5. Agent runs `python3 scripts/audit_public.py`.
6. If all pass, agent commits any fixes.
