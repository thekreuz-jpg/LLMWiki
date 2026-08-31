---
name: landing-page-prompt-generator
description: Use when user wants a random-style landing prompt.
category: creative
version: 1
author: Hermes (Arno / Kreuz)
license: MIT
metadata:
  hermes:
    tags: [creative, landing-page, design-prompt, random-style, copywriting]
    related_skills: [claude-design, popular-web-designs, sketch]
---

# Landing Page Prompt Generator

## When to Use
Use when the user asks to: generate a landing page prompt, create a design brief for a one-pager, explore or randomize a design style, or "make me a landing page concept prompt." Do NOT require them to name a style — you pick one at random (Step 1). Do not rename or repurpose this into a "build the page" skill unless the user explicitly wants the page built (see Step 3 extension).

## Core principle
The deliverable is a **prompt** — instructions for an AI or designer to then build the page — not the page itself. It must be EXACTLY THREE PARAGRAPHS, feeling-first, describing ONE cohesive single-page scrolling experience. Emphasize atmosphere, emotional arc, and abstract reference points. Never prescribe technical specs, frameworks, libraries, hex codes, or named brands inside the prompt.

## Step 1 — Select the style (your choice OR genuine randomization)
Two paths, decided by what you provide when triggering the skill:

1. **You name a style.** If your request mentions a style (e.g. "make a Bauhaus landing prompt" or
   "use Japandi"), use exactly that style. Do NOT randomize and do NOT overrule your pick — this is
   your explicit choice.

2. **You do not name a style.** Offer the choice explicitly with the `clarify` tool before writing
   the prompt:
   - Option A (recommended): "Surprise me — pick a random style"
   - Option B: "I'll choose the style" (you then name one via the auto-appended Other field)
   If you pick random (or don't engage), run the randomization code below.

The authoritative style list lives in `references/styles.md` (edit it in Obsidian to add, remove, or
retune styles — each style line: `- **Name** (short description)`). The file is organized into
`## Category` headings (e.g. "🎮 Nostalgic & Pop Culture"); categories are ignored by the picker —
only the `- **Name** (...)` lines matter. Read that file to (a) build the random pool and (b) recall
what each style represents when writing the prompt. Do NOT rely on a hardcoded list.

Do not default to a favorite (the source prompt explicitly bans defaulting to Neobrutalist). When
randomizing, pick genuinely at random from `references/styles.md` using a real random source each run:

```bash
python -c "import random,re; p=r'<SKILL_DIR>/references/styles.md'; t=open(p,encoding='utf-8').read(); s=re.findall(r'^- \*\*(.+?)\*\* \(',t,re.M); print(random.choice(s))"
```

(Replace `<SKILL_DIR>` with the skill's directory path, or read the file into context and pick from the
parsed names there.) You may substitute a *better-suited* professional style not on the list if you have
a strong, stated reason — but still choose it via a deliberate, non-defaulted decision, and say why.

After choosing, **state the path taken in one line before the prompt** so the run is self-documenting:
- You named it: `> Style selected by you: Japandi`
- Random draw: `> Random draw: Bauhaus`
- Better-suited substitution: `> Substituted: Mushin (zen flow) — reason: requested calm, focus-driven aesthetic not covered by listed styles`

## Step 2 — Write the three paragraphs
Follow this exact structure:

	**Paragraph 1 — Style + concept + feeling.** Name the chosen style(s). Ask the AI to conceive an innovative business/service concept for a SINGLE-PAGE landing page. Describe the core emotional qualities and the mood visitors should feel on arrival. Describe how visual hierarchy and flow should make them feel as they scroll one cohesive page. Include a note to weave in colorful elements as appropriate to the style to enhance emotional impact.
	
	**Paragraph 2 — Design philosophy through emotion/UX.** How should typography *feel* (authoritative, welcoming, cutting-edge)? What should interactions/animations *sense* like (smooth/liquid, snappy/precise, gentle/organic)? Describe how the single-page journey should emotionally progress from first impression → middle reveal → final call-to-action — a complete narrative arc in one scroll.
	
	**Paragraph 3 — Abstract reference points.** Capture the aesthetic's essence via the feeling of certain spaces, cultural movements, artistic periods, architectural styles, or design philosophies. Reference emotional qualities of premium experiences, sophisticated environments, or refined craftsmanship. Explain how these references should influence the emotional quality and visual sophistication of the final single-page design — without naming specific brands or platforms.

## Step 3 (optional extension) — Build it for real
If the user wants the page itself, take the generated prompt and produce a single self-contained `index.html` (inline CSS + minimal vanilla JS, no build step). Encode the chosen aesthetic via color tokens, type pairing, generous negative space, and gentle motion. Serve locally with `python -m http.server` and verify it renders. (In-session example: Japandi — warm oat/ash/linen canvas, terracotta/moss/indigo accents used sparingly, Cormorant Garamond + Mulish, slow-exhale cubic-bezier easing, IntersectionObserver reveals that settle, a drifting radial light, hand-drawn SVG vessel. Markup validated; server on 127.0.0.1.)

## Pitfalls
- Never name specific brands, products, or platforms inside the generated prompt.
- Keep it to exactly 3 paragraphs. Resist adding a fourth "technical notes" block inside the prompt   (put guidance in your chat reply, not the prompt).
- Don't let the randomization collapse into a habit — vary across runs; the ban on defaulting is real.
- The prompt is feeling-first; avoid prescribing hex codes, libraries, or exact layouts within it.

## Verification
- Output contains exactly 3 thematic paragraph blocks.
- A single, non-defaulted style is named up front.
- No brand names appear in the generated prompt.
- (If built) `index.html` is a single self-contained file and returns HTTP 200 from a local server.
