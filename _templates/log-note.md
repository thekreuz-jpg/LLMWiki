# Log Note Template

Use this template for new log notes in `Wiki/Logs/`.

```markdown
---
tags:
  - "log"
topics: []
status: seed
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
source_count: 0
aliases: []
---

# {{Title}}

## Date

{{YYYY-MM-DD}}

## Summary

{{Brief summary of the change or event}}

## Details

{{Detailed description of what changed}}

## Impact

{{What this change affects}}

## Sources

{{Links to source notes in Raw/Sources/}}
```

## Fields

| Field | Description |
|-------|-------------|
| `tags` | Must be `"log"` |
| `topics` | Related topic paths |
| `status` | `seed`, `growing`, `mature`, or `archived` |
| `created` | Date the note was created |
| `updated` | Date the note was last updated |
| `sources` | Paths to source notes in `Raw/Sources/` |
| `source_count` | Must equal `len(sources)` |
| `aliases` | Alternative names for the note |
