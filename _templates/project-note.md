# Project Note Template

Use this template for new project notes in `Wiki/Projects/`.

```markdown
---
tags:
  - "project"
topics: []
status: seed
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
source_count: 0
aliases: []
---

# {{Title}}

## Status

{{Active, completed, paused, etc.}}

## Description

{{Brief description of the project}}

## Goals

- {{Goal 1}}
- {{Goal 2}}

## Related Entities

- [[{{Entity 1}}]]
- [[{{Entity 2}}]]

## Sources

{{Links to source notes in Raw/Sources/}}
```

## Fields

| Field | Description |
|-------|-------------|
| `tags` | Must be `"project"` |
| `topics` | Related topic paths |
| `status` | `seed`, `growing`, `mature`, or `archived` |
| `created` | Date the note was created |
| `updated` | Date the note was last updated |
| `sources` | Paths to source notes in `Raw/Sources/` |
| `source_count` | Must equal `len(sources)` |
| `aliases` | Alternative names for the note |
