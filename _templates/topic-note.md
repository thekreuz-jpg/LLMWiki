# Topic Note Template

Use this template for new topic notes in `Wiki/Topics/`.

```markdown
---
tags:
  - "topic"
topics: []
status: seed
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
source_count: 0
aliases: []
---

# {{Title}}

## Overview

{{High-level overview of the topic}}

## Subtopics

- [[{{Subtopic 1}}]]
- [[{{Subtopic 2}}]]

## Key Concepts

- [[{{Concept 1}}]]
- [[{{Concept 2}}]]

## Sources

{{Links to source notes in Raw/Sources/}}
```

## Fields

| Field | Description |
|-------|-------------|
| `tags` | Must be `"topic"` |
| `topics` | Related topic paths |
| `status` | `seed`, `growing`, `mature`, or `archived` |
| `created` | Date the note was created |
| `updated` | Date the note was last updated |
| `sources` | Paths to source notes in `Raw/Sources/` |
| `source_count` | Must equal `len(sources)` |
| `aliases` | Alternative names for the note |
