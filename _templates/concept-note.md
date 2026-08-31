# Concept Note Template

Use this template for new concept notes in `Wiki/Concepts/`.

```markdown
---
tags:
  - "concept"
topics: []
status: seed
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
source_count: 0
aliases: []
---

# {{Title}}

## Definition

{{Concise definition of the concept}}

## Key Points

- {{Point 1}}
- {{Point 2}}

## Related Concepts

- [[{{Related Concept 1}}]]
- [[{{Related Concept 2}}]]

## Sources

{{Links to source notes in Raw/Sources/}}
```

## Fields

| Field | Description |
|-------|-------------|
| `tags` | Must be `"concept"` |
| `topics` | Related topic paths |
| `status` | `seed`, `growing`, `mature`, or `archived` |
| `created` | Date the note was created |
| `updated` | Date the note was last updated |
| `sources` | Paths to source notes in `Raw/Sources/` |
| `source_count` | Must equal `len(sources)` |
| `aliases` | Alternative names for the note |
