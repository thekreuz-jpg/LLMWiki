# Naming Conventions

## File Names

- Use **kebab-case** for all file names: `my-topic-note.md`
- Avoid spaces, underscores, and special characters
- Keep names concise but descriptive

## Folder Structure

```
Raw/Sources/        ← source material
Raw/Files/          ← binary attachments (gitignored by default)
Wiki/Topics/        ← broad topic notes
Wiki/Concepts/      ← specific concept notes
Wiki/Entities/      ← people, places, things
Wiki/Projects/      ← project-related notes
Wiki/Logs/          ← changelog and maintenance logs
Schema/             ← rules and conventions
_templates/         ← note templates
.agents/skills/     ← agent skills
scripts/            ← deterministic tooling
tutorial/           ← tutorial step outputs
```

## Note Titles

- Use **Title Case** for note titles in frontmatter
- Keep titles descriptive and unique within the vault

## Tags

- Use **singular** form: `concept` not `concepts`
- Use **lowercase** for all tags
- Allowed compiled note tags: `topic`, `concept`, `entity`, `project`, `log`
- Source notes must include `source` tag

## Dates

- Use **ISO 8601** format: `YYYY-MM-DD`
- `Created` — when the note was first written
- `Updated` — when the note was last modified
