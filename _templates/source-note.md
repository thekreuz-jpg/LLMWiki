# Source Note Template

Use this template for new source notes in `Raw/Sources/`.

```markdown
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

# {{Title}}

## Summary

{{Brief summary of the source}}

## Key Claims

- {{Claim 1}}
- {{Claim 2}}

## Notes

{{Additional notes for processing}}
```

## Fields

| Field | Description |
|-------|-------------|
| `Title` | Human-readable title of the source |
| `Author` | Author or creator |
| `Reference` | URL, DOI, or other reference identifier |
| `ContentType` | Format of the source content |
| `Created` | Date the source was created or published |
| `Processed` | Whether this source has been compiled into Wiki notes |
| `tags` | Must include `"source"` |
