---
name: hermes-agent-skill-authoring
description: 'Author in-repo SKILL.md files: frontmatter and structure.'
version: '1.0.0'
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, authoring, documentation]
    category: software-development
---

# Hermes Agent Skill Authoring

Write SKILL.md files to define reusable agent procedures.

## Core Structure

A skill is a single Markdown file (`SKILL.md`) with YAML frontmatter.

### Frontmatter

Required fields: `name`, `description`.

```yaml
---
name: your-skill-name
description: 'Short action-oriented summary (max 60 chars).'
version: '1.0.0'
author: Your Name
license: MIT
metadata:
  hermes:
    tags: [tag1, tag2]
    category: category-name
---
```

### Body

The Markdown body contains the instructions.

- **Use headers (`##`) to organize.**
- **Be direct.** Use imperative voice ("Do X", "Run Y").
- **Provide context.** Explain *why* a step is taken if it's not obvious.
- **Include examples.** Show expected inputs and outputs.
- **Keep it focused.** One skill per workflow.

## Best Practices

1. **Self-contained triggers:** Put the trigger condition in the first line of the description. (e.g., "Use when debugging Python.")
2. **Exact commands:** Provide the exact CLI commands or API calls.
3. **Pitfalls section:** Document known failure modes and how to fix them.
4. **Verification steps:** How does the agent know the task succeeded?

## Example

```yaml
---
name: verify-python-env
description: 'Use when a Python script fails with an import error. Checks venv.'
version: '1.0.0'
author: Hermes Agent
---

# Verify Python Environment

## Steps

1. Check if a virtual environment is active: `echo $VIRTUAL_ENV`
2. If empty, activate it: `source venv/bin/activate` (or equivalent).
3. If activation fails, create it: `python -m venv venv`.
4. Install requirements: `pip install -r requirements.txt`.

## Verification

Run `python -c "import <failing_module>"`. If it exits cleanly, the environment is ready.
```