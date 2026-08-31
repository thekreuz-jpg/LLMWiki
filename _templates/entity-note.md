# Entity Note Template

Use this template for new entity notes in `Wiki/Entities/`.

```markdown
---
tags:
  - "entity"
topics: []
status: seed
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
source_count: 0
aliases: []
---

# {{Title}}

## Type

{{Person, place, organization, thing, etc.}}

## Description

{{Brief description of the entity}}

## Relationships

- **Related to:** [[{{Entity 2}}]]
- **Part of:** [[{{Parent Entity}}]]

## Sources

{{Links to source notes in Raw/Sources/}}
```

## Fields

| Field | Description |
|-------|-------------|
| `tags` | Must be `"entity"` |
| `topics` | Related topic paths |
| `status` | `seed`, `growing`, `mature`, or `archived` |
| `created` | Date the note was created |
| `updated` | Date the note was last updated |
| `sources` | Paths to source notes in `Raw/Sources/` |
| `source_count` | Must equal `len(sources)` |
| `aliases` | Alternative names for the note |
