# Frontmatter Schema

## Source Notes (`Raw/Sources/`)

```yaml
---
Title: ""
Author: ""
Reference: ""
ContentType:
  - "markdown"
Created: YYYY-MM-DD
Processed: false
tags:
  - "source"
---
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `Title` | string | yes | Human-readable title of the source |
| `Author` | string | no | Author or creator |
| `Reference` | string | no | URL, DOI, or other reference identifier |
| `ContentType` | list | yes | Format of the source content |
| `Created` | date | yes | Date the source was created or published |
| `Processed` | boolean | yes | Whether this source has been compiled into Wiki notes |
| `tags` | list | yes | Must include `"source"` |

## Compiled Wiki Notes (`Wiki/`)

```yaml
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
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tags` | list | yes | One of: `topic`, `concept`, `entity`, `project`, `log` |
| `topics` | list | no | Related topic paths |
| `status` | string | yes | `seed`, `growing`, `mature`, `archived` |
| `created` | date | yes | Date the note was created |
| `updated` | date | yes | Date the note was last updated |
| `sources` | list | yes | Paths to source notes in `Raw/Sources/` |
| `source_count` | number | yes | Must equal `len(sources)` |
| `aliases` | list | no | Alternative names for the note |

### Allowed Tags

- `topic`
- `concept`
- `entity`
- `project`
- `log`
