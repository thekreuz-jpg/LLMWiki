# LLM Wiki Query Skill

Use this skill to query the Wiki for answers.

## Trigger

When the user asks a question that might be answered by the Wiki.

## Workflow

1. **Start with the index** — Open `Wiki/index.md` for an overview.
2. **Search the catalog** — Run `python3 scripts/wiki_tool.py search-catalog --query "<user topic>"`.
3. **Open relevant Wiki notes** — Only the most relevant compiled notes.
4. **Open Raw sources only when needed** — When the compiled note is insufficient or the user asks for source-level verification.
5. **Cite your sources** — When the answer depends on source material, cite both the Wiki note and the Raw source.

## Rules

- Always search the catalog before opening Raw sources.
- Prefer compiled Wiki notes over Raw sources.
- Cite the compiled note and Raw source when the answer depends on source material.
- If no relevant Wiki note exists, say so — don't invent answers.
