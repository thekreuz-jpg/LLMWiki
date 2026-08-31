# HyperFrames Integration Walkthrough

Complete example of integrating the HyperFrames agent skills into Hermes.

## Repository

- **URL**: https://github.com/heygen-com/hyperframes
- **Stars**: 41.7k
- **Skills**: 20 agent skills for video creation
- **License**: Apache 2.0

## What is HyperFrames?

HyperFrames is an open-source framework for turning HTML, CSS, media, and seekable animations
into deterministic MP4 videos. Key components:

- **CLI**: `hyperframes` (install via `npm install -g hyperframes`)
- **Requirements**: Node.js 22+, FFmpeg
- **Skills**: 20 agent skills organized as:
  - `/hyperframes` — Entry point and intent router
  - Creation workflows (product-launch-video, faceless-explainer, pr-to-video, etc.)
  - Domain skills (hyperframes-core, hyperframes-animation, media-use, etc.)

## Installation Steps

### 1. Clone and Inspect

```bash
cd "$APPDATA/Local"
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/heygen-com/hyperframes.git hyperframes-repo
ls hyperframes-repo/skills/
```

### 2. Install CLI

```bash
npm install -g hyperframes
hyperframes --version  # Verify installation
```

### 3. Copy Skills to Hermes

```bash
cd hyperframes-repo/skills
for dir in */; do
  cp -r "$dir" "$APPDATA/Local/hermes/skills/"
done
```

### 4. Verify

```bash
# In Hermes, use skill_view to verify each skill loads
skill_view(name="hyperframes")
skill_view(name="product-launch-video")
```

## Notes

- HyperFrames also provides a `npx hyperframes skills update` command that installs to
  `~/.agents/skills/` and `~/.claude/skills/` for Claude Code/Cursor. This is separate from
  the manual Hermes integration.
- The CLI's `init` command auto-detects Hermes and installs skills to both locations.
- Skills installed manually are user-owned, not curator-managed.

## Example: Creating a Video

After installation, you can ask HyperFrames to create a video:

```
/hyperframes
Make me a 30-second video that explains how HyperFrames works.
```

The agent will run the full pipeline: init → write HTML → GSAP animations → render MP4.
