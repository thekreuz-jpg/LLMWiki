# Build Spec — "Build It For Real"

Canonical structure for Step 3 of landing-page-prompt-generator when the user wants actual pages
instead of just prompts. Reuse this verbatim across builds so every page is consistent and
self-validating.

## Hard constraints
- ONE self-contained `index.html`. All CSS in `<style>`, all JS in `<script>`. NO build step, NO frameworks.
- Only external resource allowed: Google Fonts via `<link>`.
- Semantic, valid HTML5.

## Page structure (single scroll)
1. `<header>` fixed; JS adds class `settled` (bg + blur) once scrolled past the hero.
2. HERO — full-ish viewport, establishes mood. Eyebrow + H1 + lead + optional inline SVG/decor.
3. Philosophy / about section.
4. OFFER — what they get (pillars/cards, a quiet accent dot each).
5. Craft / trust section (a quote + supporting copy).
6. INVITATION — low-pressure CTA + front-end-only email form (on submit show a gentle
   confirmation message; no backend, no network).
7. `<footer>`.

## Motion & accessibility
- Reveal-on-scroll: give elements class `reveal` (start: translateY ~26px + opacity 0) and add
  `.in` when an IntersectionObserver fires; transition uses a slow-ease cubic-bezier
  (e.g. cubic-bezier(.16,1,.3,1)) over ~1.5s. Stagger with data-d attributes.
- `prefers-reduced-motion`: disable all animation/transition and force `.reveal` visible.
- Encode the aesthetic via CSS custom properties (color tokens) + a fitting Google-Fonts pairing.

## Validation (run before claiming success)
```python
from html.parser import HTMLParser
class V(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack=[]; s.void={'meta','link','br','hr','img','input','line','ellipse','path','stop','rect','circle','use','source','polygon','polyline'}; s.errors=[]
    def handle_starttag(s,t,a):
        if t not in s.void: s.stack.append(t)
    def handle_endtag(s,t):
        if t in s.void: return
        if s.stack and s.stack[-1]==t: s.stack.pop()
        elif t in s.stack:
            while s.stack and s.stack[-1]!=t: s.errors.append('unclosed '+s.stack.pop())
            if s.stack: s.stack.pop()
        else: s.errors.append('stray '+t)
path='index.html'
html=open(path,encoding='utf-8').read(); p=V(); p.feed(html)
assert html.lstrip().lower().startswith('<!doctype html>'), 'no doctype'
assert not p.stack and not p.errors, p.stack or p.errors
assert html.count('class="reveal') >= 1, 'no reveal elements'
print('PASS', len(html))
```

## Bulk builds (execute many prompts at once)
When the user says "build them all for real", dispatch parallel subagents (3 styles per agent)
sharing this BUILD SPEC + VALIDATION verbatim. Each agent writes
`C:/Users/Kreuz/landing-pages/<slug>/index.html` (slug = lower-case, hyphenated style name,
e.g. `retro-gaming`, `y2k-chrome`, `vintage-americana`). After all agents return, verify each file
exists and serve locally with `python -m http.server` to confirm HTTP 200.
