---
name: external-agent-skill-integration
description: >
  Add external agent skills to Hermes from GitHub repos.
---

# External Agent Skill Integration

External agent skills can be integrated into Hermes by copying them into the skills directory.
Covers evaluation, installation, and verification.

## When to Use

- User asks to install skills from a GitHub repo
- User wants capabilities from another agent ecosystem

## Workflow

### 1. Evaluate

Assess source credibility, scope, and maintenance status.

### 2. Clone and Inspect

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 <repo-url> <temp-dir>
ls <temp-dir>/skills/
```

### 3. Install

```bash
cp -r "<temp-dir>/skills/<skill-name>" "$APPDATA/Local/hermes/skills/"
```

### 4. Verify

Use `skill_view(name="<skill-name>")` to confirm the skill loads.

## Pitfalls

- Some installers copy to multiple agent directories
- Check for duplicate names before installing
- Installed skills are user-owned, not curator-managed
- Check `required_commands` and `required_environment_variables`
